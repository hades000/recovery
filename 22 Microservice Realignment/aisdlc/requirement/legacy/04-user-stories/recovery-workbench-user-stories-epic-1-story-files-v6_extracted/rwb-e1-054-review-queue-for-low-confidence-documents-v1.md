<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 054 Review queue for low confidence documents v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 054 Review queue for low confidence documents v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-054 Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-054 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-10 Send a low-confidence extraction to the review queue; FEAT-DCM-11 Check a low-confidence extraction |
| Requirement IDs | REQ-DCM-005 |
| BRD section | Business Requirements Epic 1, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-049, RWB-E1-035, RWB-E1-050, RWB-E1-053, RWB-E1-032 |
| Status | Ready for build |

## 1. Story

As a **litigation officer**, I want **a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set**, so that **no document is attached wrongly and the models improve**.

## 2. Business rationale

A wrong type or a wrong hearing date on a court notice puts the wrong date on the case and the litigation timers run from it. This story shows in one queue every intake item the pipeline could not type, read or match, and every stored document with a field below its threshold; one officer confirms or corrects the type, the case and the fields on one screen, and each correction is kept as a labeled example for the model evaluations. It meets REQ-DCM-005 and moves the measure "fields extracted without review", because each correction improves the next model version.

## 3. Preconditions

- RWB-E1-049, RWB-E1-050, RWB-E1-053 and RWB-E1-032 are done: intake items carry review_reason (LOW_CONFIDENCE, UNKNOWN_TYPE, MODEL_UNAVAILABLE, RESCAN, UNREADABLE_FILE, EXTRACTION_FAILED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED), candidates, candidate cases and extracted fields; stored documents carry review_status PENDING when a field is in REVIEW.
- RWB-E1-024 is done: DocumentStore.store writes the document, its fields and the DOCATT decision log entry.
- RWB-E1-035 shows documents on the case record view.
- Rows in document_hub_parameter: REVIEW_TEAM_UNATTACHED "DOC-SVC" (assumed), REVIEW_DATE_MIN 2000-01-01, REVIEW_DATE_MAX 2100-12-31, REVIEW_PAGE_SIZE 50.
- The officer holds RW-LITOFF (Documents CRU) with team scope. Feature flag rwb.dochub.review is on.

## 4. Flow

1. Litigation officer: opens SCR-31 Document review queue.
2. System: lists, oldest first, the intake items with a review_reason and no case that belong to the officer's review team, the intake items whose candidate cases are in the officer's scope, and the stored documents with review_status PENDING on cases in scope; each row shows the reason, the proposed type, the two candidates, confidence and age.
3. Litigation officer: opens an item; the system shows the file, the OCR text, the type with its candidates, the candidate cases and the fields, with fields in REVIEW marked.
4. Litigation officer: keeps the type or chooses another type from the list in force; a new type re-runs extraction for that type and shows the new fields.
5. Litigation officer: chooses the case from the candidates, or enters a case number that the system looks up through CaseDirectory.
6. Litigation officer: confirms each marked field with Confirm, or enters the value with Correct; the system checks it against the field data type and range.
7. Litigation officer: chooses Attach; the system calls DocumentStore.store with the case, the type and the fields, which writes the document, its fields and the DOCATT decision log entry, and stores a legal type in the write-once container.
8. System: sets the intake item review_outcome ATTACHED and the document review_status CONFIRMED (nothing changed) or CORRECTED (type, case or a value changed), and writes DocumentFieldsExtracted (EV-17).
9. Litigation officer: for a stored document with a field in REVIEW, confirms or corrects the field and completes the review with POST review.
10. Center of excellence analyst: the model evaluations (RWB-E1-060) read the resolved items through LabeledSetReader.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Correct is chosen with an empty value | 422; nothing saved | MSG-GEN-001 | AC4 |
| X2 | The chosen type is not in the type list in force | 422; nothing saved | MSG-P5-006 | AC5 |
| X3 | A corrected date is outside the allowed range | 422; nothing saved | MSG-GEN-002 | AC6 |
| X4 | Attach or complete with a field still in REVIEW | 422; nothing stored | MSG-GEN-001 | AC7 |
| X5 | The chosen case is closed | 422; nothing stored | MSG-P5-005 | AC8 |
| X6 | Another officer saved the same item first | 409; the officer reloads | MSG-GEN-004 | AC9 |
| X7 | The same file is already on the chosen case | The item is linked to the existing document; no second document | MSG-P5-024 | AC11 |
| X8 | Discard without a reason | 422 | MSG-GEN-001 | AC13 |
| X9 | No item in the officer's queue | Empty state on SCR-31 | None | AC15 |
| X10 | A document outside the officer's scope | 404 | MSG-P4-003 | AC16 |
| X11 | The same confirmation is sent twice | Second call returns the saved field; nothing changes | None | AC17 |
| X12 | The user holds Documents R only | 403 | MSG-P4-002 | Access test TC-E1-054-18 |
| X13 | The decision log write fails on attach | Nothing stored; item unchanged; incident raised | MSG-P7-003 | Principle 5 test TC-E1-054-19 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Works on the review items the Epic 1 pipeline steps already produce; stores through RWB-E1-024 |
| Negotiable | The review team, date limits and the type list are data; the layout follows the ACE components (DL31) |
| Valuable | No low-confidence or unmatched document reaches a case without a person checking it |
| Estimable | One queue endpoint, three intake endpoints, the existing field endpoint, one review endpoint, one screen |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents

  Background:
    Given DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000
    Given REVIEW_TEAM_UNATTACHED is "LIT-BKK" for this test
    Given a litigation officer with role RW-LITOFF in team "LIT-BKK" with team scope

  Scenario: AC1 Queued
    Given intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    Given its review_reason is "LOW_CONFIDENCE"
    When the officer opens SCR-31
    Then the system lists "IN-0101" with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21"

  Scenario: AC2 Corrected
    Given intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW"
    When the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and chooses Attach
    Then the system stores a document on "RW-2026-000201" with type "COURT_NOTICE" and hearing_date field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID
    Then the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED"
    Then the store writes one DOCATT decision log entry
    Then LabeledSetReader returns "IN-0101" with predicted type, confirmed type, extracted value and corrected value

  Scenario: AC3 A stored document with a field to check
    Given document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING"
    When the officer chooses Confirm on black_case_no and completes the review
    Then black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID
    Then the document review_status is "CONFIRMED"

  Scenario: AC4 An empty correction is refused
    Given document "DOC-0103" has court_name in state "REVIEW"
    When the officer chooses Correct on court_name with an empty value
    Then the response is 422 with MSG-GEN-001 naming "Court name"
    Then court_name is unchanged

  Scenario: AC5 A type not in the list is refused
    Given intake item "IN-0104" in the review queue
    When the officer sets the type to "PAYSLIP"
    Then the response is 422 with MSG-P5-006 naming "PAYSLIP"

  Scenario: AC6 A date outside the allowed range is refused
    Given REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31
    When the officer corrects hearing_date on "IN-0101" to "2569-12-16"
    Then the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31"

  Scenario: AC7 Attach with a field still in review is refused
    Given intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one
    When the officer chooses Attach
    Then the response is 422 with MSG-GEN-001 naming the field still in review
    Then the system stores no document

  Scenario: AC8 A closed case is refused
    Given intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150" with status "Closed"
    When the officer chooses case "RW-2026-000150" and chooses Attach
    Then the response is 422 with MSG-P5-005 naming "RW-2026-000150"
    Then the system stores no document

  Scenario: AC9 Two officers on the same item
    Given two officers opened intake item "IN-0107" at version 3
    Given the first officer attached it, so the item is at version 4
    When the second officer chooses Attach with version 3
    Then the response is 409 with MSG-GEN-004
    Then one document exists for "IN-0107"

  Scenario: AC10 A type change re-runs extraction for the new type
    Given intake item "IN-0108" was classified "DEMAND_LETTER" with five extracted fields
    When the officer sets the type to "GUARANTOR_NOTICE"
    Then extraction runs for "GUARANTOR_NOTICE" and the item shows its four fields, each in state "REVIEW"
    Then the DEMAND_LETTER fields are no longer offered

  Scenario: AC11 The file is already on the chosen case
    Given document "DOC-0109" on case "RW-2026-000203" holds a file with hash "H109"
    Given intake item "IN-0109" holds the same file
    When the officer attaches "IN-0109" to "RW-2026-000203"
    Then the system stores no second document and "IN-0109" is linked to "DOC-0109"
    Then the screen shows MSG-P5-024 naming "DOC-0109"

  Scenario: AC12 Discard an unreadable item
    Given intake item "IN-0110" with review_reason "UNREADABLE_FILE"
    When the officer chooses Discard with reason "Blank page from the branch scanner"
    Then "IN-0110" has review_outcome "DISCARDED" with the reason, the officer's user ID and the time
    Then it leaves the queue and no document is stored

  Scenario: AC13 Discard without a reason is refused
    Given intake item "IN-0112" with review_reason "RESCAN"
    When the officer chooses Discard with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "IN-0112" stays in the queue

  Scenario: AC14 The queue lists items in scope, oldest first
    Given 3 review items for team "LIT-BKK" received on 2 November, 4 November and 3 November
    Given 2 review items of team "HP-NE"
    When the officer opens SCR-31
    Then 3 items show, in the order 2 November, 3 November, 4 November
    Then no item of team "HP-NE" shows

  Scenario: AC15 An empty queue
    Given no review item for team "LIT-BKK"
    When the officer opens SCR-31
    Then the screen shows the empty state "No documents are waiting for review."

  Scenario: AC16 A document outside the officer's scope
    Given document "DOC-0111" belongs to a case of team "HP-NE"
    When the officer calls GET /api/recovery/v1/documents/DOC-0111
    Then the response is 404 with MSG-P4-003

  Scenario: AC17 The same confirmation sent twice
    Given the officer confirmed black_case_no on "DOC-0103"
    When the same PATCH with confirmed true and the same value arrives again
    Then the response is 200 with the saved field
    Then confirmed_by and updated_at are unchanged
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The queue holds intake items with a review_reason and no outcome, and documents with review_status PENDING | RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032; LOV-REVIEW |
| BR2 | An item with no case is shown to the review team named in REVIEW_TEAM_UNATTACHED and to roles with scope All; an item with candidate cases and a document are shown by case scope | Permission matrix scope; CTL-09; REVIEW_TEAM_UNATTACHED (DOC-SVC assumed) |
| BR3 | Attach and complete are allowed only when no field is in REVIEW, the type is in force and the case is open | LOV-REVIEW; DocumentTypeCatalog; DF-CAS-005 |
| BR4 | review_status becomes CONFIRMED when type, case and values are kept, CORRECTED when any changes | LOV-REVIEW |
| BR5 | A corrected value keeps the extracted value in extracted_value and the corrector in confirmed_by | DF-DOC-017; FEAT-DCM-11 |
| BR6 | Attach stores through DocumentStore, which writes the DOCATT decision log entry first and places a legal type in the write-once container | RWB-E1-024; Principle 5; CTL-12 |
| BR7 | Each resolved item is a labeled example for the model evaluations | FEAT-AGT-04; FEAT-DCM-11 |
| BR8 | A change saved against an old version is refused | Optimistic lock column version; MSG-GEN-004 |
| BR9 | A discarded item keeps its file in the intake container and records the reason and the person | REQ-DCM-019 (never removed silently) |
| BR10 | Field values are masked unless the role may see them | DF-DOC-015; CTL-11; DL26 |

## 9. State transitions

None. This story does not change a case status. It sets document_intake.review_outcome (ATTACHED or DISCARDED), document.review_status (PENDING to CONFIRMED or CORRECTED) and document_field.state (REVIEW to CONFIRMED or CORRECTED).

| From | Event | Condition | To |
|---|---|---|---|
| Intake item with review_reason | Attach | BR3 passes; store succeeds | review_outcome ATTACHED |
| Intake item with review_reason | Discard | Reason given | review_outcome DISCARDED |
| document.review_status PENDING | Review completed | Nothing changed | CONFIRMED |
| document.review_status PENDING | Review completed | A value changed | CORRECTED |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Lists, reads, corrects, attaches and discards review items in scope (Documents CRU) |
| RW-CASEOWN, case owner | Lists, reads, corrects and attaches review items of own cases (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the queue for the team (Documents R); cannot correct or attach |
| SY-OCR, OCR and extraction pipeline | Re-runs extraction on a type change (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-COE, center of excellence analyst | Reads the labeled examples through the model evaluations (Documents R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read, through CaseDirectory |
| DF-CAS-005 | recovery_case | status | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write, through DocumentStore |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-015 | document_field | field_value | Write |
| DF-DOC-017 | document_field | confirmed_by | Write |
| DF-DOC-034 | document_field | extracted_value | Read |
| Standard column | document_field | state, version | Write |
| DF-DOC-080 | document_intake | review_reason | Read (columns from RWB-E1-032, RWB-E1-050, RWB-E1-053) |
| DF-DOC-070 | document_intake | predicted_type | Read (columns from RWB-E1-032, RWB-E1-050, RWB-E1-053) |
| DF-DOC-072 | document_intake | type_candidates | Read (columns from RWB-E1-032, RWB-E1-050, RWB-E1-053) |
| DF-DOC-076 | document_intake | candidate_case_ids | Read (columns from RWB-E1-032, RWB-E1-050, RWB-E1-053) |
| DF-DOC-077 | document_intake | extracted_fields | Read (columns from RWB-E1-032, RWB-E1-050, RWB-E1-053) |
| DF-DOC-081 | document_intake | review_outcome | Write |
| DF-DOC-082 | document_intake | resolved_by | Write |
| DF-DOC-083 | document_intake | resolved_at | Write |
| DF-DOC-084 | document_intake | discard_reason | Write |
| DF-DOC-089 | document_text | text_content | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DocumentStore and DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /review-items** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | Query kind (INTAKE, DOCUMENT or ALL; default ALL), reason, page, size (default REVIEW_PAGE_SIZE) |
| Response | ReviewItemPage: items of kind, intakeId or documentId, caseNo, reason, predictedType, candidates, confidence, receivedAt, version |
| Errors | 401 (MSG-P4-001); 403 no Documents R (MSG-P4-002); 422 unknown kind or reason (MSG-GEN-002); 503 (MSG-GEN-006) |
| Authorization | Documents, right R, scope applied (BR2) |
| Idempotency | Not applicable |

**GET /intake-items/{intakeItemId}** and **GET /intake-items/{intakeItemId}/content** (new)

| Item | Value |
|---|---|
| Response | IntakeItem: id, source, receivedAt, reviewReason, predictedType, candidates, candidateCases (caseNo, status), pages (page number, text), fields (masked by role), version; content returns the file |
| Errors | 401; 403 (MSG-P4-002); 404 not found or not in the review scope (MSG-P4-003); 503 (MSG-GEN-006) |
| Authorization | Documents, right R |

**POST /intake-items/{intakeItemId}/resolve** (new)

| Item | Value |
|---|---|
| Request | ResolveRequest: action (SET_TYPE, ATTACH or DISCARD), documentType, caseNo, fields (fieldName, value, confirmed), discardReason, version; header Idempotency-Key |
| Response | IntakeItem for SET_TYPE and DISCARD; Document for ATTACH |
| Errors | 401; 403 no Documents U (MSG-P4-002); 404 (MSG-P4-003); 409 stale version or item already resolved (MSG-GEN-004); 422 type not in force (MSG-P5-006), case closed (MSG-P5-005), field in review or empty value or empty reason (MSG-GEN-001), date out of range (MSG-GEN-002); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header; a repeat returns the first result |

**PATCH /api/recovery/v1/documents/{documentId}/fields/{fieldId}**

| Item | Value |
|---|---|
| Request | FieldReview: value (required when confirmed is false), confirmed; header If-Match with the document version |
| Response | DocumentField |
| Errors | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 409 stale version (MSG-GEN-004); 422 empty value (MSG-GEN-001) or out of range (MSG-GEN-002); 503 (MSG-GEN-006) |
| Authorization | Documents, right U, scope applied |
| Idempotency | A repeat with the same value and flag returns the saved field without change |

**POST /documents/{documentId}/review** (new): request DocumentReviewRequest action COMPLETE and version; response Document; 409 (MSG-GEN-004); 422 field still in review (MSG-GEN-001); Documents, right U. RWB-E2-017 uses the same action for generated drafts.

**Published interfaces**

```java
// P5, used by RWB-E1-060 (P10)
package recovery.dochub.review;
public interface LabeledSetReader {
    List<LabeledExample> resolvedSince(Instant since, int limit);
    // LabeledExample: intakeId or documentId, predictedType, confirmedType, fields (fieldName, extractedValue, confirmedValue, confidence, extractorVersion)
}
// Called: P3 CaseDirectory.findByCaseNo(caseNo); P5 DocumentStore.store(StoreRequest); P5 FieldExtraction.extractIntake(intakeId)
```

## 13. Solution plan

**Package.** folder `recovery/dochub/review`, Java package `recovery.dochub.review`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReviewQueueController | Controller | GET /review-queue, GET /document-intake/{intakeId}, content, POST resolve, POST /documents/{documentId}/review |
| DocumentHubController | Controller | PATCH /documents/{documentId}/fields/{fieldId} |
| ReviewQueueService | Service | Builds the queue with the scope rule BR2 |
| ReviewResolutionService | Service | SET_TYPE, ATTACH and DISCARD for intake items; field confirm and correct; complete for documents (BR3 to BR9) |
| LabeledSetReader | Published interface | Resolved items as labeled examples |
| DocumentIntakeRepository | Repository | From RWB-E1-049; adds the outcome columns |
| ReviewQueuePage | React component | SCR-31 list, paging and empty state |
| ReviewItemPanel | React component | File and OCR text viewer, type chooser with candidates, case chooser, fields with Confirm and Correct, Attach and Discard |

**Database**

- Flyway migration `V1_5_054__review_outcome.sql` adds to document_intake: review_outcome varchar(12), resolved_by uuid, resolved_at timestamptz, discard_reason varchar(400).
- Index `ix_intake_review ON document_intake (received_at) WHERE review_reason IS NOT NULL AND review_outcome IS NULL`; index `ix_document_review ON document (review_status, created_at) WHERE review_status = 'PENDING'`.

**Configuration and reference data**

- document_hub_parameter rows REVIEW_TEAM_UNATTACHED, REVIEW_DATE_MIN, REVIEW_DATE_MAX, REVIEW_PAGE_SIZE (values assumed; DL11), loaded by the reference data administrator.
- DOCTYPE version in force through DocumentTypeCatalog (RWB-E1-025; DL19).

**Build steps**

1. Write the migration and the indexes; repository tests.
2. Build ReviewQueueService with the scope rule and ordering; test AC14 and AC15.
3. Build the intake item read and content endpoints with masking; test AC16 and the access test.
4. Build SET_TYPE with the call to FieldExtraction; test AC5 and AC10.
5. Build field confirm and correct with validation and the If-Match check; test AC3, AC4, AC6, AC9 and AC17.
6. Build ATTACH through DocumentStore.store with BR3, the duplicate link and the outcome; test AC2, AC7, AC8, AC11 and the decision log failure.
7. Build DISCARD; test AC12 and AC13. Build LabeledSetReader.
8. Build ReviewQueuePage and ReviewItemPanel on SCR-31 with the Loading, list, reviewed and empty states; browser tests (RWB-TE-010).

**Feature flag:** `rwb.dochub.review`. Off: SCR-31 is hidden and review items stay in the queue untouched.

**Done when:** the tests in section 16 pass and SCR-31 passes the browser and accessibility tests of RWB-TE-010.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | An item or document is in the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P5-005 | The chosen case is closed (new) | Case {case} is closed. Choose an open case. |
| MSG-P5-006 | The chosen type is not in force (new) | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-024 | The file is already on the case | This file is already on the case as {document}. |
| MSG-GEN-001 | Empty value, empty reason, or field still in review | Enter {field}. |
| MSG-GEN-002 | Date outside the allowed range | {field} must be between {min} and {max}. |
| MSG-GEN-004 | Saved against an old version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Field, attach or discard saved | Saved. |
| MSG-P7-003 | Decision log write failed on attach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Caller lacks Documents U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Item or document outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the queue loads |
| SCR-31 Document review queue | List | Sees review items oldest first with reason, candidates, confidence and age; opens one; sets type and case, confirms or corrects fields, attaches or discards |
| SCR-31 Document review queue | Reviewed | After attach, discard or complete the item leaves the list and MSG-GEN-005 shows |
| SCR-31 Document review queue | Empty (common state) | Sees "No documents are waiting for review." |
| SCR-30 Case documents | List | Sees the attached document with its confirmed type and fields |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-01 | AC1, BR1 | System | Intake item classified at 0.62 with two candidates |
| TC-E1-054-02 | AC2, BR4, BR5, BR6, BR7 | System | Hearing date corrected; synthetic case RW-2026-000201 |
| TC-E1-054-03 | AC3, BR4 | System | Stored document with one field in review |
| TC-E1-054-04 | AC4 | System | Empty correction |
| TC-E1-054-05 | AC5, BR3 | System | Type PAYSLIP not in force |
| TC-E1-054-06 | AC6 | System | Date 2569-12-16 entered as a Gregorian year |
| TC-E1-054-07 | AC7, BR3 | System | Two fields in review, one confirmed |
| TC-E1-054-08 | AC8, BR3 | System | Candidate case with status Closed |
| TC-E1-054-09 | AC9, BR8 | System | Two sessions on one item version |
| TC-E1-054-10 | AC10 | System | Demand letter changed to guarantor notice |
| TC-E1-054-11 | AC11 | System | Same file hash already on the case |
| TC-E1-054-12 | AC12, BR9 | System | Unreadable item discarded with a reason |
| TC-E1-054-13 | AC13 | System | Discard with an empty reason |
| TC-E1-054-14 | AC14, BR2 | System | Five review items across two teams |
| TC-E1-054-15 | AC15 | System | No review item for team LIT-BKK |
| TC-E1-054-16 | AC16, BR10 | System | Document of team HP-NE |
| TC-E1-054-17 | AC17 | System | Same PATCH sent twice |
| TC-E1-054-18 | Access | Access | RW-TEAMMGR user (Documents R) calls POST /document-intake/{intakeId}/resolve; refused with MSG-P4-002 |
| TC-E1-054-19 | Principle 5 | Resilience | Decision log write forced to fail on Attach; no document, item unchanged, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the review team, date limits, page size and the type list come from document_hub_parameter and the type table.
- No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; the labeled examples stay inside the bank.
- No read of another module's tables: cases come through CaseDirectory; scope comes from the ACE common access check.
- Attach goes only through DocumentStore, so a document never exists without its decision log entry.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01 to TC-E1-054-19 |

## 19. Out of scope

- Setting the review reasons: OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching (RWB-E1-032).
- The model evaluations that read the labeled examples (RWB-E1-060).
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040).
