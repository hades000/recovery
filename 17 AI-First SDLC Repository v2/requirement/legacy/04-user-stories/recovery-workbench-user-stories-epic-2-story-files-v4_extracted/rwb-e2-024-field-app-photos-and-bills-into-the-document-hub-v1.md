<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 024 Field app photos and bills into the document hub v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 024 Field app photos and bills into the document hub v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-024 Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-024 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-21 Take field app photos and bills into the OCR intake |
| Requirement IDs | REQ-DCM-013 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D6.5 |
| Priority | Must |
| Depends on | RWB-E1-057, RWB-E1-032, RWB-E1-053, RWB-E1-024, RWB-E1-041 |
| Status | Ready for build |

## 1. Story

As a **field collector**, I want **photos, bills and checklists captured in the field app to enter the document hub against the case, with location and time**, so that **an inspection is on the case the same day it is made**.

## 2. Business rationale

Inspection photos and utility bills are sent today by chat or carried back to the office, and the date and place of an inspection cannot be shown when it is questioned. This story takes each capture from the field app into the same malware scan, store, OCR and extraction path as other documents, attached to the case with the capture time and the GPS position, including captures made with no signal. It meets REQ-DCM-013 and gives the deed in lieu inspection step (WITH_FIELD_INSPECTION, R-DIL-22) and the repossessed vehicle photo record (CTL-38) their evidence on the case.

## 3. Preconditions

- RWB-E1-041 (MalwareScanService.scanNow), RWB-E1-024 (DocumentStore.store), RWB-E1-049 (DocumentStoredListener creates the intake item for OCR) and RWB-E1-053 (extractStep for attached documents) are done; RWB-E1-057 and RWB-E1-032 give the same intake path for files with no case.
- The field app is a bank-managed mobile app that signs in with Entra ID as role RW-FIELDCOL and calls the Workbench API. This platform is assumed: no open decision covers it. Agency field teams reach the Workbench only through the external gateway (DL03), which is not in this story.
- The document type table holds INSPECTION_PHOTO (no fields), INSPECTION_CHECKLIST (no fields) and UTILITY_BILL (bill_amount, due_date, account_ref), loaded through the RWB-E1-025 loader (assumed; DL19).
- Rows in document_hub_parameter: CAPTURE_CLOCK_SKEW_MINUTES 5; CAPTURE_MAX_AGE_DAYS 30; CAPTURE_MAX_FILES 50; INTAKE_MAX_FILE_MB 25. Values assumed (DL11).
- The field collector has a task on the case, so the case is in Own scope.

## 4. Flow

1. Field collector: captures photos, bills and the checklist in the field app; the app records for each file the device time and GPS position, and a client file ID.
2. Field app: when a signal is available, sends the captures for the case to POST /cases/{caseId}/field-captures with a manifest of the items.
3. System: checks the role, the right and the case scope, and that every manifest item has one file and every file has one manifest item.
4. System: for each item, checks the client file ID against items already received for the case; a repeat returns the earlier result.
5. System: checks file type, size, capture time and position, writes the file to the intake container, and calls MalwareScanService.scanNow.
6. System: calls DocumentStore.store with the case, the type from the item kind (photo, bill, checklist), source UPLOAD, the file and its hash; the store writes the document, the DOCATT decision log entry and DocumentStored (EV-16).
7. System: in the same transaction sets on the document captured_at, capture_latitude, capture_longitude, client_file_id and capture_kind.
8. System: DocumentStoredListener (RWB-E1-049) creates the intake item for OCR; for a UTILITY_BILL, extractStep (RWB-E1-053) writes bill_amount and due_date on the document.
9. System: returns a result per item (accepted, duplicate, refused with the message).
10. Case owner: sees the inspection photos, bills and the bill fields on SCR-30 Case documents with capture time and position.

## 5. Exception paths

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
| X11 | A role without Documents C sends captures | 403 | MSG-P4-002 | Access test TC-E2-024-16 |
| X12 | The decision log write fails for an item | Item refused; nothing stored for it | MSG-P7-003 | Principle 5 test TC-E2-024-17 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the Epic 1 scan, store, OCR and extraction path; needs no other Epic 2 story |
| Negotiable | Types, fields, limits and the clock skew are data and parameters |
| Valuable | The inspection evidence is on the case the day it is made, with time and place |
| Estimable | One endpoint, one service, five columns on document, one panel change on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic files |

## 7. Acceptance criteria

```gherkin
Feature: Field app photos and bills into the document hub

  Background:
    Given case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for field collector "FC-01" with role RW-FIELDCOL
    Given the clock skew is 5 minutes and the age limit is 30 days

  Scenario: AC1 Capture
    Given an inspection with eight photos and two bills, each with a client file ID, a capture time and a GPS position
    When the officer syncs at 2026-12-15 14:20
    Then ten documents are on case "RW-2026-000501" with source "UPLOAD": eight "INSPECTION_PHOTO" and two "UTILITY_BILL"
    Then each document shows its capture time and its latitude and longitude, for example 13.7563 and 100.5018
    Then the two bills have intake items for OCR
    Then ten DocumentStored events are in the outbox

  Scenario: AC2 Offline
    Given no signal during the visit and photos captured at 2026-12-14 10:05
    When the officer syncs later at 2026-12-15 08:30
    Then each document has captured_at 2026-12-14 10:05 and its stored date 2026-12-15 08:30

  Scenario: AC3 Bill extracted
    Given a utility bill photo showing amount "1,284.50" and due date "28/12/2569"
    When extraction runs
    Then bill_amount "1284.50" and due_date "2026-12-28" are on the case in the document index

  Scenario: AC4 The same sync sent twice
    Given the ten items of AC1 were received
    When the app sends the same ten client file IDs again
    Then the response marks all ten as "DUPLICATE"
    Then the case still has ten documents from this inspection

  Scenario: AC5 A sync cut off and resent
    Given six of ten items were received before the connection dropped
    When the app sends all ten again
    Then six items are "DUPLICATE" and four are "ACCEPTED"
    Then the case has ten documents from this inspection

  Scenario: AC6 A capture with no position
    Given a photo with capture time 2026-12-15 13:58 and no GPS position
    When the officer syncs
    Then the document is on the case with no latitude and longitude
    Then the response and SCR-30 show MSG-P5-015 with count 1

  Scenario: AC7 A capture time in the future
    Given the server receives the sync at 2026-12-15 14:20
    Given one photo has capture time 2026-12-15 14:26 and another 2026-12-15 14:25
    When the officer syncs
    Then the system refuses the photo at 14:26 with MSG-GEN-002
    Then the system accepts the photo at 14:25

  Scenario: AC8 A capture time before the case entry date
    Given a photo with capture time 2026-10-01 09:00, before the entry date 2026-10-02
    When the officer syncs
    Then the system refuses the item with MSG-GEN-003 naming "Capture time" and "Case entry date"

  Scenario: AC9 A capture older than the age limit
    Given the sync is at 2026-12-15 14:20
    Given one photo was captured at 2026-11-14 14:19, 31 days earlier, and another at 2026-11-15 14:20
    When the officer syncs
    Then the system refuses the first photo with MSG-GEN-003 naming "Capture time" and the age limit date 2026-11-15
    Then the system accepts the second photo

  Scenario: AC10 A file type not allowed
    Given a photo in HEIC format
    When the officer syncs
    Then the system refuses the item with MSG-P5-001
    Then the system accepts the other items in the same sync

  Scenario: AC11 Malware in a capture
    Given a file carrying the EICAR test signature
    When the officer syncs
    Then the system quarantines the item with MSG-P5-016 and an incident is raised
    Then the system writes no document for it

  Scenario: AC12 A case outside the collector's scope
    Given case "RW-2026-000502" where "FC-01" has no task
    When the app sends captures for "RW-2026-000502"
    Then the response is 404 with MSG-P4-003
    Then no file or document is stored

  Scenario: AC13 A bill field below the threshold
    Given the bill amount is read with confidence 0.5500 and the threshold is 0.80
    When extraction runs
    Then bill_amount has state "REVIEW" and the document is in the review queue
    Then SCR-30 shows MSG-P5-003 on the bill

  Scenario: AC14 A manifest that does not match the files
    Given a manifest of three items and two files
    When the officer syncs
    Then the response is 422 with MSG-GEN-001 naming the client file ID with no file
    Then the system stores nothing

  Scenario: AC15 Too many files in one sync
    Given 51 files in one sync and a limit of 50
    When the officer syncs
    Then the response is 413 with MSG-GEN-002 naming "Files", 1 and 50
    Then the system stores nothing
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It stores documents with review_status NOT_NEEDED, or PENDING when a bill field is in review. The inspection task and the R-DIL-22 move to ASSET_UNLOCK_DECISION are in Epic 3.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FIELDCOL, field collector | Sends captures for cases in Own scope (Documents CR) |
| RW-CASEOWN, case owner | Reads the captures and bill fields on the case (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the captures on deed in lieu cases (Documents CRU) |
| SY-OCR, OCR and extraction pipeline | Runs OCR and extraction on bills and checklists (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-PHONECOL, phone collector | Reads only (Documents R); cannot send captures |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-013 | recovery_case | entry_date | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write, through DocumentStore |
| DF-DOC-027 | document | captured_at | Write |
| DF-DOC-028 | document | capture_latitude | Write |
| DF-DOC-029 | document | capture_longitude | Write |
| DF-DOC-030 | document | client_file_id | Write |
| DF-DOC-031 | document | capture_kind | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write, through RWB-E1-053 |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DocumentStore and DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /cases/{caseId}/field-captures** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | multipart/form-data: manifest (JSON: inspectionRef, items of clientFileId, kind PHOTO, BILL or CHECKLIST, capturedAt date-time with offset, latitude, longitude, fileName) and one file part per item named by clientFileId |
| Response | 201 FieldCaptureResult: items of clientFileId, status (ACCEPTED, DUPLICATE, REFUSED, QUARANTINED), documentId, messageCode |
| Errors | 401 (MSG-P4-001); 403 no Documents C (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 413 too many files (MSG-GEN-002); 422 manifest and files do not match (MSG-GEN-001); 503 store or scanning service unavailable (MSG-GEN-006) |
| Authorization | Documents, right C, scope applied |
| Idempotency | clientFileId unique per case; a repeated item returns DUPLICATE with the first documentId |

Item-level refusals (MSG-GEN-002, MSG-GEN-003, MSG-P5-001, MSG-P5-016, MSG-P5-017, MSG-P7-003) do not fail the request; each is returned on its item. Warning MSG-P5-015 is returned when any accepted item has no position.

**Events published:** DocumentStored (EV-16) per accepted item, through DocumentStore; DocumentFieldsExtracted (EV-17) for bills through RWB-E1-053.

**Published interfaces called**

```java
// P5, RWB-E1-041
ScanResult MalwareScanService.scanNow(BlobRef file, Duration timeout);
// P5, RWB-E1-024
StoredDocument DocumentStore.store(StoreRequest request);
// P3
Optional<CaseSummary> CaseDirectory.findById(UUID caseId);
```

## 13. Solution plan

**Package.** folder `recovery/dochub/fieldcapture`, Java package `recovery.dochub.fieldcapture`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FieldCaptureController | Controller | POST /cases/{caseId}/field-captures; manifest parsing and matching to file parts |
| FieldCaptureService | Service | BR1 to BR10 per item: duplicate check, type, size, time and position checks, scan, store, capture columns |
| DocumentHubRepository | Repository | Sets the capture columns on the stored document; looks up client_file_id per case |
| CaptureDetails | React component | On SCR-30: capture time, position and a map link for each capture; MSG-P5-015 flag |

**Database**

- Flyway migration `V2_5_024__field_capture.sql` adds to document: captured_at timestamptz, capture_latitude numeric(9,6), capture_longitude numeric(9,6), client_file_id varchar(64), capture_kind varchar(12).
- Constraint `ux_document_client_file ON document (case_id, client_file_id) WHERE client_file_id IS NOT NULL`.
- Reads recovery_case.entry_date through CaseDirectory.

**Configuration and reference data**

- Document type rows INSPECTION_PHOTO, INSPECTION_CHECKLIST, UTILITY_BILL with the UTILITY_BILL fields, loaded through the RWB-E1-025 loader (DL19).
- document_hub_parameter rows CAPTURE_CLOCK_SKEW_MINUTES 5, CAPTURE_MAX_AGE_DAYS 30, CAPTURE_MAX_FILES 50 (assumed; DL11); INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB from RWB-E1-057.

**Build steps**

1. Write the migration and the client file ID constraint; repository tests.
2. Build manifest parsing and file-part matching with the 422 and 413 checks.
3. Build FieldCaptureService per item: duplicate check, type, size, time and position checks, write to the intake container, scanNow, DocumentStore.store, capture columns in the same transaction.
4. Check that DocumentStoredListener (RWB-E1-049) creates the intake item with the given type, so classifyStep skips it and extractStep reads the UTILITY_BILL fields.
5. Build CaptureDetails on SCR-30 with masking of the position for roles without the right to see it.
6. Add the contract test for the new endpoint (RWB-TE-003) and an offline replay test with a cut-off sync.

**Feature flag:** `rwb.dochub.field-capture`. Off: the endpoint returns 404.

**Done when:** the tests in section 16 pass and a synthetic inspection of ten files is on the case within 5 minutes of sync in SIT (target assumed; DL11).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-015 | Captures accepted with no GPS position (new) | {count} files have no location. They are on the case without a position. |
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

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | List | Sees inspection photos, checklists and bills with capture time and position; bill fields with confidence; MSG-P5-015 on captures without position |
| SCR-31 Document review queue | List | Sees a bill with a low-confidence field (RWB-E1-054) |

The field app screens belong to the field app and are not in this story.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-01 | AC1, BR1, BR5, BR6 | System | Ten synthetic files with positions in Bangkok |
| TC-E2-024-02 | AC2, BR2 | System | Capture one day before sync |
| TC-E2-024-03 | AC3, BR7 | System | Synthetic utility bill image |
| TC-E2-024-04 | AC4, BR4 | System | Same ten client file IDs twice |
| TC-E2-024-05 | AC5, BR4 | System | Six of ten received, then all ten resent |
| TC-E2-024-06 | AC6, BR8 | System | Photo with no position |
| TC-E2-024-07 | AC7, BR3 | System | Capture times 6 and 5 minutes after receipt |
| TC-E2-024-08 | AC8, BR3 | System | Capture one day before the entry date |
| TC-E2-024-09 | AC9, BR3 | System | Captures 31 days and 30 days before sync |
| TC-E2-024-10 | AC10, BR1 | System | HEIC file |
| TC-E2-024-11 | AC11, BR1 | System | EICAR test file |
| TC-E2-024-12 | AC12 | System | Case with no task for FC-01 |
| TC-E2-024-13 | AC13, BR7 | System | Bill amount at confidence 0.55 |
| TC-E2-024-14 | AC14 | System | Three items, two files |
| TC-E2-024-15 | AC15 | System | 51 files |
| TC-E2-024-16 | Access | Access | RW-PHONECOL user (Documents R) calls POST field-captures; refused with MSG-P4-002 |
| TC-E2-024-17 | Principle 5 | Resilience | Decision log write forced to fail during a sync of three files; no document stored, items returned with MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: types, fields, the clock skew, the age limit and the file limit are data and parameters.
- No personal data in logs, tests or prompts: positions, file names and bill values are not logged; test photos show no person or real address.
- No read of another module's tables: the case entry date and scope come through the P3 case interface and the ACE common access check.
- The device time is stored as sent, with its offset; the server never replaces it.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-17 |

## 19. Out of scope

- The field app itself and its offline store.
- Agency field teams reaching the Workbench through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (FEAT-TRT-15 and R-DIL-22, Epic 3).
- The repossessed vehicle photo standard (CTL-38, Epic 7).
