# RWB-P5-E1024-APP Document store and index

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-024 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1025-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1025-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON, RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-001, FR-P5-002, FR-P5-003, FR-P5-004, FR-P5-005, FR-P5-006, FR-P5-007, FR-P5-008, FR-P5-009, FR-P5-010, FR-P5-013, FR-P5-014, FR-P5-028, FR-P5-029, FR-P5-030, FR-P5-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the store and index moved into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1` and the `DocumentIntakeWorkflow` template of the target service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept**, so that **I find a document by case ID, type and date, and a legal document cannot be changed after it is stored**.

Inside `rwb-document` this is the store and index capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The store is the only writer of the document tables. It writes `document`, `document_field` and the document-hub parameter rows, reads the document type table of RWB-P5-E1025-APP, and writes the decision record (DP-03) and the outbox row (DP-09) in the same transaction as the document row.
- The file goes to Azure Blob with WORM through the platform storage product RWB-PLT-TE012-APP (the X dependency), never through a local file write: containers `rwb-docs` (standard), `rwb-docs-legal` (write-once) and `rwb-quarantine` (intake holds), reached by managed identity at `{container}/{caseId}/{documentId}/v1`. This service never overwrites a blob; every version is a new blob path. The storage account and the immutability policy of the containers are RWB-PLT-TE012-APP's and are Not specified in the source documents (GAP-1031; ASM-1979).
- The case is read through the `GET /cases/{caseId}` contract of `rwb-case` (RWB-P3-E1018-CON, a C dependency, DP-11, one hop, 2 s timeout), never from a case table of another service and never from a `rwb_case` copy.
- The decision is recorded through the local decision-record library of DP-03 (H RWB-PLT-E1027-CON; the central ledger contract of `rwb-decision` is RWB-P7-E1027-CON) in the same transaction as the document row and the outbox row, with decision code DOCATT and final call STORED; a failed record means nothing is stored (MSG-P7-003, R-UNI-39).
- Parameters `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON). The document-hub rows they resolve to live in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5.
- Reference lists LOV-RETENTION, LOV-REVIEW, LOV-DOC-TYPE and LOV-DOC-SOURCE are read through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); no list value is typed in code.
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1030; ASM-1978); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, exception paths, business rules, messages, authority, data fields, twelve acceptance criteria and fourteen test cases, adapted to the target service's schema, topic, API base and workflow template.

### 2. Business rationale

Recovery documents are held today in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit (FSD P5 A1.3). This story builds the store and the index that every other document story writes to: one document record in the Workbench document hub per file, the file in blob storage, legal types write-once (DT06, ADR-007, control CTL-12). It meets REQ-DCM-001, REQ-DCM-002, REQ-DCM-003 and REQ-DCM-008. The module measure is fields extracted without review (FSD P5 A2.1.1), which can only be counted once every document is indexed against its case.

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). No table of another service is read and no monolith table name survives.
2. The case arrives through the `rwb-case` contract `GET /cases/{caseId}` with a mock and a 2 s timeout (DP-11), so the store builds against a published shape and never against a `rwb_case` table.
3. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the row and the outbox row and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger.
4. The parameters come from the parameters contract and client library of `rwb-case` (DP-06); the document-hub parameter rows themselves stay in `rwb_document`, which is P5's own store for them. The reference lists come from the reference-data contract (DP-07).
5. The document type table of RWB-P5-E1025-APP is a P5 table read locally in the version in force (`valid_from` and `valid_to`), with no contract hop: the write-once flag, the retention class and the field list of a type are never taken from the caller.
6. The retry of a pending copy becomes the `copyPending` activity of the `DocumentIntakeWorkflow` template of the workflow kit (DP-10), not a Quartz job step.
7. The file is written to Blob WORM through the platform storage product RWB-PLT-TE012-APP; this service holds the reference and the hash, never a copy of the bytes in its own store.
8. The store reads reach the case documents screen through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the migration is one step in the per-service Flyway sequence (DP-15).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1027-CON | The decision-record library: `RecordAndApply` writes the DOCATT record inside the caller's transaction and publishes it on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1042-CON | The parameters client library, so `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` are read through a published shape (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-RETENTION, LOV-REVIEW, LOV-DOC-TYPE and LOV-DOC-SOURCE (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library; the DocumentStored row is written in the store transaction (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 `DocumentIntakeWorkflow` template, activity registration and retry policy (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the store migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the store reads to SCR-30 (DP-19) |
| RWB-P5-E1025-APP | The document type table `document_type` with version DOCTYPE-2026.11 in force, the write-once flag, the retention class and the field list of each of the six types |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the two intake parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the four lists (DP-07) |
| RWB-P7-E1027-CON | The central decision ledger contract that collects the local record (DP-03) |
| RWB-P3-E1018-CON | The `rwb-case` contract `GET /cases/{caseId}`, with its fake, so the case is read in one hop with a 2 s timeout (DP-11) |
| RWB-PLT-TE012-APP | The platform storage product: the Blob containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, the managed identity and the WORM policy (the X dependency) |

Business preconditions carried from RWB-E1-024:

- Document type table version DOCTYPE-2026.11 is in force with the six types, the write-once flag and the retention class of each type (RWB-P5-E1025-APP).
- Document hub parameters loaded: `INTAKE_ALLOWED_TYPES` = PDF, JPG, PNG; `INTAKE_MAX_FILE_MB` = 25, assumed (DL11). RWB-E1-053 and RWB-E1-057 read the same parameters through the same contract.
- The caller is the upload path (RWB-P5-E1026-APP, user with Documents C) or the intake (SY-OCR). A reader holds Documents R with the case in scope.
- The feature flag `rwb.document.store` is on. The legacy flag name `rwb.dochub.store` is retired with the monolith.

The storage account name and the immutability policy of the containers are Not specified in the source documents (GAP-1031; ASM-1979). The database login name is Not specified in the source documents (GAP-1030; ASM-1978).

### 4. Flow

1. Caller: calls the store command with the case ID, the document type, the source, the file reference in the intake container, its SHA-256 hash and any extracted fields. The upload path reaches it through `POST /documents`, which returns the upload link; the intake path reaches it through the same store command (12.1).
2. `DocumentStoreService`: reads the case through the `rwb-case` contract `GET /cases/{caseId}` (DP-11, one hop, 2 s timeout) and refuses the call if the case does not exist or the contract does not answer.
3. `DocumentStoreService`: reads the type row from `document_type` in the version in force (`valid_from` and `valid_to`): `write_once`, `retention_class` and the field list (RWB-P5-E1025-APP).
4. `DocumentStoreService`: checks the file type by its content signature and the file size against `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB`, read through the parameters contract and client library (DP-06).
5. `DocumentStoreService`: looks for an active document on the case with the same type and hash; if one exists it returns it and stops, with no second row, entry or event.
6. `DocumentStoreService`, one transaction in `rwb_document`: writes the decision record (decision code DOCATT, final call STORED) through the decision-record library of DP-03, inserts the `document` row with `doc_version` 1 and state COPY_PENDING, inserts the `document_field` rows, and writes the `rwb.document.DocumentStored.v1` row to the outbox. A failed record aborts the transaction: nothing is stored and MSG-P7-003 is returned.
7. `copyPending` activity of `DocumentIntakeWorkflow`, after commit: calls the storage product RWB-PLT-TE012-APP, which writes the file to `rwb-docs-legal` when `write_once` is true and to `rwb-docs` otherwise, at `{container}/{caseId}/{documentId}/v1`; the service sets `storage_ref` and state STORED. A failure leaves the row COPY_PENDING for the next run.
8. User with Documents R: opens the document from the case documents screen (SCR-30) through the gateway-bff composite route (DP-19); `GET /documents/{documentId}` returns the metadata, the extracted fields and the version list; `GET /documents/{documentId}/content` returns the file. The ACE common module writes each read to the PII access log, never this package.
9. User with Documents U: adds a version with `POST /documents/{documentId}/versions`; the service inserts a new `document` row with `doc_version` n+1 and `previous_version_id` set to the current row, and marks the earlier row `is_active` = false. The earlier version stays readable, and its blob path is untouched.
10. Outbox relay: publishes `rwb.document.DocumentStored.v1` to `rwb.document.events.v1` and the decision record to `rwb.decision-record.v1`; the event is published once per committed store, keyed by caseId, and carries no personal data.

The decision record is written before the change takes effect and in the same transaction as the document row and the outbox row, so a failure leaves all three unchanged (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Delete or content replace of a write-once document, through the service or directly on the container | Refused; the file and the row are unchanged; an audit event DOCUMENT_CHANGE_REFUSED is written for each attempt | MSG-P5-002 | AC2 |
| X2 | Document type not in the type table in force | Refused with 422; nothing stored | MSG-P5-006 | AC5 |
| X3 | File content is not PDF, JPG or PNG | Refused with 415; nothing stored | MSG-P5-001 | AC6 |
| X4 | File above `INTAKE_MAX_FILE_MB` | Refused with 413; nothing stored | MSG-P5-017 | AC7 |
| X5 | The same file is stored again on the same case with the same type | The existing document is returned; no second row, entry or event | None | AC8 |
| X6 | Two users add a version to the same document at the same time | The first succeeds; the second gets 409; one new version exists | MSG-GEN-004 | AC9 |
| X7 | A version is added to a document that is not the latest version | Refused with 409 | MSG-P5-025 | AC10 |
| X8 | The copy to the container fails after commit | The row stays COPY_PENDING; the copy is retried by the `copyPending` activity of `DocumentIntakeWorkflow`; content reads return 503 until it is stored | MSG-GEN-006 | AC11 |
| X9 | The reader's role scope does not include the case | Refused with 403; nothing is returned | MSG-P4-003 | AC12 |
| X10 | The caller's role lacks the Documents right | Refused with 403 | MSG-P4-002 | TC-E1-024-13 (Access) |
| X11 | The decision record write fails | Nothing is stored; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-024-14 (Principle 5) |
| X12 | The `rwb-case` contract does not answer within 2 s, or the breaker is open | Refused with 503; nothing is stored; the circuit breaker shields the case service | MSG-GEN-006 | TC-E1-024-11 (target path) |
| X13 | The outbox relay is down when the store commits | The row, the fields, the decision record and the outbox row are committed; the event is published by the relay when it recovers, once, with no duplicate store | None | TC-E1-024-08 (target path) |

Two target-service notes:

- A store refused at the contract read (X12) is not retried by the caller's `Idempotency-Key`; a repeat of the same key after the case service recovers returns one stored document, because the duplicate check of step 5 runs before the insert.
- The legacy `delete` and `replaceContent` methods are not REST operations in the target (12.1). The refusal of AC2 is executed against the store command and against the container, and the audit event `DOCUMENT_CHANGE_REFUSED` is written by the store service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the type table (RWB-P5-E1025-APP), the containers (RWB-PLT-TE012-APP), the case contract (RWB-P3-E1018-CON), the decision-record library and the outbox library, all earlier or contract work |
| Negotiable | File types, size limit, write-once flag and retention class are data rows or parameters; the story fixes the behaviour |
| Valuable | Every later document path (upload, OCR intake, generation) stores through this one capability |
| Estimable | One service, four public operations plus one internal store command, one detail panel, one migration |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Document store and index

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given type "COURT_NOTICE" has write_once true and retention class "LEGAL10Y"
    Given type "APPRAISAL_REPORT" has write_once false and retention class "GENERAL05Y"
    Given parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
    Given case "RW-2026-000123" exists with product group "MORTGAGE" in team "MTG-BKK-LIT"
    Given the rwb-case contract mock returns case "RW-2026-000123" with product group "MORTGAGE" in team "MTG-BKK-LIT"

  Scenario: AC1 Stored against case (legacy RWB-E1-024 AC1)
    Given a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN"
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"
    When it is stored
    Then one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today
    Then its extracted field "black_case_no" with value "BC-TEST-0456" is in the index
    Then the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1"
    Then the system writes documentStored to the outbox with the document ID, the case ID, the type and the source
    Then the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash

  Scenario: AC2 Write once (legacy RWB-E1-024 AC2)
    Given the court notice from AC1 is stored with write_once true
    When a delete and a content replace are attempted through the document store and directly on the container
    Then the system refuses each attempt with MSG-P5-002
    Then the file hash and the document row are unchanged
    Then the system writes an audit event "DOCUMENT_CHANGE_REFUSED" for each attempt with the document ID and the caller

  Scenario: AC3 Retention class (legacy RWB-E1-024 AC3)
    Given a document of type "APPRAISAL_REPORT" for case "RW-2026-000123"
    When it is stored
    Then the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11"
    Then write_once is false and the file is in container "rwb-docs"

  Scenario: AC4 A new version keeps the history (legacy RWB-E1-024 AC4)
    Given the appraisal report from AC3 at doc_version 1
    When a user with Documents U adds a new file with reason "Revised valuation"
    Then a document row with doc_version 2 and previous_version_id of version 1 exists and is active
    Then version 1 is inactive and its content is still returned by GET content
    Then GET for version 2 lists versions 1 and 2 with their stored dates and sources

  Scenario: AC5 Unknown document type is refused (legacy RWB-E1-024 AC5)
    Given a file for case "RW-2026-000123" with type "BANK_STATEMENT"
    When it is stored
    Then the system refuses the call with 422 and MSG-P5-006
    Then no document row, decision log entry or event is written

  Scenario: AC6 File type not allowed (legacy RWB-E1-024 AC6)
    Given a file "macro-0001.docx" with Word content for case "RW-2026-000123"
    When it is stored
    Then the system refuses the call with 415 and MSG-P5-001
    Then the system writes nothing to the containers or the tables

  Scenario: AC7 Size limit boundary (legacy RWB-E1-024 AC7)
    Given two PDF files for case "RW-2026-000123" of 26,214,400 bytes and 26,214,401 bytes
    When each is stored
    Then the system stores the file of 26,214,400 bytes
    Then the system refuses the file of 26,214,401 bytes with 413 and MSG-P5-017 showing 25 MB

  Scenario: AC8 The same file stored twice (legacy RWB-E1-024 AC8)
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"
    When the same file with the same hash and type is stored again on that case
    Then the system returns the existing document ID
    Then the case still holds one court notice row, one decision log entry and one DocumentStored event for it

  Scenario: AC9 Two versions added at the same time (legacy RWB-E1-024 AC9)
    Given the appraisal report at doc_version 2
    When two users add a new version at the same time
    Then one request returns 200 with doc_version 3
    Then the other returns 409 with MSG-GEN-004
    Then exactly one row with doc_version 3 exists

  Scenario: AC10 Version on a superseded document (legacy RWB-E1-024 AC10)
    Given the appraisal report version 1 is inactive
    When a user adds a new version to version 1
    Then the system refuses the request with 409 and MSG-P5-025
    Then the system writes no new row

  Scenario: AC11 The storage copy fails (legacy RWB-E1-024 AC11)
    Given container "rwb-docs" refuses writes
    When an appraisal report is stored for case "RW-2026-000123"
    Then the system writes the document row with state "COPY_PENDING"
    Then GET content returns 503 with MSG-GEN-006 naming "Document storage"
    Then when the container accepts writes again the next document intake run copies the file and sets state "STORED"

  Scenario: AC12 Case outside the reader's scope (legacy RWB-E1-024 AC12)
    Given a phone collector with scope OWN who does not own case "RW-2026-000123"
    When the phone collector requests the court notice from AC1
    Then the system refuses the request with 403 and MSG-P4-003
    Then no metadata or content is returned
```

Every Given, When and Then line above is the legacy line unchanged. The cross-service part is mocked by the added Background Given on the `rwb-case` contract and by the `rwb-decision` contract Given in AC1 and AC8. In AC11 the "next document intake run" is the `copyPending` activity of `DocumentIntakeWorkflow`, whose 15-minute Schedule belongs to RWB-P5-E1049-APP (12.6).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document is held against one case, with type, source, stored date and extracted fields | REQ-DCM-001; document.case_id is mandatory |
| BR2 | The document hub is the system of record; the file is held only in the hub containers | DT06; DL27; REQ-DCM-002 |
| BR3 | The write-once flag and the retention class come from the document type table version in force, never from the caller | Document type table (New); principle 1; DT02 |
| BR4 | A write-once document is never deleted or changed; a change is a new version | CTL-12; REQ-DCM-003; NFR-029 |
| BR5 | File types and the size limit are parameters | Document hub parameter table (New); DL11 |
| BR6 | A store with the same case, type and hash returns the existing document | R-UNI-40; events.txt rule Duplicates |
| BR7 | Only the latest version of a document takes a new version | FEAT-DCM-20 |
| BR8 | A store that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | Every read checks role, capability area and scope, and is written to the access log | CTL-09; REQ-ACA-006 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1, BR2 and BR6 are executed in `rwb_document` only: `document` and `document_field` are the index, `storage_ref` points at the WORM blob, and the duplicate check is the unique partial index `uk_document_case_type_hash` plus the pre-insert read of step 5. No foreign schema is read (DP-01); the case arrives through `GET /cases/{caseId}` of RWB-P3-E1018-CON.
- BR3 and BR5 read the type row and the two parameters from the version in force; the type table is P5's own table and the parameters arrive through the `rwb-case` parameters contract (DP-06). Neither the write-once flag, the retention class, the size limit nor the allowed types is written in code.
- BR4 is executed by the store refusing every content change on a write-once document, by the blob path being immutable per version, and by the container's own WORM policy at RWB-PLT-TE012-APP.
- BR7 is executed by the latest-version rule on `doc_version` and `is_active`, with `version` as the optimistic lock.
- BR8 is executed by the decision-record library of DP-03 inside the store transaction: the record, the row, the fields and the outbox row commit together or not at all (R-UNI-39).
- BR9 is executed by the authorisation decision the service template's guard holds and by the ACE common module's PII access log for every read; this package writes no access-log entry.
- DP-07 keeps the four lists in reference data; DP-15 puts the store migration in the per-service Flyway sequence as one step in `rwb_document`; DP-09 puts the event in the outbox inside the same transaction.

### 9. State transitions

No case state machine in this story: the store changes no case status. It sets the document record state (standard column state) and the active flag:

| From | Event | To |
|---|---|---|
| (no row) | store commits with the decision record and the outbox row | `document.state` = COPY_PENDING |
| COPY_PENDING | the `copyPending` activity stores the file and sets `storage_ref` | STORED |
| COPY_PENDING | the copy fails | COPY_PENDING (retried by the next intake run) |
| STORED, `is_active` = true | a new version is added to the latest version | `is_active` = false on the earlier row; the new row is COPY_PENDING then STORED |

A write-once document has no transition out of STORED: no delete, no content replace, no overwrite of its blob path.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Stores documents through the store command (Documents C) |
| RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and the other roles with Documents C | Store through the upload path of RWB-P5-E1026-APP |
| Roles with Documents U (for example RW-CASEOWN, RW-LITOFF, RW-LEGAL, RW-COMPLY) | Add a new version |
| Roles with Documents R (for example RW-TEAMMGR, RW-AUDIT, RW-PHONECOL) | Read metadata and content inside their scope |
| SY-DECLOG, decision record writer | Writes the DOCATT record |
| SY-DOCUMENT, the rwb-document service identity | Runs the copy after commit and writes the audit event for a refused change |
| Nobody | Deletes or changes a write-once document |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds. This story adds no operation and no guard of its own for it: the refusal shape is 403 with MSG-P4-002 or MSG-P4-003, as in the legacy endpoints. Where the legacy guard is replaced by the shared guard library (DP-08) is another story's deliverable; this story inherits it.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-1030; ASM-1978); the story refers to "the rwb-document login (DP-02)".

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Write |
| DF-DOC-025 | `document` | previous_version_id | Write |
| DF-DOC-026 | `document` | content_sha256 | Write |
| Standard column | `document` | state, is_active, version | Write |
| DF-DOC-012 to DF-DOC-017 | `document_field` | id, document_id, field_name, field_value, confidence, confirmed_by | Write |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-222 | `document_type` | write_once | Read |
| DF-REF-223 | `document_type` | retention_class | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-REF-245 | `document_hub_parameter` | param_code | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read |
| DF-CAS-001 | `rwb-case` case, through the contract | id | Read |
| DF-CAS-002 | `rwb-case` case, through the contract | case_no | Read |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, ruleId, finalCall, decidedAt, prev_hash, entry_hash | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_document` | the row for DocumentStored and the decision record | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `rwb_case` row is copied and no ACE view is read by this service: DF-CAS-001 and DF-CAS-002 arrive inside the `rwb-case` contract answer, and DP-01 forbids a foreign-schema read. Personal data never enters the event payload, the workflow input, the decision record or the log; extracted field values in logs are replaced by the field name.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/documents` | P5 | Creates the document in COPY_PENDING with its metadata and returns the upload link for the file; `Idempotency-Key` required. The exact request and response field names are Not specified in the source documents (GAP-1032; ASM-1980) |
| POST | `/api/recovery/document/v1/documents/{documentId}/store` | P5 | The store command the upload and intake paths call: case contract read, type row, signature and size, duplicate check, decision record, row, fields and outbox in one transaction. Internal operation, service identity only. Field names as above |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 | Metadata, extracted fields and the version list; Documents right R with scope applied |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 | The file of that version as `application/octet-stream`; 503 while the state is COPY_PENDING |
| POST | `/api/recovery/document/v1/documents/{documentId}/versions` | P5 | Adds a version to the latest version only; multipart file and reason; `Idempotency-Key` required |

The five operations are carried into the `rwb-document` contract stories; this story builds them. The response body of a document read and of a version is the Document shape of the TSD P5 T-A.2 (id, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion), extended with storedAt, previousVersionId, versions and fields. Errors follow RFC 9457 with `messageId`.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | RWB-P3-E1018-CON | The case exists and is in the caller's scope; one hop, 2 s timeout, breaker per downstream (DP-11) |

The two parameters and the four reference lists are not REST operations of this story: they are read through the `rwb-case` parameters and reference-data client libraries of DP-06 and DP-07, which wrap the contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON. The file is written through the storage product RWB-PLT-TE012-APP, which is not a REST contract of another service; it appears in 12.9 as File.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | caseId | documentId, caseId, documentType, source, storedAt |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with decision code DOCATT and final call STORED |

CloudEvents 1.0 envelope, binary mode; no personal data in either payload. The event is written to the outbox in the store transaction, so it exists exactly when the document row exists; the trigger guarantees the consumers rely on (once per store, order per case, no duplicate) rest on the outbox relay and the consumer inbox of DP-09, and the transfer trigger that reacts to DocumentStored in this service is stated by RWB-P5-E1021-APP.

#### 12.4 Events consumed

None. This story consumes no Kafka event. `DocumentFieldsExtracted` is published by the extraction path (RWB-P5-E1050-APP and RWB-P5-E1053-APP), not by this story, and DocumentStored is consumed by `rwb-case` and `rwb-agent`.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | OCR, classify, extract; registered by RWB-P5-E1049-APP, which owns the workflow |
| `copyPending` | Activity | `rwb-document` | Contributed by this story: copies a COPY_PENDING document to its container after commit and sets `storage_ref` and state STORED |

#### 12.6 Schedules

None in this story. The 15-minute document-intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP; this story contributes only the `copyPending` activity that the Schedule-started workflow calls.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | The index row per file and per version: metadata, storage reference, hash, retention class, write-once flag, version |
| `document_field` | P5 | The extracted fields written with the document |
| `document_type` | P5 | Read only: the type row in the version in force (RWB-P5-E1025-APP owns the load) |
| `document_hub_parameter` | P5 | Read only: the document-hub parameter rows behind the parameters contract |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record, in the store transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The DocumentStored and decision-record rows; `processed_event` for the inbox |

No foreign-schema table is read (DP-01). No ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case fake (`GET /cases/{caseId}`) | RWB-P3-E1018-CON | Unit, component and end-to-end builds of the case read, the 2 s timeout and the scope check |
| decision-record fake | RWB-PLT-E1027-CON | The local record write and the publish on `rwb.decision-record.v1` |
| central ledger fake | RWB-P7-E1027-CON | The collection of the record into the central ledger |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-RETENTION, LOV-REVIEW, LOV-DOC-TYPE and LOV-DOC-SOURCE |
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` |
| storage product stub | RWB-PLT-TE012-APP | The upload link, the copy, the WORM refusal and the "container refuses writes" case of AC11 |
| Drools kit | not used | No rule package is evaluated in this story |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 5, consumed 1 | The upload create, the store command, the document read, the content read, the version add; the case read of `rwb-case` |
| Kafka | Published 1 event and 1 decision record; consumed 0 | `rwb.document.events.v1`, `rwb.decision-record.v1` |
| Temporal | 1 workflow, 1 activity | `DocumentIntakeWorkflow` (kit template, owned by RWB-P5-E1049-APP) with the `copyPending` activity |
| File | Blob WORM | The file at `{container}/{caseId}/{documentId}/v1` through RWB-PLT-TE012-APP; containers `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/store`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentHubController | Controller | The five operations of 12.1; maps exceptions to RFC 9457 problem responses with the message ID; access check and scope |
| DocumentStoreService | Service | Case contract read, type row, signature and size check, duplicate check, decision record, inserts, outbox row, version rules |
| DocumentRepository | Repository | Reads and writes `document` and `document_field` only; the `version` column is the optimistic lock |
| DocumentTypeReader | Repository | Reads `document_type` in the version in force by `valid_from` and `valid_to` |
| DocumentHubParameters | Library client | Reads `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` through the parameters contract of `rwb-case`, cached for 5 minutes |
| DocumentStorageClient | Client | The storage product RWB-PLT-TE012-APP: upload link, copy, open, and the refusal to overwrite; called, never reimplemented |
| CopyPendingActivity | Temporal activity | `copyPending` on queue `rwb-document`: retries the copy of COPY_PENDING rows, sets `storage_ref` and state STORED |
| DocumentDetailPanel | React component | Opens from SCR-30 through the gateway-bff composite route; metadata, extracted fields, versions and the download button |

**Database.**

- Writes `document` (all columns of DF-DOC-001 to DF-DOC-011, -025, -026 and the standard columns) and `document_field` (DF-DOC-012 to DF-DOC-017).
- Reads `document_type` and `document_hub_parameter` in `rwb_document`.
- One migration in the per-service Flyway sequence (DP-15): `V1024_1__document_store.sql` adds `document.previous_version_id` uuid null with a foreign key to `document(id)` and `document.content_sha256` char(64) not null, and creates `document_hub_parameter` (id, param_code varchar(40), param_value varchar(200), unit varchar(20), table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (`param_code`, `table_version`).
- Indexes: unique partial index `uk_document_case_type_hash ON document (case_id, document_type, content_sha256) WHERE is_active`; `ix_document_case_type_created ON document (case_id, document_type, created_at)`; `ix_document_previous_version ON document (previous_version_id)`.

**Configuration and reference data.**

- Document type table version DOCTYPE-2026.11 in force, loaded and approved through RWB-P5-E1025-APP.
- Parameters `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` in `document_hub_parameter`, read through the parameters contract.
- Container names `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` as properties per environment; the account and the immutability policy are RWB-PLT-TE012-APP's and are Not specified in the source documents (GAP-1031; ASM-1979).
- Decision code DOCATT, assumed; the LOV-DECISION list is loaded by the data steward.
- Feature flag `rwb.document.store`. Off: the five operations return 404 and the store command refuses with a feature-off error; the `copyPending` activity is not registered.

**Build steps**

1. Write the migration and the entities; test that the unique partial index refuses a second active row with the same case, type and hash.
2. Build `DocumentHubParameters` and `DocumentTypeReader` with the `valid_from` and `valid_to` rule of the type table; unit test the version in force on a boundary date.
3. Build `DocumentStoreService.store` with the case contract read, validation (type, content signature, size) and the duplicate check; unit test AC5, AC6, AC7, AC8 and the 2 s timeout path X12.
4. Add the transaction: decision record, inserts and outbox row; integration test that a forced record failure leaves no row, no field and no event (X11, TC-E1-024-14).
5. Call the storage product after commit and build the `copyPending` activity; integration test against the SIT storage account with `rwb-docs-legal` under its immutability policy for AC1, AC2, AC11 and X13.
6. Build the version add with the latest-version rule and optimistic locking; test AC4, AC9, AC10.
7. Build the refusal of the legacy delete and content replace with the write-once check and the audit event; test AC2.
8. Build the five operations with the access check and scope; API tests for AC1, AC6, AC7, AC12 and the access test TC-E1-024-13.
9. Build `DocumentDetailPanel`; component test for the version list and the download.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the three tables the legacy story wrote into `rwb_document` and removes every cross-module read: the case is no longer read from a case table but from the `rwb-case` contract, which is DP-11 and the C dependency RWB-P3-E1018-CON. DP-03 replaces the in-process decision-log writer with the local library, so the record, the row and the outbox row share one transaction and the record is published on the shared topic. DP-06 and DP-07 keep the two parameters and the four lists out of the code: the library wraps the `rwb-case` contract while the document-hub parameter rows stay in this schema, as the Ownership Map gives them to P5. DP-09 puts DocumentStored in the outbox. DP-10 replaces the Quartz step that retried a pending copy with the `copyPending` activity of the workflow kit template. DP-13 and DP-15 give the service its own base and its own migration step. DP-19 puts the store reads behind the gateway-bff composite route, so the screen calls the owner once and never chains calls. The remaining legacy service call, the storage product, is an X dependency (RWB-PLT-TE012-APP) because it is platform work and not a service contract.

**Done when.** The tests in section 16 pass, the boundary test on the module tables passes, a 1.2 MB PDF is stored and listed within 2 seconds in SIT, and `rwb.document.DocumentStored.v1` is on the topic once per store with no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | File content is not an allowed type | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-002 | Delete or change of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-017 | File above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-025 | New version on a superseded version | This is not the latest version of the document. Open the latest version to add a new one. |
| MSG-P5-006 | Document type not in the type table in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-004 | Concurrent version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | Content requested while the copy is pending, or the case contract not available | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The HTTP mapping is unchanged from the legacy contract: 415 for MSG-P5-001, 413 for MSG-P5-017, 422 for MSG-P5-006, 409 for MSG-P5-025 and MSG-GEN-004, 403 for MSG-P4-002 and MSG-P4-003, 503 for MSG-GEN-006 and MSG-P7-003. A document that does not exist answers 404 with a not-found message whose ID is Not specified in the source documents (GAP-1032; ASM-1980). Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-GEN-006 the {system} value is "Document storage" for a pending copy and "Case service" for a case-contract timeout. For MSG-P5-017 the {size} value is the `INTAKE_MAX_FILE_MB` parameter.

### 15. Screens and states

SCR-30 Case documents is published through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the full tab, its upload form, its list and the search within a case are RWB-P5-E1026-APP. This story adds the DocumentDetailPanel opened from a row of SCR-30:

| State | What the user sees |
|---|---|
| Loading | The panel skeleton while the metadata arrives through the composite route |
| Panel | Metadata, extracted fields and the version list with stored date and source, and the download button |
| Error | The message from section 14 when a read is refused (MSG-P4-002, MSG-P4-003, MSG-GEN-006) with a retry action |
| Write-once label | A write-once document shows no edit control and the label "Write once" (labels.txt) |
| Pending copy | A COPY_PENDING document shows the download disabled with MSG-GEN-006 and the state label, until the `copyPending` activity stores it |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-024-13 | Access | Component | Capacity and workforce planner (RW-CAPACITY, no Documents right) reads a document; refused with MSG-P4-002 |
| TC-E1-024-14 | Principle 5 | NFR | Decision record write forced to fail during a store; nothing stored, MSG-P7-003 |
| TC-E1-024-01 | AC1, BR1, BR2 | End to end | Synthetic court notice PDF of 1.2 MB on case RW-2026-000123 |
| TC-E1-024-02 | AC2, BR4 | End to end | Stored court notice; delete and replace through the store and the container |
| TC-E1-024-03 | AC3, BR3 | End to end | Synthetic appraisal report, type APPRAISAL_REPORT |
| TC-E1-024-04 | AC4, BR7 | End to end | Appraisal report with a second file and reason "Revised valuation" |
| TC-E1-024-05 | AC5, BR3 | End to end | Type BANK_STATEMENT |
| TC-E1-024-06 | AC6, BR5 | End to end | Word file "macro-0001.docx" renamed to .pdf |
| TC-E1-024-07 | AC7, BR5 | End to end | PDFs of 26,214,400 and 26,214,401 bytes |
| TC-E1-024-08 | AC8, BR6 | End to end | The same file stored twice on one case |
| TC-E1-024-09 | AC9 | End to end | Two parallel version requests on doc_version 2 |
| TC-E1-024-10 | AC10, BR7 | End to end | Version request on an inactive version |
| TC-E1-024-11 | AC11 | End to end | Container `rwb-docs` set to refuse writes; then released |
| TC-E1-024-12 | AC12, BR9 | End to end | Phone collector with scope OWN on another owner's case |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. The wave-1 integration harness copies TC-E1-024-01 as RWB-ITG-E1024-ITG, where the real `rwb-case` and the real storage account replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: file types, size limit, write-once flag, retention class, the four lists and the container names are data rows, parameters or properties.
- No personal data in events, workflow inputs or payloads, logs or tests. Test files are synthetic; extracted field values in logs are replaced by the field name.
- No read of another service's tables (DP-01). The case is read through the `rwb-case` contract `GET /cases/{caseId}`, one hop, 2 s timeout. ACE data is reached only through the owner's contract or a `v_ace_*` view, and this service reads no view.
- The service never overwrites a blob: every version is a new path at `{container}/{caseId}/{documentId}/v1`, and a write-once container refuses the attempt on its own.
- The PII access log entry for each read is written by the ACE common module, never by this package.
- One evaluator if any: this story evaluates no rule package, so no Drools kit is loaded and no rule row is read.
- The decision record is written in the same transaction as the row, the fields and the outbox row; a failure stores nothing (R-UNI-39).
- The store is idempotent twice over: `Idempotency-Key` on the POST and the unique partial index on case, type and hash for an active row.
- The feature flag `rwb.document.store` removes the capability without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-024-01, TC-E1-024-03, TC-E1-024-05, TC-E1-024-08 |
| REQ-DCM-002 | The document hub is the system of record for recovery documents | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-024-01, TC-E1-024-11, TC-E1-024-14 |
| REQ-DCM-003 | Legal document types are held in a write-once container that cannot be altered or deleted | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-01 | L2 13.3 Store and retain documents | None | TC-E1-024-02, TC-E1-024-04, TC-E1-024-09, TC-E1-024-10 |
| REQ-DCM-008 | Documents are searchable by case ID, type and date from the case record view | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | None | TC-E1-024-01, TC-E1-024-06, TC-E1-024-07, TC-E1-024-12, TC-E1-024-13 |
| REQ-ACA-006 | Every read of the case store and the document store is written to the access log | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | CTL-09 | TC-E1-024-12, TC-E1-024-13 |
| REQ-DCM-015 | Documents are backed up on a stated schedule and a restore is tested before release | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-01 | L2 13.3 Store and retain documents | None | TC-E1-024-01 (the backup itself is RWB-PLT-TE012-APP) |
| REQ-DCM-017 | The hub answers an electronic discovery request with every document for a named population and its version history | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-20 | 13 Manage documents and correspondence | None | TC-E1-024-04 (the response itself is Epic 2) |

| Legacy reference | Where it is kept |
|---|---|
| Document type table version DOCTYPE-2026.11 and the six types | Background, sections 3, 4, 8, 13, 16 |
| Event DocumentStored (EV-16) | Sections 4, 12.3, 17 |
| MSG-P5-001, MSG-P5-002, MSG-P5-006, MSG-P5-017, MSG-P5-025, MSG-GEN-004, MSG-GEN-006, MSG-P4-002, MSG-P4-003, MSG-P7-003 | Section 14, exception paths |
| Decision code DOCATT and final call STORED | Sections 1, 4, 8, 12.3, 13 |
| Containers rwb-docs, rwb-docs-legal, rwb-quarantine and the path `{container}/{caseId}/{documentId}/v1` | Sections 1, 2, 4, 12.9, 13 |
| Parameters INTAKE_ALLOWED_TYPES = PDF, JPG, PNG and INTAKE_MAX_FILE_MB = 25 | Background, sections 3, 4, 8, 13 |
| Rules R-UNI-39, R-UNI-40, CTL-06, CTL-09, CTL-12, DT06, DL27, DL11 | Sections 2, 8, 9, 18 |
| Legacy key RWB-E1-024, story RWB-P5-E1024-APP, self-tests TC-E1-024-01 to TC-E1-024-14 | Metadata, sections 3, 12, 16 |

### 19. Out of scope

- The upload form, the case document list and the search within a case and across cases (RWB-P5-E1026-APP).
- OCR, classification and field extraction (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP).
- Confirming or correcting an extracted field (RWB-P5-E1054-APP).
- Retention periods, the retention Schedule and the virus scan (RWB-P5-E1041-APP).
- Container provisioning, the WORM policy, backup and restore tests (RWB-PLT-TE012-APP; REQ-DCM-015).
- Custody of originals and electronic discovery (RWB-P5-E2018-APP, RWB-P5-E2024-APP, Epic 2; REQ-DCM-017).
- Document generation from templates (RWB-P5-E2026-APP).
- The published contract documents of this service, their fakes and their versioning, and the contract of the key in other services.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
