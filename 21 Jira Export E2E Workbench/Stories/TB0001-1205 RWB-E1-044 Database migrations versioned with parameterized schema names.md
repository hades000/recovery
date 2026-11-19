# TB0001-1205 [RWB-E1-044] Database migrations versioned with parameterized schema names

| Field | Value |
|---|---|
| Jira | [TB0001-1205](https://scbjira.atlassian.net/browse/TB0001-1205) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | THAMMASAK JUKCHAN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2; Delivery Workbench Q4S2 Squad2 |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:42.182+0700 |
| Updated | 2026-11-17T09:59:51.398+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 6 |
| Comments | 11 |

## Description

As a platform administrator (RW-PLATADM), I want every schema change applied by a versioned Flyway migration, one migration per story, forward-only in PROD, with the schema name taken from a parameter, so that the database in every environment is the sum of known migrations and nothing else.

## Acceptance criteria

```gherkin
Feature: Database migrations versioned with parameterized schema names

  Background:
    Given the schema parameter RWB_SCHEMA is "rwb_case"
    Given the Flyway history table is "flyway_schema_history_recovery"

  Scenario: AC1 Migration applied
    Given migration V12__add_queue_to_case.sql with the header "-- Story: RWB-E1-020"
    When the deployment runs
    Then the migration applies once
    Then its version 12 and its checksum are recorded in "flyway_schema_history_recovery"
    Then a second deployment run applies nothing and changes no object

  Scenario: AC2 Drift detected
    Given a column "note_x" added by hand to table "queue" in SIT
    When the migration check runs
    Then the pipeline fails with MSG-P3-016 naming "rwb_case.queue.note_x"
    Then no deployment to SIT starts

  Scenario: AC3 Schema name as parameter
    Given RWB_SCHEMA set to "rwb_case" in DEV and in SIT
    When the migration V13__create_timer.sql runs in DEV and in SIT
    Then the table "timer" exists in schema "rwb_case" in both environments
    Then the file V13__create_timer.sql is byte for byte the same in both runs

  Scenario: AC4 Applied migration edited
    Given V12__add_queue_to_case.sql applied in SIT with checksum 104553219
    Given the file changed in the repository so its checksum is 88120477
    When the service starts in SIT
    Then Flyway validation fails with MSG-P3-016 naming version 12
    Then the service does not start

  Scenario: AC5 Literal schema name
    Given V14__add_index.sql contains the text "CREATE INDEX ix_a ON recovery.queue (team_code)"
    When the migration lint runs
    Then the build fails with MSG-P3-016 naming V14__add_index.sql line 1

  Scenario: AC6 One migration per story
    Given V15__a.sql and V16__b.sql both carry the header "-- Story: RWB-E1-028"
    When the migration lint runs
    Then the build fails with MSG-P3-016 naming both files and RWB-E1-028

  Scenario: AC7 Forward only in PROD
    Given the PROD configuration
    When a pipeline step calls Flyway clean or an undo migration U12__add_queue_to_case.sql is present
    Then the system refuses the step with MSG-P3-016
    Then no object in PROD changes

  Scenario: AC8 Migration fails part way
    Given V17__add_two_columns.sql whose second statement refers to a table that does not exist
    When the deployment runs in DEV
    Then the system rolls the first statement back
    Then the history records version 17 as failed
    Then the service does not start and the run shows "failed" on the job monitor

  Scenario: AC9 Two instances start together
    Given two service instances in SIT with migration V18__add_column.sql pending
    When both start within one second
    Then the system applies V18 exactly once
    Then both instances start
```

## Linked issues

- blocks TB0001-1357: [RWB-E1-001] BE - Migration, seeds and dictionary conformance (TASK-02..06, 12) (To Do)
- blocks TB0001-1359: [RWB-E1-001] BE - Authorisation and release readiness (TASK-15, 17) (To Do)
- is blocked by TB0001-1449: [Issue] Request to create Jenkins pipeline for Workbench Recovery (Open)

## Sub-tasks

- TB0001-1340 [To Do] [RWB-E1-044] BE - Recovery Flyway bean, local-start initializer and migrate-and-exit runner
- TB0001-1341 [To Do] [RWB-E1-044] BE - Unit tests and migration lint
- TB0001-1342 [To Do] [RWB-E1-044] BE - Container tests and coverage gates
- TB0001-1343 [To Do] [RWB-E1-044] Evidence, ACE MR and traceability

## Attachments

- [RWB-E1-044-spec-20261109.md](../../Attachments/TB0001-1205/RWB-E1-044-spec-20261109.md) (37670 bytes, Jesniphat Pukkham, 2026-11-09T11:51:27.477+0700)
- [RWB-E1-044-spec-20261109-r2.md](../../Attachments/TB0001-1205/RWB-E1-044-spec-20261109-r2.md) (46049 bytes, Jesniphat Pukkham, 2026-11-09T16:25:03.304+0700)
- [RWB-E1-044-spec-20261110-r4.md](../../Attachments/TB0001-1205/RWB-E1-044-spec-20261110-r4.md) (62031 bytes, Jesniphat Pukkham, 2026-11-10T12:04:21.367+0700)

## Comments (11)

### Comment 1: Jesniphat Pukkham, 2026-11-09T11:05:53.802+0700

Comment ID 1780540

@RAJ GHAI

*Product Owner decision needed: RWB-E1-044 Database migrations versioned with parameterized schema names*

Hi Raj,

We have re-specified RWB-E1-044 on the latest BA package (9 Nov 2026). All technical questions are closed. Two scope questions are left, and they need a Product Owner decision. The specification stays blocked until we have your answer.

Spec: [https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-001-epic-1-RWB-E1-044/specify/spec.md|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-001-epic-1-RWB-E1-044/specify/spec.md] (section "Clarification Log")

*CLAR-001: BR7 drift check before every deployment to SIT, UAT and PROD*

The story asks the pipeline to compare each target environment with a clean database before deployment, with a read-only account and the flag {{rwb.p3.migration-drift-gate}}. Squad decision D-RCV-05 parks this, because it needs a pipeline change.

* *A (recommended):* Park the real-environment gate. For this story, BR7 is accepted on the container comparison test (T-044-02), which runs in the build. No flag and no read-only account in this story. The gate stays in the parking list.
* *B:* Keep the gate in this story. This needs a Jenkins change, a read-only account per environment and the flag, and the story will take longer.

*CLAR-002: Migration run record and job monitor*

The story includes {{MigrationRunRecorder}}, {{GET /api/recovery/v1/admin/jobs?type=MIGRATION}}, the SCR-44 job monitor view and test TC-E1-044-10. These depend on the P1 job store, which does not exist yet. Squad decision D-RCV-12 defers them.

* *A (recommended):* Defer these to the story that builds the job monitor. Until then, the migration result is visible in the Flyway history table and the Jenkins log.
* *B:* Keep them in this story. The P1 job store must be built first, so RWB-E1-044 will depend on that story.

*Please reply in this thread* with your choice for each item, for example:

{quote}CLAR-001: A. CLAR-002: A.{quote}

After your answer we will finish the specification and run the compliance gate, then ask you to approve the specification (Backlog and specification gate). We will ask the BA to align the story text with your decision.

Thanks,

Jesniphat Pukkham, Recovery tech lead

### Comment 2: Chitchaya Muanchonchana, 2026-11-09T15:19:10.853+0700

Comment ID 1781236

@Jesniphat Pukkham As a Internal PO TechX. The will apply this ticket follow the scope as AI recommend. CLAR-001: A. CLAR-002: A. 

@CHANISSARA MAHAKITTIKUN  If you have any issue or concern please raise the change in new story to apply later.

### Comment 3: Jesniphat Pukkham, 2026-11-09T16:25:27.393+0700

Comment ID 1781484

@Chitchaya Muanchonchana

*RWB-E1-044: one correction, then specification approval*

Hi Chitchaya, thank you for the answers (CLAR-001: A, CLAR-002: A). They are now in the specification.

*Correction to my earlier question (CLAR-001)*

I wrote that the container comparison test T-044-02 "runs in the build". That was not accurate. Recovery container tests need Docker, so they run in a separate task ({{recoveryIntegrationTest}}), not in the CI build that every merge runs. The rule we set (D-RCV-44):

* T-044-02 and the other recovery container tests *must run before every merge request* that changes recovery migrations or the recovery Flyway setup, and the result is attached to the merge request evidence.
* They move into CI once we confirm the build agents have Docker (asked separately).
* The real drift gate against SIT, UAT and PROD stays parked, as you approved.

*Please confirm two things in this thread:*

# BR7 is accepted for this story through T-044-02 run before every merge request (OPEN-027).
# You approve the RWB-E1-044 specification (Backlog and specification gate).

The updated specification is attached: {{RWB-E1-044-spec-20261109-r2.md}}. Compliance review: no Critical, High or Medium findings.

Example reply:

{quote}Confirmed BR7 via T-044-02 before every MR. Approved: RWB-E1-044 specification.{quote}

Thanks,

Jesniphat Pukkham, Recovery tech lead

### Comment 4: Jesniphat Pukkham, 2026-11-09T16:25:27.900+0700, edited 2026-11-09T17:15:16.378+0700

Comment ID 1781485

@PONGCHAI CHAROENRUNGRODKUN cc: @PIPAT SAENGOW

*RWB-E1-044: ขอข้อมูล/ยืนยัน 3 เรื่องจากฝั่ง ACE*

ระหว่างทำ spec ของ RWB-E1-044 บน ACE develop ล่าสุด ({{eedf5c75}}) เจอ 3 เรื่องที่อยากให้พี่ช่วยดูครับ

*1. Core migration version ซ้ำ (OPEN-025) — แก้แล้ว ✅*

ใน {{backend/src/main/resources/db/migration/}} มี version 24, 25, 26, 27 อย่างละ 2 ไฟล์ เช่น {{V024__alter_efs_assignment.sql}} กับ {{V024__staff_configuration_leave_columns.sql}} ปกติ Flyway ไม่ยอมให้ version ซ้ำ ทำให้ core migrate และ {{./gradlew test}} บน develop อาจพังอยู่แล้ว (ทีมเรายังไม่ได้รันพิสูจน์) รบกวนพี่ช่วยแจ้ง squad เจ้าของไฟล์ หรือยืนยันว่าตั้งใจ (เช่นใช้ outOfOrder หรือมีการ config พิเศษ)

_อัปเดต 9 พ.ย. 17:00: ทีม ACE แก้แล้วใน develop_ {{9f450bbd}} _(commit_ {{0719ac5e}} _renumber เป็น V025.1–V025.3 และ V027–V030) ตอนนี้ไม่มี version ซ้ำแล้ว ข้อนี้ข้ามได้เลยครับ เหลือข้อ 2 และ 3_

*2. Build agent มี Docker ไหม (OPEN-026)*

Test ของ recovery ที่ใช้ Testcontainers PostgreSQL อยู่ใน task {{recoveryIntegrationTest}} แยกจาก {{check}} ตอนนี้ให้ dev รันก่อนทุก MR ถ้า build agent ของ CI มี Docker เราจะขอเพิ่ม job เข้า CI ทีหลัง

*3. DEV ต้องรวมใน Jenkins step และ DBA request ด้วยไหม — ตอบแล้ว ✅*

ที่ตกลงกันไว้ (OPEN-013/019/020) ครอบแค่ SIT, UAT, PROD: เพิ่ม step {{db-migrate,db-migrate-recovery}} ใน Jenkins Flyway job และให้ DBA สร้าง schema {{recovery}} + grant DDL (Flyway {{createSchemas(false)}}) ถ้า DEV (เช่น job {{DEV_Deploy_DbMigration}}) ใช้ทางเดียวกัน ต้องเพิ่ม DEV เข้าไปด้วย ไม่อย่างนั้น migrate บน DEV จะล้มเพราะยังไม่มี schema

_อัปเดต 9 พ.ย. 17:15: DEV ใช้ pipeline เดียวกัน คือ build image ครั้งเดียวแล้วใช้ image digest เดิม deploy DEV → SIT → UAT → PROD ดังนั้น Jenkins Flyway step ที่สอง (db-migrate,db-migrate-recovery) และ DBA request (สร้าง schema recovery + grant DDL) รวม DEV ด้วย (OPEN-019, OPEN-020) ตอนนี้เหลือข้อ 2 (Docker บน build agent) ข้อเดียวครับ_

ตอบใน thread นี้ได้เลยครับ

ขอบคุณครับ

Jesniphat Pukkham, Recovery tech lead

### Comment 5: PIPAT SAENGOW, 2026-11-10T01:47:37.346+0700

Comment ID 1782091

@Jesniphat Pukkham 

ไม่ต้องสร้าง schema แยกได้ไหมอ่อครับ? เพราะไม่งั้นกลายเป็นว่าแค่แยก module ย่อยภายในก็ต้องเดินเรื่องไปถึง DBA ทุกครั้ง และจะมีปัญหากับ deployment slot ด้วยเพราะต้องแจ้ง DBA สร้าง schema = #slot x #module.

 

รบกวนทำตาม pattern ใน [https://gitdop.se.scb.co.th/AP2477-ACE/ace-monorepo/-/tree/develop/backend/src/main/resources/db/mo…|https://gitdop.se.scb.co.th/AP2477-ACE/ace-monorepo/-/tree/develop/backend/src/main/resources/db/modulemigration/samplemodule?ref_type=heads]

ได้ไหมอะครับ?

### Comment 6: Chitchaya Muanchonchana, 2026-11-10T10:34:45.632+0700

Comment ID 1782430

@Jesniphat PukkhamAs an internal TechX PO/BA , 2 points are approved as below.


# BR7 is accepted for this story through T-044-02 run before every merge request (OPEN-027). >> Agreed
# You approve the RWB-E1-044 specification (Backlog and specification gate). >> Approved

### Comment 7: Jesniphat Pukkham, 2026-11-10T12:04:22.164+0700

Comment ID 1782808

@Chitchaya Muanchonchana

*RWB-E1-044: updated specification for your approval*

Hi Chitchaya, the specification is now final for review. The latest version is attached: {{RWB-E1-044-spec-20261110-r4.md}}. It replaces the r2 file from yesterday.

*What changed since yesterday (technical, no scope change)*

* At the ACE tech lead's request, recovery tables stay in the shared ACE schema with the prefix {{rwb_}} instead of a separate schema. No DBA request is needed (D-RCV-47).
* Flyway baseline setting aligned with the ACE sample module (D-RCV-48).
* DEV uses the same pipeline and image as SIT, UAT and PROD.

Compliance review: no Critical, High or Medium findings. Your answers CLAR-001: A and CLAR-002: A are applied unchanged.

*Still needed from you (from my message of 9 Nov), please reply in this thread:*

# BR7 is accepted for this story through test T-044-02 run before every merge request (not in the CI build), as corrected in my previous comment (OPEN-027).
# You approve the RWB-E1-044 specification (Backlog and specification gate).

Example reply:

{quote}Confirmed BR7 via T-044-02 before every MR. Approved: RWB-E1-044 specification.{quote}

Thanks,

Jesniphat Pukkham, Recovery tech lead

### Comment 8: RACHATAPON PONGANANTAYOTIN, 2026-11-10T12:32:24.282+0700

Comment ID 1782844

RWB-E1-044 planner notice for RWB-TE-001 (D-RCV-43 (2)):

`backend/build.gradle.kts` now contains the recovery-scoped JaCoCo report and verification tasks, including the test-scope architecture tooling class directory. These checks are opt-in and are not wired into the shared ACE `check` or `build` tasks. Local verification passed; evidence is in `output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/report.md`.

The ACE changes remain uncommitted, with no MR or MR pipeline evidence yet. This is a local implementation notice, not evidence of publication or human verification.

### Comment 9: Chitchaya Muanchonchana, 2026-11-10T12:53:09.633+0700

Comment ID 1782880

@Jesniphat Pukkham As an internal TechX PO/BA , I has approved both points

# BR7 is accepted for this story through test T-044-02 run before every merge request (not in the CI build), as corrected in my previous comment (OPEN-027).
# You approve the RWB-E1-044 specification (Backlog and specification gate).

### Comment 10: THAMMASAK JUKCHAN, 2026-11-10T15:02:25.690+0700

Comment ID 1783351

*Implementation blocked: no access to VPN and SCB Artifactory*

Started: 2026-11-10 14:27 ICT

*Blocker*
The ACE backend build downloads Gradle 9.4.1 and all dependencies from the SCB Artifactory ({{artfactop.se.scb.co.th:8081}}). We don't have VPN access, so it can't be reached ({{UnknownHostException}}), and no build or test can run.

*Impact*

* The implementation stopped at TASK-01 (baseline test run). No code has changed.
* TASK-01 to TASK-17 are on hold, including the unit and coverage gates and the {{recoveryIntegrationTest}} evidence required by D-RCV-44.

### Comment 11: Jesniphat Pukkham, 2026-11-16T16:57:36.687+0700, edited 2026-11-16T16:58:32.316+0700

Comment ID 1793101

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
| Rework | customfield_17514 | Rework |
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
| Story Point | customfield_17479 | 8 |
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
