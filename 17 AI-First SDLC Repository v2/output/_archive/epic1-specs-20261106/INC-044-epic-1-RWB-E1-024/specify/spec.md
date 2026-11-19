# Technical Specification — RWB-E1-024 Document store and index

| Field | Value |
|---|---|
| Story | RWB-E1-024 — Document store and index |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-044-epic-1-RWB-E1-024` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-014); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 024 Document store and index v1.md`; FSD P5 A2.1, A2.2; TSD P5 T3.1, T-A |
| Upstream IDs | BRD-RWB-005; FR-RWB-014; BR-RWB-010; REQ-DCM-001, 002, 003, 008; US-RWB-E1-024; CTX-FEATURE-005; CTL-09, CTL-12; NFR-029; DL11, DL27 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — adds the `DocumentDetailPanel` opened from SCR-30 Case documents: loading, panel with metadata, extracted fields and versions, and error state. No new route. |
| Logic In Scope | `YES` — validation, type lookup, duplicate detection, decision log write, store transaction, post-commit copy, write-once refusal, versioning and scope checks. |
| API In Scope | `YES` — three document endpoints are new to the build: `GET /documents/{documentId}`, `GET /documents/{documentId}/content`, `POST /documents/{documentId}/versions`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `document` and `document_field` (created by RWB-E1-001); `document_hub_parameter` (created here); `CaseDirectory` (P3); `DecisionLogWriter` (P7); `DocumentStorage` (RWB-TE-012); document type table (RWB-E1-025); SCR-30 (RWB-E1-026). |
| New Nodes Required | `YES` — `DocumentHubController` (document endpoints), `DocumentStore`, `DocumentStoreService`, `DocumentHubRepository`, `DocumentEntity`, `DocumentFieldEntity`, `DocumentTypeReader`, `DocumentHubParameters`, `CopyPendingStep`, `DocumentDetailPanel`. |
| Inherited Existing Behavior | Tables and module boundary (RWB-E1-001); containers and managed identity (RWB-TE-012); cases and `CaseDirectory` (RWB-E1-018); decision log writer (RWB-E1-027); document types (RWB-E1-025); upload screen and list (RWB-E1-026). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every document is held against one case, with type, source, stored date and extracted fields. | SPEC-RWB-E1-024-001, SPEC-RWB-E1-024-002 | DIRECT | `case_id`, `document_type`, `source`, `created_at`; fields in `document_field`. | COVERED |
| BR2 | The document hub is the system of record; the file is held only in the hub containers. | SPEC-RWB-E1-024-001, SPEC-RWB-E1-024-007 | DIRECT | Row and blob written by this service; no other store holds the file. | COVERED |
| BR3 | The write-once flag and retention class come from the type table version in force, never from the caller. | SPEC-RWB-E1-024-003 | DIRECT | `DocumentTypeReader` reads the version in force; caller values are ignored. | COVERED |
| BR4 | A write-once document is never deleted or changed; a change is a new version. | SPEC-RWB-E1-024-008 | DIRECT | `WriteOnceViolationException`; 409 MSG-P5-002; audit event. | COVERED |
| BR5 | File types and the size limit are parameters. | SPEC-RWB-E1-024-004 | DIRECT | `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB` in `document_hub_parameter`. | COVERED |
| BR6 | A store with the same case, type and hash returns the existing document. | SPEC-RWB-E1-024-005 | DIRECT | Unique partial index on active rows; return existing ID. | COVERED |
| BR7 | Only the latest version of a document takes a new version. | SPEC-RWB-E1-024-009, SPEC-RWB-E1-024-010 | DIRECT | `is_active` and `doc_version`; 409 MSG-P5-025. | COVERED |
| BR8 | A store that cannot be written to the decision log does not proceed. | SPEC-RWB-E1-024-006 | DIRECT | `DecisionLogWriter.write` before insert; rollback on failure. | COVERED |
| BR9 | Every read checks role, capability area and scope, and is written to the access log. | SPEC-RWB-E1-024-014 | DIRECT | Spring Security method check; ACE PII access log. | COVERED |
| AC1 | A court notice is stored with case, type, source, version 1 and today's date; `black_case_no` is indexed; the file is in `rwb-docs-legal`; `DocumentStored` is written; content returns the same hash. | SPEC-RWB-E1-024-001, SPEC-RWB-E1-024-006, SPEC-RWB-E1-024-007, SPEC-RWB-E1-024-012, SPEC-RWB-E1-024-018 | DIRECT | Full store path. | COVERED |
| AC2 | Delete and content replace of a write-once document are refused through the service and the container; hash and row unchanged; `DOCUMENT_CHANGE_REFUSED` for each attempt. | SPEC-RWB-E1-024-008 | DIRECT | Service refusal plus storage policy. | COVERED |
| AC3 | An appraisal report carries `GENERAL05Y`, write-once false and is stored in `rwb-docs`. | SPEC-RWB-E1-024-003, SPEC-RWB-E1-024-007 | DIRECT | Type lookup drives container. | COVERED |
| AC4 | A new version is `doc_version 2` with `previous_version_id`; version 1 is inactive but readable; the detail lists both versions. | SPEC-RWB-E1-024-009, SPEC-RWB-E1-024-012 | DIRECT | New row; earlier row `is_active=false`. | COVERED |
| AC5 | Type `BANK_STATEMENT` is refused with 422 MSG-P5-006; no row, log or event. | SPEC-RWB-E1-024-003 | DIRECT | Type not in the version in force. | COVERED |
| AC6 | A Word file renamed `.pdf` is refused with 415 MSG-P5-001; nothing written. | SPEC-RWB-E1-024-004 | DIRECT | Content-signature check, not extension. | COVERED |
| AC7 | 26,214,400 bytes is stored; 26,214,401 bytes is refused with 413 MSG-P5-017 showing 25 MB. | SPEC-RWB-E1-024-004 | DIRECT | Boundary uses `<=` on bytes. | COVERED |
| AC8 | The same file, type and case returns the existing document ID; one row, one log entry, one event. | SPEC-RWB-E1-024-005 | DIRECT | Duplicate check before the transaction. | COVERED |
| AC9 | Two simultaneous versions: one 200 at version 3, one 409 MSG-GEN-004; exactly one version 3 row. | SPEC-RWB-E1-024-011 | DIRECT | Optimistic `version` column; unique latest. | COVERED |
| AC10 | A version added to an inactive version is refused with 409 MSG-P5-025; no row. | SPEC-RWB-E1-024-010 | DIRECT | Latest-version check. | COVERED |
| AC11 | Copy failure leaves `COPY_PENDING`; content returns 503 MSG-GEN-006; the next JOB-12 copies and sets `STORED`. | SPEC-RWB-E1-024-007, SPEC-RWB-E1-024-013 | DIRECT | `CopyPendingStep`; state gate on content. | COVERED |
| AC12 | A phone collector outside scope gets 403 MSG-P4-003; no metadata or content. | SPEC-RWB-E1-024-014 | DIRECT | Scope filter on the case. | COVERED |
| X1 | Delete or replace of a write-once document. | SPEC-RWB-E1-024-008 | DIRECT | Refused; audit; MSG-P5-002. | COVERED |
| X2 | Type not in the table in force. | SPEC-RWB-E1-024-003 | DIRECT | 422 MSG-P5-006. | COVERED |
| X3 | Content is not PDF, JPG or PNG. | SPEC-RWB-E1-024-004 | DIRECT | 415 MSG-P5-001. | COVERED |
| X4 | File above `INTAKE_MAX_FILE_MB`. | SPEC-RWB-E1-024-004 | DIRECT | 413 MSG-P5-017. | COVERED |
| X5 | Same file, type and case stored again. | SPEC-RWB-E1-024-005 | DIRECT | Existing returned; no second row. | COVERED |
| X6 | Two users add a version at the same time. | SPEC-RWB-E1-024-011 | DIRECT | 409 MSG-GEN-004; one version. | COVERED |
| X7 | Version added to a superseded document. | SPEC-RWB-E1-024-010 | DIRECT | 409 MSG-P5-025. | COVERED |
| X8 | Copy to the container fails after commit. | SPEC-RWB-E1-024-007, SPEC-RWB-E1-024-013 | DIRECT | `COPY_PENDING`; 503 on content; retry. | COVERED |
| X9 | Reader's scope excludes the case. | SPEC-RWB-E1-024-014 | DIRECT | 403 MSG-P4-003. | COVERED |
| X10 | Caller lacks the Documents right. | SPEC-RWB-E1-024-014 | DIRECT | 403 MSG-P4-002. | COVERED |
| X11 | Decision log write fails. | SPEC-RWB-E1-024-006 | DIRECT | Nothing stored; MSG-P7-003; incident. | COVERED |

## User story intent interpretation

As a **litigation officer (RW-LITOFF)**, I want **every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept**, so that **I find a document by case ID, type and date, and a legal document cannot be changed after it is stored**.

The story builds the single store that every later document path uses: upload, OCR intake and generation. It writes one document record per file, the file to the correct container, the extracted fields to the index, and a decision log entry before the change. It adds the detail panel on SCR-30 and the three read/version endpoints. It does not build the upload form or the case document list; RWB-E1-026 does that.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `DocumentStore.store` from the upload service (RWB-E1-026) or intake (RWB-E1-032); `addVersion` from a user with Documents U; a read from SCR-30. |
| Preconditions | RWB-E1-001 tables exist; RWB-TE-012 containers and managed identity ready; RWB-E1-018 cases and `CaseDirectory`; RWB-E1-025 type table in force; RWB-E1-027 `DecisionLogWriter`; parameters `INTAKE_ALLOWED_TYPES=PDF,JPG,PNG` and `INTAKE_MAX_FILE_MB=25` (assumed; DL11); `rwb.dochub.store` flag on. |
| Input | Case ID, document type, source, file in the intake container, SHA-256 hash, extracted fields, optional party ID; for a version: document ID, file, reason, actor. |
| Output | `document` row with `doc_version` and state; `document_field` rows; `DOCATT` decision log entry; `DocumentStored` outbox event; `storage_ref`; content. |
| Feature flag | `rwb.dochub.store`. Off: the endpoints return 404 and `DocumentStore.store` refuses with a feature-off error. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document` | `case_id` | Store request | System writes | Must exist through `CaseDirectory` |
| `document` | `party_id` | Store request | System writes | Optional |
| `document` | `document_type` | Store request | System writes | Must be in the type table version in force |
| `document` | `source` | Store request | System writes | `LOV-DOC-SOURCE` |
| `document` | `storage_ref` | `BlobStorageAdapter` | System writes | `{container}/{caseId}/{documentId}/v{docVersion}` |
| `document` | `retention_class`, `write_once` | Type table in force | System writes | Never taken from the caller |
| `document` | `doc_version` | Store / version | System writes | 1 on store; n+1 on a new version |
| `document` | `previous_version_id` | Version request | System writes | Null on version 1; current row on n+1 |
| `document` | `content_sha256` | File | System writes | 64 hex characters; compared on duplicate and read |
| `document` | `state` | Store | System writes | `COPY_PENDING` then `STORED` |
| `document` | `is_active` | Store / version | System writes | True on the latest row; false on a superseded row |
| `document_field` | `field_name`, `field_value`, `confidence`, `extracted_value`, `extractor_version` | Store request | System writes | One row per extracted field |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Store | Validation and duplicate check pass | `COPY_PENDING` | Row, fields, `DOCATT` log, `DocumentStored` |
| `COPY_PENDING` | Blob copy succeeds | Container accepts the write | `STORED` | `storage_ref` set; content readable |
| `COPY_PENDING` | Blob copy fails | Container refuses or times out | `COPY_PENDING` | Content returns 503 MSG-GEN-006; JOB-12 retries |
| Active version n | Add version | Caller holds Documents U and n is latest | New row n+1 active | Row n `is_active=false`; n+1 `previous_version_id=n` |
| Active version n | Add version | Two requests at once | One succeeds; one 409 | One row n+1; MSG-GEN-004 for the loser |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Delete or replace a write-once document | Refused; row and hash unchanged; `DOCUMENT_CHANGE_REFUSED` | MSG-P5-002 |
| X2 | Type not in force | 422; nothing written | MSG-P5-006 |
| X3 | Content not PDF, JPG or PNG | 415; nothing written | MSG-P5-001 |
| X4 | File above the limit | 413; nothing written | MSG-P5-017 |
| X5 | Same case, type and hash | Existing document returned | None |
| X6 | Concurrent version requests | One 200; one 409; one new row | MSG-GEN-004 |
| X7 | Version on a superseded row | 409; no row | MSG-P5-025 |
| X8 | Copy fails after commit | `COPY_PENDING`; content 503; JOB-12 retries | MSG-GEN-006 |
| X9 | Case outside scope | 403; nothing returned | MSG-P4-003 |
| X10 | Role lacks the Documents right | 403; nothing returned | MSG-P4-002 |
| X11 | Decision log write fails | Nothing stored; incident | MSG-P7-003 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints | `GET /api/recovery/v1/documents/{documentId}` (API-P5-003); `GET /api/recovery/v1/documents/{documentId}/content` (API-P5-004); `POST /api/recovery/v1/documents/{documentId}/versions` (API-P5-005). |
| Contract delta | The `Document` response carries `storedAt`, `previousVersionId` and `versions` (array of `DocumentVersion`); the version request is multipart `file` plus `reason`. Both are already written into API specification v2, so no new contract authoring is required. |
| Backward compatibility | Additive; no existing field changes meaning. |
| Authorization | Documents R for reads; Documents U for a version; scope applied on every call. 401 MSG-P4-001; 403 MSG-P4-002/MSG-P4-003; 404; 409 MSG-P5-025/MSG-GEN-004; 413 MSG-P5-017; 415 MSG-P5-001; 503 MSG-GEN-006/MSG-P7-003. |
| Versioning | No API version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-008; SPEC-RWB-E1-024-016 | New `DocumentDetailPanel` with loading, panel, version list, download and error states. | Component tests: loading; metadata and field render; version list order; write-once label and no edit control; 403/503 error message; download action. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001..003, 008; SPEC-RWB-E1-024-001..018 | New service, repository, reader, parameters, copy step and three endpoints. | Store happy path; unknown type; content signature; size boundary; duplicate; write-once refusal; version latest rule; concurrency; copy pending; scope and right refusal; decision log failure. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DocumentHubController` | Controller | GET document, GET content, POST versions; maps exceptions to problem responses with the message ID. |
| `DocumentStore` | Published interface | `store`, `addVersion`, `delete`, `replaceContent`, `findById`; used by RWB-E1-026, RWB-E1-032 and the retention job. |
| `DocumentStoreService` | Service | Validation, type lookup, duplicate check, decision log write, insert, outbox event and version rules. |
| `DocumentHubRepository` | Repository | Reads and writes `document` and `document_field` only. |
| `DocumentEntity`, `DocumentFieldEntity` | Entity | Map the tables with the optimistic `version` column. |
| `DocumentTypeReader` | Repository | Reads the document type version in force (table from RWB-E1-025). |
| `DocumentHubParameters` | Rule table | Reads `document_hub_parameter` rows in force, cached 5 minutes. |
| `DocumentStorage` | Published interface | From RWB-TE-012; writes, opens and refuses overwrite; called, never reimplemented. |
| `CopyPendingStep` | Job | Step of JOB-12 that retries copies for rows in `COPY_PENDING`. |
| `DocumentDetailPanel` | React component | Opens from SCR-30; metadata, extracted fields, versions and download. |

### Package and boundaries

Folder `recovery/dochub/store`, Java package `recovery.dochub.store`; front-end folder
`recovery/documents`. The service reads the case only through `CaseDirectory`, writes the decision log
only through `DecisionLogWriter`, and stores blobs only through `DocumentStorage`. No module reads
another module's tables.

### Data and migration

Flyway `V1_5_024__document_store.sql` adds `document.previous_version_id uuid` (FK to `document(id)`)
and `document.content_sha256 char(64) not null`; creates `document_hub_parameter` (`id`, `param_code
varchar(40)`, `param_value varchar(200)`, `unit varchar(20)`, `table_version varchar(20)`, `valid_from`,
`valid_to`, `load_id`, standard columns) with unique (`param_code`, `table_version`). Indexes:
`ix_document_case_type_created` on (`case_id`, `document_type`, `created_at`); unique partial
`uk_document_case_type_hash` on (`case_id`, `document_type`, `content_sha256`) where `is_active`;
`ix_document_previous_version` on (`previous_version_id`).

### Store flow

1. Resolve the case through `CaseDirectory`; refuse if absent.
2. Read the type row from the version in force: `write_once`, `retention_class`, `table_version`.
3. Check the content signature against `INTAKE_ALLOWED_TYPES` and the size against `INTAKE_MAX_FILE_MB`.
4. Look for an active document on the case with the same type and hash; return it and stop.
5. In one transaction: write the `DOCATT` decision log entry (`final_call=STORED`), insert the document
   row with `doc_version=1` and state `COPY_PENDING`, insert the field rows, write `DocumentStored` to
   the outbox.
6. After commit, call `DocumentStorage.store`; set `storage_ref` and state `STORED`.
7. If the copy fails, leave `COPY_PENDING`; `CopyPendingStep` retries on the next JOB-12 run.

### Duplicate and idempotency

- Duplicate key: case ID + document type + content hash, active rows only. A superseded version does
  not block a re-upload of the same file.
- A duplicate returns the existing document ID with no second row, decision log entry or event.
- The version endpoint accepts an `Idempotency-Key`; a repeat with the same key returns the first result.

### Versioning

- A version inserts a new row with `doc_version = current + 1` and `previous_version_id = current id`.
- The earlier row becomes `is_active=false`; its blob and metadata stay readable.
- A version on a row that is not the latest returns 409 MSG-P5-025.
- The optimistic `version` column detects a concurrent change; the loser gets 409 MSG-GEN-004.
- `GET /documents/{documentId}` returns the requested version with its version list; `GET content`
  returns the content of the requested version.

### Write-once and audit

`delete` and `replaceContent` check `write_once` before calling storage; a write-once document raises
`WriteOnceViolationException`, mapped to 409 MSG-P5-002. A direct container attempt is refused by the
storage policy (RWB-TE-012). Each attempt writes `DOCUMENT_CHANGE_REFUSED` with the document ID and the
caller. No endpoint exposes delete or replace in Epic 1.

### Reads, access and the detail panel

- `GET /documents/{documentId}` returns metadata, extracted fields and versions.
- `GET content` returns the file of that version; while `COPY_PENDING` it returns 503 MSG-GEN-006.
- The stored date is `document.created_at`; the content response hash equals `content_sha256`, so a
  reader can verify the file against the row (SPEC-018).
- Every read checks Documents R and the case scope; the ACE common module writes the PII access log.
- `DocumentDetailPanel` states: Loading; panel with metadata, fields and versions; Error with the
  message from the contract. A write-once document shows the label "Write once" and no edit control.

### Transaction and events

One transaction per store and per version. `DocumentStored` (EV-16) carries `documentId`, `caseId`,
`type` and `source`, written to the outbox in the same transaction. The outbox publisher delivers it
with retry and idempotency.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR | Documents C; stores intake documents | All |
| RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and other roles with Documents C | Store through upload | Own/team |
| Roles with Documents U (RW-CASEOWN, RW-LITOFF, RW-LEGAL, RW-COMPLY) | Add a version | Own/team |
| Roles with Documents R (RW-TEAMMGR, RW-AUDIT, RW-PHONECOL) | Read metadata and content | Own/team |
| SY-DECLOG | Writes the `DOCATT` entry | All |
| Nobody | Deletes or changes a write-once document | — |

### Observability and operations

- Metrics: stores, duplicates, validation refusals by reason, versions, copy-pending count, copy
  failures, content reads, access refusals.
- Alerts: copy-pending older than one JOB-12 cycle; decision log failure; storage unavailable.
- Logs carry document ID, case ID and counts; no file name, field value or personal data.
- Run book: retry copy, rereun JOB-12, check container readiness.

### Performance

- Store target: a 1.2 MB PDF stored and listed within 2 seconds in SIT (story "Done when").
- One indexed duplicate lookup; one insert batch; one blob write after commit.
- `ix_document_case_type_created` serves the case/type/date list.
- Content reads stream from storage; no full-file load into memory.

### Feature flag and rollback

- `rwb.dochub.store`. Off: the endpoints return 404 and `store` refuses with a feature-off error.
- Rollback: turn the flag off; redeploy the previous tag. The migration is forward-only; added columns
  are nullable or defaulted and harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-024-01 | AC1, BR1, BR2 | System | Synthetic court notice PDF on `RW-2026-000123` | Row, field, legal blob, `DocumentStored`, hash match |
| TC-E1-024-02 | AC2, BR4 | System | Stored court notice; delete and replace via service and container | Both refused; hash and row unchanged; audit each |
| TC-E1-024-03 | AC3, BR3 | System | Synthetic appraisal report | `GENERAL05Y`, write-once false, `rwb-docs` |
| TC-E1-024-04 | AC4, BR7 | System | Appraisal report plus a second file | v2 active; v1 inactive and readable; both listed |
| TC-E1-024-05 | AC5, BR3 | System | Type `BANK_STATEMENT` | 422 MSG-P5-006; nothing written |
| TC-E1-024-06 | AC6, BR5 | System | Word file renamed `.pdf` | 415 MSG-P5-001; nothing written |
| TC-E1-024-07 | AC7, BR5 | System | PDFs of 26,214,400 and 26,214,401 bytes | First stored; second 413 MSG-P5-017 |
| TC-E1-024-08 | AC8, BR6 | System | Same file stored twice | Existing ID; one row, log and event |
| TC-E1-024-09 | AC9 | System | Two parallel version requests | One 200 at v3; one 409 MSG-GEN-004; one row |
| TC-E1-024-10 | AC10, BR7 | System | Version request on inactive v1 | 409 MSG-P5-025; no row |
| TC-E1-024-11 | AC11 | System | `rwb-docs` refuses writes | `COPY_PENDING`; content 503; retry sets `STORED` |
| TC-E1-024-12 | AC12, BR9 | System | Phone collector, scope OWN, another owner's case | 403 MSG-P4-003; nothing returned |
| TC-E1-024-13 | X10 | Security | RW-CAPACITY (no Documents right) reads a document | 403 MSG-P4-002 |
| TC-E1-024-14 | X11 | Resilience | Decision log write forced to fail | Nothing stored; MSG-P7-003 |
| TC-E1-024-U1 | BR3, BR6, BR7, AC5, AC8, AC10 | Unit | Unknown type; duplicate active row; inactive version; concurrent update | 422; existing returned; 409 MSG-P5-025; 409 MSG-GEN-004; one new row |

## Guardrails

- No business value in code: file types, size limit, write-once flag, retention class and container
  names are data rows or properties.
- No personal data in logs, tests or prompts. Test files are synthetic; extracted values in logs are
  replaced by the field name.
- No read of another module's tables: the case is read through `CaseDirectory`, the decision log is
  written through `DecisionLogWriter`.
- The service never overwrites a blob; every version is a new blob path.
- The PII access log entry for each read is written by the ACE common module, never by this package.

## Out of scope

- The upload form, the case document list and the search within a case (RWB-E1-026).
- Classification, field extraction and automatic attach from the OCR intake (RWB-E1-050, RWB-E1-053,
  RWB-E1-032).
- Confirming or correcting an extracted field with `PATCH /documents/{documentId}/fields/{fieldId}`
  (RWB-E1-054).
- Retention periods, the retention job and the virus scan (RWB-E1-041).
- Container creation, backup and restore tests (RWB-TE-012; REQ-DCM-015).
- Custody of originals (Epic 2, SCR-32) and electronic discovery (Epic 2, REQ-DCM-017).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | Business Requirements Epic 1, section 3.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-024-01, 03, 05, 08 |
| REQ-DCM-002 | The document hub is the system of record | Business Requirements Epic 1, section 3.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-024-01, 11, 14 |
| REQ-DCM-003 | Legal types held write-once | Business Requirements Epic 1, section 3.5 | FEAT-DCM-01 | L2 13.3 Store and retain documents | None | TC-E1-024-02, 04, 09, 10 |
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | Business Requirements Epic 1, section 3.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | None | TC-E1-024-01, 06, 07, 12, 13 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-006 | Is `DOCATT` the approved decision code? | Decision log content. | Assumed `DOCATT` (story §13); the `LOV-DECISION` list is loaded by the data steward. | RESOLVED | SPEC-006 |
| CLAR-002 | BR6; SPEC-005 | Does the duplicate check include superseded versions? | Would block a re-upload after versioning. | No: the unique partial index covers active rows only, so a superseded version does not block the same file. | RESOLVED | SPEC-005 |
| CLAR-003 | AC1; SPEC-018 | What is the "stored date"? | Search and display. | The document `created_at` timestamp, as used by RWB-E1-026. | RESOLVED | SPEC-018 |
| CLAR-004 | Flow step 7; SPEC-007 | Is the blob written before or after the commit? | Crash behaviour. | After commit; a failed copy leaves `COPY_PENDING` and is retried by JOB-12 (AC11). | RESOLVED | SPEC-007 |
| CLAR-005 | AC11; SPEC-013 | What does a content read return while the copy is pending? | User-visible behaviour. | 503 MSG-GEN-006 naming Document storage; no partial file. | RESOLVED | SPEC-013 |
| CLAR-006 | Authority; SPEC-008 | May a non-write-once document be deleted in Epic 1? | Scope of the interface methods. | No endpoint exposes delete or replace in Epic 1. The methods exist for the published interface and are specified only for the write-once refusal; non-write-once deletion is out of scope. | RESOLVED | SPEC-008 |
| CLAR-007 | API assessment; SPEC-012 | Are the three endpoints a contract change? | API impact classification. | They are new to the build, and API specification v2 already carries `storedAt`, `previousVersionId` and `versions`; no new contract authoring is required. | RESOLVED | SPEC-012 |
| CLAR-008 | TSD T3.1; SPEC-001 | Is `party_id` required? | Store request validation. | No; the TSD marks it optional and the story does not require it. | RESOLVED | SPEC-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the API specification or
the named decision log entries. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-30 screen specification; no Figma source.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New document store, index, versioning and detail panel; three document endpoints new to the build, contract already in API specification v2.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new store and version endpoints plus a new detail panel]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 12 acceptance criteria, 11 exception paths and 5 document states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
