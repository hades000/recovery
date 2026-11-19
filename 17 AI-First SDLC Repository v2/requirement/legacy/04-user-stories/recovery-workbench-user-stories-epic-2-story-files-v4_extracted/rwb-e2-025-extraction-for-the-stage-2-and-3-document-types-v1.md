<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 025 Extraction for the stage 2 and 3 document types v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 025 Extraction for the stage 2 and 3 document types v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-025 Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-025 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-22 Extend extraction to the stage 2 and 3 document types |
| Requirement IDs | REQ-DCM-006, REQ-DCM-005 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.2 |
| Priority | Must |
| Depends on | RWB-E1-053, RWB-E1-050, RWB-E1-054 |
| Status | Ready for build |

## 1. Story

As a **litigation officer**, I want **field extraction extended to the stage 2 and 3 types: contracts, credit approvals, mortgage documents, court filings, hearing notices and judgments**, so that **the litigation pack and the treatment record fill themselves**.

## 2. Business rationale

The litigation pack and the treatment record need the contract amount, the mortgage registration, the black and red case numbers, the hearing dates and the judgment amount, which officers read from paper and type in today. This story adds five document types to classification and extraction and extends the hearing notice fields, using the Epic 1 extraction and review path, so these values reach the case index with a confidence and a person checks only the uncertain ones. It meets REQ-DCM-006 and REQ-DCM-005 for the stage 2 and 3 types, and prepares the pack assembly of R-LIT-16 and the treatment documents of FEAT-TRT-18.

## 3. Preconditions

- RWB-E1-050 (classifyStep), RWB-E1-053 (extractStep, extractors, normalizer, evaluation runner) and RWB-E1-054 (review queue) are done.
- A document type table version DOCTYPE-2026.12 is prepared through the RWB-E1-025 loader with the five new types, their classify_threshold and their field_definitions (section 13), signed by legal counsel and the Head of NPA (assumed list; DL19). Hearing notices stay under the Epic 1 type COURT_NOTICE.
- A labeled sample of 60 documents, 10 for each of the five new types and 10 court notices, is in the SIT test data store, masked (RWB-TE-004).
- The classifier version that knows the new types is trained on the sample and selected through the agent runtime (P10).
- The pass mark for field accuracy is 0.90 per field on the sample (document_hub_parameter EXTRACT_ACCURACY_PASS, assumed; DL11).
- DL30 names the Workbench squads as the builder of stage 2 and 3 extraction where no bank-wide service exists; this story assumes option A.

## 4. Flow

1. Reference data administrator: loads DOCTYPE-2026.12 with valid from 2026-12-31 after approval.
2. JOB-12 Document intake: an inbound contract, credit approval, mortgage document, court filing, hearing notice or judgment passes scanStep and ocrStep (RWB-E1-041, RWB-E1-049).
3. ClassifyStep (RWB-E1-050): the classifier version for the eleven types returns a type and a confidence; below the classify_threshold of the type the item goes to the review queue with reason LOW_CONFIDENCE.
4. ExtractStep (RWB-E1-053): reads the field definitions of the type from DocumentTypeCatalog for the version in force and calls the extractor named by extraction_method.
5. System: normalizes each value, checks it against the field pattern held in the type table, and writes document_field rows with confidence and state.
6. System: a field below the threshold, failing its pattern or marked review-only gets state REVIEW and the document goes to the review queue.
7. MatchStep (RWB-E1-032): stores the document with its fields through DocumentStore; DocumentFieldsExtracted (EV-17) is written for documents already attached.
8. Litigation officer: sees the fields on SCR-30, and checks the marked ones on SCR-31.
9. S4 and S2 modules: read confirmed field values through DocumentFieldReader to fill the pack and the treatment record (from Epic 3 and Epic 5).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field is below the threshold | Field state REVIEW; document in the review queue with the field marked | MSG-P5-003 | AC3 |
| X2 | A field's accuracy on the sample is below the pass mark | Field proposed as review-only in the next table version | None | AC4 |
| X3 | A value does not match the field pattern | Field state REVIEW | MSG-P5-003 | AC8 |
| X4 | A document arrives before the new table version is in force | Classified against the earlier version; goes to review with reason UNKNOWN_TYPE | MSG-P5-003 | AC6 |
| X5 | A reader asks for fields still in REVIEW | Only fields in state OK, CONFIRMED or CORRECTED are returned | None | AC9 |
| X6 | The document is write-once | Fields are written; the file and write_once are unchanged | None | AC10 |
| X7 | The document is outside the caller's scope | 404 | MSG-P4-003 | AC11 |
| X8 | A role without Documents R reads the document | 403 | MSG-P4-002 | Access test TC-E2-025-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the Epic 1 extraction and review path; adds data, a classifier version and one reader |
| Negotiable | Types, fields, patterns and pass marks are data |
| Valuable | Pack and treatment values reach the case without typing |
| Estimable | One table version, one classifier version, field patterns, one published reader |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with the labeled sample or synthetic documents |

## 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types

  Background:
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the labeled sample holds 60 documents: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE

  Scenario: AC1 Court notice
    Given the 10 scanned court notices of the sample with 30 labeled values of court_name, black_case_no and hearing_date
    When extraction runs
    Then court, case number and hearing date are on the index
    Then at least 27 of the 30 values match the labels, which is 90% field accuracy on the sample

  Scenario: AC2 Contract
    Given a signed contract "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300
    Given its text names two parties, amount "2,400,000.00 บาท" and date "1 พฤศจิกายน 2569"
    When extraction runs
    Then party_names holds the two party names, masked in responses for roles without the right
    Then contract_amount is "2400000.00" and contract_date is "2026-11-01"

  Scenario: AC3 Low confidence
    Given a judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100
    When extraction runs
    Then judgment_amount has state "REVIEW"
    Then the document is in the review queue on SCR-31 with judgment_amount marked
    Then SCR-30 shows MSG-P5-003 on "DOC-0602"

  Scenario: AC4 A field below the pass mark is proposed as review-only
    Given judgment_amount matches the labels on 8 of the 10 sample judgments
    When the extraction evaluation run processes the sample
    Then the report lists judgment_amount at 0.80, below the pass mark 0.90
    Then the proposed table version marks judgment_amount review_only = true
    Then the version in force does not change until it is loaded

  Scenario: AC5 Classification into the new types
    Given the 50 sample documents of the five new types
    When classification runs with the new classifier version
    Then the system gives each document one of the eleven types with a confidence
    Then the report shows the confusion matrix and at least 45 of 50 correct

  Scenario: AC6 A document before the new version is in force
    Given a judgment "DOC-0603" received on 2026-12-26, before the valid-from date of "DOCTYPE-2026.12"
    When it is classified and extracted
    Then the system classifies it against the six types of "DOCTYPE-2026.11"
    Then the classifier returns "JUDGMENT", which is not in that version, so the item goes to the review queue with review_reason "UNKNOWN_TYPE"

  Scenario: AC7 A Thai judgment date in Buddhist Era
    Given a judgment whose text reads "พิพากษา ณ วันที่ 5 มีนาคม 2570"
    When extraction runs
    Then judgment_date is "2027-03-05"

  Scenario: AC8 A value that does not match its pattern
    Given the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits
    Given the extractor reads red_case_no "Por345-2570" with confidence 0.9200
    When extraction runs
    Then red_case_no has state "REVIEW"
    Then a value "Por 345/2570" with confidence 0.9200 has state "OK"

  Scenario: AC9 Readers get only checked or confident values
    Given judgment "DOC-0602" has red_case_no in state "OK" and judgment_amount in state "REVIEW"
    When the litigation module calls DocumentFieldReader for case "RW-2026-000601" and type "JUDGMENT"
    Then the system returns red_case_no
    Then the system does not return judgment_amount until it is confirmed or corrected

  Scenario: AC10 A write-once document is not altered
    Given judgment "DOC-0604" is held write-once with write_once true
    When extraction runs
    Then the system writes four document_field rows
    Then the stored file hash, storage_ref and write_once are unchanged

  Scenario: AC11 A document outside the caller's scope
    Given a litigation officer with scope team "LIT-BKK"
    Given document "DOC-0605" belongs to a case of team "LIT-NE"
    When the officer calls GET /api/recovery/v1/documents/DOC-0605
    Then the response is 404 with MSG-P4-003
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the extraction date | Document types reference table; DL19; R-UNI-38 |
| BR2 | A field below the threshold, failing its pattern, or marked review-only has state REVIEW and sends the document to the review queue | RWB-E1-053 BR2, BR3; REQ-DCM-005 |
| BR3 | A field whose accuracy on the sample is below the pass mark is proposed as review-only; the proposal takes effect only when loaded | EXTRACT_ACCURACY_PASS (0.90 assumed); DL11; CTL-08 |
| BR4 | Each field may carry a pattern in field_definitions; the pattern is data | Principle 1; RWB-E1-053 BR5 |
| BR5 | Readers in other modules receive only fields in state OK, CONFIRMED or CORRECTED | FEAT-DCM-10 |
| BR6 | Extraction never changes the stored file of a write-once document | CTL-12 |
| BR7 | Party names and other personal field values are masked unless the role may see them | DF-DOC-015; CTL-11; DL26 |
| BR8 | Dates read in Buddhist Era are stored as ISO dates | RWB-E1-053 BR6 |

## 9. State transitions

None. This story does not change a case status. It sets document_field.state and document.review_status as in RWB-E1-053.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Classifies and extracts the new types (Documents CRU) |
| RW-LITOFF, litigation officer | Reads and checks the fields in scope (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads and checks contract, credit approval and mortgage fields in scope (Documents CRU) |
| RW-REFADM, reference data administrator | Loads DOCTYPE-2026.12 (Reference data CRUD) |
| Business lead with Legal | Approves the new type and field list (DL19) |
| RW-COE, center of excellence analyst | Reads the evaluation report |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-006 | document | storage_ref | Read |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-DOC-034 | document_field | extracted_value | Write |
| DF-DOC-035 | document_field | extractor_version | Write |
| Standard column | document_field | state, is_active | Write |
| DF-DOC-070 | document_intake | predicted_type | Write (by classifyStep with the new classifier version) |
| DF-DOC-071 | document_intake | classification_confidence | Write (by classifyStep with the new classifier version) |
| DF-DOC-080 | document_intake | review_reason | Write (by classifyStep with the new classifier version) |
| DF-DOC-077 | document_intake | extracted_fields | Write |
| DF-DOC-078 | document_intake | extract_status | Write |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-233 | document_type | classify_threshold | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Published interface (P5) for S4 and S2**

```java
package recovery.dochub.extract;
public interface DocumentFieldReader {
    List<CheckedField> checkedFields(UUID caseId, String documentType);
}
// CheckedField: documentId, docVersion, fieldName, value, state (OK, CONFIRMED, CORRECTED), confidence
```

The caller passes its own service identity; values are returned unmasked only to a module whose purpose needs them (SY-CASEWF, SY-AGENT), and never logged.

**Event published:** DocumentFieldsExtracted (EV-17), as in RWB-E1-053.

**Endpoint read:** GET /api/recovery/v1/documents/{documentId}, as in RWB-E1-053 (Documents R, scope applied; 401, 403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006).

**Idempotency:** document ID, doc_version and table version, as in RWB-E1-053.

## 13. Solution plan

**Package.** folder `recovery/dochub/extract`, Java package `recovery.dochub.extract` (extends RWB-E1-053).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractStep, FieldExtractionService | Job, Service | From RWB-E1-053; no change in code for the new types |
| DocumentFieldReader | Published interface | Checked fields for a case and type (BR5) |
| DocumentFieldReaderImpl | Service | Implements the reader with masking rules |
| ExtractionEvaluationRunner | Job | Adds field accuracy against the pass mark and the confusion matrix for the classifier |
| DocumentFieldRepository | Repository | Query by case, type and state |

**Database**

- No new table or column. Reads and writes document_field as in RWB-E1-053.
- Index `ix_document_type_case ON document (case_id, document_type)` for the reader.

**Configuration and reference data**

- Document type table version DOCTYPE-2026.12 (RWB-E1-025 loader), loaded by RW-REFADM, signed by legal counsel and the Head of NPA (DL19). Assumed new types and fields: CONTRACT (contract_no, party_names, contract_amount, contract_date); CREDIT_APPROVAL (approval_no, approved_amount, approval_date, approval_level); MORTGAGE_DOCUMENT (title_doc_no, mortgage_amount, registration_date, land_office); COURT_FILING (court_name, black_case_no, filing_date, claim_amount); JUDGMENT (court_name, red_case_no, judgment_date, judgment_amount). COURT_NOTICE keeps court_name, black_case_no, notice_date and hearing_date from DOCTYPE-2026.11. Each field has data type, method, review_only and an optional pattern.
- document_hub_parameter row EXTRACT_ACCURACY_PASS 0.90 (assumed; DL11), loaded by the reference data administrator.
- Classifier version for the eleven types, selected through the agent runtime (P10).

**Build steps**

1. Prepare the load file for DOCTYPE-2026.12 with a test case per new row; validate it in SIT.
2. Add the patterns of the new fields to the load file; unit tests for AC8 against ValueNormalizer (RWB-E1-053).
3. Add the new types to the TemplateFieldExtractor and ModelFieldExtractor configuration through the type table only; no code per type.
4. Extend ExtractionEvaluationRunner with field accuracy and the confusion matrix; run it on the 60-document sample.
5. Build DocumentFieldReader with the state filter and masking; contract test from the S4 side.
6. Run the regression set of RWB-E1-053 to show the six Epic 1 types are unchanged.

**Feature flag:** `rwb.dochub.extraction-stage23`. Off: the new types are not offered to classification and DocumentFieldReader returns nothing for them.

**Done when:** the tests in section 16 pass and the evaluation report for the 60-document sample is attached to the story.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document store is unavailable | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | List | Sees the new types with their fields and confidence; MSG-P5-003 on documents with fields in review |
| SCR-31 Document review queue | List; reviewed | Checks and corrects marked fields of the new types (RWB-E1-054) |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-01 | AC1, BR1 | System | 10 masked court notices from the sample |
| TC-E2-025-02 | AC2, BR7, BR8 | System | Synthetic signed contract with two parties |
| TC-E2-025-03 | AC3, BR2 | System | Judgment with amount at confidence 0.71 |
| TC-E2-025-04 | AC4, BR3 | System | 10 sample judgments, 8 amounts correct |
| TC-E2-025-05 | AC5 | System | 50 sample documents of the new types |
| TC-E2-025-06 | AC6, BR1 | System | Judgment received the day before the valid-from date |
| TC-E2-025-07 | AC7, BR8 | System | Judgment dated 5 March 2570 |
| TC-E2-025-08 | AC8, BR4 | System | Red case numbers with and without the pattern |
| TC-E2-025-09 | AC9, BR5 | System | Judgment with one OK and one REVIEW field |
| TC-E2-025-10 | AC10, BR6 | System | Write-once judgment |
| TC-E2-025-11 | AC11 | System | Document of team LIT-NE |
| TC-E2-025-12 | Access | Access | RW-REFADM user (Documents -) calls GET /documents/{documentId}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: types, fields, patterns, thresholds and pass marks are data and parameters; no class per document type.
- No personal data in logs, tests or prompts: party names and amounts never enter a log or an event; the sample is masked.
- No read of another module's tables: S4 and S2 read through DocumentFieldReader; P5 writes nothing to legal_action, hearing or treatment.
- The Epic 1 types keep their results: the RWB-E1-053 tests run unchanged in the regression suite.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, R-LIT-16 | TC-E2-025-01, TC-E2-025-02, TC-E2-025-04 to TC-E2-025-12 |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38 | TC-E2-025-03, TC-E2-025-05, TC-E2-025-06, TC-E2-025-09 |

## 19. Out of scope

- Writing extracted values into legal_action, hearing or treatment (S4 in Epic 5, S2 in Epic 3).
- Litigation pack assembly and the defect list check (FEAT-LIT-04, FEAT-LIT-05, Epic 5).
- Generation of contract, credit approval and mortgage documents (RWB-E2-026).
- Electronic discovery and court evidence attributes (REQ-DCM-017, REQ-DCM-018).
