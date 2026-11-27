# RWB-P5-E2024-CON Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2024-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P5-E2024-CON-16) |
| Contract version | v1, the major version of base `/api/recovery/document/v1`, fixed by this baseline |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | H RWB-PLT-E1027-CON; H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON; H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-021) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the field-capture API of `rwb-document` is split out of legacy RWB-E2-024 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the capture operation, the manifest and result shapes, the image and PDF type rules, the limits, the four per-item statuses, the capture block of the stored document, the error envelope, the event schema, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E2024-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members**, I want **the published contract baseline of the field-capture API of `rwb-document` — the single capture operation on base `/api/recovery/document/v1/cases/{caseId}/field-captures` with the `FieldCaptureManifest`, `FieldCaptureItem`, `CaptureBlock` and `FieldCaptureResult` shapes, the accepted image and PDF types and the limits declared as contract elements, the four per-item statuses with their message codes, the error envelope with every message ID of section 14 and its HTTP status, the `Idempotency-Key` and `clientFileId` rules, the `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` schemas with no personal data, and the fakes with their drift test**, so that **the app story of this legacy key, the store and scan capabilities of the same service, the capture screen panel and the wave 2 integration harness build against a fixed, testable contract on Day 1, and a renamed part, a different set of accepted types, a limit that moves without a document or an item status answered with the wrong code can never drift between two builds without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E2-024 carries one `multipart/form-data` operation in a section 12 of prose, with `MalwareScanService.scanNow`, `DocumentStore.store` and `CaseDirectory.findById` beside it as in-process interfaces, and it leaves the field app and the screen to infer the exact parts, the exact limits and the exact statuses. Under the target architecture the parts most likely to drift silently are exactly the ones this baseline fixes:

- a manifest part renamed or a file part no longer named by its `clientFileId`, so the app's sync and the service disagree on which file belongs to which item;
- an accepted type set that differs from `INTAKE_ALLOWED_TYPES`, so a HEIC photo is refused by one build and stored by another;
- a file limit or a size limit that moves without a document, so the app composes a batch the service answers 413 for;
- an item status outside the four declared values, or a refusal answered with a request-level error, so the app cannot tell which item failed and why;
- the capture block missing from the stored document, so a sync succeeds and the position and the time are lost;
- a `DocumentStored` payload changed or a position put into it, so a consumer cannot read it and a data steward cannot approve it.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit — the P3 parameters contract `RWB-P3-E1042-CON` and the P3 reference-data contract `RWB-P3-E1043-CON` — and it records that the case read of `rwb-case` and the capture client of the field app are consumed and faked although the plan lists them in no C row (`ASM-1883`).

It also records what the sources leave open. TSD P5 T-A.2 declares 415 for the operation and the legacy contract refuses an item with MSG-P5-001 and keeps the request at 201; this baseline declares 415 for a request whose content type is not `multipart/form-data` and keeps the item-level refusal at 201 with status REFUSED (`ASM-1889`). The field-level names of the manifest beyond the legacy list, the stored-answer window of `Idempotency-Key` and the not-found message are Not specified in the source documents (GAP-1019; ASM-1887).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-015, and TSD P5 T3.1 and T3.2 are in force for `document` (DF-DOC-001 to DF-DOC-033), `document_intake` (DF-DOC-045 to DF-DOC-084) and the lists LOV-DOC-TYPE, LOV-DOC-SOURCE, LOV-CAPTURE-KIND and LOV-REVIEW.
- The Ownership Map is the only source of owners: `document`, `document_intake`, `document_type`, `document_field` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; `decision_log_entry` is P7's; the ACE views are P1's.
- The baselines this document sits beside are in force: the store of RWB-P5-E1024-APP (`Document` shape), the scan of RWB-P5-E1041-CON (`ScanRequest`, `ScanResult`), the intake of RWB-P5-E1057-CON (`document_intake` item) and the extraction of RWB-P5-E1053-CON (`FieldSet`).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7; `ASM-1888`), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 31 December 2026 is the legacy one and is tentative (`ASM-1892`), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (`ASM-1892`).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the capture operation, the four resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the request: the `multipart/form-data` media type, the `manifest` part as a JSON object with `inspectionRef` and `items`, and one file part per item named by its `clientFileId`.
3. Fix the `FieldCaptureItem`: `clientFileId`, `kind` (PHOTO, BILL or CHECKLIST), `capturedAt` with an offset, `latitude`, `longitude`, `fileName`; and the `CaptureBlock` the store takes: `capturedAt`, `captureLatitude`, `captureLongitude`, `clientFileId`, `captureKind`.
4. Fix the answer: `FieldCaptureResult` with `items`, each carrying `clientFileId`, `status`, `documentId` and `messageCode`, and the warning count of the items accepted without a position.
5. Declare the accepted types and the limits as contract elements with their parameter names and their legacy values, so no limit is a literal in a schema description.
6. Fix the four item statuses and their message codes, and declare which refusals are request-level and which are item-level.
7. Map every failure to the error envelope and a message ID, status by status, and carry the 415 reading and the missing C row as a gap and an assumption.
8. Record the `Idempotency-Key` rule, the stored answer of a repeat and the `clientFileId` uniqueness per case.
9. Declare the event position: `rwb.document.DocumentStored.v1` per accepted item and `rwb.document.DocumentFieldsExtracted.v1` for a bill, both with no position, no file name and no bill value.
10. Publish the seven fakes, the drift test and the baseline tag, then hand the baseline to RWB-P5-E2024-APP, the store story, the scan story and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A part or a field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2 |
| X3 | The accepted types, the file limit or the size limit differs from its parameter name or its legacy value | The contract test fails on the limits and the type rules | None | AC3 |
| X4 | An item status outside the four declared values, or a refusal answered as a request error | The contract test fails on the enum and on the status of the operation | MSG-P5-001 | AC4 |
| X5 | An error carries no `messageId`, or a message ID with the wrong status | The contract test fails on the error envelope and on the status mapping of section 14 | MSG-GEN-004 | AC5 |
| X6 | A repeat of the same `Idempotency-Key` or the same `clientFileId` creates a second document | The contract test fails on the stored-answer and uniqueness rules of AC2 | None | AC2 |
| X7 | An event payload changes, a field is added, or a position appears in it | The AsyncAPI schema test and the no-personal-data test fail | None | AC6 |
| X8 | A fake drifts from the document, or a second capture operation is declared | The drift test and the absence test fail the build | None | AC7 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, the Ownership Map and the four P5 baselines only |
| Negotiable | Pass | The field-level names beyond the legacy list are settled with the consumers; the operation, the parts, the type rules, the limits, the statuses and the event schema are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E2024-APP, the capture panel and the wave 2 harness on Day 1 |
| Estimable | Pass | One document, four resources, one operation, six consumed rows, nine contract tables and seven fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

INVEST result for each criterion above: independent Pass, negotiable Pass, valuable Pass, estimable Pass, small Pass and testable Pass.

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the field-capture API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document definitions of TSD P5 T3.1 and the operation API-P5-015 of TSD P5 T-A are in force
    Given the store baseline RWB-P5-E1024-APP, the scan baseline RWB-P5-E1041-CON, the intake baseline RWB-P5-E1057-CON and the extraction baseline RWB-P5-E1053-CON are published

  Scenario: AC1 The capture operation is declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /api/recovery/document/v1/cases/{caseId}/field-captures as the capture sync and maps it to API-P5-015
    Then the operation declares multipart/form-data with the part manifest and the file parts, and the answer 201 FieldCaptureResult
    Then the operation carries the Documents area, right C, the scope rule on the case and the statuses 201, 401, 403, 404, 413, 415, 422 and 503 as section 14 fixes them
    Then the document states that the legacy path POST /cases/{caseId}/field-captures is not declared as a monolith path and that it is served on the service base of DP-01
    Then no operation of another service's base is declared as provided

  Scenario: AC2 The manifest, the item and the result shapes are fixed, with the idempotency rules (new, D-RCV-60)
    Given the FieldCaptureManifest, FieldCaptureItem and FieldCaptureResult resources declared in the document
    When they are compared with the legacy section 12 request and answer and the TSD P5 T3.1 capture fields
    Then FieldCaptureManifest carries inspectionRef and items as required, and items is an array of FieldCaptureItem
    Then FieldCaptureItem carries clientFileId, kind, capturedAt, latitude, longitude and fileName, with clientFileId, kind and capturedAt required
    Then kind is one of "PHOTO", "BILL" and "CHECKLIST", and capturedAt is a date-time that carries its offset
    Then latitude and longitude are numbers with six decimal places and are optional, because a capture may have no position
    Then FieldCaptureResult carries items and warningCount, and each item carries clientFileId, status, documentId and messageCode
    Then status is one of "ACCEPTED", "DUPLICATE", "REFUSED" and "QUARANTINED", and messageCode is required on DUPLICATE, REFUSED and QUARANTINED and absent on ACCEPTED
    Then the manifest is one JSON part named manifest and each file part is named by its clientFileId (ASM-1891)
    Then the header Idempotency-Key is required and a repeat with the same key returns the first answer with 201 and creates no second document
    Then clientFileId is unique per caseId and a repeated item returns DUPLICATE with the first documentId
    Then the stored-answer window of the header is Not specified in the source documents (GAP-1019; ASM-1887)
    Then the example carries clientFileId "FC-0001", kind "PHOTO" and capturedAt "2026-12-15T14:05:00+07:00"

  Scenario: AC3 The accepted types and the limits are declared contract elements (new, D-RCV-60)
    Given the type and limit declarations of the document
    When they are compared with the legacy exception paths X5 and X10 and the parameters of the document hub
    Then the document declares the accepted file types as PDF, JPG and PNG, read at run time from the parameter INTAKE_ALLOWED_TYPES, and declares that the type is checked by content signature and not by file extension
    Then the document declares the file count limit as 50 per request, read at run time from the parameter CAPTURE_MAX_FILES
    Then the document declares the file size limit as 25 MB, read at run time from the parameter INTAKE_MAX_FILE_MB
    Then the document declares the clock skew of 5 minutes and the capture age limit of 30 days, read at run time from CAPTURE_CLOCK_SKEW_MINUTES and CAPTURE_MAX_AGE_DAYS
    Then no limit is written into a schema as an enum or a constant, and each is named by its parameter code
    Then more files than the limit answers 413 with MSG-GEN-002, and a refused type answers an item with status REFUSED and MSG-P5-001 while the request stays 201
    Then a file above the size limit answers an item with status REFUSED and MSG-P5-017

  Scenario: AC4 The four item statuses and the capture block of the stored document are fixed (new, D-RCV-60)
    Given the status declarations of the result and the capture block of the store request
    When they are compared with the legacy flow and the TSD P5 T3.1 fields DF-DOC-027 to DF-DOC-031
    Then the four statuses are ACCEPTED, DUPLICATE, REFUSED and QUARANTINED, and no fifth value is declared
    Then DUPLICATE answers the first documentId and a DUPLICATE item creates no second document, no second decision record and no second event
    Then REFUSED answers its messageCode, one of MSG-GEN-002, MSG-GEN-003, MSG-P5-001, MSG-P5-017 and MSG-P7-003
    Then QUARANTINED answers MSG-P5-016 and a documentId that is absent, because no document exists for a quarantined item
    Then an item accepted without a position is ACCEPTED and the answer carries warningCount with MSG-P5-015 shown on the screen
    Then the CaptureBlock the store takes carries capturedAt, captureLatitude, captureLongitude, clientFileId and captureKind, all optional, and the document declares that the store writes them in the same transaction as the document row
    Then the CaptureBlock is an additive optional block of the store request within major version 1, and the intake item for a bill and a checklist is created by the intake submit of RWB-P5-E1057-CON
    Then the document states that captureKind carries LOV-CAPTURE-KIND values and that documentType is derived from kind and never sent by the caller (ASM-1894)

  Scenario: AC5 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the capture operation
    When each status is compared with the legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 for the right and MSG-P4-003 for a case outside the scope
    Then 404 answers MSG-P4-003 for a case outside the collector's scope and the not-found message for a case that does not exist, whose ID is Not specified in the source documents (GAP-1019; ASM-1890)
    Then 413 answers MSG-GEN-002 naming "Files", 1 and 50
    Then 415 answers a request whose content type is not multipart/form-data, and the document records that the legacy contract refuses a type per item instead (ASM-1889)
    Then 422 answers MSG-GEN-001 naming the client file ID with no file or the file with no item
    Then 503 answers MSG-GEN-006 naming the system that failed, and MSG-P7-003 for a failed decision record at request level
    Then MSG-P5-003 and MSG-P5-015 are declared as labels and warnings and not as error responses
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refused request stores no file and no document

  Scenario: AC6 The stored and extracted events and the decision record are declared schemas (new, D-RCV-60)
    Given the AsyncAPI fragments of this baseline and the record declaration of the document
    When they are compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.DocumentStored.v1 is declared on the topic rwb.document.events.v1 with its retry topics at 1 min, 10 min and 1 h and its .dlt topic
    Then the stored event is keyed by caseId and carries documentId, caseId, documentType, source, storageRef, contentSha256 and storedAt, and no position, no file name and no client file ID
    Then rwb.document.DocumentFieldsExtracted.v1 is declared for a bill, keyed by caseId, with fieldCodes, extractStatus, extractorVersion and no field value in clear
    Then the envelope is CloudEvents 1.0 in binary mode and neither payload carries a personal value and neither carries a file byte
    Then the decision record is declared on rwb.decision-record.v1 with the decision code DOCATT, final call STORED and the item kind as inputsRef content
    Then whether a refused item leaves an entry in the decision record is Not specified in the source documents (GAP-1284)
    Then the document states that the store writes both events and the record in its own transaction and that this baseline publishes nothing itself
    Then the document states that no third event is declared for this key

  Scenario: AC7 The seven fakes answer the document and the drift test fails on any mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the seven fakes of 12.8 answer the operation of 12.1 and the six reads of 12.2 with the values of the legacy examples, including case "RW-2026-000501", the entry date 2026-10-02, the positions 13.7563 and 100.5018, the limit of 50 files and the size limit of 25 MB
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a part name, a status, a field name or a required flag
    Then the absence test fails a build that declares a second capture operation, an event name outside rwb.document.<Event>.v1, or a position in a payload
```

The seven criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E2024-APP. The legacy AC1 to AC15 are owned by RWB-P5-E2024-APP, and the wave 2 harness consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Arch v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Arch v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | The event names of this service follow `rwb.document.<Event>.v1` on its own topic, and the baseline declares two events and one record and no third event | Arch v5 slides 16 and 42; DP-09; DP-14 |
| BR6 | No business value is fixed in the contract: the accepted types, the limits, the clock skew, the age limit, the type codes and the decision code are parameters, reference rows or document defaults | Template and Rules §R7.2 s17; RWB-E2-024 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, confidences, dates, synthetic positions and the file names of synthetic files only, and no customer name, address, national ID number or real position in any payload | Arch v5 slide 11; RWB-E2-024 section 17; CTL-11 |
| BR8 | A position and a file name never enter the event or the record: the payload carries the document ID, the type, the source and the hash, and the position stays behind the masked read | DP-09; RWB-E2-024 section 17 |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed; the scan row states its own 30 s declared budget | DP-11, ADR-020; Arch v5 slide 11; RWB-P5-E1041-CON |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E2-024 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer; the operation is idempotent twice over, by the header and by the unique client file ID per case | Architecture v5 slide 11; DP-09; legacy AC4 and AC5 |
| BR12 | The contract declares no case state and no document state machine beyond the values a field may take and the four item statuses; a transition belongs to the app story that performs it | RWB-E2-024 section 9; RWB-P5-E2024-APP owns the item statuses |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The operation, the four resources, the six consumed rows and the event schemas are described | In review |
| In review | Consumer sign-off | RWB-P5-E2024-APP, the store owner, the scan owner and the wave 2 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `inspectionRef` on the result | Baselined |
| Baselined | Breaking change | A part, a property or a status is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The four item statuses are values of `FieldCaptureResult.items[].status`, and the transitions between them belong to RWB-P5-E2024-APP.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `status` = "ACCEPTED" | The item and its file carried every check and the store committed; `documentId` is present |
| `status` = "DUPLICATE" | The client file ID already exists on the case; the first `documentId` is returned and nothing new is stored |
| `status` = "REFUSED" | Type, size, capture time, position or the decision record failed a check; `messageCode` names which |
| `status` = "QUARANTINED" | The scan answered INFECTED; the file stays in `rwb-quarantine` and no document exists |
| `captureKind` = "PHOTO", "BILL" or "CHECKLIST" | The item kind, carried on the stored document; the document type is derived from it |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragments and the seven fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the resolution of `GAP-1019` |
| Consuming teams (RWB-P5-E2024-APP, the store owner, the scan owner, the capture panel, the wave 2 harness) | Review and sign off the parts they consume |
| RW-FIELDCOL, the field collector role | Confirms that the manifest and the result carry what the app needs to resend safely (Documents C on the case) |
| RW-CASEOWN, the case owner role | Confirms that the capture block gives the screen its time and position (Documents R on the case) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no position, file name or bill value is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1019; ASM-1887). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here. The declared area DOCUMENTS with the right C for the capture and R for the read is named here; the rwb-access authorise path and its request and answer shape are Not specified in the source documents (GAP-0952), and this baseline does not call that operation.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| FieldCaptureManifest | inspectionRef (string), items (array of FieldCaptureItem); both required |
| FieldCaptureItem | clientFileId (string, required), kind (one of PHOTO, BILL, CHECKLIST, required), capturedAt (date-time with offset, required), latitude (numeric(9,6), optional), longitude (numeric(9,6), optional), fileName (string, optional); from `document` DF-DOC-027 to DF-DOC-031 |
| FieldCaptureResult | items (array of the result item), warningCount (integer); each result item carries clientFileId, status, documentId, messageCode |
| CaptureBlock | capturedAt, captureLatitude, captureLongitude, clientFileId, captureKind, all optional; the block the store of RWB-P5-E1024-APP takes |
| Document | the store's shape answered for an accepted item: documentId, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion |
| Item status set | ACCEPTED, DUPLICATE, REFUSED, QUARANTINED, and no fifth value |
| Intake item (for a bill and a checklist) | the `document_intake` item created by RWB-P5-E1057-CON, from DF-DOC-045, DF-DOC-046, DF-DOC-055 and DF-DOC-057 |
| DecisionRecord | decisionCode DOCATT, finalCall STORED, inputsRef, decidedAt and the chain fields of the library; the item kind and the type are inputsRef content |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: case "RW-2026-000501", the entry date 2026-10-02, the positions 13.7563 and 100.5018, the sync time 2026-12-15 14:20, the limit of 50 files and the size limit of 25 MB. No example carries a real customer value and no example carries a real position: the coordinates are the legacy illustrative pair. The field-level names of the manifest and the result beyond the legacy list are Not specified in the source documents (GAP-1019; ASM-1887), and the baseline fixes them as the smallest superset of that list. The position fields (latitude, longitude, captureLatitude and captureLongitude) and fileName are classed as personal data; the baseline carries them and TC-P5-E2024-CON-06 runs the no-personal-data test over them. The BR Field ID of each row above is Not specified in the source documents (DOR-RWB-P5-E2024-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/field-captures` | API-P5-015 | Request `multipart/form-data`: part `manifest` (`FieldCaptureManifest`) and one file part per item named by its `clientFileId`; answer 201 `FieldCaptureResult`; item-level refusals stay at 201 with status REFUSED, DUPLICATE (with `documentId`) or QUARANTINED (with `messageCode`) | Documents C, scope applied to the case | `Idempotency-Key` header plus `clientFileId` unique per case |

Request-level statuses 401, 403, 404, 413, 415, 422 and 503 are those of T-A.2 and section 14. The legacy path `POST /cases/{caseId}/field-captures` is the same operation on the service base of DP-01, and the path is declared with the `/api/recovery/document/v1` prefix and nowhere else.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its entry date and the task that puts it in the collector's scope; one hop, 2 s, faked; the contract is RWB-P3-E1018-CON and the plan lists it in no C row (`ASM-1883`) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `CAPTURE_CLOCK_SKEW_MINUTES`, `CAPTURE_MAX_AGE_DAYS`, `CAPTURE_MAX_FILES`, `INTAKE_ALLOWED_TYPES` and `INTAKE_MAX_FILE_MB` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-CAPTURE-KIND, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW (C `RWB-P3-E1043-CON`) |
| POST | `/api/recovery/document/v1/scans` | P5 rwb-document, same service | The scan before storage, `ScanResult` CLEAN or INFECTED, 30 s declared budget (RWB-P5-E1041-CON) |
| POST | the store command of RWB-P5-E1024-APP | P5 rwb-document, same service | The document row with the optional capture block (RWB-P5-E1024-APP; `ASM-1877`) |
| POST | the intake submit of RWB-P5-E1057-CON | P5 rwb-document, same service | The `document_intake` item for a bill and a checklist; the path and shape are fixed by that baseline and are Not specified in the source documents (GAP-1019; `ASM-1878`) |

Every cross-service row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to an item answered as accepted. The scan row carries the 30 s declared budget of its own baseline and is the one declared exception to the 2 s rule. The case read is consumed and faked and is named in no C row of the plan, so it carries `ASM-1883` and no row is added to the metadata C list. The capture client of the field app is the party that sends the request; it is not a consumed operation and it is faked for the tests.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (the legacy EV-16) | `rwb.document.events.v1` | P5 rwb-document | Key caseId; payload documentId, caseId, documentType, source, storageRef, contentSha256, storedAt; CloudEvents 1.0 binary mode; no position, no file name, no client file ID, no file byte; one event per accepted item |
| `rwb.document.DocumentFieldsExtracted.v1` (the legacy EV-17) | `rwb.document.events.v1` | P5 rwb-document | Key caseId; payload intakeItemId, documentId, documentType, fieldCodes, extractStatus, extractorVersion, extractedAt; field codes only and no field value in clear; for a bill |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | The hash-chained record with decision code DOCATT, final call STORED, the source UPLOAD and the item kind, and `inputsRef` naming the document |

This baseline declares the event schemas because the service owns the topic; the event rows themselves are written by the store path of RWB-P5-E1024-APP inside its transaction, and this key publishes nothing at run time (`ASM-1893`). Arch v5 slide 42 lists `DocumentStored` and `DocumentFieldsExtracted` for this service and this baseline declares exactly those two names. No third event exists for this key.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This baseline consumes no event: the trigger is the field app's request, and the intake item is created inside the same request through the intake submit of RWB-P5-E1057-CON |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| None | — | — | The capture path is synchronous and declares no workflow, no activity and no compensation. `DocumentIntakeWorkflow` on queue `rwb-document` reads the intake items this operation creates; it is owned and registered by RWB-P5-E1049-APP and is named here only to show where the item goes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This baseline declares no Schedule and no cron entry; the intake Schedule is registered and monitored by the stories that own the intake pipeline |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document` | P5 (`rwb_document`) | The capture columns DF-DOC-027 to DF-DOC-031 behind the capture block and the `Document` shape the answer carries, written by the store |
| `document_intake` | P5 (`rwb_document`) | The item created by the intake submit for a bill and a checklist; DF-DOC-045, DF-DOC-046, DF-DOC-055 and DF-DOC-057 |
| `document_type` | P5 (`rwb_document`) | The type code, the field list and the write-once flag of the three types, read locally in the version in force |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the rows behind the five parameters |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record the store writes |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency row behind `Idempotency-Key` and the event envelope objects |

`recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `decision_log_entry` is P7's, and the ACE views are P1's and are named as consumed answers and never declared as this service's tables (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case WireMock | `GET /cases/{caseId}` for case "RW-2026-000501" open with entry date 2026-10-02 and a field inspection task, case "RW-2026-000502" with no task for the collector, and a delayed answer beyond 2 s | App story, contract tests |
| parameters WireMock | `CAPTURE_CLOCK_SKEW_MINUTES` 5, `CAPTURE_MAX_AGE_DAYS` 30, `CAPTURE_MAX_FILES` 50, `INTAKE_MAX_FILE_MB` 25 and `INTAKE_ALLOWED_TYPES` "PDF,JPG,PNG" | App story, contract tests |
| reference-data WireMock | LOV-CAPTURE-KIND with PHOTO, BILL and CHECKLIST; LOV-DOC-TYPE with INSPECTION_PHOTO, INSPECTION_CHECKLIST and UTILITY_BILL; LOV-DOC-SOURCE with UPLOAD; LOV-REVIEW with the four review states | App story, contract tests |
| scan fake | `ScanResult` CLEAN for a synthetic file, INFECTED for the EICAR signature, and a 30 s budget answer | App story, contract tests |
| document store fake | The `Document` answer with the capture block applied, the duplicate answer with the existing document ID, and the COPY_PENDING state | App story, contract tests |
| intake submit fake | The `document_intake` item ID for a bill and a checklist, with source UPLOAD and the type derived from the item kind | App story, contract tests |
| capture client fake | A manifest, one file part per item, the resend of the same client file IDs, a three-item-two-file mismatch and a 51-file batch | Contract tests |
| error envelope fake | One answer per message ID of section 14 with its status and its `detail` text | Contract tests, capture panel |

A drifted fake fails the drift test of AC7. The exact response field names of the case read are Not specified in the source documents (GAP-1019; ASM-1883).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The capture operation; the case read, the parameters read and the lists read; the scan, the store and the intake submit of the same service; one hop and 2 s on every consumed cross-service call and the 30 s scan budget |
| Kafka | 2 event schemas and 1 record declared, 0 consumed | `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`, the record on `rwb.decision-record.v1` |
| Temporal | 1 workflow named, 0 declared | `DocumentIntakeWorkflow` on queue `rwb-document`, owned by RWB-P5-E1049-APP; no activity and no Schedule |
| File | 3 references and 1 read | The file parts of the request, the quarantine object the scan reads and the stored blob `storageRef` points at; this baseline carries no byte |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the capture operation and the four resources; the AsyncAPI 3.0 fragments for `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` and the record declaration; the contract README rows for the type rules, the limits, the item statuses, the error mapping and the idempotency rule; and the eight WireMock mapping sets of section 12.8.

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

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own, and the platform and service contracts it names are the ones the app story declares (`ASM-1888`). DP-01 is applied because every shape derives from a table of `rwb_document` and no other schema is declared. DP-03 is applied because the store's record is declared and faked here, although the row is written by the store of RWB-P5-E1024-APP. DP-06 and DP-07 are the two C rows: the five parameters and the four lists are read through the `rwb-case` contracts and never typed into the document. DP-09 fixes the topic, the two event schemas, the envelope and the `Idempotency-Key` rule. DP-11 fixes the three consumed cross-service rows to one hop with 2 s and a fake each, and records the 30 s scan budget as the one declared exception. DP-15 records that the five capture columns behind the capture block belong to this service's own migration sequence. DP-19 records that the capture detail panel of SCR-30 is reached through the gateway-bff composite route; this baseline fixes the answer shapes only and no route specification.

**Build steps**

1. Write the operation with its path, media type, parts, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and the manifest-to-file-part rule as schema constraints and README rows.
3. Declare the type rules and the limits of AC3 with their parameter codes and legacy values, and no literal in a schema description.
4. Declare the four item statuses, their message codes and the capture block of AC4.
5. Map every status and message ID of AC5 and record the RFC 9457 envelope, including the 404 and 401 placeholders and the 415 reading.
6. Record the `Idempotency-Key` rule and the `clientFileId` uniqueness of AC2.
7. Declare the two events and the record of AC6, with the no-personal-data test and the absence test for a second operation and a foreign event name.
8. Publish the eight fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E2024-APP, the store owner, the scan owner and the wave 2 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragments validate in the pipeline, the eight contract tests pass, the eight fakes answer the operation and the six reads of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E2024-APP and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-015 | Items accepted with no position (a warning, not an error) | {count} files have no location. They are on the case without a position. | 201 |
| MSG-P5-001 | File type not allowed (an item status) | This file type cannot be stored. Use PDF, JPG or PNG. | 201 on the item |
| MSG-P5-003 | A bill field needs checking (a label, not an error) | Some fields need checking. The document is in the review queue. | 201 on the item |
| MSG-P5-016 | A capture with malware (an item status) | This file was not stored because the malware scan found a threat. It is held in quarantine. | 201 on the item |
| MSG-P5-017 | A capture above the size limit (an item status) | This file is larger than {size} MB and cannot be stored. | 201 on the item |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 201 on the item, 503 at request level |
| MSG-GEN-001 | Manifest and files do not match | Enter {field}. | 422 |
| MSG-GEN-002 | Too many files, or a capture time in the future | {field} must be between {min} and {max}. | 413, or 201 on the item |
| MSG-GEN-003 | Capture time before the case entry date or the age limit | {field} cannot be before {other}. | 201 on the item |
| MSG-GEN-004 | A repeat with a changed record | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Case outside the collector's scope | This case is not in your scope. | 404 |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-1019; ASM-1887) | 401 |
| MSG-GEN-006 | The case read, the scan or the intake submit failed | {system} is not available. Your request is queued and will be retried. | 503 |
| not-found message | A case that does not exist | Not specified in the source documents (GAP-1019; ASM-1890) | 404 |

The message IDs and the wording are contract elements copied unchanged from RWB-E2-024 section 14; Thai text for each follows decision DL10, which is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the directive. MSG-P4-001, MSG-GEN-004, MSG-GEN-006 and the not-found message are named by the platform error envelope and are copied from the platform set, and their exact texts are recorded as the placeholder above.

Delivery shape: every request-level error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one plus the platform rows: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003 or the not-found message, 409 with MSG-GEN-004, 413 with MSG-GEN-002, 415 for a content type other than `multipart/form-data`, 422 with MSG-GEN-001, and 503 with MSG-GEN-006 or MSG-P7-003 at request level. An item-level refusal is not a request error and the request stays 201 with the item status. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed, and it is "Case service" for the case read.

### 15. Screens and states

SCR-30 Case documents is the screen these shapes serve, reached through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; the capture detail panel and the no-position flag are RWB-P5-E2024-APP and the case document list is RWB-P5-E1026-APP. This baseline fixes the answer shapes only and declares no screen field list and no route specification. The states its shapes imply are: an item in each of the four statuses, an item accepted without a position, a batch refused at request level for the file count, and a capture whose position is masked for a role without the right to see it. The loading state is the one Screen Specifications v1 defines for SCR-30; the empty, error and no access states are Not specified in the source documents (CG-ALL-6223).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E2024-CON-01 | AC1, BR1, BR4 | Contract | The OpenAPI 3.1 document validates; the single operation and its statuses are declared; no foreign base is provided |
| TC-P5-E2024-CON-02 | AC2, BR3, BR11 | Contract | A manifest of one photo and one bill with the file parts named by clientFileId; a renamed part fails the lint; the same `Idempotency-Key` twice answers one result |
| TC-P5-E2024-CON-03 | AC3, BR6 | Contract | The type rules and the four limits with their parameter codes; a literal limit in a schema description fails the test |
| TC-P5-E2024-CON-04 | AC4, BR12 | Contract | One item in each of the four statuses and the capture block; a fifth status fails the schema |
| TC-P5-E2024-CON-05 | AC5, BR10 | Contract | One answer per message ID of section 14 with its status; a missing `messageId` fails the test; the 415 reading is declared |
| TC-P5-E2024-CON-06 | AC6, BR7, BR8 | Contract | The two AsyncAPI fragments; a position or an eighth field added to a payload fails the no-personal-data test; no third event |
| TC-P5-E2024-CON-07 | AC7, BR2, BR9 | Contract | The eight fakes run against the document; a drifted path, part name, status, field name or required flag fails the drift test |
| TC-P5-E2024-CON-08 | AC1, BR1 | Contract | Boundary of the section 12.7 tables: each of the six tables names its owner; a table owned by P1, P3 or P7 declared here fails the test; the idempotency tables are PLT library tables created in `rwb_document` |
| TC-E2-024-16 | X11, Access | Contract | A caller with Documents R only calls the capture operation; refused with 403 and MSG-P4-002 |
| TC-E2-024-17 | X12, Principle 5 | Contract | The decision-record fake refuses the write; the item answers REFUSED with MSG-P7-003 and no document is declared |
| TC-E2-024-01 | AC1, BR1, BR5, BR6 | Contract | Ten synthetic files with positions in Bangkok answered as ten ACCEPTED items with document IDs |
| TC-E2-024-02 | AC2, BR2 | Contract | A capture one day before the sync answered with capturedAt and storedAt as two fields |
| TC-E2-024-03 | AC3, BR7 | Contract | A synthetic utility bill image answered with the UTILITY_BILL type and the extracted fields |
| TC-E2-024-04 | AC4, BR4 | Contract | The same ten client file IDs twice answered as ten DUPLICATE items with the first document IDs |
| TC-E2-024-05 | AC5, BR4 | Contract | Six of ten received, then all ten resent: six DUPLICATE and four ACCEPTED items |
| TC-E2-024-06 | AC6, BR8 | Contract | A photo with no position answered ACCEPTED with warningCount 1 and MSG-P5-015 |
| TC-E2-024-07 | AC7, BR3 | Contract | Capture times 6 and 5 minutes after receipt: one REFUSED with MSG-GEN-002 and one ACCEPTED |
| TC-E2-024-08 | AC8, BR3 | Contract (run by RWB-P5-E2024-APP) | A capture one day before the entry date answered REFUSED with MSG-GEN-003 |
| TC-E2-024-09 | AC9, BR3 | Contract (run by RWB-P5-E2024-APP) | Captures 31 days and 30 days before the sync: one REFUSED with MSG-GEN-003 and one ACCEPTED |
| TC-E2-024-10 | AC10, BR1 | Contract (run by RWB-P5-E2024-APP) | A HEIC file answered as a REFUSED item with MSG-P5-001 while the request is 201 |
| TC-E2-024-11 | AC11, BR1 | Contract (run by RWB-P5-E2024-APP) | The EICAR test file answered as a QUARANTINED item with MSG-P5-016 and no document ID |
| TC-E2-024-12 | AC12 | Contract (run by RWB-P5-E2024-APP) | A case with no task answered 404 with MSG-P4-003 and nothing stored |
| TC-E2-024-13 | AC13, BR7 | Contract (run by RWB-P5-E2024-APP) | A bill amount at confidence 0.55 answered with MSG-P5-003 and reviewStatus PENDING |
| TC-E2-024-14 | AC14 | Contract (run by RWB-P5-E2024-APP) | Three items and two files answered 422 with MSG-GEN-001 naming the client file ID with no file |
| TC-E2-024-15 | AC15 | Contract (run by RWB-P5-E2024-APP) | 51 files answered 413 with MSG-GEN-002 naming "Files", 1 and 50 |

The seventeen legacy test cases of RWB-E2-024 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E2024-APP. TC-E2-024-16 keeps the legacy level Access and maps to Component in the app story and to Contract here, TC-E2-024-17 keeps the legacy level Resilience and maps to NFR in the app story and to Contract here, and the System level of the others maps to Contract because the artefact under test is the contract. The integration copies of the wave 2 harness end in `-ITG` and belong to that harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the accepted types, the four limits, the clock skew, the age limit, the type codes and the decision code stay parameters, reference rows or document defaults of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, dates and the illustrative coordinates of the legacy example only, and no customer name, address, national ID number or real position.
- No position, file name or bill value in an event or a record: the payload carries the document ID, the type, the source and the hash, and the position stays behind the masked read.
- The case read is consumed and faked and never declared as provided; the parameters and the lists arrive through their client libraries (DP-06, DP-07).
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view and no cross-schema join (DP-05, by removal).
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; a foreign base or a foreign table fails the review (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- The event names carry the service short and the topic is the service's own; the baseline declares exactly the two names the catalogue holds (DP-14).
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no document state machine; the four item statuses are field values and their transitions belong to RWB-P5-E2024-APP.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | The capture operation, the manifest and result shapes, the type rules and the capture block | TC-P5-E2024-CON-01, TC-P5-E2024-CON-02, TC-P5-E2024-CON-03, TC-E2-024-01, TC-E2-024-03 |
| REQ-DCM-013 | A capture carries its time and place, and a capture without a position is flagged | The `capturedAt`, `latitude` and `longitude` fields, the capture block and `warningCount` | TC-P5-E2024-CON-02, TC-P5-E2024-CON-04, TC-E2-024-02, TC-E2-024-06 |
| REQ-DRI-004 | Every decision is recorded before it takes effect | The DOCATT record declaration and MSG-P7-003 | TC-P5-E2024-CON-06, TC-E2-024-17 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the case read consumed and faked |
| DP-03 | The decision record declaration of 12.3 and the store's record |
| DP-06 | The parameters row of 12.2 and the five parameter names |
| DP-07 | The reference-list row of 12.2 and the four lists |
| DP-09 | The `Idempotency-Key` rule, the two event schemas and the CloudEvents envelope |
| DP-11 | The three consumed cross-service rows with one hop, a 2 s timeout and a fake, and the 30 s scan budget |
| DP-15 | The migration position recorded for the five capture columns |
| DP-19 | SCR-30 behind gateway-bff, and the capture panel reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E2-024; its AC1 to AC15 are owned by RWB-P5-E2024-APP, and the cross-service proof of the same values belongs to the wave 2 integration harness.

### 19. Out of scope

- The build of the capture service, the checks, the duplicate rule and the capture panel: RWB-P5-E2024-APP.
- The store, the write-once container and the version history: RWB-P5-E1024-APP.
- The scan engine and its capacity: RWB-P5-E1041-CON and its operations stories.
- The intake channels of branches, mailroom, partner SFTP and email: RWB-P5-E1057-APP.
- OCR, classification and field extraction: RWB-P5-E1049-APP, RWB-P5-E1050-APP and RWB-P5-E1053-APP.
- The review of a stored document's type and fields: RWB-P5-E1054-APP.
- The field app itself and its offline store.
- The compute, the storage, the topic and the ACL provisioning of this key, and its chart, dashboards and runbook.
- The parameters and reference-data catalogues themselves and their admin operations: P3 rwb-case.
- The cross-service proof of these values: the wave 2 integration harness.
