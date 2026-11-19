# RWB-E1-024 Document store and index

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-024 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-01 Store documents with a write-once container for legal types; FEAT-DCM-02 Index documents by case, type, date and extracted fields; FEAT-DCM-19 Keep the Workbench document hub as the system of record for documents; FEAT-DCM-20 Version a document and keep its history |
| Requirement IDs | REQ-DCM-001, REQ-DCM-002, REQ-DCM-003, REQ-DCM-008 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence; L2 13.3 Store and retain documents |
| Decision | D7.2 |
| Priority | Must |
| Depends on | RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept**, so that **I find a document by case ID, type and date, and a legal document cannot be changed after it is stored**.

## 2. Business rationale

Recovery documents are held today in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit (FSD P5 A1.3). This story builds the store and the index that every other document story writes to: one document record in the Workbench document hub per file, the file in blob storage, legal types write-once (DT06, ADR-007, control CTL-12). It meets REQ-DCM-001, REQ-DCM-002, REQ-DCM-003 and REQ-DCM-008. The module measure is fields extracted without review (FSD P5 A2.1.1), which can only be counted once every document is indexed against its case.

## 3. Preconditions

- RWB-E1-001 is done: the tables document and document_field exist in the recovery schema.
- RWB-TE-012 is done: the intake container, rwb-docs (standard), rwb-docs-legal (write-once) and rwb-quarantine exist, reached by managed identity through DocumentStorage.
- RWB-E1-018 is done: cases exist and the P3 published interface CaseDirectory returns a case by ID.
- RWB-E1-025 is done: document type table version DOCTYPE-2026.11 is in force with the six types, the write-once flag and the retention class of each type.
- RWB-E1-027 is done: the P7 published interface DecisionLogWriter writes an entry inside the caller's transaction.
- Document hub parameters loaded (this story creates the table): INTAKE_ALLOWED_TYPES = PDF, JPG, PNG; INTAKE_MAX_FILE_MB = 25, assumed (DL11). RWB-E1-053 and RWB-E1-057 read the same table.
- The caller is the upload service (RWB-E1-026, user with Documents C) or the intake (RWB-E1-032, SY-OCR). A reader holds Documents R with the case in scope.
- Feature flag rwb.dochub.store is on.

## 4. Flow

1. Caller: calls DocumentStore.store with the case ID, the document type, the source, the file in the intake container, its SHA-256 hash and any extracted fields.
2. DocumentStoreService: gets the case through CaseDirectory.findById and refuses the call if the case does not exist.
3. DocumentStoreService: reads the type row from the document type table version in force: write_once and retention_class.
4. DocumentStoreService: checks the file type by its content signature and the file size against INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB.
5. DocumentStoreService: looks for an active document on the case with the same type and hash; if one exists, returns it and stops.
6. DocumentStoreService: in one transaction, writes the decision log entry (decision code DOCATT, final call STORED) through DecisionLogWriter, inserts the document row with doc_version 1 and state COPY_PENDING, inserts the document_field rows and writes DocumentStored (EV-16) to the outbox.
7. DocumentStoreService: after commit, calls DocumentStorage.store (RWB-TE-012), which writes the file to rwb-docs-legal when write_once is true and to rwb-docs otherwise, at {container}/{caseId}/{documentId}/v1; the service sets storage_ref and state STORED.
8. User with Documents R: opens the document from the case documents screen (SCR-30); GET /documents/{documentId} returns the metadata, the extracted fields and the version list; GET /documents/{documentId}/content returns the file. The ACE common module writes each read to the PII access log.
9. User with Documents U: adds a version with POST /documents/{documentId}/versions; the service inserts a new document row with doc_version n+1 and previous_version_id set to the current row, and marks the earlier row is_active = false. The earlier version stays readable.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Delete or content replace of a write-once document, through the service or directly on the container | Refused; the file and the row are unchanged; an audit event DOCUMENT_CHANGE_REFUSED is written | MSG-P5-002 | AC2 |
| X2 | Document type not in the type table in force | Refused with 422; nothing stored | MSG-P5-006 | AC5 |
| X3 | File content is not PDF, JPG or PNG | Refused with 415; nothing stored | MSG-P5-001 | AC6 |
| X4 | File above INTAKE_MAX_FILE_MB | Refused with 413; nothing stored | MSG-P5-017 | AC7 |
| X5 | The same file is stored again on the same case with the same type | The existing document is returned; no second row, entry or event | None | AC8 |
| X6 | Two users add a version to the same document at the same time | The first succeeds; the second gets 409; one new version exists | MSG-GEN-004 | AC9 |
| X7 | A version is added to a document that is not the latest version | Refused with 409 | MSG-P5-025 | AC10 |
| X8 | The copy to the container fails after commit | The row stays COPY_PENDING; the copy is retried by the next document intake run (JOB-12); content reads return 503 until it is stored | MSG-GEN-006 | AC11 |
| X9 | The reader's role scope does not include the case | Refused with 403; nothing is returned | MSG-P4-003 | AC12 |
| X10 | The caller's role lacks the Documents right | Refused with 403 | MSG-P4-002 | TC-E1-024-13 (Access) |
| X11 | The decision log write fails | Nothing is stored; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-024-14 (Principle 5) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables (RWB-E1-001), the containers (RWB-TE-012), the case (RWB-E1-018), the type table (RWB-E1-025) and the decision log writer (RWB-E1-027), all earlier in Epic 1 |
| Negotiable | File types, size limit, write-once flag and retention class are data rows; the story fixes the behavior |
| Valuable | Every later document path (upload, OCR intake, generation) stores through this one service |
| Estimable | One service, one published interface, three endpoints, one detail panel, one migration |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Document store and index

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given type "COURT_NOTICE" has write_once true and retention class "LEGAL10Y"
    Given type "APPRAISAL_REPORT" has write_once false and retention class "GENERAL05Y"
    Given parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
    Given case "RW-2026-000123" exists with product group "MORTGAGE" in team "MTG-BKK-LIT"

  Scenario: AC1 Stored against case
    Given a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN"
    When it is stored
    Then one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today
    Then its extracted field "black_case_no" with value "BC-TEST-0456" is in the index
    Then the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1"
    Then the system writes documentStored to the outbox with the document ID, the case ID, the type and the source
    Then the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash

  Scenario: AC2 Write once
    Given the court notice from AC1 is stored with write_once true
    When a delete and a content replace are attempted through the document store and directly on the container
    Then the system refuses each attempt with MSG-P5-002
    Then the file hash and the document row are unchanged
    Then the system writes an audit event "DOCUMENT_CHANGE_REFUSED" for each attempt with the document ID and the caller

  Scenario: AC3 Retention class
    Given a document of type "APPRAISAL_REPORT" for case "RW-2026-000123"
    When it is stored
    Then the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11"
    Then write_once is false and the file is in container "rwb-docs"

  Scenario: AC4 A new version keeps the history
    Given the appraisal report from AC3 at doc_version 1
    When a user with Documents U adds a new file with reason "Revised valuation"
    Then a document row with doc_version 2 and previous_version_id of version 1 exists and is active
    Then version 1 is inactive and its content is still returned by GET content
    Then GET for version 2 lists versions 1 and 2 with their stored dates and sources

  Scenario: AC5 Unknown document type is refused
    Given a file for case "RW-2026-000123" with type "BANK_STATEMENT"
    When it is stored
    Then the system refuses the call with 422 and MSG-P5-006
    Then no document row, decision log entry or event is written

  Scenario: AC6 File type not allowed
    Given a file "macro-0001.docx" with Word content for case "RW-2026-000123"
    When it is stored
    Then the system refuses the call with 415 and MSG-P5-001
    Then the system writes nothing to the containers or the tables

  Scenario: AC7 Size limit boundary
    Given two PDF files for case "RW-2026-000123" of 26,214,400 bytes and 26,214,401 bytes
    When each is stored
    Then the system stores the file of 26,214,400 bytes
    Then the system refuses the file of 26,214,401 bytes with 413 and MSG-P5-017 showing 25 MB

  Scenario: AC8 The same file stored twice
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    When the same file with the same hash and type is stored again on that case
    Then the system returns the existing document ID
    Then the case still holds one court notice row, one decision log entry and one DocumentStored event for it

  Scenario: AC9 Two versions added at the same time
    Given the appraisal report at doc_version 2
    When two users add a new version at the same time
    Then one request returns 200 with doc_version 3
    Then the other returns 409 with MSG-GEN-004
    Then exactly one row with doc_version 3 exists

  Scenario: AC10 Version on a superseded document
    Given the appraisal report version 1 is inactive
    When a user adds a new version to version 1
    Then the system refuses the request with 409 and MSG-P5-025
    Then the system writes no new row

  Scenario: AC11 The storage copy fails
    Given container "rwb-docs" refuses writes
    When an appraisal report is stored for case "RW-2026-000123"
    Then the system writes the document row with state "COPY_PENDING"
    Then GET content returns 503 with MSG-GEN-006 naming "Document storage"
    Then when the container accepts writes again the next document intake run copies the file and sets state "STORED"

  Scenario: AC12 Case outside the reader's scope
    Given a phone collector with scope OWN who does not own case "RW-2026-000123"
    When the phone collector requests the court notice from AC1
    Then the system refuses the request with 403 and MSG-P4-003
    Then no metadata or content is returned
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It sets the document record state (standard column state): new row COPY_PENDING; COPY_PENDING to STORED when the copy succeeds; on a new version the earlier row changes is_active from true to false.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Stores documents through DocumentStore (Documents C) |
| RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and the other roles with Documents C | Store through the upload in RWB-E1-026 |
| Roles with Documents U (for example RW-CASEOWN, RW-LITOFF, RW-LEGAL, RW-COMPLY) | Add a new version |
| Roles with Documents R (for example RW-TEAMMGR, RW-AUDIT, RW-PHONECOL) | Read metadata and content inside their scope |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Nobody | Deletes or changes a write-once document |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-002 | recovery_case | case_no | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write |
| DF-DOC-025 | document | previous_version_id | Write |
| DF-DOC-026 | document | content_sha256 | Write |
| Standard column | document | state | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-REF-222 | document_type | write_once | Read |
| DF-REF-223 | document_type | retention_class | Read |
| DF-REF-229 | document_type | table_version | Read |
| DF-REF-245 | document_hub_parameter | param_code | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /documents/{documentId}**

| Item | Value |
|---|---|
| Request | Path documentId (uuid) |
| Response | 200 Document: id, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion. Extended with storedAt, previousVersionId, versions and fields (see additions) |
| Errors | 401 not signed in; 403 no Documents R (MSG-P4-002) or case out of scope (MSG-P4-003); 404 no such document; 503 store unavailable (MSG-GEN-006) |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**GET /api/recovery/v1/documents/{documentId}/content**

| Item | Value |
|---|---|
| Request | Path documentId (uuid) |
| Response | 200 application/octet-stream, the file of that version |
| Errors | 401; 403 as above; 404; 503 while state is COPY_PENDING (MSG-GEN-006) |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**POST /documents/{documentId}/versions**

| Item | Value |
|---|---|
| Request | multipart/form-data: file (binary), reason (string, required) |
| Response | 200 Document, the new version |
| Errors | 401; 403 no Documents U (MSG-P4-002) or out of scope (MSG-P4-003); 404; 409 not the latest version (MSG-P5-025) or concurrent change (MSG-GEN-004); 413 file above the limit (MSG-P5-017, see additions); 415 file type (MSG-P5-001); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header; a repeat with the same key returns the first result |

**Published interface (P5, used by RWB-E1-026, RWB-E1-032 and the retention job in RWB-E1-041)**

```java
public interface DocumentStore {
    StoredDocument store(StoreRequest request);          // caseId, documentType, source, intakeBlobRef, sha256, fields, partyId
    StoredDocument addVersion(UUID documentId, BlobRef file, String reason, UUID actor);
    void delete(UUID documentId, String reason, UUID actor);          // throws WriteOnceViolationException when write_once
    void replaceContent(UUID documentId, BlobRef file, UUID actor);   // throws WriteOnceViolationException when write_once
    Optional<StoredDocument> findById(UUID documentId);
}
```

**Event published:** DocumentStored (EV-16), payload documentId, caseId, type, source, written to the outbox in the store transaction.

## 13. Solution plan

**Package.** Folder `recovery/dochub/store`, Java package `recovery.dochub.store`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| DocumentHubController | Controller | GET document, GET content, POST versions; maps exceptions to problem responses with the message ID |
| DocumentStore | Published interface | The contract in section 12 for other modules and P5 packages |
| DocumentStoreService | Service | Validation, type lookup, duplicate check, decision log write, insert, outbox event, version rules |
| DocumentHubRepository | Repository | Reads and writes document and document_field only |
| DocumentEntity, DocumentFieldEntity | Entity | Map the two tables, with the optimistic lock column version |
| DocumentTypeReader | Repository | Reads the document type table version in force (table from RWB-E1-025) |
| DocumentHubParameters | Rule table | Reads document_hub_parameter rows in force, cached for 5 minutes; used by every P5 package |
| DocumentStorage | Published interface | From RWB-TE-012: writes, opens and refuses overwrite of blobs; called, never reimplemented |
| CopyPendingStep | Job | Step of JOB-12 Document intake that retries copies for rows in COPY_PENDING |
| DocumentDetailPanel | React component | Opens from SCR-30; shows metadata, extracted fields, versions and the download button |

**Database.**
- Reads and writes document (all columns) and document_field (all columns).
- Flyway migration `V1_5_024__document_store.sql`: adds document.previous_version_id uuid null with a foreign key to document(id) and document.content_sha256 char(64) not null; creates document_hub_parameter (id, param_code varchar(40), param_value varchar(200), unit varchar(20), table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (param_code, table_version).
- Indexes: ix_document_case_type_created on document (case_id, document_type, created_at); unique partial index uk_document_case_type_hash on document (case_id, document_type, content_sha256) where is_active; ix_document_previous_version on document (previous_version_id).

**Configuration and reference data.**
- Document type table (RWB-E1-025), loaded by the reference data administrator.
- Parameters INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB in document_hub_parameter, loaded by the reference data administrator.
- Container names rwb-docs and rwb-docs-legal from RWB-TE-012, held as properties per environment.
- Decision code DOCATT, assumed; the LOV-DECISION list is loaded by the data steward.

**Build steps.**
1. Write the migration and the entities; test the unique partial index refuses a second active row with the same case, type and hash.
2. Build DocumentHubParameters and DocumentTypeReader with the valid_from and valid_to rule of the type table; unit test the version in force on a boundary date.
3. Build DocumentStoreService.store with validation (case, type, content signature, size) and the duplicate check; unit test AC5, AC6, AC7, AC8.
4. Add the transaction: DecisionLogWriter call, inserts and outbox event; integration test that a forced writer failure leaves no row and no event.
5. Call DocumentStorage after commit and build CopyPendingStep; integration test against the SIT storage account with rwb-docs-legal under its immutability policy for AC1, AC2 and AC11.
6. Build addVersion with the latest-version rule and optimistic locking; test AC4, AC9, AC10.
7. Build delete and replaceContent with the write-once refusal and the audit event; test AC2.
8. Build the controller endpoints with the access check and scope; API tests for AC1, AC12 and the access test.
9. Build DocumentDetailPanel; component test for the version list and the download.

**Feature flag.** `rwb.dochub.store`. Off: the endpoints return 404 and DocumentStore.store refuses with a feature-off error.

**Done when.** The tests in section 16 pass, the boundary test on module tables passes, and a 1.2 MB PDF is stored and listed within 2 seconds in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | File content is not an allowed type | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-002 | Delete or change of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-017 | File above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-025 | New version on a superseded version | This is not the latest version of the document. Open the latest version to add a new one. |
| MSG-P5-006 | Document type not in the type table in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-004 | Concurrent version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | Content requested while the copy is pending | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-30 Case documents (states Loading; list; upload) is built in RWB-E1-026. This story adds the DocumentDetailPanel opened from a row of SCR-30: Loading while the metadata arrives; the panel with metadata, extracted fields and versions; the Error state with the message from section 14 when a read is refused. A write-once document shows no edit control and the label "Write once" (labels.txt).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-024-01 | AC1, BR1, BR2 | System | Synthetic court notice PDF on case RW-2026-000123 |
| TC-E1-024-02 | AC2, BR4 | System | Stored court notice; delete and replace through the service and the container |
| TC-E1-024-03 | AC3, BR3 | System | Synthetic appraisal report |
| TC-E1-024-04 | AC4, BR7 | System | Appraisal report with a second file |
| TC-E1-024-05 | AC5, BR3 | System | Type BANK_STATEMENT |
| TC-E1-024-06 | AC6, BR5 | System | Word file renamed to .pdf |
| TC-E1-024-07 | AC7, BR5 | System | PDFs of 26,214,400 and 26,214,401 bytes |
| TC-E1-024-08 | AC8, BR6 | System | Same file stored twice |
| TC-E1-024-09 | AC9 | System | Two parallel version requests |
| TC-E1-024-10 | AC10, BR7 | System | Version request on an inactive version |
| TC-E1-024-11 | AC11 | System | Standard container set to refuse writes |
| TC-E1-024-12 | AC12, BR9 | System | Phone collector with scope OWN on another owner's case |
| TC-E1-024-13 | Access | Access | Capacity and workforce planner (RW-CAPACITY, no Documents right) reads a document; refused with MSG-P4-002 |
| TC-E1-024-14 | Principle 5 | Resilience | Decision log write forced to fail during a store; nothing stored, MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: file types, size limit, write-once flag, retention class and container names are data rows or properties.
- No personal data in logs, tests or prompts. Test files are synthetic; extracted field values in logs are replaced by the field name.
- No read of another module's tables: the case is read through CaseDirectory, the decision log is written through DecisionLogWriter.
- The service never overwrites a blob; every version is a new blob path.
- The PII access log entry for each read is written by the ACE common module, never by this package.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | Business Requirements Epic 1, section 3.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-024-01, TC-E1-024-03, TC-E1-024-05, TC-E1-024-08 |
| REQ-DCM-002 | The document hub is the system of record | Business Requirements Epic 1, section 3.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-024-01, TC-E1-024-11, TC-E1-024-14 |
| REQ-DCM-003 | Legal types held write-once | Business Requirements Epic 1, section 3.5 | FEAT-DCM-01 | L2 13.3 Store and retain documents | None | TC-E1-024-02, TC-E1-024-04, TC-E1-024-09, TC-E1-024-10 |
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | Business Requirements Epic 1, section 3.5 | FEAT-DCM-02 | 13 Manage documents and correspondence | None | TC-E1-024-01, TC-E1-024-06, TC-E1-024-07, TC-E1-024-12, TC-E1-024-13 |

## 19. Out of scope

- The upload form, the case document list and the search within a case (RWB-E1-026).
- Classification, field extraction and automatic attach from the OCR intake (RWB-E1-050, RWB-E1-053, RWB-E1-032).
- Confirming or correcting an extracted field with PATCH /documents/{documentId}/fields/{fieldId} (RWB-E1-054).
- Retention periods, the retention job and the virus scan (RWB-E1-041).
- Container creation, backup and restore tests (RWB-TE-012; REQ-DCM-015).
- Custody of originals (Epic 2, SCR-32) and electronic discovery (Epic 2, REQ-DCM-017).

