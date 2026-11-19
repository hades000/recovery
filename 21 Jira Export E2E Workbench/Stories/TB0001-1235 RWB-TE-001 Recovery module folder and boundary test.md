# TB0001-1235 [RWB-TE-001] Recovery module folder and boundary test

| Field | Value |
|---|---|
| Jira | [TB0001-1235](https://scbjira.atlassian.net/browse/TB0001-1235) |
| Type | Story |
| Status | Done |
| Resolution | Done |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | RAPEEPAT CHULAOTRAKUL |
| Reporter | PIMPISUT SRIPAVATAKUL |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Delivery Workbench Q4S1 Squad2 |
| Team | RWB_SQ1 |
| Created | 2026-11-05T16:11:09.780+0700 |
| Updated | 2026-11-17T22:04:31.125+0700 |
| Due date | - |
| Resolved | 2026-11-13T17:06:02.950+0700 |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 7 |
| Comments | 17 |

## Description

As a squad member (RW-TRIBE), I want the recovery module folder and packages in the ACE repository with a build-time boundary test, so that no module calls the inside of another module and no recovery code calls a system of record directly.

h2. Completed original scope

The user confirmed on 2026-11-11 that all previous tasks are complete. Jira subtasks TB0001-1287, TB0001-1288, TB0001-1289 and TB0001-1290 are Done. Keep these tasks and their implementation/test evidence unchanged. This amendment does not reopen them or change the parent workflow status.

Original delivery: ACE MR !285, implementation f144a1aa, merge 7050e771 into develop-recovery, as recorded in the increment card. Previous specification/plan approvals apply only to that completed baseline, not to the delta below.

h2. Namespace amendment requested 2026-11-11

Move the recovery backend package from {{th.co.scb.ace.demo.recovery}} to {{th.co.scb.ace.workbench.recovery}}. This is additional backend-only work under RWB-TE-001, with no UI or API contract change.

h3. Current evidence

ACE develop-recovery at 5fb90334 already has WorkbenchApplication and ModulithTest in {{th.co.scb.ace.workbench}}, while 58 recovery main-source files, 8 architecture test/tooling files and the module-map recovery root still use {{th.co.scb.ace.demo.recovery}}. The actual host must discover recovery after the move; a passing verify() without recovery discovery is not sufficient.

The current backend/build.gradle.kts has no JaCoCo plugin or recoveryCoverageReport/recoveryCoverageVerification tasks, unlike the completed plan. The amended plan must reconcile the current build and name the recovery-only shared-file changes; old test evidence cannot prove the delta.

h3. Proposed scope (pending decision)

* Relocate the complete recovery main/test subtree to {{backend/src/main/java/th/co/scb/ace/workbench/recovery/}} and {{backend/src/test/java/th/co/scb/ace/workbench/recovery/}}. Update declarations, imports, FQCN expectations and path selectors.
* Update only the recovery root in {{backend/src/test/resources/architecture/recovery-modules.yaml}}. Preserve all 19 nested module names, published/client packages, client-library allow-list and BND-1 through BND-5 semantics.
* Assert that discovery from WorkbenchApplication includes recovery and every one of the 19 mapped nested modules before verification. Missing recovery, stale map roots and omitted modules must fail explicitly.
* Retain existing architecture fixtures and their positive/negative assertions. Keep {{th.co.scb.ace.recoveryfixture}} test-only and unchanged except references to moved recovery tooling.
* Reconcile and obtain approval for recovery-only shared Gradle coverage wiring and recovery-specific ModulithTest assertions. Use corrected new-root selectors and native coverage reports including executable test tooling; no new dependency or CI stage is authorised.

h3. Proposed amendment acceptance criteria

These are draft delta criteria for PO specification approval, not replacement BA acceptance criteria and not executed results.

||ID||Given||When||Then||Planned test||
|AC-NS-01|Approved D-RCV-51 and existing recovery files|Recovery packages are moved and compiled|All recovery main/test declarations and references use the new root; no files remain under the old recovery path|T-TE001-NS-01: clean compile and scoped old-root/path scan|
|AC-NS-02|Actual Workbench application and versioned 19-module map|Production module discovery runs|Recovery and all 19 nested modules are discovered and verified; missing recovery or a nested module fails explicitly|T-TE001-NS-02: actual-host discovery and stale-root/missing-module negatives|
|AC-NS-03|Relocated architecture tooling and existing fixtures|Boundary/map/loader suites execute|Valid dependencies pass and existing illegal dependency, cycle, map and published-interface cases fail for the intended rule|T-TE001-NS-03: existing positive/negative suites with corrected imports|
|AC-NS-04|Approved reconciled coverage tasks|Backend tests and coverage run|Expected test counts are nonzero, tests pass, and each supported native JaCoCo metric meets 80% for moved main/tooling scope; absent tasks or empty selectors fail verification|T-TE001-NS-04: task/selector checks and native XML/HTML reports|
|AC-NS-05|Completed original tasks and current contracts|Delta diff and trace are inspected|Original tasks stay Done; no frontend, API, database or external-root changes; old evidence remains historical|T-TE001-NS-05: scoped diff and trace/contract review|

h3. Guardrails and unchanged surfaces

No frontend folder/lint/Vitest change; no route, API, payload, OpenAPI/generated-type, schema ace, rwb_ object, SQL migration, Flyway history/profile/resource-path or business-behaviour change. No global demo-package rename. Common/collection roots remain D-RCV-41 placeholders pending OPEN-024; do not infer new roots for another module. No shared application/security changes beyond the explicitly proposed recovery-only test/build scope. Backend unit tests are REQUIRED with an independent 80% gate for every supported native metric; frontend tests/coverage are NOT_APPLICABLE for this delta. Do not treat missing coverage tooling as an exemption.

h2. Open decision D-RCV-51

Status: OPEN / PROPOSED, not approved. Approval question: approve the recovery-only namespace move and actual-host discovery assertions, and confirm the exact recovery-only shared Gradle/test reconciliation scope? Record approver, date, constraints and PO amended-spec disposition.

Owners: recovery tech lead/FDA and ACE tech lead for architecture/shared files; Product Owner for amended specification. If approved, supersede only the recovery-root part of D-RCV-02. All other rulings remain binding. Context Updater aligns BS-1.1, BS-1.4 and backend/project context after approval; affected story owners assess their own specs/plans without rewriting completed history or the BA source corpus.

Tracking in the AISDLC repository: {{docs/decisions/INC-001-decisions.md}} (D-RCV-51), {{docs/open-items.md}} (OPEN-032 approval/build reconciliation, OPEN-033 context/impact alignment).

h2. Specification trace and next step

RUN_ID: {{INC-002-epic-1-RWB-TE-001}}. New draft SPEC-RWB-TE-001-021 through 024 map to FR-RWB-003 / FR-RWB-020 in {{requirement/Traceability_Matrix.md}}. Active draft: {{output/INC-002-epic-1-RWB-TE-001/specify/spec.md}}. CLAR-013 / OPEN-032 is unresolved; amended specification handoff is BLOCKED. No new delta tasks or implementation are created in this stage.

NEXT_STEP: resolve D-RCV-51 / OPEN-032, incorporate the decision and re-run Technical Specifier and its compliance gate with the same RUN_ID. Do not start planning or implementation until the amendment is approved.

## Acceptance criteria

```gherkin
Feature: Recovery module folder and boundary test

  Background:
    Given the module map lists modules P1 to P10 and S1 to S9 with their packages
    Given the published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module

  Scenario: AC1 Boundary enforced
    Given a class "recovery.casewf.internal.SampleService" that imports "collection.internal.CollectorRepository"
    When the pipeline runs
    Then the boundary test fails the build
    Then the build log names boundary rule BND-1, "SampleService" and "CollectorRepository"

  Scenario: AC2 Published interface allowed
    Given a class "recovery.casewf.internal.SampleService" that calls an interface in "common.api"
    When the pipeline runs
    Then the build passes

  Scenario: AC3 Recovery modules meet only through their api package
    Given a class in "recovery.integration.internal" that imports "recovery.decision.internal.DecisionLogRepository"
    When the pipeline runs
    Then the build fails with boundary rule BND-3
    When the class imports the published "recovery.decision.writer.DecisionLogWriter" instead
    Then the build passes

  Scenario: AC4 A module uses only its own tables
    Given a class in "recovery.integration.internal" that uses the entity "recovery.casewf.internal.RecoveryCaseEntity"
    When the pipeline runs
    Then the build fails with boundary rule BND-4

  Scenario: AC5 No direct call to a system of record
    Given a class in "recovery.casewf.internal" that uses "java.net.http.HttpClient"
    When the pipeline runs
    Then the build fails with boundary rule BND-5
    Then the same use in "recovery.integration.adapter" passes

  Scenario: AC6 Front end boundary
    Given a component in "src/modules/recovery/caselist" that imports "src/modules/collection/worklist/WorkList"
    When the front end build runs
    Then it fails with rule no-collection-import

  Scenario: AC7 A package missing from the module map
    Given a new package "recovery.vendorx" not in the module map
    When the pipeline runs
    Then the build fails with "package recovery.vendorx is not in the module map"
```

## Sub-tasks

- TB0001-1287 [Done] [RWB-TE-001] BE - Module skeleton and boundary rules
- TB0001-1288 [Done] [RWB-TE-001] BE - JaCoCo coverage and backend check
- TB0001-1289 [Done] [RWB-TE-001] FE - Import rule and Vitest setup
- TB0001-1290 [Done] [RWB-TE-001] Evidence, ACE MR and traceability
- TB0001-1372 [Done] [RWB-TE-001] BE - Namespace relocation to th.co.scb.ace.workbench.recovery

## Attachments

- [report.md](../../Attachments/TB0001-1235/report.md) (8120 bytes, RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:53:43.590+0700)
- [RWB-TE-001-spec-20261109.md](../../Attachments/TB0001-1235/RWB-TE-001-spec-20261109.md) (54053 bytes, Jesniphat Pukkham, 2026-11-09T13:37:43.129+0700)

## Comments (17)

### Comment 1: Jesniphat Pukkham, 2026-11-09T14:00:50.010+0700

Comment ID 1780957

@RAJ GHAI

*Approval request: Specification for RWB-TE-001 Recovery module folder and boundary test*

Hi Raj,

The technical specification for RWB-TE-001 is ready for your *Backlog and specification approval*. It is attached to this issue: {{RWB-TE-001-spec-20261109.md}}.

*Status*

* No open clarifications. All 6 business rules are covered.
* Compliance review: no Critical, High or Medium findings. The remaining Low findings are text-only and accepted by the tech lead.
* This is a technical enabler with no business acceptance criteria, so no product decision is needed. We only need your approval.

*What the story delivers*

* The recovery module folder in the ACE repository, with one package per Workbench module (P1–P10, S1–S9).
* Build-time checks that fail a pull request when code breaks the module boundaries: no use of another module's internals, entities or repositories, and no direct call to external systems outside the approved adapter packages.
* A frontend lint rule that stops recovery screens from importing other squads' code.

*What moved out (for your information)*

* The shared access check ({{RecoveryAccessGuard}}, 403 for a role without the right) moves to RWB-E1-022 (sign-on and roles). That is where the access model is built (D-RCV-36).

New build dependencies (Vitest, JaCoCo) are being confirmed with the ACE tech lead separately.

*Please reply in this thread:*

{quote}Approved: RWB-TE-001 specification.{quote}

Thanks,

Jesniphat Pukkham, Recovery tech lead

### Comment 2: Jesniphat Pukkham, 2026-11-09T14:08:08.104+0700, edited 2026-11-09T14:49:21.215+0700

Comment ID 1780978

@PIPAT SAENGOW

cc: @PONGCHAI CHAROENRUNGRODKUN 

*ขออนุมัติ dependency ใหม่และการแก้ไฟล์ shared ของ ACE สำหรับ RWB-TE-001*

Story RWB-TE-001 (Recovery module folder and boundary test) ต้องเพิ่ม dependency และแก้ไฟล์ shared บางไฟล์ใน ace-monorepo ก่อนเริ่ม build เลยรบกวนพี่ช่วยอนุมัติครับ (ใน plan คือเงื่อนไข PRE-2 / OPEN-023)

*Dependency ใหม่*

* Frontend (devDependencies เท่านั้น): {{vitest}} 4.1.12 และ {{@vitest/coverage-v8}} 4.1.12 ใช้รัน unit test ของ recovery และวัด coverage 80% เฉพาะ {{src/modules/recovery/**}}
* Backend: Gradle plugin {{jacoco}} (tool 0.8.14) วัด coverage เฉพาะ package ของ recovery ส่วน ArchUnit กับ SnakeYAML มีใน test classpath อยู่แล้ว ไม่ได้เพิ่ม

*ไฟล์ shared ที่จะแก้*

* {{frontend/package.json}}: เพิ่ม devDependencies ข้างบน และ {{nx.targets.test}} ({{vitest run --coverage}}) ใส่ไว้ใน {{check}} เพราะ Nx 24 ไม่ infer test target ให้
* {{frontend/eslint.config.js}}: เพิ่ม block {{no-restricted-imports}} ที่มีผลเฉพาะ {{src/modules/recovery/**}} และ ignore โฟลเดอร์ fixture ไม่แตะ block อื่น
* {{frontend/tsconfig.app.json}}: exclude โฟลเดอร์ test และ fixture ของ recovery
* {{frontend/vitest.config.ts}}: ไฟล์ใหม่ ใช้เฉพาะ test ของ recovery
* {{package-lock.json}} และ {{frontend/package-lock.json}}: อัปเดตจาก {{npm install -D --save-exact ... -w frontend}}
* {{backend/build.gradle.kts}}: เพิ่ม plugin {{jacoco}} และ task {{recoveryCoverageReport}} / {{recoveryCoverageVerification}}

*Package ใหม่ (test เท่านั้น)*

* {{th.co.scb.ace.recoveryfixture}} อยู่ใต้ {{src/test}} ไม่ติดไปใน jar ใช้พิสูจน์ว่ากฎ boundary fail ตามที่ควร ตั้งไว้นอก {{th.co.scb.ace.demo}} เพราะ {{@EnableJpaRepositories}} ใน AppConfig scan ทั้ง {{th.co.scb.ace.demo}} ถ้าวางไว้ข้างใน fixture จะถูกโหลดใน {{@SpringBootTest}} ทุกตัว

*ผลข้างเคียงที่อยากให้พี่ทราบ*

* พอใส่ plugin {{jacoco}} agent จะติดไปกับทุก Test task ({{test}}, {{testE2E}}) ทีมจะวัดเวลารัน {{test}} ก่อนและหลังแล้วแจ้งให้ทราบ

*ไม่แก้*: โค้ด ACE core, module อื่น, {{nx.json}}, root {{package.json}}, {{.gitlab-ci.yml}}, {{vite.config.ts}} ส่วน ACE tests เดิมยังใช้ H2 และควรผ่านเหมือนเดิม

รายละเอียดอยู่ใน plan: {{recovery/output/INC-002-epic-1-RWB-TE-001/plan/plan.md}} (repo AP2477-ACE/ace-aisdlc, MR !15)

*รบกวนพี่ตอบใน thread นี้ครับ* เช่น

{quote}อนุมัติ OPEN-023 สำหรับ RWB-TE-001{quote}

หรือถ้าอยากให้เปลี่ยนข้อไหน (เวอร์ชัน, ไฟล์, ชื่อ package) บอกได้เลยครับ

ขอบคุณครับ

Jesniphat Pukkham, Recovery tech lead

### Comment 3: Chitchaya Muanchonchana, 2026-11-09T14:14:53.249+0700, edited 2026-11-09T14:33:42.605+0700

Comment ID 1781003

@Jesniphat Pukkham No inquiry left for this ticket , This ticket is approved to continue by TechX PO ka.

### Comment 4: PONGCHAI CHAROENRUNGRODKUN, 2026-11-09T15:27:14.653+0700

Comment ID 1781273

@Jesniphat Pukkham 

อนุมัติ OPEN-023 สำหรับ RWB-TE-001

### Comment 5: RACHATAPON PONGANANTAYOTIN, 2026-11-10T12:32:24.217+0700

Comment ID 1782843

OPEN-023 implementation notice for RWB-TE-001:

The local implementation includes the approved shared-file changes and the new test-only fixture root package `th.co.scb.ace.recoveryfixture`. Shared files changed are `backend/build.gradle.kts`, `frontend/eslint.config.js`, `frontend/package.json`, `frontend/tsconfig.app.json`, both npm lockfiles, and the new `frontend/vitest.config.ts`. The fixture package is under backend `src/test/java`, outside the deployed application package and is not included in the production artifact.

The backend and frontend unit-test/coverage checks passed locally; evidence is in `output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/report.md`. Changes remain uncommitted; no MR or pipeline run exists yet. This comment records the planned OPEN-023 notice only; it does not claim an MR, pipeline result, or merge.

### Comment 6: RACHATAPON PONGANANTAYOTIN, 2026-11-10T12:34:34.495+0700

Comment ID 1782848

Story-owner approval requested for the BND-4 diagnostic proposed in REVIEW-RWB-TE-001-034.

For an entity or repository target outside the recovery modules and the mapped `common`/`collection` roots, the current fallback says to use `common.api`, which can misidentify ACE `model` or `repository` packages. Proposed fallback wording:

{quote}Use the owning module's service or published interface, not its entity or repository.{quote}

This would change only the fallback diagnostic; the existing `common.api` and `collection.api` messages remain unchanged. Please reply with explicit approval of this exact wording or provide the approved alternative. No ACE source, test, specification, or plan change has been made pending approval.

### Comment 7: Jesniphat Pukkham, 2026-11-10T14:11:19.793+0700

Comment ID 1783131

@RACHATAPON PONGANANTAYOTIN Approved, as story owner (Jesniphat Pukkham, recovery tech lead), 2026-11-10.

REVIEW-RWB-TE-001-034: use this exact fallback wording for BND-4 targets outside the recovery modules and the mapped common/collection roots:
"Rule BND-4 broken: {class} depends on {dependency}. Use the owning module's service or published interface, not its entity or repository."

The "Rule BND-4 broken: {class} depends on {dependency}." prefix stays as in SPEC-RWB-TE-001-010. The common.api and collection.api messages stay unchanged.
Record this as a spec deviation from SPEC-RWB-TE-001-010 (fallback text only) in output/INC-002-epic-1-RWB-TE-001/implement/ with a link to this comment. No /specify or plan re-run needed.

### Comment 8: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:46:38.569+0700

Comment ID 1783556

h3. หลักฐานยืนยัน Acceptance และขอบเขต MR pipeline — RWB-TE-001

*ยืนยันว่าไม่มี business Acceptance Criteria (AC) ใน story ต้นฉบับ แต่ไม่ได้หมายความว่าไม่มีเกณฑ์รับงานหรือไม่ต้องทดสอบ*

*หลักฐาน*
# Story ต้นฉบับ §7 Acceptance criteria ระบุชัดว่า:
{quote}No business acceptance criteria. This story is an engineering enabler for module boundary tests; its development-process criteria were removed on 4 November 2026.{quote}
แหล่งอ้างอิง: repo {{AP2477-ACE/ace-aisdlc}}, {{recovery/requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 001 Recovery module folder and boundary test v1.md}}, §7 (เอกสาร v1, 28 Oct 2026).
# D-RCV-16 กำหนดให้ใช้ *business rules (BR1–BR6) และ test cases ที่ยังอยู่ใน story* เป็นเกณฑ์ acceptance แทน AC ที่ถูกนำออก: [Decision log|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/decisions/INC-001-decisions.md].
# [Technical specification|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/specify/spec.md] หัวข้อ Requirement-to-SPEC Logic Coverage ยืนยันเกณฑ์นี้ พร้อม mapping BR/test cases; SPEC-016 ระบุว่า access guard และ TC-TE-001-08 ย้ายไป RWB-E1-022 (D-RCV-36).
# หลักฐานใน Jira เดิม: [comment 1780957|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1780957] ระบุว่าเป็น technical enabler with no business acceptance criteria; [comment 1781003|https://scbjira.atlassian.net/browse/TB0001-1235?focusedCommentId=1781003] เป็นการอนุมัติให้ดำเนินการต่อโดย TechX PO.

*ข้อสรุปเรื่อง pipeline / MR gate*
* Story §4 ข้อ 6–7, §12 และ §13 ข้อ 7 ต้องการ backend boundary tests และ frontend dependency check ใน PR build; ผิดกฎต้อง fail build.
* แต่ *D-RCV-05 และ SPEC-012/015/016 กำหนดให้ใช้ build เดิม ไม่เพิ่ม pipeline stage และไม่แก้ {{.gitlab-ci.yml}}* (ชื่อไฟล์จริงใช้ {{.yml}} ไม่ใช่ {{.yaml}}): backend อยู่ใน Gradle {{test}}; frontend อยู่ใน ESLint และ Vitest target ที่ผูกกับ Nx {{check}}.
* ไฟล์ CI ที่ตรวจใน workspace เรียก {{nx affected -t check}} สำหรับ MR ที่ target เป็น default branch โดย {{allow_failure: false}}; default-branch build เรียก {{nx run-many -t check}}. ไม่ใช่หลักฐานว่ารันกับ MR ทุก target branch.
* การ block merge จริงต้องตรวจ GitLab project setting “Pipelines must succeed” แยกต่างหาก; ยังไม่ได้ยืนยัน setting หรือผล MR pipeline จากการตรวจนี้.
* Story text ที่ยังกล่าวถึงการเพิ่ม pipeline step ถูกติดตามให้ BA แก้ใน OPEN-021: [Open items|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/open-items.md].

คอมเมนต์นี้บันทึกหลักฐานขอบเขต requirement เท่านั้น ไม่ได้เพิ่ม AC ใหม่ ไม่ใช่การรับรองว่าทดสอบผ่านหรืออนุมัติปิดงาน และไม่เปลี่ยนสถานะ ticket.

### Comment 9: RACHATAPON PONGANANTAYOTIN, 2026-11-10T15:52:08.829+0700, edited 2026-11-10T15:53:43.581+0700

Comment ID 1783617

h3. QA evidence: BR1–BR6 / story test cases — fresh local verification, 10 Nov 2026

*Result: LOCAL AUTOMATED PASS. Live GitLab MR pipeline / merge blocking: NOT RUN.*

ACE branch: {{feature/TB0001-1235-recovery-module-boundary}}
ACE commit: {{f144a1aa9b26ef30ff052ca4285850345ad9247c}}
Source worktree was clean before testing; no product/test source was changed. Synthetic static fixtures only; no application launch, database, Docker or customer data.

*Executed commands*
Backend, from {{ace-monorepo/backend}}, Java 21:

{code:java}DISABLE_SCB_REPO=1 ./gradlew test --tests 'th.co.scb.ace.demo.recovery.architecture.*' --tests 'th.co.scb.ace.demo.ModulithTest' recoveryCoverageReport recoveryCoverageVerification --rerun-tasks --console=plain{code}

Frontend, from {{ace-monorepo/frontend}}:

{code:java}npx --no-install vitest run src/modules/recovery/__tests__/importBoundary.test.ts --coverage --reporter=default --reporter=junit --outputFile.junit="$EVIDENCE/frontend/junit.xml"{code}

Both exit codes: *0*. Backend: *23 passed / 0 failed / 0 errors / 0 skipped*, BUILD SUCCESSFUL in 23s. Frontend: *2 passed / 0 failed / 0 errors / 0 skipped*, 3.36s.

||*BR / story case*||*Local result*||*Executed proof*||
|BR1 / TC-TE-001-01|PASS|RecoveryBoundaryRulesTest.rejectsRecoveryDependenciesOnUnpublishedCollectionTypes asserts BND-1 + dependency diagnostic; allowsDependenciesOnPublishedCollectionTypes verifies the permitted path.|
|BR2 / TC-TE-001-02|PASS|allowsDependenciesOnPublishedCommonTypes passes; rejectsRecoveryDependenciesOnUnpublishedCommonTypes verifies BND-2 and the forbidden dependency.|
|BR3 / TC-TE-001-03|PASS against approved spec|RecoveryModulithFixtureTest rejects unpublished nested-module types, accepts published types and rejects cycles; existing ModulithTest passes against actual application modules.|
|BR4 / TC-TE-001-04|PASS|rejectsEntitiesAndRepositoriesFromOtherRecoveryModules + allowsEntitiesAndRepositoriesFromTheSameRecoveryModule; tests also reject common/collection/unmapped ACE data dependencies and check diagnostics.|
|BR5 / TC-TE-001-05|PASS|rejectsClientLibraryDependenciesOutsideDeclaredClientPackages detects java.net.http.HttpClient; allowsClientLibrariesOnlyInEachModuleDeclaredClientPackage permits adapter/agent-client packages; lookalike matching tested.|
|BR6 / TC-TE-001-07|PASS against approved spec|RecoveryModuleMapTest rejects an unmapped package and declaration mismatches; valid map passes. ModuleMapLoaderTest covers actual map, valid configuration, invalid fields and missing resources.|
|Frontend / TC-TE-001-06 from Test Cases v5|PASS against approved spec|Vitest asserts 11 no-restricted-imports errors at exact fixture lines, and no restricted-import errors for allowed imports. This case is in the test-case workbook, not a row in story section 16.|
|Access / TC-TE-001-08|OUT OF SCOPE / NOT RUN|Moved to RWB-E1-022 by D-RCV-36 and SPEC-016; not claimed PASS.|

*Native JUnit suite counts*

||*Suite*||*Passed*||*Failed*||*Skipped*||
|ModulithTest|1|0|0|
|ModuleMapLoaderTest|4|0|0|
|RecoveryBoundaryRulesTest|12|0|0|
|RecoveryBoundaryTest|1|0|0|
|RecoveryModuleMapTest|2|0|0|
|RecoveryModulithFixtureTest|3|0|0|
|Frontend importBoundary.test.ts|2|0|0|

*Coverage*
JaCoCo recovery-only + approved architecture tooling: instructions 96.12% (1488/1548), branches 88.82% (151/170), lines 96.26% (309/321), methods 100% (63/63). All four 80% thresholds passed. Frontend native report prints 100% (0/0) for all metrics because the recovery folder has no measurable runtime implementation; this is not runtime UI coverage.

*Interpretation / limitations for QA*

* Negative-fixture PASS means the expected violation was thrown and asserted. No forbidden dependency was accepted; no live CI job was intentionally failed.
* Fixture names differ from the legacy story examples (CollectionSecret vs CollectorRepository; dataengine/integration vs decision/writer; rogue vs vendorx). These are approved-spec equivalent checks, not a literal replay of those example names. BR3 diagnostic is Spring Modulith's own (SPEC-007/D-RCV-42); frontend rule is no-restricted-imports (SPEC-014/015/D-RCV-39), not legacy no-collection-import.
* RecoveryBoundaryTest also checks current main classes with the real module map. Some rules can have no matching runtime dependencies in a skeleton; passing/breaking fixtures provide separate enforcement evidence.
* D-RCV-05 reuses existing CI; no CI YAML/stage changes. This run does *not* prove live MR pipeline execution, “Pipelines must succeed”, merge protection, SIT/UAT or a fresh full ACE regression.
* No business AC is added: acceptance remains BR + test cases under D-RCV-16.

*Saved evidence*
Local workspace directory (not yet committed/pushed or uploaded as Jira attachments):
{{recovery/output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/qa-br-verification-20261110T084952Z/}}
Contains report.md, backend/test-run.log, backend/test-results/*.xml, backend/test-report/index.html, backend/recoveryCoverageReport.xml, frontend/test-run.log, frontend/junit.xml, frontend/coverage-summary.json and both exit-code.txt files. $EVIDENCE in the frontend command points to this absolute directory. This comment contains the shareable result summary; unpublished artifact links are not claimed available.

Requirements: [Approved spec|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/output/INC-002-epic-1-RWB-TE-001/specify/spec.md], [Decision log|https://gitdop.se.scb.co.th/AP2477-ACE/ace-aisdlc/-/blob/main/recovery/docs/decisions/INC-001-decisions.md].

No Jira status change or QA acceptance/sign-off is implied.

[^report.md]



### Comment 10: RACHATAPON PONGANANTAYOTIN, 2026-11-11T14:39:36.674+0700

Comment ID 1785593

h2. ขออนุมัติ D-RCV-51 / OPEN-032: ย้าย Recovery package เข้า Workbench application

ขอให้ Recovery Tech Lead / FDA, ACE Tech Lead และ Product Owner พิจารณา amendment ของ RWB-TE-001 ตามรายละเอียดด้านล่าง

*สถานะปัจจุบัน: OPEN / PROPOSED — คอมเมนต์นี้เป็นคำขออนุมัติ ไม่ใช่หลักฐานว่าอนุมัติแล้ว*

h3. 1. เหตุผลและ baseline

* ขอเปลี่ยน backend package จาก {{th.co.scb.ace.demo.recovery}} เป็น {{th.co.scb.ace.workbench.recovery}}
* จากการตรวจ ACE {{develop-recovery}} ที่ commit {{5fb90334}} พบว่า {{WorkbenchApplication}} และ {{ModulithTest}} อยู่ใต้ {{th.co.scb.ace.workbench}} แล้ว แต่ recovery main-source 58 ไฟล์, architecture test/tooling 8 ไฟล์ และ module-map recovery root ยังอยู่ใต้ {{demo.recovery}}
* จึงต้องตรวจหลังย้ายว่า actual Workbench application ค้นพบ recovery และ nested modules จริง ไม่ใช่อาศัยเพียง {{verify()}} ที่ผ่านโดยยังไม่ได้ยืนยัน module discovery
* งานเดิมเสร็จแล้ว: TB0001-1287, TB0001-1288, TB0001-1289 และ TB0001-1290 เป็น Done ทั้งหมด ขอคงสถานะและหลักฐานเดิมไว้ การเปลี่ยนนี้เป็น delta เพิ่มเติม ไม่ใช่ reopen task เดิม

h3. 2. ขอบเขตที่ขออนุมัติทางเทคนิค

# ย้าย recovery main/test subtree ทั้งหมดไปยัง {{backend/src/main/java/th/co/scb/ace/workbench/recovery/}} และ {{backend/src/test/java/th/co/scb/ace/workbench/recovery/}} พร้อมปรับ package declarations, imports, FQCN expectations และ path selectors ที่อ้างถึง recovery
# เปลี่ยนเฉพาะ recovery {{rootPackage}} ใน {{backend/src/test/resources/architecture/recovery-modules.yaml}} โดยคงชื่อและโครงสร้าง 19 nested modules, published interfaces, client-package/client-library allow-list และกฎ BND-1..BND-5 / BR1..BR6 เดิม
# เพิ่ม recovery-specific assertions ใน {{ModulithTest}} เพื่อยืนยันว่า {{ApplicationModules.of(WorkbenchApplication.class)}} ค้นพบ recovery และ nested modules ครบทั้ง 19 รายการก่อน verify; stale root, missing module และ illegal internal dependency ต้องทำให้ test fail อย่างชัดเจน
# ปรับ tests/fixtures ที่อ้างถึง recovery tooling ให้ใช้ root ใหม่ โดยคง fixture root {{th.co.scb.ace.recoveryfixture}} เป็น test-only ตามเดิม ไม่ย้าย module อื่น
# ตรวจ reconciliation ของ recovery-only Gradle coverage wiring: ณ commit ที่ตรวจ {{backend/build.gradle.kts}} ไม่มี JaCoCo plugin หรือ {{recoveryCoverageReport}} / {{recoveryCoverageVerification}} ตาม completed plan จึงขอให้ยืนยันขอบเขตการคืน/ปรับ wiring ที่จำเป็นตาม D-RCV-40/-43 ก่อนอนุมัติ amended plan โดย planner ต้องระบุ shared-file diff ให้ชัดเจน ไม่ใช่อนุมัติให้ restore build changes อื่นแบบเหมารวม
# Backend unit tests และ native coverage ต้องรันใหม่ด้วย selectors ของ root ใหม่ รวม executable architecture tooling และไฟล์ที่ยังไม่มี test; coverage อย่างน้อย 80% แยกทุก metric ที่ native tool รองรับ ห้ามใช้ผลเดิมหรือ test count เป็นศูนย์เป็นหลักฐานว่าการย้ายสำเร็จ

h3. 3. สิ่งที่ไม่เปลี่ยน / guardrails

* ไม่แก้ frontend folder, ESLint/Vitest rule, UI, route, API, payload, OpenAPI หรือ generated frontend types
* ไม่แก้ schema {{ace}}, {{rwb_}} naming, SQL migration ที่ merge แล้ว, Flyway history/profile/resource paths; Java package rename นี้ไม่ต้องเพิ่ม SQL migration
* ไม่ทำ global rename {{demo}} และไม่ย้าย common/collection modules; external roots ยังคงตาม D-RCV-41 และรอ OPEN-024
* ไม่เพิ่ม dependency หรือ CI stage ใหม่; coverage tasks คงอยู่นอก {{check}} ตาม decision เดิม
* ไม่เปลี่ยน shared host application/security code นอกเหนือจาก recovery-specific test/build scope ที่ระบุและผ่าน plan approval
* ไม่แก้ BA legacy source หรือ context files ในรอบนี้; Context Updater เป็นผู้ปรับ context หลัง decision อนุมัติ
* ไม่ reopen task เดิม และไม่ถือว่า prior spec/plan approvals ครอบคลุม delta นี้

h3. 4. Acceptance criteria ของ delta ที่ขอ PO พิจารณา

||ID||เงื่อนไขการยอมรับ||
|AC-NS-01|Recovery main/test declarations, imports และ references ใช้ root ใหม่ compile ผ่าน และไม่มี recovery files ค้างใต้ path เดิม|
|AC-NS-02|Actual Workbench discovery พบ recovery และ nested modules ครบ 19 รายการ; stale root หรือ missing module ต้อง fail|
|AC-NS-03|Boundary/map/loader positive และ negative fixtures เดิมยังผ่าน/ปฏิเสธได้ตรง rule โดยไม่ skip หรือ weaken test|
|AC-NS-04|Approved coverage wiring ใช้ root ใหม่ มี expected test count มากกว่าศูนย์, tests ผ่าน และ native coverage แต่ละ supported metric อย่างน้อย 80%; missing tasks/empty selectors ไม่ถือว่าผ่าน|
|AC-NS-05|Task เดิมคง Done; diff ไม่เปลี่ยน frontend/API/database/external roots และแยกหลักฐานเดิมออกจากผลทดสอบ delta ใหม่|

Frontend unit tests/coverage เป็น NOT_APPLICABLE สำหรับ delta นี้เพราะไม่มี frontend change; backend เป็น REQUIRED ผลทดสอบของ delta ยังไม่ได้ execute ในขั้น specification

h3. 5. ขอคำตอบจากผู้มีอำนาจอนุมัติ

* *Recovery Tech Lead / FDA:* ยืนยัน target namespace, discovery/boundary scope และขอบเขต recovery-only shared test/build reconciliation
* *ACE Tech Lead:* ยืนยันความสอดคล้องกับ Workbench host และ shared-file scope โดยเฉพาะ {{ModulithTest}} / {{backend/build.gradle.kts}}
* *Product Owner:* อนุมัติ amended specification และ AC-NS-01..05 โดยคง completed original tasks เป็น Done

กรุณาระบุ *Approve / Request changes*, ชื่อผู้อนุมัติ, บทบาท, วันที่ และข้อจำกัดที่มี หากอนุมัติได้เพียงบางส่วน กรุณาระบุส่วนที่อนุมัติและส่วนที่ยัง pending แยกกัน

ตัวอย่างข้อความตอบสำหรับผู้อนุมัติทางเทคนิค:
{quote}
Approve D-RCV-51 / OPEN-032: ย้ายเฉพาะ recovery จาก th.co.scb.ace.demo.recovery ไป th.co.scb.ace.workbench.recovery พร้อม actual-host discovery ครบ 19 nested modules และ recovery-only test/coverage reconciliation ตามขอบเขตที่ขอ โดย amended plan ต้องแจกแจง shared-file diff ก่อน implementation ไม่มี frontend/API/database change และไม่ reopen task เดิม
ผู้อนุมัติ: <ชื่อ> / บทบาท: <Recovery Tech Lead-FDA หรือ ACE Tech Lead> / วันที่: <วันที่> / ข้อจำกัด: <ระบุ หรือ ไม่มี>
{quote}

ตัวอย่างข้อความตอบสำหรับ Product Owner:
{quote}
Approve amended specification ของ RWB-TE-001 สำหรับ D-RCV-51 และ AC-NS-01..05 โดยงานเดิมและ task เดิมยังคง Done; delta ใหม่ต้องผ่าน amended plan และ test evidence ก่อนส่งมอบ
ผู้อนุมัติ: <ชื่อ> / บทบาท: Product Owner / วันที่: <วันที่> / ข้อจำกัด: <ระบุ หรือ ไม่มี>
{quote}

h3. 6. เอกสารและสถานะ gate

* RUN_ID: {{INC-002-epic-1-RWB-TE-001}}
* Decision: {{docs/decisions/INC-001-decisions.md}} — D-RCV-51 (OPEN / PROPOSED)
* Open items: {{docs/open-items.md}} — OPEN-032 (approval/build reconciliation), OPEN-033 (context/affected-story alignment หลังอนุมัติ)
* Active draft: {{output/INC-002-epic-1-RWB-TE-001/specify/spec.md}} — SPEC-RWB-TE-001-021..024, CLAR-013
* Traceability: {{requirement/Traceability_Matrix.md}} — FR-RWB-003 / FR-RWB-020
* Bounded Compliance Review: {{REVIEW-RWB-TE-001-NS-001}} = PASS, 0 findings; ไม่ทดแทน human approval

*SPEC_CLARIFICATION_STATUS: BLOCKED [OPEN_ITEMS: 1]*

หลังได้รับคำตอบครบ จะบันทึก decision และนำกลับเข้า Technical Specifier ด้วย RUN_ID เดิมเพื่อปรับ spec/re-review ก่อน handoff ไป amended planning ตามขั้นตอนที่มนุษย์เริ่มเอง ขณะนี้ยังไม่มีการแก้ application code, สร้าง delta tasks หรือเริ่ม implementation

### Comment 11: RACHATAPON PONGANANTAYOTIN, 2026-11-11T14:56:07.084+0700

Comment ID 1785682

@Jesniphat Pukkham @PIPAT SAENGOW @Chitchaya Muanchonchana please confirm this decision krub.

### Comment 12: Jesniphat Pukkham, 2026-11-11T15:08:44.260+0700

Comment ID 1785735

@RACHATAPON PONGANANTAYOTIN Approved

### Comment 13: PIPAT SAENGOW, 2026-11-11T15:31:53.556+0700

Comment ID 1785826

Approve with condition that P' @Jesniphat Pukkham  must adjust process such that these kind of recovery-only approval is not required. My approval is not value-added for non-cross-cutting concern like this..

### Comment 14: Chitchaya Muanchonchana, 2026-11-11T16:14:59.377+0700

Comment ID 1785987

@RACHATAPON PONGANANTAYOTIN As internal PO/BA techX, I have approved ka,

### Comment 15: Jesniphat Pukkham, 2026-11-12T10:01:44.720+0700

Comment ID 1786858

@RACHATAPON PONGANANTAYOTIN Approve ครับ

### Comment 16: RACHATAPON PONGANANTAYOTIN, 2026-11-12T10:22:05.335+0700

Comment ID 1786926

h2. Unit test report — RWB-TE-001

รายงานผลที่บันทึกไว้สำหรับ namespace-relocation delta วันที่ 2026-11-12 (ไม่ได้รัน tests ใหม่ในการโพสต์ comment นี้)
* RUN_ID: {{INC-002-epic-1-RWB-TE-001}}
* Source report: {{output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/report.md}}
* Working directory: {{ace-monorepo/backend}}
* Command: {{DISABLE_SCB_REPO=1 ./gradlew checkstyleMain checkstyleTest test recoveryCoverageReport recoveryCoverageVerification}}
* Exit code: 0 — BUILD SUCCESSFUL in 2m 10s; 9/9 tasks executed

||Surface||Passed||Failed||Skipped||Statements / instructions||Branches||Functions / methods||Lines||Gate||Status||
|Backend suite|789|0|290|96.12% (1488/1548)|88.82% (151/170)|100.00% (63/63)|96.26% (309/321)|80% per supported metric|PASS (interim evidence)|
|Frontend — namespace delta|N/A|N/A|N/A|N/A|N/A|N/A|N/A|N/A|NOT_APPLICABLE — no frontend changes in this delta (SPEC-RWB-TE-001-024)|

หมายเหตุ: จำนวน tests เป็นผลของ backend suite ทั้งชุด ส่วน coverage เป็น Recovery scope ตามรายงาน ไม่ใช่ coverage ของ ACE ทั้งโปรเจกต์; JaCoCo instructions ใช้แทน statements และ methods ใช้แทน functions

h3. Recovery verification detail
* RecoveryModuleDiscoveryTest: 2/2
* ModulithTest: 1/1
* RecoveryBoundaryRulesTest: 12/12
* ModuleMapLoaderTest: 4/4
* RecoveryBoundaryTest: 1/1
* RecoveryModulithFixtureTest: 3/3
* RecoveryModuleMapTest: 2/2
* Checkstyle main/test: 0 errors
* Recovery coverage verification: passed 80% LINE/INSTRUCTION/BRANCH/METHOD gate

h3. Evidence locations
ไฟล์ต่อไปนี้อยู่ใน workspace repository; ยังไม่ได้แนบไฟล์เข้า Jira และ path เหล่านี้ไม่ใช่ URL สำหรับดาวน์โหลด
* Full report: {{output/INC-002-epic-1-RWB-TE-001/implement/unit-tests/report.md}}
* Run log: {{output/INC-002-epic-1-RWB-TE-001/implement/backend/delta-20261112/gradle-run.log}}
* JaCoCo XML: {{output/INC-002-epic-1-RWB-TE-001/implement/backend/delta-20261112/recoveryCoverageReport.xml}}
* Recovery JUnit XML: {{output/INC-002-epic-1-RWB-TE-001/implement/backend/delta-20261112/test-results-recovery/}}
* Checkstyle: {{output/INC-002-epic-1-RWB-TE-001/implement/backend/delta-20261112/checkstyle-main.xml}} และ {{checkstyle-test.xml}} ใน directory เดียวกัน

h3. Limitations / pending verification
* ผลนี้เป็น *interim public-mirror evidence*: ใช้ existing switch {{DISABLE_SCB_REPO=1}} เพื่อ resolve จาก Gradle Plugin Portal / Maven Central แทน SCB repository ที่เข้าไม่ถึง
* ยังไม่ได้ยืนยันความเทียบเท่ากับ ACE GitLab MR pipeline; *HV-3 ยังต้องดำเนินการ* ก่อนถือเป็น final pipeline-equivalent evidence
* REVIEW-RWB-TE-001-NS-002-03 เรื่อง negative-case simulation ยังเปิดอยู่และไม่ได้ถูกปิดด้วยผลรันนี้
* Backend suite มี skipped 290 ตามรายงาน; ไม่ได้นับ skipped เป็น passed
* PASS นี้ยืนยันเฉพาะผลรันและ coverage ที่อ้างอิง ไม่ใช่การอนุมัติปิด story หรือ release readiness

### Comment 17: RAPEEPAT CHULAOTRAKUL, 2026-11-13T17:05:35.694+0700, edited 2026-11-13T17:24:23.694+0700

Comment ID 1790639

QA Verified unit test results. No Test in-Sprint / SIT / UAT testing required as this is a non-testable technical ticket. Moved status to Done.

@Pe Chichareon 


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| [CHART] Time in Status | customfield_10025 | 10019_*:*_1_*:*_6730_*\|*_10018_*:*_1_*:*_2421_*\|*_12708_*:*_1_*:*_18711_*\|*_10073_*:*_1_*:*_78804918_*\|*_10072_*:*_1_*:*_7276_*\|*_10075_*:*_1_*:*_3254_*\|*_10074_*:*_1_*:*_1069595_*\|*_10076_*:*_1_*:*_0_*\|*_10014_*:*_1_*:*_327387701_*\|*_10069_*:*_1_*:*_287181052 |
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| Business Go-live Date | customfield_17518 | 2026-11-13 |
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
| Story Point | customfield_17479 | 5 |
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
