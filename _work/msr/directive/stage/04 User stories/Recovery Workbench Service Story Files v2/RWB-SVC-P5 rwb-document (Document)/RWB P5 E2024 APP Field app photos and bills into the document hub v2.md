# RWB-P5-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Size | Not specified in the source documents (DOR-RWB-P5-E2024-APP-16); who sets it is Not specified in the source documents (DOR-RWB-P5-E2024-APP-16) |
| Contract baseline | RWB-P5-E2024-CON; contract version Not specified in the source documents (DOR-RWB-P5-E2024-APP-23); REST base /api/recovery/document/v1 |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1032-APP, RWB-P5-E1024-APP |
| Depends on (build) | RWB-P5-E2024-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1032-APP, RWB-P5-E1024-APP, RWB-P5-E1057-CON, RWB-P5-E1053-CON, RWB-P5-E1041-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-021) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the field-capture path of RWB-E2-024 moves into `rwb-document` with the schema `rwb_document`, the REST base `/api/recovery/document/v1`, the topic `rwb.document.events.v1`, the queue `rwb-document` in namespace `rwb-recovery`, the Java package `th.co.scb.ace.workbench.recovery.document` and the contract baseline RWB-P5-E2024-CON; the fifteen legacy criteria, the twelve exception paths, the ten business rules, the eleven messages and the seventeen test cases are kept word for word in intent and values. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E2024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **field collector**, I want **photos, bills and checklists captured in the field app to enter the document hub against the case, with location and time**, so that **an inspection is on the case the same day it is made**.

Inside `rwb-document` this is the field-capture capability of the document hub, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The operation is `POST /api/recovery/document/v1/cases/{caseId}/field-captures`, the legacy `POST /cases/{caseId}/field-captures` (API-P5-015 in TSD P5 T-A.1) on the service base of DP-01; its shapes, its statuses and its per-item result are fixed by the baseline RWB-P5-E2024-CON.
- The case, its entry date and the task that puts the case in the collector's scope arrive through the `rwb-case` contract `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E1018-CON, one hop, 2 s timeout, DP-11), never from a case table of another service and never from a `recovery_case` copy.
- The three parameters `CAPTURE_CLOCK_SKEW_MINUTES`, `CAPTURE_MAX_AGE_DAYS` and `CAPTURE_MAX_FILES`, and the intake parameters `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB`, are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON). The rows they resolve to stay in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5 (ASM-1879).
- The item kinds, the document types, the document sources, the capture kinds and the review states are read as reference data through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON): LOV-CAPTURE-KIND, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW. No list value is typed in code (ASM-1880).
- The scan runs through the scan operation of RWB-P5-E1041-CON in the same service (`POST /api/recovery/document/v1/scans`, `ScanResult` CLEAN or INFECTED with the 30 s budget that baseline declares), and never through a second scanning implementation of this story (ASM-1884).
- The document is stored through the store capability of RWB-P5-E1024-APP, which stays the only writer of the `document` table and the DOCATT decision record; this story passes the five capture values to the store in an optional capture block and writes no `document` row of its own (ASM-1877).
- A bill or a checklist enters OCR through the intake submit of RWB-P5-E1057-CON in the same service, which creates the `document_intake` item with source UPLOAD and the type the item kind gives, so the OCR pipeline of RWB-P5-E1049-APP reads it and the extraction of RWB-P5-E1053-CON fills the bill fields (ASM-1878).
- The decision is recorded through the local decision-record library of DP-03 (H RWB-PLT-E1027-CON; the central ledger contract is RWB-P7-E1027-CON) with decision code DOCATT, written in the same transaction as the store and the intake item. A failed record means nothing is stored for that item (MSG-P7-003, R-UNI-39; ASM-1886).
- The store's `rwb.document.DocumentStored.v1` (the legacy DocumentStored, EV-16) is written to the outbox in the store transaction and published by the relay (DP-09, H RWB-PLT-TE006-CON); the bill fields raise `rwb.document.DocumentFieldsExtracted.v1` through RWB-P5-E1053-CON (EV-17).
- The five capture columns are added to `document` by this service's own per-service Flyway step in `rwb_document` (DP-15, H RWB-PLT-E1044-CON), and the capture details on SCR-30 reach the screen through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1018; ASM-1877); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.
- The legacy feature flag `rwb.dochub.field-capture` is retired with the monolith and replaced by `rwb.document.field-capture` (ASM-1882).

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, twelve exception paths, ten business rules, eleven messages, authority, data fields, fifteen acceptance criteria and seventeen test cases, adapted to the target service's schema, topic, API base and contract baseline.

### 2. Business rationale

Inspection photos and utility bills are sent today by chat or carried back to the office, and the date and place of an inspection cannot be shown when it is questioned. This story takes each capture from the field app into the same malware scan, store, OCR and extraction path as other documents, attached to the case with the capture time and the GPS position, including captures made with no signal. It meets REQ-DCM-013 and gives the deed in lieu inspection step (WITH_FIELD_INSPECTION, R-DIL-22) and the repossessed vehicle photo record (CTL-38) their evidence on the case (FSD P5 A2.21).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01). No table of another service is read and no monolith table name survives.
2. The case is no longer read in process through `CaseDirectory`: it arrives through the `rwb-case` contract with a mock and a 2 s timeout (DP-11, ASM-1883), so the capture path builds against a published shape and its fake on Day 1.
3. The five capture values no longer sit on a document row this module writes directly: the store of RWB-P5-E1024-APP takes them in an optional capture block of its store request, so one writer owns the `document` table (ASM-1877).
4. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the store and the intake item and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger.
5. The malware scan is the published scan operation of the same service (RWB-P5-E1041-CON) with its declared 30 s budget, not a second scan client in this package (ASM-1884).
6. The intake item for a bill and a checklist is created through the intake submit of RWB-P5-E1057-CON, so the OCR pipeline of RWB-P5-E1049-APP and the extraction of RWB-P5-E1053-CON run unchanged on a capture (ASM-1878).
7. The three capture parameters and the two intake parameters arrive through the parameters contract, and the four lists through the reference-data contract (DP-06, DP-07); the document-hub parameter rows stay in `rwb_document`, which is P5's own store for them.
8. The stored event is written to the outbox inside the store transaction (DP-09); the five capture columns are created in the per-service Flyway sequence (DP-15); the capture details on SCR-30 are served through the gateway-bff composite route (DP-19).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2024-CON | The published baseline of the capture operation, the manifest, the seven-field item shape and the `FieldCaptureResult`, the four per-item statuses, the limits and the type rules as declared contract elements, the error envelope and the `Idempotency-Key` and `clientFileId` rules |
| RWB-P5-E1032-APP | The intake and match path of the same service, so a document stored here is attached to the case it names without a second matcher |
| RWB-P5-E1024-APP | The store: `DocumentStoreService`, the DOCATT record, the `document` row with its duplicate check on case, type and hash, and the outbox row |
| RWB-P5-E1041-CON | The scan operation `POST /api/recovery/document/v1/scans` with `ScanResult` CLEAN or INFECTED and its 30 s budget (DP-11 in-service) |
| RWB-P5-E1053-CON | The extraction operation, so a bill item is read with the UTILITY_BILL field list and a low-confidence field reaches review |
| RWB-P5-E1057-CON | The intake submit that creates the `document_intake` item for a bill or a checklist with source UPLOAD |
| RWB-PLT-E1027-CON | The decision-record library: the DOCATT record inside the caller's transaction, published on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1042-CON | The parameters client library for `CAPTURE_CLOCK_SKEW_MINUTES`, `CAPTURE_MAX_AGE_DAYS`, `CAPTURE_MAX_FILES`, `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-CAPTURE-KIND, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so the store row, the item and the event share one transaction (DP-09) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the capture migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes SCR-30 with the capture details of each document (DP-19) |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the five parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the four lists (DP-07) |
| RWB-P3-E1018-CON | The `rwb-case` contract `GET /cases/{caseId}`, with its fake, for the case, its entry date and its task (DP-11) |

Business preconditions carried from RWB-E2-024, in the target wording:

- RWB-E1-041 (`MalwareScanService.scanNow`) is done: in the target it is the scan operation of RWB-P5-E1041-CON in the same service, called before storage and never replaced by a second engine (ASM-1884).
- RWB-E1-024 (`DocumentStore.store`) is done: in the target it is RWB-P5-E1024-APP, called through its published store command with the optional capture block (ASM-1877).
- RWB-E1-049 (the `DocumentStoredListener` that creates the intake item for OCR) and RWB-E1-053 (`extractStep`) are done: in the target the intake item is created through the intake submit of RWB-P5-E1057-CON and the fields are read through the extraction operation of RWB-P5-E1053-CON (ASM-1878).
- RWB-E1-057 and RWB-E1-032 give the same intake path for files with no case; in the target that path is the same intake submit and the auto attach of RWB-P5-E1032-APP.
- The field app is a bank-managed mobile app that signs in with Entra ID as role RW-FIELDCOL and calls the Workbench API through gateway-bff. This platform is assumed: no open decision covers it; the field app route through gateway-bff is to be stated in RWB-PLT-N001-CON (GAP-0951). Agency field teams reach the Workbench only through the external gateway (DL03), which is not in this story.
- The document type table holds INSPECTION_PHOTO (no fields), INSPECTION_CHECKLIST (no fields) and UTILITY_BILL (bill_amount, due_date, account_ref), loaded through the RWB-E1-025 loader in the target type table of RWB-P5-E1025-APP (assumed; DL19).
- Rows in `document_hub_parameter`: CAPTURE_CLOCK_SKEW_MINUTES 5; CAPTURE_MAX_AGE_DAYS 30; CAPTURE_MAX_FILES 50; INTAKE_MAX_FILE_MB 25. Values assumed (DL11); the rows are read through the parameters contract of DP-06 (ASM-1879).
- The field collector has a task on the case, so the case is in Own scope; the task is read from the `rwb-case` answer (ASM-1883).
- The feature flag `rwb.document.field-capture` is on; it replaces the legacy `rwb.dochub.field-capture` (ASM-1882).
- The release date 31 December 2026 is the legacy one and is tentative (ASM-1881), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1881).

The store of RWB-P5-E1024-APP takes an optional capture block (`capturedAt`, `captureLatitude`, `captureLongitude`, `clientFileId`, `captureKind`) as a change of its request (GAP-1018; ASM-1877); whether it is additive within major version 1 is Not specified in the source documents (GAP-1018). The intake item is created by the intake submit of RWB-P5-E1057-CON, and RWB-P5-E1049-CON is read as the OCR pipeline that consumes the item. The baseline RWB-P5-E2024-CON declares the manifest as one JSON part named `manifest` and each file part named by its `clientFileId`; the item required set is `clientFileId`, `kind` and `capturedAt` (GAP-1019). A content type other than multipart/form-data is refused with 415; a refused type stays an item with status REFUSED and MSG-P5-001 at 201 (GAP-1019). The `Idempotency-Key` stored-answer window and the not-found message ID are Not specified in the source documents (GAP-1019) until the platform catalogue fixes them. The name of the rwb-document login is Not specified in the source documents (GAP-1018; ASM-1877). The field-app test client, the capture fixtures, the intake test profile, the SIT harness pack and the evidence format are Not specified in the source documents (GAP-0406). The legacy Decision D6.5 is the routing tag that produced a capture; each document-attach entry carries DOCATT as the value of LOV-DECISION (GAP-1283). Each stored document and each item the store refuses has one DOCATT entry; a refused item's entry carries result REFUSED and its message ID, and a DUPLICATE item resolves to the entry of the item received first (GAP-1284).

### 4. Flow

1. Field collector: captures photos, bills and the checklist in the field app; the app records for each file the device time and GPS position, and a client file ID.
2. Field app: when a signal is available, sends the captures for the case to `POST /api/recovery/document/v1/cases/{caseId}/field-captures` with a manifest of the items.
3. System: checks the role, the right and the case scope, and that every manifest item has one file and every file has one manifest item. The case, its entry date and the collector's task are read through the `rwb-case` contract (DP-11).
4. System: for each item, checks the client file ID against items already received for the case; a repeat returns the earlier result, and the `Idempotency-Key` of the request covers the whole sync (12.1).
5. System: checks file type and size against `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB`, checks the capture time against the receipt time plus `CAPTURE_CLOCK_SKEW_MINUTES`, the case entry date and `CAPTURE_MAX_AGE_DAYS`, writes the file to the intake container `rwb-quarantine`, and calls the scan operation of RWB-P5-E1041-CON.
6. System: on CLEAN, calls the store of RWB-P5-E1024-APP with the case, the type from the item kind (photo, bill, checklist), source UPLOAD, the file and its hash, and the optional capture block with `captured_at`, `capture_latitude`, `capture_longitude`, `client_file_id` and `capture_kind`. The store writes the `document` row, the DOCATT decision record and the `rwb.document.DocumentStored.v1` outbox row (ASM-1877).
7. System: in the same transaction as the store, the store writes the five capture values on the document, so the capture time, the position and the client file ID exist exactly when the document exists.
8. System: submits the bill and the checklist item to the intake submit of RWB-P5-E1057-CON, which creates the `document_intake` row with source UPLOAD and the type the item kind gives; the OCR pipeline of RWB-P5-E1049-APP reads it and, for a UTILITY_BILL, the extraction of RWB-P5-E1053-CON writes `bill_amount` and `due_date` on the document (ASM-1878).
9. System: returns a result per item (accepted, duplicate, refused with the message). Item-level refusals do not fail the request.
10. Case owner: sees the inspection photos, bills and the bill fields on SCR-30 Case documents with capture time and position, through the gateway-bff composite route (DP-19).
11. Outbox relay: publishes `rwb.document.DocumentStored.v1` once per committed store, keyed by caseId, and the decision record on `rwb.decision-record.v1`; neither payload carries a position, a file name or a bill value.

The decision record is written before the change takes effect and inside the store transaction, so a failed record leaves the document, the intake item and the outbox unchanged and the item is refused with MSG-P7-003 (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same client file ID is sent again | The earlier result is returned; nothing new is stored | None | AC4, AC5 |
| X2 | A capture has no GPS position | Stored without position; warning returned and shown | MSG-P5-015 | AC6 |
| X3 | Capture time later than receipt time plus the clock skew | Item refused; the other items are accepted | MSG-GEN-002 | AC7 |
| X4 | Capture time before the case entry date, or older than the age limit | Item refused | MSG-GEN-003 | AC8, AC9 |
| X5 | File type not allowed | Item refused | MSG-P5-001 | AC10 |
| X6 | Malware found | Item quarantined; incident raised | MSG-P5-016 | AC11 |
| X7 | The case is outside the collector's scope | 404; nothing stored | MSG-P4-003 | AC12 |
| X8 | A bill field is below the confidence threshold | Document in the review queue | MSG-P5-003 | AC13 |
| X9 | A manifest item without a file, or a file without an item | 422; nothing stored | MSG-GEN-001 | AC14 |
| X10 | More files than the limit in one request | 413; nothing stored | MSG-GEN-002 | AC15 |
| X11 | A role without Documents C sends captures | 403 | MSG-P4-002 | AC16 |
| X12 | The decision log write fails for an item | Item refused; nothing stored for it | MSG-P7-003 | AC17 |

Three target-service notes:

- The scan of step 5 is the published scan operation of the same service (`POST /api/recovery/document/v1/scans`), whose declared budget is 30 s and is the one declared exception to the 2 s one-hop rule; a scan that cannot answer is a refusal and never a safe answer, so the item is refused with MSG-GEN-006 naming "Document scan" and nothing is stored (ASM-1884).
- A `rwb-case` read that times out at 2 s or meets an open breaker fails the request with 503 and MSG-GEN-006 naming "Case service"; the request may be repeated with the same `Idempotency-Key` and the duplicate rule of step 4 keeps the result single (ASM-1883).
- The legacy `DocumentStoredListener` is not registered by this story: the intake item for a bill or a checklist is created by the intake submit of RWB-P5-E1057-CON inside the same request, and an item already created is not created again (ASM-1878).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the scan (RWB-P5-E1041-CON), the store (RWB-P5-E1024-APP), the intake submit (RWB-P5-E1057-CON), the extraction (RWB-P5-E1053-CON), the case contract (RWB-P3-E1018-CON) and the decision-record, parameters, reference-data, outbox and edge libraries, all earlier or contract work; needs no other Epic 2 story |
| Negotiable | Types, fields, limits and the clock skew are data rows and parameters; the shapes come from the contract baseline |
| Valuable | The inspection evidence is on the case the day it is made, with time and place |
| Estimable | One endpoint, one service, five columns on `document`, one panel change on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic files |

### 7. Acceptance criteria

```gherkin
Feature: Field app photos and bills into the document hub

  Background:
    Given case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for field collector "FC-01" with role RW-FIELDCOL
    Given the clock skew is 5 minutes and the age limit is 30 days
    Given the rwb-case contract mock returns case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for "FC-01"
    Given the parameters contract mock returns CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50 and INTAKE_MAX_FILE_MB 25
    Given the reference-data contract mock returns LOV-CAPTURE-KIND with PHOTO, BILL and CHECKLIST and LOV-DOC-TYPE with INSPECTION_PHOTO, INSPECTION_CHECKLIST and UTILITY_BILL

  Scenario: AC1 Capture (legacy RWB-E2-024 AC1)
    Given an inspection with eight photos and two bills, each with a client file ID, a capture time and a GPS position
    Given the scan contract mock returns CLEAN for each of the ten files
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"
    When the officer syncs at 2026-12-15 14:20
    Then ten documents are on case "RW-2026-000501" with source "UPLOAD": eight "INSPECTION_PHOTO" and two "UTILITY_BILL"
    Then each document shows its capture time and its latitude and longitude, for example 13.7563 and 100.5018
    Then the two bills have intake items for OCR
    Then ten DocumentStored events are in the outbox

  Scenario: AC2 Offline (legacy RWB-E2-024 AC2)
    Given no signal during the visit and photos captured at 2026-12-14 10:05
    When the officer syncs later at 2026-12-15 08:30
    Then each document has captured_at 2026-12-14 10:05 and its stored date 2026-12-15 08:30

  Scenario: AC3 Bill extracted (legacy RWB-E2-024 AC3)
    Given a utility bill photo showing amount "1,284.50" and due date "28/12/2569"
    When extraction runs
    Then bill_amount "1284.50" and due_date "2026-12-28" are on the case in the document index

  Scenario: AC4 The same sync sent twice (legacy RWB-E2-024 AC4)
    Given the ten items of AC1 were received
    When the app sends the same ten client file IDs again
    Then the response marks all ten as "DUPLICATE"
    Then the case still has ten documents from this inspection

  Scenario: AC5 A sync cut off and resent (legacy RWB-E2-024 AC5)
    Given six of ten items were received before the connection dropped
    When the app sends all ten again
    Then six items are "DUPLICATE" and four are "ACCEPTED"
    Then the case has ten documents from this inspection

  Scenario: AC6 A capture with no position (legacy RWB-E2-024 AC6)
    Given a photo with capture time 2026-12-15 13:58 and no GPS position
    When the officer syncs
    Then the document is on the case with no latitude and longitude
    Then the response and SCR-30 show MSG-P5-015 with count 1

  Scenario: AC7 A capture time in the future (legacy RWB-E2-024 AC7)
    Given the server receives the sync at 2026-12-15 14:20
    Given one photo has capture time 2026-12-15 14:26 and another 2026-12-15 14:25
    When the officer syncs
    Then the system refuses the photo at 14:26 with MSG-GEN-002
    Then the system accepts the photo at 14:25

  Scenario: AC8 A capture time before the case entry date (legacy RWB-E2-024 AC8)
    Given a photo with capture time 2026-10-01 09:00, before the entry date 2026-10-02
    When the officer syncs
    Then the system refuses the item with MSG-GEN-003 naming "Capture time" and "Case entry date"

  Scenario: AC9 A capture older than the age limit (legacy RWB-E2-024 AC9)
    Given the sync is at 2026-12-15 14:20
    Given one photo was captured at 2026-11-14 14:19, 31 days earlier, and another at 2026-11-15 14:20
    When the officer syncs
    Then the system refuses the first photo with MSG-GEN-003 naming "Capture time" and the age limit date 2026-11-15
    Then the system accepts the second photo

  Scenario: AC10 A file type not allowed (legacy RWB-E2-024 AC10)
    Given a photo in HEIC format
    Given the capture client mock sends that file as one item of the sync and valid files as the others
    When the officer syncs
    Then the system refuses the item with MSG-P5-001
    Then the system accepts the other items in the same sync

  Scenario: AC11 Malware in a capture (legacy RWB-E2-024 AC11)
    Given a file carrying the EICAR test signature
    Given the scan contract mock returns INFECTED for that file
    When the officer syncs
    Then the system quarantines the item with MSG-P5-016 and an incident is raised
    Then the system writes no document for it

  Scenario: AC12 A case outside the collector's scope (legacy RWB-E2-024 AC12)
    Given case "RW-2026-000502" where "FC-01" has no task
    Given the rwb-case contract mock returns case "RW-2026-000502" with no task for "FC-01"
    When the app sends captures for "RW-2026-000502"
    Then the response is 404 with MSG-P4-003
    Then no file or document is stored

  Scenario: AC13 A bill field below the threshold (legacy RWB-E2-024 AC13)
    Given the bill amount is read with confidence 0.5500 and the threshold is 0.80
    When extraction runs
    Then bill_amount has state "REVIEW" and the document is in the review queue
    Then SCR-30 shows MSG-P5-003 on the bill

  Scenario: AC14 A manifest that does not match the files (legacy RWB-E2-024 AC14)
    Given a manifest of three items and two files
    Given the capture client mock sends the three items and the two files in one request
    When the officer syncs
    Then the response is 422 with MSG-GEN-001 naming the client file ID with no file
    Then the system stores nothing

  Scenario: AC15 Too many files in one sync (legacy RWB-E2-024 AC15)
    Given 51 files in one sync and a limit of 50
    Given the capture client mock sends the 51 files in one request
    When the officer syncs
    Then the response is 413 with MSG-GEN-002 naming "Files", 1 and 50
    Then the system stores nothing

  Scenario: AC16 A role without Documents C sends captures (exception X11) (new, D-RCV-60)
    Given a phone collector with role RW-PHONECOL who has Documents R only
    Given the capture client mock sends one photo for case "RW-2026-000501"
    When the officer syncs
    Then the response is 403 with MSG-P4-002
    Then no file or document is stored

  Scenario: AC17 A decision log write fails for one item (exception X12, business rule BR10) (new, D-RCV-60)
    Given the sync carries two photos for case "RW-2026-000501"
    Given the rwb-decision contract mock fails the write for the first photo
    When the officer syncs
    Then the system refuses the first photo with MSG-P7-003
    Then the system accepts the second photo
    Then no file or document is stored for the first photo

  Scenario: AC18 Position and bill data are not logged (business rule BR9) (new, D-RCV-60)
    Given a photo with a GPS position and a bill with amount "1,284.50"
    When the officer syncs
    Then the log lines for the sync carry the case ID, the item status and the message code only
    Then no position, file name or bill value appears in any log line

  Scenario: AC19 A sync without valid credentials (401 of the provided operations) (new, D-RCV-60)
    Given the capture client mock sends one photo for case "RW-2026-000501" without valid credentials
    When the officer syncs
    Then the response is 401
    Then no file or document is stored

  Scenario: AC20 A case read times out and the sync is repeated (activity timeout and retry) (new, D-RCV-60)
    Given the rwb-case read for case "RW-2026-000501" does not answer within 2 s
    When the officer syncs
    Then the response is 503 with MSG-GEN-006 naming "Case service"
    When the officer repeats the sync with the same Idempotency-Key
    Then the case has one set of documents from this sync

  Scenario: AC21 The document scan does not answer (a consumed call fails) (new, D-RCV-60)
    Given a photo for case "RW-2026-000501"
    Given the scan contract mock does not answer for that file
    When the officer syncs
    Then the system refuses the item with MSG-GEN-006 naming "Document scan"
    Then no file or document is stored for it
```

Every Given, When and Then line of the legacy scenarios above is unchanged: the only added lines are the five Background mock Givens on the `rwb-case`, parameters and reference-data contracts, the scan and `rwb-decision` Givens where a cross-service or published part is mocked, and the three capture-client Givens that state what the field app sends. Scenarios AC16 to AC21 are new: AC16 covers exception X11, AC17 covers exception X12 and business rule BR10, AC18 covers business rule BR9, AC19 covers the 401 answer, AC20 covers the timeout and retry, and AC21 covers the failed scan call. The legacy endpoint `POST /cases/{caseId}/field-captures` maps to `POST /api/recovery/document/v1/cases/{caseId}/field-captures` of 12.1, and `MalwareScanService.scanNow` maps to the scan operation of RWB-P5-E1041-CON.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field capture goes through the same checks as other documents: type, size, malware scan before storage | REQ-DCM-013; RWB-E1-041; RWB-E1-024 |
| BR2 | The capture time is the device time recorded at capture; the receipt time is the server time | FEAT-DCM-21 |
| BR3 | A capture time later than receipt plus the clock skew, before the case entry date, or older than the age limit is refused | CAPTURE_CLOCK_SKEW_MINUTES (5), CAPTURE_MAX_AGE_DAYS (30), assumed; DF-CAS-013 |
| BR4 | The client file ID is unique per case; a repeat returns the earlier result | R-UNI-40 |
| BR5 | The item kind sets the document type: photo to INSPECTION_PHOTO, bill to UTILITY_BILL, checklist to INSPECTION_CHECKLIST; no classification runs | Document types reference table; DL19 |
| BR6 | A capture is attached to the case named in the request; no case matching runs | FEAT-DCM-12 is not needed when the case is known |
| BR7 | Bills are extracted with the UTILITY_BILL field list; a low-confidence field goes to review | RWB-E1-053 BR2; RWB-E1-054 |
| BR8 | A capture with no position is stored and flagged | FEAT-DCM-21 |
| BR9 | GPS position and photos of a home are personal data: masked by role and never logged | CTL-11; DL26 |
| BR10 | A capture that cannot be written to the decision log through the store is not stored | Principle 5; R-UNI-39 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by the scan operation of RWB-P5-E1041-CON called before the store and by the store's own content-signature and size checks, so a capture takes exactly the checks of an upload; the item-level refusal keeps the rest of the sync (ASM-1884).
- BR2 and BR3 are executed by `CaptureChecks` over the manifest values and the three parameters read through the parameters contract (DP-06); the device time is stored as sent, with its offset, and the server never replaces it.
- BR4 is executed twice: by the unique index `ux_document_client_file` on `(case_id, client_file_id)` of this service's migration, and by the `Idempotency-Key` of the request, which returns the first answer of the whole sync.
- BR5 is executed by `CaptureKindMap`, which maps the item kind to the type code read from LOV-DOC-TYPE through the reference-data contract (DP-07); no type code is typed in code and no classifier is called.
- BR6 is executed by taking the case from the path only: the `rwb-case` read confirms the case and its scope and never performs a match; a capture never enters the intake match path of RWB-P5-E1032-APP (ASM-1883).
- BR7 is executed by the intake submit of RWB-P5-E1057-CON and the extraction operation of RWB-P5-E1053-CON, which sets `review_status` PENDING and `write_once` false on a low-confidence field, so the file stays in `rwb-docs` until review (RWB-P5-E1054-APP owns the review).
- BR8 is stored as NULL latitude and longitude with `MSG-P5-015` returned once per sync with the count.
- BR9 is executed by the masking rule `rwb-access` holds and by the ACE common PII access log, which writes every read of a document detail; this package logs the item ID, the status and the message code only.
- BR10 is executed by the decision-record library of DP-03 inside the store transaction: the DOCATT record, the `document` row, the capture columns, the intake item and the outbox row commit together or not at all (R-UNI-39).

### 9. State transitions

None for the case. This story does not change a case status. It stores documents with review_status NOT_NEEDED, or PENDING when a bill field is in review. The inspection task and the R-DIL-22 move to ASSET_UNLOCK_DECISION are in Epic 3.

| Item state in the `FieldCaptureResult` | Event | Condition | Next state |
|---|---|---|---|
| (received) | The manifest item and its file both arrive and every check passes | The scan answers CLEAN and the store commits | ACCEPTED |
| (received) | The client file ID already exists on the case | The unique index or the earlier item is found | DUPLICATE, with the first documentId |
| (received) | Type, size, capture time or position fails a check | The store is not called | REFUSED, with its messageCode |
| (received) | The scan answers INFECTED | The store is not called; the file stays in `rwb-quarantine` | QUARANTINED, with MSG-P5-016 |

The document state machine COPY_PENDING to STORED belongs to RWB-P5-E1024-APP and is not changed by this story; the intake item states PENDING to MATCHED belong to RWB-P5-E1032-APP and are not changed either, because a capture names its case and never enters the matcher.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FIELDCOL, field collector | Sends captures for cases in Own scope (Documents CR) |
| RW-CASEOWN, case owner | Reads the captures and bill fields on the case (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the captures on deed in lieu cases (Documents CRU) |
| SY-OCR, OCR and extraction pipeline | Runs OCR and extraction on bills and checklists (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-PHONECOL, phone collector | Reads only (Documents R); cannot send captures |

In the target the authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds behind gateway-bff; every REST operation of 12.1 calls the authorise check POST /api/recovery/access/v1/authorise (DP-08) with the caller, the case, the area DOCUMENTS and the right of the operation (shape assumed; GAP-0952); this story adds no guard of its own and inherits the 403 shapes of MSG-P4-002 and MSG-P4-003. SY-DECLOG is the local decision-record library of DP-03 in the target, called inside the store transaction, and it publishes the DOCATT record on `rwb.decision-record.v1`. The request runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference; the login name is Not specified in the source documents (GAP-1018; ASM-1877).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `rwb-case` case, through the contract | id | Read |
| DF-CAS-013 | `rwb-case` case, through the contract | entry_date | Read |
| DF-DOC-001 to DF-DOC-011 | `document`, through the store of RWB-P5-E1024-APP | all fields | Write, through the store |
| DF-DOC-027 | `document`, through the capture block of the store | captured_at | Write, through the store |
| DF-DOC-028 | `document`, through the capture block of the store | capture_latitude | Write, through the store |
| DF-DOC-029 | `document`, through the capture block of the store | capture_longitude | Write, through the store |
| DF-DOC-030 | `document`, through the capture block of the store | client_file_id | Write, through the store |
| DF-DOC-031 | `document`, through the capture block of the store | capture_kind | Write, through the store |
| DF-DOC-012 to DF-DOC-017 | `document_field`, through the extraction of RWB-P5-E1053-CON | all fields | Write, through the extraction |
| DF-DOC-045, DF-DOC-046, DF-DOC-055, DF-DOC-057 | `document_intake`, through the intake submit of RWB-P5-E1057-CON | id, source, received_at, intake_ref | Write, through the intake submit |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-224 | `document_type` | field_definitions | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read, resolved through DP-06 |
| DF-DEC-001 to DF-DEC-018 | decision-record library table in `rwb_document`, collected into `rwb-decision`'s `decision_log_entry` | all fields | Write, through the library |
| (outbox) | outbox library table in `rwb_document` | the row for the stored event | Write, through the library |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `recovery_case` row is copied and no ACE view is read by this service: DF-CAS-001 and DF-CAS-013 arrive inside the `rwb-case` contract answer, and DP-01 forbids a foreign-schema read. Personal data never enters the event payload, the decision record or the log: a position, a file name and a bill value are never logged, and a log line carries the case ID, the item status and the message code only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E2024-CON.

| Method | Path | API ID | Owner | Notes |
|---|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/field-captures` | API-P5-015 | P5 | Sync a field capture batch: `multipart/form-data` with a `manifest` part (inspectionRef, items of clientFileId, kind PHOTO, BILL or CHECKLIST, capturedAt with offset, latitude, longitude, fileName) and one file part per item named by its clientFileId; answer 201 `FieldCaptureResult` with items of clientFileId, status ACCEPTED, DUPLICATE, REFUSED or QUARANTINED, documentId and messageCode. Documents C with scope applied on the case; `Idempotency-Key` required; `clientFileId` unique per case |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1018-CON | The case, its entry date and the task that puts it in the collector's scope; one hop, 2 s timeout, breaker per downstream, one GET retry with jitter (DP-11). A failed read maps to 503 with MSG-GEN-006 naming "Case service" |
| GET | the parameters read of DP-06 | P3 behind the client library | RWB-P3-E1042-CON | `CAPTURE_CLOCK_SKEW_MINUTES`, `CAPTURE_MAX_AGE_DAYS`, `CAPTURE_MAX_FILES`, `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, cached for 5 minutes |
| GET | the reference-data read of DP-07 | P3 behind the client library | RWB-P3-E1043-CON | LOV-CAPTURE-KIND, LOV-DOC-TYPE, LOV-DOC-SOURCE, LOV-REVIEW |
| POST | `/api/recovery/document/v1/scans` | P5 rwb-document, same service | RWB-P5-E1041-CON | `ScanRequest` in, `ScanResult` CLEAN or INFECTED out, 30 s declared budget; called after the file is written to `rwb-quarantine` and before the store (ASM-1884) |
| POST | the store command of RWB-P5-E1024-APP | P5 rwb-document, same service | RWB-P5-E1024-APP | The case, the type, source UPLOAD, the file and its SHA-256, the extracted fields and the optional capture block (ASM-1877) |
| POST | the intake submit of RWB-P5-E1057-CON | P5 rwb-document, same service | RWB-P5-E1057-CON | Creates the `document_intake` item with source UPLOAD and the type of the item kind for a bill or a checklist; the exact path and shape are fixed by that baseline and are Not specified in the source documents (GAP-1018; ASM-1878) |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (the legacy DocumentStored, EV-16), one per accepted item, written by the store | `rwb.document.events.v1` | P5 | caseId | caseid, documentid, source, type; no position, no file name, no bill value |
| `rwb.document.DocumentFieldsExtracted.v1` (the legacy EV-17), for a bill, through the extraction of RWB-P5-E1053-CON | `rwb.document.events.v1` | P5 | caseId | confidence, documentid, fields; no field value in clear |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with decision code DOCATT, final call STORED, the document type, the source UPLOAD and the item kind as inputsRef content |

CloudEvents 1.0 envelope, binary mode; no personal data in any payload. The stored event and the record are written to the outbox inside the store transaction, so they exist exactly when the document row, its capture values and the intake item exist.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The path is started by the request, not by an event: the capture values and the manifest arrive in the request body, and the intake item is created inside the same request through the intake submit. `rwb.document.DocumentStored.v1` is consumed by `rwb-case` and `rwb-agent`, not by this story |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, owned by RWB-P5-E1049-APP | `rwb-document` | Observed only: it reads the intake item this story creates and runs `ocr`, `classify` and `extract` on it. This story contributes no activity and registers no workflow |
| None contributed | — | — | The capture path is synchronous: no workflow, no activity and no compensation of its own is declared by this story |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None in this story | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | The intake Schedule is registered and monitored by the stories that own the intake pipeline and its operations; this story only creates the items it reads |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Written only through the store of RWB-P5-E1024-APP, never by this story directly; the five capture columns are passed in the optional capture block and created by this story's migration |
| `document_intake` | P5 | Written only through the intake submit of RWB-P5-E1057-CON for a bill and a checklist; read for the intake item ID returned on the result |
| `document_hub_parameter` | P5 | Read only through the parameters contract of DP-06; the rows are P5's |
| `document_type` | P5 | Read only: the type code, the field list and the write-once flag of the three types (RWB-P5-E1025-APP) |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record, in the store transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The stored event; the `Idempotency-Key` row of the capture operation |

No foreign-schema table is read (DP-01) and no ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case fake (`GET /cases/{caseId}`) | RWB-P3-E1018-CON | The case, its entry date and the task of AC1 to AC9 and AC12, and the 2 s timeout path |
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | The clock skew of 5 minutes, the age limit of 30 days, the limit of 50 files and the size limit of 25 MB |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-CAPTURE-KIND, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW |
| scan fake | RWB-P5-E1041-CON | The CLEAN answer of AC1, the INFECTED answer of AC11 and the 30 s budget |
| store stub | RWB-P5-E1024-APP | The store answer, the duplicate answer of AC4 and AC5, and the COPY_PENDING state |
| intake submit stub | RWB-P5-E1057-CON | The intake item ID returned for a bill and a checklist |
| field-capture baseline fake | RWB-P5-E2024-CON | The single operation and the `FieldCaptureResult` shape, so the tests build before the app code lands |
| capture client fake | This story's test harness | The field app sync: a manifest, one file part per item and the resend of AC4 and AC5 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 2 cross-service plus 3 in-service | The capture operation; the case read, the parameters read and the lists read; the scan, the store and the intake submit of the same service |
| Kafka | Published 2 events and 1 decision record; consumed 0 | `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`; the record on `rwb.decision-record.v1` |
| Temporal | 1 workflow observed, 0 contributed, 0 Schedules | `DocumentIntakeWorkflow` on queue `rwb-document` reads the items this story creates |
| File | The intake file and the stored file | Written to `rwb-quarantine` for the scan, then to `rwb-docs` or `rwb-docs-legal` by the store of RWB-P5-E1024-APP under the type's write-once flag |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `capture/field`; front end folder `recovery/documents`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FieldCaptureController | Controller | The single operation of 12.1: `Idempotency-Key` check, manifest parsing, matching of items to file parts, the 413 and 422 checks, the RFC 9457 error mapping |
| FieldCaptureService | Service | BR1 to BR10 per item: duplicate check, type, size, time and position checks, write to `rwb-quarantine`, scan, store with the capture block, intake submit for a bill or a checklist, result assembly |
| CaptureChecks | Service | The four time and position rules over the manifest values and the parameters read through DP-06; stores the device time as sent with its offset |
| CaptureKindMap | Library client | The item kind to type code mapping over LOV-DOC-TYPE and LOV-CAPTURE-KIND read through DP-07; no type code in code |
| FieldCaptureRepository | Repository | Looks up `client_file_id` per case, reads the intake item ID and reads `document_hub_parameter` through the parameters client; never writes `document` |
| CaptureDetails | React component | On SCR-30: capture time, position and a map link for each capture; the MSG-P5-015 flag and the masking of a position for a role without the right to see it |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V2024_1__field_capture.sql` adds to `document` `captured_at` timestamptz, `capture_latitude` numeric(9,6), `capture_longitude` numeric(9,6), `client_file_id` varchar(64) and `capture_kind` varchar(12) (DF-DOC-027 to DF-DOC-031).
- Constraint `ux_document_client_file ON document (case_id, client_file_id) WHERE client_file_id IS NOT NULL` (ASM-1885).
- Index `ix_document_capture_kind ON document (capture_kind, captured_at) WHERE capture_kind IS NOT NULL` for the SCR-30 filter (ASM-1885).
- The case entry date is read through the `rwb-case` contract; no `recovery_case` row is read or copied (DP-01).

**Configuration and reference data.**

- Document type rows INSPECTION_PHOTO, INSPECTION_CHECKLIST and UTILITY_BILL with the UTILITY_BILL fields, loaded into the type table of RWB-P5-E1025-APP (DL19).
- `document_hub_parameter` rows CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50 (assumed; DL11), and INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB shared with the intake of RWB-P5-E1057-CON; all read through the parameters contract of DP-06 (ASM-1879).
- Four lists read through the reference-data contract of DP-07: LOV-CAPTURE-KIND (PHOTO, BILL, CHECKLIST), LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW (ASM-1880).
- Decision code DOCATT, assumed, with the LOV-DECISION list loaded by the data steward.
- Feature flag `rwb.document.field-capture` (ASM-1882). Off: the operation answers 404, exactly as the legacy flag states.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the five capture columns and the parameter rows the legacy story wrote into `rwb_document` and stops the module reaching into the recovery schema: the `document` row is written only through the store, and the case entry date arrives inside the `rwb-case` answer. DP-03 replaces `DecisionLogWriter` with the local library, so the DOCATT record, the store row, the intake item and the outbox row share one transaction and the record is published on the shared topic. DP-06 keeps the five parameters out of the code through the client library, while the parameter rows themselves stay in `rwb_document` as the Ownership Map gives them to P5. DP-07 keeps the four lists out of the code, so the item kinds and the three type codes are reference rows and never constants. DP-09 puts the stored event in the outbox in the store transaction and fixes the CloudEvents envelope. DP-11 replaces the in-process `CaseDirectory` with one hop, a published shape, a fake in the build and a 2 s timeout. DP-15 puts the capture migration in the service's own sequence. DP-19 puts the capture details of SCR-30 behind the gateway-bff composite route, so the screen calls the owner once.

**Build steps**

1. Write the migration, the unique client-file constraint and the index; test that a second row with the same case and client file ID is refused and that a NULL client file ID is allowed.
2. Build the manifest parsing and the item-to-file matching with the 413 and 422 checks; unit test the three-item-two-file case of AC14 and the 51-file case of AC15.
3. Build `CaptureChecks` against the parameters fake; unit test the clock skew of AC7, the entry date of AC8 and the age limit of AC9 with the exact boundary values of the legacy story.
4. Build the per-item path with the scan fake, the store stub and the intake submit stub; integration test AC1, AC2, AC3, AC6, AC10 and AC11.
5. Build the duplicate path over the unique index and the `Idempotency-Key`; integration test the resend of AC4 and the cut-off resend of AC5.
6. Build the scope refusal of AC12 against the case fake, and the bill review of AC13 against the extraction fake with the confidence 0.5500.
7. Build `CaptureDetails` on SCR-30 with the position masking and the MSG-P5-015 flag; component tests for the list, the map link and the flag.
8. Test the decision-record failure path (TC-E2-024-17) and the access test (TC-E2-024-16), and confirm that nothing is stored and that the item carries MSG-P7-003 or the 403.

**Done when.** The tests in section 16 pass and a synthetic inspection of ten files is on the case within 5 minutes of sync in SIT (target assumed; DL11), with one DOCATT record and one `DocumentStored` event per accepted item and no position, file name or bill value in a payload or a log line.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-015 | Captures accepted with no GPS position (new) | {count} files have no location. They are on the case without a position. | 201 |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. | 201 on the item |
| MSG-P5-003 | A bill field needs checking | Some fields need checking. The document is in the review queue. | 201 on the item |
| MSG-P5-016 | A capture with malware | This file was not stored because the malware scan found a threat. It is held in quarantine. | 201 on the item |
| MSG-P5-017 | A capture above the size limit | This file is larger than {size} MB and cannot be stored. | 201 on the item |
| MSG-P7-003 | Decision log write failed for an item | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 201 on the item |
| MSG-GEN-001 | Manifest and files do not match | Enter {field}. | 422 |
| MSG-GEN-002 | Capture time in the future; too many files | {field} must be between {min} and {max}. | 201 on the item, or 413 for the file count |
| MSG-GEN-003 | Capture time before the case entry date or the age limit | {field} cannot be before {other}. | 201 on the item |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Case outside the collector's scope | This case is not in your scope. | 404 |
| Not specified in the source documents (CG-ALL-6208) | No authenticated caller | Not specified in the source documents (CG-ALL-6208) | 401 |
| MSG-GEN-006 | The case read, the scan or the intake submit failed | {system} is not available. Your request is queued and will be retried. | 503 |

Thai text for each message follows decision DL10.

Open decisions (each with its assumptions, all still open): DL03 (ASM-0189, ASM-0193, ASM-0578, ASM-2567); DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL19 (ASM-1051, ASM-1164, ASM-1809, ASM-1810); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355).

Delivery shape: every request-level error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. An item-level refusal is not a request error: the request answers 201 and the item carries its status and its message code, exactly as the legacy contract states. The HTTP mapping is the legacy one and is fixed by AC12 to AC15 and the baseline RWB-P5-E2024-CON: 401, 403, 404, 413, 422 and 503 at request level, and 201 with ACCEPTED, DUPLICATE, REFUSED or QUARANTINED per item. MSG-P5-015 is a warning returned once per sync with the count and is not an error.

### 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-30 Case documents | Loading | Skeleton rows while the case document list loads through the gateway-bff composite route |
| SCR-30 Case documents | list | Sees inspection photos, checklists and bills with capture time and position; bill fields with confidence; MSG-P5-015 on captures without position |
| SCR-30 Case documents | capture detail | The capture time, the position, a map link and the client file ID of a capture; the position is masked for a role without the right to see it and each read is written to the access log |
| SCR-30 Case documents | no position | A capture stored without a position shows the MSG-P5-015 flag with no map link |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-6212) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-6212) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-6212) |
| SCR-31 Document review queue | list | Sees a bill with a low-confidence field (RWB-E1-054, now RWB-P5-E1054-APP) |
| SCR-31 Document review queue | Empty | Not specified in the source documents (CG-ALL-6213) |
| SCR-31 Document review queue | Error | Not specified in the source documents (CG-ALL-6213) |
| SCR-31 Document review queue | No access | Not specified in the source documents (CG-ALL-6213) |

The field app screens belong to the field app and are not in this story. The case document list is RWB-P5-E1026-APP; this story adds the capture detail panel and the no-position flag only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-16 | X11, Access | Component | RW-PHONECOL user (Documents R) calls the field-captures operation; refused with 403 and MSG-P4-002 |
| TC-E2-024-18 | AC16, X11, Access | Component | RW-PHONECOL user (Documents R) sends captures; refused with 403 and MSG-P4-002 |
| TC-E2-024-19 | AC17, X12, BR10 | Component | Decision log write fails for one item of a sync; that item is refused with MSG-P7-003 and nothing is stored for it |
| TC-E2-024-20 | AC18, BR9 | Component | Sync with a GPS position and a bill; log lines carry the case ID, the item status and the message code only |
| TC-E2-024-17 | X12, Principle 5 | NFR | Decision-record write forced to fail during a sync of three files; no document stored, items returned with MSG-P7-003, incident raised |
| TC-E2-024-01 | AC1, BR1, BR5, BR6 | End to end | Ten synthetic files with positions in Bangkok |
| TC-E2-024-02 | AC2, BR2 | End to end | Capture one day before sync |
| TC-E2-024-03 | AC3, BR7 | End to end | Synthetic utility bill image |
| TC-E2-024-04 | AC4, BR4 | End to end | Same ten client file IDs twice |
| TC-E2-024-05 | AC5, BR4 | End to end | Six of ten received, then all ten resent |
| TC-E2-024-06 | AC6, BR8 | End to end | Photo with no position |
| TC-E2-024-07 | AC7, BR3 | End to end | Capture times 6 and 5 minutes after receipt |
| TC-E2-024-08 | AC8, BR3 | End to end | Capture one day before the entry date |
| TC-E2-024-09 | AC9, BR3 | End to end | Captures 31 days and 30 days before sync |
| TC-E2-024-10 | AC10, BR1 | End to end | HEIC file |
| TC-E2-024-11 | AC11, BR1 | End to end | EICAR test file |
| TC-E2-024-12 | AC12 | End to end | Case with no task for FC-01 |
| TC-E2-024-13 | AC13, BR7 | End to end | Bill amount at confidence 0.55 |
| TC-E2-024-14 | AC14 | End to end | Three items, two files |
| TC-E2-024-15 | AC15 | End to end | 51 files |
| TC-E2-024-24 | Section 12 operations, events and activities | Contract | Every operation, event and activity of section 12 checked against RWB-P5-E2024-CON |
| TC-E2-024-25 | Section 12.7 tables | Boundary | Each table of section 12.7 read or written only through its owner (ASM-3438) |
| TC-E2-024-21 | AC19 | Component | Sync request with no valid credentials; refused with 401; no file or document stored |
| TC-E2-024-22 | AC20 | NFR | rwb-case read times out at 2 s; sync refused with 503 and MSG-GEN-006 naming "Case service"; repeat with the same Idempotency-Key leaves one set of documents |
| TC-E2-024-23 | AC21, Resilience | NFR | Document scan does not answer; item refused with MSG-GEN-006 naming "Document scan"; nothing stored for it |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. The same twenty-five test case IDs are answered at contract level by RWB-P5-E2024-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: types, fields, the clock skew, the age limit and the file limit are data rows and parameters read through DP-06 and DP-07.
- No personal data in logs, tests or prompts: positions, file names and bill values are not logged; test photos show no person or real address; the event and the decision record carry no position and no field value.
- No read of another module's tables: the case, its entry date and its task come through the P3 case contract, and no `v_ace_*` view is read by this service (DP-01).
- The device time is stored as sent, with its offset; the server never replaces it.
- The scan is the published operation of this service and never a second engine; an unavailable scan is a refusal and never a safe answer (ASM-1884).
- The `document` row is written only by the store of RWB-P5-E1024-APP; this story passes the capture block and creates the columns, nothing more (ASM-1877).
- The capture is idempotent twice over: `Idempotency-Key` on the request, and `ux_document_client_file` on `(case_id, client_file_id)`.
- The feature flag `rwb.document.field-capture` removes the capture path without a rollback of the schema (ASM-1882).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-17 |

| Legacy reference | Where it is kept |
|---|---|
| DocumentStored (EV-16) through DocumentStore | Sections 1, 4, 12.3, 17 |
| MSG-P5-015, MSG-P5-001, MSG-P5-003, MSG-P5-016, MSG-P5-017, MSG-P7-003, MSG-GEN-001, MSG-GEN-002, MSG-GEN-003, MSG-P4-002, MSG-P4-003 | Section 14 and the exception paths |
| Parameters CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50, INTAKE_MAX_FILE_MB 25 | Background, sections 1, 3, 8, 13 |
| Document types INSPECTION_PHOTO, INSPECTION_CHECKLIST, UTILITY_BILL | Sections 3, 7, 8, 13 |
| Rules R-DIL-22, R-UNI-39, R-UNI-40, CTL-11, CTL-38, DL10, DL19, DL26 | Sections 2, 8, 17, 18 |
| Containers `rwb-quarantine`, `rwb-docs`, `rwb-docs-legal` | Sections 4, 12.9, 13 |
| Legacy key RWB-E2-024, AC1 to AC15, TC-E2-024-01 to TC-E2-024-17 | Metadata, section 7, section 16 |

### 19. Out of scope

- The field app itself and its offline store.
- Agency field teams reaching the Workbench through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (FEAT-TRT-15 and R-DIL-22, Epic 3).
- The repossessed vehicle photo standard (CTL-38, Epic 7).
- The published contract documents, the fakes and their versioning (RWB-P5-E2024-CON).
- The store itself, the write-once container and the version history (RWB-P5-E1024-APP).
- The scan engine, its provider and its capacity (RWB-P5-E1041-CON and RWB-E1-041's operations stories).
- The intake channels of branches, mailroom, partner SFTP and email (RWB-P5-E1057-APP).
- OCR, classification and field extraction (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP), which this story calls only.
- Confirming or correcting a bill field in review (RWB-P5-E1054-APP).
- The compute, the storage, the topic and the ACL provisioning of this story (its infrastructure story) and its chart, dashboards and runbook (its operations story).
