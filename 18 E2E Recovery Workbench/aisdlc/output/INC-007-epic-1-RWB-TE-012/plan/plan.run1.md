---
title: "Implementation Plan: RWB-TE-012 Document storage containers"
run_id: "INC-007-epic-1-RWB-TE-012"
story: "RWB-TE-012"
epic: "EPIC-001"
status: "SUCCESS"
revision: "v1 (18 Nov 2026): first plan for RWB-TE-012, written against spec v10 (spec gate round 10 PASS 0C/0H/0M/0L, `review/spec-gate-review-10.md`). The plan gate has not been run in this stage; the orchestrator runs it."
prepared: "2026-11-18"
---

# Implementation Plan: RWB-TE-012 Document storage containers

Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in `../specify/spec.md`; no screen, component, route or client type changes).

| Field | Value |
|---|---|
| Spec | `../specify/spec.md` v10. Spec gate round 10: `PASS` 0/0/0/0 (`../review/spec-gate-review-10.md`). `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 37] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`; 26 `CLAR-*` rows, all `RESOLVED`; `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`. |
| Precondition | RWB-TE-001 merged in this repository, at its plan v7 layout: `dochub/api`, `dochub/storage`, the module map and `RecoveryBoundaryTest`, the `recoveryCoverageVerification` four-counter task. Build Sequence v6 places TE-001 at order 2 and this story at order 7; D-RUN-17 fixes the wave-A order (TE-001 before E1-044), and the same package dependency makes TE-001 the precondition here. TASK-00 stops the run if the merged layout differs. |
| Code base | This repository as read on 18 Nov 2026 (`backend/`, `infra/`, `scripts/`, `.env.example`, `docker-compose.yml`, `README.md`, `.gitlab-ci.yml`) and the TE-001 plan v7 with its `data-model.md`. No git command was run; this workspace is not a git repository. |
| Builder | Implementation Builder, in its own git worktree on `feature/RWB-TE-012-document-storage`, commits `RWB-TE-012: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers. |
| Smallest change | One ARM template with its parameter files and one pre-deploy check, one runbook, the single `dochub.api` write path, the P5 adapter/readiness/audit classes, the local emulator path, and the configuration and local-stack edits the story names. No endpoint, no migration, no new dependency, no second adapter or store. |
| Work type split | **Code:** 19 Java main classes (7 `dochub.api`, 12 `dochub.storage`) and 21 test files (18 new including one helper, 2 edited, 1 deleted). **Templates:** 1 ARM JSON template, 1 required-input schema, 1 synthetic local parameter file, 4 environment parameter files. **Scripts and local configuration:** `Test-DeployParameters.ps1`, `scripts/dev.ps1`, `.env.example`, `docker-compose.yml`. **Pipeline:** none added; `.gitlab-ci.yml` unchanged (DGAP-24; A-09 owned by RWB-TE-003/RWB-TE-011). **Docs and build:** `RUNBOOK.md`, two README edits, one build comment. **Builder-verified external CLI evidence:** BE-01 to BE-13, the DEV and SIT template applies, the DGAP-03 DEV spike, the SIT test cases and the RW-SECADM role listing; none of these is automated here and none is claimed as executed by this stage. |

## Upstream readiness

| Check | Result |
|---|---|
| Spec status | `SUCCESS` (front matter and "Status reporting") |
| Spec gate | `PASS` round 10, no open finding (`../review/spec-gate-review-10.md`) |
| Clarification log | 26 `CLAR-*` rows, all `RESOLVED`; `CLARIFICATION_STATUS: RESOLVED`; no `OPEN` row |
| Requirement coverage | `MISSING_RULES: 0`, `CONTRADICTIONS: 0`; 37 rows |
| Document gaps | 23 active rows (DGAP-01 to -17, -19 to -24), DGAP-18 withdrawn; **no blocker**. The external citations SG-43/SG-44 use are Microsoft Learn pages, not document-set gaps |
| Design evidence | `NOT_REQUIRED` (UI In Scope NO): no screenshot, per-screen, visual-fidelity or component-inventory requirement |
| Migration | None. SPEC-016 says no data migration and D-RUN-07 is not exercised; no `V<seq>` file is planned |
| Precondition | RWB-TE-001 merged (TASK-00 verifies the merged layout before anything is written) |

`PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]`. The spec's shared open items (template values, SY-OCR identity, SCR-44 owner, DGAP-03 spike) are open-item rows, not `CLAR-*` items; none blocks this plan.

## Work type classification (what is code, what is not)

| Work | Kind | Where | How it is verified |
|---|---|---|---|
| Storage account, four containers, versioning and soft delete, legal policy, six container-scope role assignments, private endpoint | **Infrastructure template** (ARM JSON, parameter files, required-input list) | `infra/azure/document-storage/` | Unit test T-TE012-15 (structure and per-file values, no undecided value); template apply in DEV and SIT (external) |
| Refuse a deployment while an input is undecided or the environment binding is wrong; print the report and the exact deploy command | **Script** (PowerShell, the tool `scripts/dev.ps1` already uses; no new tool) | `infra/azure/document-storage/Test-DeployParameters.ps1` | Deterministic stage-1 runs (local file, placeholder, mode) with no Azure call; BE-01 to BE-13 on disposable DEV resources (external CLI) |
| Apply, PROD lock, Extend, DEV spike, evidence | **Document / operational procedure** | `infra/azure/document-storage/RUNBOOK.md` | Plan-gate review; TASK-23 checklist; the PROD steps are approved with the PROD deploy |
| Published write path, adapter, readiness, health, audit, hash guard, emulator | **Java code** | `dochub.api`, `dochub.storage` | Unit tests T-TE012-01 to -18; Azurite integration tests; coverage gate |
| Properties and flag | **Java code + YAML configuration** | `DocumentStorageProperties`, `application.yaml`, `application-local.yaml` | T-TE012-01, T-TE012-13 |
| Local `.env` healing and Docker wiring | **Script + configuration** | `.env.example`, `docker-compose.yml`, `scripts/dev.ps1` | Builder `.env` upgrade evidence; TASK-21 `dev.ps1 test` |
| Build comment and code-tree line | **Build file + document** | `backend/build.gradle.kts:60`, `README.md:25` and "Decisions taken" | Diff review (TASK-19, TASK-23) |
| Pipeline | **None** | `.gitlab-ci.yml` untouched | `.gitlab-ci.yml` has no infrastructure stage (DGAP-24); A-09 CI wiring belongs to RWB-TE-003/RWB-TE-011; the new integration cases run through `./scripts/dev.ps1 it` (ASM-TE012-23) |
| Azure reads and writes against a real account | **Builder-verified external CLI evidence** | Disposable DEV resources, then DEV/SIT | BE-01 to BE-13 with printed reports; DEV and SIT applies; SIT TCs 01 to 12 (PENDING_ENVIRONMENT) |

## Scope

Each bullet maps to tasks in `tasks.md` (see "Scope bullet to task map" there).

1. **S-1 Template:** `azuredeploy.json` with the account settings of SPEC-001, the four private containers of SPEC-002, versioning and soft delete of SPEC-003, the conditional legal policy of SPEC-004 and the six container-scope role assignments of SPEC-005; `azuredeploy.parameters.schema.json`, `azuredeploy.local.parameters.json` and the four environment files. → TASK-01, TASK-02
2. **S-2 Pre-deploy check:** two stages, printed report on every outcome, six explicit inputs, the "no policy" rows 1–7, incremental mode only, local file refused. → TASK-03
3. **S-3 Runbook:** Apply, PROD lock, Extend, later PROD applies, the DGAP-03 DEV spike and the evidence each step leaves. → TASK-04
4. **S-4 Published surface:** `DocumentStorage`, `BlobRef`, `BlobWriteRequest`, `StoredBlob`, `StorageReadiness`, `WriteOnceViolationException`, `StorageUnavailableException`; exact `dochub.api` list in T-TE001-14. → TASK-05, TASK-06, TASK-16
5. **S-5 Properties and flag:** `DocumentStorageProperties` binds and validates `rwb.dochub.*`; `rwb.blob` removed; flag off needs no URL. → TASK-07, TASK-08
6. **S-6 Containers and credentials:** `DocumentContainers`, `DocumentContainersConfig`, two managed-identity clients, 10 s operation timeout, no create outside the emulator bootstrap. → TASK-09, TASK-10
7. **S-7 Local emulator:** five-condition guard, one shared-key client, four containers created inside the probe deadline, `EMULATED` identity and policy, startup neither fails nor waits when Azurite is down. → TASK-09, TASK-10
8. **S-8 Readiness and health:** single-flight probe with the `timeout-seconds` deadline, `readiness-recheck-seconds` reuse, `documentHub` health component, `UNKNOWN`/`UP`/`DOWN`, not in liveness or readiness. → TASK-09, TASK-10, TASK-15, TASK-16
9. **S-9 Errors and audit:** `StorageErrorMapper` rows, `DOCUMENT_CHANGE_REFUSED` with its fields, no readiness write from the mapper. → TASK-11, TASK-12
10. **S-10 Hash guard:** same hash returns the existing blob, different hash is a violation, metadata absent is downloaded, one re-compare after `BlobAlreadyExists`. → TASK-13, TASK-14
11. **S-11 Store and open:** validation before any storage call, intake and D-RCV-31 re-store sources, standard and legal routing, `open()` allow-list, `BLOB_MISSING`. → TASK-15, TASK-16
12. **S-12 Integration evidence:** Azurite `recovery-it` cases, `RecoveryDatabaseIT` without line 61, the HTTP stub cases, the isolation and single-flight cases. → TASK-15, TASK-16, TASK-17
13. **S-13 Local stack and baseline evolution:** `.env.example`, `docker-compose.yml`, `scripts/dev.ps1`, `application*.yaml`, the `build.gradle.kts` comment and the README edits; no baseline class remains. → TASK-08, TASK-18, TASK-19
14. **S-14 Verification, external evidence and handover:** unit suite, coverage gate with per-class and no-drop checks, regression, the Builder external evidence, the scope/guardrail check and the SIT/PROD handover. → TASK-20, TASK-21, TASK-22, TASK-23, TASK-24

## Out of scope and seams (D-RUN-08, SPEC-019)

Not built here: the document record, RWB-E1-024's own `DocumentStore`, `StoreRequest` and `StoredDocument` interfaces, the type-to-`writeOnce` choice, `replaceContent` → 409 MSG-P5-002 and the HTTP 503 mapping (RWB-E1-024, order 42); the upload endpoint and TC-TE-012-13 (RWB-E1-026, order 58); intake writes and `IntakeService` (RWB-E1-026/-057); the quarantine mover and scan (RWB-E1-041, order 54); OCR reads (RWB-E1-049); the legal re-store caller step (RWB-E1-032/-054, DGAP-23); the archive container expected by RWB-E1-017 (DGAP-22); retention classes and JOB-17; legal hold; backup/restore; sizing and cost; the SCR-44 screen (DGAP-20, no owner story). Each is a seam row in SPEC-019 and a note in `shared-updates.md` §6; no task depends on an unmerged story.

## One-module check

AGENTS.md §7 and §9 ask that a plan "touches one module". For this build that rule is read as the ACE module, the recovery module, as settled by D-RUN-21 (18 Nov 2026 05:36; ratification pending under OPEN-050, `aisdlc/docs/open-items.md`). This plan changes P5 `dochub` only. `infra/azure/document-storage/`, `scripts/dev.ps1`, `.env.example`, `docker-compose.yml`, `README.md`, `backend/build.gradle.kts` and `application*.yaml` are repository-level files the story itself names (`[S]` §13, §21); they are not another ACE module. No common or collection code, and no other design module, is touched. Under the alternative design-module reading the plan still touches one design module (P5) plus those repository files, so it passes either reading. Gap PG-03 keeps the definition gap visible for the document owners; Blocker = No.

## Carried plan inputs

| Input | Content | Where applied |
|---|---|---|
| D-RUN-17 | TE-001 merges before RWB-E1-044 in wave A; migration numbering is unaffected. TE-012's own precondition is TE-001 merged (Build Sequence v6 order 2 before order 7, and the package dependency). | TASK-00 reads the merged layout; all paths below assume it |
| D-RUN-19 | Parameter reads from outside P3 go through a P4 `access.api` interface implemented in P3. TE-012 reads **no** parameter catalog row; its values are Spring configuration (`rwb.dochub.*`), the flag and template parameters. No P4/P3 edge is added. | "Configuration properties"; TASK-08 |
| D-RUN-21 | "Touches one module" means the ACE module (recovery). | "One-module check"; PG-03 |
| D-RUN-07 | No migration number is fixed. | No migration; SPEC-016 |
| Spec gate round-10 editorial notes | (a) ASM-33's basis still lists `az storage container-rm show`; no `show` is used. (b) BE-10 must name the input that holds the placeholder. (c) The printed raw outputs are what the "rows 2 and 4" expectations are checked against. (d) `legal-container.json` is per apply: the runbook says to use a per-run report folder. (e) A container-parameter mismatch with `rwb.dochub.container.*` fails safe through `CONTAINER_MISSING:<name>`. | BE table in `tests/scenarios.md`; check report format in `data-model.md` §10; RUNBOOK note; T-TE012-14 |

## Plan-time verification (read only, 18 Nov 2026)

| Item | Source or command | Result |
|---|---|---|
| TE-001 plan v7 and its conventions | `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/plan.md`, `tasks.md`, `data-model.md` | Read. Package layout `dochub.api` / `dochub.storage`, the `recoveryCoverageVerification` four-counter task, test-first red/green task pairs and the "every row has six cells" style are the model for this plan |
| Baseline document code | `backend/src/main/java/th/co/scb/ace/demo/recovery/documents/api/DocumentStore.java`, `.../documents/internal/BlobDocumentStore.java` | Read. Nested `Config`, `BlobProperties` (`rwb.blob`), `createIfNotExists()` on first write, `DefaultAzureCredential`, `If-None-Match: *`, no timeout |
| Callers of `DocumentStore` | `Select-String -Pattern "DocumentStore"` over `backend/src` | Only the interface, its implementation, the build comment and `RecoveryProperties`' Javadoc. No caller |
| New names not present yet | `Select-String -Pattern "DocumentStorage\|rwb\.dochub\|BlobStorageAdapter\|DocumentContainers"` over `backend/src` | None. TE-001's `RecoveryProperties` is split by its TASK-11, so the `rwb.blob` Javadoc reference disappears with it |
| `infra/azure` | `Test-Path infra/azure` | `False`. The template folder is new |
| Integration-test path convention | `RecoveryDatabaseIT.java:34` | `Path.of("..", "infra", "postgres")` from `backend/`. `StorageTemplateConformanceTest` uses the same convention for `../infra/azure/document-storage` |
| `.env.example` keys | `Get-Content .env.example` with line numbers | `RWB_BLOB_CONNECTION_STRING` at line 23, `RWB_BLOB_CONNECTION_STRING_DOCKER` at line 24; no `RWB_DOCHUB_*` key |
| Docker backend key | `docker-compose.yml:135` | `RWB_BLOB_CONNECTION_STRING: ${RWB_BLOB_CONNECTION_STRING_DOCKER}` |
| Build comment | `backend/build.gradle.kts:60` | `// so the SDK is wired directly in DocumentStorageConfig.` |
| Integration test line | `RecoveryDatabaseIT.java:61` | `registry.add("rwb.blob.connection-string", () -> "UseDevelopmentStorage=true");` |
| README line | `README.md:25` | `documents/             Azure Blob DocumentStore, write-once container for legal types` |
| `dev.ps1` | `scripts/dev.ps1` lines 28–42, 86–87, 114–118 | `Initialize-EnvFile` copies `.env.example` only when `.env` is absent, then generates the codec key; every command calls it; `test` = `gradlew test` + `npm run check`; `it` = `gradlew recoveryIntegrationTest` |
| Actuator | `application.yaml` lines 39–49 | `health` exposed, `show-details: when-authorized`, `roles: RW-PLATADM`, probes enabled; no group includes a custom component |
| Virtual threads | `application.yaml` lines 8–10 | `spring.threads.virtual.enabled: true` |
| Jackson | `ProblemFactory.java:14` | Jackson 3 `tools.jackson.databind.json.JsonMapper`; the template test uses the same library, no JSON-schema library |
| Azure SDK | `backend/build.gradle.kts` | `azure-storage-blob 12.37.2`, `azure-identity 1.19.0`. `javap` confirms `BlobContainerProperties.hasImmutabilityPolicy()`, `BlobContainerClient.getPropertiesWithResponse(String, Duration, Context)`, `BlobClientBase.uploadWithResponse(BlobParallelUploadOptions, Duration, Context)`, `downloadContentWithResponse(DownloadRetryOptions, BlobRequestConditions, Duration, Context)` and the public `ChainedTokenCredentialBuilder` (the `ChainedTokenCredential` constructor is package-private, hence the `Credentials` seam in PA-04) |
| Spring Boot health | `spring-boot-health-4.1.2.jar` via `javap` | Boot 4.1 moved health to `org.springframework.boot.health.actuate.endpoint`; `HealthEndpoint.health()`, `HealthEndpointGroups.get(String)`, `HealthEndpointGroup.isMember(String)`, `SimpleStatusAggregator`, `SimpleHttpCodeStatusMapper` exist. The plan names the new package; the Builder imports from the jar, not from memory |
| Testcontainers | `backend/build.gradle.kts` lines 77–80 | `testcontainers-junit-jupiter`, `testcontainers-postgresql`; core is present transitively. `GenericContainer` needs no new dependency |
| Azurite image | `docker-compose.yml:98–104` | `mcr.microsoft.com/azure-storage/azurite:3.37.0`, `azurite-blob --skipApiVersionCheck`, port 10000 |
| CI | `.gitlab-ci.yml` | 3 jobs (`backend-unit`, `frontend-check`, `backend-recovery-it`). `backend-recovery-it` rules cover `backend/src/main/resources/db/**`, `RecoveryFlywayConfig.java` and `infra/postgres/**` only, plus a schedule; this MR touches none of them. Local `./scripts/dev.ps1 it` is the evidence (ASM-TE012-23); a CI rule for `infra/azure/**` is proposed as an open item, not changed here (A-09) |
| Existing tests | `backend/src/test` | 8 classes, none at `dochub/**` yet (TE-001 adds `BlobDocumentStoreTest` and moves the others). T-TE012-14 redistributes its assertions |
| Frontend | `frontend/` exists; no file is planned | UI In Scope NO |

## Backend Plan

Surface status: **CHANGED**. Unit tests **REQUIRED** (Trace: SPEC-001..-023; AC1–AC12; BR1–BR7). Gate: `./gradlew test recoveryCoverageVerification` in `backend/`, LINE, INSTRUCTION, BRANCH, METHOD each ≥ 0.80 over the `recovery/**` bundle plus the TE-001 tooling, no exclusion, `test` execution data only; plus per-class ≥ 0.80 under `recovery/dochub/**` and no bundle counter below the TASK-00 snapshot (SPEC-023; TE-001 SPEC-020).

### Files added or changed (backend, template, scripts, docs)

Paths are relative to the repository root. `SPEC-nnn` is `SPEC-RWB-TE-012-nnn`. Every file the story adds or changes is listed; "unchanged" rows are evidence only.

| Kind | Path | Task | SPEC | Work type |
|---|---|---|---|---|
| Add | `infra/azure/document-storage/azuredeploy.json` | TASK-02 | 001–005 | Template |
| Add | `infra/azure/document-storage/azuredeploy.parameters.schema.json` | TASK-02 | 001 | Template |
| Add | `infra/azure/document-storage/azuredeploy.local.parameters.json` | TASK-02 | 001 | Template (synthetic, never applied) |
| Add | `infra/azure/document-storage/azuredeploy.dev.parameters.json` | TASK-02 | 001 | Template |
| Add | `infra/azure/document-storage/azuredeploy.sit.parameters.json` | TASK-02 | 001 | Template |
| Add | `infra/azure/document-storage/azuredeploy.uat.parameters.json` | TASK-02 | 001 | Template |
| Add | `infra/azure/document-storage/azuredeploy.prod.parameters.json` | TASK-02 | 001 | Template |
| Add | `infra/azure/document-storage/Test-DeployParameters.ps1` | TASK-03 | 001 | Script |
| Add | `infra/azure/document-storage/RUNBOOK.md` | TASK-04 | 004 | Document |
| Add | `infra/azure/document-storage/.gitignore` (`reports/`) | TASK-03 | 001 | Configuration |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/DocumentStorage.java` | TASK-06 | 010, 022 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/BlobRef.java` | TASK-06 | 010 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/BlobWriteRequest.java` | TASK-06 | 010 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/StoredBlob.java` | TASK-06 | 010 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/StorageReadiness.java` | TASK-06 | 010 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/WriteOnceViolationException.java` | TASK-06 | 010 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/StorageUnavailableException.java` | TASK-06 | 010 | Code |
| Unchanged | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/package-info.java` | — | 022 | Code (TE-001 file) |
| Delete | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/DocumentStore.java` | TASK-16 | 016 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentStorageProperties.java` | TASK-08 | 006 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentClients.java` | TASK-10 | 007, 008 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentContainers.java` | TASK-10 | 008 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentContainersConfig.java` | TASK-10 | 007, 008, 017 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageReadinessIndicator.java` | TASK-10 | 009, 020 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/ReadinessProbe.java` | TASK-10 | 009 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/ContainerReadinessProbe.java` | TASK-10 | 009, 017 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/LocalEmulatorBootstrap.java` | TASK-10 | 017 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageErrorMapper.java` | TASK-12 | 013 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentAuditLog.java` | TASK-12 | 014 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/ContentHashGuard.java` | TASK-14 | 012 | Code |
| Add | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobStorageAdapter.java` | TASK-16 | 011, 015, 010 | Code |
| Edit | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentContainersConfig.java` (declare the `DocumentStorage` bean) | TASK-16 | 010 | Code |
| Delete | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobDocumentStore.java` | TASK-16 | 016 | Code |
| Edit | `backend/src/main/resources/application.yaml` (remove `rwb.blob` lines 98–102, add `rwb.dochub`) | TASK-08 | 006, 016 | Configuration |
| Edit | `backend/src/main/resources/application-local.yaml` (flag, `emulator`, `emulator-connection-string`) | TASK-08 | 006, 017 | Configuration |
| Edit | `.env.example` (rename the two Blob keys) | TASK-18 | 021 | Script/configuration |
| Edit | `docker-compose.yml:135` (rename the backend variable) | TASK-18 | 021 | Configuration |
| Edit | `scripts/dev.ps1` (`Initialize-EnvFile` append-missing-keys loop) | TASK-18 | 021 | Script |
| Edit | `backend/build.gradle.kts:60` (comment only: `DocumentContainersConfig`) | TASK-19 | 016 | Build |
| Edit | `README.md:25` and "Decisions taken while setting this up" item (b) (`shared-updates.md` §5) | TASK-19 | 021 | Document |
| Unchanged | `.gitlab-ci.yml`, `frontend/**`, `infra/postgres/**`, `backend/src/main/resources/db/**`, `AceRecoveryApplication.java`, `backend/build.gradle.kts` dependencies and JaCoCo tasks | — | 016, 018, 023 | — |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/api/BlobRefTest.java` | TASK-05 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentStoragePropertiesTest.java` | TASK-07 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentContainersConfigTest.java` | TASK-09 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageReadinessIndicatorTest.java` | TASK-09 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentHealthAggregateTest.java` | TASK-09 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/LocalEmulatorBootstrapTest.java` | TASK-09 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/LocalProfileStartupTest.java` | TASK-09 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageErrorMapperTest.java` | TASK-11 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/DocumentAuditLogTest.java` | TASK-11 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/ContentHashGuardTest.java` | TASK-13 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobStorageAdapterStoreTest.java` | TASK-15 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobStorageAdapterOpenTest.java` | TASK-15 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobStorageAdapterHttpStubTest.java` | TASK-15 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageReadinessProbeTest.java` | TASK-15 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/ReadinessIsolationTest.java` | TASK-15 | 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageTemplateConformanceTest.java` | TASK-01 | 001–005, 018 | Test |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/AzuriteDocumentStorageIT.java` | TASK-15 | 018 | Test (integration) |
| Add | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/StorageTestSupport.java` (emulator runner, connection string builder, mutable clock) | TASK-09 | 018 | Test helper |
| Edit | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java` (`dochub.api` expected list; T-TE001-14) | TASK-15 | 022, 016 | Test |
| Edit | `backend/src/test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java` (delete line 61) | TASK-17 | 016, 018 | Test (integration) |
| Delete | `backend/src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/BlobDocumentStoreTest.java` (successors written first in TASK-15) | TASK-16 | 018 | Test |

### Published surface (`dochub.api`, SPEC-010, SPEC-022)

```java
package th.co.scb.ace.demo.recovery.dochub.api;

public interface DocumentStorage {
    StoredBlob store(BlobWriteRequest request);
    byte[] open(BlobRef ref);
    StorageReadiness readiness();
}
public record BlobRef(String container, String blobName) {
    public String storageRef();
    public static BlobRef fromStorageRef(String storageRef);
}
public record BlobWriteRequest(UUID caseId, UUID documentId, int docVersion, boolean writeOnce, BlobRef source) { }
public record StoredBlob(BlobRef ref, String sha256, long size, boolean existing) { }
public record StorageReadiness(boolean ready, List<String> reasons, Instant checkedAt) { }
public class WriteOnceViolationException extends RuntimeException { }
public class StorageUnavailableException extends RuntimeException {
    public enum Reason { NOT_READY, TIMEOUT, UNAVAILABLE, ACCESS_REFUSED, BLOB_MISSING }
}
```

No `com.azure.storage` type in `dochub.api`. `package-info.java` keeps `@NamedInterface(name = "api", propagate = false)` from TE-001. The final state deletes `DocumentStore` (TASK-16); TASK-06 adds the new types first so the tree keeps compiling, and TASK-15 moves T-TE001-14's expected list to the final set.

### Storage package design (`dochub.storage`, package-private except where stated)

| Class | Responsibility | Public? |
|---|---|---|
| `DocumentStorageProperties` | `@ConfigurationProperties("rwb.dochub")`; nested `Storage` and `Container` records; validates every startup rule of the properties table that is a property rule; names the emulator environment variable in its message | no |
| `DocumentClients` | Immutable holder of the four `BlobContainerClient`s; `enabled` and an absent quarantine client are explicit | no |
| `DocumentContainers` | `intake()`, `standard()`, `legal()`, `quarantine()`, `readiness()`; flag off or a missing OCR client throws `StorageUnavailableException(NOT_READY)` with no storage call | yes (P5, non-published) |
| `DocumentContainersConfig` | `@Configuration(proxyBeanMethods = false)`; `@EnableConfigurationProperties`; flag-on client beans (`serviceBlobServiceClient`, and `ocrBlobServiceClient` only when its client ID is set), the emulator shared-key client bean, `DocumentClients`, `LocalEmulatorBootstrap` (property-conditional), `ContainerReadinessProbe`, the single `StorageReadinessIndicator` bean named `documentHub` (one `HealthIndicator`, no second contributor), `DocumentContainers`, `DocumentStorage` (TASK-16), the mapper, guard and audit beans; validates the `local` profile rule; exposes `static Credentials credentialChain(String clientId)` for T-TE012-02 | no |
| `StorageReadinessIndicator` | Implements `HealthIndicator`; is the single bean named `documentHub`; holds the state of the transition matrix, the single-flight `CompletableFuture`, the `readiness-recheck-seconds` window, the `Clock`, the virtual-thread executor and the `ApplicationReadyEvent` listener; only the probe writes the state | no |
| `ReadinessProbe` | Interface `Result probe()`; nested `Result(StorageReadiness readiness, Map<String,String> containers, String legalPolicy, Map<String,String> identities)`; the stub seam for T-TE012-09 | no |
| `ContainerReadinessProbe` | One probe: emulator bootstrap first, four container checks in parallel with virtual threads, legal `hasImmutabilityPolicy`, OCR client-ID check, one deadline of `timeout-seconds`, each SDK call gets the time left | no |
| `LocalEmulatorBootstrap` | Creates the four containers (`createIfNotExists`) inside the probe deadline; one WARN on failure; never fails or delays startup | no (bean only in emulator mode) |
| `StorageErrorMapper` | SPEC-013 rows; requests one background probe only for `TIMEOUT`, transport `UNAVAILABLE` and `ContainerNotFound`; never writes readiness | no |
| `DocumentAuditLog` | One structured `DOCUMENT_CHANGE_REFUSED` line on `recovery.audit`, with the SPEC-014 fields; no content, URL or client ID | no |
| `ContentHashGuard` | Reads the existing legal blob's `sha256` metadata, downloads and hashes when absent, returns the existing blob on equality, throws `WriteOnceViolationException` plus `HASH_MISMATCH` on difference, re-compares once after `BlobAlreadyExists` | no |
| `BlobStorageAdapter` | Implements `DocumentStorage`; validates before any storage call, enforces readiness, copies from intake (or the D-RCV-31 standard source), routes standard or legal, sets metadata and content type, maps errors; `open()` allow-list; never deletes the source | no |

Break of the construction cycle: `DocumentClients` → `ContainerReadinessProbe` → `StorageReadinessIndicator` → `DocumentContainers`; `DocumentContainers` does not feed the probe. No `@Lazy` and no setter wiring.

### Baseline evolution (SPEC-016) — no baseline class remains beside its successor

| Baseline after RWB-TE-001 | Successor | Task |
|---|---|---|
| `dochub.api.DocumentStore` | `DocumentStorage` + the six records/exceptions | TASK-06, TASK-16 |
| `DocumentStore.StoredDocument` | `StoredBlob` and `BlobRef` | TASK-06 |
| `DocumentStore.DocumentImmutableException` | `WriteOnceViolationException` | TASK-06 |
| `dochub.storage.BlobDocumentStore` | `BlobStorageAdapter` | TASK-16 |
| nested `BlobDocumentStore.Config` | `DocumentContainersConfig` | TASK-10 |
| nested `BlobDocumentStore.BlobProperties` (`rwb.blob`) | `DocumentStorageProperties` (`rwb.dochub`) | TASK-08 |
| containers `rwb-documents`, `rwb-documents-legal` | `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` | TASK-02, TASK-08 |
| blob name = document UUID | `{caseId}/{documentId}/v{docVersion}` | TASK-16 |
| `createIfNotExists()` at first write | only `LocalEmulatorBootstrap` | TASK-10 |
| `DefaultAzureCredential` full chain | workload + managed identity chain | TASK-10 |
| no timeout | `timeout-seconds` on every SDK call | TASK-10, TASK-16 |
| `If-None-Match: *` alone | behind `ContentHashGuard` | TASK-14, TASK-16 |
| `BlobDocumentStoreTest` | successors in T-TE012-04, -05, -06, -07, written first in TASK-15; the obsolete runtime-creation assertion has no successor (SPEC-007); deleted in TASK-16 | TASK-15, TASK-16 |
| `application.yaml` `rwb.blob` block | `rwb.dochub` block | TASK-08 |
| `RecoveryDatabaseIT.java:61` | deleted; the flag-off P5 context needs no storage property | TASK-17 |
| `build.gradle.kts:60` comment | names `DocumentContainersConfig` | TASK-19 |
| `.env.example:23`, `:24`, `docker-compose.yml:135`, `scripts/dev.ps1` | `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` family and the append-missing-keys loop | TASK-18 |
| `README.md:25` | the P5 `dochub/` line and the "Decisions taken" item (b) | TASK-19 |

Containers `rwb-documents` and `rwb-documents-legal` held no data outside local Azurite volumes; no data migration is planned or needed.

### Configuration properties (SPEC-006)

| Property | `application.yaml` | `application-local.yaml` | Rule and source |
|---|---|---|---|
| `rwb.dochub.storage-containers` | `${RWB_DOCHUB_STORAGE_CONTAINERS:false}` | `true` | Flag; off → no client, every accessor and `store`/`open` refuse NOT_READY, `readiness()` FLAG_OFF (`[S]` §13) |
| `rwb.dochub.storage.account-url` | `${RWB_DOCHUB_ACCOUNT_URL:}` | — | Required and `https://` only when the flag is on and emulator is false |
| `rwb.dochub.storage.timeout-seconds` | `10` | `10` | Integer 1–60; per SDK call, retries included; probe deadline and caller wait (`[S]` §13, AC10) |
| `rwb.dochub.storage.readiness-recheck-seconds` | `30` | `30` | Integer 1–300; NOT_READY reuse window (ASM-TE012-30) |
| `rwb.dochub.storage.service-identity-client-id` | `${RWB_DOCHUB_SERVICE_MI_CLIENT_ID:}` | — | ACE identity client ID; blank uses the default managed identity (ASM-TE012-05) |
| `rwb.dochub.storage.ocr-identity-client-id` | `${RWB_DOCHUB_OCR_MI_CLIENT_ID:}` | — | SY-OCR client ID; blank → NOT_READY `IDENTITY_NOT_CONFIGURED:rwb-quarantine`; not used in emulator mode |
| `rwb.dochub.storage.emulator` | `false` | `true` | Emulator mode only with the five conditions (SPEC-017) |
| `rwb.dochub.storage.emulator-connection-string` | absent | `${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}` | Used only when `emulator` is true |
| `rwb.dochub.container.intake` | `rwb-intake` | same | `[S]` §4, §13 |
| `rwb.dochub.container.standard` | `rwb-docs` | same | `[S]` §4, §13; FSD P5 |
| `rwb.dochub.container.legal` | `rwb-docs-legal` | same | `[S]` §4, §13; D-RCV-31 |
| `rwb.dochub.container.quarantine` | `rwb-quarantine` | same | `[S]` §4, §13; E1-041 |

Startup fails for: emulator true without the `local` profile; four names not distinct or outside 3–63 lower-case/digit/hyphen; timeout outside 1–60; recheck outside 1–300; flag on, emulator false, account URL blank or not https; emulator false with an emulator string; emulator true with an account URL. The `rwb.blob` block is removed. No container, period or timeout is a Java literal.

### Infrastructure template and parameter files (SPEC-001 to SPEC-005, T-TE012-15)

| File | Content |
|---|---|
| `azuredeploy.json` | ARM JSON, no compile step. `storageAccountName` (no default, 3–24 `^[a-z0-9]{3,24}$`), `location`, `skuName`, `accessTier`, `privateEndpointSubnetId`, `aceServicePrincipalId`, `ocrPrincipalId`, `deployLegalPolicy` (no defaults); container names with defaults `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine`; `legalRetentionDays` 3650; `softDeleteDays` 30. Account: `allowSharedKeyAccess: false`, `publicNetworkAccess: Disabled`, `minimumTlsVersion: TLS1_2`, `supportsHttpsTrafficOnly: true`, `allowBlobPublicAccess: false`, `kind: StorageV2`, SKU and tier from parameters. Blob service: `isVersioningEnabled: true`, `deleteRetentionPolicy` days `softDeleteDays`. Four containers with `publicAccess: None`. Private endpoint with `groupIds: ["blob"]` on `privateEndpointSubnetId`. Conditional `immutabilityPolicies` child on `legalContainerName`, `immutabilityPeriodSinceCreationInDays` `legalRetentionDays`, `allowProtectedAppendWrites: false`, `condition` on `deployLegalPolicy`; no lock parameter or property. Six `roleAssignments` at container scope (3 ACE, 3 SY-OCR); no account-scope data role. |
| `azuredeploy.parameters.schema.json` | `requiredInputs`: one object per required input with `name`, `type`, `pattern`, `owner`, `neededBy`; the eight names above. Plain JSON read with Jackson 3; no JSON-schema library. |
| `azuredeploy.local.parameters.json` | Synthetic shape-valid values for all eight inputs (all-zero subscription GUID in the subnet ID, `location` `conformance`, account `rwbconformance001`, SKU `Standard_LRS`, tier `Hot`, UUID-shaped zero principals, `deployLegalPolicy` false). Used only by T-TE012-15; the check refuses it. |
| `azuredeploy.<env>.parameters.json` (dev, sit, uat, prod) | Every schema input; each value is a decided value or exactly `__SET_BEFORE_APPLY__`. `deployLegalPolicy` is `true` in DEV, SIT, UAT and `false` in PROD. UAT and PROD hold placeholders for every undecided value; the plan chooses none of them. |
| `.gitignore` | `reports/` (the check's per-run report folders are evidence, not source) |

### Pre-deploy check and runbook (SPEC-001, SPEC-004)

`Test-DeployParameters.ps1` takes `-Environment`, `-ResourceGroup`, `-StorageAccountName`, `-ParameterFile`, `-Mode`, `-DeployLegalPolicy`. All six are received as strings and validated by the check itself, so a wrong value produces the printed refusal instead of a PowerShell binding error; `-DeployLegalPolicy` must be exactly `true` or `false` and is parsed explicitly (a `[bool]` parameter would treat the string `false` as true), and `-Mode` must be exactly `Incremental`. Stage 1 (local, always first, no Azure call) refuses a wrong environment or file-name mismatch, a missing/blank/placeholder/shape-invalid schema input, an invalid container-name parameter, a mode other than `Incremental`, a resource group outside 1–90 characters, or an account name that differs from the file. Stage 2 (only PROD with effective `true`) runs the three "no policy" reads and follows rows 1–7. It prints the report defined in `data-model.md` §10 on every outcome and, on accept, the one deploy command with the effective value and incremental mode. Reports and `legal-container.json` go to `reports/<environment>-<yyyyMMddTHHmmssZ>/` under the script folder (PA-09).

`RUNBOOK.md` sections: **Apply** (step 1 the check, step 2 the printed command, step 3 the report with the apply record), **PROD lock** (RW-PLATADM, in the change window after the apply and before the flag, approved with the PROD deploy, evidence `immutability-policy show` on the printed `<legal>`), **Extend** (increase only, at most five over the policy life, same approval, no shortening or removal), **Later PROD applies** (PROD file `false`, incremental mode, policy untouched), **DEV spike (DGAP-03)** (apply with the policy once and then skip it in incremental mode; confirm the unlocked policy is unchanged; never lock or extend outside PROD), and **Report handling** (per-run folder; do not reuse `legal-container.json`).

### Local stack and scripts (SPEC-021, ASM-TE012-22)

`.env.example:23` and `:24` become `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` and `..._DOCKER` with the same values. `docker-compose.yml:135` passes the Docker value to the renamed key. `scripts/dev.ps1` `Initialize-EnvFile` gains, between the copy-when-absent block and the codec-key block, a loop over each `KEY=` line in `.env.example` that appends the line when the key is absent from `.env` and prints `Added <KEY> to .env from .env.example`; existing lines are never changed or removed, and the codec-key step is unchanged. Old `RWB_BLOB_*` lines left in an existing `.env` are unused and harmless.

### Tests (SPEC-018)

All unit tests are JUnit 5, Mockito, AssertJ and `ApplicationContextRunner`; no Docker, database or external network; random UUIDs and generated bytes only; each class Javadoc names RWB-TE-012 and its purpose. `StorageTestSupport` holds the emulator runner, the runtime-built `devstoreaccount1` connection string (random Base64 key per run) and a mutable clock; no key is committed.

| ID | Class | Cases | Task |
|---|---|---|---|
| T-TE012-01 | `DocumentStoragePropertiesTest` | Defaults (10, 30, four names, flag false, emulator false); every property-rule startup failure; flag off needs no URL. The `local`-profile rule cannot be evaluated inside a properties record, so T-TE012-02 asserts it; together the two cover every startup rule of the properties table | TASK-07, TASK-08 |
| T-TE012-02 | `DocumentContainersConfigTest` | Flag off: no client bean, `DocumentContainers` present, every accessor NOT_READY, `readiness()` FLAG_OFF (the `DocumentStorage` bean clause is asserted by T-TE012-04 after TASK-16); flag on: two named clients, the `Credentials` chain is exactly workload then managed identity with the configured client ID, no create call; emulator guard: each of the five conditions false in turn, all true → one shared-key client | TASK-09, TASK-10 |
| T-TE012-03 | `BlobRefTest` | `storageRef()`; round trip for a document and an intake name; null, blank, no `/`, bad container, over 400 characters; document name format and length bound | TASK-05, TASK-06 |
| T-TE012-04 | `BlobStorageAdapterStoreTest` | Standard routing and overwrite; legal routing with `If-None-Match: *`; metadata `sha256` and content type; `existing=false`; source not deleted; D-RCV-31 re-store; every refused source with `IllegalArgumentException` and zero interactions; flag off NOT_READY with zero interactions; probe NOT_READY refuses with no download or upload; the configured timeout reaches every SDK call | TASK-15, TASK-16 |
| T-TE012-05 | `ContentHashGuardTest` | Same hash → existing, no upload; different → violation plus `HASH_MISMATCH`; metadata absent → download and hash; `BlobAlreadyExists` → one re-compare; client-timeout-then-retry → `existing=true` | TASK-13, TASK-14 |
| T-TE012-06 | `StorageErrorMapperTest` | Every SPEC-013 row, including an unexpected code and an unparsable response rethrown unchanged; exactly one background probe for TIMEOUT, 5xx/I-O and ContainerNotFound; none for BlobNotFound, 403 and other 4xx; indicator state unchanged in every row; ERROR line for 403 and ContainerNotFound | TASK-11, TASK-12 |
| T-TE012-07 | `BlobStorageAdapterOpenTest` | Standard and legal read; intake, quarantine and unknown → `IllegalArgumentException` with zero interactions; `BlobNotFound` → `BLOB_MISSING`; flag off NOT_READY; readiness unchanged | TASK-15, TASK-16 |
| T-TE012-08 | `StorageReadinessIndicatorTest` | Each reason; flag off `UNKNOWN`/`ready=false`/`FLAG_OFF` with no storage call; NOT_EVALUATED `UNKNOWN`; READY `UP`; NOT_READY `DOWN`; start evaluation once off the calling thread; a health read makes zero storage calls; one INFO line per state change; details hold no URL or client ID | TASK-09, TASK-10 |
| T-TE012-09 | `DocumentHealthAggregateTest` | Default status aggregator and HTTP mapper with one other component UP: flag off root UP/200; NOT_READY root DOWN/503; `liveness` and `readiness` groups do not contain `documentHub`; the only hub contributor is the bean named `documentHub` (no second indicator); no Blob client built | TASK-09, TASK-10 |
| T-TE012-10 | `DocumentAuditLogTest` | One line on `recovery.audit` with every field; `actorId` present with an authenticated principal and absent without; no content, account URL or client ID | TASK-11, TASK-12 |
| T-TE012-11 | `LocalEmulatorBootstrapTest` | Direct construction with a mocked service: `createIfNotExists` for the four names; legal policy and identities `EMULATED`; no client IDs needed; unreachable → one WARN, no exception; context runner: bean present only in emulator mode. The "next probe re-runs the bootstrap through `store()`" clause is asserted in T-TE012-17 (adapter exists) | TASK-09, TASK-10 |
| T-TE012-12 | `BlobStorageAdapterHttpStubTest` | JDK `HttpServer` on a free loopback port, emulator-mode runner, `timeout-seconds=1`: 201 → `StoredBlob`; no answer → TIMEOUT within 1 s plus a bound; 503 then no answer → retries end inside the overall timeout; 400 unexpected code → rethrown unchanged; malformed error body → rethrown unchanged | TASK-15, TASK-16 |
| T-TE012-13 | `LocalProfileStartupTest` | `local` profile plus `ConfigDataApplicationContextInitializer`: valid `devstoreaccount1` string → emulator context starts; property explicitly blank → startup fails naming `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` | TASK-09, TASK-10 |
| T-TE012-14 | Successors of the TE-001 SPEC-024 tests | Standard put → T-TE012-04 standard routing; legal put → T-TE012-04 legal routing; legal overwrite → T-TE012-05 different hash; get present → T-TE012-07 standard read; get absent → T-TE012-07 `BLOB_MISSING`. The old "container created once" assertion has no successor because SPEC-007 removes runtime creation outside the emulator bootstrap; the old "other storage error rethrown" assertion moves to T-TE012-06. Written before the old test is deleted (AGENTS.md §4.5) | TASK-15, TASK-16 |
| T-TE012-15 | `StorageTemplateConformanceTest` | Account settings; private endpoint and subnet; four containers with defaults; versioning and soft delete; conditional policy; no lock parameter; six container-scope roles; required-input list equals the template's parameters without defaults; local file shape-valid; each environment file names every input with a value or the placeholder; `deployLegalPolicy` per environment; container-name parameters valid and equal to the matching property. No undecided value | TASK-01, TASK-02 |
| T-TE012-16 | Existing `RecoveryBoundaryTest`, `ModulithTest`, T-TE001-14 | Pass under the TE-001 map; expected `dochub.api` list replaced by the SPEC-022 list in the same merge request; BND-5 and Modulith unchanged | TASK-15, TASK-16, TASK-20 |
| T-TE012-17 | `StorageReadinessProbeTest` | Outage at start ends NOT_READY `UNREACHABLE` within 1 s plus 1 s; 20 concurrent `store()` calls on stale NOT_READY and a silent storage → exactly one probe (four property calls) and each call raises TIMEOUT or NOT_READY within 1 s plus 1 s; `store()` during the start probe joins it; fresh NOT_READY refuses with zero calls; emulator probe finishes inside one deadline; READY with an old probe then a `store()` TIMEOUT → one background probe, state READY until it ends NOT_READY, next store within the window refuses with zero calls; a READY probe lets waiters proceed; `ApplicationReadyEvent` joins a running probe; suppression inside the window and exactly one probe after it; a passing background probe returns READY with `checkedAt` updated | TASK-15, TASK-16 |
| T-TE012-18 | `ReadinessIsolationTest` | READY with a missing blob → `BLOB_MISSING`, hub stays UP, readiness and `checkedAt` unchanged, root 200, zero probes; same for ACCESS_REFUSED, a write-once refusal and a 409 conflict; probe 503 → NOT_READY `UNREACHABLE`, hub DOWN, root 503; missing container → `CONTAINER_MISSING:<name>`, root 503 | TASK-15, TASK-16 |

**Profile and connection-string rule** (spec table "How tests set the profile and the emulator string"): no test relies on `.env`, `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` or `dev.ps1`, and no key is committed. Non-emulator tests pass no profile and set every `rwb.dochub.*` key they read. Emulator tests set the profile with `ctx -> ctx.getEnvironment().setActiveProfiles("local")` on a P5-only `ApplicationContextRunner` and build the string at run time from a random key, `127.0.0.1` and a free port or the mapped Azurite port; T-TE012-13 registers the profile initializer before `ConfigDataApplicationContextInitializer`. T-TE012-09 pins the keys it reads and uses the synthetic account URL `https://rwbconformance.blob.core.windows.net` (never called).

**Spring-context rule.** Every context this story starts pins each `rwb.dochub.*` key it reads and the profile it relies on; no context reads a `.env.example` variable through a placeholder it does not pin. Tests that need the `application.yaml` defaults use TE-001's `T/testsupport/ApplicationYamlEnvironment.java` (system environment and system-property sources removed) rather than a raw `ConfigDataApplicationContextInitializer`; the two spec-named exceptions (T-TE012-09 and T-TE012-13) pin their keys explicitly. TASK-23 checks the rule.

**Integration tests** (`@Tag("recovery-it")`, `recoveryIntegrationTest`, `./scripts/dev.ps1 it`): `AzuriteDocumentStorageIT` starts `GenericContainer` `mcr.microsoft.com/azure-storage/azurite:3.37.0` with `azurite-blob --blobHost 0.0.0.0 --blobPort 10000 --location /data --skipApiVersionCheck` and `AZURITE_ACCOUNTS=devstoreaccount1:<random Base64 per run>`, waits for the Azurite Blob listening line, and asserts the host is loopback. Cases: READY with no client IDs; naming; copy from intake; standard overwrite; write-once conditional upload; guard AC12 both branches; `CONTAINER_MISSING` when a container is absent; `open` refusal of quarantine. `RecoveryDatabaseIT` passes without line 61. These are required implementation evidence (ASM-TE012-23), not coverage input.

### Coverage (SPEC-023)

`./gradlew test recoveryCoverageVerification` in `backend/`, outside `check`; LINE, INSTRUCTION, BRANCH and METHOD each ≥ 0.80 over the bundle, no exclusion, `test` data only. From the report: every main class with measurable counters under `recovery/dochub/**` is at or above 0.80 on the four counters; classes with no measurable counter (for example the two interfaces) are recorded as n/a per D-RCV-43 (3); no bundle counter is lower than the TASK-00 snapshot. Reports: `backend/build/reports/jacoco/recoveryCoverageReport.xml` and the HTML folder, saved under `implement/backend/coverage/`.

## Frontend Plan

**NOT_APPLICABLE.** `[S]` §15: "No screen in this story." The spec's Frontend Specification records no screen, component, route or client type change; `UI In Scope: NO` and `API Impact Type: NO_API_CHANGE`. No file under `frontend/` is added or changed, so frontend unit tests and the Vitest gate are **NOT_APPLICABLE** (trace: `[S]` §15, SPEC-019 "SCR-44 has no owner story"; DGAP-20). `contracts/frontend-integrations.json` records `NOT_APPLICABLE` with evidence. No `plan/frontend/components.md` is created (UI In Scope NO).

## Unit test applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Trace | Evidence and rationale | Test acceptance criteria |
|---|---|---|---|---|---|---|
| Backend | YES | REQUIRED | SPEC-023: LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 bundle; per-class ≥ 0.80 under `recovery/dochub/**`; no-drop against the TASK-00 snapshot | SPEC-001..-023; AC1–AC12; BR1–BR7 | New template files, 19 new main classes, 2 deleted, 21 test files (18 new, 2 edited, 1 deleted); the adapter, readiness, guard, mapper, audit and emulator logic is new | Every T-TE012-01 to -18 case passes in `test`; `recoveryCoverageVerification` passes; per-class and no-drop checks pass from the XML; `RecoveryBoundaryTest`, `ModulithTest` and T-TE001-14 pass |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | `[S]` §15; SPEC-019 | No screen; SCR-44 has no owner story (DGAP-20) | n/a |

The final evidence follows `implementation-execution-gates.md`: one row per surface, native reports, and the measured table; the frontend row is `NOT_APPLICABLE` with `N/A` counts and the scope rationale, not invented zeros.

## Execution order (tests before code, AGENTS.md rules 3 and 10)

1. TASK-00 pre-flight on the worktree base.
2. Red/green pairs, each red run immediately before its green partner so the test source set compiles for every other task:
   - TASK-01 → TASK-02 (template conformance red, template green)
   - TASK-05 → TASK-06 (API surface red, `dochub.api` green)
   - TASK-07 → TASK-08 (properties red, properties and YAML green)
   - TASK-09 → TASK-10 (containers, config, readiness, health, emulator red → green)
   - TASK-11 → TASK-12 (mapper and audit red → green)
   - TASK-13 → TASK-14 (hash guard red → green)
   - TASK-15 → TASK-16 (adapter, isolation, HTTP stub, Azurite IT and boundary list red → green; baseline classes deleted in the green half)
3. TASK-03 and TASK-04 (script and runbook) after the template; TASK-18 (local stack) in parallel after TASK-08.
4. TASK-17 (integration suite and `RecoveryDatabaseIT`), TASK-19 (baseline naming), then TASK-20 (unit suite and coverage), TASK-21 (regression), TASK-22 (external CLI evidence), TASK-23 (scope and guardrail), TASK-24 (handover).

The red runs are recorded as command, exit code and first failing assertion or first runtime failure. No test is skipped or weakened.

## Functional Test Scenarios

| ID | Scenario | Owner | Scope and evidence |
|---|---|---|---|
| FTS-01 | AC9: with the policy missing in DEV, an upload through `POST /api/recovery/v1/cases/{caseId}/documents` returns 503 MSG-GEN-006 and writes no document row | API Tester at RWB-E1-024/RWB-E1-026 | **Not owned here.** The endpoint and the row are E1-024/E1-026; this story supplies `readiness()` and `StorageUnavailableException(NOT_READY)`. Trace: SPEC-019, DGAP-17. Evidence at those stories; recorded as a seam, not executed |
| FTS-02 | AC10: storage does not answer within 10 s; the upload returns 503 MSG-GEN-006 | API Tester at RWB-E1-024/RWB-E1-026 | **Not owned here.** The bound is proved by T-TE012-12 and T-TE012-17; the HTTP mapping is E1-024/E1-026 (SPEC-019) |
| FTS-03 | TC-TE-012-01 to -12: the SIT system tests against the real account (write-once, delete refused, new version, versions and soft delete, role listing, key and SAS refused, no-role identity, public network, missing policy, timeout, quarantine, same hash) | Human: QA lead with the platform team and RW-SECADM (SIT) | **PENDING_ENVIRONMENT**: the template is not applied in SIT yet. Recorded as a human-verification gap; no result is claimed. TC-01's storage clause uses a raw client with the ACE identity (DGAP-15) |
| FTS-04 | TC-TE-012-13: a role without Documents C uploads and gets 403 MSG-P4-002 | API Tester at RWB-E1-026 | **Not owned here** (E1-026 endpoint, spec §12) |
| FTS-05 | Existing `PlatformE2ETest` still passes after the story (`NO_API_CHANGE`) | API Tester; the Builder runs the suite as regression evidence in TASK-21 | `./gradlew e2eTest` in `backend/` against `./scripts/dev.ps1 up` and `./scripts/dev.ps1 backend`; report saved |
| FTS-06 | UI journeys | Functional Automation Test | **NOT_APPLICABLE**: UI In Scope NO; no screen, route or component |
| HV-01 | Template applied in DEV and SIT; RW-SECADM reviews the SIT role listing (story §13 "Done when") | Human: RW-PLATADM applies, RW-SECADM reviews | Open item (PG-04); `PENDING_ENVIRONMENT`; the check report and the listing are the evidence |
| HV-02 | BE-01 to BE-13 on disposable DEV resources standing in for PROD | **Builder-verified external CLI evidence** | Printed reports under `implement/infra/`; not Functional or API automation; not claimed as executed by this stage |
| HV-03 | The ACE pipeline gains an infrastructure stage so the check runs as its first step | Human: platform team with the release owner | Not testable here (DGAP-24); open item |

Uncovered non-API, non-UI acceptance checks (AC5, AC6, AC7, AC8, AC9's policy clause, AC10's real network clause and all SIT TCs) remain in FTS-03/HV-01 as human-verification gaps, not fabricated QA results.

## Requirement Logic To Task Coverage

`REQ_REF` values are the spec's "Requirement-to-SPEC Logic Coverage" rows; `SPEC-nnn` = `SPEC-RWB-TE-012-nnn`. Every row is `COVERED`; no row is `BLOCKED`.

| # | REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|---|
| 1 | `[S]` §4 step 1 | 001, 002 | TASK-02 | DIRECT_IMPLEMENTATION | T-TE012-15 account and container assertions | COVERED |
| 2 | `[S]` §4 step 2, BR6 | 003 | TASK-02 | DIRECT_IMPLEMENTATION | T-TE012-15 versioning and soft delete | COVERED |
| 3 | `[S]` §4 step 2, BR1 | 004 | TASK-02, TASK-03, TASK-04 | DIRECT_IMPLEMENTATION | T-TE012-15 policy and condition; BE-04, BE-05; runbook PROD lock | COVERED |
| 4 | `[S]` §4 step 2, BR4 | 005 | TASK-02 | DIRECT_IMPLEMENTATION | T-TE012-15 six container-scope roles | COVERED |
| 5 | `[S]` §4 step 3, BR5 | 009, 020 | TASK-10 | DIRECT_IMPLEMENTATION | T-TE012-08, T-TE012-09 | COVERED |
| 6 | `[S]` §4 step 4 | 007, 010, 011 | TASK-06, TASK-10, TASK-14, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-04, T-TE012-05, Azurite IT | COVERED |
| 7 | `[S]` §4 step 5, X1 | 012, 013, 014 | TASK-12, TASK-14 | DIRECT_IMPLEMENTATION | T-TE012-05, T-TE012-06, T-TE012-10; TC-TE-012-01 (SIT) | COVERED |
| 8 | `[S]` §4 step 6, BR2 | 010, 011, 015 | TASK-06, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-04 naming; Azurite IT v2 readable | COVERED |
| 9 | `[S]` §4 step 7 | 009, 020 | TASK-10 | DIRECT_IMPLEMENTATION | T-TE012-08, T-TE012-09; SCR-44 is a seam (DGAP-20) | COVERED |
| 10 | `[S]` BR3, X3 | 001, 007 | TASK-02, TASK-10 | DIRECT_IMPLEMENTATION | T-TE012-15 shared key off; T-TE012-02 credential chain; TC-TE-012-06 (SIT) | COVERED |
| 11 | `[S]` BR7, X9, AC12 | 012 | TASK-14 | DIRECT_IMPLEMENTATION | T-TE012-05 both branches; TC-TE-012-12 (SIT) | COVERED |
| 12 | AC1 | 004, 012, 013, 014, 018, 019 | TASK-02, TASK-04, TASK-12, TASK-14, TASK-16, TASK-20 | DIRECT_IMPLEMENTATION | T-TE012-05, T-TE012-06, T-TE012-10; TC-TE-012-01 (SIT, raw client); 409 is E1-024 | COVERED |
| 13 | AC2 | 004, 018 | TASK-02, TASK-04, TASK-12, TASK-17 | DIRECT_IMPLEMENTATION | T-TE012-06 DELETE row; TC-TE-012-02 (SIT) | COVERED |
| 14 | AC3 | 010, 011, 015 | TASK-06, TASK-16, TASK-17 | DIRECT_IMPLEMENTATION | T-TE012-04; Azurite IT; TC-TE-012-03 (SIT) | COVERED |
| 15 | AC4 | 003, 011, 018 | TASK-02, TASK-16, TASK-17 | DIRECT_IMPLEMENTATION | T-TE012-15 versioning and soft delete; T-TE012-04 overwrite; TC-TE-012-04 (SIT) | COVERED |
| 16 | AC5 | 005, 018 | TASK-02, TASK-22 | DIRECT_IMPLEMENTATION | T-TE012-15 roles; TC-TE-012-05 and RW-SECADM listing (PENDING_ENVIRONMENT) | COVERED |
| 17 | AC6 | 001, 018 | TASK-02, TASK-22 | DIRECT_IMPLEMENTATION | T-TE012-15 `allowSharedKeyAccess: false`; TC-TE-012-06 (SIT) | COVERED |
| 18 | AC7 | 005, 018 | TASK-02, TASK-12 | DIRECT_IMPLEMENTATION | T-TE012-06 403 mapping; TC-TE-012-07 (SIT) | COVERED |
| 19 | AC8 | 001, 018 | TASK-02, TASK-22 | DIRECT_IMPLEMENTATION | T-TE012-15 private endpoint and public network off; TC-TE-012-08 (SIT) | COVERED |
| 20 | AC9 | 009, 011, 019, 020 | TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-08 `LEGAL_POLICY_MISSING`; T-TE012-18 DOWN/503; 503 and no row are E1-024/E1-026 (DGAP-17); TC-TE-012-09 (SIT) | COVERED |
| 21 | AC10 | 007, 013, 019 | TASK-10, TASK-12, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-12 timeout within 1 s; T-TE012-17 bound; HTTP 503 is E1-024/E1-026 | COVERED |
| 22 | AC11 | 005, 015 | TASK-02, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-07 quarantine refusal; T-TE012-15 role scope; TC-TE-012-11 (SIT) | COVERED |
| 23 | AC12 | 012 | TASK-14, TASK-15 | DIRECT_IMPLEMENTATION | T-TE012-05 both branches; Azurite IT | COVERED |
| 24 | X2, X4–X8, X10 | 013, 015, 020 | TASK-10, TASK-12, TASK-16, TASK-23 | DIRECT_IMPLEMENTATION | T-TE012-06, T-TE012-07, T-TE012-08, T-TE012-18; X5 and X10 are SIT/E1-026 (FTS-03, FTS-04) | COVERED |
| 25 | `[S]` §13 flag | 006, 009, 011, 020 | TASK-08, TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-01, T-TE012-02, T-TE012-04, T-TE012-07, T-TE012-08 | COVERED |
| 26 | `[S]` §17 guardrails | 006, 007, 010, 014, 017 | TASK-08, TASK-10, TASK-12, TASK-23 | DIRECT_IMPLEMENTATION | Property-only values; T-TE012-10 no content or URL; TASK-23 guardrail check | COVERED |
| 27 | `[DL]` D-RCV-31 | 010, 011 | TASK-06, TASK-16 | DIRECT_IMPLEMENTATION | `DocumentStorage` is the only write path; T-TE012-04 re-store; TASK-23 grep | COVERED |
| 28 | FR-RWB-007 | 001 to 017, 020 | TASK-01, TASK-02, TASK-06, TASK-10, TASK-12, TASK-14, TASK-16 | DIRECT_IMPLEMENTATION | The storage and write-path tasks and their tests | COVERED |
| 29 | REQ-DCM-003 | 004, 011, 012, 013 | TASK-02, TASK-12, TASK-14, TASK-16 | DIRECT_IMPLEMENTATION | Policy, guard and mapper; TC-TE-012-01, -02 (SIT) | COVERED |
| 30 | REQ-DCM-002 | 010, 011, 015 | TASK-06, TASK-16 | DIRECT_IMPLEMENTATION | Single write path; `open()` allow-list; TASK-23 | COVERED |
| 31 | NFR-029 | 004, 009, 012 | TASK-02, TASK-10, TASK-14 | DIRECT_IMPLEMENTATION | T-TE012-15 policy; T-TE012-05; T-TE012-08 | COVERED |
| 32 | NFR-053 | 001 | TASK-02 | DIRECT_IMPLEMENTATION | T-TE012-15 TLS 1.2 and platform encryption | COVERED |
| 33 | CTL-12 | 004, 010, 011, 012, 013, 014, 018 | TASK-02, TASK-04, TASK-06, TASK-12, TASK-14, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-05, T-TE012-06, T-TE012-10; BE-04, BE-05; TC-TE-012-01, -02 | COVERED |
| 34 | CTL-09 | 005, 015, Guardrails | TASK-02, TASK-16, TASK-23 | DIRECT_IMPLEMENTATION | Six container-scope roles; `open()` is not an authorization point; TASK-23 | COVERED |
| 35 | Health endpoint | 020 | TASK-10 | INHERITED_EXISTING_BEHAVIOR for the actuator block; DIRECT_IMPLEMENTATION for the component | T-TE012-08, T-TE012-09; `application.yaml` management block unchanged | COVERED |
| 36 | `[TE001]` SPEC-009, -022, -024, -025 | 016, 022 | TASK-00, TASK-05, TASK-06, TASK-15, TASK-16, TASK-19 | DIRECT_IMPLEMENTATION | TASK-00 pre-flight; T-TE001-14 list; `RecoveryBoundaryTest`, `ModulithTest` | COVERED |
| 37 | `[DL]` D-RCV-31 re-store | 010, 011 | TASK-06, TASK-15, TASK-16 | DIRECT_IMPLEMENTATION | T-TE012-04 re-store case; Azurite IT; source kept | COVERED |

## SPEC to task map

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-01, TASK-02 | T-TE012-15 |
| 002 | TASK-01, TASK-02 | T-TE012-15 |
| 003 | TASK-01, TASK-02 | T-TE012-15 |
| 004 | TASK-02, TASK-03, TASK-04 | T-TE012-15; BE-04, BE-05; runbook |
| 005 | TASK-02 | T-TE012-15 |
| 006 | TASK-07, TASK-08 | T-TE012-01 |
| 007 | TASK-09, TASK-10 | T-TE012-02 |
| 008 | TASK-09, TASK-10 | T-TE012-02 |
| 009 | TASK-09, TASK-10 | T-TE012-08, T-TE012-17 |
| 010 | TASK-05, TASK-06 | T-TE012-03, T-TE012-04 |
| 011 | TASK-15, TASK-16 | T-TE012-04, T-TE012-17 |
| 012 | TASK-13, TASK-14 | T-TE012-05 |
| 013 | TASK-11, TASK-12 | T-TE012-06 |
| 014 | TASK-11, TASK-12 | T-TE012-10 |
| 015 | TASK-15, TASK-16 | T-TE012-07, T-TE012-18 |
| 016 | TASK-06, TASK-16, TASK-17, TASK-19 | T-TE012-14, T-TE001-14 |
| 017 | TASK-09, TASK-10 | T-TE012-11, T-TE012-13 |
| 018 | TASK-01, TASK-05, TASK-07, TASK-09, TASK-11, TASK-13, TASK-15, TASK-17 | All T-TE012 tests; Azurite IT |
| 019 | TASK-16, TASK-23 | Seam review; TASK-23 |
| 020 | TASK-09, TASK-10 | T-TE012-08, T-TE012-09 |
| 021 | TASK-18 | Builder `.env` evidence; TASK-21 |
| 022 | TASK-05, TASK-06, TASK-15 | T-TE001-14 |
| 023 | TASK-20, TASK-23 | Coverage XML and team report |

No orphan `SPEC-*`; every active SPEC 001–023 has at least one task.

## Screen-to-task mapping

`NOT_APPLICABLE`: UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`, no effective-screen node or `SCR-*` screen in the spec. No screen consolidation or visual-fidelity task is created; the pre-submit check records this.

## Rule and parameter sources

| Value | Where it is read | Source |
|---|---|---|
| Four container names | Template parameters with defaults and `rwb.dochub.container.*` | `[S]` §4 step 1, §13; FSD P5; D-RCV-31 |
| `legalRetentionDays` 3650 | Template parameter | ASM-TE012-01; `[S]` BR1, DL26 open |
| `softDeleteDays` 30 | Template parameter | ASM-TE012-02; `[S]` BR6, DL27 open |
| `timeout-seconds` 10 | Property | `[S]` §13, AC10 |
| `readiness-recheck-seconds` 30 | Property | ASM-TE012-30 (assumed; no document gives a value) |
| Service and OCR client IDs | Properties from the environment | ASM-TE012-05; `[URP]` |
| Storage Blob Data Contributor | One ARM `variables` entry, built-in role | `[S]` §4 step 2, AC5; Azure built-in role (PA-08) |
| Flag `rwb.dochub.storage-containers` | Property | `[S]` §13; `[ENV]` §6 |
| Blob name `{caseId}/{documentId}/v{docVersion}` | Code building the name | `[S]` §4 step 4, §11; D-RCV-31 |
| `storage_ref` read/write format | `BlobRef` | `[S]` §11; `[SCH]` `varchar(400)` |
| `DOCUMENT_CHANGE_REFUSED` and its fields | `DocumentAuditLog` | FSD P5; `[AUD]`; SPEC-014 |
| Blob metadata key `sha256`, content-type header | Adapter and guard | SPEC-011, SPEC-012 |
| Readiness reasons and health detail values | Indicator and probe | SPEC-009, SPEC-020 |
| Six pre-deploy inputs, report, rows 1–7 | Check script | SPEC-001; ASM-TE012-32 |
| `__SET_BEFORE_APPLY__` | Parameter files and check | ASM-TE012-32, -33 |
| Message IDs MSG-P5-002, MSG-GEN-006, MSG-P4-002 | Callers only; this story raises exceptions | `[MSG]`; SPEC-019 |
| Deviations from the context 30 s external timeout | 10 s property | DGAP-08 (story wins) |

No business threshold, container, timeout, route or role permission is a Java literal. The only fixed strings are contract names the spec defines (the audit role labels, event type, reason enum values, metadata key, API property names) and the Azure built-in role GUID in one template variable (PA-08).

## Security, privacy and compliance

- No endpoint, no method-security change, no new permission. `open()` is not an authorization point; its callers own the Documents R right and scope check and the PII access log (SPEC-015, E1-024 step 8). The story adds no HTTP mapping.
- Managed identity only. No account key or SAS outside emulator mode; the published Azurite development key remains only in `.env`/`.env.example` (SPEC-017). The emulator string is read from the environment and is never logged.
- No personal data. Blob names carry UUIDs; audit fields are IDs, reason, operation and role label; no content, URL, client ID or hash of another blob is logged. Test data is random UUIDs and generated bytes.
- Audit: `DOCUMENT_CHANGE_REFUSED` on `recovery.audit`, the stand-in for the ACE audit log (ASM-TE012-06). Direct container attempts are the platform-log gap DGAP-11, not claimed.
- Write-once control: policy on the legal container, locked in PROD by the runbook, conditional in the template, incremental applies, hash guard in the service (CTL-12, NFR-029, REQ-DCM-003).
- Secrets and configuration: no secret in code, config, tests or pipeline; client IDs are object IDs, not secrets; the pre-deploy check uses the logged-in Azure CLI credential and adds no secret.
- Feature flag: off returns the previous path; no client is built, the beans still exist and refuse (AGENTS.md §3.13).
- KYC/AML/suitability/consent and customer data: not in scope for a storage enabler.

## Assumptions

Plan assumptions are in `assumptions.md` (PA-01 to PA-24); spec assumptions ASM-TE012-01 to -33 are carried unchanged and not repeated. None changes a requirement and none needs a source decision. The plan-gate items the spec carries (the README "Decisions taken" item (b), the `RUNBOOK.md` content of SPEC-004, the template format and folder) stay visible in `shared-updates.md`; this stage claims no human approval.

## Release and rollback

- Flag off by default in `application.yaml`, so the merged code returns the previous path (no document storage bean work) until the platform enables it per environment.
- The template apply is additive and incremental; the PROD lock is the only irreversible step and is approved with the PROD deploy. No migration and no data move, so a rollback is a revert merge request plus a flag off; the template can be re-applied forward.
- Merge gate: `./scripts/dev.ps1 test` exits 0 on the branch; `./scripts/dev.ps1 it` exits 0 and its log is attached; `recoveryCoverageVerification` and the per-class/no-drop evidence are shown separately (it is outside `check`).
- SIT and PROD evidence is handed over, not claimed: template apply, role listing, TCs 01–12 and BE-01 to BE-13 remain the platform/QA steps.

## Status

```text
PLANNER_STATUS_SUMMARY: Plan ready: 25 tasks (TASK-00 to TASK-24) for the ARM template, pre-deploy check and runbook, the published DocumentStorage path, adapter, readiness and health, hash guard, audit, local emulator, integration tests, coverage and external evidence.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: spec v10 passed round 10 with 0 findings; every SPEC 001-023, AC1-AC12, BR1-BR7 and all 37 requirement-logic rows map to tasks and named tests] [UNBLOCK_ACTION: n/a]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; no screen in the story]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: 37 of 37 spec logic rows map to tasks; AC1-AC12 and BR1-BR7 have named unit or integration tests; SIT TCs, BE-01 to BE-13 and the DEV/SIT applies are recorded as pending human or external evidence, not as executed results.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 37] [TASK_COVERED_RULES: 37] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```

Source conflicts settled by precedence remain in `../specify/document-gaps.md` and in `document-gaps.md`; `CONTRADICTIONS` counts only conflicts left unresolved in this plan, which is none.
