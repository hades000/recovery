# RWB-ITG-E1024-ITG Document store and index

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-024 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 9 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; finishing pass.

**Version 3 changes**

- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004).
- Customer and account reads follow the published paths `/customers/{personKey}` (`getCustomer`) and `/accounts/{accountKey}` (`getAccount`) (RD-P1-060).
- Finishing follow-up: linked AC1 to TC-ITG-E1024-ITG-01 in Test Cases v9.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1024-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-024 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1024-ITG-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | 5.0.0 of the rwb-document, rwb-case and rwb-source-data REST and event contracts (API Specification v5), on the /v1 paths |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P1-E1001-APP, RWB-P5-E1024-APP (not yet built; each must be in SIT before the suite runs) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-019, FR-PLT-026, FR-PLT-028, FR-PLT-029, FR-PLT-033) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-060 |

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-024 document store and index across rwb-document (P5, the owner of the document and its index), rwb-case (P3, the case and the parameters) and rwb-source-data (P1, the customer contract)**, so that **a document is stored against a real case, held write-once on a real WORM container, versioned with its history, deduplicated, recorded in the decision record and published as DocumentStored, all proved on real services before wave 1 exits**.

### 2. Business rationale

The legacy story is the store that every other document story writes to: one document record per file in the document hub, the file in Blob storage, legal types write-once, the case read through the in-process CaseDirectory, the decision written through DecisionLogWriter inside the caller's transaction and the local DocumentStored event written to the outbox. In the target the same behaviour is split across owners. The document, the document index, the extracted fields and the document type table are `rwb_document`, owned by P5 rwb-document (Architecture v5 slides 16 and 41); the file lives in the Blob WORM container reached by rwb-document only. The case, the case number and the parameters in force are P3 rwb-case, read through the P3 case contract and the P3 parameter contract (DP-06); the reference data, including the document type list and the write-once flag, is read through the P3 reference-data contract (DP-07). The decision record is written locally by the decision-record library in the same transaction as the document row (DP-03) and published as `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`; the central ledger in P7 rwb-decision seals it and is proved in RWB-ITG-E1027-ITG. `rwb.document.DocumentStored.v1` leaves on `rwb.document.events.v1` in the CloudEvents envelope (ADR-015, DP-09). The two-second window that made the legacy store acceptable now spans three services and a container, so it is a cross-service fact that no single service story can prove.

This is an integration slice, not a re-statement of the component behaviour. The legacy criteria AC1 to AC12 stay with RWB-P5-E1024-APP, which owns the contract and the full behaviour in `rwb_document`; they are not re-owned here. What this story owns is the nine criteria that only exist when the store, the case, the customer, the parameters, the container, the shared decision-record topic and the intake workers are all real. The target reading is recorded in GAP-0349 and ASM-0443.

No service contract is faked. The suite exercises the published wave 1 contracts of P5, P3 and P1, the shared decision-record topic and a real write-once container; the only stubs are the external ones named in section 12.8.

### 3. Preconditions

- RWB-P5-E1024-APP is done: the document and document_field tables, the document type table version in force, the store, the version path, the write-once refusal and the copy-pending step are in SIT under `rwb_document`.
- RWB-P3-E1018-APP is done: the case record is readable through `GET /api/recovery/case/v1/cases/{caseId}` and the parameters and reference data are served through the P3 admin contracts.
- RWB-P1-E1001-APP is done: the customer and party facts are published through the P1 customer contract against the ACE views.
- The published contracts of P5 rwb-document, P3 rwb-case and P1 rwb-source-data are deployed under `/api/recovery/<short>/v1` and versioned in the registry.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic documents, cases and customers, and it is the only source of data for the run.
- The environment is SIT, with the wave 1 topics and their retry and `.dlt` topics, the namespace `rwb-recovery`, and a Blob WORM container (Azurite in the lower environment).
- The document type table version in force and the parameters INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB are loaded through the P3 contracts for the run date.
- No production data is read, copied or connected to; every case, customer, party key and document used by the run is synthetic.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, customers and files of the RWB-ITG-W1J01-ITG set; no service schema is opened and no production row is used.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` for case RW-2026-000123 and asserts that the case exists with product group MORTGAGE and team MTG-BKK-LIT before any store.
3. Harness: stores the synthetic court notice "notice-0001.pdf" of 1.2 MB through `POST /api/recovery/document/v1/documents` on P5 with type COURT_NOTICE, source SCAN, the party key and the extracted field black_case_no BC-TEST-0456.
4. Harness: reads the stored document through `GET /api/recovery/document/v1/documents/{documentId}` and asserts the case, the type, the source, doc_version 1, the stored date, the file type, the size and the extracted field, and reads `GET /api/recovery/document/v1/documents/{documentId}/content` to compare the SHA-256.
5. Harness: reads `GET /api/recovery/source-data/v1/customers/{personKey}` on P1 and asserts that the party key carried by the document resolves to the same synthetic customer, without reading any other field.
6. Harness: consumes `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` and asserts the CloudEvents envelope, the key caseId, the document ID, the case ID, the type and the source, and the absence of a personal data field.
7. Harness: consumes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and asserts decision code DOCATT, final call STORED and the document ID; it makes no assertion on the P7 central ledger, which belongs to RWB-ITG-E1027-ITG.
8. Harness: attempts a delete and a content replace on the write-once document, through the owner's contract and directly on the WORM container, and asserts MSG-P5-002, an unchanged row and an unchanged hash, and the audit event DOCUMENT_CHANGE_REFUSED.
9. Harness: adds a version through `POST /api/recovery/document/v1/documents/{documentId}/versions`, asserts doc_version 2 active with version 1 inactive and still readable, and then re-posts the same file, same case and same type to assert the single row, single decision record and single DocumentStored.
10. Harness: reads the parameters in force through `GET /api/recovery/case/v1/admin/parameters`, posts the two boundary files and the Word-content file, posts a store for a case the P3 contract does not return, sets the container to refuse writes for the copy-pending path, and posts the access refusal; it records every status and message, writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Delete or content replace of a write-once document, through the owning service or directly on the WORM container | Refused; the file and the document row are unchanged; an audit event DOCUMENT_CHANGE_REFUSED is written with the document ID and the caller | MSG-P5-002 | AC2 |
| X2 | Document type not in the type table in force | Refused with 422; nothing is stored and no event is published | MSG-P5-006 | Regression of RWB-P5-E1024-APP AC5 |
| X3 | File content is not PDF, JPG or PNG | Refused with 415; nothing is stored | MSG-P5-001 | AC5 |
| X4 | File above INTAKE_MAX_FILE_MB | Refused with 413; nothing is stored | MSG-P5-017 | AC5 |
| X5 | The same file is stored again on the same case with the same type | The existing document is returned; no second row, decision record or event | None | AC4 |
| X6 | Two callers add a version to the same document at the same time | The first succeeds; the second gets 409; one new version exists | MSG-GEN-004 | Regression of RWB-P5-E1024-APP AC9 |
| X7 | A version is added to a document that is not the latest version | Refused with 409; no new row | MSG-P5-025 | AC13 |
| X8 | The copy to the container fails after commit | The row stays COPY_PENDING; the copy is retried by the next JOB-12 run; content reads return 503 until the file is stored | MSG-GEN-006 | AC8 |
| X9 | The reader's role scope does not include the case | Refused with 403; nothing is returned | MSG-P4-003 | AC14 |
| X10 | The caller's role lacks the Documents right | Refused with 403 by the owning service | MSG-P4-002 | AC9 |
| X11 | The decision record cannot be written | The document row and the event are not written; the caller is told the action was not taken | MSG-P7-003 | AC6 |
| X12 | The P3 case contract does not return the case named in the store request | The store is refused; no document row, no file and no event are written | None | AC7 |
| X13 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the suite stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X14 | The W1J01 synthetic set does not match the run (missing case, customer or file) | The suite fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC7 |
| X15 | A consumed call exceeds the 2 s budget or returns a server error | The step is retried under the run policy and the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC3 |
| X16 | A suite step tries to read a service schema directly | The step does not exist: the suite ships with no client for a service schema, and the pipeline scan fails any change that adds one | None | AC15 |

X1 to X11 are the legacy exception paths carried onto the real services; X12 to X16 are the cross-service failures that appear only when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P5, P3 and P1, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval and the report layout are configuration; the file, the case, the type, the party key, the extracted field, the sizes, the decision code and the messages are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: the store against a real case, write-once on a real container, one decision record with one row, one DocumentStored per file, the parameter-driven limits, the case refusal and the copy-pending path |
| Estimable | One suite module, one fixture pack, four contract probes, one container control and one evidence report |
| Small | Nine scenarios over three services and one container; no service code and no schema change |
| Testable | Every criterion asserts a contract response, an event, a container object, a row count or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Document store and index, proven across the wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-case and rwb-source-data are deployed in SIT with their published contracts
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production data is used
    Given document type table version "DOCTYPE-2026.11" is in force
    Given type "COURT_NOTICE" has write_once true and retention class "LEGAL10Y"
    Given parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
    Given case "RW-2026-000123" exists with product group "MORTGAGE" in team "MTG-BKK-LIT"

  Scenario: AC1 A court notice is stored against a real case (new, D-RCV-60)
    Given a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN"
    When the harness stores it through POST /api/recovery/document/v1/documents on rwb-document
    Then rwb-document returns the document with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today
    Then GET /api/recovery/case/v1/cases/{caseId} on rwb-case returns that case with product group "MORTGAGE" and team "MTG-BKK-LIT"
    Then GET /api/recovery/source-data/v1/customers/{personKey} on rwb-source-data returns the party key carried by the document
    Then the extracted field "black_case_no" with value "BC-TEST-0456" is returned by the document contract
    Then rwb.document.DocumentStored.v1 is published on rwb.document.events.v1 with the document ID, the case ID, the type and the source
    Then GET /api/recovery/document/v1/documents/{documentId}/content returns the same SHA-256 hash

  Scenario: AC2 Write-once holds on the real WORM container (new, D-RCV-60)
    Given the court notice from AC1 is stored with write_once true in the WORM container
    When a delete and a content replace are attempted through the owning service and directly on the container
    Then each attempt is refused with MSG-P5-002
    Then the file hash and the document row are unchanged
    Then an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller

  Scenario: AC3 A new version keeps the history through the owner contract (new, D-RCV-60)
    Given the court notice from AC1 at doc_version 1
    When a caller with Documents U adds a new file with reason "Revised valuation"
    Then the document contract returns the new version as active at doc_version 2 with previous_version_id of version 1
    Then version 1 is inactive and its content is still returned by GET /api/recovery/document/v1/documents/{documentId}/content
    Then the document contract lists versions 1 and 2 with their stored dates and sources

  Scenario: AC4 The same file on the same case returns the existing document (new, D-RCV-60)
    Given the court notice from AC1 is stored on case "RW-2026-000123" with type "COURT_NOTICE"
    When the same file with the same hash and type is stored again on that case
    Then rwb-document returns the existing document ID
    Then the case holds one document row for it in the document contract
    Then exactly one decision record and one DocumentStored event exist for it

  Scenario: AC5 The size limit and file types come from the parameter contract (new, D-RCV-60)
    Given GET /api/recovery/case/v1/admin/parameters returns INTAKE_MAX_FILE_MB 25 and INTAKE_ALLOWED_TYPES "PDF,JPG,PNG" in force for the run date
    Given two PDF files for case "RW-2026-000123" of 26,214,400 bytes and 26,214,401 bytes
    When each is stored
    Then the file of 26,214,400 bytes is stored and returned by the document contract
    Then the file of 26,214,401 bytes is refused with 413 and MSG-P5-017 showing 25 MB
    Then a file "macro-0001.docx" with Word content is refused with 415 and MSG-P5-001
    Then nothing is written to the container or the index for either refused file

  Scenario: AC6 The decision record and the document row commit together (new, D-RCV-60)
    Given a court notice for case "RW-2026-000123" to be stored
    When rwb-document commits the store
    Then rwb.decision.DecisionRecorded.v1 is published on rwb.decision-record.v1 with decision code "DOCATT" and final call "STORED"
    Then the document contract returns the same document ID carried by the event
    When the decision-record library is forced to fail on a second store
    Then no document row is returned by the document contract for that store
    Then no DocumentStored event and no DecisionRecorded event are published for it

  Scenario: AC7 A case the case contract does not return is refused (new, D-RCV-60)
    Given a store request that names case "RW-2026-000999"
    Given GET /api/recovery/case/v1/cases/{caseId} on rwb-case returns 404 for that case
    When the store is posted to rwb-document
    Then the store is refused and the caller receives the owner's refusal
    Then no document row, no file and no event are written

  Scenario: AC8 Copy pending until the intake run copies the file (new, D-RCV-60)
    Given the WORM container refuses writes
    When a court notice is stored for case "RW-2026-000123"
    Then the document contract returns the document with state "COPY_PENDING"
    Then GET /api/recovery/document/v1/documents/{documentId}/content returns 503 with MSG-GEN-006 naming "Document storage"
    When the container accepts writes again and the next JOB-12 document intake run copies the file
    Then the document contract returns state "STORED"
    Then content returns the same SHA-256 hash as the stored file

  Scenario: AC9 A caller without the Documents right is refused (new, D-RCV-60)
    Given a synthetic test identity whose role has no Documents right
    When the identity reads a document through the owning service
    Then the owning service refuses the call with 403 and MSG-P4-002
    Then no metadata and no content are returned

  Scenario: AC13 A version added to a document that is not the latest version is refused (new, D-RCV-60)
    Given the court notice from AC3 with version 1 inactive and version 2 as the latest version
    When a caller with Documents U adds a new file to inactive version 1 of that document
    Then the document contract refuses the version with 409 and MSG-P5-025
    Then no new document row is written

  Scenario: AC14 A reader whose role scope does not include the case is refused (new, D-RCV-60)
    Given a reader whose role scope does not include case "RW-2026-000123"
    When the reader reads a document of that case through the owning service
    Then the owning service refuses the call with 403 and MSG-P4-003
    Then nothing is returned

  Scenario: AC15 A suite step cannot read a service schema directly (new, D-RCV-60)
    Given the suite holds only the published wave 1 contracts
    When the pipeline scans the suite for a client of a service schema
    Then the scan fails any change that adds one
    Then no suite step reads a service schema directly

  Scenario: AC16 The section 8 business rules hold across the run (new, D-RCV-60)
    Given the run has completed AC1 to AC9 and AC13 to AC15 against the wave 1 services
    When the run's documents, events, logs, workflow history and report are checked against section 8
    Then BR1 to BR8 are shown to hold by the criteria AC1 to AC8
    Then BR9 is shown to hold by AC9 and AC14, and BR10 to BR12 by the contract reads described in the Target reading
    Then BR13 is shown to hold by AC6, and BR14 and BR15 by AC15 and the one-hop budget in the Target reading
    Then the events, logs, workflow history, fixtures and report carry identifiers, document IDs, case IDs, party keys and counts only (BR16)

  Scenario: AC17 A retried or timed-out activity does not duplicate the store (new, D-RCV-60)
    Given a store for case "RW-2026-000123" where the owning service does not answer within the 2 s budget
    When the store activity is retried
    Then the store either completes once or is refused with no document row, no file and no event
    Then a completed store returns the same document ID on every answered attempt
    Then a completed store leaves one document row, one decision record and one DocumentStored event for the case
```

**Target reading.** The case is read through the P3 case contract, the parameters in force through the P3 parameter contract (DP-06), the reference data through the P3 reference-data contract (DP-07) and the party key through the P1 customer contract, all one hop with a 2 s budget (ADR-020). The document, its index, its extracted fields and its type rows are asserted only through the P5 contract on `rwb_document`; the suite opens no service schema. The decision record is written by the local decision-record library in the same transaction as the document row and read on `rwb.decision-record.v1`; the central ledger is not asserted here. The limits and the allowed types are rows in force, never values in the suite.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document is held against one case, with type, source, stored date and extracted fields | REQ-DCM-001; RWB-E1-024 BR1 |
| BR2 | rwb-document is the system of record; the file is held only in the WORM container reached by rwb-document | DT06; DL27; REQ-DCM-002 |
| BR3 | The write-once flag and the retention class come from the document type table version in force, never from the caller | RWB-E1-024 BR3; DT02 |
| BR4 | A write-once document is never deleted or changed; a change is a new version | CTL-12; REQ-DCM-003; NFR-029 |
| BR5 | File types and the size limit are parameters in force, read through the P3 parameter contract | RWB-E1-024 BR5; DL11; DP-06 |
| BR6 | A store with the same case, type and hash returns the existing document | R-UNI-40; RWB-E1-024 BR6 |
| BR7 | Only the latest version of a document takes a new version | FEAT-DCM-20; RWB-E1-024 BR7 |
| BR8 | A store that cannot be recorded in the decision record does not proceed | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR9 | Every read checks role, capability area and scope, and is written to the access log | CTL-09; REQ-ACA-006 |
| BR10 | P5 rwb-document owns the document, the document index, the extracted fields and the document type table in `rwb_document`; no other service holds a copy | DP-01; Architecture v5 slides 16 and 41; Ownership Map P5 |
| BR11 | P3 rwb-case owns the case, the case number, the parameters and the reference data; the suite reads them through the P3 contracts only | DP-06; DP-07; Ownership Map P3 |
| BR12 | P1 rwb-source-data owns the customer and party facts behind its ACE views; the suite reads the party key through the P1 customer contract only | DP-05; Ownership Map P1 |
| BR13 | The decision record is written locally in the document transaction and published on `rwb.decision-record.v1`; the central ledger in P7 is out of scope of this suite | DP-03; ADR-015; ADR-022 |
| BR14 | Each cross-service call is one hop to the owning service with a 2 s budget, behind gateway-bff where a screen is involved | ADR-020; DP-11; DP-19 |
| BR15 | No service reads or writes another service's schema; the suite ships with no client for a service schema | DP-01; ADR-021 |
| BR16 | No personal data in events, logs, workflow history, fixtures or the report: identifiers, document IDs, case IDs, party keys and counts only | RWB-E1-024 section 17; ADR-015 |

### 9. State transitions

The legacy document states are unchanged; the run observes them through the owner's contract.

| Object | From | Event | To |
|---|---|---|---|
| Document record | None | Store committed with the decision record | COPY_PENDING |
| Document record | COPY_PENDING | The copy to the container succeeds | STORED |
| Document record | STORED | A new version is added | The earlier row is inactive and the new row is active at the next doc_version |

The states the run observes across the services:

| Item | States |
|---|---|
| Document record | COPY_PENDING, STORED; is_active true or false per version |
| DocumentStored | Not published, published once for a stored document |
| Decision record | Written with the row, or not written and no row |
| Suite run | Not started, running, passed, failed with the failing test case named |
| Parameter set in force | In force for the run date, superseded after it |

The run changes no case status: the case is read only, through the P3 contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the container control and the evidence report |
| Service owner of rwb-document | Owns the document, the index, the type table, the WORM container path and the DocumentStored event |
| Service owner of rwb-case | Owns the case, the case number, the parameters and the reference data |
| Service owner of rwb-source-data | Owns the customer and party facts and the customer contract |
| Service owner of rwb-decision | Owns the shared decision-record topic, the local library and the central ledger |
| Roles with Documents R | Read metadata and content inside their scope; no write in this story |
| Roles with Documents U | Add a new version through the owner's contract |
| Data steward | Owns the document type rows and the parameter rows in force |
| Platform administrator | Receives an incident when the container or the topic is unavailable |
| Nobody | Deletes or changes a write-once document, or reads a service schema directly |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 rwb-case) | id | Read through the P3 case contract |
| DF-CAS-002 | recovery_case (P3 rwb-case) | case_no | Read through the P3 case contract |
| DF-DOC-001 to DF-DOC-011 | document (P5 rwb-document) | all fields | Read through the P5 document contract; written by rwb-document |
| DF-DOC-025 | document (P5 rwb-document) | previous_version_id | Read through the P5 document contract |
| DF-DOC-026 | document (P5 rwb-document) | content_sha256 | Read through the P5 document contract |
| Standard column | document (P5 rwb-document) | state | Read through the P5 document contract |
| DF-DOC-012 to DF-DOC-017 | document_field (P5 rwb-document) | all fields | Read through the P5 document contract; written by rwb-document |
| DF-REF-222 | document_type (P5 rwb-document) | write_once | Read through the P5 document contract |
| DF-REF-223 | document_type (P5 rwb-document) | retention_class | Read through the P5 document contract |
| DF-REF-229 | document_type (P5 rwb-document) | table_version | Read through the P5 document contract |
| DF-REF-245 | document_hub_parameter (P3 rwb-case) | param_code | Read through the P3 parameter contract |
| DF-REF-246 | document_hub_parameter (P3 rwb-case) | param_value | Read through the P3 parameter contract |
| DF-EXT-001 | party_ext (P1 rwb-source-data) | person_key | Read through the P1 customer contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 rwb-decision) | all fields | Read on rwb.decision-record.v1; written by the local library in rwb-document |
| Cross-service trigger and fixture composition | Document, case and customer fixtures | Trigger point, fixture set and poll window | Not specified in the source documents (GAP-0349; ASM-0443) |

Field IDs are those of RWB-E1-024 and are copied unchanged, with the owner of each table in brackets. The suite owns no field and no table: every row is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract, and no production value is used. The parameter rows are read through the P3 parameter contract, because parameters and reference data are held by P3 rwb-case (DP-06, DP-07), so the limits in force are asserted through the owner of the parameter contract and not through a table read (GAP-0349; ASM-0443).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are unused, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/document/v1/documents | P5 rwb-document | Store the synthetic document against a case |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the document, its index, its extracted fields, its state and its version list |
| GET /api/recovery/document/v1/documents/{documentId}/content | P5 rwb-document | Read the file and compare the SHA-256; the 503 path while the copy is pending |
| POST /api/recovery/document/v1/documents/{documentId}/versions | P5 rwb-document | Add a version and prove the history of AC3 |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Confirm the case before a store and refuse a case the contract does not return |
| GET /api/recovery/case/v1/admin/parameters | P3 rwb-case | Read INTAKE_MAX_FILE_MB and INTAKE_ALLOWED_TYPES in force for the run date |
| GET /api/recovery/source-data/v1/customers/{personKey} | P1 rwb-source-data | Read the party key carried by the document |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; no service is called through another service.

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | One event per stored document, with the document ID, the case ID, the type and the source; CloudEvents 1.0, key caseId, no personal data |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision ledger, written by the local library (DP-03) | One record per store with decision code DOCATT and final call STORED, read on the shared topic; the central ledger is proved in RWB-ITG-E1027-ITG |

The envelope is CloudEvents 1.0 and a consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the suite reads no service schema.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Copies a COPY_PENDING file to the container and runs the intake path under test |

The suite observes the workflow through Temporal visibility and asserts its result through the P5 contract; it starts no workflow of its own.

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| JOB-12 | Document intake | Every 15 min | P5 rwb-document | Event-started workflow with KEDA workers, not a Quartz job; copies the pending file of AC8 |

No Schedule of the suite is registered; the run waits for the owner's cadence and records the wait in the evidence report.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01, ADR-021).

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| Blob WORM container (Azurite in the lower environment) | The file of a stored document, its immutability policy, the delete and replace refusal and the deliberate write refusal of AC8 |
| RWB-ITG-W1J01-ITG synthetic fixture set | The synthetic cases, customers, party keys and files of the run |
| Mock Entra sign-in | Gives the run its synthetic test identities, including the identity without the Documents right |

No published service contract is faked: every P5, P3 and P1 call goes to the real service in SIT, and a run that needs a fake for any of them fails the preflight. No contract fake is named for rwb-case, rwb-document or rwb-source-data, and no contract fake library version is recorded as published for this story.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 7 |
| Kafka | 0 | 2 event types |
| Temporal | 0 | 1 workflow (DocumentIntakeWorkflow) observed through JOB-12 |
| File | 0 | 1 WORM container |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture pack for the synthetic documents, cases and customers, contract probes for the three owners, a container control for the WORM and copy-pending paths, and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts, run order, report and exit code |
| DocumentProbe | Test harness | Calls the four P5 document operations and asserts the row, the index, the state, the version list and the hash |
| CaseProbe | Test harness | Calls the P3 case read and the P3 parameter read; confirms the case and refuses a case the contract does not return |
| CustomerProbe | Test harness | Calls the P1 customer contract and asserts the party key carried by the document |
| EventProbe | Test harness | Consumes DocumentStored and DecisionRecorded, asserts the envelope, the counts and the absence of a personal data field |
| ContainerControl | Test harness | Refuses writes, attempts a delete and a replace on the WORM container, and records the refusal |
| ParameterStep | Test harness | Reads the size limit and the allowed types in force and builds the 26,214,400 and 26,214,401 byte files at runtime |
| ReportWriter | Test harness | One row per test case with the evidence, the elapsed time, the messages and the cleanup record |

**Configuration and reference data**

- The SIT endpoints of P5, P3 and P1, the topic names, the queue name `rwb-document`, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic case RW-2026-000123, the synthetic customer and party key, the file "notice-0001.pdf" of 1.2 MB and the extracted field black_case_no BC-TEST-0456.
- The document type table version "DOCTYPE-2026.11" and the type COURT_NOTICE with write_once true and retention class LEGAL10Y, loaded as rows through the owner's administration path.
- The parameter rows INTAKE_MAX_FILE_MB 25 and INTAKE_ALLOWED_TYPES "PDF,JPG,PNG", read through the P3 parameter contract and never written in the suite code.
- The 2 s client budget, the poll interval and the JOB-12 wait window.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Synthetic case set | Case RW-2026-000123 with product group MORTGAGE and team MTG-BKK-LIT, and the absent case RW-2026-000999 | AC1, AC7 |
| Synthetic customer set | The customer of case RW-2026-000123 and the party key carried by the document | AC1 |
| Synthetic files | notice-0001.pdf of 1.2 MB, two PDFs of 26,214,400 and 26,214,401 bytes, and macro-0001.docx with Word content | AC1, AC5 |
| Type and parameter rows | DOCTYPE-2026.11 with the six types, and the two parameters in force for the run date | All |
| Access identity | A synthetic identity with the Documents right and one without it | AC9 |
| Container state | The WORM container accepting writes, refusing writes and refusing delete and replace | AC2, AC8 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the topics and the container, with the contract preflight that fails on any drift.
2. Build DocumentProbe for the four document operations and assert AC1 through the owner's contract only.
3. Build CaseProbe and CustomerProbe; assert the case and the party key, and the case-not-returned path of AC7.
4. Build EventProbe for DocumentStored and DecisionRecorded, with the envelope, the count-per-store and the no-personal-data assertions.
5. Build ContainerControl for the write-once refusal of AC2 and the copy-pending path of AC8, including the JOB-12 wait and the 503 message.
6. Build ParameterStep and the boundary files; assert AC5 exactly at 26,214,400 and 26,214,401 bytes, and the Word-content refusal.
7. Add the duplicate store of AC4, the version path of AC3 and the forced decision-record failure of AC6.
8. Add the access refusal of AC9, write the evidence report, clean up the synthetic set and run the suite twice to prove that a repeated run adds no row and no event.

**Done when.** The fourteen test cases of section 16 pass on the real services in SIT, the nine criteria this story owns are signed off against the contracts, exactly one DocumentStored and one decision record exist per stored document, no service table was read, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

**Decoupling patterns applied** (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The suite asserts through contracts only and opens none of these schemas; each is owned by its service: P5 `rwb_document`, P3 `rwb_case`, P1 `rwb_source_data` |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | On RWB-P5-E1024-APP and on the P7 library; the suite only reads the topic |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The size limit and the allowed types are read through the P3 parameter contract |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The document type list and the write-once flag are read through the P3 reference-data contract |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | DocumentStored on `rwb.document.events.v1` and DecisionRecorded on `rwb.decision-record.v1` |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 document intake as an event-started workflow with KEDA workers |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The seven consumed REST operations of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P5-E1024-APP and RWB-P3-E1018-APP; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The SCR-30 and DocumentDetailPanel assertions of section 15 |

The dependency-added column records the build dependency of the owning story. An ITG story carries no H, C or X dependency of its own: this story's build dependencies are None, its contract dependencies are None, and its I dependencies are the three APP stories of the metadata table, RWB-P3-E1018-APP, RWB-P1-E1001-APP and RWB-P5-E1024-APP.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | File content is not an allowed type | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-002 | Delete or change of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-006 | Document type not in the type table in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-017 | File above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-025 | New version on a superseded version | This is not the latest version of the document. Open the latest version to add a new one. |
| MSG-GEN-004 | Concurrent version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | Content requested while the copy is pending | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs and wording are copied from RWB-E1-024 and this story adds no message ID. The refusal of AC7 carries the owning service's own refusal and no new message. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-30 Case documents (Loading; list; upload; empty: a search with no match shows "No documents match this search." with the action "Clear the search"; error: a refused or failed call shows its message from the RWB-E1-026 contract, such as MSG-P7-003 in the upload dialog; no access: 403 with MSG-P4-002 for a role without the right, where the Upload button is hidden for a role without Documents C, or MSG-P4-003 for a case outside the reader's scope) and the DocumentDetailPanel opened from one of its rows are reached through the gateway-bff composite route (DP-19); the panel shows the metadata, the extracted fields, the version list and the download button, and a write-once document shows no edit control and the label "Write once". The suite does not drive the screen; it asserts the same facts through the contracts of section 12.2 — the document, its fields, its versions and its content — and checks that the panel's read calls go through gateway-bff and then one hop to rwb-document. The screen states themselves are owned by RWB-E1-026 and are out of scope here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-024-13-ITG | AC9 | Integration | Capacity and workforce planner (RW-CAPACITY, no Documents right) reads a document; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-14-ITG | AC6 | NFR | Decision record write forced to fail during a store; no document row and no event; MSG-P7-003; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-01-ITG | AC1 | Integration | Synthetic court notice PDF of 1.2 MB on case RW-2026-000123; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-02-ITG | AC2 | Integration | Stored court notice; delete and replace through the service and on the WORM container; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-03-ITG | Regression of RWB-P5-E1024-APP AC3 | Integration | Synthetic appraisal report with write_once false and retention class GENERAL05Y; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-04-ITG | AC3 | Integration | Court notice with a second file and reason "Revised valuation"; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-05-ITG | Regression of RWB-P5-E1024-APP AC5 | Integration | Type BANK_STATEMENT, not in DOCTYPE-2026.11; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-06-ITG | AC5 | Integration | Word file renamed to .pdf; refused with MSG-P5-001; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-07-ITG | AC5 | Integration | PDFs of 26,214,400 and 26,214,401 bytes; the limit read through the P3 parameter contract; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-08-ITG | AC4 | Integration | Same file, same case and same type stored twice; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-09-ITG | Regression of RWB-P5-E1024-APP AC9 | Integration | Two parallel version requests on the same document; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-10-ITG | Regression of RWB-P5-E1024-APP AC10; criterion owned by RWB-P5-E1024-APP | Integration | Version request on an inactive version; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-11-ITG | AC8 | Integration | WORM container set to refuse writes; content 503 with MSG-GEN-006, then STORED after JOB-12; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-12-ITG | Regression of RWB-P5-E1024-APP AC12; criterion owned by RWB-P5-E1024-APP | Integration | Phone collector with scope OWN on another owner's case; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-15-ITG | AC7 | Integration | Store posted naming case RW-2026-000999; rwb-case returns 404; refused with no document row, no file and no event; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-16-ITG | §12 contract (operations, events and activities) | Integration | Contract test of the operations, events and activities of §12 against the published contracts; no fake; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-17-ITG | AC13 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1024-ITG-AC13); end-to-end: real services on the wave 1 contracts |
| TC-E1-024-18-ITG | AC14 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1024-ITG-AC14); end-to-end: real services on the wave 1 contracts |
| TC-E1-024-19-ITG | AC15 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1024-ITG-AC15); end-to-end: real services on the wave 1 contracts |
| TC-E1-024-20-ITG | AC16 | Integration | Run of AC1 to AC9 and AC13 to AC15 on synthetic set RWB-ITG-W1J01-ITG; section 8 rules BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15 and BR16 traced to the criteria and checked as AC16 states; end-to-end: real services on the wave 1 contracts |
| TC-E1-024-21-ITG | AC17 | Integration | Court notice for case RW-2026-000123 with the owning service delayed beyond the 2 s budget; store activity retried; end-to-end: real services on the wave 1 contracts |
| TC-ITG-E1024-ITG-01 | AC1 | Integration | Store the synthetic court notice on the existing case. Resolve its party using getCustomer with personKey. |

TC-E1-024-13-ITG, TC-E1-024-14-ITG, TC-E1-024-01-ITG, TC-E1-024-02-ITG, TC-E1-024-04-ITG, TC-E1-024-06-ITG, TC-E1-024-07-ITG, TC-E1-024-08-ITG, TC-E1-024-11-ITG, TC-E1-024-15-ITG and TC-E1-024-16-ITG are the copies this story signs off, for AC9, AC6, AC1, AC2, AC3, AC5, AC5, AC4, AC8, AC7 and the §12 contract. The other five are regression evidence for the component copy RWB-P5-E1024-APP, which owns their criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed. TC-E1-024-17-ITG, TC-E1-024-18-ITG and TC-E1-024-19-ITG are the copies this story signs off for AC13, AC14 and AC15. TC-E1-024-20-ITG and TC-E1-024-21-ITG are the copies this story signs off for AC16 and AC17. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, and the legacy Resilience level becomes NFR.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case, customer, party key and file, and no production data is read, copied or connected to.
- No personal data in events, logs, workflow history, fixtures or the report: document IDs, case IDs, party keys, type codes, parameter codes and counts only.
- No cross-service table read: every fact is read through an owner's contract or an owner's event, and the suite ships with no client for a service schema (DP-01, DP-05, ADR-021).
- No business value in the test code: the size limit, the allowed types, the write-once flag, the retention class and the type table version are rows in force, read through the P3 and P5 contracts.
- CloudEvents 1.0 with IDs and facts only on every asserted event, one DocumentStored per stored document, and the consumer inbox as the only dedupe (ADR-015).
- One hop and a 2 s budget on every REST call, with no service called through another service (ADR-020, DP-11).
- The suite never overwrites a WORM file and never writes a row: every write goes through the owning service.
- No production access and no production namespace: the run is pinned to SIT and refuses to start against any other environment.
- Clean-up in the same run: the synthetic set, the stored files and the versions are removed through the owner's own cleanup path, and the report records what was cleaned.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | `POST /api/recovery/document/v1/documents`, `GET /api/recovery/case/v1/cases/{caseId}`, DocumentStored | TC-E1-024-01-ITG, TC-E1-024-04-ITG, TC-E1-024-08-ITG |
| REQ-DCM-002 | rwb-document is the system of record, files in the WORM container | The four P5 document operations and the container assertion | TC-E1-024-01-ITG, TC-E1-024-11-ITG, TC-E1-024-14-ITG |
| REQ-DCM-003 | Legal types held write-once, with versions kept | `POST /api/recovery/document/v1/documents/{documentId}/versions`, MSG-P5-002 | TC-E1-024-02-ITG, TC-E1-024-04-ITG, TC-E1-024-09-ITG, TC-E1-024-10-ITG |
| REQ-DCM-008 | Documents searchable by case, type and date from the case record view | `GET /api/recovery/document/v1/documents/{documentId}` and the version list, SCR-30 through gateway-bff | TC-E1-024-01-ITG, TC-E1-024-06-ITG, TC-E1-024-07-ITG, TC-E1-024-12-ITG, TC-E1-024-13-ITG |
| REQ-ACA-006 | Every read checks role, capability area and scope and is written to the access log | The document read and the 403 refusal of MSG-P4-002 and MSG-P4-003 | TC-E1-024-13-ITG, TC-E1-024-12-ITG |
| REQ-DCM-015 | Container creation, backup and restore are platform work, not this suite | The WORM container is consumed as an external stub | TC-E1-024-02-ITG, TC-E1-024-11-ITG |
| REQ-DCM-017 | Custody of originals and electronic discovery stay in Epic 2 | Not exercised; declared out of scope in section 19 | None |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | DocumentStored on `rwb.document.events.v1` and DecisionRecorded on `rwb.decision-record.v1` | TC-E1-024-01-ITG, TC-E1-024-08-ITG, TC-E1-024-14-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed REST operations of section 12.2 and the contract preflight | TC-E1-024-01-ITG, TC-E1-024-07-ITG, TC-E1-024-13-ITG |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the suite asserts through contracts | All |
| DP-03 | Decision-record library and the shared topic | DecisionRecorded on `rwb.decision-record.v1` with decision code DOCATT | TC-E1-024-14-ITG, TC-E1-024-08-ITG |
| DP-06 | Parameters contract of rwb-case | INTAKE_MAX_FILE_MB and INTAKE_ALLOWED_TYPES read through `GET /api/recovery/case/v1/admin/parameters` | TC-E1-024-07-ITG, TC-E1-024-06-ITG |
| DP-07 | Reference-data contract of rwb-case | The document type list and the write-once flag read through the P3 contract | TC-E1-024-02-ITG, TC-E1-024-05-ITG |
| DP-09 | Outbox and inbox, owner's Kafka topic, CloudEvents | The two events of section 12.4 and the one-event-per-store count | TC-E1-024-01-ITG, TC-E1-024-08-ITG |
| DP-10 | Temporal workflow replaces the Quartz job | JOB-12 document intake as an event-started workflow with KEDA workers | TC-E1-024-11-ITG |
| DP-13 | `/api/recovery/<short>/v1` | Every consumed path of section 12.2 | TC-E1-024-01-ITG, TC-E1-024-07-ITG |
| DP-15 | Per-service Flyway sequence | On the P5 and P3 APP stories; the suite changes no schema | Every test case, at the preflight |
| DP-19 | gateway-bff composite route | SCR-30 and DocumentDetailPanel read through gateway-bff | TC-E1-024-01-ITG, TC-E1-024-12-ITG |
| RWB-E1-024 (legacy story) | Document store and index | The nine criteria of section 7 and the fourteen test cases of section 16 | All |

The legacy criteria AC1 to AC12 of RWB-E1-024 stay with RWB-P5-E1024-APP, which owns the contract and the full behaviour in `rwb_document`; they are not re-owned here and appear only as regression evidence in section 16. The integration dependencies are RWB-P5-E1024-APP, RWB-P3-E1018-APP and RWB-P1-E1001-APP.

Open decisions DL10 (Thai names for fields, labels and messages), DL11 (non-functional target values) and DL27 (storage, backup, legal hold and e-discovery for the document hub) apply to this story. The story builds on their recorded assumptions, confirmed by the programme directive: DL10 on ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL11 on ASM-0553, ASM-0703, ASM-1051 and ASM-1104; DL27 on ASM-1771, ASM-2532, ASM-2709 and ASM-2716. The decisions themselves remain open with their owners, and none of them blocks the build of this suite.

### 19. Out of scope

- The three application builds this run depends on: RWB-P5-E1024-APP, RWB-P3-E1018-APP and RWB-P1-E1001-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- The legacy criteria AC1 to AC12 at component level, which RWB-P5-E1024-APP owns.
- The central decision ledger, the hash chain and the access log into the decision log, which RWB-ITG-E1027-ITG proves.
- The upload form, the case document list and the search within a case (RWB-E1-026).
- Classification, field extraction and the automatic attach from the OCR intake (RWB-E1-050, RWB-E1-053, RWB-E1-032).
- Confirming or correcting an extracted field (RWB-E1-054).
- Retention periods, the retention job and the virus scan (RWB-E1-041).
- Container creation, backup and restore (REQ-DCM-015; platform work).
- Custody of originals (Epic 2, SCR-32) and electronic discovery (Epic 2, REQ-DCM-017).
- The build of the harness RWB-ITG-W1J01-ITG itself.
- The non-functional epic RWB-ITG-NFR, including load, resilience and performance testing.
