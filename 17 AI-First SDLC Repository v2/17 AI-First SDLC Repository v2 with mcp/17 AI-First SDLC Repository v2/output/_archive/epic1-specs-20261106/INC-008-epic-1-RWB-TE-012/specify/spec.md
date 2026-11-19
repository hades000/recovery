# Technical Specification — RWB-TE-012 Document storage containers

| Field | Value |
|---|---|
| Story | RWB-TE-012 — Document storage containers |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-008-epic-1-RWB-TE-012` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-014); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 012 Document storage containers v1.md`; FSD P5 A2.1; TSD P5 T3.1, T6 |
| Upstream IDs | BRD-RWB-005; FR-RWB-014; BR-RWB-010; REQ-DCM-002, REQ-DCM-003; US-RWB-TE-012; CTX-FEATURE-005; CTL-09, CTL-12; NFR-029; DL26, DL27 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Platform administrator and solution architect (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label or state changes. The platform administrator reads document hub readiness on SCR-44 Interface and job monitor, which is an Epic 2/E8 screen and is not built here. |
| Logic In Scope | `YES` — container configuration, write-once policy, managed-identity access, role assignment, readiness, error mapping and content-hash guard. |
| API In Scope | `NO` — no endpoint or schema of its own. The story supplies storage to `POST /api/recovery/v1/cases/{caseId}/documents` (API-P5-001, built in RWB-E1-026). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | ACE storage account and private endpoint; containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine`; ACE health endpoint; upload (RWB-E1-026), store (RWB-E1-024), malware scan (RWB-E1-041) and intake (RWB-E1-057). |
| New Nodes Required | `YES` — storage infrastructure template, `DocumentContainers`, `DocumentContainersConfig`, `BlobStorageAdapter`, `StorageReadinessIndicator`, `StorageErrorMapper`, `ContentHashGuard`. |
| Inherited Existing Behavior | Module folder and boundary test (RWB-TE-001); ACE health endpoint; ACE audit log; ACE storage pattern and private endpoint (DL27). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The write-once container refuses overwrite and delete for the retention period; the policy is locked in PROD and unlocked in DEV, SIT and UAT. | SPEC-RWB-TE-012-003, SPEC-RWB-TE-012-008 | DIRECT | Template parameter `legalPolicyLocked`; policy `legalRetentionDays` 3650 (assumed; DL26). | COVERED |
| BR2 | A change to a stored document is a new blob at the next version; earlier versions stay readable. | SPEC-RWB-TE-012-009 | DIRECT | Path `{caseId}/{documentId}/v{docVersion}`; v1 is never replaced. | COVERED |
| BR3 | Storage is reached only by managed identity; account keys and shared access signatures are disabled. | SPEC-RWB-TE-012-005 | DIRECT | `allowSharedKeyAccess=false`, `publicNetworkAccess=Disabled`, TLS 1.2, private endpoint. | COVERED |
| BR4 | Each identity holds a role only on the containers it needs. | SPEC-RWB-TE-012-006 | DIRECT | ACE identity: intake, standard, legal. SY-OCR: intake, standard, quarantine. | COVERED |
| BR5 | The document hub reports ready only when the four containers exist and the write-once policy is in place. | SPEC-RWB-TE-012-007 | DIRECT | `StorageReadinessIndicator` joins the ACE health endpoint. | COVERED |
| BR6 | The standard container keeps blob versions and soft-deleted blobs for 30 days. | SPEC-RWB-TE-012-004 | DIRECT | Versioning on; `softDeleteDays` 30 (assumed; DL27). | COVERED |
| BR7 | A write of identical content to an existing write-once name returns the existing blob; different content is a violation. | SPEC-RWB-TE-012-012 | DIRECT | `ContentHashGuard` compares SHA-256 before the write. | COVERED |
| AC1 | A court notice is stored at `rwb-docs-legal/{caseId}/{documentId}/v1`; overwrite is refused, hash unchanged, attempt audited, `replaceContent` raises 409 MSG-P5-002. | SPEC-RWB-TE-012-003, SPEC-RWB-TE-012-008 | DIRECT | Storage returns `BlobImmutableDueToPolicy`; mapper raises `WriteOnceViolationException`. | COVERED |
| AC2 | A delete of the write-once blob is refused and the blob stays readable. | SPEC-RWB-TE-012-008 | DIRECT | Same refusal path; audit event for the delete attempt. | COVERED |
| AC3 | A new blob at v2 in the write-once container succeeds and both versions are readable. | SPEC-RWB-TE-012-009 | DIRECT | New name, not an overwrite. | COVERED |
| AC4 | The standard container keeps the previous blob version and restores a deleted blob within 30 days. | SPEC-RWB-TE-012-004 | DIRECT | Blob versioning and soft delete on `rwb-docs`. | COVERED |
| AC5 | The ACE identity and `RWB-SIT-SY-OCR` hold Storage Blob Data Contributor only on their named containers. | SPEC-RWB-TE-012-006 | DIRECT | Role listing is handed to the security administrator. | COVERED |
| AC6 | Key-based access and shared access signatures are refused with `KeyBasedAuthenticationNotPermitted`. | SPEC-RWB-TE-012-005 | DIRECT | Shared key access off; no connection string or SAS in configuration. | COVERED |
| AC7 | An identity with no role is refused with `AuthorizationPermissionMismatch`. | SPEC-RWB-TE-012-006 | DIRECT | `RWB-SIT-SY-AGENT` has no role on `rwb-docs-legal`. | COVERED |
| AC8 | Public network access is refused. | SPEC-RWB-TE-012-005 | DIRECT | Private endpoint only. | COVERED |
| AC9 | A missing immutability policy makes the hub not ready; upload returns 503 MSG-GEN-006 and writes no document row. | SPEC-RWB-TE-012-007, SPEC-RWB-TE-012-013 | DIRECT | Readiness fails naming `rwb-docs-legal`; upload gate. | COVERED |
| AC10 | Storage that does not answer within 10 seconds raises `StorageUnavailableException`; upload returns 503 MSG-GEN-006. | SPEC-RWB-TE-012-010 | DIRECT | Client timeout 10 seconds; no retry inside the request. | COVERED |
| AC11 | A user session cannot read the quarantine container; only `RWB-SIT-SY-OCR` writes it. | SPEC-RWB-TE-012-011 | DIRECT | No read path through the document store; role assignment excludes the ACE identity. | COVERED |
| AC12 | A repeated write of the same content to the same write-once name returns the existing blob; different content raises `WriteOnceViolationException`. | SPEC-RWB-TE-012-012 | DIRECT | Hash comparison before the write. | COVERED |
| X1 | Overwrite of a write-once blob. | SPEC-RWB-TE-012-008 | DIRECT | Refused; audit; MSG-P5-002. | COVERED |
| X2 | Delete of a write-once blob. | SPEC-RWB-TE-012-008 | DIRECT | Refused; blob unchanged. | COVERED |
| X3 | Access with an account key or shared access signature. | SPEC-RWB-TE-012-005 | DIRECT | Storage refuses. | COVERED |
| X4 | Access by an identity with no role. | SPEC-RWB-TE-012-006 | DIRECT | Storage refuses. | COVERED |
| X5 | Access from outside the private endpoint. | SPEC-RWB-TE-012-005 | DIRECT | Storage refuses. | COVERED |
| X6 | A container or the write-once policy is missing at start. | SPEC-RWB-TE-012-007, SPEC-RWB-TE-012-013 | DIRECT | Hub not ready; MSG-GEN-006. | COVERED |
| X7 | Storage does not answer within the timeout. | SPEC-RWB-TE-012-010 | DIRECT | `StorageUnavailableException`; 503. | COVERED |
| X8 | A user session reads the quarantine container. | SPEC-RWB-TE-012-011 | DIRECT | Refused. | COVERED |
| X9 | A same-hash write to an existing write-once name. | SPEC-RWB-TE-012-012 | DIRECT | Existing blob returned. | COVERED |
| X10 | A role without Documents C uploads. | SPEC-RWB-TE-012-016 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.

The story is an infrastructure enabler. It creates the storage account settings and four containers that every later P5 story writes to: `rwb-intake` for files received, `rwb-docs` for standard documents with version history, `rwb-docs-legal` for legal types under a time-based immutability policy, and `rwb-quarantine` for infected files. It also adds the adapter, readiness check and error mapper that turn storage behaviour into the document store's contract. It does not create a screen or an endpoint.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Infrastructure pipeline applies the storage template to an environment; ACE service start runs the readiness check; a document write calls `BlobStorageAdapter`. |
| Preconditions | RWB-TE-001 done; ACE storage pattern (DL27, option A) approved; managed identities `RWB-<ENV>-SY-OCR` and the ACE service identity exist; the infrastructure pipeline can apply templates to DEV and SIT; `rwb.dochub.storage-containers` flag on. |
| Input | Environment name; template parameters `legalRetentionDays`, `legalPolicyLocked`, `softDeleteDays`; container names; storage account URL. |
| Output | Four containers; immutability policy on `rwb-docs-legal`; versioning and soft delete on `rwb-docs`; role assignments; readiness state; audit events for refused changes. |
| Feature flag | `rwb.dochub.storage-containers`. Off: readiness reports not ready and every document write is refused with 503 rather than written outside the write-once container. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document` | `storage_ref` | Computed by `BlobStorageAdapter` | System writes | `{container}/{caseId}/{documentId}/v{docVersion}`, at most 400 characters |
| `document` | `write_once` | Document type table (RWB-E1-025) | Read-only to storage | Decides `rwb-docs-legal` or `rwb-docs` |
| `document` | `doc_version` | Document store | System writes | 1..n; a new version is a new blob |
| Storage account | `allowSharedKeyAccess` | Template | Immutable after apply | `false` |
| Storage account | `publicNetworkAccess` | Template | Immutable after apply | `Disabled`; private endpoint only |
| Storage account | `minimumTlsVersion` | Template | Immutable after apply | `TLS1_2` |
| Container `rwb-docs-legal` | Immutability policy | Template | Locked in PROD; unlocked elsewhere | `legalRetentionDays` 3650 (assumed; DL26) |
| Container `rwb-docs` | Versioning and soft delete | Template | Immutable after apply | Versioning on; `softDeleteDays` 30 (assumed; DL27) |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `STARTING` | Readiness check | Four containers exist and the legal policy is present | `READY` | Document writes allowed |
| `STARTING` | Readiness check | A container or the legal policy is missing | `NOT_READY` | Writes refused with 503 MSG-GEN-006; readiness names the missing item |
| `READY` | Readiness check | Policy removed or container unavailable | `NOT_READY` | Subsequent writes refused; no document row |
| Blob absent | Store version 1 | Type resolved and file validated | Blob at `v1` | Hash recorded; row `COPY_PENDING` then `STORED` |
| Blob at `v1` | Add version | Caller holds Documents U and the row is latest | Blob at `v2` | `v1` stays readable |

This story changes no case status and no document status; the document state transitions belong to RWB-E1-024.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Overwrite of a write-once blob | Storage refuses; blob unchanged; attempt in the ACE audit log with identity and time; 409 | MSG-P5-002 |
| X2 | Delete of a write-once blob | Storage refuses; blob unchanged; audit attempt | MSG-P5-002 |
| X3 | Account key or shared access signature | Storage refuses with `KeyBasedAuthenticationNotPermitted` | None |
| X4 | Identity with no role on the container | Storage refuses with `AuthorizationPermissionMismatch` | None |
| X5 | Call from outside the private endpoint | Storage refuses | None |
| X6 | Container or policy missing at start | Hub `NOT_READY`; uploads return 503; no document row | MSG-GEN-006 |
| X7 | Storage timeout | `StorageUnavailableException` after 10 seconds; caller returns 503 | MSG-GEN-006 |
| X8 | User session reads quarantine | Refused; only `RWB-<ENV>-SY-OCR` has access | None |
| X9 | Same-hash write to an existing write-once name | No overwrite attempt; existing blob reference returned | None |
| X10 | Role without Documents C uploads | 403; nothing written | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/cases/{caseId}/documents` (API-P5-001, built in RWB-E1-026). |
| Contract delta | None. The storage layer changes no request or response field. |
| Backward compatibility | Unchanged. |
| Authorization | Documents C on the upload endpoint; the storage layer acts under the ACE service identity. |
| Error behaviour | 403 MSG-P4-002; 503 MSG-GEN-006 when the hub is not ready or storage does not answer. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes; SCR-44 is Epic 2/E8. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-002, REQ-DCM-003; SPEC-RWB-TE-012-001..016 | New template, adapter, readiness indicator, error mapper and hash guard. | Container selection by `write_once`; refusal mapping for overwrite and delete; timeout mapping; readiness with each missing item; same-hash and different-hash writes; role-denied and key-denied clients. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| Storage infrastructure template | Configuration | Account settings, four containers, versioning, soft delete, immutability policy and role assignments. |
| `DocumentContainers` | Published interface | Returns the four container clients and the readiness state. |
| `DocumentContainersConfig` | Service | Builds clients with `DefaultAzureCredential` restricted to managed identity; 10-second timeout. |
| `BlobStorageAdapter` | Service | Writes, opens and refuses overwrite of blobs; implements `DocumentStorage`. |
| `StorageReadinessIndicator` | Service | Checks the four containers and the legal policy; joins the ACE health endpoint. |
| `StorageErrorMapper` | Service | Maps `BlobImmutableDueToPolicy` and conflicts on `rwb-docs-legal` to `WriteOnceViolationException`; timeouts to `StorageUnavailableException`; writes the audit event. |
| `ContentHashGuard` | Service | Compares SHA-256 of an existing write-once blob before a write. |

### Package and boundaries

Folder `recovery/dochub/storage`, Java package `recovery.dochub.storage`; the infrastructure template
lives in the ACE infrastructure folder in the format the ACE team uses. The package is the only place
that holds a blob client. Other P5 packages call `DocumentStorage`; they never build a client or read
a container directly.

### Data and migration

No table and no column. `storage_ref` follows `{container}/{caseId}/{documentId}/v{docVersion}` within
`varchar(400)`. Container names and the account URL are environment properties, not database rows.
There is no Flyway migration in this story.

### Container configuration

| Container | Purpose | Versioning | Soft delete | Immutability |
|---|---|---|---|---|
| `rwb-intake` | Files received from scan, SFTP, email and upload before storage | No | No | No |
| `rwb-docs` | Standard documents | Yes | 30 days (assumed; DL27) | No |
| `rwb-docs-legal` | Legal document types | No | No | Time-based, 3650 days (assumed; DL26); locked in PROD |
| `rwb-quarantine` | Files that fail the malware scan | No | No | No; SY-OCR only |

The template sets shared key access off, public network access off, TLS 1.2 minimum and a private
endpoint. No connection string, account key or shared access signature appears in code, configuration
or the pipeline.

### Write-once and versioning

- A type with `write_once = true` writes to `rwb-docs-legal`; every other type writes to `rwb-docs`.
- The immutability policy refuses any overwrite or delete inside its period. The refusal is a storage
  error, not an application check; the application cannot bypass it.
- A change is a new blob at `v{n+1}`. The earlier blob is never modified and remains readable.
- The policy is locked in PROD. In DEV, SIT and UAT it is unlocked so synthetic test data can be
  removed; this is a template parameter, not a code branch.

### Identity, network and roles

| Identity | Role | Containers |
|---|---|---|
| ACE service identity | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-docs-legal` |
| `RWB-<ENV>-SY-OCR` | Storage Blob Data Contributor | `rwb-intake`, `rwb-docs`, `rwb-quarantine` |
| Any other identity | None | None |

`DocumentContainersConfig` uses `DefaultAzureCredential` restricted to managed identity. Key-based
and SAS clients are not constructed anywhere.

### Readiness and error mapping

- `StorageReadinessIndicator` checks the four containers exist and that `rwb-docs-legal` carries its
  immutability policy. It reports `NOT_READY` naming the missing item.
- The upload endpoint checks readiness before accepting a file; `NOT_READY` returns 503 MSG-GEN-006 and
  writes no document row.
- `StorageErrorMapper` maps `BlobImmutableDueToPolicy` and write conflicts on `rwb-docs-legal` to
  `WriteOnceViolationException`; the store maps that to 409 MSG-P5-002. A timeout maps to
  `StorageUnavailableException` and 503 MSG-GEN-006.
- Each refused overwrite or delete writes the ACE audit event `DOCUMENT_CHANGE_REFUSED` with the
  document ID and the caller.

### Transaction and events

No database transaction and no domain event in this story. The audit event is written through the ACE
audit log after the storage refusal; a failed audit write does not change the refusal.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM Platform administrator | Platform administration CRUD; applies the template and reads readiness | All |
| RW-SECADM Security administrator | Platform administration CRUDA; reviews role assignments | All |
| SY-OCR OCR and extraction pipeline | Documents CRU on intake, standard and quarantine | All |
| ACE service identity | Storage Blob Data Contributor on intake, standard and legal | All |
| RW-CASEOWN Case owner | Documents CRU; uploads through the service identity | Own cases |

### Observability and operations

- Readiness appears on the ACE health endpoint and on SCR-44 when it is built.
- Metrics: write count by container; refusal count by reason; timeout count; readiness state.
- Alerts: hub not ready; storage timeout rate above threshold; policy missing in PROD.
- Run book: purpose, containers, policy lock state per environment, failure signs, escalation.

### Performance

- One blob write per document version; no read-before-write except the hash guard on a repeated
  write-once name.
- The 10-second client timeout bounds a failing call.
- Versioning and soft delete are storage features; they add no application latency.

### Feature flag and rollback

- `rwb.dochub.storage-containers`. Off: readiness is `NOT_READY` and every write is refused with 503.
- Rollback: turn the flag off and redeploy the previous tag. Containers and the policy are
  infrastructure; removing them is a separate, approved infrastructure change.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-012-01 | AC1, BR1 | System | Synthetic court notice in `rwb-docs-legal` | Overwrite refused; hash unchanged; audit; 409 MSG-P5-002 |
| TC-TE-012-02 | AC2, BR1 | System | Delete attempt on the same blob | Delete refused; blob readable |
| TC-TE-012-03 | AC3, BR2 | System | v2 blob for the same document | Write succeeds; v1 and v2 readable |
| TC-TE-012-04 | AC4, BR6 | System | Overwrite and delete in `rwb-docs` in SIT | Previous version readable; deleted blob restorable within 30 days |
| TC-TE-012-05 | AC5, BR4 | System | Role assignment listing in SIT | Only the named containers appear |
| TC-TE-012-06 | AC6, BR3 | System | Client with account key and with a SAS | Both refused with `KeyBasedAuthenticationNotPermitted` |
| TC-TE-012-07 | AC7, BR4 | System | `RWB-SIT-SY-AGENT` reads the legal blob | Refused with `AuthorizationPermissionMismatch` |
| TC-TE-012-08 | AC8, BR3 | System | Client outside the private endpoint | Refused |
| TC-TE-012-09 | AC9, BR5 | System | Policy removed in DEV | Hub not ready naming `rwb-docs-legal`; upload 503 MSG-GEN-006; no row |
| TC-TE-012-10 | AC10 | System | Storage stub with a 10-second timeout | `StorageUnavailableException`; upload 503 |
| TC-TE-012-11 | AC11, BR4 | System | File in `rwb-quarantine` | User read refused; SY-OCR write allowed |
| TC-TE-012-12 | AC12, BR7 | System | Same and different content to an existing name | Same returns existing; different raises `WriteOnceViolationException` |
| TC-TE-012-13 | X10 | Security | RW-REFADM user (no Documents C) calls upload | 403 MSG-P4-002 |
| TC-TE-012-U1 | BR1, BR7, AC9, AC12 | Unit | Storage stub returning immutable, conflict and timeout; same and different hash | Mapper raises the right exception; guard returns the existing blob or raises a violation; readiness names the missing item |

## Guardrails

- No business value in code: retention period, soft delete days, container names and policy lock state
  come from template parameters and environment properties.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only; test files
  are synthetic.
- No account key, connection string or shared access signature in code, configuration or the pipeline.
- No read of another module's tables. The storage package holds no business data.

## Out of scope

- Choosing the container per document type and writing the document row (RWB-E1-024).
- Retention classes, archive and the retention job (RWB-E1-041, JOB-17).
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- Backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-003 | Legal document types held in a write-once container that cannot be altered or deleted | Business Requirements Program, section 5.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40 | TC-TE-012-01..03, 09, 12 |
| REQ-DCM-002 | The document hub is the system of record; no other store holds the authoritative copy | Business Requirements Program, section 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | None | TC-TE-012-04..08, 10, 11, 13 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1; SPEC-003 | Is the legal retention period 3,650 days? | Sets the immutability policy length. | Assumed at 3,650 days to match LEGAL10Y until the bank retention schedule arrives (DL26). It is a template parameter. | RESOLVED | SPEC-003 |
| CLAR-002 | BR6; SPEC-004 | Is the soft-delete window 30 days? | Sets restore ability in the standard container. | Assumed at 30 days (DL27); template parameter `softDeleteDays`. | RESOLVED | SPEC-004 |
| CLAR-003 | BR1; SPEC-003 | Is the policy locked outside PROD? | Test data could not be removed if locked. | Locked in PROD only; unlocked in DEV, SIT and UAT (story BR1). | RESOLVED | SPEC-003 |
| CLAR-004 | API assessment; SPEC-016 | Does the storage layer need an API of its own? | Would add a contract. | No. It supplies the upload endpoint built in RWB-E1-026; no endpoint is added. | RESOLVED | SPEC-016 |
| CLAR-005 | BR5; SPEC-007 | What happens when the feature flag is off? | Determines write behaviour. | Readiness reports not ready and every write is refused with 503; nothing is written outside the write-once container (story §13). | RESOLVED | SPEC-007, SPEC-015 |
| CLAR-006 | AC1, AC2; SPEC-008 | Where is a refused change recorded? | Audit evidence. | The ACE audit log event `DOCUMENT_CHANGE_REFUSED` with the document ID and the caller (story AC1, AC2). | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story or the named decision log
entries. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this infrastructure enabler.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New storage containers, write-once policy and managed-identity access; no screen and no contract change; the upload endpoint is reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: infrastructure enabler with no endpoint of its own]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 12 acceptance criteria, 10 exception paths and 5 storage/readiness states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
