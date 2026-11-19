# Technical Specification — RWB-TE-012 Document storage containers

| Field | Value |
|---|---|
| Story | RWB-TE-012 — Document storage containers (Enabler, Must) |
| Epic / module | E1 / P5 Document hub. Code module `th.co.scb.ace.demo.recovery.documents` (TE-001 baseline) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Source requirement | Story file RWB-TE-012 v1, 28 Oct 2026, in Epic 1 story files v7 (`[S]` below); increment card `docs/increments/INC-007-epic-1-RWB-TE-012.md` |
| Upstream IDs | REQ-DCM-003, REQ-DCM-002 (BRD Program v4 §5.5); `BR-RWB-007` / `FR-RWB-007` (Traceability Matrix row 007); CTL-12, CTL-09; NFR-029; DL26, DL27; D-RCV-31 |
| Build order | 7 of 72 (Build Sequence v6). Depends on RWB-TE-001 (done). Consumed by RWB-E1-024, RWB-E1-041, RWB-E1-057, RWB-E1-032 |
| Status | `BLOCKED` — spec gate FAIL (1 High, 5 Medium, 5 Low) in `review/spec-gate-review.md`; re-issue and re-review required |
| Prepared | 2026-11-17, Technical Specifier (agent run). No question asked (L-RCV-03) |

## Sources cited

All paths are under `requirement/legacy/` in the document set (read only). Short names are used in the text.

| Short name | Document, version | Path |
|---|---|---|
| `[S]` | RWB-TE-012 story file v1 (Epic 1 story files v7) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md` |
| `[E1-024]` | RWB-E1-024 Document store and index v1 (story files v7) | same folder, `rwb-e1-024-document-store-and-index-v1.md` |
| `[E1-041]` / `[E1-057]` | RWB-E1-041 v1, RWB-E1-057 v1 (story files v7) | same folder |
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
| `[URP]` | Users, Roles and Permissions v4 | `02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` |
| `[CTL]` | Controls Catalog v3 | `10-policy-controls-and-compliance/recovery-workbench-controls-catalog-v3-xlsx.md` |
| `[SCH]` | Physical Schema v6 | `06-data/recovery-workbench-physical-schema-v6.sql` |
| `[API]` | API Specification v4 | `05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| `[TC]` | Test Cases v7 | `09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |

Workspace and code evidence: `backend-context.md` §2 (BND-5), §8; `RecoveryBoundaryTest`; `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-04); README "Decisions taken while setting this up" items 3, 5, 6; `aisdlc/docs/increments/story-defects.md` (RWB-TE-012 row, step 5).

## Baseline: what exists, what this story adds, what it corrects

What exists (verified in code, 17 Nov 2026; audit A-04):

| Item | Today | Evidence |
|---|---|---|
| Published interface | `documents.api.DocumentStore` (`put`, `get`, `StoredDocument`, `DocumentImmutableException`) | `backend/src/main/java/.../documents/api/DocumentStore.java` |
| Adapter | `documents.internal.BlobDocumentStore`; two containers; blob name = document UUID; `If-None-Match: *` on legal writes; `createIfNotExists()` on first write; `DefaultAzureCredential` (full chain) or connection string; no timeout, readiness or audit | `.../documents/internal/BlobDocumentStore.java` |
| Properties | `rwb.blob.connection-string`, `endpoint`, `document-container: rwb-documents`, `legal-container: rwb-documents-legal` | `backend/src/main/resources/application.yaml` |
| Callers | None (no class uses `DocumentStore`) | grep, 17 Nov 2026 |
| Tests | None for the adapter. `RecoveryDatabaseIT` sets `rwb.blob.connection-string=UseDevelopmentStorage=true` | `backend/src/test/...` |
| Local stack | Azurite 3.37.0 on port 10000 (`docker-compose.yml`); README "Local versus target": conditional write locally, immutability policy and managed identity in target | README |
| SDK | Azure Blob SDK 12.37.2, azure-identity 1.19.0, used directly (README decision 3) | `backend/build.gradle.kts` |
| Boundary | `RecoveryBoundaryTest.blobClientOnlyInDocumentsModule`: only `documents.internal..` may depend on `com.azure.storage..` (BND-5) | `backend/src/test/...` |

This story **adds**: the storage infrastructure template (SPEC-001 to -005), the `rwb.dochub.*` properties and flag (SPEC-006), managed-identity-only clients with a 10 s timeout (SPEC-007), the container set and readiness (SPEC-008, -009), the `DocumentStorage` published interface with naming, guard, error mapping, audit and read rules (SPEC-010 to -015), and local emulator support (SPEC-017).

This story **corrects** in the baseline (SPEC-016):

| Baseline | Corrected to | Reason |
|---|---|---|
| Containers `rwb-documents`, `rwb-documents-legal` | `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` | `[S]` §4 step 1; `[DL]` D-RCV-31 names `rwb-docs-legal`; `[FSD-P5]` names `rwb-docs`. The baseline names appear in no document |
| `rwb.blob.*` | `rwb.dochub.*` | `[S]` §13 "Configuration and reference data" |
| Blob name = document UUID | `{caseId}/{documentId}/v{docVersion}` | `[S]` §4 step 4, §11 DF-DOC-006; `[DL]` D-RCV-31 |
| `createIfNotExists()` at first write | Never created by the service outside local emulator mode | `[S]` BR5: not ready unless the containers and policy exist. A runtime create would make `rwb-docs-legal` without a policy |
| `DefaultAzureCredential` full chain | Managed identity credentials only | `[S]` §13 DocumentContainersConfig, BR3 |
| No timeout | 10 s per call, retries included | `[S]` §13, AC10 |
| `DocumentStore` / `BlobDocumentStore` / `DocumentImmutableException` | `DocumentStorage` / `BlobStorageAdapter` / `WriteOnceViolationException` | `[DL]` D-RCV-31 names "DocumentStorage" as the TE-012 interface; `[E1-024]` §12 uses the name `DocumentStore` for its own interface, so the baseline name is freed (zero callers) |
| `build.gradle.kts` comment naming "DocumentStorageConfig" | Names the real config class | Accuracy |

Kept: the `If-None-Match: *` condition on write-once uploads, as a second guard behind the immutability policy (README "Local versus target").

## Assumptions

Full list with basis and effect in `assumptions.md` (`ASM-TE012-01` to `-19`). The ones that shape behaviour:

| ID | Assumption (short) |
|---|---|
| ASM-TE012-01 | Write-once period 3,650 days from blob creation, a template parameter, until DL26 (`[S]` §3, BR1) |
| ASM-TE012-02 | Soft delete 30 days, a template parameter, until DL27 (`[S]` BR6) |
| ASM-TE012-03 | Template written as Azure Bicep with one parameter file per environment, in `infra/azure/document-storage/` as the stand-in for the ACE infrastructure folder |
| ASM-TE012-05 | The service process can obtain the SY-OCR managed identity by a configured client ID; the quarantine client uses it |
| ASM-TE012-06 | `DOCUMENT_CHANGE_REFUSED` is written to a dedicated structured audit logger until an ACE audit interface is supplied |
| ASM-TE012-07 | `caseId` and `documentId` in blob names are the UUIDs `recovery_case.id` and `document.id`; the story's "RW-2026-000701" and "DOC-0701" are illustrative |
| ASM-TE012-09 | The `documentHub` health component is not in the liveness or readiness probe groups |
| ASM-TE012-11 | Local emulator mode (Azurite) is allowed in DEV only and is a recorded local deviation |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | NEW_STORY (no earlier spec or trace chain; the baseline `documents` code is inherited footprint, A-04) |
| UI In Scope | NO. `[S]` §15: "No screen in this story" |
| Logic In Scope | YES |
| API In Scope | NO. `[S]` §12: "No endpoint of its own" |
| API Impact Type | NO_API_CHANGE |
| Impacted Existing Nodes | `documents.api.DocumentStore`, `documents.internal.BlobDocumentStore` (replaced); `application.yaml`, `application-local.yaml`; `.env.example`; `RecoveryDatabaseIT` (one property line); `build.gradle.kts` (comment) |
| New Nodes Required | Infrastructure template and parameter files; `documents.api`: `DocumentStorage`, `StoreRequest`, `BlobRef`, `StorageReadiness`, `WriteOnceViolationException`, `StorageUnavailableException`; `documents.internal.storage`: `DocumentContainers`, `DocumentContainersConfig`, `DocumentStorageProperties`, `StorageReadinessIndicator`, `StorageErrorMapper`, `ContentHashGuard`, `BlobStorageAdapter`, `DocumentAuditLog`, `LocalEmulatorBootstrap` |
| Inherited Existing Behavior | Actuator health with `show-details: when-authorized`, role RW-PLATADM (`application.yaml`); `SecurityConfig` permits `/actuator/health/**`; Spring Modulith boundaries; JaCoCo 80% line and branch gate |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| `[S]` §4 step 1 | Account: shared key off, public network off, TLS 1.2, private endpoint; four containers | SPEC-001, -002 | DIRECT | Template; verified by conformance test and SIT | COVERED |
| `[S]` §4 step 2, BR6 | Versioning and 30-day soft delete for rwb-docs | SPEC-003 | DIRECT | Account scope in Azure; see DGAP-03 | COVERED |
| `[S]` §4 step 2, BR1 | Time-based policy on rwb-docs-legal; locked in PROD only | SPEC-004 | DIRECT | `legalRetentionDays`, `legalPolicyLocked` parameters | COVERED |
| `[S]` §4 step 2, BR4 | Role assignments per container | SPEC-005 | DIRECT | Storage Blob Data Contributor at container scope | COVERED |
| `[S]` §4 step 3, BR5 | Ready only if four containers exist and legal policy present | SPEC-009 | DIRECT | `StorageReadinessIndicator` | COVERED |
| `[S]` §4 step 4 | Write by managed identity, legal type to rwb-docs-legal, else rwb-docs, name `{caseId}/{documentId}/v{docVersion}` | SPEC-007, -010, -011 | DIRECT | Choice of type per document stays in E1-024; this story routes on `writeOnce` | COVERED |
| `[S]` §4 step 5, X1 | Refused overwrite → WriteOnceViolationException; audit | SPEC-012, -013, -014 | DIRECT | 409 MSG-P5-002 mapping is E1-024 (seam SPEC-019) | COVERED |
| `[S]` §4 step 6, BR2 | New version is a new blob; earlier readable | SPEC-010, -011, -015 | DIRECT | `docVersion` in the name | COVERED |
| `[S]` §4 step 7 | Readiness visible to platform administrator | SPEC-009 | DIRECT | Actuator `documentHub` component; SCR-44 display is another story | COVERED |
| `[S]` BR3, X3 | Managed identity only; keys and SAS disabled | SPEC-001, -007 | DIRECT | | COVERED |
| `[S]` BR7, X9, AC12 | Identical content returns existing blob; different is a violation | SPEC-012 | DIRECT | Resolves story-defect row step 5 (DGAP-14) | COVERED |
| AC1 | Overwrite refused, hash unchanged, audit, replaceContent → 409 | SPEC-004, -012, -013, -014, -018, -019 | DIRECT | Storage clause verified in SIT with a raw client (DGAP-15); `replaceContent` → 409 is E1-024 | COVERED |
| AC2 | Delete refused, blob readable | SPEC-004, -018 | DIRECT | Storage-level; SIT | COVERED |
| AC3 | v2 in write-once container allowed; v1 and v2 readable | SPEC-010, -011, -015 | DIRECT | | COVERED |
| AC4 | Standard container keeps versions; soft delete restore within 30 days | SPEC-003, -011, -018 | DIRECT | SIT | COVERED |
| AC5 | Identities hold only their roles | SPEC-005, -018 | DIRECT | SIT listing handed to RW-SECADM | COVERED |
| AC6 | Key or SAS refused with KeyBasedAuthenticationNotPermitted | SPEC-001, -018 | DIRECT | SIT | COVERED |
| AC7 | Identity with no role refused with AuthorizationPermissionMismatch | SPEC-005, -018 | DIRECT | SIT, RWB-SIT-SY-AGENT | COVERED |
| AC8 | Public network access refused | SPEC-001, -018 | DIRECT | SIT | COVERED |
| AC9 | Missing policy: not ready naming rwb-docs-legal; upload 503 MSG-GEN-006; no document row | SPEC-009, -011, -019 | DIRECT | Readiness and refusal here; HTTP 503 and "no row" in E1-024/E1-026 (seam) | COVERED |
| AC10 | No answer in 10 s → StorageUnavailableException; upload 503 | SPEC-007, -013, -019 | DIRECT | HTTP 503 in E1-024/E1-026 (seam) | COVERED |
| AC11 | Quarantine closed to user sessions; only SY-OCR writes | SPEC-005, -015 | DIRECT | | COVERED |
| AC12 | Same hash → no overwrite, existing ref; different → violation | SPEC-012 | DIRECT | | COVERED |
| X2, X4–X8, X10 | Exception paths | see Exceptional-case behaviour | DIRECT | X10 is TC-TE-012-13 via E1-026 endpoint | COVERED |
| `[S]` §13 flag | `rwb.dochub.storage-containers`: off → not ready, writes 503 | SPEC-006, -009, -011 | DIRECT | | COVERED |
| `[S]` §17 guardrails | No business values in code; no personal data; no keys, connection strings or SAS | SPEC-006, -007, -010, -014, -017 | DIRECT | Emulator key exception is local only (SPEC-017) | COVERED |
| `[DL]` D-RCV-31 | Published `DocumentStorage`; store refuses when policy absent (MSG-GEN-006); no blob written except through it | SPEC-010, -011 | DIRECT | | COVERED |
| Health endpoint | Actuator health, details for RW-PLATADM | SPEC-009 | INHERITED_EXISTING_BEHAVIOR | `application.yaml` management block | COVERED |

28 rows, 28 covered, 0 blocked.

## User story intent interpretation

`[S]` §1: a platform administrator wants blob containers for documents, a write-once container for legal types, reached by managed identity, "so that legal documents cannot be overwritten". The deliverable is storage plus the single code path through which the service writes it (`[DL]` D-RCV-31). It is not the document record, the type-to-container choice, retention classes, legal hold or backup (`[S]` §19). The business outcome is REQ-DCM-003 (write-once legal documents) and REQ-DCM-002 (the hub is the system of record) (`[S]` §18).

## Entry trigger and preconditions

| Trigger | Preconditions | Source |
|---|---|---|
| Platform administrator applies the template per environment | RWB-TE-001 done; DL27 option A (one storage account per environment in the SCB tenant, private endpoint); managed identities RWB-{DEV,SIT,UAT,PROD}-SY-OCR and the ACE service identity exist; the ACE pipeline can apply storage templates to DEV and SIT | `[S]` §3 |
| Service start | Flag `rwb.dochub.storage-containers` on; `rwb.dochub.*` properties set | `[S]` §4 step 3, §13 |
| A caller in P5 stores or opens a blob | Readiness READY for a store | `[S]` BR5; `[DL]` D-RCV-31 |

DL26 and DL27 are open and past their needed-by date in `[DL]`; the story gives assumed defaults (3,650 days; 30 days), so they do not block (DGAP-04).

## Field-level behaviour matrix

### Configuration properties (SPEC-006)

| Property | Default in `application.yaml` | Local profile | Rule | Source |
|---|---|---|---|---|
| `rwb.dochub.storage-containers` | `false` | `true` | Feature flag. Off: not ready, every store refused | `[S]` §13 |
| `rwb.dochub.storage.account-url` | `${RWB_DOCHUB_ACCOUNT_URL:}` | — | Required when flag on and not emulator mode; `https://` only | `[S]` §13 |
| `rwb.dochub.storage.timeout-seconds` | `10` | `10` | Integer 1–60; overall time per SDK call, retries included | `[S]` §13, AC10 |
| `rwb.dochub.storage.service-identity-client-id` | `${RWB_DOCHUB_SERVICE_MI_CLIENT_ID:}` | — | Client ID of the ACE service identity; blank uses the default managed identity | ASM-TE012-05 |
| `rwb.dochub.storage.ocr-identity-client-id` | `${RWB_DOCHUB_OCR_MI_CLIENT_ID:}` | — | Client ID of RWB-{ENV}-SY-OCR; blank makes readiness NOT_READY naming `rwb-quarantine` | ASM-TE012-05 |
| `rwb.dochub.storage.emulator-connection-string` | `${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}` | from `.env` | Emulator mode only; see SPEC-017 | ASM-TE012-11 |
| `rwb.dochub.container.intake` | `rwb-intake` | same | Container name | `[S]` §4, §13 |
| `rwb.dochub.container.standard` | `rwb-docs` | same | Container name | `[S]` §4, §13; `[FSD-P5]` |
| `rwb.dochub.container.legal` | `rwb-docs-legal` | same | Container name | `[S]` §4, §13; `[DL]` D-RCV-31 |
| `rwb.dochub.container.quarantine` | `rwb-quarantine` | same | Container name | `[S]` §4, §13; `[E1-041]` |

The four names must be distinct, 3–63 characters, lower case letters, digits and hyphens; otherwise startup fails (Azure container naming). The `rwb.blob.*` block is removed.

### StoreRequest (input to `DocumentStorage.store`)

| Field | Type | Rule | Source |
|---|---|---|---|
| `caseId` | UUID | Not null. `recovery_case.id` | `[S]` §11; `[API]` caseId format uuid; `[SCH]` `document.case_id uuid` |
| `documentId` | UUID | Not null. `document.id` | `[SCH]` |
| `docVersion` | int | ≥ 1 | `[SCH]` `doc_version integer NOT NULL DEFAULT 1` (DF-DOC-011) |
| `writeOnce` | boolean | true → `rwb-docs-legal`; false → `rwb-docs` | `[S]` §4 step 4; DF-DOC-010 |
| `contentType` | String | Not blank | Blob header |
| `content` | byte[] | Not null | — |

A violation raises `IllegalArgumentException` with no storage call (programming error; size limits and 413/415 belong to the upload endpoint, `[API]`).

### BlobRef (output)

| Field | Value | Source |
|---|---|---|
| `container` | Configured container name | `[S]` §11 |
| `blobName` | `{caseId}/{documentId}/v{docVersion}`, UUIDs in canonical lower-case form | `[S]` §4 step 4; `[DL]` D-RCV-31 |
| `storageRef()` | `{container}/{blobName}`; at most 100 characters, within `varchar(400)` | `[S]` §11, §13 "Database"; `[SCH]` `storage_ref varchar(400)` |
| `sha256` | Lower-case hex SHA-256 of the content | `[S]` §13 ContentHashGuard |
| `size` | Bytes | — |
| `existing` | true when ContentHashGuard returned an existing write-once blob | `[S]` AC12 |

### Blob metadata written at creation

| Key | Value | Rule |
|---|---|---|
| `sha256` | As `BlobRef.sha256` | Read by ContentHashGuard. No other metadata; no personal data (`[S]` §17) |
| Content-Type header | `contentType` | — |

### Audit event `DOCUMENT_CHANGE_REFUSED` (SPEC-014)

| Field | Value | Source |
|---|---|---|
| `eventType` | `DOCUMENT_CHANGE_REFUSED` | `[FSD-P5]` AC-ALT-P5-001-01; `[E1-024]` X1 |
| `occurredAt` | UTC instant | `[S]` AC1 "with the identity and the time" |
| `storageIdentity` | `ACE_SERVICE` or `SY_OCR` (identity role label, not a secret) | `[S]` AC1 |
| `operation` | `WRITE` or `DELETE` | `[S]` §13 StorageErrorMapper |
| `documentId` | UUID from the request or name | `[FSD-P5]` AC-ALT-P5-001-01 "with the document ID and the caller" |
| `actorId` | Subject of the authenticated user in the security context, when present; absent for system calls | `[FSD-P5]` "the caller"; staff identifier only, no customer data |
| `container`, `blobName` | As BlobRef | IDs only (`[S]` §17) |
| `reason` | `HASH_MISMATCH` or `STORAGE_REFUSED` (with the Azure error code) | `[S]` BR7, X1 |
| `traceId` | Current trace ID if present | Observability baseline |

### Health component `documentHub` (SPEC-009)

| Detail | Values |
|---|---|
| status | `UP` (READY); `DOWN` (container or policy missing, identity not configured, storage unreachable); `OUT_OF_SERVICE` (flag off) |
| `containers` | Map of each configured name to `PRESENT`, `MISSING` or `UNVERIFIED` |
| `legalPolicy` | `PRESENT`, `MISSING` or `EMULATED` |
| `reasons` | List of codes: `CONTAINER_MISSING:<name>`, `LEGAL_POLICY_MISSING:<name>`, `IDENTITY_NOT_CONFIGURED:<name>`, `UNREACHABLE`, `FLAG_OFF` |
| `checkedAt` | UTC instant |

Details are shown only to RW-PLATADM (existing `show-details: when-authorized`). No account URL, key or client ID is shown.

## Status-transition matrix

`[S]` §9: no case or document status changes. The only state is readiness, held in memory:

| From | Event | Guard | To |
|---|---|---|---|
| NOT_EVALUATED | Application ready | Flag off | NOT_READY (`FLAG_OFF`) |
| NOT_EVALUATED | Application ready | All four containers present and legal policy present (or `EMULATED`) and both identities configured | READY |
| NOT_EVALUATED | Application ready | Any check fails or storage unreachable | NOT_READY (reasons) |
| READY / NOT_READY | Health read of `documentHub` | Re-evaluate | READY or NOT_READY |
| NOT_READY | `store()` called | One re-evaluation, then the state decides | READY (store proceeds) or NOT_READY (refused) |

## Exceptional-case behaviour

| ID | Case | Behaviour in this story | Message (owner of HTTP mapping) | Source |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | Through the adapter: ContentHashGuard finds a different hash → `WriteOnceViolationException` + audit, no write. Raw client: storage returns `BlobImmutableDueToPolicy` (SIT) | MSG-P5-002, 409 (E1-024) | `[S]` X1, AC1; `[MSG]` |
| X2 | Delete of a write-once blob | Storage refuses; no delete operation is published in this story; `StorageErrorMapper` maps a `DELETE` refusal to `WriteOnceViolationException` + audit for later callers | MSG-P5-002 (E1-024) | `[S]` X2, AC2 |
| X3 | Account key or SAS | Storage refuses (`KeyBasedAuthenticationNotPermitted`); the service never builds a key or SAS client outside emulator mode | None | `[S]` X3, AC6 |
| X4 | Identity with no role | Storage refuses (`AuthorizationPermissionMismatch`). If the service meets it, `StorageUnavailableException(ACCESS_REFUSED)` and an ERROR log line with container and error code | MSG-GEN-006, 503 (E1-024) | `[S]` X4, AC7; ASM-TE012-15 |
| X5 | Outside the private endpoint | Storage refuses; network-level, SIT | None | `[S]` X5, AC8 |
| X6 | Container or policy missing at start | NOT_READY naming the container; `store()` raises `StorageUnavailableException(NOT_READY)` | MSG-GEN-006, 503 (E1-024/E1-026) | `[S]` X6, AC9; `[DL]` D-RCV-31 |
| X7 | No answer within the timeout | `StorageUnavailableException(TIMEOUT)` after `timeout-seconds` | MSG-GEN-006, 503 (E1-024/E1-026) | `[S]` X7, AC10 |
| X8 | User session reads quarantine | `open()` accepts only the standard and legal containers; a quarantine ref raises `IllegalArgumentException` with no storage call; the ACE identity holds no role on `rwb-quarantine` | None | `[S]` X8, AC11 |
| X9 | Same name, same content, write-once | Guard compares first: same hash → existing `BlobRef`, no upload. Race: `If-None-Match: *` upload gets `BlobAlreadyExists` → guard re-compares | None | `[S]` X9, AC12; story-defect row step 5 |
| X10 | Role without Documents C uploads | Not reachable in this story; endpoint check in E1-026 (TC-TE-012-13) | MSG-P4-002, 403 (existing `ApiError.NOT_PERMITTED`) | `[S]` X10 |
| — | Storage 5xx or I/O failure after SDK retries | `StorageUnavailableException(UNAVAILABLE)` | MSG-GEN-006, 503 | `[S]` §12 "503 when storage is unavailable" |
| — | Flag off | `StorageUnavailableException(NOT_READY)`; reason `FLAG_OFF` | MSG-GEN-006, 503 | `[S]` §13 |

`StorageUnavailableException` carries a `Reason` enum `{NOT_READY, TIMEOUT, UNAVAILABLE, ACCESS_REFUSED}` and the container name; the story names only two exceptions to callers (`[S]` §12), so not-ready uses this type (ASM-TE012-10).

## API change assessment

| Item | Assessment |
|---|---|
| Endpoints added or changed | None. `[S]` §12 "No endpoint of its own" |
| Endpoint that depends on this story | `POST /api/recovery/v1/cases/{caseId}/documents` (`postCasesCaseidDocuments`, `[API]`), owned by RWB-E1-026/RWB-E1-024. `[API]` lists 503 and no 409 for it; 409 MSG-P5-002 arises on `replaceContent` in E1-024 (seam) |
| Actuator | `documentHub` health component under the existing `/actuator/health`. Operational endpoint outside the API specification, as README decision 6 records for existing operational endpoints |
| Contract file | `contracts/backend-apis.json`: `NO_API_CHANGE` |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | `[S]` §15 | No screen; SCR-44 display is another story | n/a |
| Backend | YES | REQUIRED | 80% line and branch on `th.co.scb.ace.demo.recovery` (`recoveryCoverageVerification`) | SPEC-006 to -017; AC9, AC10, AC12; BR5, BR7 | New adapter, guard, mapper, readiness and config logic | Every row of "Unit tests" in SPEC-018 passes; coverage gate passes; `RecoveryBoundaryTest` and Modulith verification pass unchanged |

## Frontend Specification

Not applicable. No screen, component, route or client type changes (`[S]` §15). The readiness display on SCR-44 Interface and job monitor is owned by the story that builds SCR-44 and reads the `documentHub` component. `contracts/frontend-integrations.json` records `NOT_APPLICABLE`.

## Backend Specification

### SPEC-RWB-TE-012-001 — Storage account settings (template)

The template sets, per environment, on one storage account (DL27 option A, `[S]` §3):

| Setting | Value | Source |
|---|---|---|
| Shared key access | Disabled | `[S]` §4 step 1, BR3 |
| Public network access | Disabled | `[S]` §4 step 1; `[ENV]` §3 Network; `[SEC]` Network |
| Minimum TLS | 1.2 | `[S]` §4 step 1 |
| Private endpoint | Blob sub-resource, in the ACE network | `[S]` §3, §4 step 1; `[ENV]` §3 |
| Region, redundancy SKU, default access tier | Required parameters with no default in the template; supplied by the platform team per environment | Not stated in the document set (DGAP-05, -07, -13); ASM-TE012-12 |
| Encryption at rest | Platform default (Microsoft-managed keys); no key parameter added | `[NFR]` NFR-053 says only "encrypted" (DGAP-06); ASM-TE012-12 |

### SPEC-RWB-TE-012-002 — Containers (template)

Four private containers (no public access) named by parameters with the defaults `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` (`[S]` §4 step 1). The parameter values must equal the `rwb.dochub.container.*` properties for that environment.

### SPEC-RWB-TE-012-003 — Versioning and soft delete (template)

Blob versioning on; blob soft delete on with `softDeleteDays` (default 30, ASM-TE012-02) (`[S]` §4 step 2, BR6). In Azure these are blob-service (account) settings, so they also apply to `rwb-intake`, `rwb-docs-legal` and `rwb-quarantine`. The effect on the legal container and its policy is checked when the template is applied in DEV and SIT (DGAP-03).

### SPEC-RWB-TE-012-004 — Write-once policy (template)

Container-level time-based immutability policy on `rwb-docs-legal`, period `legalRetentionDays` since creation (default 3650, ASM-TE012-01). `legalPolicyLocked` = true in PROD only; DEV, SIT and UAT stay unlocked so test data can be removed (`[S]` BR1). Locking is irreversible; where the template format cannot express the lock, it is a separate PROD-only pipeline step after the policy exists (ASM-TE012-04). No legal hold is set (`[S]` §19).

### SPEC-RWB-TE-012-005 — Role assignments (template)

| Identity | Role | Scope | Source |
|---|---|---|---|
| ACE service managed identity | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-docs-legal` (each container) | `[S]` §4 step 2, AC5 |
| RWB-{ENV}-SY-OCR | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-quarantine` (each container) | `[S]` §4 step 2, AC5; `[URP]` SY-OCR Documents CRU |

No account-scope data role for either identity; no other identity. RW-SECADM reviews the SIT listing (`[S]` §13 "Done when").

### SPEC-RWB-TE-012-006 — Properties and flag

`DocumentStorageProperties` (`@ConfigurationProperties("rwb.dochub")`, in `documents.internal.storage`) binds the table in "Configuration properties" and validates it at startup (names, timeout range, `https` URL). This follows the module sub-prefix rule in `RecoveryProperties`. No container name, period or timeout is a literal in Java (`[S]` §17). Flag off: no client is built and no account URL is required.

### SPEC-RWB-TE-012-007 — DocumentContainersConfig: identities, timeout, no creation

- Two `BlobServiceClient`s against `account-url`: one with the ACE service identity, one with SY-OCR. Each credential is a chain of `WorkloadIdentityCredential` and `ManagedIdentityCredential` only, with the configured client ID. No environment secret, CLI, developer-tool or shared-cache credential (`[S]` §13 "restricted to managed identity"; BR3; `[SEC]` "one identity per non-human actor").
- Every SDK call goes through one helper that passes `Duration.ofSeconds(timeout-seconds)` as the overall operation timeout, so SDK retries are inside the 10 s (`[S]` AC10).
- No `create`, `createIfNotExists`, `setAccessPolicy` or delete-container call outside `LocalEmulatorBootstrap` (SPEC-017).
- If `account-url` is set together with `emulator-connection-string`, startup fails.

### SPEC-RWB-TE-012-008 — DocumentContainers (internal)

`documents.internal.storage.DocumentContainers` with `intake()`, `standard()`, `legal()`, `quarantine()` returning `BlobContainerClient`, and `readiness()`. Intake, standard and legal use the ACE identity; quarantine uses SY-OCR. It is internal to the `documents` module: `[S]` §12 calls it a published interface, but it returns an Azure type and BND-5 forbids `com.azure.storage` outside `documents.internal` (DGAP-02). Its callers in E1-041 (QuarantineMover) and E1-057 (IntakeService) are in P5.

### SPEC-RWB-TE-012-009 — Readiness

`StorageReadinessIndicator` (a `HealthIndicator` named `documentHub`) and `StorageReadiness` (published record: `ready`, `reasons`, `checkedAt`).

- Checks: for each container, get properties (404 → `MISSING`); for `rwb-docs-legal`, `hasImmutabilityPolicy` must be true (`[S]` BR5, AC9). Intake, standard and legal are checked with the ACE identity; quarantine with SY-OCR. A blank OCR client ID gives `IDENTITY_NOT_CONFIGURED:rwb-quarantine`. A timeout or 5xx gives `UNREACHABLE`.
- Evaluated when the application is ready, on every read of the component, and once inside a `store()` while NOT_READY (ASM-TE012-08).
- Lock state and period are not visible to the data-plane identity; they are checked by the template conformance test and SIT (TC-TE-012-09).
- Not added to the `liveness` or `readiness` probe groups, so the service stays in rotation and answers 503 MSG-GEN-006 as AC9 requires (ASM-TE012-09).
- One INFO log line on each change of state, with reasons; no URL or ID.

### SPEC-RWB-TE-012-010 — DocumentStorage (published)

```java
package th.co.scb.ace.demo.recovery.documents.api;

public interface DocumentStorage {
    BlobRef store(StoreRequest request);   // WriteOnceViolationException, StorageUnavailableException
    byte[] open(BlobRef ref);              // StorageUnavailableException
    StorageReadiness readiness();
}
public record StoreRequest(UUID caseId, UUID documentId, int docVersion, boolean writeOnce,
                           String contentType, byte[] content) { }
public record BlobRef(String container, String blobName, String sha256, long size, boolean existing) {
    public String storageRef() { return container + "/" + blobName; }
}
```

`WriteOnceViolationException` (container, blobName) and `StorageUnavailableException` (reason, container) are unchecked, in `documents.api`. No Azure type appears in `documents.api` (BND-5). Name per `[DL]` D-RCV-31 and `[E1-024]` §13 ("DocumentStorage … called, never reimplemented").

### SPEC-RWB-TE-012-011 — BlobStorageAdapter: store

1. Flag off → `StorageUnavailableException(NOT_READY)`.
2. Readiness NOT_READY after one re-evaluation → `StorageUnavailableException(NOT_READY)`; no storage write (`[DL]` D-RCV-31).
3. Validate `StoreRequest`; build the name; SHA-256 the content.
4. `writeOnce = false` → upload to `rwb-docs`, overwrite allowed; versioning keeps the earlier version (`[S]` AC4, ASM-TE012-18).
5. `writeOnce = true` → ContentHashGuard (SPEC-012), then upload to `rwb-docs-legal` with `If-None-Match: *` and the `sha256` metadata.
6. Errors go through StorageErrorMapper (SPEC-013).
7. Return `BlobRef`. A new version is a new name (`v{n+1}`); earlier blobs are untouched (`[S]` BR2, AC3).

### SPEC-RWB-TE-012-012 — ContentHashGuard

Before a write-once upload: read the existing blob's properties. Not found → proceed. Found → take metadata `sha256`; if absent, download and hash it (within the timeout). Equal → return the existing `BlobRef` (`existing = true`), no upload. Different → `WriteOnceViolationException` and audit `HASH_MISMATCH`. On `BlobAlreadyExists` from the conditional upload (a concurrent writer), compare once more with the same rule. This meets AC12 ("attempts no overwrite") and X9, and settles the story-defect row (DGAP-14).

### SPEC-RWB-TE-012-013 — StorageErrorMapper

| Input | Output |
|---|---|
| `BlobImmutableDueToPolicy`, or 409 on `rwb-docs-legal` after the guard re-check | `WriteOnceViolationException` + audit `STORAGE_REFUSED` |
| `DELETE` refused on `rwb-docs-legal` | `WriteOnceViolationException` + audit `STORAGE_REFUSED` |
| Overall timeout exceeded (`TimeoutException` cause) | `StorageUnavailableException(TIMEOUT)` |
| 5xx after retries, connection or I/O failure | `StorageUnavailableException(UNAVAILABLE)` |
| 403 `AuthorizationPermissionMismatch`, `KeyBasedAuthenticationNotPermitted`, `AuthorizationFailure` | `StorageUnavailableException(ACCESS_REFUSED)` + ERROR log (ASM-TE012-15) |
| `BlobNotFound` on `open()` | `StorageUnavailableException(UNAVAILABLE)`; the row points to a missing blob (ASM-TE012-15) |
| Anything else | Rethrown unchanged |

Log lines carry container, blob name, error code and trace ID only.

### SPEC-RWB-TE-012-014 — Audit of refused changes

`DocumentAuditLog` writes `DOCUMENT_CHANGE_REFUSED` (fields above) as one structured line to the logger `recovery.audit`, the stand-in for the ACE audit log (`[AUD]` "ACE audit log … ACE logging"; ASM-TE012-06). Attempts made directly on the container, not through the service, are recorded by the storage platform only if resource logs are on; the document set does not say so (DGAP-11).

### SPEC-RWB-TE-012-015 — BlobStorageAdapter: open

Accepts a `BlobRef` whose container is the configured standard or legal container; anything else (including quarantine and intake) → `IllegalArgumentException`, no storage call (`[S]` AC11). Downloads with the ACE identity within the timeout. Reads are not gated by readiness (ASM-TE012-13).

### SPEC-RWB-TE-012-016 — Baseline corrections

Delete `DocumentStore`, `BlobDocumentStore`, `DocumentImmutableException` and `BlobProperties`; remove the `rwb.blob` block from `application.yaml` and the `rwb.blob` mention in the `RecoveryProperties` comment; remove the `rwb.blob.connection-string` line from `RecoveryDatabaseIT` (flag off by default needs no storage); rename `RWB_BLOB_CONNECTION_STRING` in `.env.example` to `RWB_DOCHUB_EMULATOR_CONNECTION_STRING`; correct the `build.gradle.kts` comment. The `documents.api` package-info (`@NamedInterface("api")`) and the module package-info are unchanged.

### SPEC-RWB-TE-012-017 — Local emulator mode

Active only when `emulator-connection-string` is set **and** `rwb.environment` is `DEV` **and** the account name is `devstoreaccount1` **and** the blob endpoint host is `127.0.0.1`, `localhost` or `azurite`. Otherwise startup fails. In this mode: one shared-key client for all four containers (Azurite has no managed identity); `LocalEmulatorBootstrap` creates the four containers at startup; `legalPolicy` is `EMULATED` because Azurite has no immutability policy, so write-once is the conditional upload plus ContentHashGuard. This is a local deviation; the Builder adds a README "Decisions taken" row (shared-updates). The published Azurite development key is the only key allowed, and only in `.env` / `.env.example`.

### SPEC-RWB-TE-012-018 — Tests

Unit (`./scripts/dev.ps1 test`, counted in the 80% gate):

| Test | Proves |
|---|---|
| `DocumentStoragePropertiesTest` | Binding, defaults (timeout 10, four names), name and URL validation, flag off needs no URL |
| `DocumentContainersConfigTest` | Credential chain holds only workload and managed identity types; no create call; emulator guard refuses non-DEV, non-loopback and non-`devstoreaccount1` |
| `BlobNamingTest` | `{caseId}/{documentId}/v{docVersion}`; `storageRef` ≤ 100 characters; invalid requests refused |
| `ContentHashGuardTest` | Same hash → existing ref, no upload; different → violation + audit; missing metadata → computed; race re-check |
| `StorageErrorMapperTest` | Each row of SPEC-013 |
| `StorageReadinessIndicatorTest` | Each reason; flag off → `OUT_OF_SERVICE`; re-evaluation on `store()` |
| `BlobStorageAdapterTimeoutTest` | JDK `HttpServer` stub that never answers, emulator mode, `timeout-seconds=1`: `StorageUnavailableException(TIMEOUT)` within 1 s plus a bound (AC10 logic; the 10 s value by the properties test) |
| `StorageTemplateConformanceTest` | Parses the four parameter files and the template: shared key off, public network off, TLS 1.2, four containers, versioning, soft delete days, policy days, lock true only in PROD, six container-scope role assignments |

Integration (`@Tag("recovery-it")`, Testcontainers `GenericContainer` with `mcr.microsoft.com/azure-storage/azurite:3.37.0`): naming, standard overwrite, write-once conditional upload, guard AC12 both branches, readiness `CONTAINER_MISSING` when a container is absent, `open` refusal of quarantine.

System tests in SIT (`[TC]` TC-TE-012-01 to -12): run against the real account; recorded `PENDING_ENVIRONMENT` until the template is applied in SIT. AC1's storage clause uses a raw client with the ACE identity, because the adapter's guard stops the write first (DGAP-15).

No new dependency: Testcontainers core is already present; the stub uses the JDK.

### SPEC-RWB-TE-012-019 — Seams to later stories (out of scope here, D-RUN-08)

| Seam | Owner |
|---|---|
| Choose `writeOnce` per document type; write the document row; `replaceContent` → 409 MSG-P5-002; map `StorageUnavailableException` → 503 MSG-GEN-006 (`ApiError` entries per README decision 5) | RWB-E1-024 |
| Call `readiness()` before inserting the document row so AC9 "no document row" holds; `[E1-024]` writes the row (COPY_PENDING) before storing | RWB-E1-024 (open item in shared-updates) |
| Upload endpoint and TC-TE-012-13 | RWB-E1-026 |
| QuarantineMover, retention classes | RWB-E1-041 |
| IntakeService | RWB-E1-057 |
| Legal re-store after type confirmation | RWB-E1-032 (`[DL]` D-RCV-31) |

## Security, privacy and performance

- No key, connection string or SAS outside the local emulator mode (`[S]` §17; `[SEC]` "No secret in code, configuration or prompts").
- Blob names and logs carry UUIDs only. The case number is not used: `[PDPA]` §1 treats case and account numbers as indirect identifiers (ASM-TE012-07).
- Region: `[PDPA]` §8 keeps data in the SCB Azure tenant, Southeast Asia, with the bank position to confirm (DGAP-13).
- Timeout: 10 s per call (`[S]` §13). `backend-context.md` §8 says 30 s for external calls; the story value applies (DGAP-08).

## Guardrails and out of scope

Guardrails (`[S]` §17): no business value in code; no personal data in logs, tests or prompts (synthetic UUIDs and generated bytes only); no read of another module's tables; no account key, connection string or SAS in code, configuration or pipeline (local Azurite key only, SPEC-017).

Out of scope (`[S]` §19): container choice per type and the document row (E1-024); retention classes, archive and JOB-17 (E1-041); legal hold (REQ-DCM-016, DL27); backup and restore test (REQ-DCM-015, DL27); sizing and cost (REQ-DCM-014, NFR-069).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | `[S]` §12, §4 step 4; `[DL]` D-RCV-31; `[E1-024]` §13 | Who publishes the write path: story says `DocumentContainers` with the adapter in E1-024; D-RCV-31 and E1-024 say TE-012 publishes `DocumentStorage` | Interface ownership | Precedence: Decision Log v10 over story v7. TE-012 publishes `DocumentStorage`; `DocumentContainers` is internal (DGAP-01) | RESOLVED | SPEC-008, -010 |
| CLAR-002 | `[S]` §12; BND-5 | Published interface returns `BlobContainerClient` | Boundary test would fail | Keep `DocumentContainers` in `documents.internal` (DGAP-02) | RESOLVED | SPEC-008 |
| CLAR-003 | `[S]` BR6; Azure blob service settings | Versioning and soft delete "for rwb-docs" are account-wide | Applies to all four containers | Set at account scope; verify interaction with the legal policy in DEV/SIT (DGAP-03) | RESOLVED | SPEC-003 |
| CLAR-004 | `[S]` §3, BR1; `[RET]` §1 | 3,650 days from creation versus "10 years after the case closes" | Policy is a floor, not the full retention | Template parameter 3650; full retention in E1-041 after DL26 (DGAP-04) | RESOLVED | SPEC-004 |
| CLAR-005 | `[RET]` §2; `[ADR]`; `[NFR]`; `[PDPA]` | Access tier, encryption key type, redundancy and region not set | Template values | Required parameters or platform default; no value invented (DGAP-05, -06, -07, -13) | RESOLVED | SPEC-001 |
| CLAR-006 | `[S]` X9 vs AC12; story-defect row | Order of storage refusal and hash check | Behaviour of a repeated write | Hash first, conditional upload second, re-check on race | RESOLVED | SPEC-012 |
| CLAR-007 | `[S]` AC5, AC11; `[E1-041]` | Quarantine readable only by SY-OCR, but the service checks it | Second identity in the service | Configured SY-OCR client ID (DGAP-10, ASM-TE012-05) | RESOLVED | SPEC-007, -009 |
| CLAR-008 | `[S]` AC1, X1; `[AUD]` | Where the refused-change audit goes; direct attempts | Audit sink | Structured audit logger now; resource logs gap (DGAP-11, ASM-TE012-06) | RESOLVED | SPEC-014 |
| CLAR-009 | `[S]` AC examples; `[API]`; `[SCH]` | Case number or UUID in blob name | Name and PDPA | UUIDs (ASM-TE012-07, DGAP-16) | RESOLVED | SPEC-010 |
| CLAR-010 | `[S]` §13 "format the ACE team uses" | Template format and location | Template file | Bicep in `infra/azure/document-storage/` (ASM-TE012-03, DGAP-09) | RESOLVED | SPEC-001 to -005 |
| CLAR-011 | `[S]` AC9; `[E1-024]` flow | Row written before storage call vs "no document row" | AC9 last clause | E1-024 checks `readiness()` first; open item | RESOLVED | SPEC-019 |
| CLAR-012 | Local stack; README "Local versus target" | Azurite has no managed identity or immutability | Local runs | Emulator mode, DEV only (ASM-TE012-11) | RESOLVED | SPEC-017 |

`CLARIFICATION_STATUS: RESOLVED` — 12 items resolved by precedence, the story's assumed defaults or labelled assumptions. No question was asked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Jira, Confluence, GitLab or Figma MCP connected (RUN-BRIEF rule 5); no UI in scope.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Storage template, managed-identity clients, readiness and the published DocumentStorage write path; corrects the baseline BlobDocumentStore; no endpoint, screen or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: enabler with no endpoint of its own, story §12]
REQUIREMENT_COVERAGE_SUMMARY: 7 BRs, 12 ACs, 7 flow steps, 10 exception paths, flag, guardrails and D-RCV-31 mapped in 28 rows.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [COVERED_RULES: 28] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_GATE_RESULT: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 5] [LOW: 5] — handoff blocked
NEXT_STEP: Human resolves SG-01 to SG-06 (first SG-01: module map dochub per the TE-001 remediation), reruns this stage, then spec-gate-review-2.md.
```

Contradictions between sources are recorded and resolved in `document-gaps.md`; none is left open in this spec.
