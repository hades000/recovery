# RWB-ITG-E2024-ITG Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2024-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E2024-APP, RWB-P4-E2024-APP, RWB-P3-E2024-APP, RWB-P7-E2024-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-013) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-024 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service journey harness for field captures that carries an inspection of photos and bills into the document hub with its capture time, position and bill fields, and shows the result on the case, in the review queue and in the decision log**, so that **the field capture journey is proven end to end across rwb-document, rwb-access, rwb-case and rwb-decision before the app stories of RWB-E2-024 are signed off**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, screen, table or migration.

### 2. Business rationale

RWB-E2-024 splits into four app stories and this integration story. The app stories build their own part inside their own service: the field capture endpoint and the capture columns on the document in RWB-P5-E2024-APP, the scope and role check in RWB-P4-E2024-APP, the case and task facts the journey starts from in RWB-P3-E2024-APP, and the decision record behind the store in RWB-P7-E2024-APP. None of them can prove on its own that a photo taken with no signal on 14 December arrives on 15 December with its own capture time, that the same sync sent twice still leaves ten documents on the case, that a bill photographed in the field is read into `bill_amount` and `due_date` without a chat message or a paper envelope, or that a low-confidence amount stops in the review queue instead of passing as a fact. That proof is this story.

The journey is the one the business asks for: an inspection is on the case the same day it is made, with the date, the place and the bill values that can be shown when the inspection is questioned (REQ-DCM-013). The harness runs it against the published contracts of the four services on one business date and produces evidence that can be re-run for any build.

The architecture changes the path, not the business. The monolith wrote one `recovery.document` table and one `recovery.document_hub_parameter` row set from one module, called the case interface in process, and logged the decision in the same transaction as the state change. In the target, rwb-document owns `rwb_document` for metadata, custody, OCR text and fields, and the harness never reads it (DP-01); the case entry date and the task come from rwb-case by one hop with a 2 s timeout and never from a case table (DP-11); the type, field and parameter values are reference data and parameters owned by rwb-case and read through its contract (DP-06, DP-07); the DOCATT decision record goes to the local library and the shared topic `rwb.decision-record.v1` (DP-03); Flyway in `rwb_document` carries the capture columns (DP-15); the store writes its outbox and `DocumentStored` travels on `rwb.document.events.v1` (DP-09); and the whole journey runs on the gateway route the real screens use, on the owners' own bases (DP-19). The harness is the place where those boundaries are exercised together, so a capture that is lost, duplicated or misread is found in SIT and not by a case owner who cannot show the inspection.

The legacy exception table gives the measure: eleven triggers, each with a named message and each returned on the item rather than failing the request. The harness asserts that shape too, because a batch that fails whole on one bad file is as wrong as a batch that accepts it.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topics `rwb.document.events.v1` and `rwb.decision-record.v1`, and the intake profile of rwb-document. The harness environment, its seed pack and its evidence format: Not specified in the source documents (GAP-0406; ASM-0581).
- The four integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P5-E2024-APP (rwb-document), RWB-P4-E2024-APP (rwb-access), RWB-P3-E2024-APP (rwb-case) and RWB-P7-E2024-APP (rwb-decision).
- Case `RW-2026-000501` exists in the seeded data with entry date 2026-10-02 and a field inspection task for the collector `FC-01` with role RW-FIELDCOL, so the case is in that collector's Own scope (legacy section 7 Background).
- The document type rows INSPECTION_PHOTO with no fields, INSPECTION_CHECKLIST with no fields and UTILITY_BILL with `bill_amount`, `due_date` and `account_ref` are loaded as reference data, through the P3 contract only.
- The parameters CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50 and INTAKE_MAX_FILE_MB 25 are in force through the P3 parameter contract; 5, 30, 50 and 25 are the legacy values (legacy section 3, section 13) and are read, never coded.
- The clock skew of 5 minutes and the age limit of 30 days are asserted as the values in force, so the boundary conditions of AC1 and AC5 are fixed by data and not by the build.
- The test user of role RW-FIELDCOL (`FC-01` in the legacy data) holds Documents right C on the case in scope; the P4 session operation is the only place that right is confirmed.
- Synthetic files only: synthetic photos with no person and no real address, synthetic utility bills, one HEIC file and one EICAR test file. No real customer data, phone number or position enters the harness or its evidence.
- The feature switch `rwb.dochub.field-capture` is on in the harness profile; off, the operation answers 404 and the run stops at step 5 with X1.
- No build dependency and no contract dependency. Day 1: the whole story runs against the four fakes from the first day.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date 2026-12-15 and the four contract versions it is about to exercise.
2. Harness: seeds the case `RW-2026-000501` with entry date 2026-10-02, the field inspection task for `FC-01`, the three document types and the four parameters, and, per scenario, the extra case and task state the scenario names; a missing seed item stops the run (X7).
3. Harness: calls `GET /api/recovery/access/v1/me/session` for `FC-01` and records the role, the scope and the Documents right it will exercise.
4. Harness: calls `GET /api/recovery/case/v1/cases/{caseId}` and records the case state, the entry date and the task the journey starts from.
5. Harness: calls `POST /api/recovery/document/v1/cases/{caseId}/field-captures` with the manifest of `clientFileId`, kind PHOTO, BILL or CHECKLIST, capture time with offset, latitude and longitude, and one file part per item, with an Idempotency-Key per scenario; records the status and the item results.
6. Harness: reads `GET /api/recovery/document/v1/cases/{caseId}/documents` and records the count, the type, the source, the capture time, the position and the review state of each document.
7. Harness: reads one document through `GET /api/recovery/document/v1/documents/{documentId}` and records its `captured_at`, `capture_latitude`, `capture_longitude`, `client_file_id` and, for a bill, its extracted fields with their confidence.
8. Harness: reads `GET /api/recovery/document/v1/review-items` and records whether the low-confidence bill field appears there (AC8).
9. Harness: reads `GET /api/recovery/decision/v1/decision-log` and records whether the DOCATT entry exists for each stored document and for each item the store refused (AC1, AC6).
10. Harness: subscribes to `rwb.document.events.v1` and `rwb.decision-record.v1` for the run window and records `DocumentStored`, `DocumentFieldsExtracted` and `DecisionRecorded` for the case, and asserts that no event names a file, a position or a bill value.
11. Harness: waits for the JOB-12 Document intake window and records the intake item per bill and per checklist, and the state the review queue holds after extraction (AC1, AC8).
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate and attaches the report to the wave 2 release record; then releases the run lock and restores the seeded data.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A contract fake or a real service answers an unexpected status for the journey | The scenario is marked failed and the report names the operation, the expected status and the answer | None | AC1, AC6 |
| X2 | A document that the response named as ACCEPTED is not readable through the document operation within the run window | The scenario is marked failed; the report names the case, the document ID and the missing entry | None | AC1, AC2, AC3 |
| X3 | The batch is answered 413 or 422 instead of a per-item result | The scenario is marked failed unless the scenario is the batch-shape one, and the report carries the problem detail | MSG-GEN-001, MSG-GEN-002 | AC6 |
| X4 | An item carrying the EICAR signature is accepted and a document is written | The scenario is marked failed; a quarantine that leaves a document is a defect, not a warning | MSG-P5-016 | AC6 |
| X5 | A capture is sent for a case with no task for the collector and is accepted | The scenario is marked failed; the report names the case and the absent task | MSG-P4-003 | AC7 |
| X6 | The decision log answers 503 on the journey read | The scenario is marked failed and the report keeps the last good ledger read for rerun | None | AC1, AC6 |
| X7 | The seeded data cannot be loaded (case, task, type, field or parameter missing) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X8 | Another run holds the environment lock | The run refuses to start and names the holder and the start time | None | All |
| X9 | The evidence pack cannot be attached to the release record | The run is marked failed; the local evidence file is kept for rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four published contracts or their fakes and the intake profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded values, the file fixtures and the item results are data files, never code |
| Valuable | The capture journey is proven once across four services, before the app stories claim Done |
| Estimable | One journey runner, one fake set, one capture pack, two assertions, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a scenario with a fixed Given, When and Then and a recorded result |

### 7. Acceptance criteria

```gherkin
Feature: Field app photos and bills into the document hub

  Background:
    Given case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for field collector "FC-01" with role RW-FIELDCOL
    Given the clock skew is 5 minutes and the age limit is 30 days
    Given the document types INSPECTION_PHOTO, INSPECTION_CHECKLIST and UTILITY_BILL are in force with the UTILITY_BILL fields bill_amount, due_date and account_ref
    Given the parameters CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30 and CAPTURE_MAX_FILES 50 are in force

  Scenario: AC1 Capture journey to the document hub and the decision log (new, D-RCV-60)
    Given an inspection with eight photos and two bills, each with a client file ID, a capture time and a GPS position
    When the collector syncs at 2026-12-15 14:20 through POST /api/recovery/document/v1/cases/RW-2026-000501/field-captures
    Then ten documents are on case "RW-2026-000501" with source "UPLOAD": eight "INSPECTION_PHOTO" and two "UTILITY_BILL"
    Then each document shows its capture time and its latitude and longitude, for example 13.7563 and 100.5018
    Then the two bills have intake items for OCR
    Then ten DocumentStored events are on rwb.document.events.v1 for the case
    Then ten DOCATT decision records are on rwb.decision-record.v1 for the case

  Scenario: AC2 Offline capture kept with its capture time (new, D-RCV-60)
    Given no signal during the visit and photos captured at 2026-12-14 10:05
    When the collector syncs later at 2026-12-15 08:30
    Then each document has captured_at 2026-12-14 10:05 and its stored date 2026-12-15 08:30

  Scenario: AC3 Bill extracted across the service boundary (new, D-RCV-60)
    Given a utility bill photo showing amount "1,284.50" and due date "28/12/2569"
    When JOB-12 Document intake runs and extraction completes
    Then bill_amount 1284.50 and due_date 2026-12-28 are readable from the document through GET /api/recovery/document/v1/documents/{documentId}

  Scenario: AC4 The same sync sent twice (new, D-RCV-60)
    Given the ten items of AC1 were received
    When the app sends the same ten client file IDs again with a new Idempotency-Key
    Then the response marks all ten as "DUPLICATE"
    Then the case still has ten documents from this inspection
    Then no second DocumentStored event is written for any of the ten

  Scenario: AC5 A sync cut off and resent (new, D-RCV-60)
    Given six of ten items were received before the connection dropped
    When the app sends all ten again
    Then six items are "DUPLICATE" and four are "ACCEPTED"
    Then the case has ten documents from this inspection

  Scenario: AC6 Item refusals do not fail the batch (new, D-RCV-60)
    Given the server receives the sync at 2026-12-15 14:20
    Given one photo has capture time 2026-12-15 14:26 and another 2026-12-15 14:25
    Given a photo in HEIC format and a file carrying the EICAR test signature
    When the collector syncs
    Then the system refuses the photo at 14:26 with MSG-GEN-002 and accepts the photo at 14:25
    Then the system refuses the HEIC item with MSG-P5-001
    Then the system quarantines the EICAR item with MSG-P5-016 and writes no document for it
    Then the response is 200 with one result per item and the accepted items are on the case

  Scenario: AC7 A case outside the collector's scope (new, D-RCV-60)
    Given case "RW-2026-000502" where "FC-01" has no task
    When the app sends captures for "RW-2026-000502"
    Then the response is 404 with MSG-P4-003
    Then no document is written and no DocumentStored event is on rwb.document.events.v1 for "RW-2026-000502"

  Scenario: AC8 A bill field below the confidence threshold (new, D-RCV-60)
    Given the bill amount is read with confidence 0.5500 and the threshold is 0.80
    When extraction runs
    Then bill_amount has state "REVIEW"
    Then the document is in the review queue through GET /api/recovery/document/v1/review-items
    Then the document carries MSG-P5-003
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field capture goes through the same type, size and malware checks as any other document, before storage | REQ-DCM-013; RWB-E1-041; RWB-E1-024 |
| BR2 | The capture time is the device time recorded at capture; the receipt time is the server time, and the server never replaces the device time | FEAT-DCM-21 |
| BR3 | A capture time later than receipt plus the clock skew, before the case entry date, or older than the age limit is refused on the item | CAPTURE_CLOCK_SKEW_MINUTES (5), CAPTURE_MAX_AGE_DAYS (30); DF-CAS-013 |
| BR4 | The client file ID is unique per case; a repeat returns the earlier result and stores nothing | R-UNI-40 |
| BR5 | The item kind sets the document type: photo to INSPECTION_PHOTO, bill to UTILITY_BILL, checklist to INSPECTION_CHECKLIST; no classification runs | Document types reference data; DL19 |
| BR6 | A capture is attached to the case named in the request; no case matching runs | FEAT-DCM-12 is not needed when the case is known |
| BR7 | Bills are extracted with the UTILITY_BILL field list, and a field below the confidence threshold goes to review | RWB-E1-053 BR2; RWB-E1-054 |
| BR8 | GPS position and photos of a home are personal data: masked by role and never logged | CTL-11; DL26 |
| BR9 | A capture that cannot be written to the decision log through the store is not stored | Principle 5; R-UNI-39 |

BR1 to BR9 are the legacy rules BR1 to BR10 of RWB-E2-024, with legacy BR6 folded into BR5 and legacy BR8 into BR2. The split changes none of them; the harness asserts them across the service boundaries and restates none of them in code.

### 9. State transitions

None on the case. This story does not change a case status. The document `review_status` it observes is NOT_NEEDED on an accepted capture, PENDING after extraction of a bill, and REVIEW on a bill field below the threshold (AC8); the intake item it observes is created by JOB-12 and then resolved by extraction. The inspection task and the R-DIL-22 move to ASSET_UNLOCK_DECISION stay in Epic 3.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FIELDCOL, test user "FC-01" | Sends the captures of the journey for a case in Own scope (Documents CR); the only writer in the run |
| RW-CASEOWN | Reads the captures and the bill fields in the evidence where a scenario names them (Documents CRU) |
| RW-RESTRUCT, restructuring officer | Reads the captures on a deed in lieu case in the evidence (Documents CRU) |
| SY-OCR, OCR and extraction pipeline | Supplies the extracted bill fields and their confidence through rwb-document only |
| SY-DECLOG, decision log writer | Supplies the DOCATT record the harness asserts, through rwb-decision's contract only |
| RW-PHONECOL, phone collector | The negative case when the access fake is exercised (Documents R); never sends a capture |
| Integration lead | Agrees the four contract versions and the intake profile with the owning teams |
| QA lead | Owns the seed pack, the evidence pack and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-013 | recovery_case | entry_date | Read through the P3 case operation |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Read through the P5 document operations; written by rwb-document, never by the harness |
| DF-DOC-027 | document | captured_at | Read through the P5 document operation |
| DF-DOC-028 | document | capture_latitude | Read through the P5 document operation |
| DF-DOC-029 | document | capture_longitude | Read through the P5 document operation |
| DF-DOC-030 | document | client_file_id | Read through the P5 document operation |
| DF-DOC-031 | document | capture_kind | Read through the P5 document operation |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Read through the P5 document operation; written by rwb-document through JOB-12 |
| DF-REF-219 | document_type | doc_type_code | Read through the P3 reference-data operation |
| DF-REF-224 | document_type | field_definitions | Read through the P3 reference-data operation |
| DF-REF-246 | document_hub_parameter | param_value | Read through the P3 parameter operation |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation |

The harness owns no table and no schema (DP-01, DP-15). It reads and writes only through the published operations, and its own evidence holds document identifiers, statuses, message codes and timestamps only, never a file, a position or a bill value. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/field-captures` | P5 rwb-document | The capture request under test (AC1, AC4, AC5, AC6, AC7), with an Idempotency-Key per scenario |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Reads the document list with type, source, capture time, position and review state (AC1, AC2, AC4, AC5, AC6, AC7) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | Reads one document, its capture columns and, for a bill, its extracted fields with confidence (AC2, AC3, AC8) |
| GET | `/api/recovery/document/v1/review-items` | P5 rwb-document | Asserts the bill with a low-confidence field in the review queue (AC8) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case state, the entry date and the task the journey starts from (AC1, AC7) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | Confirms the role, the scope and the Documents right the sync runs under (AC1, AC7) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the DOCATT entry per stored document and the absent entry per refused item (AC1, AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout and the breaker of DP-11, and the POST carries an Idempotency-Key (BR4). The scope check that rwb-document makes inside its own process is not a separate path in the Ownership Map, so the harness confirms the right through the P4 session operation instead. The reference-data and parameter reads named in section 11 are rwb-case contract operations called by rwb-document, not by the harness, and their paths are not restated here.

#### 12.3 Events published

None. The harness publishes no Kafka event; the evidence goes to the release record through its pipeline integration.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Asserts one event per accepted document, ten for AC1, six for AC5, none for a refused or quarantined item (AC1, AC4, AC5, AC6, AC7) |
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` | P5 rwb-document | Asserts the extracted bill fields of AC3 and the review state of AC8 without reading a table |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the DOCATT record of each stored document reached the shared topic inside the run window (DP-03, DP-09), alongside the ledger read of 12.2 |

The harness subscribes with its own consumer group and asserts the event, never the producer's table. Key is `caseId`; the payload carries IDs and facts only.

#### 12.5 Workflows and activities

JOB-12 Document intake (`DocumentIntakeWorkflow` on queue `rwb-document`) is exercised, not built: the harness waits for its window after the sync, records the intake item per bill and per checklist, and asserts the state extraction leaves behind (AC1, AC3, AC8). JOB-11 Outbox sender is observed on its every-minute window for `DocumentStored` and `DocumentFieldsExtracted`.

Legacy section 12 has the store and the listener create the intake item inside the monolith; Architecture v5 slide 16 gives rwb-document `DocumentIntakeWorkflow` with OCR, classify and extract, and slide 44 gives JOB-12 the every-15-minute window with KEDA workers. The harness follows the higher source, so it asserts the item and the fields after the window rather than a call inside the request.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; JOB-12's window and JOB-11's minute timer are the platform's and are only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-document, field captures | `POST /api/recovery/document/v1/cases/{caseId}/field-captures` | OpenAPI of P5 | 200 with one result per item, status ACCEPTED, DUPLICATE, REFUSED or QUARANTINED, with the message code of AC6; 404 with MSG-P4-003 for AC7; keeps the request journal for the idempotency assertions of AC4 and AC5 |
| WireMock rwb-document, reads | `GET .../documents`, `GET /documents/{documentId}`, `GET /review-items` | OpenAPI of P5 | The ten documents of AC1 with type, source, capture time and position, the bill fields of AC3, the single review item of AC8 |
| WireMock rwb-document, intake profile | JOB-12 `DocumentIntakeWorkflow` outcome | The P5 intake contract | The intake item per bill and the extracted fields with confidence 0.5500 on the amount for AC8 |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | The case state, entry date 2026-10-02 and the task for `FC-01` of AC1; no task for `RW-2026-000502` in AC7 |
| WireMock rwb-access | `GET /api/recovery/access/v1/me/session` | OpenAPI of P4 | Role RW-FIELDCOL, the Own scope and Documents right C; the refusal of MSG-P4-003 for AC7 |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The DOCATT entry per stored document and the absent entry per refused item; 503 for X6 |
| Malware-scan and intake profile | The scan and store step rwb-document makes before storage | The rwb-document profile, not a service contract | Clean for the ten files of AC1, a threat for the EICAR file of AC6, a size refusal for MSG-P5-017 when the profile is switched to 1 MB |

Each fake is replaced by the real service as its I story lands, without a change to the scenarios. The concrete fake mappings, the intake profile and the evidence format: Not specified in the source documents (GAP-0406; ASM-0581).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop on the owner's base with the 2 s timeout of DP-11; Idempotency-Key on the POST |
| Kafka | 3 events consumed on `rwb.document.events.v1` and `rwb.decision-record.v1`; none published |
| Temporal | Observed only: JOB-12 Document intake on queue `rwb-document` and JOB-11 Outbox sender; no workflow, activity or schedule added |
| File | None. The synthetic files travel in the multipart request body and are never written to a shared share or a fixture folder by the harness |

### 13. Solution plan

**Package.** Folder `integration/recovery-document-capture` in the ACE repository, package `<ACE base package>.recovery.integration.documentcapture`. Not part of any deployed service, and it ships no Flyway script and no schema of its own (DP-15 applies to rwb-document, which owns the capture columns).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every document, case, session and ledger read is an operation of 12.2 |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The DOCATT entry is read through rwb-decision and the `DecisionRecorded` event on the shared topic, per stored document |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The clock skew 5, the age limit 30 and the file limit 50 are read as parameters, so a boundary scenario needs a parameter change and no code change |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The three document types and the UTILITY_BILL field list are seeded reference data, never values in the harness code |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group and counts the events per accepted item; it never reads an outbox table |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | Each consumed operation is called once from the harness with a 2 s timeout and an Idempotency-Key on the POST; no chain is built |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The capture columns are rwb-document's own Flyway change; the harness asserts the columns through the contract and runs no migration |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real case screens use, on the owners' own bases, so a route fault is found in SIT |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the four I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date, and owns the run lock |
| FakeRegistry | Configuration | WireMock mappings for the four services and the intake profile, one set per contract version |
| CapturePack | Data | The synthetic files and manifests of each scenario: eight photos and two bills, a HEIC file, an EICAR file, a bill image with the amount and due date of AC3, and the parameter boundary sets |
| DocumentAssertion | Service | Reads the document list and one document through rwb-document and compares count, type, source, capture time, position, review state and extracted fields |
| DecisionAssertion | Service | Reads the decision log and the shared topic and compares the DOCATT record per stored document, with none for a refused item |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with request, response, item results, document reads, review items and decision entries |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached |

**Environment and test data.** SIT, the wave 2 harness profile, business date 2026-12-15, synthetic files only. The seeded values are the legacy section 7 Background and the state each scenario names; no other value is added, and no file shows a person or a real address. The environment, the seed pack and the evidence format: Not specified in the source documents (GAP-0406; ASM-0581).

**Build steps**

1. Write the CapturePack for the Background and the eight scenarios, including the parameter boundary sets; test that a bad seed stops the run (X7).
2. Write the FakeRegistry with the four WireMock mapping sets and the intake profile, and pin each contract version in the run report; fail the run on a version mismatch (X1).
3. Write the JourneyRunner for AC1: the session and case reads, the sync of ten files, the ten document reads and the ten events.
4. Add the DocumentAssertion for the capture time, the position and the stored date, which carries AC2 and the offline replay.
5. Add AC3 and AC8 with the JOB-12 window, the extracted fields of the bill, the confidence 0.5500 and the review queue read.
6. Add AC4 and AC5 with the request journal and the two Idempotency-Keys, and the duplicate count of ten and six.
7. Add AC6 and AC7: the per-item refusals of MSG-GEN-002, MSG-P5-001 and MSG-P5-016 with the batch answering 200, then the 404 of MSG-P4-003 with no document and no event.
8. Write the EvidenceCollector and the GateEvaluator, attach the report to the wave 2 release record, and rerun the eight scenarios on the release build.

**Feature switch.** `rwb.dochub.field-capture` is on in the harness profile, as the legacy story sets it; the harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all eight owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The intake profile and the evidence sign-off wait for the values of GAP-0406.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-015 | Captures accepted with no GPS position | {count} files have no location. They are on the case without a position. |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-003 | A bill field needs checking | Some fields need checking. The document is in the review queue. |
| MSG-P5-016 | A capture with malware | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P5-017 | A capture above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P7-003 | Decision log write failed for an item | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Manifest and files do not match | Enter {field}. |
| MSG-GEN-002 | Capture time in the future; too many files | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Capture time before the case entry date or the age limit | {field} cannot be before {other}. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the collector's scope | This case is not in your scope. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a date. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-30 Case documents | List | Sees inspection photos, checklists and bills with capture time and position; bill fields with confidence; MSG-P5-015 on captures without position |
| SCR-31 Document review queue | List | Sees a bill with a low-confidence field in review (RWB-E1-054) |

No screen is built by this story. The harness drives the operations behind those screens through the gateway route of DP-19 and asserts the states a case owner would see, so a passed run means SCR-30 and SCR-31 have the right data behind them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-16-ITG | Access, AC7 | Component | RW-PHONECOL user (Documents R) calls the capture operation and is refused with MSG-P4-002 |
| TC-E2-024-17-ITG | Principle 5, BR9 | NFR | Decision log write forced to fail during a sync of three files; no document stored, items returned with MSG-P7-003, incident raised |
| TC-E2-024-01-ITG | AC1, BR1, BR5, BR6 | Integration | Ten synthetic files with positions in Bangkok; ten documents, two intake items, ten DocumentStored events and ten DOCATT records |
| TC-E2-024-02-ITG | AC2, BR2 | Integration | Capture one day before sync; captured_at 2026-12-14 10:05 against stored date 2026-12-15 08:30 |
| TC-E2-024-03-ITG | AC3, BR7 | Integration | Synthetic utility bill image; amount "1,284.50" and due date "28/12/2569" read as 1284.50 and 2026-12-28 |
| TC-E2-024-04-ITG | AC4, BR4 | Integration | The same ten client file IDs twice; ten DUPLICATE and ten documents |
| TC-E2-024-05-ITG | AC5, BR4 | Integration | Six of ten received, then all ten resent; six DUPLICATE, four ACCEPTED, ten documents |
| TC-E2-024-06-ITG | BR2 | Integration | Photo with no position; MSG-P5-015 with count 1 (legacy AC6, asserted here as the message path of the journey) |
| TC-E2-024-07-ITG | AC6, BR3 | Integration | Capture times 6 and 5 minutes after receipt; the 14:26 item refused with MSG-GEN-002, the 14:25 item accepted |
| TC-E2-024-08-ITG | BR3 | Integration | Capture one day before the entry date; MSG-GEN-003 naming "Capture time" and "Case entry date" |
| TC-E2-024-09-ITG | BR3 | Integration | Captures 31 days and 30 days before sync; the first refused with MSG-GEN-003, the second accepted |
| TC-E2-024-10-ITG | AC6, BR1 | Integration | HEIC file refused with MSG-P5-001 while the other items of the same sync are accepted |
| TC-E2-024-11-ITG | AC6, BR1 | Integration | EICAR test file quarantined with MSG-P5-016 and no document written |
| TC-E2-024-12-ITG | AC7 | Integration | Case "RW-2026-000502" with no task for FC-01; 404 with MSG-P4-003, no document and no event |
| TC-E2-024-13-ITG | AC8, BR7 | Integration | Bill amount at confidence 0.5500 against the threshold 0.80; state REVIEW, one review item, MSG-P5-003 |
| TC-E2-024-14-ITG | BR5 | Integration | Three manifest items and two files; 422 with MSG-GEN-001 naming the client file ID with no file, nothing stored |
| TC-E2-024-15-ITG | BR5 | Integration | 51 files against the parameter 50; 413 with MSG-GEN-002 naming "Files", 1 and 50, nothing stored |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the four contracts and the intake profile. The app stories keep the unit and component copies of the same cases.

### 17. Guardrails

- No business value in code: the three document types, the UTILITY_BILL field list, the clock skew, the age limit, the file limit and the confidence threshold are parameters and reference data.
- No personal data in events, workflow inputs, logs, evidence or prompts. The harness evidence carries document identifiers, statuses, message codes and timestamps only, never a file, a position or a bill value.
- No read of another service's tables and no schema of the harness's own: every read and write goes through the operations of 12.2 (DP-01).
- GPS position and photos of a home are personal data (BR8): the synthetic files show no person and no real address, and a position appears only as the value a contract returns, once, in the report.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and an exception is never added to a scenario; a value that must change changes in the seed pack or the parameters through a reviewed change.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-16-ITG, TC-E2-024-17-ITG, TC-E2-024-01-ITG, TC-E2-024-02-ITG, TC-E2-024-03-ITG, TC-E2-024-04-ITG, TC-E2-024-05-ITG, TC-E2-024-06-ITG, TC-E2-024-07-ITG, TC-E2-024-08-ITG, TC-E2-024-09-ITG, TC-E2-024-10-ITG, TC-E2-024-11-ITG, TC-E2-024-12-ITG, TC-E2-024-13-ITG, TC-E2-024-14-ITG, TC-E2-024-15-ITG |

### 19. Out of scope

- The field app itself and its offline store.
- Agency field teams reaching the Workbench through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (FEAT-TRT-15 and R-DIL-22, Epic 3).
- The repossessed vehicle photo standard (CTL-38, Epic 7).
- The production code of any service: the endpoint, the capture columns, the extraction rule and the decision record are the deliverables of RWB-P5-E2024-APP, RWB-P4-E2024-APP, RWB-P3-E2024-APP and RWB-P7-E2024-APP.

The harness and its fakes cover the items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
