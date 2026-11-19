# Technical Specification — RWB-TE-012 Document storage containers

Status: SUCCESS

| Field | Value |
|---|---|
| Story | RWB-TE-012 — Document storage containers (Enabler, Must) |
| Epic / module | E1 / P5 Document hub. Code module `th.co.scb.ace.demo.recovery.dochub` as RWB-TE-001 v4 maps it: published `dochub.api`, client package `dochub.storage` (`[TE001]` SPEC-001, SPEC-009, SPEC-022) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Revision | v7, spec gate round 6 remediation (findings SG-37, SG-38, `gate-response.md` Round 6). Earlier versions: `spec.run6.md` (v6), `spec.run5.md` (v5), `spec.run4.md` (v4), `spec.run3.md` (v3), `spec.run2.md` (v2), `spec.run1.md` (v1) |
| Source requirement | Story file RWB-TE-012 v1, 28 Oct 2026, in Epic 1 story files v7 (`[S]` below); increment card `docs/increments/INC-007-epic-1-RWB-TE-012.md` |
| Upstream IDs | REQ-DCM-003, REQ-DCM-002 (BRD Program v4 §5.5); `BR-RWB-007` / `FR-RWB-007` (Traceability Matrix row 007); CTL-12, CTL-09; NFR-029, NFR-053; DL26, DL27; D-RCV-31 |
| Build order | 7 of 72 (Build Sequence v6). **Precondition: RWB-TE-001 merged in this repository** (order 2; its spec v4 passed the spec gate, round 5; build not yet merged). Consumed by RWB-E1-017 (17, archive container: not delivered here, DGAP-22), RWB-E1-024 (42), RWB-E1-049 (49), RWB-E1-041 (54), RWB-E1-026 (58), RWB-E1-057 (61), RWB-E1-032 (63), RWB-E1-054 (70) |
| Prepared | 2026-11-18, Technical Specifier (agent run). No question asked (L-RCV-03) |
| Spec gate | Round 7 in `review/spec-gate-review-7.md`; result in "Status reporting" |

## Sources cited

Document-set paths are under `requirement/legacy/` (read only). Short names are used in the text.

| Short name | Document, version | Path |
|---|---|---|
| `[S]` | RWB-TE-012 story file v1 (Epic 1 story files v7) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md` |
| `[BN]` | Build notes, technical enablers v2, section RWB-TE-012 | `04-user-stories/recovery-workbench-build-notes-technical-enablers-v2.md` |
| `[E1-024]` | RWB-E1-024 Document store and index v1 (story files v7) | same folder as `[S]`, `rwb-e1-024-document-store-and-index-v1.md` |
| `[E1-026]`, `[E1-032]`, `[E1-041]`, `[E1-049]`, `[E1-057]` | RWB-E1-026, -032, -041, -049, -057 v1 (story files v7) | same folder |
| `[E1-056]` | RWB-E1-056 v1 (story files v7) | same folder |
| `[E1-017]`, `[E1-054]` | RWB-E1-017 Retention and archive rule for the data store v1; RWB-E1-054 Review queue for low-confidence documents v1 (story files v7) | same folder |
| `[ERR]` | Error Handling and Resilience Standard v3 (§2 failure table, §3 retry) | `05-technical-architecture/` |
| `[AZ-IMM]` | Microsoft Learn, "Immutable storage for blob data overview", section "Locked versus unlocked policies" (page dated 18 August 2026) | learn.microsoft.com, Azure Storage documentation (external, not in the document set) |
| `[AZ-REST]` | Microsoft Learn, Storage Resource Provider REST API "Blob Containers - Create Or Update Immutability Policy" (api-version 2026-09-01) | learn.microsoft.com (external) |
| `[AZ-COND]` | Microsoft Learn, "Conditional deployment with templates", section "Complete mode" (page dated 26 June 2026) | learn.microsoft.com, Azure Resource Manager documentation (external) |
| `[AZ-MODES]` | Microsoft Learn, "Deployment modes", sections "Incremental mode" and "Complete mode" (page dated 26 June 2026) | learn.microsoft.com, Azure Resource Manager documentation (external) |
| `[AZ-GET]` | Microsoft Learn, Storage Resource Provider REST API "Blob Containers - Get" (api-version 2026-09-01; page dated 23 October 2026): `properties.hasImmutabilityPolicy`, `properties.immutabilityPolicy.properties.state`, `accountName` pattern | learn.microsoft.com (external) |
| `[AZ-CLI-CRM]` | Microsoft Learn, Azure CLI reference "az storage container-rm" (`exists`, `show`; page dated 9 November 2026) | learn.microsoft.com (external) |
| `[AZ-CLI-IMM]` | Microsoft Learn, Azure CLI reference "az storage container immutability-policy" (`show`, `lock`, `extend`; page dated 9 November 2026) | learn.microsoft.com (external) |
| `[TEV7]` | Technical enabler stories v7 | `04-user-stories/recovery-workbench-technical-enabler-stories-v7.md` |
| `[SCR]` | Screen Inventory and Navigation v2 | `07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md` |
| `[ADR]` | Architecture Decision Records v3, ADR-007 | `05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| `[DL]` | Decision Log v10 (DL26, DL27 open; D-RCV-31 taken) | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| `[NFR]` | Non-Functional Specification v3 | `03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| `[PDPA]` | Personal Data Protection Design v2 | `10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md` |
| `[RET]` | Records Retention and Archiving v2 | `10-policy-controls-and-compliance/recovery-workbench-records-retention-and-archiving-v2-docx.md` |
| `[FSD-P5]` | FSD P5 Document hub v3 | `03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p5-document-hub-v3.md` |
| `[ENV]` | Environment and Deployment Design v4 | `05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| `[SEC]` | Security and Access Design v4 | `05-technical-architecture/recovery-workbench-security-and-access-design-v4-docx.md` |
| `[AUD]` | Audit and Logging Design v2 | `05-technical-architecture/recovery-workbench-audit-and-logging-design-v2-docx.md` |
| `[MSG]` | Error and Message Standard v4 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| `[URP]` | Users, Roles and Permissions v4 (SY-DATALOAD retired under D-RCV-35 U1) | `02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` |
| `[CTL]` | Controls Catalog v3 | `10-policy-controls-and-compliance/recovery-workbench-controls-catalog-v3-xlsx.md` |
| `[SCH]` | Physical Schema v6 | `06-data/recovery-workbench-physical-schema-v6.sql` |
| `[API]` | API Specification v4 | `05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| `[TC]` | Test Cases v7 | `09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |

Workspace sources (this repository, not the document set):

| Short name | Source |
|---|---|
| `[TE001]` | `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` v4 (spec gate passed, round 5) and its `shared-updates.md` SU-08 |
| `[DEC]` | `aisdlc/docs/decisions/INC-001-decisions.md` and `decision-register.md`: D-RCV-06, D-RCV-28 (3), D-RCV-40, D-RCV-41, D-RCV-44 |
| `[TS]` | `aisdlc/.github/contexts/testing-standards.md` §6; `aisdlc/.github/contexts/backend-context.md` §2 (BND-5), §8 |
| `[BSEQ]` | `aisdlc/docs/increments/build-sequence.md` (Build Sequence v6) |
| `[AGENTS]` | `AGENTS.md` §3.13 (flag off returns the previous code path), §4.4, §4.5 |
| `[CODE]` | Code read on 18 Nov 2026: `backend/`, `docker-compose.yml`, `.env.example`, `scripts/dev.ps1`, `README.md`; Phase 0 audit `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-04, A-09) |

## Baseline: what exists after RWB-TE-001, what this story evolves, what it adds

The baseline document code is inherited footprint (audit A-04). RWB-TE-001 relocates it without behaviour change (`[TE001]` SPEC-022 (a), (b) and its Relocation table). This story starts from the relocated code and **evolves it in place**; it adds no second adapter, store or configuration.

| Item after RWB-TE-001 merges | Evidence |
|---|---|
| `dochub.api.DocumentStore` (public; `put`, `get`, nested `StoredDocument`, `DocumentImmutableException`) | `[TE001]` Relocation table; SPEC-025 lists it as the only `dochub.api` public type |
| `dochub.storage.BlobDocumentStore` (package-private; nested `Config` building one `BlobServiceClient` from `rwb.blob.connection-string` or `rwb.blob.endpoint` + `DefaultAzureCredential`; nested `BlobProperties` `@ConfigurationProperties("rwb.blob")`; two containers; blob name = document UUID; `If-None-Match: *` on legal writes; `createIfNotExists()` on first write; `get` returns empty on `BlobNotFound`) | `[TE001]` Relocation table; `[CODE]` `documents/internal/BlobDocumentStore.java` |
| Unit tests for `dochub.storage.BlobDocumentStore` and its configuration, mocked Blob clients: standard put, legal put, legal overwrite refused, get present, get absent | `[TE001]` SPEC-024 |
| BND-5 map-driven: `com.azure.storage` allowed only in, or under, `dochub.storage` | `[TE001]` SPEC-009, SPEC-026 |
| `T-TE001-14`: the public types of `dochub.api` equal the SPEC-025 list | `[TE001]` T-TE001-14 |
| Coverage: `recoveryCoverageVerification` with LINE, INSTRUCTION, BRANCH, METHOD at 0.80 over all main `recovery/**` classes, no exclusion, `test` execution data only, outside `check` | `[TE001]` SPEC-020 |
| `application.yaml` `rwb.blob` block (keys unchanged by RWB-TE-001); `RecoveryDatabaseIT:61` sets `rwb.blob.connection-string` | `[TE001]` "Not changed: `application*.yaml` property keys"; `[CODE]` |
| Local stack: `.env.example:23` `RWB_BLOB_CONNECTION_STRING`, `:24` `RWB_BLOB_CONNECTION_STRING_DOCKER`; `docker-compose.yml:135` passes the `_DOCKER` value to the backend; `scripts/dev.ps1` `Initialize-EnvFile` copies `.env.example` only when `.env` is absent; `README.md:25` "documents/ Azure Blob DocumentStore" | `[CODE]` |
| Callers of `DocumentStore` | None (grep, 18 Nov 2026) |

**Evolution map (SPEC-016).** Each baseline element has exactly one successor:

| Baseline element (after RWB-TE-001) | Successor in this story | Reason |
|---|---|---|
| `dochub.api.DocumentStore` | Renamed and reshaped to `dochub.api.DocumentStorage` (SPEC-010) | `[DL]` D-RCV-31 names "DocumentStorage" as the TE-012 interface; `[E1-024]` §12 owns the name `DocumentStore` for its own interface |
| `DocumentStore.put(UUID, boolean, String, byte[])` | `DocumentStorage.store(BlobWriteRequest)` (copy from the intake container) | `[E1-024]` flow steps 1 and 7: the file is in the intake container and `DocumentStorage.store` writes it to `rwb-docs` or `rwb-docs-legal` |
| `DocumentStore.get(UUID, boolean)` → `Optional<byte[]>` | `DocumentStorage.open(BlobRef)` → `byte[]`; a missing blob is `StorageUnavailableException(BLOB_MISSING)` | `[E1-024]` stores `storage_ref`; a STORED row whose blob is missing is a fault, not an empty result (ASM-TE012-15) |
| `DocumentStore.StoredDocument` | `dochub.api.StoredBlob` and `dochub.api.BlobRef` | `[E1-024]` §12 returns its own `StoredDocument`; the name is left to it |
| `DocumentStore.DocumentImmutableException` | `dochub.api.WriteOnceViolationException` | `[S]` §12; `[E1-024]` §12 `replaceContent` "throws WriteOnceViolationException" |
| `dochub.storage.BlobDocumentStore` | Renamed in place to `dochub.storage.BlobStorageAdapter` and extended | `[S]` §4 step 4 and `[BN]` step 4 name "BlobStorageAdapter" |
| `BlobDocumentStore.Config` | `dochub.storage.DocumentContainersConfig` | `[S]` §13 |
| `BlobDocumentStore.BlobProperties` (`rwb.blob`) | `dochub.storage.DocumentStorageProperties` (`rwb.dochub`), package-private | `[S]` §13 "Configuration and reference data"; `[TE001]` SPEC-023 (each module binds its own keys) |
| Containers `rwb-documents`, `rwb-documents-legal` | `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` | `[S]` §4 step 1; `[DL]` D-RCV-31; `[FSD-P5]`. The baseline names appear in no document |
| Blob name = document UUID | `{caseId}/{documentId}/v{docVersion}` | `[S]` §4 step 4, §11; `[DL]` D-RCV-31 |
| `createIfNotExists()` at first write | Never outside local emulator mode | `[S]` BR5: a runtime create would make `rwb-docs-legal` without its policy |
| `DefaultAzureCredential` full chain | Workload and managed identity credentials only | `[S]` §13 "restricted to managed identity", BR3 |
| No timeout | 10 s per call, retries included | `[S]` §13, AC10 |
| `If-None-Match: *` on legal writes | Kept, behind ContentHashGuard | README "Local versus target" Blob row; `[S]` AC12 |
| RWB-TE-001 SPEC-024 tests | Carried forward and extended (SPEC-022, T-TE012-14) | Each old assertion has a successor; no test is deleted without one (`[AGENTS]` §4.5) |
| `build.gradle.kts:60` comment naming "DocumentStorageConfig" | Names `DocumentContainersConfig` | Accuracy |

## Assumptions

Full list with basis and effect in `assumptions.md` (`ASM-TE012-01` to `-33`). The ones that shape behaviour:

| ID | Assumption (short) |
|---|---|
| ASM-TE012-01 | Write-once period 3,650 days from blob creation, a template parameter, until DL26 (`[S]` §3, BR1) |
| ASM-TE012-02 | Soft delete 30 days, a template parameter, until DL27 (`[S]` BR6) |
| ASM-TE012-03 | Template written as an Azure Resource Manager (ARM) JSON template with four environment parameter files, a required-input list and a synthetic local parameter file used only by T-TE012-15, in `infra/azure/document-storage/` |
| ASM-TE012-05 | The service process obtains the SY-OCR managed identity by a configured client ID |
| ASM-TE012-06 | `DOCUMENT_CHANGE_REFUSED` is written to logger `recovery.audit` until an ACE audit interface is supplied |
| ASM-TE012-07 | `caseId` and `documentId` in blob names are UUIDs |
| ASM-TE012-04 | The PROD lock of the legal policy is a runbook step outside the template, run by RW-PLATADM after the policy apply, approved with the PROD deploy (SPEC-004) |
| ASM-TE012-08 | Only the readiness probe writes the readiness state. It runs single-flight, bounded by `timeout-seconds`, on application ready, from `store()` when the state is NOT_EVALUATED or a NOT_READY result is older than `readiness-recheck-seconds`, and in the background when an operation meets a transport failure or `ContainerNotFound`; a health read never calls storage (SPEC-009) |
| ASM-TE012-09 | `documentHub` is not in the liveness or readiness probe groups |
| ASM-TE012-11 | Local emulator mode needs the `local` profile active, `rwb.dochub.storage.emulator=true` and three connection-string checks |
| ASM-TE012-28 | Unreachable Azurite at startup: the bootstrap logs, leaves the hub NOT_READY and runs again in the next probe; startup neither fails nor waits |
| ASM-TE012-29 | Flag off: `DocumentContainers` bean present, accessors throw NOT_READY, `readiness()` returns `FLAG_OFF` |
| ASM-TE012-30 | `readiness-recheck-seconds` default 30: a NOT_READY result is reused for 30 s before `store()` probes again (no source gives a value) |
| ASM-TE012-31 | Emulator mode skips the identity checks (reported `EMULATED`); quarantine uses the shared-key client |
| ASM-TE012-32 | Template parameter files: the four environment files may hold the placeholder `__SET_BEFORE_APPLY__` for an undecided input; a pre-deploy check refuses to apply while one remains (SPEC-001) |
| ASM-TE012-33 | After the PROD lock, later PROD applies skip the policy resource (`deployLegalPolicy=false`); the period changes only by the runbook "extend" step (SPEC-004) |
| ASM-TE012-20 | Flag off: `documentHub` reports `UNKNOWN` with `ready=false`, so the root health status is what it was before this story |
| ASM-TE012-21 | `store()` copies from the intake container or, for the D-RCV-31 re-store, from the standard container (download, hash, upload); it never deletes the source |
| ASM-TE012-22 | `dev.ps1` adds keys that are in `.env.example` and missing from an existing `.env` |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | NEW_STORY (no earlier spec or trace chain; the baseline document code is inherited footprint, A-04, relocated by RWB-TE-001) |
| UI In Scope | NO. `[S]` §15: "No screen in this story" |
| Logic In Scope | YES |
| API In Scope | NO. `[S]` §12: "No endpoint of its own" |
| API Impact Type | NO_API_CHANGE |
| Impacted Existing Nodes | `dochub.api.DocumentStore` and `dochub.storage.BlobDocumentStore` (with nested `Config`, `BlobProperties`) — evolved in place per the Evolution map; the RWB-TE-001 SPEC-024 unit tests for them; the `dochub.api` expected list in the T-TE001-14 test; `backend/src/main/resources/application.yaml` (`rwb.blob` block removed, `rwb.dochub` added); `application-local.yaml`; `backend/src/test/.../RecoveryDatabaseIT.java:61`; `backend/build.gradle.kts:60` (comment); `.env.example:23` and `:24`; `docker-compose.yml:135`; `scripts/dev.ps1` `Initialize-EnvFile`; `README.md:25` (Builder, `shared-updates.md` §5) |
| New Nodes Required | YES. In `infra/azure/document-storage/`: ARM JSON template `azuredeploy.json`, four environment parameter files, the required-input list `azuredeploy.parameters.schema.json`, the synthetic `azuredeploy.local.parameters.json` (T-TE012-15 only), the pre-deploy check `Test-DeployParameters.ps1`, and `RUNBOOK.md` with the Apply, PROD lock and Extend steps; `dochub.api`: `BlobRef`, `BlobWriteRequest`, `StoredBlob`, `StorageReadiness`, `StorageUnavailableException`; `dochub.storage`: `DocumentContainers`, `StorageReadinessIndicator`, `StorageErrorMapper`, `ContentHashGuard`, `DocumentAuditLog`, `LocalEmulatorBootstrap`; the unit and integration tests of SPEC-018 |
| Inherited Existing Behavior | Actuator health with `show-details: when-authorized`, role RW-PLATADM, probe groups enabled (`application.yaml`); `SecurityConfig` permits `/actuator/health/**` anonymously; Spring Modulith and the RWB-TE-001 module map; coverage verification per `[TE001]` SPEC-020 |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| `[S]` §4 step 1 | Account: shared key off, public network off, TLS 1.2, private endpoint; four containers | SPEC-001, -002 | DIRECT | Template; conformance test and SIT | COVERED |
| `[S]` §4 step 2, BR6 | Versioning and 30-day soft delete for rwb-docs | SPEC-003 | DIRECT | Account scope in Azure (DGAP-03) | COVERED |
| `[S]` §4 step 2, BR1 | Time-based policy on rwb-docs-legal; locked in PROD only | SPEC-004 | DIRECT | Template parameters | COVERED |
| `[S]` §4 step 2, BR4 | Role assignments per container | SPEC-005 | DIRECT | Container scope | COVERED |
| `[S]` §4 step 3, BR5 | On start, ready only if four containers exist and the legal policy is present | SPEC-009, -020 | DIRECT | `StorageReadinessIndicator` | COVERED |
| `[S]` §4 step 4 | Write by managed identity; legal type to rwb-docs-legal, else rwb-docs; name `{caseId}/{documentId}/v{docVersion}` | SPEC-007, -010, -011 | DIRECT | Type-to-`writeOnce` choice stays in E1-024 (SPEC-019) | COVERED |
| `[S]` §4 step 5, X1 | Refused overwrite → WriteOnceViolationException; audit | SPEC-012, -013, -014 | DIRECT | 409 MSG-P5-002 mapping in E1-024 (SPEC-019) | COVERED |
| `[S]` §4 step 6, BR2 | New version is a new blob; earlier readable | SPEC-010, -011, -015 | DIRECT | `docVersion` in the name | COVERED |
| `[S]` §4 step 7 | Readiness visible to the platform administrator | SPEC-009, -020 | DIRECT | `documentHub` health component and `readiness()`; SCR-44 display has no owner story (DGAP-20, SPEC-019) | COVERED |
| `[S]` BR3, X3 | Managed identity only; keys and SAS disabled | SPEC-001, -007 | DIRECT | | COVERED |
| `[S]` BR7, X9, AC12 | Identical content returns the existing blob; different is a violation | SPEC-012 | DIRECT | DGAP-14 | COVERED |
| AC1 | Overwrite refused, hash unchanged, audit, replaceContent → 409 | SPEC-004, -012, -013, -014, -018, -019 | DIRECT | Storage clause in SIT with a raw client (DGAP-15); 409 in E1-024 | COVERED |
| AC2 | Delete refused, blob readable | SPEC-004, -018 | DIRECT | Storage level; SIT | COVERED |
| AC3 | v2 in write-once container allowed; v1 and v2 readable | SPEC-010, -011, -015 | DIRECT | | COVERED |
| AC4 | Standard container keeps versions; soft delete restore within 30 days | SPEC-003, -011, -018 | DIRECT | SIT | COVERED |
| AC5 | Identities hold only their roles | SPEC-005, -018 | DIRECT | SIT listing to RW-SECADM | COVERED |
| AC6 | Key or SAS refused | SPEC-001, -018 | DIRECT | SIT | COVERED |
| AC7 | Identity with no role refused | SPEC-005, -018 | DIRECT | SIT | COVERED |
| AC8 | Public network access refused | SPEC-001, -018 | DIRECT | SIT | COVERED |
| AC9 | Missing policy: not ready naming rwb-docs-legal; upload 503 MSG-GEN-006; no document row | SPEC-009, -011, -019, -020 | DIRECT | HTTP 503 and "no row" in E1-024/E1-026 (seam, DGAP-17) | COVERED |
| AC10 | No answer in 10 s → StorageUnavailableException; upload 503 | SPEC-007, -013, -019 | DIRECT | HTTP 503 in E1-024/E1-026 | COVERED |
| AC11 | Quarantine closed to user sessions; only SY-OCR writes | SPEC-005, -015 | DIRECT | `open()` allow-list | COVERED |
| AC12 | Same hash → no overwrite, existing ref; different → violation | SPEC-012 | DIRECT | | COVERED |
| X2, X4–X8, X10 | Exception paths | see Exceptional-case behaviour | DIRECT | X10 is TC-TE-012-13 via the E1-026 endpoint | COVERED |
| `[S]` §13 flag | `rwb.dochub.storage-containers`: off → not ready, writes refused with 503 | SPEC-006, -009, -011, -020 | DIRECT | | COVERED |
| `[S]` §17 guardrails | No business values in code; no personal data; no keys, connection strings or SAS | SPEC-006, -007, -010, -014, -017 | DIRECT | Emulator key exception is local only (SPEC-017) | COVERED |
| `[DL]` D-RCV-31 | Published `DocumentStorage`; store refuses when the policy is absent; no blob written except through it | SPEC-010, -011 | DIRECT | | COVERED |
| FR-RWB-007 | Functional group for BR-RWB-007 (document hub), shared by RWB-E1-024 and 11 other stories; this story's part is the storage and its write path | SPEC-001 to -017, -020 | DIRECT | Traceability Matrix §2 and row 007 | COVERED |
| REQ-DCM-003 | Legal documents are write-once | SPEC-004, -011, -012, -013 | DIRECT | `[S]` §18 | COVERED |
| REQ-DCM-002 | The document hub is the system of record for documents | SPEC-010, -011, -015 | DIRECT | Single write path (`[DL]` D-RCV-31); the document row is E1-024 | COVERED |
| NFR-029 | Write-once storage for legal documents | SPEC-004, -009, -012 | DIRECT | `[NFR]` | COVERED |
| NFR-053 | Data encrypted at rest and in transit | SPEC-001 | DIRECT | TLS 1.2 minimum; platform encryption at rest (DGAP-06) | COVERED |
| CTL-12 | "Legal documents cannot be changed or deleted; a new version is added instead" (`[CTL]`) | SPEC-004, -010, -011, -012, -013, -014, -018 | DIRECT | SIT evidence TC-TE-012-01, -02; MSG-P5-002 mapping in E1-024 | COVERED |
| CTL-09 | Every request is checked against role, capability and scope (`[CTL]`) | SPEC-005, -015, Guardrails | DIRECT | Storage side: container-scope roles only (AC5, AC7, AC11). Request side: `open()` is not an authorization point; callers apply the check (E1-024) | COVERED |
| Health endpoint | Actuator health, details for RW-PLATADM | SPEC-020 | INHERITED_EXISTING_BEHAVIOR | `application.yaml` management block | COVERED |
| `[TE001]` SPEC-009, -022, -024, -025 | Placement in `dochub`, BND-5, carried tests, published list | SPEC-016, -022 | DIRECT | Precondition: RWB-TE-001 merged | COVERED |
| `[DL]` D-RCV-31 re-store | Confirmed write-once document re-stored from rwb-docs into rwb-docs-legal at `{caseId}/{documentId}/v{docVersion}`; standard object kept | SPEC-010, -011 | DIRECT | Standard source allowed only with `writeOnce=true` and the same name; callers RWB-E1-032 / RWB-E1-054 (SPEC-019) | COVERED |

37 rows, 37 covered, 0 blocked. The RWB-E1-017 archive-container expectation is a consumer's expectation, not a TE-012 rule: it is recorded in DGAP-22, CLAR-018 and SPEC-019, not in this table. Counting rule for `CONTRADICTIONS`: only contradictions left unresolved in this spec are counted, so the value is 0; source conflicts settled by precedence are listed in `document-gaps.md` (DGAP-01, -02, -08, -14, -15, -17, -22, -23, -24).

## User story intent interpretation

`[S]` §1: a platform administrator wants blob containers for documents, a write-once container for legal types, reached by managed identity, "so that legal documents cannot be overwritten". The deliverable is the storage plus the single code path through which the service writes it (`[DL]` D-RCV-31). It is not the document record, the type-to-container choice, retention classes, legal hold or backup (`[S]` §19). The business outcome is REQ-DCM-003 and REQ-DCM-002 (`[S]` §18).

## Entry trigger and preconditions

| Trigger | Preconditions | Source |
|---|---|---|
| Builder starts this story | RWB-TE-001 merged in this repository (`dochub.api`, `dochub.storage`, BND-5 map, SPEC-020 coverage tasks and SPEC-024 tests present). If it is not merged, this story does not start | `[TE001]` SPEC-022; `[BSEQ]` order 2 before order 7 |
| Platform administrator applies the template per environment | DL27 option A (one storage account per environment in the SCB tenant, private endpoint); managed identities RWB-{DEV,SIT,UAT,PROD}-SY-OCR and the ACE service identity exist; the ACE pipeline can apply storage templates to DEV and SIT | `[S]` §3 |
| Service start | Flag `rwb.dochub.storage-containers` on; `rwb.dochub.*` properties set | `[S]` §4 step 3, §13 |
| A P5 caller stores or opens a blob | Readiness READY for a store | `[S]` BR5; `[DL]` D-RCV-31 |

DL26 and DL27 are open; the story gives assumed defaults (3,650 days; 30 days), so they do not block (DGAP-04).

## Field-level behaviour matrix

### Configuration properties (SPEC-006)

Bound by the package-private record `dochub.storage.DocumentStorageProperties` (`@ConfigurationProperties("rwb.dochub")`). P5 reads no other module's properties type and no key outside `rwb.dochub` (`[TE001]` SPEC-023).

| Property | `application.yaml` | `application-local.yaml` | Rule | Source |
|---|---|---|---|---|
| `rwb.dochub.storage-containers` | `${RWB_DOCHUB_STORAGE_CONTAINERS:false}` | `true` | Feature flag. Off: not ready, every store and open refused | `[S]` §13; ASM-TE012-14 |
| `rwb.dochub.storage.account-url` | `${RWB_DOCHUB_ACCOUNT_URL:}` | — | Required when the flag is on and emulator is false; `https://` only | `[S]` §13 |
| `rwb.dochub.storage.timeout-seconds` | `10` | `10` | Integer 1–60; overall time per SDK call, retries included; also the deadline of a readiness probe and of a `store()` caller's wait for it (SPEC-009) | `[S]` §13, AC10 ("after 10 seconds") |
| `rwb.dochub.storage.readiness-recheck-seconds` | `30` | `30` | Integer 1–300; how long a NOT_READY probe result is reused before `store()` probes again (SPEC-009) | ASM-TE012-30 (assumed; no document gives a value) |
| `rwb.dochub.storage.service-identity-client-id` | `${RWB_DOCHUB_SERVICE_MI_CLIENT_ID:}` | — | ACE service identity client ID; blank uses the default managed identity (not a readiness failure) | ASM-TE012-05 |
| `rwb.dochub.storage.ocr-identity-client-id` | `${RWB_DOCHUB_OCR_MI_CLIENT_ID:}` | — | RWB-{ENV}-SY-OCR client ID; blank gives NOT_READY `IDENTITY_NOT_CONFIGURED:rwb-quarantine`. Not used and not checked in emulator mode (SPEC-017) | ASM-TE012-05, -31 |
| `rwb.dochub.storage.emulator` | `false` | `true` | Enables emulator mode together with the `local` profile (SPEC-017). Like any Spring property it can be overridden by an environment variable or system property, so it is not the only guard | ASM-TE012-11 |
| `rwb.dochub.storage.emulator-connection-string` | not present | `${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}` | Used only when `emulator` is true | ASM-TE012-11 |
| `rwb.dochub.container.intake` | `rwb-intake` | same | Container name | `[S]` §4, §13 |
| `rwb.dochub.container.standard` | `rwb-docs` | same | Container name | `[S]` §4, §13; `[FSD-P5]` |
| `rwb.dochub.container.legal` | `rwb-docs-legal` | same | Container name | `[S]` §4, §13; `[DL]` D-RCV-31 |
| `rwb.dochub.container.quarantine` | `rwb-quarantine` | same | Container name | `[S]` §4, §13; `[E1-041]` |

Startup fails when: `emulator` is true and the `local` profile is not active; the four names are not distinct or not 3–63 characters of lower-case letters, digits and hyphens; `timeout-seconds` is outside 1–60; `readiness-recheck-seconds` is outside 1–300; the flag is on, `emulator` is false and `account-url` is blank or not `https`; `emulator` is false and an emulator connection string is set; `emulator` is true and `account-url` is set. The `rwb.blob` block is removed.

### BlobRef (`dochub.api`, used by RWB-E1-024, -026, -041, -049, -057)

| Member | Rule | Source |
|---|---|---|
| `container` | 3–63 characters, `[a-z0-9-]`; not null | Azure container naming |
| `blobName` | 1–1024 characters; not starting with `/` | Azure blob naming; intake names are set by RWB-E1-026/-057 |
| `storageRef()` | `container + "/" + blobName` | `[S]` §11; `[E1-024]` step 7 `{container}/{caseId}/{documentId}/v1`; `[SCH]` `storage_ref varchar(400)` |
| `static fromStorageRef(String)` | Splits at the first `/`; each part validated as above; null, blank, no `/`, or a value over 400 characters → `IllegalArgumentException` | Finding SG-02; `[SCH]` `varchar(400)` |

A document blob name is `{caseId}/{documentId}/v{docVersion}` with UUIDs in canonical lower-case form: at most 149 characters with a 63-character container, 100 with the default names, so it fits `varchar(400)`.

### BlobWriteRequest (input to `DocumentStorage.store`)

| Field | Type | Rule | Source |
|---|---|---|---|
| `caseId` | UUID | Not null; `recovery_case.id` | `[S]` §11; `[API]` caseId uuid; `[SCH]` |
| `documentId` | UUID | Not null; `document.id` | `[SCH]` |
| `docVersion` | int | ≥ 1 | `[SCH]` `doc_version` (DF-DOC-011) |
| `writeOnce` | boolean | true → legal container; false → standard container | `[S]` §4 step 4; DF-DOC-010 |
| `source` | BlobRef | Not null. Either the intake container (any name), or, only when `writeOnce = true`, the standard container with `blobName` equal to the target name `{caseId}/{documentId}/v{docVersion}` (the D-RCV-31 re-store). Any other container (legal, quarantine, unknown) is refused | `[E1-024]` step 1 ("the file in the intake container"), step 7; `[DL]` D-RCV-31 (re-store into rwb-docs-legal at the same `{caseId}/{documentId}/v{docVersion}`; standard object kept) |

A violation raises `IllegalArgumentException` with no storage call.

### StoredBlob (output of `store`)

| Field | Value | Source |
|---|---|---|
| `ref` | BlobRef of the written (or existing) blob | `[S]` §11 |
| `sha256` | Lower-case hex SHA-256 of the content | `[S]` §13 ContentHashGuard |
| `size` | Bytes | — |
| `existing` | true when ContentHashGuard returned an existing write-once blob | `[S]` AC12 |

### Blob metadata written at creation

| Key | Value | Rule |
|---|---|---|
| `sha256` | As `StoredBlob.sha256` | Read by ContentHashGuard. No other metadata; no personal data (`[S]` §17) |
| Content-Type header | The source blob's content type; `application/octet-stream` when absent | — |

### Audit event `DOCUMENT_CHANGE_REFUSED` (SPEC-014)

| Field | Value | Source |
|---|---|---|
| `eventType` | `DOCUMENT_CHANGE_REFUSED` | `[FSD-P5]` AC-ALT-P5-001-01; `[E1-024]` X1 |
| `occurredAt` | UTC instant | `[S]` AC1 "with the identity and the time" |
| `storageIdentity` | `ACE_SERVICE` or `SY_OCR` (role label, not a secret) | `[S]` AC1 |
| `operation` | `WRITE` or `DELETE` | `[S]` §13 StorageErrorMapper |
| `documentId` | UUID parsed from the blob name, when the name has the document form | `[FSD-P5]` "with the document ID and the caller" |
| `actorId` | Subject of the authenticated principal in the security context when present; the field is absent for system calls | `[FSD-P5]` "the caller"; staff identifier only |
| `container`, `blobName` | As BlobRef | IDs only (`[S]` §17) |
| `reason` | `HASH_MISMATCH`, or `STORAGE_REFUSED` with the Azure error code | `[S]` BR7, X1 |
| `traceId` | Current trace ID if present | Observability baseline |

No content, hash of content of another blob, account URL, client ID or personal data is logged.

### Health component `documentHub` (SPEC-020)

| Detail | Values |
|---|---|
| status | Flag off: `UNKNOWN`. Flag on: `UP` (READY), `DOWN` (NOT_READY), `UNKNOWN` (NOT_EVALUATED, before the start evaluation completes) |
| `ready` | `true` or `false` |
| `containers` | Each configured name → `PRESENT`, `MISSING` or `UNVERIFIED` (flag on only) |
| `legalPolicy` | `PRESENT`, `MISSING` or `EMULATED` (flag on only) |
| `identities` | `CONFIGURED`, `NOT_CONFIGURED` or `EMULATED` (emulator mode, SPEC-017) (flag on only) |
| `reasons` | `FLAG_OFF`, `NOT_EVALUATED`, `CONTAINER_MISSING:<name>`, `LEGAL_POLICY_MISSING:<name>`, `IDENTITY_NOT_CONFIGURED:<name>`, `UNREACHABLE` |
| `checkedAt` | UTC instant the last probe ended (absent when never evaluated); an operation's outcome never sets it (SPEC-009) |

Details are shown only to RW-PLATADM (existing `show-details: when-authorized`). No account URL, key or client ID is shown.

## Status-transition matrix

`[S]` §9: no case or document status changes. The only state is readiness, held in memory in `StorageReadinessIndicator`. **Only the readiness probe (SPEC-009) writes it**; an operation's own outcome never does (round 4 finding SG-26):

| From | Event | Guard | To |
|---|---|---|---|
| (start) | Context starts | Flag off | FLAG_OFF (terminal while the flag is off; no storage call ever) |
| (start) | Context starts | Flag on | NOT_EVALUATED |
| NOT_EVALUATED | Probe ends (start probe on `ApplicationReadyEvent`, or a probe a `store()` started) | All four containers present; legal policy present or `EMULATED`; OCR client ID set (service identity: configured client ID or the default managed identity); in emulator mode the identity checks are `EMULATED` (SPEC-017) | READY |
| NOT_EVALUATED or READY or NOT_READY | Probe ends | Any check fails, storage unreachable, or the probe deadline (`timeout-seconds`) passes | NOT_READY (reasons; `checkedAt` = probe end) |
| NOT_READY | Probe ends | All checks pass | READY |
| READY | Probe ends | All checks pass | READY (`checkedAt` = probe end) |
| NOT_EVALUATED | `ApplicationReadyEvent` | No probe in flight → starts the single probe; a probe in flight (started by an earlier `store()`) → joins it, starts none | Unchanged until the probe ends |
| NOT_EVALUATED | `store()` called, no probe in flight (for example from a lifecycle bean before `ApplicationReadyEvent`) | — | Unchanged; the caller starts the single probe and waits at most `timeout-seconds`; the start event later joins or, if that probe ended less than `readiness-recheck-seconds` before, starts none |
| NOT_EVALUATED | `store()` called while a probe runs | — | Unchanged; the caller joins the probe and waits at most `timeout-seconds` |
| NOT_READY | `store()` called, probe result younger than `readiness-recheck-seconds` | — | Unchanged; `StorageUnavailableException(NOT_READY)` at once, no storage call |
| NOT_READY | `store()` called, probe result older than `readiness-recheck-seconds` | No probe in flight → one probe starts; a probe in flight → the caller joins it | Unchanged until the probe ends; the caller proceeds on READY, gets `NOT_READY` on NOT_READY, or `TIMEOUT` when its wait ends first |
| any (NOT_EVALUATED, READY or NOT_READY) | A `store()` or `open()` operation ends in `TIMEOUT`, transport `UNAVAILABLE` (5xx or I/O after SDK retries) or `ContainerNotFound` | No probe in flight and none ended within `readiness-recheck-seconds` → one background probe is requested; otherwise none (suppressed) | Unchanged; only a probe's result can change the state |
| any | A `store()` or `open()` operation ends in any other outcome (`BLOB_MISSING`, `ACCESS_REFUSED`, write-once refusal, conflict, other 4xx, or a caller's size or type refusal) | — | Unchanged; no probe requested |
| any | Health read | — | Unchanged; no storage call |

## Exceptional-case behaviour

| ID | Case | Behaviour in this story | Message (owner of HTTP mapping) | Source |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | Through the adapter: ContentHashGuard finds a different hash → `WriteOnceViolationException` + audit, no write. Raw client: storage returns `BlobImmutableDueToPolicy` (SIT) | MSG-P5-002, 409 (E1-024) | `[S]` X1, AC1; `[MSG]` |
| X2 | Delete of a write-once blob | Storage refuses; no delete is published here; `StorageErrorMapper` maps a refused `DELETE` to `WriteOnceViolationException` + audit for later callers | MSG-P5-002 (E1-024) | `[S]` X2, AC2 |
| X3 | Account key or SAS | Storage refuses; the service never builds a key or SAS client outside emulator mode | None | `[S]` X3, AC6 |
| X4 | Identity with no role | `StorageUnavailableException(ACCESS_REFUSED)` and an ERROR log line with container and error code | MSG-GEN-006, 503 (E1-024) | `[S]` X4, AC7; ASM-TE012-15 |
| X5 | Outside the private endpoint | Storage refuses; network level, SIT | None | `[S]` X5, AC8 |
| X6 | Container or policy missing at start | NOT_READY naming the container; `store()` raises `StorageUnavailableException(NOT_READY)` | MSG-GEN-006, 503 (E1-024/E1-026) | `[S]` X6, AC9; `[DL]` D-RCV-31 |
| X7 | No answer within the timeout | `StorageUnavailableException(TIMEOUT)` or `(NOT_READY)` (SPEC-009) within `timeout-seconds`: an operation that gets no answer raises `TIMEOUT`; a `store()` while the hub is not READY raises `NOT_READY` (fresh result, or the probe ended NOT_READY) or `TIMEOUT` (its wait for the probe ended first) | MSG-GEN-006, 503 (E1-024/E1-026) | `[S]` X7, AC10 |
| X8 | User session reads quarantine | `open()` accepts only the standard and legal containers; any other ref → `IllegalArgumentException`, no storage call; the ACE identity holds no role on `rwb-quarantine` | None | `[S]` X8, AC11 |
| X9 | Same name, same content, write-once | Guard compares first: same hash → existing ref, no upload. Race: conditional upload gets `BlobAlreadyExists` → guard re-compares once | None | `[S]` X9, AC12; DGAP-14 |
| X10 | Role without Documents C uploads | Not reachable here; endpoint check in E1-026 (TC-TE-012-13) | MSG-P4-002, 403 | `[S]` X10 |
| — | Store source not allowed (not intake; standard with `writeOnce=false` or a different name; legal, quarantine, unknown) | `IllegalArgumentException`, no storage call | None (programming error) | `[E1-024]` step 1; `[DL]` D-RCV-31 |
| — | Storage 5xx or I/O failure after SDK retries | `StorageUnavailableException(UNAVAILABLE)`; a background probe is requested (SPEC-009); readiness unchanged until it ends | MSG-GEN-006, 503 | `[S]` §12 |
| — | `open()` of a blob that does not exist | `StorageUnavailableException(BLOB_MISSING)`; readiness unchanged, no probe | MSG-GEN-006, 503 (E1-024); the Error and Message Standard v4 has no message for a stored file that is missing, and the caller owns the mapping | ASM-TE012-15 |
| — | Client timeout, but the server completed the upload | The caller retries (E1-024 X8, COPY_PENDING); the guard finds the same hash and returns `existing = true` | None | `[E1-024]` X8; review input 3 |
| — | Flag off | `StorageUnavailableException(NOT_READY)`; reason `FLAG_OFF` | MSG-GEN-006, 503 | `[S]` §13 |

`StorageUnavailableException` carries `Reason {NOT_READY, TIMEOUT, UNAVAILABLE, ACCESS_REFUSED, BLOB_MISSING}` and the container name (ASM-TE012-10).

## API change assessment

| Item | Assessment |
|---|---|
| Endpoints added or changed | None. `[S]` §12 "No endpoint of its own" |
| Endpoint that depends on this story | `POST /api/recovery/v1/cases/{caseId}/documents` (`postCasesCaseidDocuments`, `[API]`), owned by RWB-E1-026/RWB-E1-024 |
| Actuator | `documentHub` component under the existing `/actuator/health` (SPEC-020). Operational endpoint outside the API specification, as README decision 6 records for existing operational endpoints |
| Published Java surface | `dochub.api` types change (SPEC-010, SPEC-022); recorded in `contracts/backend-apis.json` |
| Contract file | `contracts/backend-apis.json`: `NO_API_CHANGE` |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | `[S]` §15 | No screen; SCR-44 has no owner story (DGAP-20) | n/a |
| Backend | YES | REQUIRED | `[TE001]` SPEC-020: LINE, INSTRUCTION, BRANCH and METHOD each ≥ 80%, bundle over all main `recovery/**` classes, no exclusion, `test` execution data only; run by `./gradlew test recoveryCoverageVerification` outside `check` (D-RCV-28 (3), D-RCV-40). Plus, for this story, every main class under `recovery/dochub/**` ≥ 80% on the four counters (changed code first, `[TS]` §6) and no bundle counter lower than on `develop-recovery` before the merge (SPEC-023) | SPEC-006 to -017, -020 to -023; AC9, AC10, AC11, AC12; BR5, BR7 | New and evolved adapter, guard, mapper, readiness, audit, config and emulator logic | Every T-TE012 unit test in SPEC-018 passes in `test`; `recoveryCoverageVerification` passes; per-class and no-drop checks pass from the report; `RecoveryBoundaryTest` and `ModulithTest` pass under the RWB-TE-001 module map; T-TE001-14 passes with the updated `dochub.api` list |

## Frontend Specification

Not applicable. No screen, component, route or client type changes (`[S]` §15). `[BN]` step 7: "No screen is built here, and the monitor itself belongs to another story." No story in Build Sequence v6 builds SCR-44 (DGAP-20); this story exposes the value the screen will read (SPEC-020). `contracts/frontend-integrations.json` records `NOT_APPLICABLE`.

## Backend Specification

### SPEC-RWB-TE-012-001 — Storage account settings (template)

The template sets, per environment, on one storage account (DL27 option A, `[S]` §3):

| Setting | Value | Source |
|---|---|---|
| Shared key access | Disabled | `[S]` §4 step 1, BR3 |
| Public network access | Disabled | `[S]` §4 step 1; `[ENV]` §3; `[SEC]` Network |
| Minimum TLS | 1.2 | `[S]` §4 step 1; NFR-053 "in transit" |
| Private endpoint | `Microsoft.Network/privateEndpoints` with group `blob`, in the subnet given by the required parameter `privateEndpointSubnetId` (ACE network) | `[S]` §3, §4 step 1; `[ENV]` §3 |
| Region, redundancy SKU, default access tier | Required parameters `location`, `skuName`, `accessTier` with no default | DGAP-05, -07, -13; ASM-TE012-12 |
| Identities for role assignments | Required parameters `aceServicePrincipalId`, `ocrPrincipalId` with no default (object IDs, not secrets) | `[S]` §4 step 2, AC5 |
| Storage account name | Required parameter `storageAccountName` with no default; shape `^[a-z0-9]{3,24}$`; the template names the account with it | `[AZ-GET]` `accountName` pattern; environment fact (open item) |
| Encryption at rest | Platform default (Microsoft-managed keys); no key parameter | NFR-053 says only "encrypted" (DGAP-06); ASM-TE012-12 |

Template format: an Azure Resource Manager JSON template `infra/azure/document-storage/azuredeploy.json` with `azuredeploy.<env>.parameters.json` for dev, sit, uat and prod. The document set names no format (`[S]` §13 "in the format the ACE team uses"; `[ENV]` §4 names pipeline gates and the release path but no template format or folder): DGAP-09. Reason for ARM JSON: it is Azure's native deployment format with no compile step, so the conformance test (T-TE012-15) reads it with the Jackson already on the test classpath and runs in pipeline gate 1 "every unit … test passes" (`[ENV]` §4.1) with no new tool (`[AGENTS]` §4.4).

**Required inputs, parameter files and the pre-deploy check** (round 4 finding SG-27):

| File | Holds | Checked by |
|---|---|---|
| `azuredeploy.parameters.schema.json` | The list of every required input, one entry each: name, type, a shape pattern, owner, needed by. Inputs: `storageAccountName`, `location`, `skuName`, `accessTier`, `privateEndpointSubnetId`, `aceServicePrincipalId`, `ocrPrincipalId`, `deployLegalPolicy`. A plain JSON list read with Jackson (no JSON-schema library) | T-TE012-15 |
| `azuredeploy.local.parameters.json` | Synthetic, shape-valid values for every required input (for example an all-zero subscription GUID in the subnet ID, location `conformance`). Used only by T-TE012-15; never applied | T-TE012-15; the pre-deploy check refuses it |
| `azuredeploy.dev.parameters.json`, `.sit.`, `.uat.`, `.prod.` | Every required input; each value is either a decided value or exactly the placeholder `__SET_BEFORE_APPLY__`. UAT and PROD hold placeholders for every undecided value; DEV and SIT hold them until the platform team supplies the values | T-TE012-15 (presence and shape only); the pre-deploy check (values) |

T-TE012-15 is the unit test: it checks the template against the schema list and the local file, and checks that each environment file names every input with a shape-valid value or the placeholder. It never needs an undecided value, so it passes in `test` at merge.

The **pre-deploy check** is not a unit test. `infra/azure/document-storage/Test-DeployParameters.ps1` (PowerShell, as `scripts/dev.ps1`; no new tool) runs as step 1 of the `RUNBOOK.md` "Apply" procedure before every deployment, in every environment, and as the first step of an ACE pipeline infrastructure stage if one is added (`[ENV]` §4.2 has none, DGAP-24). It takes six explicit inputs: `-Environment`, `-ResourceGroup`, `-StorageAccountName`, `-ParameterFile`, `-Mode` and `-DeployLegalPolicy` (the effective value: the file value, or the one-time override for the first PROD apply). It exits non-zero, and the apply does not run, when: the file is the local file; any schema input is missing, blank, the placeholder, or fails its shape pattern; the mode is not `Incremental`; `-StorageAccountName` differs from the file's `storageAccountName`; or, in PROD with an effective `deployLegalPolicy` of true, the legal container's policy state is not "no policy" (table below; SPEC-004). On success it prints the one deploy command step 2 runs unchanged: `az deployment group create --resource-group <rg> --template-file azuredeploy.json --parameters @<parameter file> deployLegalPolicy=<effective value> --mode Incremental`, so the resource group, file and value checked are the ones applied. Incremental mode is required because in complete mode Azure deletes a resource whose `condition` is false (`[AZ-COND]` "Complete mode"; `[AZ-MODES]` "Complete mode"), while incremental mode "leaves unchanged" resources not in the deployment (`[AZ-MODES]` "Incremental mode").

"No policy" is an observable state, read in this order with the inputs `-ResourceGroup` and `-StorageAccountName` (a mismatch with the file's `storageAccountName` is a refusal):

| # | Observation | Read with | Result |
|---|---|---|---|
| 1 | The account does not exist in the resource group: `az storage account list --resource-group <rg> --query "[?name=='<account>']"` returns `[]` | Azure CLI | No policy → accept |
| 2 | The account exists and `az storage container-rm exists --resource-group <rg> --storage-account <account> --name rwb-docs-legal` returns `"exists": false` | `[AZ-CLI-CRM]` "exists" | No policy → accept |
| 3 | The container exists and `az storage container-rm show` (Storage Resource Provider "Blob Containers - Get") returns `properties.hasImmutabilityPolicy` = `false` | `[AZ-CLI-CRM]` "show"; `[AZ-GET]` `hasImmutabilityPolicy` ("set to false by SRP if ImmutabilityPolicy has not been created") | No policy → accept |
| 4 | `properties.hasImmutabilityPolicy` = `true`, whatever `properties.immutabilityPolicy.properties.state` (`Unlocked` or `Locked`) | `[AZ-GET]` | Policy present → refuse |
| 5 | Any command fails (resource group not found, authorisation, network, unparsable output) | — | Unknown → refuse |

This replaces reading `az storage container immutability-policy show` for the decision, because its reference (`[AZ-CLI-IMM]`) documents only the existing-policy case, so an absent policy would surface as an undocumented error rather than an observable value. The lock step and the "Extend" step still use that command group for the ETag (`[AZ-CLI-IMM]`).

Run by RW-PLATADM (`[S]` §10); maintained by the platform team; the deploy step it guards is approved as `[ENV]` §4.2 names for that environment. Evidence: its output is kept with the apply record. Builder evidence (not automated, on disposable DEV resources standing in for PROD, environment argument `prod`, with a completed copy of the PROD file): **accepts** the first PROD apply with `-DeployLegalPolicy true` when the account does not yet exist (row 1) and when the account exists without the legal container (row 2), and in both cases prints the command with `--resource-group`, `--template-file`, `--mode Incremental` and `deployLegalPolicy=true`; **refuses** the same run once the template has created the (unlocked) policy (row 4), a run naming a resource group that does not exist (row 5), a `-StorageAccountName` that differs from the file, a copy of the PROD file holding a placeholder, and mode `Complete`; accepts a completed copy of the local file renamed as an environment file for a non-PROD environment.

Each undecided value is an open item with an owner and a "needed by" (`shared-updates.md` §3). A document gap is recorded only where the document set should hold the value: region (DGAP-13), redundancy SKU (DGAP-07), access tier (DGAP-05). Subnet IDs and identity object IDs are environment facts the document set does not hold, so they are open items, not gaps.

### SPEC-RWB-TE-012-002 — Containers (template)

Four private containers named by parameters with the defaults `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` (`[S]` §4 step 1). The values must equal the `rwb.dochub.container.*` properties for that environment.

### SPEC-RWB-TE-012-003 — Versioning and soft delete (template)

Blob versioning on; blob soft delete on with `softDeleteDays` (default 30, ASM-TE012-02) (`[S]` §4 step 2, BR6). In Azure these are blob-service (account) settings, so they also apply to the other three containers. The interaction with the legal policy is checked early in DEV, as a spike before SIT (DGAP-03; review input 2). If Azure requires version-level immutability with versioning on, SPEC-004 and the `hasImmutabilityPolicy` check change, and this spec is re-issued.

### SPEC-RWB-TE-012-004 — Write-once policy (template)

Container-level time-based immutability policy on `rwb-docs-legal`: the template declares the container's `immutabilityPolicies` child resource with `immutabilityPeriodSinceCreationInDays` = `legalRetentionDays` (default 3650, ASM-TE012-01) and `allowProtectedAppendWrites` false. The policy is unlocked after every apply. No legal hold (`[S]` §19). The policy resource carries the ARM `condition` `[parameters('deployLegalPolicy')]`: `true` in the DEV, SIT and UAT files, `false` in the PROD file.

**PROD lock: a runbook step outside the template** (`[S]` BR1 "locked in PROD and unlocked in DEV, SIT and UAT"). An ARM template cannot lock the policy (the lock is a separate action on the policy, and the policy's state is read-only in the template), so the template has no lock parameter. `[S]` §13 lists "legalPolicyLocked true in PROD only" as a template parameter; that parameter is not created, and the lock is this step instead (DGAP-24, Blocker = No).

| Field | Value | Source |
|---|---|---|
| What | Lock the time-based immutability policy on `rwb-docs-legal` in PROD (Azure CLI `az storage container immutability-policy lock`, with the policy's ETag) | `[S]` BR1 |
| Where written | `infra/azure/document-storage/RUNBOOK.md`, section "PROD lock", committed with the template; reviewed at the plan gate | ASM-TE012-04 |
| When | In the PROD change window, after the template apply and before the PROD flag `rwb.dochub.storage-containers` is turned on | `[ENV]` §4.2 "Deploy to PROD … in the monthly change window" |
| Who runs it | RW-PLATADM, platform administrator | `[S]` §10 Authority (applies the infrastructure template) |
| Who approves it | The release owner in the ACE team with the application owner, as part of the PROD deploy approval; the step is irreversible, so the approval names it explicitly | `[ENV]` §4.2 "Deploy to PROD" approvers |
| Evidence | Output of `az storage container immutability-policy show` for `rwb-docs-legal` showing state `Locked` and the period equal to `legalRetentionDays`, attached to the PROD change record; RW-SECADM receives it with the role-assignment listing | `[S]` §13 "Done when" (security administrator review) |
| Never | Run in DEV, SIT or UAT | `[S]` BR1 |

**Later PROD applies after the lock** (round 4 finding SG-28). Azure allows changes to an unlocked policy only: the create-or-update operation "Creates or updates an unlocked immutability policy" (`[AZ-REST]`), and a locked time-based policy cannot be deleted and can only be extended, not shortened, with at most five increases for a container-level policy (`[AZ-IMM]` "Locked versus unlocked policies"). So the template never sends the policy after the PROD lock:

| Step | Rule | Enforced by |
|---|---|---|
| First PROD apply | Run once with the override `deployLegalPolicy=true`, passed to the pre-deploy check as the effective value and applied by the command the check prints (`--mode Incremental`), then the lock step above | Pre-deploy check: in PROD, an effective `deployLegalPolicy=true` is accepted only in an observable "no policy" state (SPEC-001 table rows 1–3: account absent, legal container absent, or `hasImmutabilityPolicy` false); refused when a policy exists in any state or a read fails |
| Every later PROD apply | PROD file value `false`, mode `Incremental`: the policy resource is not created (`[AZ-COND]`), and incremental mode leaves unchanged resources that are not deployed (`[AZ-MODES]` "Incremental mode"), so the apply neither changes nor removes the locked policy; account, containers, endpoint and roles are still applied | T-TE012-15 (PROD file `false`; policy resource conditional) and the pre-deploy check (mode `Incremental` only) |
| Change of the period in PROD | Only the `RUNBOOK.md` "Extend" step (`az storage container immutability-policy extend` with the policy ETag): increase only, at most five times over the policy's life, same approval as the lock | `RUNBOOK.md`; `[AZ-IMM]` |
| Shortening or removal in PROD | Not possible and not attempted | `[AZ-IMM]` |

The DGAP-03 DEV spike also applies the template on a disposable DEV account once with `deployLegalPolicy=true` and then once with `false` in incremental mode, and confirms the (unlocked) policy is unchanged (ASM-TE012-33). The lock and the "Extend" step are never run outside PROD (`[S]` BR1); the "Extend" step follows `[AZ-IMM]` and is first used in PROD, with the same approval as the lock.

The data-plane identity cannot read the lock state (SPEC-009), so no service test covers it; T-TE012-15 asserts that the template declares the policy and its period, that the policy resource is conditional on `deployLegalPolicy`, and that it has no lock parameter. TC-TE-012-09 (policy removed in DEV) is unchanged.

### SPEC-RWB-TE-012-005 — Role assignments (template)

| Identity | Role | Scope | Source |
|---|---|---|---|
| ACE service managed identity | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-docs-legal` (each container) | `[S]` §4 step 2, AC5 |
| RWB-{ENV}-SY-OCR | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-quarantine` (each container) | `[S]` §4 step 2, AC5; `[URP]` |

No account-scope data role; no other identity. RW-SECADM reviews the SIT listing (`[S]` §13 "Done when").

### SPEC-RWB-TE-012-006 — Properties and flag

`DocumentStorageProperties` binds and validates the "Configuration properties" table at startup. It is the successor of the baseline `BlobProperties` (Evolution map). No container name, period or timeout is a literal in Java (`[S]` §17). P5 does not read `rwb.environment` or any other module's configuration type. Flag off: no `BlobServiceClient` is built and no account URL is required; the `DocumentStorage` and `DocumentContainers` beans still exist and refuse (SPEC-008, -011, -015).

### SPEC-RWB-TE-012-007 — DocumentContainersConfig: identities, timeout, no creation

- Successor of the baseline nested `Config`, in `dochub.storage`.
- Flag on, emulator false: two `BlobServiceClient`s against `account-url`, one with the ACE service identity and one with SY-OCR. Each credential is a chain of `WorkloadIdentityCredential` and `ManagedIdentityCredential` only, with the configured client ID. No environment secret, CLI, developer-tool or shared-cache credential (`[S]` §13; BR3; `[SEC]` "one identity per non-human actor").
- Every SDK call goes through one helper that passes `Duration.ofSeconds(timeout-seconds)` as the overall operation timeout, so SDK retries stay inside it (`[S]` AC10).
- No `create`, `createIfNotExists`, `setAccessPolicy` or delete-container call outside `LocalEmulatorBootstrap` (SPEC-017).

### SPEC-RWB-TE-012-008 — DocumentContainers

`dochub.storage.DocumentContainers` with `intake()`, `standard()`, `legal()`, `quarantine()` returning `BlobContainerClient`, and `readiness()`, in the package the story names (`[S]` §13). Intake, standard and legal use the ACE identity; quarantine uses SY-OCR. The class is `public` in the non-published package `dochub.storage`: Modulith keeps it inside P5 (`[TE001]` SPEC-022 (c) uses the same rule), and BND-5 allows its Azure types only for classes in, or under, `dochub.storage` (`[TE001]` SPEC-009). The story calls it a "published interface" (`[S]` §12); under the RWB-TE-001 map it cannot be published, because `dochub.api` would then expose `com.azure.storage` types (DGAP-02). A later P5 package that uses it must sit under `dochub.storage` or add its own package to the P5 `clientPackages` (D-RCV-41: each client library "is allowed only in client packages that their stories add to the map"). Seam: SPEC-019.

Flag off: the `DocumentContainers` bean is present (later P5 beans inject it without `ObjectProvider`), builds no client, every container accessor throws `StorageUnavailableException(NOT_READY)` with no storage call, and `readiness()` returns `ready=false`, `reasons=[FLAG_OFF]` (`[AGENTS]` §3.13). A default-profile context, such as `RecoveryDatabaseIT`, therefore starts without any storage property.

### SPEC-RWB-TE-012-009 — Readiness evaluation

`StorageReadinessIndicator` holds the state of the Status-transition matrix.

- **Only the probe writes readiness.** `ReadinessProbe` (in `dochub.storage`) runs the checks below and is the only writer of the state in `StorageReadinessIndicator`. `store()`, `open()` and `StorageErrorMapper` never write it; an operation's outcome maps only to its own exception (SPEC-013).
- **Checks** (one probe), flag on: for each container, get properties (404 → `MISSING`); for the legal container, `hasImmutabilityPolicy` must be true (`[S]` BR5, AC9). Intake, standard and legal use the ACE identity; quarantine uses SY-OCR. A blank OCR client ID gives `IDENTITY_NOT_CONFIGURED:rwb-quarantine` without a call. A timeout or 5xx gives `UNREACHABLE`. In emulator mode the probe first runs the `LocalEmulatorBootstrap` creates, the identity checks are reported `EMULATED` (no client ID is needed) and quarantine uses the shared-key client (SPEC-017).
- **Probe deadline:** a probe runs its four container checks in parallel (Java 21 virtual threads; no new dependency), and in emulator mode its four creates in parallel before them. The whole probe has one deadline of `timeout-seconds` from its start; each SDK call gets the time left as its timeout, and a check not finished at the deadline counts as `UNREACHABLE`. A probe therefore never takes longer than `timeout-seconds` (10 s), in emulator mode too.
- **Single-flight:** at most one probe is in flight, held as one shared future in `StorageReadinessIndicator`. Every trigger (start event, `store()`, background request) joins the probe in flight and never starts a second one. `ApplicationReadyEvent` (background thread, `[S]` §4 step 3 "on start") starts the start probe unless one is in flight (it joins) or one ended less than `readiness-recheck-seconds` before (it starts none).
- **When `store()` probes:** state READY → no probe. State NOT_READY with `checkedAt` younger than `readiness-recheck-seconds` (default 30, ASM-TE012-30) → refused at once with `NOT_READY`, no storage call. State NOT_EVALUATED, or NOT_READY older than that → the caller joins or starts the probe and waits at most `timeout-seconds` from its own entry. Probe READY → the store proceeds; probe NOT_READY → `StorageUnavailableException(NOT_READY)`; the caller's wait ends first → `StorageUnavailableException(TIMEOUT)`, and the probe goes on to its own deadline and sets the state. Each of the three refusals maps to 503 MSG-GEN-006 at the endpoint (`[S]` AC9, AC10, X6, X7). This bounds the AC10 case: when storage does not answer, `store()` raises within `timeout-seconds` plus scheduling slack (tests use a 1 s bound), not after four or eight timeouts.
- **Background probe request:** when a `store()` or `open()` operation ends in `TIMEOUT`, transport `UNAVAILABLE` (5xx or I/O after SDK retries) or `ContainerNotFound`, the adapter requests a probe on a background thread, unless one is in flight or one ended less than `readiness-recheck-seconds` before. The operation itself still raises its own exception and does not wait for the probe. The probe's result alone moves the state (READY → NOT_READY `UNREACHABLE` or `CONTAINER_MISSING:<name>`). `BLOB_MISSING`, `ACCESS_REFUSED`, write-once refusals, conflicts, other 4xx, and a caller's size or type refusals request no probe and never change readiness. The same rule applies in every state. A request is suppressed only while a probe is in flight or one ended less than `readiness-recheck-seconds` before. So during an outage, while operations keep failing, NOT_READY and `documentHub` `DOWN` follow within `readiness-recheck-seconds` + `timeout-seconds` (40 s with the defaults) of the first failing operation: within `timeout-seconds` when no probe ended in the window, otherwise after the first failing operation once the window has passed. Later stores then fail fast for `readiness-recheck-seconds`.
- **Reuse window:** the 30 s reuse applies to probe results only (ASM-TE012-30).
- **Numbers and where they come from:** probe deadline and caller wait = `timeout-seconds` = 10, from `[S]` §13 and AC10 ("after 10 seconds"); `readiness-recheck-seconds` = 30, assumed (ASM-TE012-30): no document gives a value, and `[ERR]` §3 gives intervals only for inbound loads ("Check each hour"), outbound files, agents and Temporal, none for storage. Both are properties, not reference-table rows, as `[S]` §13 makes the timeout a property. Why a held state is needed: AC10 bounds the store at 10 s, which an unshared, unbounded re-evaluation on every call does not meet (round 3 finding SG-19).
- No scheduled refresh: a probe runs only at start and from `store()` as above. A health read returns the held state and makes no storage call (ASM-TE012-08).
- Lock state and period are not visible to the data-plane identity; the PROD lock is the SPEC-004 runbook step; the policy's presence is checked here (TC-TE-012-09).
- One INFO log line on each change of state, with reasons; no URL or ID.

### SPEC-RWB-TE-012-010 — DocumentStorage (published, `dochub.api`)

```java
package th.co.scb.ace.demo.recovery.dochub.api;

public interface DocumentStorage {
    StoredBlob store(BlobWriteRequest request);   // WriteOnceViolationException, StorageUnavailableException
    byte[] open(BlobRef ref);                      // StorageUnavailableException
    StorageReadiness readiness();
}
public record BlobRef(String container, String blobName) {
    public String storageRef();
    public static BlobRef fromStorageRef(String storageRef);
}
public record BlobWriteRequest(UUID caseId, UUID documentId, int docVersion, boolean writeOnce, BlobRef source) { }
public record StoredBlob(BlobRef ref, String sha256, long size, boolean existing) { }
public record StorageReadiness(boolean ready, List<String> reasons, Instant checkedAt) { }
public class WriteOnceViolationException extends RuntimeException { /* container, blobName */ }
public class StorageUnavailableException extends RuntimeException { /* Reason reason, String container */
    public enum Reason { NOT_READY, TIMEOUT, UNAVAILABLE, ACCESS_REFUSED, BLOB_MISSING } }
```

- No Azure type in `dochub.api` (BND-5). `package-info` (`@NamedInterface("api")`) is unchanged from RWB-TE-001.
- Name per `[DL]` D-RCV-31 and `[E1-024]` §13 ("DocumentStorage … called, never reimplemented"). No source gives the signature (DGAP-19); it is defined here to fit `[E1-024]` §12: E1-024's `StoreRequest.intakeBlobRef` and the `BlobRef file` parameters of `addVersion`, `replaceContent`, `[E1-041]` `scanNow` and `[E1-049]` `read` use this `BlobRef`. The request type is named `BlobWriteRequest` so that `StoreRequest` and `StoredDocument` stay free for E1-024. The same `store()` carries the D-RCV-31 re-store (standard source, `writeOnce=true`, same name); no separate operation is added.
- Implemented by `dochub.storage.BlobStorageAdapter`.

### SPEC-RWB-TE-012-011 — BlobStorageAdapter: store

1. Flag off → `StorageUnavailableException(NOT_READY)`; no storage call.
2. Validate the request (field matrix); a source the `source` rule does not allow → `IllegalArgumentException`; no storage call.
3. State not READY → the SPEC-009 rule: fresh NOT_READY refuses at once; otherwise join or start the single probe and wait at most `timeout-seconds`; not READY → `StorageUnavailableException(NOT_READY)`, wait ended first → `StorageUnavailableException(TIMEOUT)`; no write in either case (`[DL]` D-RCV-31; `[S]` AC10).
4. Download the source blob (ACE identity, which holds Contributor on intake and standard) within the timeout; compute SHA-256 and size; read its content type. For the D-RCV-31 re-store the source is the standard-container object at the same name; it stays in place as evidence under the `rwb-docs` versioning policy.
5. `writeOnce = false` → upload to the standard container at `{caseId}/{documentId}/v{docVersion}`, overwrite allowed; versioning keeps the earlier version (`[S]` AC4, ASM-TE012-18).
6. `writeOnce = true` → ContentHashGuard (SPEC-012), then upload to the legal container with `If-None-Match: *`.
7. Both uploads set metadata `sha256` and the content type. Errors go through StorageErrorMapper (SPEC-013).
8. Return `StoredBlob`; for a re-store, its `ref` is the new `storage_ref` the caller moves to (`[DL]` D-RCV-31). The source blob is never deleted (ASM-TE012-21). A new version is a new name; earlier blobs are untouched (`[S]` BR2, AC3).

### SPEC-RWB-TE-012-012 — ContentHashGuard

Before a write-once upload: read the existing blob's properties. Not found → proceed. Found → take metadata `sha256`; if absent, download and hash it within the timeout. Equal → `StoredBlob(existing = true)`, no upload. Different → `WriteOnceViolationException` and audit `HASH_MISMATCH`. On `BlobAlreadyExists` from the conditional upload (a concurrent writer, or an earlier upload that completed after a client timeout), compare once more with the same rule. This meets AC12 and X9 and settles the story-defect row (DGAP-14).

### SPEC-RWB-TE-012-013 — StorageErrorMapper

| Input | Output |
|---|---|
| `BlobImmutableDueToPolicy`, or 409 on the legal container after the guard re-check | `WriteOnceViolationException` + audit `STORAGE_REFUSED` |
| `DELETE` refused on the legal container | `WriteOnceViolationException` + audit `STORAGE_REFUSED` |
| Overall timeout exceeded | `StorageUnavailableException(TIMEOUT)`; background probe requested |
| 5xx after retries; connection or I/O failure | `StorageUnavailableException(UNAVAILABLE)`; background probe requested |
| `ContainerNotFound` | `StorageUnavailableException(UNAVAILABLE)` + ERROR log; background probe requested (the probe sets NOT_READY `CONTAINER_MISSING:<name>`) |
| 403 `AuthorizationPermissionMismatch`, `KeyBasedAuthenticationNotPermitted`, `AuthorizationFailure` | `StorageUnavailableException(ACCESS_REFUSED)` + ERROR log (ASM-TE012-15) |
| `BlobNotFound` on `open()` | `StorageUnavailableException(BLOB_MISSING)` (ASM-TE012-15); no probe |
| Any other error code, or a response the SDK cannot parse | Rethrown unchanged |

Rows without "background probe requested" request none. The mapper never writes readiness (SPEC-009). Log lines carry container, blob name, error code and trace ID only.

### SPEC-RWB-TE-012-014 — Audit of refused changes

`DocumentAuditLog` writes `DOCUMENT_CHANGE_REFUSED` (fields above) as one structured line to logger `recovery.audit`, the stand-in for the ACE audit log (`[AUD]`; ASM-TE012-06). Attempts made directly on the container are recorded by the storage platform only if resource logs are on; the document set does not say so (DGAP-11).

### SPEC-RWB-TE-012-015 — BlobStorageAdapter: open

Flag off → `StorageUnavailableException(NOT_READY)`. Accepts a `BlobRef` whose container is the configured standard or legal container; anything else (intake, quarantine, unknown) → `IllegalArgumentException`, no storage call (`[S]` AC11). Downloads with the ACE identity within the timeout. Not gated by readiness, and its outcome never changes readiness; a transport failure or `ContainerNotFound` only requests a background probe (ASM-TE012-13, SPEC-009). `open()` is not an authorization point: its callers own the Documents R right and scope check and the PII access-log entry (Guardrails; `[E1-024]` step 8 and §17).

### SPEC-RWB-TE-012-016 — Baseline evolution

Apply the Evolution map to the code RWB-TE-001 relocated: rename and reshape `dochub.api.DocumentStore` into the SPEC-010 types; rename `dochub.storage.BlobDocumentStore` to `BlobStorageAdapter` and its nested `Config` and `BlobProperties` to `DocumentContainersConfig` and `DocumentStorageProperties`; remove the `rwb.blob` block from `application.yaml` and add `rwb.dochub`; remove `RecoveryDatabaseIT.java:61` (the flag is off by default and every P5 bean has a defined flag-off path, SPEC-008, so the context needs no storage); correct the `build.gradle.kts:60` comment. No baseline class remains beside its successor. The containers `rwb-documents` and `rwb-documents-legal` held no data outside local Azurite volumes; no data migration is needed.

### SPEC-RWB-TE-012-017 — Local emulator mode

Active only when **all** hold: the `local` Spring profile is active (`Environment.acceptsProfiles(Profiles.of("local"))`), `rwb.dochub.storage.emulator=true` (`true` only in `application-local.yaml`; like any property it can be overridden from the environment, which is why it is not the only condition), the emulator connection string is non-blank, its account name is `devstoreaccount1`, and its blob endpoint host is `127.0.0.1`, `localhost` or `azurite`. If `emulator` is true and any other condition fails, startup fails with a message naming the failed condition (the `local` profile, or `RWB_DOCHUB_EMULATOR_CONNECTION_STRING`). `rwb.environment` is not used.

In this mode: one shared-key client for all four containers, quarantine included (Azurite has no managed identity); the service and OCR client IDs are not used, and the readiness identity checks are reported `EMULATED`, so the hub reaches READY with all four containers present and no client ID set (ASM-TE012-31; round 3 finding SG-20). `LocalEmulatorBootstrap` creates the four containers (`createIfNotExists`) as the first part of every SPEC-009 probe, inside the probe deadline. If Azurite is unreachable or a call times out, it logs one WARN line, readiness becomes NOT_READY (`UNREACHABLE`), and startup is neither failed nor delayed; this keeps the baseline property that the service starts while Blob storage is down (baseline `BlobDocumentStore` comment, A-04). The bootstrap runs again in the next probe (ASM-TE012-28). `docker-compose.yml` `depends_on` is not changed, because the backend must not need Azurite to start; `legalPolicy` is `EMULATED` because Azurite has no immutability policy, so write-once is the conditional upload plus ContentHashGuard. This is the local deviation the README "Local versus target" Blob row already records ("Azurite with a conditional write for legal documents"). The README "Decisions taken" row for it (`shared-updates.md` §5) is a **plan-gate item**: it is approved at the plan gate and committed before or with the first code commit. The published Azurite development key is the only key allowed, and only in `.env` / `.env.example`.

### SPEC-RWB-TE-012-018 — Tests

All unit tests run in the `test` task (JUnit 5, Mockito, Spring `ApplicationContextRunner`; no Docker, database or external network) and count toward SPEC-023. Test data: random UUIDs and generated bytes only.

| ID | Test | Proves |
|---|---|---|
| T-TE012-01 | `DocumentStoragePropertiesTest` | Binding and defaults (timeout 10, `readiness-recheck-seconds` 30, four names, flag false, emulator false); every startup-failure rule of the properties table; flag off needs no URL |
| T-TE012-02 | `DocumentContainersConfigTest` | Flag off: no `BlobServiceClient` bean; `DocumentStorage` and `DocumentContainers` beans present; each `DocumentContainers` accessor throws `StorageUnavailableException(NOT_READY)` and `readiness()` returns `ready=false`, `FLAG_OFF`. Flag on: two clients; each credential chain holds only workload and managed identity types with the configured client ID; no create call. Emulator guard: each of the five conditions false in turn (`local` profile, `emulator` property, non-blank string, `devstoreaccount1`, host) → startup fails (or, for `emulator=false`, emulator mode stays off); all true → one shared-key client |
| T-TE012-03 | `BlobRefTest` | `storageRef()`; `fromStorageRef` round trip for a document name and an intake name; refused inputs (null, blank, no `/`, bad container, over 400 characters); document name format and length bound |
| T-TE012-04 | `BlobStorageAdapterStoreTest` (mocked `BlobContainerClient` / `BlobClient`) | Success: download from intake, SHA-256 and size, upload to standard when `writeOnce=false`, to legal with `If-None-Match: *` when true, metadata `sha256` and content type, `existing=false`, source not deleted. D-RCV-31 re-store: standard source at the same name with `writeOnce=true` → legal blob at that name, standard object untouched. Refused with `IllegalArgumentException` and zero interactions: standard source with `writeOnce=false`; standard source with a different name; legal, quarantine and unknown source containers. Flag off → NOT_READY with zero storage interactions. Probe result NOT_READY → NOT_READY with no download or upload |
| T-TE012-05 | `ContentHashGuardTest` | Same hash → existing, no upload; different → violation + audit `HASH_MISMATCH`; metadata absent → downloaded and hashed; `BlobAlreadyExists` → one re-compare; client-timeout-then-retry sequence (first store times out after the server stored the blob; the second store with the same source returns `existing=true`, no exception) |
| T-TE012-06 | `StorageErrorMapperTest` | Each row of SPEC-013, including an unexpected error code and an unparsable response rethrown unchanged; `TIMEOUT`, 5xx/I/O and `ContainerNotFound` request exactly one background probe; `BlobNotFound`, 403 and other 4xx request none; the mapper never writes readiness (indicator state unchanged in every row) |
| T-TE012-07 | `BlobStorageAdapterOpenTest` | Standard and legal refs read; intake, quarantine and unknown containers → `IllegalArgumentException` with zero interactions; `BlobNotFound` → `BLOB_MISSING`; flag off → NOT_READY |
| T-TE012-08 | `StorageReadinessIndicatorTest` | Each reason; flag off → `UNKNOWN`, `ready=false`, `FLAG_OFF`, no storage call; NOT_EVALUATED → `UNKNOWN`; READY → `UP`; NOT_READY → `DOWN`; start evaluation runs once off the calling thread; a health read after start makes zero storage calls; details hold no URL or client ID |
| T-TE012-09 | `DocumentHealthAggregateTest` | With Spring Boot's default `SimpleStatusAggregator` and `SimpleHttpCodeStatusMapper` and one other component `UP`: flag off → root `UP`, HTTP 200; NOT_READY → root `DOWN`, HTTP 503; the `liveness` and `readiness` groups do not contain `documentHub`. Runner: default profile, emulator off; `ApplicationContextRunner` with `ConfigDataApplicationContextInitializer` (loads `application.yaml` only), the health endpoint auto-configuration, `DocumentStorageProperties` (so its startup rules run) and `StorageReadinessIndicator` with a stub `ReadinessProbe`; no Blob client is built. Flag-on cases set `rwb.dochub.storage.account-url=https://rwbconformance.blob.core.windows.net` explicitly (synthetic; never called) |
| T-TE012-10 | `DocumentAuditLogTest` (Logback `ListAppender`) | One line on logger `recovery.audit` with every field; `actorId` present with an authenticated principal and absent without one; no content bytes, account URL or client ID in the line |
| T-TE012-11 | `LocalEmulatorBootstrapTest` (emulator-mode runner, see "How tests set the profile and the emulator string"; mocked `BlobServiceClient`) | Emulator mode: `createIfNotExists` for each of the four names; legal policy `EMULATED`; with all four containers present and **no** service or OCR client ID set → READY, identity checks `EMULATED`, quarantine served by the shared-key client. Unreachable emulator (mock throws, or a closed 127.0.0.1 port): one WARN line, readiness NOT_READY `UNREACHABLE`, no exception out of startup; after `readiness-recheck-seconds` (set to 1) a `store()` probe re-runs the bootstrap and proceeds when it succeeds. Not emulator mode: bean absent |
| T-TE012-12 | `BlobStorageAdapterHttpStubTest` (JDK `HttpServer` on 127.0.0.1 on a free port, emulator-mode runner with the string pointing at that port, `timeout-seconds=1`; the stub does not check signatures) | Integration-client cases: success (201) → `StoredBlob`; no answer → `TIMEOUT` within 1 s plus a bound; 503 then no answer → SDK retries end inside the overall timeout (elapsed ≤ timeout plus a bound); 400 with an unexpected error code → rethrown unchanged; malformed error body → rethrown unchanged |
| T-TE012-13 | `LocalProfileStartupTest` (`ApplicationContextRunner` with `ConfigDataApplicationContextInitializer`, profile `local`, P5 configuration only) | With `rwb.dochub.storage.emulator-connection-string` set to a `devstoreaccount1` string on 127.0.0.1 → context starts in emulator mode; with the property set explicitly to blank (not relying on the variable being absent, because `dev.ps1` imports `.env` into the Gradle process) → startup fails naming `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` |
| T-TE012-14 | Carried RWB-TE-001 SPEC-024 tests (moved into the classes above) | Successors: standard put → T-TE012-04 standard routing; legal put → T-TE012-04 legal routing; legal overwrite refused → T-TE012-05 different hash; get present → T-TE012-07 standard read; get absent → T-TE012-07 `BlobNotFound` → `BLOB_MISSING` (behaviour changed by the published-surface change, Evolution map) |
| T-TE012-15 | `StorageTemplateConformanceTest` (backend `src/test/java/th/co/scb/ace/demo/recovery/dochub/storage/`; reads `../infra/azure/document-storage/` relative to `backend/`, as `RecoveryDatabaseIT` reads `../infra/postgres`) | Unit test, Jackson only; needs no undecided value. Template `azuredeploy.json` against the schema list and `azuredeploy.local.parameters.json`: `allowSharedKeyAccess` false, `publicNetworkAccess` Disabled, `minimumTlsVersion` TLS1_2; a `Microsoft.Network/privateEndpoints` resource whose connection targets the storage account with `groupIds` [`blob`] and whose subnet is `privateEndpointSubnetId`; four containers with `publicAccess` None; versioning on; soft delete days = `softDeleteDays`; an `immutabilityPolicies` resource on the legal container with `immutabilityPeriodSinceCreationInDays` = `legalRetentionDays`, `allowProtectedAppendWrites` false and `condition` `[parameters('deployLegalPolicy')]`; **no** lock parameter or property; six container-scope role assignments and no account-scope data role. Required inputs: the template parameters without `defaultValue` are exactly the schema list (private endpoint subnet included); the local file gives each a shape-valid value. Environment files: each of the four names every schema input with a shape-valid value or exactly `__SET_BEFORE_APPLY__`; `deployLegalPolicy` is `false` in PROD and `true` in DEV, SIT and UAT. Placeholder values are the pre-deploy check's job (SPEC-001), not this test's |
| T-TE012-16 | Existing `RecoveryBoundaryTest`, `ModulithTest`, T-TE001-14 | Pass under the RWB-TE-001 module map with no rule changed; T-TE001-14's expected `dochub.api` list updated per SPEC-022 in the same merge request |
| T-TE012-17 | `StorageReadinessProbeTest` (unit; mocked container clients that block, with `timeout-seconds=1`, `readiness-recheck-seconds` 1 or 30; a controllable clock) | Outage at start: start probe ends NOT_READY `UNREACHABLE` within 1 s plus a 1 s bound. **Single-flight:** 20 concurrent `store()` calls with a stale NOT_READY state and storage not answering → exactly one probe (four property calls counted), and each call raises `StorageUnavailableException(TIMEOUT)` or `(NOT_READY)` within 1 s plus a 1 s bound of its own entry. `store()` while the start probe runs (NOT_EVALUATED) → joins it; no second probe. Fresh NOT_READY (younger than `readiness-recheck-seconds`) → `NOT_READY` at once with zero storage calls. Emulator mode: bootstrap creates and checks finish inside one deadline. READY, with the last probe ended more than `readiness-recheck-seconds` before on the controllable clock, then a `store()` ending in `TIMEOUT` → the `store()` raises `TIMEOUT`, exactly one background probe is requested, and the state stays READY until that probe ends NOT_READY `UNREACHABLE`; the next `store()` within the window → `NOT_READY` with zero calls. A probe that ends READY lets the waiting callers proceed. `ApplicationReadyEvent` while a `store()`-started probe runs → joins it; no second probe. **Suppression:** READY with a probe ended less than `readiness-recheck-seconds` before, then an `open()` ending in transport `UNAVAILABLE` → no probe requested, state READY; after the clock passes the window, the next failing operation → exactly one probe, which ends NOT_READY. A background probe that ends with all checks passing → READY with `checkedAt` updated |
| T-TE012-18 | `ReadinessIsolationTest` (unit; mocked container clients; indicator with Spring Boot's default status aggregator and HTTP code mapper, one other component `UP`) | State READY: `open()` of a missing blob → `BLOB_MISSING`; `documentHub` stays `UP`, readiness and `checkedAt` unchanged, root HTTP 200, zero probes. The same for `ACCESS_REFUSED`, a write-once refusal and a 409 conflict. Probe failure (container properties answer 503 after retries) → NOT_READY `UNREACHABLE`, `documentHub` `DOWN`, root HTTP 503. Probe finds a container missing → NOT_READY `CONTAINER_MISSING:<name>`, root 503 |

**How tests set the profile and the emulator string** (round 3 finding SG-21). No test relies on `.env`, on `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` or on `dev.ps1`, and no key is committed in test code:

| Tests | Profile | Properties set explicitly | Connection string |
|---|---|---|---|
| T-TE012-01 to -08, -10, -14, -17, -18 (non-emulator) | none (default) | `rwb.dochub.storage-containers` as each case needs; mocked clients | none |
| T-TE012-09 | default; `ConfigDataApplicationContextInitializer` loads `application.yaml` | `rwb.dochub.storage-containers` as each case needs, `rwb.dochub.storage.emulator=false`; flag-on cases also `rwb.dochub.storage.account-url=https://rwbconformance.blob.core.windows.net` | none |
| T-TE012-02 (guard), -11, -12, -13, -17 (emulator cases): the "emulator-mode runner" | `local`, set by an initializer `ctx -> ctx.getEnvironment().setActiveProfiles("local")` on an `ApplicationContextRunner` that holds the P5 configuration classes only; T-TE012-13 also adds `ConfigDataApplicationContextInitializer` to load `application-local.yaml` | `rwb.dochub.storage-containers=true`, `rwb.dochub.storage.emulator=true`, `rwb.dochub.storage.emulator-connection-string=<built>`; T-TE012-13 overrides the string to blank for its failure case | Built in the test at run time: `DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=<random 64-byte Base64 generated per run>;BlobEndpoint=http://127.0.0.1:<port>/devstoreaccount1`. Mocks and the JDK stub do not check signatures |
| Azurite integration tests | `local` via the same initializer, on a P5-only `ApplicationContextRunner` (no database, Temporal or Drools beans, so `rwb.p3.*` is not involved) | as above | Azurite is started with `AZURITE_ACCOUNTS=devstoreaccount1:<random Base64 key generated per run>`, and the string is built from that key, `container.getHost()` and `getMappedPort(10000)`. The test asserts the host is loopback (`dev.ps1 it` runs local Docker) and fails with a clear message otherwise |

**Integration tests** (`@Tag("recovery-it")`, `recoveryIntegrationTest`, run by `./scripts/dev.ps1 it`): Testcontainers `GenericContainer` with `mcr.microsoft.com/azure-storage/azurite:3.37.0` started with `--skipApiVersionCheck` (as `docker-compose.yml`; SDK 12.37.2 sends a newer service version). Cases: READY with no client IDs set; naming; copy from intake; standard overwrite; write-once conditional upload; guard AC12 both branches; readiness `CONTAINER_MISSING` when a container is absent; `open` refusal of quarantine. `RecoveryDatabaseIT` passes without line 61. These are **required implementation evidence for this story's merge**: the story edits an integration test and adds Azurite tests, which is beyond D-RCV-44's floor (migrations and `RecoveryFlywayConfig`) but uses the same mechanism (ASM-TE012-23). They are not counted in coverage (`[TE001]` SPEC-020 (c)).

**Builder evidence (not automated):** `.env` upgrade (SPEC-021): with a `.env` that lacks the two new keys, run `./scripts/dev.ps1 test`; afterwards `.env` contains both keys with the `.env.example` values and every earlier line unchanged.

**System tests in SIT** (`[TC]` TC-TE-012-01 to -12): against the real account; `PENDING_ENVIRONMENT` until the template is applied in SIT. AC1's storage clause uses a raw client with the ACE identity (DGAP-15).

No new dependency: Testcontainers core, Mockito, Logback and the JDK `HttpServer` are already present.

### SPEC-RWB-TE-012-019 — Seams to later stories (D-RUN-08)

Later stories in Build Sequence v6 conform to this contract; this story conforms to what they state.

| Seam | Owner (order) | What this story provides; what the owner does |
|---|---|---|
| `DocumentStore` interface, `StoreRequest`, `StoredDocument`, document row, type-to-`writeOnce` choice, `replaceContent` → 409 MSG-P5-002, `StorageUnavailableException` → 503 MSG-GEN-006 | RWB-E1-024 (42) | Provides `DocumentStorage.store(BlobWriteRequest)` copying from the intake `BlobRef` E1-024 receives (`StoreRequest.intakeBlobRef`) to `{container}/{caseId}/{documentId}/v{docVersion}`, and `BlobRef.fromStorageRef` for its `storage_ref`. E1-024 owns its `dochub.store` package and its own map entries |
| AC9 "no document row" | RWB-E1-024 (42) | E1-024 calls `readiness()` before inserting the row (DGAP-17; open item) |
| COPY_PENDING retry (X8, JOB-12) | RWB-E1-024 (42) | A retried store after a client timeout returns `existing=true` (SPEC-012) |
| Clean-up of the intake blob after store | RWB-E1-024 / RWB-E1-041 | `store()` never deletes the source |
| Intake writes: upload service, IntakeService | RWB-E1-026 (58), RWB-E1-057 (61) | `DocumentContainers.intake()` in `dochub.storage` (throws NOT_READY when the flag is off, SPEC-008). Their packages `dochub.casedocs` and `dochub.intake` use Azure types only if added to the P5 `clientPackages` by that story (D-RCV-41), or by placing that code under `dochub.storage` |
| QuarantineMover, scan | RWB-E1-041 (54) | `DocumentContainers.quarantine()` (SY-OCR identity); same BND-5 rule for `dochub.scan` |
| OCR read of a `BlobRef` | RWB-E1-049 (49) | `BlobRef`; `open()` refuses intake, so OCR of intake files reads through `DocumentContainers` under the same BND-5 rule |
| Legal re-store after type confirmation | RWB-E1-032 (63), RWB-E1-054 (70) confirm flow | `store()` with `writeOnce=true`, the same `docVersion`, and `source` = the document's current standard-container `BlobRef` (`[DL]` D-RCV-31: re-store at `{caseId}/{documentId}/v{docVersion}`, "moves storage_ref", standard object kept). The caller moves `storage_ref` to the returned ref and writes the DOCATT entry. `[E1-054]` v1 has no step that re-stores a stored document (its type change is for intake items only); DGAP-23 and an open item to the solution architect with the analyst, needed by RWB-E1-032 and RWB-E1-054 specify |
| Write-once archive container for retention (`retention/YYYY-MM-DD/<table>/`) | RWB-E1-017 (17) | Not delivered: `[S]` §4 defines four containers and AC5 limits each identity to its named containers; `[E1-017]` §3 expects an archive container "writable by SY-DATALOAD", an actor `[URP]` marks retired under D-RCV-35 (U1). A P1 writer would also need a `dochub.api` operation (D-RCV-31 single write path); `DocumentContainers` is confined to P5. DGAP-22; open item to the solution architect with Compliance |
| Upload endpoint and TC-TE-012-13 | RWB-E1-026 (58) | — |
| Read access check and PII access log for `open()` | RWB-E1-024 (endpoints); ACE common module per `[E1-024]` §17 | `open()` performs neither |
| SCR-44 display of readiness | No owner story (DGAP-20); `[SCR]` release "E2; E8 full" | `documentHub` component and `readiness()` (SPEC-020) |

### SPEC-RWB-TE-012-020 — Health component and the root health status

- `StorageReadinessIndicator` is a Spring Boot health indicator registered as `documentHub` under the existing `/actuator/health` (`[S]` §13 "joins the ACE health endpoint"; `[BN]` step 7 "published through the ACE health endpoint").
- **Flag off:** status `UNKNOWN`, details `ready=false`, `reasons=[FLAG_OFF]`. Story §13 requires "not ready" when off; `ready=false` and `readiness()` state it. `UNKNOWN` leaves the root aggregate as before this story: Spring Boot's default order (DOWN, OUT_OF_SERVICE, UP, UNKNOWN) makes the root `UP` when the other components are `UP`, and HTTP stays 200. Source for leaving the root unchanged: `[AGENTS]` §3.13 (flag off returns the previous code path; before this story the root had no such component). No document defines how a module's health affects the ACE root status (DGAP-21).
- **Flag on:** READY → `UP`; NOT_READY → `DOWN`, so the root turns `DOWN` and `/actuator/health` answers 503. This is the "not ready" signal of `[S]` §4 step 3 and AC9 on the ACE health endpoint. `./scripts/dev.ps1 status` then prints its existing "Backend not reachable" line, because `Invoke-RestMethod` throws on 503; this story does not change that command.
- Not in the `liveness` or `readiness` probe groups (ASM-TE012-09), so a NOT_READY hub keeps the pod in service and uploads answer 503 MSG-GEN-006 as AC9 requires.
- A health read, anonymous or authorized, makes no storage call (SPEC-009). Details only for RW-PLATADM.

### SPEC-RWB-TE-012-021 — Local stack and existing `.env` files

| Node | Change |
|---|---|
| `.env.example:23` | `RWB_BLOB_CONNECTION_STRING` → `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` (same value, loopback host) |
| `.env.example:24` | `RWB_BLOB_CONNECTION_STRING_DOCKER` → `RWB_DOCHUB_EMULATOR_CONNECTION_STRING_DOCKER` (same value, `azurite` host) |
| `docker-compose.yml:135` | `RWB_DOCHUB_EMULATOR_CONNECTION_STRING: ${RWB_DOCHUB_EMULATOR_CONNECTION_STRING_DOCKER}` |
| `scripts/dev.ps1` `Initialize-EnvFile` | After the existing copy-when-absent step: for each `KEY=` line in `.env.example` whose key is absent from `.env`, append that line to `.env` and print "Added <KEY> to .env from .env.example". Existing lines are never changed or removed; the codec-key step is unchanged. Every `dev.ps1` command calls `Initialize-EnvFile`, so `up`, `backend` and `it` all heal an old `.env` (ASM-TE012-22) |
| `application-local.yaml` | Flag `true`, `emulator: true`, `emulator-connection-string: ${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}` |
| `README.md:25` | Builder edit (`shared-updates.md` §5): the `documents/` line becomes the P5 `dochub/` line |

RWB-TE-001 lists `scripts/dev.ps1` as unchanged by RWB-TE-001; this story changes it and lists it here as an impacted node. Old `RWB_BLOB_*` lines left in an existing `.env` are unused and harmless.

### SPEC-RWB-TE-012-022 — Published surface and boundary tests

- After this story the public types in `dochub.api` are exactly: `DocumentStorage`, `BlobRef`, `BlobWriteRequest`, `StoredBlob`, `StorageReadiness`, `WriteOnceViolationException`, `StorageUnavailableException` (+ nested `Reason`). T-TE001-14's expected `dochub.api` list (`[TE001]` SPEC-025: "`DocumentStore` (+ its nested records and exception)") is replaced by this list in the same merge request. This is a change of the published surface that the test records, not a weakened test.
- Every class that uses `com.azure.storage` is in `dochub.storage`, so BND-5 passes unchanged. `dochub` gains no dependency on another module, so `ModulithTest` passes unchanged. No map change.
- The RWB-TE-001 SPEC-024 tests move to their successors (T-TE012-14); none is deleted without one.

### SPEC-RWB-TE-012-023 — Coverage gate for this story

- Metrics, scope and task as `[TE001]` SPEC-020: LINE, INSTRUCTION, BRANCH, METHOD at 0.80, bundle over all main `recovery/**` classes plus the tooling classes, no exclusion, execution data from `test` only. This story adds no exclusion; none is allowed without a cited source.
- Command: the Builder runs `./gradlew test recoveryCoverageVerification` in `backend/` and saves the XML and HTML reports as implementation evidence. It is outside `check` (D-RCV-28 (3), D-RCV-40) and `./scripts/dev.ps1 test` does not run it; CI wiring is audit item A-09, owned by RWB-TE-003/RWB-TE-011.
- The package reaches the gate through RWB-TE-001 (precondition; `[TE001]` SPEC-024 lifts the measured 32% line baseline). This story keeps it there: from the report, every main class under `recovery/dochub/**` is at or above 80% on the four counters (T-TE012-01 to -13, -17 and -18 are the tests that cover them), and no bundle counter is below its value on `develop-recovery` before the merge (`[TS]` §6 "changed code first"; a global drop blocks the merge).
- D-RCV-06 names line and branch only; `[TE001]` SPEC-020 adds INSTRUCTION and METHOD and is applied here (later and more specific; not a new gap).

## Security, privacy and performance

- No key, connection string or SAS outside local emulator mode (`[S]` §17; `[SEC]`).
- Blob names and logs carry UUIDs only (`[PDPA]` §1; ASM-TE012-07).
- Region: `[PDPA]` §8, bank position to confirm (DGAP-13).
- Timeout 10 s per call (`[S]` §13); `backend-context.md` §8 says 30 s for external calls; the story value applies (DGAP-08).
- Health reads are cheap: no storage call, so the anonymous `/actuator/health/**` path cannot drive storage traffic.

## Guardrails and out of scope

Guardrails (`[S]` §17): no business value in code; no personal data in logs, tests or prompts; no read of another module's tables; no account key, connection string or SAS in code, configuration or pipeline (local Azurite key only, SPEC-017). **`open()` is not an authorization point:** every caller owns the Documents R right and scope check and the PII access-log entry (`[E1-024]` step 8 and §17 place the log in the ACE common module; RWB-E1-039 owns the PII access log).

Out of scope (`[S]` §19): container choice per type and the document row (E1-024); retention classes, archive and JOB-17 (E1-041); legal hold (REQ-DCM-016, DL27); backup and restore test (REQ-DCM-015, DL27); sizing and cost (REQ-DCM-014, NFR-069); the SCR-44 screen.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | `[S]` §12, §4 step 4; `[DL]` D-RCV-31; `[E1-024]` §13 | Who publishes the write path | Interface ownership | Precedence: Decision Log v10 over story v7. TE-012 publishes `DocumentStorage` (DGAP-01) | RESOLVED | SPEC-010 |
| CLAR-002 | `[S]` §12; `[TE001]` SPEC-009 | `DocumentContainers` returns Azure types but is called "published" | Boundary | Stays in `dochub.storage` as `[S]` §13 says; usable inside P5 under BND-5 and D-RCV-41 (DGAP-02) | RESOLVED | SPEC-008 |
| CLAR-003 | `[S]` BR6 | Versioning and soft delete are account-wide | Applies to all four containers | Account scope; early DEV spike (DGAP-03) | RESOLVED | SPEC-003 |
| CLAR-004 | `[S]` §3, BR1; `[RET]` §1 | 3,650 days vs "10 years after the case closes" | Policy is a floor | Parameter 3650; full retention in E1-041 (DGAP-04) | RESOLVED | SPEC-004 |
| CLAR-005 | `[RET]`; `[ADR]`; `[NFR]`; `[PDPA]` | Tier, key type, redundancy, region not set | Template values | Required parameters or platform default (DGAP-05, -06, -07, -13) | RESOLVED | SPEC-001 |
| CLAR-006 | `[S]` X9 vs AC12 | Order of storage refusal and hash check | Repeated write | Hash first, conditional upload, re-check on race | RESOLVED | SPEC-012 |
| CLAR-007 | `[S]` AC5, AC11; `[E1-041]` | Quarantine readable only by SY-OCR | Second identity | Configured SY-OCR client ID (DGAP-10, ASM-TE012-05) | RESOLVED | SPEC-007, -009 |
| CLAR-008 | `[S]` AC1, X1; `[AUD]` | Audit sink; direct attempts | Audit | Structured audit logger; resource logs gap (DGAP-11) | RESOLVED | SPEC-014 |
| CLAR-009 | `[S]` AC examples; `[API]`; `[SCH]` | Case number or UUID in names | Name and PDPA | UUIDs (DGAP-16) | RESOLVED | SPEC-010 |
| CLAR-010 | `[S]` §13; `[ENV]` §4 | Template format and location | Template file | ARM JSON template and JSON parameter files in `infra/azure/document-storage/` (DGAP-09; reason cited in SPEC-001) | RESOLVED | SPEC-001 to -005, T-TE012-15 |
| CLAR-011 | `[S]` AC9; `[E1-024]` flow | Row written before storage call vs "no document row" | AC9 last clause | E1-024 checks `readiness()` first; open item (DGAP-17) | RESOLVED | SPEC-019 |
| CLAR-012 | README "Local versus target" | Azurite has no managed identity or immutability | Local runs | Emulator mode behind `rwb.dochub.storage.emulator` (ASM-TE012-11) | RESOLVED | SPEC-017 |
| CLAR-013 | `[TE001]` SPEC-022; `[S]` §13 | Module and package placement | All packages | `dochub.api` and `dochub.storage` per RWB-TE-001 v4; DGAP-18 withdrawn | RESOLVED | SPEC-016, -022 |
| CLAR-014 | `[E1-024]` §12, steps 1, 7; `[DL]` D-RCV-31 | `DocumentStorage` signature and the intake-to-store path | Contract | Copy from an intake `BlobRef`; `BlobWriteRequest`; `BlobRef.fromStorageRef` (DGAP-19) | RESOLVED | SPEC-010, -011 |
| CLAR-015 | `[S]` §13 flag, §4 step 3; `[AGENTS]` §3.13 | Effect of `documentHub` on the root health status | HTTP 200/503 of `/actuator/health` | Flag off `UNKNOWN`; flag on `UP`/`DOWN`; no storage call on reads (DGAP-21) | RESOLVED | SPEC-009, -020 |
| CLAR-016 | `[SCR]`; `[E1-056]` §15, §19; `[BSEQ]` | Owner of SCR-44 | Readiness display | No owner story; open item (DGAP-20) | RESOLVED (seam) | SPEC-019 |
| CLAR-017 | `[TE001]` SPEC-020; `[TS]` §6; D-RCV-06 | Coverage scope and metrics | Merge evidence | Four counters, bundle, per-class for `dochub`, no drop | RESOLVED | SPEC-023 |
| CLAR-018 | `[E1-017]` §3, BR4; `[S]` §4, AC5; D-RCV-35; D-RCV-31 | E1-017 expects an archive container from TE-012 | Container set | Not delivered; seam and open item (DGAP-22) | RESOLVED (seam) | SPEC-019 |
| CLAR-019 | `[DL]` D-RCV-31; `[E1-032]` BR4, AC10 | Re-store source is the standard container, not intake | `store()` source rule | Standard source allowed with `writeOnce=true` and the same name | RESOLVED | SPEC-010, -011 |
| CLAR-020 | `[S]` AC10, X7; `[S]` §4 step 3 | Store while the hub is not READY must still end within 10 s | `store()` readiness path | Single-flight probe with a `timeout-seconds` deadline; NOT_READY reused for `readiness-recheck-seconds` (ASM-TE012-30) | RESOLVED | SPEC-009, -011, T-TE012-17 |
| CLAR-021 | `[S]` BR1, §13 (`legalPolicyLocked`); `[ENV]` §4.2 | PROD lock cannot be a template parameter | PROD lock | Runbook step outside the template with owner, approver and evidence (DGAP-24) | RESOLVED | SPEC-004 |
| CLAR-022 | `[DL]` D-RCV-31; `[E1-032]` step 6, BR4; `[E1-054]` steps 4, 7, 9 | No owner step for re-storing a stored document | Re-store caller | Contract provided; caller step open (DGAP-23) | RESOLVED (seam) | SPEC-019 |
| CLAR-023 | `[S]` §13; SPEC-017 | Emulator mode readiness without client IDs | Local READY | Identity checks `EMULATED` in emulator mode (ASM-TE012-31) | RESOLVED | SPEC-009, -017 |
| CLAR-024 | `[S]` AC9, AC10, X6, X7; SPEC-013 | Which outcomes may change readiness | Health and fail-fast | Only the probe writes readiness; transport failures and `ContainerNotFound` request a background probe; `BLOB_MISSING` and other per-operation outcomes never touch it | RESOLVED | SPEC-009, -013, T-TE012-18 |
| CLAR-025 | `[S]` §13 "Done when"; DGAP-05, -07, -13 | Template inputs not yet decided | Parameter files | Schema list and local file for the unit test; placeholders plus a pre-deploy check; open item per value (ASM-TE012-32) | RESOLVED | SPEC-001, T-TE012-15 |
| CLAR-026 | `[S]` BR1; `[AZ-IMM]`; `[AZ-REST]` | Later PROD applies after the lock | PROD template | Policy resource conditional; PROD file `false`; period change only by the runbook extend step (ASM-TE012-33) | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — 26 items resolved by precedence, the story's defaults, RWB-TE-001 v4, or labelled assumptions. No question was asked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Jira, Confluence, GitLab or Figma MCP connected (RUN-BRIEF rule 5); no UI in scope.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Storage template, managed-identity clients, readiness and health, and the published DocumentStorage write path in dochub; evolves the relocated baseline DocumentStore/BlobDocumentStore in place; no endpoint, screen or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: enabler with no endpoint of its own, story §12]
REQUIREMENT_COVERAGE_SUMMARY: 7 BRs, 12 ACs, 7 flow steps, 10 exception paths, flag, guardrails, D-RCV-31, FR/REQ/NFR/CTL IDs, the RWB-TE-001 obligations and the D-RCV-31 re-store mapped in 37 rows. The RWB-E1-017 expectation is a seam (SPEC-019, DGAP-22), not a coverage row.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 37] [COVERED_RULES: 37] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_GATE_RESULT: PENDING — review/spec-gate-review-7.md (round 6: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2], answered in gate-response.md Round 6)
NEXT_STEP: Spec gate round 7 (Compliance Reviewer).
```

Contradictions between sources are recorded in `document-gaps.md` and settled there by precedence; `CONTRADICTIONS` counts only those left unresolved in this spec, which is none.
