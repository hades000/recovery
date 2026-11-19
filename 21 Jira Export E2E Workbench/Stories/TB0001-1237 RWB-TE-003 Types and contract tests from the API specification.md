# TB0001-1237 [RWB-TE-003] Types and contract tests from the API specification

| Field | Value |
|---|---|
| Jira | [TB0001-1237](https://scbjira.atlassian.net/browse/TB0001-1237) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | thanapat khumprom |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-05T16:11:11.716+0700 |
| Updated | 2026-11-17T10:00:02.362+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 3 |
| Comments | 8 |

## Description

As a squad member (RW-TRIBE), I want server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint, so that the front end and the service never drift from the specification and no endpoint skips its access check.

## Acceptance criteria

```gherkin
Feature: Types and contract tests from the API specification

  Background:
    Given the build property rwb.release is "E1"
    Given operation getCasesCaseidTimers is first in E1 with capability Case record R

  Scenario: AC1 Types generated
    Given a change to the OpenAPI file that adds property "warnAt" to schema Timer
    When the build runs
    Then the generated server model and the front end type for Timer both hold "warnAt"
    Then the service and the front end compile against them

  Scenario: AC2 Contract broken
    Given the implementation of getCasesCaseidTimers returns "escalationLevel" as the text "two"
    When the contract tests run
    Then the build fails
    Then the report names getCasesCaseidTimers and the path "$[0].escalationLevel"

  Scenario: AC3 The specification is checked before generation
    Given an operation in the file with no x-capability
    When the build runs
    Then it fails at the lint step naming the operation

  Scenario: AC4 An undocumented status fails
    Given the implementation of getCasesCaseidTimers returns 400 for an unknown case
    Given the specification lists 200, 401, 403, 404 and 503 only
    When the contract tests run
    Then the build fails with "undocumented status 400" for getCasesCaseidTimers

  Scenario: AC5 A current operation with no implementation fails
    Given operation getAdminJobs is first in E1 and has no controller method
    When the build runs
    Then it fails with "getAdminJobs has no implementation"

  Scenario: AC6 A later operation is pending
    Given operation postQueuesQueueidPlacements is first in E2 and has no controller method
    When the build runs for release E1
    Then the build passes
    Then the report lists postQueuesQueueidPlacements as pending

  Scenario: AC7 The front end cannot use a removed field
    Given the file removes property "legalHold" from schema Case
    Given the case record screen reads "legalHold"
    When the front end build runs
    Then the type check fails naming the file and the line

  Scenario: AC8 An endpoint that skips its access check fails the build
    Given the implementation of getCasesCaseidTimers does not call the access check
    When the access tests run with role RW-REFADM, which holds no Case record right
    Then the operation answers 200
    Then the build fails with "access not enforced" for getCasesCaseidTimers
```

## Linked issues

- relates to TB0001-1349: [RWB-TE-003] Pipeline: run recovery contract checks on MRs into develop-recovery and develop, archive the report, allow new build dependencies (To Do)
- is blocked by TB0001-1449: [Issue] Request to create Jenkins pipeline for Workbench Recovery (Open)

## Sub-tasks

- TB0001-1297 [Done] [RWB-TE-003] Plan and task review — FDA plan approval, FDE task approval
- TB0001-1302 [Review] [RWB-TE-003] TASK-001 Generator compatibility proof (first task, CLAR-017)
- TB0001-1303 [Review] [RWB-TE-003] TASK-002 Validator, security-slice and client proof
- TB0001-1304 [Review] [RWB-TE-003] TASK-003 Pin dependencies, record ACE tech lead acknowledgement, post pinned coordinates
- TB0001-1305 [Review] [RWB-TE-003] TASK-004 RWB-TE-001 dependency gate
- TB0001-1306 [Review] [RWB-TE-003] TASK-005 Copy the API file unchanged
- TB0001-1307 [Review] [RWB-TE-003] TASK-006 Reference-list file
- TB0001-1308 [Review] [RWB-TE-003] TASK-007 Compile-path lint
- TB0001-1309 [Review] [RWB-TE-003] TASK-008 Unit tests for the lint
- TB0001-1310 [Review] [RWB-TE-003] TASK-009 Module pre-processor
- TB0001-1311 [Review] [RWB-TE-003] TASK-010 Unit tests for the pre-processor
- TB0001-1312 [Review] [RWB-TE-003] TASK-011 Server generation wiring
- TB0001-1313 [Review] [RWB-TE-003] TASK-012 Generation wiring verification
- TB0001-1314 [Review] [RWB-TE-003] TASK-013 Module map and boundaries
- TB0001-1315 [Review] [RWB-TE-003] TASK-014 Module-map check in the test task
- TB0001-1316 [Review] [RWB-TE-003] TASK-015 Unit tests for ModuleMapCheck
- TB0001-1317 [Review] [RWB-TE-003] TASK-016 OperationCatalog
- TB0001-1318 [Review] [RWB-TE-003] TASK-017 Unit tests for the catalog and generated structure
- TB0001-1319 [Review] [RWB-TE-003] TASK-018 Contract harness and RecoveryContractTest
- TB0001-1320 [Review] [RWB-TE-003] TASK-019 Unit tests for the contract harness
- TB0001-1321 [Review] [RWB-TE-003] TASK-020 Access harness and RecoveryAccessContractTest
- TB0001-1322 [Review] [RWB-TE-003] TASK-021 Unit tests for the access harness
- TB0001-1323 [Review] [RWB-TE-003] TASK-022 Fixtures and harness self-tests
- TB0001-1324 [Review] [RWB-TE-003] TASK-023 Report writer
- TB0001-1325 [Review] [RWB-TE-003] TASK-024 Unit tests for the report
- TB0001-1326 [Review] [RWB-TE-003] TASK-025 Generated-path guard
- TB0001-1327 [Review] [RWB-TE-003] TASK-026 Unit tests for the guard
- TB0001-1328 [Review] [RWB-TE-003] TASK-027 Front-end generation config
- TB0001-1329 [Review] [RWB-TE-003] TASK-028 Front-end verification
- TB0001-1330 [Review] [RWB-TE-003] TASK-029 Recovery JaCoCo tasks
- TB0001-1331 [Review] [RWB-TE-003] TASK-030 Privacy and security review
- TB0001-1332 [Review] [RWB-TE-003] TASK-031 Regression and image-build simulation
- TB0001-1333 [Review] [RWB-TE-003] TASK-032 Final coverage verification (80% gate)
- TB0001-1334 [Review] [RWB-TE-003] TASK-033 Coverage consolidation
- TB0001-1335 [Pending] [RWB-TE-003] TASK-034 Code-owner coverage gate
- TB0001-1336 [Review] [RWB-TE-003] TASK-035 Raise the pipeline Jira task (pipeline team)
- TB0001-1337 [Review] [RWB-TE-003] TASK-036 Merge request into ACE develop
- TB0001-1338 [To Do] [RWB-TE-003] TASK-037 E1 go-live control (Product Owner)
- TB0001-1339 [Review] [RWB-TE-003] TASK-038 Hand-over notes

## Comments (8)

### Comment 1: thanapat khumprom, 2026-11-10T11:56:01.918+0700

Comment ID 1782784

*Implementation sub-tasks created (2026-11-10)* — one per plan task of the approved plan (commit {{fd93eb7}}, [tasks.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/fd93eb7/recovery/output/INC-005-epic-1-RWB-TE-003/plan/tasks.md]). Each sub-task holds what to do, deliverable, done-when, blocked-by and trace. Labels {{RWB-TE-003}}, {{AISDLC}}; unassigned for distribution.

*Can start now:* TASK-001 (TB0001-1302) generator proof, then TASK-002, -005..-010, -027..-029; TASK-035 (TB0001-1336) pipeline request. *Gate:* TASK-004 (TB0001-1305) opens when RWB-TE-001 is merged in ACE {{develop}}; tasks marked "Yes" wait for it. The merge (TASK-036) also needs code owners from RWB-TE-002 (TB0001-1236).

||TASK||Jira||Title||Waits for RWB-TE-001||
|TASK-001|TB0001-1302|Generator compatibility proof|No|
|TASK-002|TB0001-1303|Validator, security-slice and client proof|No|
|TASK-003|TB0001-1304|Pin dependencies, ACE tech lead acknowledgement, post pinned coordinates|No|
|TASK-004|TB0001-1305|RWB-TE-001 dependency gate|Yes|
|TASK-005|TB0001-1306|Copy the API file unchanged|No|
|TASK-006|TB0001-1307|Reference-list file|No|
|TASK-007|TB0001-1308|Compile-path lint|No|
|TASK-008|TB0001-1309|Unit tests for the lint|No|
|TASK-009|TB0001-1310|Module pre-processor|No|
|TASK-010|TB0001-1311|Unit tests for the pre-processor|No|
|TASK-011|TB0001-1312|Server generation wiring|Yes|
|TASK-012|TB0001-1313|Generation wiring verification|Yes|
|TASK-013|TB0001-1314|Module map and boundaries|Yes|
|TASK-014|TB0001-1315|Module-map check in the test task|Yes|
|TASK-015|TB0001-1316|Unit tests for ModuleMapCheck|Yes|
|TASK-016|TB0001-1317|OperationCatalog|Yes|
|TASK-017|TB0001-1318|Unit tests for the catalog and generated structure|Yes|
|TASK-018|TB0001-1319|Contract harness and RecoveryContractTest|Yes|
|TASK-019|TB0001-1320|Unit tests for the contract harness|Yes|
|TASK-020|TB0001-1321|Access harness and RecoveryAccessContractTest|Yes|
|TASK-021|TB0001-1322|Unit tests for the access harness|Yes|
|TASK-022|TB0001-1323|Fixtures and harness self-tests|Yes|
|TASK-023|TB0001-1324|Report writer|Yes|
|TASK-024|TB0001-1325|Unit tests for the report|Yes|
|TASK-025|TB0001-1326|Generated-path guard|Yes|
|TASK-026|TB0001-1327|Unit tests for the guard|Yes|
|TASK-027|TB0001-1328|Front-end generation config|No|
|TASK-028|TB0001-1329|Front-end verification|No|
|TASK-029|TB0001-1330|Recovery JaCoCo tasks|No|
|TASK-030|TB0001-1331|Privacy and security review|Yes|
|TASK-031|TB0001-1332|Regression and image-build simulation|Yes|
|TASK-032|TB0001-1333|Final coverage verification (80% gate)|Yes|
|TASK-033|TB0001-1334|Coverage consolidation|Yes|
|TASK-034|TB0001-1335|Code-owner coverage gate|No (needs RWB-TE-002)|
|TASK-035|TB0001-1336|Raise the pipeline Jira task|No|
|TASK-036|TB0001-1337|Merge request into ACE develop|Yes|
|TASK-037|TB0001-1338|E1 go-live control (Product Owner)|Yes|
|TASK-038|TB0001-1339|Hand-over notes|Yes|

Plan review / approval: TB0001-1297.

### Comment 2: thanapat khumprom, 2026-11-10T13:55:06.713+0700

Comment ID 1783063

@Jesniphat Pukkham

h3. ขออนุมัติ: บันทึกข้อตกลงของ RWB-TE-003 ลง decisions file (OPEN-029)

ก่อนเริ่ม implement RWB-TE-003 ต้องบันทึกข้อตกลงที่ plan ใช้ (approved version {{fd93eb7}}) ลงไฟล์ {{recovery/docs/decisions/INC-001-decisions.md}} ให้ตรงกันก่อน ผมร่างข้อความไว้ 4 ข้อด้านล่าง รบกวนตอบรายข้อใน thread นี้ครับ

h4. ข้อควรรู้ก่อน: เลข D-RCV ชนกับ main

* branch ของ TE-003 ({{spec/INC-005-te-003-attempt-02}}) แยกออกมาก่อนที่ {{main}} จะเปลี่ยนการนับเลข
* บน {{main}} เลข D-RCV-29..33 เป็น ruling ของ BA (Decision Log v8) ส่วน D-RCV-34..49 เป็นของ squad เลขว่างถัดไปคือ D-RCV-50
* ข้อตกลง 5 ข้อของ TE-003 ที่ branch ใช้เลข D-RCV-31..35 ยังไม่มีบน {{main}} จึงขอเลขใหม่ตามนี้:
* D-RCV-31 → *D-RCV-50*: ที่อยู่ไฟล์ API spec ใน ACE ({{backend/src/main/resources/recovery/api/recovery-api.yaml}})
* D-RCV-32 → *D-RCV-51*: วิธี generate server code (แก้ข้อความ ดูข้อ 4)
* D-RCV-33 → *D-RCV-52*: contract test และ access test รันใน Gradle {{test}} ไม่ใช้ database
* D-RCV-34 → *D-RCV-53*: pipeline เป็น Jenkins ของอีกทีม ขอเปลี่ยนผ่าน Jira task
* D-RCV-35 → *D-RCV-54*: test ครอบทุก operation ที่ implement แล้ว ตัวที่ยังไม่ทำเป็น pending และไม่ทำให้ build fail
* ข้อตกลงใหม่ → *D-RCV-55*: ข้อยกเว้นในข้อ 2
* ถ้ามีคนใช้ D-RCV-50 ขึ้นไปก่อนบันทึก จะเลื่อนเป็นเลขว่างถัดไปตามลำดับเดิม

h4. ข้อ 1: ขยาย D-RCV-15 ให้ครอบ INC-005

ตอนนี้ D-RCV-15 ให้คุณอนุมัติ gate FDE/FDA ได้เฉพาะ EPIC-001, INC-001 และ INC-002 แต่ plan ของ TE-003 ใช้คุณอนุมัติไปแล้ว ({{TB0001-1297}}) เสนอแก้เป็น:

{noformat}Jesniphat Pukkham approves the FDE/FDA gates (context readiness, design and architecture, plan, task, PR, release readiness) for EPIC-001, INC-001, INC-002 and INC-005 (RWB-TE-003) on behalf of the squad. Product Owner gates (intake, requirements, backlog and specification, deployment) stay with the Product Owner.
Recorded in: EPIC-001, INC-001, INC-002, INC-005 cards{noformat}

h4. ข้อ 2: ข้อยกเว้นกฎ ACE "normal test + e2e test" สำหรับ RWB-TE-003 (D-RCV-55)

{noformat}RWB-TE-003 only: exception to the ACE rule "write both a normal test and an e2e test before an MR" (ace-monorepo docs/coding-standard.md, Testing). The story adds no endpoint and no screen, so there is nothing for an e2e test to drive; the evidence is its unit tests, the contract test and the access test. Approved by Jesniphat Pukkham as FDA, 2026-11-10.
Closes: RWB-TE-003 OPEN-027 (plan AC-PLAN-06)
Confirm with: ACE tech lead (inform)
Recorded in: INC-005 card; backend-standards (through the Context Updater){noformat}

h4. ข้อ 3: ใครคือ ACE tech lead

plan ของ TE-003 บันทึกว่าคุณเป็น ACE tech lead (คุณ Thanapat แจ้งเมื่อ 10 พ.ย. 2026 โดยส่งต่อคำยืนยันของคุณ) และใช้ข้อนี้ปิดเรื่องการรับทราบ dependency ใหม่และไฟล์ shared ของ ACE (plan §6, §7) แต่บันทึกบน {{main}} เขียนต่างออกไป:

* OPEN-028 บน {{main}}: "Pipat Saengow (ACE tech lead)"
* OPEN-023 บน {{main}}: dependency ใหม่ของ RWB-TE-001 อนุมัติโดยคุณ Pongchai Charoenrungrodkun (ACE and Recovery lead) ใน {{TB0001-1235}}

รบกวนเลือก (a) หรือ (b):

* (a) คุณเป็น ACE tech lead: ช่วยยืนยันเป็นลายลักษณ์อักษร และบอกว่ารับทราบ D-RCV-01..07, -10, -11, -13 และ ADR-RCV-001 (ข้อที่คอลัมน์ "Confirm with" เขียนว่า ACE tech lead) หรือบอกข้อที่ยังไม่รับทราบ
* (b) ACE tech lead เป็นคนอื่น: บอกชื่อ แล้ว TE-003 จะขออนุมัติ dependency ใหม่และไฟล์ shared จากคนนั้นก่อน merge เหมือนที่ RWB-TE-001 ทำ (OPEN-023)

dependency ใหม่ของ TE-003: OpenAPI generator Gradle plugin {{org.openapi.generator}}, validator {{com.atlassian.oai:swagger-request-validator-mockmvc}} (ตัวสำรอง {{com.networknt:json-schema-validator}}), JaCoCo และ npm {{openapi-fetch}} ไฟล์ shared ที่แก้: {{backend/build.gradle.kts}}, {{backend/gradle.properties}}, checkstyle suppression, {{backend/package.json}}, {{frontend/package.json}}, lockfiles และไฟล์ ignore ของ front-end

h4. ข้อ 4: แก้ข้อความ D-RCV-32 (เลขใหม่ D-RCV-51)

ข้อความเดิมเขียนว่า "one interface set per {{x-module}} (not per tag)" แต่ plan ที่อนุมัติแล้วสร้าง 1 interface ต่อ operation ภายในชุดของแต่ละ module (PD-04, PD-05) เพื่อให้ API ที่ยังไม่มีคนทำไม่มี route เสนอข้อความใหม่:

{noformat}Server code is generated from the API specification per x-module: a hand-written pre-processing step writes one build copy of the file per x-module, and the generator writes one interface per operation (for example GetCasesCaseidTimersApi) into that module's package under th.co.scb.ace.demo.recovery; models go in one shared package. An operation with no controller has no route and is reported pending. Approved by Jesniphat Pukkham, recovery tech lead, 2026-11-09 (relayed by Thanapat K.); wording updated to the RWB-TE-003 plan (PD-04, PD-05) on 2026-11-10.{noformat}

h4. วิธีตอบ

{noformat}ข้อ 1: อนุมัติ
ข้อ 2: อนุมัติ
ข้อ 3: (a) ยืนยัน และรับทราบทุกข้อ / (b) ACE tech lead คือ ...
ข้อ 4: อนุมัติเลขใหม่ D-RCV-50..55 และข้อความ D-RCV-51{noformat}

ถ้าอยากแก้ถ้อยคำข้อไหน เขียนแก้มาได้เลยครับ หลังได้คำตอบ ผมจะบันทึกลง decisions file ตามนั้น

ขอบคุณครับ
Thanapat K.

### Comment 3: Jesniphat Pukkham, 2026-11-10T14:17:45.634+0700

Comment ID 1783157

@thanapat khumprom 

{{ข้อ 1: อนุมัติ ข้อ 2: อนุมัติ ข้อ 3: (a) ยืนยัน และรับทราบทุกข้อ ข้อ 4: อนุมัติเลขใหม่ D-RCV-50..55 และข้อความ D-RCV-51}}

### Comment 4: thanapat khumprom, 2026-11-12T13:02:23.258+0700

Comment ID 1787333

h3. RWB-TE-003: confirmations needed before MR !295 is merged (12 Nov 2026)

RWB-TE-003 is implemented on ACE branch {{feature/TB0001-1237-api-contract-tests}}. It is open as Draft [MR !295|https://gitdop.se.scb.co.th/AP2477-ACE/ace-monorepo/-/merge_requests/295] into {{develop-recovery}}, head {{5ae9ebb2}}. The backend gate passes: 1260 tests, 0 failed, recovery coverage at least 80 % (rules R1 and R2), bootJar OK. The MR has no conflict with {{develop-recovery}} {{d539fc0f}}.

The items below need a named answer. Please reply in this ticket. Code-gate review run 2 starts once C1 and C2 are answered.

*C1. Approve plan deviations DV-12 and DV-13. For: recovery tech lead and plan approver (Jesniphat Pukkham)*

* DV-12, package move. {{develop-recovery}} {{d539fc0f}} (MR !300, TB0001-1372, D-RCV-59) moved the recovery root to {{th.co.scb.ace.workbench.recovery}}. RWB-TE-003 follows it:
** test support: {{th.co.scb.ace.workbench.recovery.apicontract}}
** generated interfaces and models: {{th.co.scb.ace.workbench.recovery.<module>.internal.web.generated}}
* DV-12, build file. {{backend/build.gradle.kts}} keeps the JaCoCo tasks exactly as you restored them on {{develop-recovery}}. It adds only the RWB-TE-003 part: the generated code is left out of coverage, the contract-support and API-tooling classes are measured, and rule R2 checks each RWB-TE-003 package at 80 %. The JaCoCo setup that MR !295 had put back itself is removed, so OPEN-047 is closed as option (b).
* DV-13, tooling location. The lint and the module grouper moved from {{src/recoveryApiTooling/java}} (package {{th.co.scb.ace.recoverytooling.apicontract}}) into {{backend/src/main/java/th/co/scb/ace/workbench/recovery/integration/internal/apitooling/}}.
** They are still compiled on their own (source set {{recoveryApiTooling}}), before {{compileJava}}, because they feed the generators. They are not in the application jar.
** The source set points at the package folder, not at {{src/main/java}}. When it pointed at {{src/main/java}}, the OpenRewrite plugin disabled its compile task.
* For information: DV-14 is a set of fixes from a re-check against the spec and plan. They harden the contract harness and change no scope. Details are in the AISDLC file {{plan-spec-recheck.md}}.

Question: do you approve DV-12 and DV-13 as plan amendments? If not, please say what to change.

*C2. Confirm the TASK-031 acceptance (TB0001-1332). For: FDE (Jesniphat Pukkham)*

On 11 Nov 2026 the squad BA accepted TASK-031 (regression and image-build check). The image-build step is left to the normal Jenkins build after merge (HV-08), because this workstation cannot reach the SCB proxy. Step 5 of BV-04 no longer applies: {{backend/Dockerfile}} was removed upstream in {{develop-recovery}} {{5fb90334}}.

Question: do you confirm the acceptance (code-gate finding REVIEW-C-05)?

*C3. Person with no Workbench role: 401 or 403? (OPEN-050) For: Product Owner, with RW-SECADM and the RWB-E1-037 owner*

For a signed-in person who holds no Workbench role, the specification (CLAR-012) expects 403 with message MSG-P4-002. The API file's {{E401}} response says the opposite: "No valid session, or the person holds no Workbench role", which is 401 with MSG-P4-001.

Five E1 operations declare both responses: {{getAdminListsListcode}}, {{getAdminTrackers}}, {{getAdminTrackersRetirementReport}}, {{getAdminDataDictionaryFields}} and {{getAdminDataContracts}}.

Question: which status and message should this person get? We then align either the specification or the API file; a change to the API file needs approval by the TechX tech leads.

Needed by: before the access test is switched on ({{rwb.accessMatrixRequired=true}}, RWB-E1-037).

*C4. Front-end type check (OPEN-051). For: ACE front-end owner, with the recovery tech lead*

SPEC-005 says a type error against the generated API types fails the build. On the front end this is not true yet:

* the nx {{typecheck}} target only prints a message ({{echo}}), and {{skipLibCheck}} is on;
* a real {{tsc -p tsconfig.app.json}} reports 5 errors (TS2554) that already exist in {{DateInput.tsx}}.

The back-end half of SPEC-005 is met.

Question: who makes the front-end type check real, and when?

Needed by: before the first recovery screen is merged (together with OPEN-036).

*C5. develop-recovery lockfile (OPEN-049). For: owner of develop-recovery (Jesniphat Pukkham)*

{{npm ci}} fails on {{develop-recovery}} itself, at {{5fb90334}} and at {{d539fc0f}}, with or without MR !295. The root {{package-lock.json}} is out of sync with {{package.json}} ({{Missing: vitest@4.1.12 from lock file}}, {{Missing: @vitest/coverage-v8@4.1.12 from lock file}}). Until it is fixed, the front-end checks of MR !295 ({{nx affected -t check}}) cannot run. They passed before the merge, 46 of 46 tasks at {{553913ad}}.

Question: please fix the lockfile on {{develop-recovery}}, or name an owner and a date.

Needed by: before MR !295 is merged.

*C6. Code owners (OPEN-042, RWB-TE-002). For: recovery tech lead (Jesniphat Pukkham)*

ACE has no code-owners file, so code-owner coverage of the RWB-TE-003 paths cannot pass (TASK-034, TB0001-1335).

Question: when will the code-owners file come (RWB-TE-002), and who approves MR !295 as code owner until then?

Needed by: before MR !295 is merged.

*C7. Merge-request pipeline (TB0001-1349). For: recovery tech lead, to route to the pipeline team*

The GitLab {{test}} job does not run for merge requests into {{develop-recovery}}: the MR !295 pipeline shows "skipped". The pipeline request TB0001-1349, with pinned versions, has no assignee yet.

Question: who takes TB0001-1349?

Needed by: before MR !295 is merged.

Evidence (AISDLC repository, branch {{spec/INC-005-te-003-attempt-02}}, folder {{recovery/output/INC-005-epic-1-RWB-TE-003/implement/}}): {{implementation-summary.md}} (DV-12 to DV-14), {{plan-spec-recheck.md}}, {{ace-mr.md}}, {{build-verification.md}}, {{unit-tests/report.md}}. Open items: {{recovery/docs/open-items.md}} (OPEN-042, OPEN-049, OPEN-050, OPEN-051).

### Comment 5: Jesniphat Pukkham, 2026-11-12T13:22:56.705+0700, edited 2026-11-12T13:26:32.057+0700

Comment ID 1787386

@thanapat khumprom 
RWB-TE-003 / MR !295: answers from the recovery tech lead (12 Nov 2026)

C1. Approved. DV-12 (package move to th.co.scb.ace.workbench.recovery per D-RCV-59, and the build-file change that keeps the restored JaCoCo tasks and adds only the RWB-TE-003 part; OPEN-047 closed as (b)) and DV-13 (tooling in backend/src/main/java/.../integration/internal/apitooling, compiled as its own source set recoveryApiTooling, not in the application jar) are approved as plan amendments. DV-14 noted.

C2. Confirmed as FDE. TASK-031 (TB0001-1332) is accepted; the image-build check moves to the Jenkins build after merge (HV-08), and BV-04 step 5 no longer applies because backend/Dockerfile was removed in develop-recovery 5fb90334. REVIEW-C-05 can be closed on this basis.

C3. For the Product Owner. My technical recommendation: a signed-in person with no Workbench role gets 403 / MSG-P4-002, as in the spec (CLAR-012). 401 / MSG-P4-001 stays for "no valid session" only. If the PO agrees, the E401 description in the API file is corrected for the five E1 operations, with TechX tech-lead approval. Not blocking MR !295; needed before rwb.accessMatrixRequired=true.

C4. Not blocking MR !295. I will raise it with the ACE front-end owner; target is before the first recovery screen is merged (with OPEN-036). Until then the back-end half of SPEC-005 is the gate.

C5. I take it. The root package-lock.json on develop-recovery will be regenerated to match frontend/package.json (vitest and @vitest/coverage-v8 at 4.1.12), before MR !295 is merged. The mismatch came in with the develop merge 5fb90334.

C6. Until RWB-TE-002 delivers the code-owners file, I approve MR !295 as interim code owner (recovery tech lead, D-RCV-15, D-RCV-50). ACE reviews the shared-file changes in the develop-recovery to develop batch MR.

C7. I take TB0001-1349 and will route it to the pipeline team.

Code-gate review run 2 can start.

### Comment 6: thanapat khumprom, 2026-11-12T15:36:28.015+0700

Comment ID 1787828

h3. RWB-TE-003: decision needed on hand-written recovery controllers (code-gate review REVIEW-C-16, 12 Nov 2026)

*For:* Jesniphat Pukkham (recovery tech lead), with the RWB-E1-042 owner (TB0001-1203)
*Needed by:* before MR !295 is merged

*What changed.* At 13:38 today develop-recovery moved to ac921bf8 (merge of RWB-E1-042). It brings the first recovery controller, {{ReferenceLoadController}} in module {{access}}. It serves three E1 operations of the API file:

* {{postAdminReferenceLoads}} (POST /recovery/v1/admin/reference-loads)
* {{postAdminReferenceLoadsLoadidApprove}} (…/{loadId}/approve)
* {{postAdminReferenceLoadsLoadidRollback}} (…/{loadId}/rollback)

The controller is hand-written. It does not implement the generated interfaces of MR !295 ({{PostAdminReferenceLoadsApi}} and the other two, package {{th.co.scb.ace.workbench.recovery.access.internal.web.generated}}). They do not exist on develop-recovery yet.

*Effect once MR !295 is merged with ac921bf8.* We read this from the code and have not run it yet. MR !295 must first be merged with ac921bf8 anyway (REVIEW-C-15: conflict in backend/build.gradle.kts).

# The contract and access tests are expected to fail at start. The test slice loads every recovery controller, but it has no stand-in for {{ReferenceLoadService}}, {{RecoveryCaller}} or {{recoveryCapabilities}}.
# If the slice is made to start, the three operations are reported {{PENDING}} ("not implemented"), although they are live. Their response contract and their permission check ({{REFERENCE_DATA}} C, A, U) are then not tested, and no test flags this.

*Question 1. How do hand-written recovery controllers come under the contract?*

* (a) Each recovery controller implements the generated interface of each operation it serves (PD-05, the RWB-TE-003 convention). {{ReferenceLoadController}} implements the three interfaces and gets a contract fixture with stand-ins for its services. This is a follow-up on RWB-E1-042 after MR !295 is merged.
* (b) The harness counts an operation as implemented when any controller serves its route, whether or not it implements the generated interface. This changes the RWB-TE-003 spec and plan and needs your approval as a plan amendment.

The review proposes (a): it keeps one rule for every story and matches PD-05.

*Question 2. If (a): what happens until the controller is changed?*
In both cases RWB-TE-003 adds a check: a recovery controller that serves an API-file route without implementing its generated interface is reported by name. The slice loads only controllers it can start.

* (i) The check fails the build. Then MR !295 must also change {{ReferenceLoadController}}, which is RWB-E1-042 code, or develop-recovery stays red until the follow-up is merged.
* (ii) The check fails the build except for a named, temporary list of these three operations, with the follow-up ticket key. The report shows them as "not under contract" instead of {{PENDING}}. The list is removed when the follow-up is merged.

*Question 3. Who does the follow-up, and by when?* Please give an owner and a ticket. We will record the decision as a new D-RCV at the next free number.

Note: {{postAdminReferenceLoadsLoadidVerify}} (…/{loadId}/verify) is not in the controller. It stays {{PENDING}} as an operation that is not built yet.

Evidence (AISDLC repository, folder recovery/output/INC-005-epic-1-RWB-TE-003/review/): code-gate-review.md, run 2, findings REVIEW-C-15 and REVIEW-C-16.

### Comment 7: Jesniphat Pukkham, 2026-11-13T09:52:58.725+0700

Comment ID 1789071

@thanapat khumprom 1. a, 2. I, 3. Thanapat Khumprom

### Comment 8: Jesniphat Pukkham, 2026-11-16T16:58:11.217+0700

Comment ID 1793103

Waiting for create jenkins pipeline build and deploy new microservice and dbmigration.


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
| Created Date | customfield_10249 | 2026-11-05 |
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
