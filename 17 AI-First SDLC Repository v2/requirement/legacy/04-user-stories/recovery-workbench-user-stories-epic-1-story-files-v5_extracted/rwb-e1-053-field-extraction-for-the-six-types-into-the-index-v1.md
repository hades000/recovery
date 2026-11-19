<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 053 Field extraction for the six types into the index v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 053 Field extraction for the six types into the index v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-053 Field extraction for the six types into the index

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-053 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-09 Extract fields from the six document types |
| Requirement IDs | REQ-DCM-006, REQ-DCM-001 |
| BRD section | Business Requirements Epic 1, section 3.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.2 |
| Priority | Must |
| Depends on | RWB-E1-049, RWB-E1-050, RWB-E1-025 |
| Status | Ready for build |

## 1. Story

As a **case owner**, I want **the key fields of each of the six document types extracted and written to the document index with a confidence per field**, so that **documents are searchable by their content**.

## 2. Business rationale

Court dates, case numbers, appraisal values and title numbers are typed by hand from paper today, and a document is found only by the person who filed it. This story reads the agreed fields of each classified intake item and each uploaded document into the index with a confidence score, so the case owner and the litigation officer find a document by its content, the attach step finds the case from the extracted case number, and the low-confidence values go to a person. It meets REQ-DCM-006 and REQ-DCM-001 and feeds the module measure "fields extracted without review", which is to rise each month.

## 3. Preconditions

- RWB-E1-049 (OCR text per page through OcrOutputReader) and RWB-E1-050 (predicted_type and classification on the intake item) are done.
- RWB-E1-025 is done: DOCTYPE-2026.11 is in force with the six types and 26 fields, read through DocumentTypeCatalog. Each entry of field_definitions holds name, data_type, personal, extraction_method (TEMPLATE or MODEL), review_only and an optional pattern (keys recorded in the additions file).
- RWB-E1-024 is done: DocumentStore.store writes the fields passed in StoreRequest as document_field rows.
- Rows in document_hub_parameter: EXTRACT_FIELD_THRESHOLD 0.80; EXTRACT_PRECISION_PASS 0.90; EXTRACT_RECALL_PASS 0.90; EXTRACT_MAX_ATTEMPTS 3; EXTRACT_TIMEOUT_SECONDS 60; BE_YEAR_OFFSET 543. Values assumed until the RWB-E1-060 report (DL11).
- The labeled sample of 180 synthetic documents, 30 per type, holds the true value of every field.
- The step runs as SY-OCR (Documents CRU). Feature flag rwb.dochub.extract is on.

## 4. Flow

1. JOB-12 Document intake: runs extractStep after classifyStep and before matchStep.
2. ExtractStep: selects intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document ID with a given type (uploads), locking each row.
3. ExtractStep: reads the field definitions of the type from the version of DocumentTypeCatalog in force, the threshold and the attempts.
4. ExtractStep: reads the page text and layout through OcrOutputReader.
5. FieldExtractor: the extractor named by extraction_method returns a raw value and a confidence per field, with the extractor version.
6. ValueNormalizer: converts each value to its data type: Thai and English dates to ISO dates, Buddhist Era years less BE_YEAR_OFFSET, Thai digits to Arabic digits, amounts to numeric(18,2) baht.
7. ExtractStep: sets each field to state OK, or REVIEW when the confidence is below the threshold, the value cannot be converted, the value fails its pattern, or the field is review_only.
8. ExtractStep: for an item with no document, writes the fields to document_intake.extracted_fields and sets extract_status DONE; matchStep (RWB-E1-032) passes them to DocumentStore.store, which writes the document_field rows and sets review_status PENDING when a field is in REVIEW.
9. ExtractStep: for an item with a document, writes the document_field rows directly, sets document.review_status PENDING when a field is in REVIEW, and writes DocumentFieldsExtracted (EV-17) to the outbox in the same transaction.
10. Case owner: opens SCR-30 Case documents and sees the fields with their confidence; a document with review_status PENDING shows MSG-P5-003.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field confidence is below the threshold | Field state REVIEW; document review_status PENDING when stored | MSG-P5-003 | AC3, AC5 |
| X2 | The field is review_only in the type table | Field state REVIEW whatever its confidence | MSG-P5-003 | AC4 |
| X3 | A value cannot be converted to its data type | Raw value kept, confidence 0.0000, state REVIEW | MSG-P5-003 | AC6 |
| X4 | The extractor does not answer within the timeout on every attempt | extract_status FAILED; review_reason EXTRACTION_FAILED; no fields; item in the review queue | MSG-P5-003 | AC8 |
| X5 | The job runs again over extracted items | Not extracted again; no second set of fields | None | AC9 |
| X6 | Two workers start on the same item | The row lock lets one worker take it; the other skips it | None | AC10 |
| X7 | A new version of an uploaded document is added | New rows for the new version; old rows inactive and readable | None | AC11 |
| X8 | A user reads a document outside their scope | 404 | MSG-P4-003 | AC13 |
| X9 | A user without Documents R reads the document | 403 | MSG-P4-002 | Access test TC-E1-053-14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds one step to JOB-12 after the OCR and classification steps of Epic 1 |
| Negotiable | Fields, thresholds, methods, patterns and review-only flags are data |
| Valuable | Ends re-keying of court dates, case numbers and appraisal values from paper |
| Estimable | One job step, an extractor interface with two implementations, a normalizer, an evaluation runner |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Field extraction for the six types into the index

  Background:
    Given DOCTYPE-2026.11 is in force
    Given COURT_NOTICE lists court_name (text), black_case_no (text, pattern two to four letters, a space, digits, "/" and four digits), notice_date (date) and hearing_date (date)
    Given EXTRACT_FIELD_THRESHOLD is 0.80

  Scenario: AC1 Fields extracted
    Given intake item "IN-0001" classified "COURT_NOTICE" with confidence 0.9400
    Given its OCR text holds court "Civil Court", black case number "Por 1234/2569", notice date "1 ธันวาคม 2569" and hearing date "15 ธันวาคม 2569"
    When extractStep runs
    Then extracted_fields of "IN-0001" holds court_name "Civil Court" 0.9600, black_case_no "Por 1234/2569" 0.9100, notice_date "2026-12-01" 0.9000 and hearing_date "2026-12-15" 0.8800, each with state "OK" and extractor version "EXT-TPL-1.0"
    Then extract_status is "DONE"
    Then when matchStep stores the document on case "RW-2026-000123" the four fields are in the index and review_status is "NOT_NEEDED"

  Scenario: AC2 Precision and recall
    Given the labeled sample of 180 documents and the pass marks precision 0.90 and recall 0.90 per field
    When the extraction evaluation run processes the sample
    Then the report lists precision and recall for each of the 26 fields with the extractor version
    Then the system lists TITLE_DEED area_sq_wa with precision 0.84 as "review-only"
    Then the run writes a proposed DOCTYPE load file with review_only true for area_sq_wa only
    Then the version in force does not change until the proposed version is loaded and approved

  Scenario: AC3 A field below the threshold goes to review
    Given intake item "IN-0002" classified "COURT_NOTICE"
    Given the extractor returns hearing_date with confidence 0.6200
    When extractStep runs
    Then hearing_date has state "REVIEW" and the other three fields state "OK"
    Then when the document is stored its review_status is "PENDING" and SCR-30 shows MSG-P5-003

  Scenario: AC4 A review-only field always goes to review
    Given TITLE_DEED field area_sq_wa has review_only true
    Given the extractor returns area_sq_wa "940" with confidence 0.9900 on item "IN-0003"
    When extractStep runs
    Then area_sq_wa has state "REVIEW"

  Scenario: AC5 Confidence equal to the threshold passes
    Given the extractor returns black_case_no on item "IN-0004" with confidence 0.8000
    When extractStep runs
    Then black_case_no has state "OK"

  Scenario: AC6 A value that cannot be converted goes to review
    Given the OCR text of item "IN-0005" holds hearing date "32 ธันวาคม 2569"
    When extractStep runs
    Then hearing_date keeps the value "32 ธันวาคม 2569" with confidence 0.0000 and state "REVIEW"

  Scenario: AC7 The extracted case number and account number are given to matchStep
    Given intake item "IN-0006" classified "DEMAND_LETTER" whose text holds case "RW-2026-000123" and an account number
    When extractStep runs
    Then extracted_fields holds case_no "RW-2026-000123" and account_no
    Then the system marks account_no personal and is not written to the job record or the logs

  Scenario: AC8 The extractor does not answer
    Given the extractor does not answer within 60 seconds on 3 attempts for item "IN-0007"
    When extractStep runs
    Then extract_status is "FAILED" and review_reason is "EXTRACTION_FAILED"
    Then extracted_fields is empty
    Then matchStep does not attach "IN-0007"

  Scenario: AC9 A repeated run has no effect
    Given item "IN-0001" has extract_status "DONE"
    When extractStep runs again
    Then the system does not read "IN-0001" again and extracted_fields is unchanged

  Scenario: AC10 Two workers on the same item
    Given two extractStep workers start at the same time
    When both select item "IN-0008"
    Then one worker extracts it and the other skips it
    Then "IN-0008" has one set of fields

  Scenario: AC11 A new version of an uploaded document
    Given uploaded court notice "DOC-0001" has four active document_field rows from version 1
    Given version 2 of "DOC-0001" is added with hearing date "20 มกราคม 2570"
    When extractStep runs on the intake item for version 2
    Then the system writes four new active rows with hearing_date "2027-01-20"
    Then the four version 1 rows have is_active false and stay readable
    Then one DocumentFieldsExtracted event is in the outbox for "DOC-0001"

  Scenario: AC12 An English document is extracted
    Given item "IN-0009" classified "APPRAISAL_REPORT" with English text holding appraisal number "AP-2026-0457", date "3 October 2026" and value "THB 4,250,000"
    When extractStep runs
    Then appraisal_no is "AP-2026-0457", appraisal_date is "2026-10-03" and appraised_value is "4250000.00"

  Scenario: AC13 A document outside the caller's scope
    Given a case owner whose scope is team "MTG-BKK"
    Given document "DOC-0010" belongs to a case in team "HP-NE"
    When the case owner calls GET /api/recovery/v1/documents/DOC-0010
    Then the response is 404 with MSG-P4-003 and no field value is returned
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The fields extracted are those listed for the type in the document type table version in force on the business date | DocumentTypeCatalog (RWB-E1-025); DL19; R-UNI-38 |
| BR2 | A field at or above the threshold has state OK; below it has state REVIEW | EXTRACT_FIELD_THRESHOLD, 0.80 assumed; DL11 |
| BR3 | A review_only field has state REVIEW whatever its confidence | field_definitions.review_only; FEAT-AGT-04 |
| BR4 | A field whose precision or recall on the labeled sample is below the pass mark is proposed as review-only; it takes effect only through an approved load | CTL-08; Principle 1 |
| BR5 | A value that cannot be converted or fails its pattern has state REVIEW with confidence 0.0000 for the conversion case | field_definitions.data_type and pattern |
| BR6 | Dates are stored as ISO dates; a Buddhist Era year is converted by subtracting BE_YEAR_OFFSET; amounts in baht with two decimals | BE_YEAR_OFFSET 543 |
| BR7 | An extractor that does not answer within the timeout is retried up to the attempt limit; then the item goes to review with no partial fields | R-UNI-32; EXTRACT_TIMEOUT_SECONDS, EXTRACT_MAX_ATTEMPTS |
| BR8 | An item already extracted for the table version is not extracted again | R-UNI-40 |
| BR9 | A personal field value is masked in every response unless the role may see it, and never logged | DF-DOC-015; CTL-11; DL26 |
| BR10 | Extraction never changes the stored file, so a write-once document is not altered | CTL-12 |

## 9. State transitions

None. This story does not change a case status. It sets document_intake.extract_status (PENDING to DONE or FAILED), document_field.state (OK or REVIEW) and, for attached documents, document.review_status (NOT_NEEDED to PENDING).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs extractStep; writes extracted fields and document_field rows (Documents CRU) |
| RW-CASEOWN, case owner | Reads the document and its fields in scope (Documents R) |
| RW-LITOFF, litigation officer | Reads the document and its fields in scope (Documents R) |
| RW-COE, center of excellence analyst | Reads the evaluation report; prepares the review-only proposal |
| RW-REFADM, reference data administrator | Loads a new DOCTYPE version (Reference data CRUD) |
| Business lead with Legal | Approves the type and field list (DL19) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-011 | document | doc_version | Read |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-DOC-034 | document_field | extracted_value | Write |
| DF-DOC-035 | document_field | extractor_version | Write |
| Standard column | document_field | state, is_active | Write |
| DF-DOC-070 | document_intake | predicted_type | Read (columns from RWB-E1-049 and RWB-E1-050) |
| DF-DOC-080 | document_intake | review_reason | Read (columns from RWB-E1-049 and RWB-E1-050) |
| DF-DOC-061 | document_intake | document_id | Read (columns from RWB-E1-049 and RWB-E1-050) |
| DF-DOC-063 | document_intake | ocr_status | Read (columns from RWB-E1-049 and RWB-E1-050) |
| DF-DOC-077 | document_intake | extracted_fields | Write |
| DF-DOC-078 | document_intake | extract_status | Write |
| DF-DOC-079 | document_intake | extract_attempts | Write |
| DF-DOC-089 | document_text | text_content | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Job name | JOB-12 Document intake; this story adds extractStep after classifyStep |
| Schedule | Every 15 minutes in business hours |
| Input | Intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document with a given type |
| Output | extracted_fields and extract_status on the item; document_field rows and review_status for attached documents; counts on the job record |
| Events published | DocumentFieldsExtracted (EV-17) for attached documents, payload documentId, field names and confidence; no values |
| Idempotency key | Intake item ID and table version; an item with extract_status DONE or FAILED is not read again |
| Restart | Unfinished items stay PENDING and are taken by the next run |

**Published interface (P5, used by RWB-E1-032 and RWB-E1-054)**

```java
package recovery.dochub.extract;
public interface FieldExtraction {
    ExtractionResult extractIntake(UUID intakeId);                         // used by extractStep and by a type change in review
    List<ExtractedField> fieldsForIntake(UUID intakeId);                    // fieldName, value, extractedValue, confidence, state, extractorVersion, personal
}
```

**Endpoint read:** GET /api/recovery/v1/documents/{documentId}, response Document extended with fields as recorded by RWB-E1-024. Errors 401; 403 no Documents R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 (MSG-GEN-006). Authorization Documents, right R, scope applied.

## 13. Solution plan

**Package.** folder `recovery/dochub/extract`, Java package `recovery.dochub.extract`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractStep | Job | Step of JOB-12: select with SKIP LOCKED, extract, set states, write |
| FieldExtraction | Published interface | Section 12 |
| FieldExtractionService | Service | Applies BR1 to BR8 for one item in one transaction |
| FieldExtractor | Service (interface) | extract(pages, fieldDefinitions, timeout) returns raw value and confidence per field |
| TemplateFieldExtractor | Service | Layout and anchor-text extractor for extraction_method TEMPLATE |
| ModelFieldExtractor | Service | Calls the model through the P10 model gateway (RWB-TE-013) for extraction_method MODEL, with masked text as in RWB-E1-050 |
| ValueNormalizer | Service | Dates, Buddhist Era years, Thai digits, amounts (BR6) and pattern checks (BR5) |
| ExtractionEvaluationRunner | Service | Runs the labeled sample; writes evaluation/extraction/{runDate}.json and the proposed load file |
| DocumentIntakeRepository | Repository | From RWB-E1-049; adds the extraction columns |
| DocumentFieldRepository | Repository | Writes document_field for attached documents |

**Database**

- Flyway migration `V1_5_053__extraction.sql`: adds to document_intake extracted_fields jsonb, extract_status varchar(12) default 'PENDING', extract_attempts integer default 0; adds to document_field extracted_value varchar(1000) and extractor_version varchar(40).
- Index `ix_intake_extract ON document_intake (extract_status) WHERE ocr_status = 'DONE'`; unique index `ux_document_field_active ON document_field (document_id, field_name) WHERE is_active`.
- DocumentStore.store (RWB-E1-024) copies extracted_value, extractor_version and state from the StoreRequest fields into document_field.

**Configuration and reference data**

- DOCTYPE-2026.11 field definitions (RWB-E1-025) with extraction_method, review_only and pattern, loaded by RW-REFADM and approved by the business lead with Legal (DL19).
- document_hub_parameter rows EXTRACT_FIELD_THRESHOLD, EXTRACT_PRECISION_PASS, EXTRACT_RECALL_PASS, EXTRACT_MAX_ATTEMPTS, EXTRACT_TIMEOUT_SECONDS, BE_YEAR_OFFSET (values assumed; DL11).
- Property rwb.dochub.extract.model-route for the gateway route (DL33).

**Build steps**

1. Write the migration and the indexes; repository tests.
2. Build ValueNormalizer with unit tests for Thai and English dates, Buddhist Era years, Thai digits, amounts, patterns and the invalid date of AC6.
3. Build FieldExtractor, TemplateFieldExtractor and ModelFieldExtractor against fixed OCR pages; timeout and attempts on the model path.
4. Build FieldExtractionService and ExtractStep with SKIP LOCKED selection and the skip rules; test AC8 to AC10.
5. Write fields to extracted_fields for unattached items and to document_field for attached items with the outbox event; test AC1, AC3 and AC11.
6. Check with RWB-E1-024 that StoreRequest fields carry state, extracted_value and extractor_version, and that the store sets review_status PENDING when a field is in REVIEW.
7. Build ExtractionEvaluationRunner; run the 180-document sample in SIT and attach the report.

**Feature flag:** `rwb.dochub.extract`. Off: extractStep sets extract_status DONE with no fields, and items continue to matchStep with the OCR text only.

**Done when:** the tests in section 16 pass and the evaluation report for the 180 sample documents is attached to the story.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW or extraction failed | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document store is unavailable on read | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | Loading | Skeleton rows while the documents and fields load |
| SCR-30 Case documents | List | Sees each document with its fields, the confidence of each and a mark on fields in REVIEW; a PENDING document shows MSG-P5-003 and a link to SCR-31 |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-053-01 | AC1, BR1, BR6 | System | Synthetic Thai court notice; case RW-2026-000123 |
| TC-E1-053-02 | AC2, BR4 | System | Labeled sample of 180 synthetic documents |
| TC-E1-053-03 | AC3, BR2 | System | hearing_date at confidence 0.6200 |
| TC-E1-053-04 | AC4, BR3 | System | Title deed with area_sq_wa review-only |
| TC-E1-053-05 | AC5, BR2 | System | Confidence exactly 0.8000 |
| TC-E1-053-06 | AC6, BR5 | System | Invalid date 32 December 2569 |
| TC-E1-053-07 | AC7, BR9 | System | Synthetic demand letter with case and account numbers |
| TC-E1-053-08 | AC8, BR7 | System | Extractor stub timing out three times |
| TC-E1-053-09 | AC9, BR8 | System | Item already DONE |
| TC-E1-053-10 | AC10 | System | Two parallel workers |
| TC-E1-053-11 | AC11 | System | Uploaded document, version 2 |
| TC-E1-053-12 | AC12, BR6 | System | Synthetic English appraisal report |
| TC-E1-053-13 | AC13, BR9 | System | Case owner of team MTG-BKK, document of team HP-NE |
| TC-E1-053-14 | Access | Access | RW-REFADM user (Documents -) calls GET /documents/{documentId}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and document_hub_parameter.
- No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; text sent to the model is masked as in RWB-E1-050.
- No read of another module's tables: the model is reached through the P10 gateway.
- Extraction never writes to a stored file or a container.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-38, R-UNI-40 | TC-E1-053-01 to TC-E1-053-12 |
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-053-01, TC-E1-053-11, TC-E1-053-13, TC-E1-053-14 |

## 19. Out of scope

- The review queue screen and correction of fields (RWB-E1-054).
- Matching the item to its case and storing the document (RWB-E1-032, RWB-E1-024).
- Search by extracted field (RWB-E1-033).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- The choice of extraction approach per type (RWB-E1-060).
