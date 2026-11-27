# RWB-P5-E1007-APP Integration adapters for outbound files

**Version 3 changes.**

- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1007-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P5-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P5-E1007-APP-16). Fit to a two-week sprint: Not specified in the source documents (DOR-RWB-P5-E1007-APP-15) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON; rwb-source-data contract (addressee and contact read, GAP-1162); rwb-document contract (store and read of the built file, GAP-1164) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-DRI-006, REQ-DRI-007, REQ-DRI-008) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: this is the P5 slice of legacy RWB-E1-007, split (rework). The legacy story's adapter, its `recovery_svc` identity, its SFTP session, its retry ladder and its exception queue stay in `rwb-integration` (RWB-P2-E1007-APP); this slice takes only the document-hub side of the same outbound path — the store of the built file, its claim-check reference, its retention class and the read back — in `rwb-document` with schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with `DocumentStored` only, task queue `rwb-document` and Java package `th.co.scb.ace.workbench.recovery.document`. The legacy data-lake statements of JOB-13 and JOB-15 are retired (DP-17). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 33 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the file that rwb-integration has built for an outbound interface to be stored once in the document hub with its manifest, its claim-check reference and the retention class of its type, served back to the flow that owns it through the claim-check link, and announced by one `DocumentStored` event**, so that **every outbound file of the Workbench is held in one place under write-once storage, is found again by its document ID, and never travels as content on a Kafka message or in a workflow payload**.

Inside `rwb-document` this is the document-hub side of the one outbound-file path of legacy RWB-E1-007:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the event name `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- Three operations carry the outbound path: `POST /api/recovery/document/v1/documents` takes the built file and its manifest and returns the document ID, the storage reference, the SHA-256, the state, the retention class and the claim-check link; `GET /api/recovery/document/v1/documents/{documentId}` and `GET /api/recovery/document/v1/documents/{documentId}/content` serve the metadata and the file back to its owner and to the requesting flow.
- rwb-document accepts the file that rwb-integration has built — the `deliverFile(manifest)` path of RWB-P2-E1007-CON — stores it through the platform storage product RWB-PLT-TE012-APP in Azure Blob with WORM, keeps the claim-check reference (`storage_ref`) and the manifest facts (`fileId`, `batchId`, `sha256`, record count), and applies the retention class of the document type in force. It publishes `rwb.document.DocumentStored.v1` to its outbox in the store transaction and consumes nothing.
- The claim-check link is a SAS link for one file, valid 15 minutes (Arch v5 slide 11). No file bytes and no personal value travel in an event, a workflow input or a log.
- There is no adapter of its own in this slice, no SFTP call, no file-system call and no inbound path: rwb-integration builds, sends and retries the file (RWB-P2-E1007-APP), and this slice stores and serves it.
- There is no data lake: INT-19 and INT-20 carry no lake target; the reporting extract is delivered to rwb-reporting through `deliverFile` and the decision and outcome feed is continuous Kafka ingest in rwb-decision (DP-17).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1027; ASM-1959); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

This slice owns no legacy acceptance criterion: AC1 to AC7 of RWB-E1-007 belong to RWB-P2-E1007-APP, which builds, sends, retries and escalates the file. The six criteria of section 7 are new under D-RCV-60 and test only the document-hub side stated here (GAP-1027; ASM-1951).

### 2. Business rationale

The outbound file is the largest payload on the outbound path: the WIN registered-mail notice file (INT-14), the debt-buyer data tape (INT-25), the reporting extract that is now delivered to rwb-reporting (legacy INT-19) and the decision and outcome feed that is continuous Kafka ingest in rwb-decision (legacy INT-20). Only one of those is a message-sized fact; the rest are files of many megabytes. The claim-check keeps the bytes off the bus, WORM keeps a legal file from being altered after it is stored, and the retention class of the type fixes how long the evidence is kept. The P5 measure of this path is therefore the document hub's own storage and read, not the transport: a file that is stored once, found by its document ID and read back with the same SHA-256.

The behaviour the business asked for is unchanged; only the seams moved. A file that cannot be built because today's ACE batch is not complete is still held by rwb-integration; a transfer that fails is still retried on the same three attempts and the same 5, 15 and 45 minute intervals; the case still moves to `RETRY_QUEUE` and then `EXCEPTION_QUEUE` and the owner still gets one task. What this slice adds is the place where the built file rests, and it is deliberately narrow: one store, one read pair, one event, no adapter.

Seven realignment changes:

1. One service, one schema: the store and the index move to `rwb_document` (DP-01), and no `recovery` table and no other `rwb_*` schema is read by this slice.
2. One login: the shared `recovery_svc` identity becomes the rwb-document login (DP-02); its name is Not specified in the source documents (GAP-1027; ASM-1959).
3. The claim-check replaces the in-process file hand-off: rwb-integration passes a manifest and follows a SAS link for one file, valid 15 minutes, instead of a file path on a shared folder (Arch v5 slides 8 and 11; ASM-1956).
4. WORM through the platform storage product: the file is written to `rwb-docs-legal` when its type is write-once and to `rwb-docs` otherwise, at `{container}/{caseId}/{documentId}/v1`, through RWB-PLT-TE012-APP (ASM-1957).
5. The document type table is the source of the retention class and the write-once flag: version `DOCTYPE-2026.11` in force, never a value typed in code or taken from the caller.
6. The event is the announcement: `rwb.document.DocumentStored.v1` is written to the outbox in the store transaction (DP-09) and carries IDs and facts only. No lake copy and no lake row exist (DP-17).
7. The two file statements of the legacy scheduler are retired, not restated: JOB-13 (decision log copy to the lake) is continuous Kafka ingest in rwb-decision and JOB-15 (reporting extract to the lake) is a `deliverFile` request to rwb-reporting (Arch v5 slide 44; DP-17). JOB-10 (WIN notices, 16:00) is owned by rwb-comms, with rwb-integration building the file. INT-19 and INT-20 are removed with no target in this service. rwb-integration registers no Schedule and provides the delivery capability the owning service calls.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E1007-CON | The published contract of the requesting side: the `deliverFile(manifest)` activity with the claim-check manifest (`fileId`, `batchId`, `sha256`, `recordCount`, `interfaceId`, `businessDate`, `caseIds`, `idempotencyKey`, the claim-check link and the requesting service), the OpenAPI shape of the store request, and the `FileDelivered` and `FileFailed` schemas on the rwb-integration topic `rwb.integration.events.v1`. No P2 operation is called by this slice: the contract is what the store request and the manifest must accept |
| RWB-P5-E1024-APP | The store contract of the document hub: `POST /documents`, the Document shape, the error envelope with `messageId`, the `Idempotency-Key` rule and the `copyPending` activity of `DocumentIntakeWorkflow`. This slice builds and tests against it as a fake and lists it in no H dependency (GAP-1027; ASM-1955) |
| RWB-P3-E1018-CON (consumed, not in C) | `GET /api/recovery/case/v1/cases/{caseId}` on `rwb-case`, one hop with a 2 s timeout, so the scope check of the store never reads a case table (DP-11). It is not listed in this slice's contract dependencies in the story JSON (GAP-1027; ASM-1958) |
| RWB-PLT-TE012-APP (no X dependency listed) | The platform storage product: the Blob containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, the managed identity and the WORM policy. The story JSON lists no external dependency for this slice (GAP-1027; ASM-1957) |

Business preconditions carried from the legacy story, unchanged in value:

- The interface configuration version "IF-2026.11" is in force, with interface rows INT-14 (WIN registered mail), INT-19 (reporting extract), INT-20 (decision and outcome feed) and INT-25 (debt-buyer data tape), each with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes. This slice reads no interface row: the interface ID and the business date arrive in the store request (DF-OPS-137 to DF-OPS-148 are read through the P2 contract, and no `rwb_integration` row is read by SQL).
- The document type table version "DOCTYPE-2026.11" is in force, with the six types DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE, each with its retention class and its write-once flag.
- The storage containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` exist in each environment with their immutability policy.
- The rwb-document login (DP-02) holds its grant on `rwb_document` only; the name is Not specified in the source documents (GAP-1027; ASM-1959).
- The feature flag `rwb.document.outbound-store` is on in the environment; its name is Not specified in the source documents (GAP-1027; ASM-1959).
- The outbound file's document type row and its retention class are data rows of `document_type`. Which type code an outbound interface file is stored under, and therefore which retention class it carries, is Not specified in the source documents (GAP-1027; ASM-1954).

The store story of the same lane, RWB-P5-E1024-APP, is earlier in the lane but is not an H dependency in this slice's JSON. This slice therefore tests against the store fake of RWB-P5-E1024-APP and adds no build dependency of its own (GAP-1027; ASM-1955).

### 4. Flow

1. rwb-integration (`OutboundFileWorkflow`, after `buildOutboundFile`) stores the built file with `POST /api/recovery/document/v1/documents`, a multipart request carrying the file, the document type, the source `GENERATED`, the case ID the request anchors, the interface ID, the business date and the manifest (`fileId`, `batchId`, `sha256`, `recordCount`, the case IDs and the requesting service), with the `Idempotency-Key` header of the `deliverFile` request.
2. `OutboundFileStoreService`: reads the case through the `rwb-case` contract `GET /cases/{caseId}` (one hop, 2 s timeout) and refuses the store when the case is not found or not in scope, so no case table of another service is read (DP-01, DP-11).
3. `DocumentTypeReader`: reads the type row of `document_type` in the version in force (`valid_from` and `valid_to`) and takes the allowed size and file-type rules of the document hub from `document_hub_parameter`, plus the retention class and the write-once flag of the type. Neither value is taken from the caller. The row of the outbound interface file type is loaded with the type table; its code is Not specified in the source documents (GAP-1027).
4. `OutboundFileStoreService`: checks the file content signature against the allowed types (PDF, JPG, PNG) and the size against the limit of 25 MB; refuses a file that fails either check before any row is written (X2, X3).
5. `StorageClient`: generates the document ID, then calls the platform storage product RWB-PLT-TE012-APP, which writes the file to `rwb-docs-legal` when the type is write-once and to `rwb-docs` otherwise, at `{container}/{caseId}/{documentId}/v1`. The path is deterministic, so a repeat of the same request writes the same path and the product answers it idempotently; a failed or refused write ends the store here, before any database row.
6. `OutboundFileStoreService`, one transaction in `rwb_document` after the accepted write: inserts the `document` row with source `GENERATED`, `storage_ref`, `content_sha256` from the manifest, `doc_version` 1 and state `STORED`, and writes the `rwb.document.DocumentStored.v1` row to the outbox (DP-09). The legacy decision record of the store is the DOCATT record of RWB-P5-E1024-APP's library, written in the same transaction (DP-03). A failure here leaves the row and the event absent and the blob unreferenced.
7. `OutboundFileStoreController`: answers the store with the document ID, the storage reference, the SHA-256, the state `STORED`, the retention class and a SAS link for one file valid 15 minutes (ASM-1956).
8. A repeat of the same `Idempotency-Key` returns the document stored by the first call, with no second row and no second event (X5).
9. The requesting flow, or the owner of the case, follows the claim-check with `GET /documents/{documentId}` for the metadata and `GET /documents/{documentId}/content` for the file; the content read returns the same SHA-256 as the manifest, and each read is written to the PII access log by the ACE common module, never by this package.
10. The outbox relay (JOB-11, the platform relay of DP-09) publishes `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` once per committed store, keyed by `caseId`, with IDs and facts only and no file content.

The case ID the store request anchors is `document.case_id`, which the schema requires; an outbound batch file covers 85 notices on 85 cases, and which case anchors the document row is Not specified in the source documents (GAP-1027; ASM-1953). The case IDs of the file travel in the manifest and in the `DocumentStored` payload is only the anchor case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document type of the file is not in `document_type` in force, or its retention class cannot be resolved from the type row | The store is refused with 422 before any row, any upload and any outbox row; nothing is stored | MSG-P5-006 | AC4 |
| X2 | The file content is not PDF, JPG or PNG | The store is refused with 415; nothing is written to a container or to a table | MSG-P5-001 | None (inherited from RWB-P5-E1024-APP AC6) |
| X3 | The file is larger than the size limit in force (25 MB, from `document_hub_parameter`) | The store is refused with 413; nothing is stored | MSG-P5-017 | AC4 |
| X4 | The platform storage product RWB-PLT-TE012-APP does not answer, or refuses the write | The store is refused with 503 before the database transaction opens; no document row and no outbox row exist; the retry belongs to the caller (RWB-P2-E1007-APP), which retries the attempt on the intervals of `interface_config` | MSG-GEN-006 naming "Document storage" | AC5 |
| X5 | The same `Idempotency-Key` is presented again | The document stored by the first call is returned; one `document` row and one `DocumentStored` event exist for it | None | AC3 |
| X6 | Two store requests for the same interface, business date and manifest arrive at the same time | One holds the unique key and the other is answered with 409; exactly one row exists | MSG-GEN-004 | AC3 |
| X7 | A read names a document ID that does not exist | 404, with a not-found message whose ID is Not specified in the source documents (GAP-1027; ASM-1953) | None (message ID not specified) | AC7 |
| X8 | The claim-check link is used after its lifetime | The link is refused with 403 by the storage product and the reader asks for a new one with `GET /documents/{documentId}`; no second file and no stored copy is created | MSG-P4-002 | AC2 |
| X9 | The `rwb-case` contract does not answer within 2 s, or its breaker is open | The store is refused with 503 before any row; the breaker shields the case service; the retry belongs to the caller | MSG-GEN-006 | AC2, AC5 |
| X10 | A statement of this slice reads a table of another service, a `recovery` table or another `rwb_*` schema | The grant refuses the statement and the architecture boundary test fails the build; the case and the interface facts arrive through their contracts | None (pipeline log) | AC1, AC6 |

The legacy copy-failure path that leaves the row `COPY_PENDING` and retries it on the next intake run (FSD P5 AC-EXC-P5-001-03) is RWB-P5-E1024-APP's `copyPending` activity, not this slice's: X4 is the store refused before any row is left behind, and the caller's retry is the outbound retry ladder of rwb-integration (ASM-1955).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the published rwb-integration contract, the store fake of RWB-P5-E1024-APP, the `rwb-case` contract fake and the storage stub; no in-lane story is waited for |
| Negotiable | The type code of an outbound file, its retention class, the size limit, the container names, the 15-minute window and the interface facts are data rows or properties; the story fixes only the behaviour |
| Valuable | Every outbound file of the Workbench rests once in the document hub under write-once storage and is found and read again by its document ID |
| Estimable | One service slice, three operations, one store transaction, one event, two readers and six criteria |
| Small | One squad, one iteration with its tests |
| Testable | Each criterion of section 7 is one automated test against the fakes; the ten legacy cases of section 16 stay with the path |

### 7. Acceptance criteria

```gherkin
Feature: Integration adapters for outbound files — document-hub side

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has direction "OUTBOUND", max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given the business date is 2026-11-10
    Given document type table version "DOCTYPE-2026.11" is in force
    Given the document type of an outbound interface file is Not specified in the source documents (GAP-1027; ASM-1954) and is read from the type table in force
    Given storage containers "rwb-docs", "rwb-docs-legal" and "rwb-quarantine" exist
    Given the document hub parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
    Given the rwb-integration contract mock returns the manifest of "WIN_NOTICE_20261110.txt" for 85 notices with its fileId, batchId, SHA-256 and record count 85
    Given the rwb-case contract mock returns the case the store request anchors
    Given the storage product stub accepts the write and returns a storage reference

  Scenario: AC1 Store the built outbound file (new, D-RCV-60)
    Given the built outbound file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases for interface "INT-14" and business date "2026-11-10"
    Given the manifest carries the SHA-256 of the file and the record count 85
    When rwb-integration stores it with POST /api/recovery/document/v1/documents with source "GENERATED" and the manifest
    Then one document row exists with source "GENERATED", doc_version 1, content_sha256 equal to the SHA-256 of the manifest and state "STORED"
    Then the row carries the document type and the retention class of the type row in force
    Then the file is at "rwb-docs/{caseId}/{documentId}/v1", or at "rwb-docs-legal/{caseId}/{documentId}/v1" when the type is write-once
    Then the response carries the document ID, the storage reference, the SHA-256, the state, the retention class and a claim-check link valid 15 minutes
    Then rwb.document.DocumentStored.v1 is in the outbox of the store transaction with the document ID, the case ID, the document type, the source and the stored date

  Scenario: AC2 Claim-check read returns the stored file (new, D-RCV-60)
    Given the outbound file of AC1 is stored with its SHA-256
    When the requesting flow follows the claim-check with GET /api/recovery/document/v1/documents/{documentId} and then GET /api/recovery/document/v1/documents/{documentId}/content
    Then the metadata answer carries the document ID, the document type, the source "GENERATED", the interface ID "INT-14", the business date "2026-11-10", the retention class and the stored date
    Then the content read returns a file whose SHA-256 equals the SHA-256 of the manifest
    Then the claim-check link the store answered is valid for 15 minutes and for one file only
    Then the DocumentStored payload of the outbox row carries no file content and no personal value

  Scenario: AC3 A repeat with the same Idempotency-Key returns the first document (new, D-RCV-60)
    Given the outbound file of AC1 is stored under the Idempotency-Key of the "deliverFile" request
    When the same store request is presented again with the same Idempotency-Key and the same manifest
    Then the response carries the document ID stored by the first call
    Then one document row exists for the interface and business date and one DocumentStored event exists for it
    Then no second upload and no second outbox row is written

  Scenario: AC4 A type or a retention class that is not in force is refused (new, D-RCV-60)
    Given an outbound file whose document type is not a type of the type table version in force
    When rwb-integration stores it with POST /api/recovery/document/v1/documents
    Then the store is refused with 422 and MSG-P5-006
    Then no document row, no container write and no DocumentStored event exists for it
    When a file of 26,214,401 bytes is stored with a type in force
    Then the store is refused with 413 and MSG-P5-017 showing 25 MB

  Scenario: AC5 The storage product is not available (new, D-RCV-60)
    Given the platform storage product RWB-PLT-TE012-APP refuses the write or does not answer
    Given the built outbound file "WIN_NOTICE_20261110.txt" for interface "INT-14" and business date "2026-11-10"
    When rwb-integration stores it with POST /api/recovery/document/v1/documents
    Then the store is refused with 503 and MSG-GEN-006 naming "Document storage"
    Then no document row and no DocumentStored event exists for the file
    Then the retry of the store belongs to the caller and follows the attempts and intervals of interface "INT-14"

  Scenario: AC6 No data lake anywhere on the path (new, D-RCV-60)
    Given the interface configuration version "IF-2026.11" is in force
    When every interface row and every store and read of this slice are inspected
    Then every interface row has direction "OUTBOUND"
    Then interface "INT-19" and interface "INT-20" name no lake target
    Then no lake file, no lake copy and no lake delivery row exists for any outbound file
    Then the reporting extract is delivered to rwb-reporting through "deliverFile" and the decision and outcome feed is continuous Kafka ingest in rwb-decision

  Scenario: AC7 A read of a document ID that does not exist is refused with 404 (new, D-RCV-60)
    Given no document row exists with the document ID named in the read
    When the requesting flow reads GET /api/recovery/document/v1/documents/{documentId} with that document ID
    Then the read is refused with 404 and a not-found problem response whose message ID is Not specified in the source documents (GAP-1027; ASM-1953)
    Then no document row, no container write and no DocumentStored event is created by the read

  Scenario: AC8 Error answers 403 and 404 of the provided read operations (new, D-RCV-60)
    Given the outbound file of AC1 is stored with its SHA-256
    When a caller without the Documents right or outside scope reads GET /api/recovery/document/v1/documents/{documentId}
    Then the read is refused with 403 and MSG-P4-002
    When the requesting flow reads GET /api/recovery/document/v1/documents/{documentId} with a document ID that does not exist
    Then the read is refused with 404 and a not-found problem response whose message ID is Not specified in the source documents (GAP-1027; ASM-1953)
    Then no document row, no container write and no DocumentStored event is created by the read
```

AC1 to AC6 are new under D-RCV-60 and test only the document-hub side of the outbound path. They do not restate AC1 to AC7 of RWB-E1-007, which RWB-P2-E1007-APP owns and which keep their legacy values. Every business value inside the six criteria is a legacy value: the interface "INT-14", the business date "2026-11-10", the file name "WIN_NOTICE_20261110.txt", the 85 notices, the 25 MB limit, the three attempts and the 5, 15 and 45 minute intervals, and the type table version "DOCTYPE-2026.11". The two values the sources do not fix — the document type of an outbound interface file and its retention class — carry the placeholder of the gap register, not an invented code.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The file of an outbound interface is stored once per interface ID and business date, and a repeat with the same Idempotency-Key returns the stored document with no second row and no second event | Legacy RWB-E1-007 AC6; R-UNI-40; Arch v5 slide 11; ASM-1953 |
| BR2 | The bytes are held only in the WORM storage of RWB-PLT-TE012-APP; the claim-check link and the manifest are the only hand-off, and no file content travels in an event, a workflow input or a log | Arch v5 slide 11; CTL-11; DP-09; BR10 of the legacy story |
| BR3 | The document type, its retention class and its write-once flag come from the type table version in force, never from the caller; a type or class not in force is refused | FSD P5 AC-EXC-P5-001-01; principle 1; DT02 |
| BR4 | The size limit and the allowed file types are document-hub parameter rows, read as data | FSD P5 VR-P5-001-1; legacy DF-OPS-143 read pattern; DT02 |
| BR5 | The store is idempotent twice over: the `Idempotency-Key` of the POST and a unique key on the interface, the business date and the manifest | Arch v5 slide 11; R-UNI-40; legacy AC6 |
| BR6 | No personal value and no address of a party enters `DocumentStored`; the payload carries the document ID, the case ID, the document type, the source and the stored date | CTL-11; Arch v5 slide 11; legacy BR10 |
| BR7 | No table of another service is read: the case comes from the `rwb-case` contract, the interface facts from the store request and its manifest, and the interface rows stay in `rwb_integration` | DP-01; DP-11; Arch v5 slides 13 and 37 |
| BR8 | There is no data lake: INT-19 is a `deliverFile` request to rwb-reporting and INT-20 is continuous Kafka ingest in rwb-decision; no lake file, lake copy or lake delivery row exists | DP-17; Arch v5 slides 37 and 44 |
| BR9 | The outbox row is the event: `DocumentStored` is written in the store transaction and published by the relay once per committed store, keyed by the case ID | DP-09; Arch v5 slides 11 and 22 |
| BR10 | Disposal belongs to the retention run of the document type, not to this slice: JOB-17 of rwb-document is RWB-P5-E1017-APP and the class stored here is the input of that run | Arch v5 slide 44; FSD P5 A2.17; ASM-1954 |

Rule statements of the target service:

- BR1 and BR5 are executed in `rwb_document` only: the stored response of the POST is keyed by the `Idempotency-Key` header, and the unique key on interface ID, business date and manifest answers 409 to a concurrent second store. No foreign schema is read (DP-01).
- BR2 is executed by the service holding the storage reference and the hash and never a copy of the bytes, and by the container's own WORM policy at RWB-PLT-TE012-APP.
- BR3 and BR4 read the type row and the two parameter rows in the version in force; neither the type code, the retention class, the write-once flag, the size limit nor the allowed types is written in code.
- BR7 is executed by the `rwb-case` contract read of the store and by the manifest that carries the interface facts; this slice holds no grant on `rwb_integration`, `recovery` or another `rwb_*` schema, and the boundary test fails the build on any violation.
- BR9 is executed by the outbox library of DP-09 inside the store transaction: the row, the checks and the event commit together or not at all.
- BR10 is executed by storing the class on the row and by naming JOB-17 as the owner of the disposal decision; this slice deletes nothing.

### 9. State transitions

The document record state (standard column `state`) on the outbound store path:

| From | Event | Condition | To |
|---|---|---|---|
| (no row) | the storage product accepts the write at `{container}/{caseId}/{documentId}/v1` and the store transaction commits with the checks and the outbox row | The read checks pass and the type is in force | `STORED` |
| (no row) | the storage product does not answer or refuses the write | X4 ends the store before the transaction opens | (no row) |
| `STORED` | a repeat with the same `Idempotency-Key` | The first store committed | `STORED` (the existing row is returned; no transition) |
| `STORED` | a second store of the same interface, business date and manifest under a different key | The unique key holds | `STORED` (refused with 409; no new row) |

The state `COPY_PENDING` is not left behind by this slice: the blob is written before the row, so an outbound file is `STORED` when its row exists. The `COPY_PENDING` path of the legacy copy failure — the row first and the copy after commit, retried by the `copyPending` activity — is RWB-P5-E1024-APP's and is entered only by the paths of that story (ASM-1955).

A write-once outbound document has no transition out of `STORED`: no delete, no content replace and no overwrite of its blob path. An outbound file is never superseded by a new version inside this slice; a corrected file is a new interface run with its own business date. No case state changes: this slice writes no case row and raises no task, and the route state of the cases of the file belongs to RWB-P2-E1007-APP and `rwb-case`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-integration service identity, through its own login (DP-02) | Stores the built file and follows the claim-check link; reads the metadata and the content it stored |
| the rwb-document login (DP-02) | Writes the `document` row, the upload and size checks and the outbox row; calls the storage product; publishes `DocumentStored` |
| RW-PLATADM, platform administrator | Reads the stored outbound file and its state (Documents R) |
| RW-DATASTEW, data steward | Reads the stored outbound file and its state; receives the held-file and failed-file alerts of the path (Documents R) |
| RW-AUDIT, RW-COMPLY | Read the stored file, its metadata and its fingerprint (Documents R) |
| RW-CASEOWN, RW-LITOFF and the other case roles | Read a file of their case inside their scope (Documents R) |
| the storage product identity of RWB-PLT-TE012-APP | Writes the blob, holds the WORM policy and answers the claim-check link |
| Nobody | Deletes or changes a write-once stored outbound file, or reads a file outside scope |

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-1027; ASM-1959); the story refers to "the rwb-document login (DP-02)". The authorisation decision is taken by the `rwb-access` authorise check (DP-08) and consumed as the cached permission decision the service holds; each operation calls that check before it reads or writes. This slice adds no guard of its own and refuses with 403 and MSG-P4-002 as the legacy endpoints did.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` (P5, `rwb_document`) | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Write |
| DF-DOC-025 | `document` (P5) | previous_version_id | Write |
| DF-DOC-026 | `document` (P5) | content_sha256 | Write |
| Standard columns | `document` (P5) | state, is_active, version, created_at, created_by, updated_at, updated_by | Write |
| DF-REF-219 | `document_type` (P5) | doc_type_code | Read |
| DF-REF-222 | `document_type` (P5) | write_once | Read |
| DF-REF-223 | `document_type` (P5) | retention_class | Read |
| DF-REF-229 | `document_type` (P5) | table_version | Read |
| DF-REF-245 | `document_hub_parameter` (P5) | param_code | Read |
| DF-REF-246 | `document_hub_parameter` (P5) | param_value | Read |
| DF-OPS-137 to DF-OPS-148 | `interface_config` (P2, read through the P2 contract and the store request only) | interface_id, direction, transport, file_pattern, data_product, max_attempts, retry_intervals_min, owner_role, alert_role, valid_from, valid_to | Read through the P2 contract |
| DF-CAS-001 | `recovery_case` (P3, read through the `rwb-case` contract) | id | Read through the P3 contract |
| (outbox) | outbox library table in `rwb_document` (PLT library) | the `DocumentStored` row | Write |
| (inbox and idempotency) | `processed_event` and the idempotency row in `rwb_document` (PLT library) | the stored response of the POST | Write |

Field IDs are those of the Logical Data Model and Data Dictionary and the TSD P5 T3.1 tables. The legacy login name `recovery_svc` is not a field or entity of LDM v9 or Data Classification v5 and is not a data field of this slice. The interface facts of DF-OPS-137 to DF-OPS-148 are not read by SQL: no `rwb_integration` row is read by this service, and the interface ID, the business date and the manifest arrive in the store request (DP-01). No `rwb_case` row is copied and no `recovery.v_ace_*` view is read by this service. `document_intake` is not written by this slice: an outbound file is built by another service and has no intake item. Personal data never enters the event payload, the workflow input or the log; the file content is never logged, only its name, its record count and its SHA-256.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/document/v1`; owner rwb-document (P5).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/documents` | Stores the file built by rwb-integration: multipart with the file, the document type, the source `GENERATED`, the case ID, the interface ID, the business date and the manifest; answers the Document with documentId, storageRef, sha256, state, retentionClass and the claim-check link | Documents C, service identity of rwb-integration | `Idempotency-Key` required; a repeat returns the first document; 409 on a concurrent store of the same interface, business date and manifest |
| GET | `/documents/{documentId}` | Metadata of the stored file: documentId, caseId, documentType, source, interfaceId, businessDate, retentionClass, writeOnce, docVersion, contentSha256, state, storedAt, and a fresh claim-check link | Documents R, scope applied | Not applicable |
| GET | `/documents/{documentId}/content` | The stored file as `application/octet-stream`; 503 while the row is in the `COPY_PENDING` state of RWB-P5-E1024-APP's copy path | Documents R, scope applied | Not applicable |

The request and response field names are fixed by RWB-P2-E1007-CON on the caller side and by the store contract of RWB-P5-E1024-APP inside this service, which also declares `POST /documents` as the create with an upload link for a browser-built document; the multipart shape that carries a file built by another service is settled there (GAP-1027; ASM-1955). Errors: 401 no session (message ID Not specified in the source documents (DOR-RWB-P5-E1007-APP-8)); 403 no Documents right or outside scope (MSG-P4-002); 404 unknown document (message ID Not specified in the source documents (CG-ALL-5739; GAP-1027; ASM-1953)); 409 concurrent store (MSG-GEN-004); 413 size above the limit (MSG-P5-017); 415 file type not allowed (MSG-P5-001); 422 type or class not in force (MSG-P5-006); 503 storage product or `rwb-case` unavailable (MSG-GEN-006). Every error is an RFC 9457 problem response with `messageId`.

#### 12.2 REST operations consumed

| Operation or contract | Path | Owner | Use |
|---|---|---|---|
| RWB-P2-E1007-CON | No operation is called | rwb-integration (P2) | The `deliverFile` manifest, the `FileDelivered` and `FileFailed` schemas on `rwb.integration.events.v1`, and the store request shape this slice must accept. The contract is consumed as a document, not as a call |
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case exists and is in the caller's scope; one hop, 2 s timeout, breaker per downstream (DP-11). Consumed, not listed in C (GAP-1027; ASM-1958) |
| RWB-P5-E1024-APP store contract | `/documents`, `/documents/{documentId}`, `/documents/{documentId}/content` | rwb-document (P5) | The published store contract of this service, used as the fake this slice builds and tests against (GAP-1027; ASM-1955) |

No other operation is called. The interface rows, the retry ladder, the attempt count and the exception queue stay in rwb-integration; this slice never calls them and reads none of their tables.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 | caseId | documentId, caseId, documentType, source, storedAt |

CloudEvents 1.0 envelope in binary mode; no personal data and no file content. The event is written to the outbox in the store transaction, so it exists exactly when the document row exists; the relay publishes it once per committed store and the consumers `rwb-agent` and `rwb-case` dedupe through their inbox (DP-09; Arch v5 slides 42 and 43). No other event is published by this slice.

#### 12.4 Events consumed

None. This slice consumes no Kafka event. `DocumentFieldsExtracted` is published by the extraction path and `DocumentStored` is consumed by `rwb-case` and `rwb-agent`, not here.

#### 12.5 Workflows and activities

None in this slice. The `copyPending` activity of `DocumentIntakeWorkflow` — the activity that copies a `COPY_PENDING` document and sets the state `STORED` — belongs to RWB-P5-E1024-APP and is named here only. The outbound store is a synchronous transaction plus one call to the storage product, with no Temporal workflow of its own and no workflow payload carrying a file.

#### 12.6 Schedules

None. JOB-11 is the platform outbox relay of DP-09, in every service; JOB-10 is the WIN file window of the bank Airflow scheduler, which reaches rwb-integration and not rwb-document; JOB-17 is the retention run of rwb-document and belongs to RWB-P5-E1017-APP. The 15-minute document-intake Schedule of JOB-12 belongs to RWB-P5-E1024-APP.

#### 12.7 Tables owned

| Table or object | Schema | Owner | Use in this story |
|---|---|---|---|
| `document` | `rwb_document` | P5 | The one row per stored outbound file: metadata, storage reference, hash, retention class, state |
| `document_type` | `rwb_document` | P5 | Read only: the type row in the version in force (the load is RWB-P5-E1025-APP's) |
| `document_hub_parameter` | `rwb_document` | P5 | Read only: the size limit and the allowed file types |
| outbox, inbox and idempotency library tables | `rwb_document` | PLT library, created in `rwb_document` | The `DocumentStored` row, the inbox and the stored response of the POST |

No foreign-schema table is read (DP-01). No ACE view is read by this service. `document_field`, `document_intake` and `document_text` are not written by this slice.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-integration contract fake | RWB-P2-E1007-CON | The `deliverFile` manifest of "WIN_NOTICE_20261110.txt" for 85 notices, the interface ID and business date, the `FileDelivered` and `FileFailed` schemas, and one delayed answer beyond 2 s |
| document store fake | RWB-P5-E1024-APP | The store, the metadata read, the content read, the Document shape, the error envelope and the `copyPending` state, so this slice builds with no in-lane wait |
| rwb-case case fake | RWB-P3-E1018-CON | The case read, the scope check, the 404 and the 2 s timeout of X9 |
| storage product stub | RWB-PLT-TE012-APP | The accepted write and the storage reference, the WORM refusal, the expired link of X8 and the outage of X4 |
| rwb-source-data contract fake | Not specified in the source documents (CG-ALL-5748) | The person and contact facts of the 85 notices of TC-E1-007-02 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 1 | The store, the metadata read and the content read on `/api/recovery/document/v1`; the case read of `rwb-case` |
| Kafka | Published 1, consumed 0 | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` through the outbox |
| Temporal | 0 | No workflow and no activity of its own; the `copyPending` activity is RWB-P5-E1024-APP's |
| File | 1 | Azure Blob with WORM through RWB-PLT-TE012-APP at `{container}/{caseId}/{documentId}/v1`; claim-check link only |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/outbound`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OutboundFileStoreController | Controller | The three operations of 12.1; validation; the RFC 9457 problem response with `messageId`; the access check and the scope |
| OutboundFileStoreService | Service | The case contract read, the type and parameter reads, the signature and size checks, the idempotency and unique-key rule, the row, the checks and the outbox row in one transaction, and the call to the storage product |
| DocumentTypeReader | Repository | Reads `document_type` in the version in force by `valid_from` and `valid_to` |
| StorageClient | Client | The storage product RWB-PLT-TE012-APP: the write, the WORM refusal, the open, and the SAS link valid 15 minutes for one file |
| DocumentRepository | Repository | Reads and writes `document` only, with `version` as the optimistic lock |
| IdempotencyRepository | Repository | The stored response of the POST by `Idempotency-Key` and the unique key on interface, business date and manifest |
| OutboundStoreBoundaryTest | Test | ArchUnit rule: no SFTP, no file-system call, no HTTP client to a party, and no read of any schema other than `rwb_document` |

**Database.**

- Writes `document` (DF-DOC-001 to DF-DOC-011, -025, -026 and the standard columns) and the library objects of outbox, inbox and idempotency.
- Reads `document_type` (DF-REF-219, -222, -223, -229) and `document_hub_parameter` (DF-REF-245, -246).
- One Flyway step in the per-service sequence (DP-15) if the library objects or the unique key on interface, business date and manifest are not already in place: `ux_document_interface_run` on the manifest reference and the business date. No other new table.

**Configuration and reference data.**

- Container names `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` as properties per environment.
- Parameters are local P5 rows read from `document_hub_parameter` (DF-REF-245, DF-REF-246); no list is copied here. DP-06 is not among the patterns applied in this slice.
- `CLAIM_CHECK_MINUTES` = 15 as a property; 15 is the architecture value of Arch v5 slide 11 and is not changed here (ASM-1956).
- The size limit and the allowed file types as `document_hub_parameter` rows read as data (`INTAKE_MAX_FILE_MB` = 25, `INTAKE_ALLOWED_TYPES` = PDF, JPG, PNG).
- The type mapping of an interface file as a data row of `document_type`; its code and its retention class are Not specified in the source documents (GAP-1027; ASM-1954).
- Feature flag `rwb.document.outbound-store`; the name is assumed (ASM-1959).

**Open decisions.** DL06 is open. It is carried with assumptions ASM-0189, ASM-2559, ASM-2608 and ASM-2776, which this slice relies on until DL06 is decided.

**Build steps**

1. Build `DocumentTypeReader` and the parameter read, with the version-in-force rule and its boundary-date test; refuse an unknown type or a missing class with 422 and MSG-P5-006.
2. Build the content-signature and size checks (415 MSG-P5-001, 413 MSG-P5-017) and the case contract read with its 2 s timeout and breaker.
3. Build `StorageClient` with the deterministic path `{container}/{caseId}/{documentId}/v1`; test the write to `rwb-docs-legal` for a write-once type, the write to `rwb-docs` otherwise, the WORM refusal and the outage of X4, and that a refused write leaves no row.
4. Build the store transaction: the `document` row in `STORED` with `storage_ref` and `content_sha256`, the checks, the idempotency record and the `DocumentStored` outbox row; test that a forced failure leaves no row and no event.
5. Build the metadata and content reads with the claim-check link, the 15-minute window and the re-issue on request; test X7 and X8.
6. Build the three operations with the access check and add `OutboundStoreBoundaryTest` to the pipeline; run the six criteria of section 7 against the fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency in this slice |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_document`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none added here; the library is used through RWB-P5-E1024-APP (ASM-1955) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through the owner's contract; this service owns no ACE view and holds no grant | none; this slice reads no ACE data |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the lists stay rows | none added here; the type table and the parameter rows are local P5 tables |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the service topic, retry and `.dlt` | none added here; the outbox library is part of the store contract of RWB-P5-E1024-APP (ASM-1955) |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | none; this slice registers no workflow, and the `copyPending` activity is RWB-P5-E1024-APP's |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | C RWB-P2-E1007-CON; the `rwb-case` read is consumed and not listed in C (ASM-1958) |
| DP-16 | `recovery.integration.adapter` | The rwb-integration contract | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed: delivery to rwb-reporting through `deliverFile` and continuous ingest in rwb-decision | none; gap if a lake file were needed |
| DP-19 | Screen, ace-web | gateway-bff composite route | none added here; the stored file is shown on SCR-30 through the route of RWB-P5-E1024-APP |

DP-16 is applied as a consuming rule, not as a build dependency on the P2 app story: this slice imports the published contract and its fake and never the P2 code. DP-17 resolves to "no lake target, no lake file, no lake row" and is applied to the retired JOB-13 and JOB-15 statements. INT-19 and INT-20 have no target and no replacement in this service; no source restates the two lake files on a target path, and the two lake extracts are dropped. The three DPs that normally add an H dependency — DP-03, DP-09 and DP-10 — add none here, because the library and the workflow are already inside the store contract this slice consumes; that is the reason the metadata lists no build dependency, and it is recorded as ASM-1955.

**Done when.** The six criteria of section 7 pass against the fakes, the boundary test on the tables passes, a built file of 85 records is stored and read back with the same SHA-256 in SIT inside 2 seconds, and `rwb.document.DocumentStored.v1` is on the topic once per store with no personal data and no file content.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | The file content is not PDF, JPG or PNG | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-006 | The document type or its retention class is not in the type table in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-017 | The file is above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-GEN-004 | A concurrent store of the same interface, business date and manifest | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The storage product or the case contract is not available | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | A role without the Documents right, or a link used after its lifetime | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P2-001 | Named only: the outbound item moves to the exception queue in rwb-integration | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-P1-001 | Named only: data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. |

MSG-P2-001 and MSG-P1-001 are named here because they are the messages of the same path; this slice raises neither. MSG-P2-001 carries the Error and Message Standard v4 wording; MSG-P1-001 carries the Error and Message Standard v4 wording, placeholder included. Status mapping: 415 for MSG-P5-001, 413 for MSG-P5-017, 422 for MSG-P5-006, 409 for MSG-GEN-004, 403 for MSG-P4-002, 404 for the not-found message (Not specified in the source documents (CG-ALL-5739; GAP-1027; ASM-1953)), 503 for MSG-GEN-006. Delivery shape: every error is an RFC 9457 problem response with `messageId`, `detail` carrying the text with its placeholders filled and `instance` naming the request. For MSG-GEN-006 the {system} value is "Document storage" for a storage failure and "Case service" for a case-contract timeout; for MSG-P5-017 the {size} value is the `INTAKE_MAX_FILE_MB` parameter. A 404 carries a not-found message whose ID is Not specified in the source documents (GAP-1027; ASM-1953).

### 15. Screens and states

This slice has no screen and no screen state of its own. SCR-09 Exception queue is rwb-integration's and is named here only: the platform administrator lists and resends failed outbound items there, and nothing of that screen is built in this service. A stored outbound file appears on SCR-30 Case documents and in the case documents list of the case it anchors, served through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON) by the reads of 12.1; the tab, the list and the search belong to RWB-P5-E1026-APP and the detail panel to RWB-P5-E1024-APP. The claimant flow reads the file through the claim-check link and no screen is involved in that read. Screen states: SCR-09 has loading as in Screen Specifications v1 section SCR-09; empty, error and no access are Not specified in the source documents (CG-ALL-5749). SCR-30 has loading as in Screen Specifications v1 section SCR-30; empty, error and no access are Not specified in the source documents (CG-ALL-5750).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-10 | Legacy Access case of RWB-E1-007; the right check of the outbound path (BR7 of this story) | Component | RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend; refused with MSG-P4-002 |
| TC-E1-007-01 | Legacy AC1, BR1, BR8, BR9 | End to end | Synthetic INT-25 tape, 120 accounts; interface load with an INBOUND row |
| TC-E1-007-02 | Legacy AC2, BR2, BR10 | End to end | 85 synthetic notices with person_key and contact_key; rwb-source-data contract fake (§12.8) |
| TC-E1-007-03 | Legacy AC3, BR4, BR5, BR6 | End to end | Synthetic WIN file for 85 cases; SFTP stub failing three times |
| TC-E1-007-04 | Legacy AC4, BR3 | End to end | ALS batch FAILED for 2026-11-10; WIN file due at 16:00 |
| TC-E1-007-07 | Legacy AC7, BR7 | End to end | Event key EV-10:TRT-0001:v1 sent twice |
| TC-E1-007-08 | Legacy AC2 | End to end | One due item, two sender threads |
| TC-E1-007-09 | Legacy AC4; run by RWB-P2-E1007-APP | End to end | Item in EXCEPTION after 3 attempts |
| TC-E1-007-05 | Legacy inbound case, retired with the inbound file load; NFR assertion of absence, behaviour is ACE ingestion (EV-27 AceDataLate); closes when RWB-ACE-001 publishes its checks | NFR | Absence of the inbound adapter, the inbound folder listing, DQ-057, DQ-059, JOB-09 File loads, interface_run and interface_signoff; file missing at the cut-off (inbound; retired) |
| TC-E1-007-06 | Legacy inbound case, retired with the inbound file load; NFR assertion of absence, behaviour is ACE ingestion (EV-27 AceDataLate); closes when RWB-ACE-001 publishes its checks | NFR | Absence of the inbound adapter, the inbound folder listing, DQ-057, DQ-059, JOB-09 File loads, interface_run and interface_signoff; same file delivered twice (inbound; retired) |
| TC-E1-007-11 | P5 contract of section 12: the operations, events and activities of §12 (AC1 to AC6 of section 7) | Component | Contract fakes of §12.8; POST /documents, the GET reads and the DocumentStored schema |
| TC-E1-007-12 | P5 boundary of the tables of section 12.7 (ASM-3438) | Component | Boundary rows of document, document_type and document_hub_parameter, including the size limit and the allowed file types |
| TC-E1-007-13 | P5 AC7 of section 7 (read of a document ID that does not exist; X7 of section 5) | Component | GET /api/recovery/document/v1/documents/{documentId} with a document ID that has no row; expects 404 |
| TC-E1-007-14 | P5 AC8 of section 7 (403 of a caller without the Documents right; 404 of a missing document ID) | Component | Caller without the Documents right reads GET /api/recovery/document/v1/documents/{documentId}; the same GET with an unknown ID |

The Level column follows the mapping of Template and Rules §R7.2: the legacy level System becomes End to end, Access becomes Component. TC-E1-007-05 (file missing at the cut-off) and TC-E1-007-06 (the same file delivered twice) are the two inbound cases of the legacy story; their behaviour is ACE ingestion and EV-27 AceDataLate, and they are carried here as NFR rows that assert the absence of the inbound adapter, the inbound folder listing, DQ-057, DQ-059 and the run table; they close when RWB-ACE-001 publishes its own checks. The ten cases exercise the path of the legacy key, whose AC1 to AC7 are RWB-P2-E1007-APP's; the criteria that prove the P5 side are AC1 to AC6 of section 7. The `-ITG` copies of these test cases belong to RWB-ITG-E1007-ITG and are not listed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Until RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON publish, the cases run against the fake of each contract, and each fake is replaced by its real contract in the same iteration.

### 17. Guardrails

- No adapter, no SFTP session and no file-system call in this service: the file is built by rwb-integration, and the boundary test fails the build on any such call.
- No file bytes on a Kafka message, in a workflow input or in a log: the message carries the document ID, the case ID, the type, the source and the stored date, and the claim-check link carries the file for 15 minutes to its owner.
- No personal data in events, workflow inputs, logs or tests; a test file is synthetic and only its name, its record count and its SHA-256 are logged.
- No read of another service's tables (DP-01): the case comes from the `rwb-case` contract and the interface facts from the store request and its manifest; ACE data is reached only through the owner's contract, and this service reads no view.
- WORM: the service never overwrites a blob, every store is a new path at `{container}/{caseId}/{documentId}/v1`, and a write-once container refuses a change on its own.
- Idempotent twice over: the `Idempotency-Key` on the POST and the unique key on the interface, the business date and the manifest.
- The decision record, the row, the checks and the outbox row are one transaction; a failure stores nothing.
- No data lake, no lake target and no lake row anywhere on the path (DP-17).
- No inbound path: this service receives no file from a party, has no inbound folder and signs nothing off; the inbound load belongs to ACE ingestion (RWB-ACE-001).
- No business value in code: the type code, the retention class, the size limit, the allowed types, the container names and the 15-minute window are data rows or properties.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the views and leaves through ACE's paths | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE | TC-E1-007-01, TC-E1-007-02 |
| REQ-DRI-007 | Log every outbound file, retry, exception queue with an owner task | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40 | TC-E1-007-03, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06 | TC-E1-007-01, TC-E1-007-04 |

| Legacy reference | Where it is kept |
|---|---|
| Interface configuration version IF-2026.11 and interfaces INT-14, INT-19, INT-20, INT-25 | Metadata, sections 3, 7, 13, 14 |
| The WIN registered-mail notice file and the 85 notices of business date 2026-11-10 | Sections 3, 4, 7, 16 |
| Event DocumentStored and the topic `rwb.document.events.v1` | Sections 1, 4, 12.3, 12.9, 17 |
| Messages MSG-P5-001, MSG-P5-006, MSG-P5-017, MSG-GEN-004, MSG-GEN-006, MSG-P4-002, MSG-P4-003, MSG-P2-001, MSG-P1-001 | Section 14, exception paths |
| Rules R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-40 | Sections 8, 12.3, 18 |
| DP-16 and DP-17 | Sections 2, 12.2, 13, 17 |
| Containers `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine` and the path `{container}/{caseId}/{documentId}/v1` | Sections 1, 4, 7, 12.9, 13 |
| The 15-minute claim-check link of Arch v5 slide 11 | Sections 1, 2, 4, 7, 12.1, 13 |
| Legacy key RWB-E1-007 and the split into RWB-P2-E1007-APP and RWB-P5-E1007-APP | Metadata, sections 1, 3, 16, 19 |

### 19. Out of scope

- The build, the send, the retry ladder, the exception queue and the resend of the outbound file in rwb-integration (RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF, RWB-P2-E1007-OPS).
- The full document hub: the store capability, the index, the upload path, the versions, the custody and the review queue (RWB-P5-E1024-APP, RWB-P5-E1026-APP and the other P5 document stories).
- The document type table and its load (RWB-P5-E1025-APP), and the retention classes and the legal hold (RWB-P5-AD021-APP, RWB-P5-AD021-CON).
- The retention run and the disposal decision of a stored file (RWB-P5-E1017-APP; JOB-17).
- The OCR, classification and extraction path and the intake item, which an outbound file does not have (RWB-P5-E1049-APP and its siblings).
- The Win notice content and template (RWB-E2-021, P6) and the notice facts behind INT-14 (rwb-comms).
- The ACE views, the data products, their grants and the access log (RWB-P1-E1069-APP; rwb-access and ACE Common).
- The inbound source ingestion, its schedules, its checks and the ACE team sign-off (RWB-ACE-001).
- SCR-44 the interface and job monitor, and the full SCR-09 exception queue screen.
- The deployment: the Helm chart, the topic and DLT provisioning, the SFTP endpoints, the key store, the metrics, the dashboards and the runbook.
