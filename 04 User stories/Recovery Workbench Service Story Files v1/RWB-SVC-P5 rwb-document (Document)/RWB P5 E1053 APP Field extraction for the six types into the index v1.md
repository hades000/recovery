# RWB-P5-E1053-APP Field extraction for the six types into the index

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1053-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-053 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1049-APP, RWB-P5-E1025-APP, RWB-P5-E1050-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P10-TE013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-001, FR-P5-002, FR-P5-013, FR-P5-014, FR-P5-016, FR-P5-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the extraction step of JOB-12 moved into `rwb-document` as the `extract` activity of `DocumentIntakeWorkflow`, on schema `rwb_document`, topic `rwb.document.events.v1`, REST base `/api/recovery/document/v1`, with the model path reached only through the rwb-agent contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the key fields of each of the six document types extracted and written to the document index with a confidence per field**, so that **documents are searchable by their content**.

Inside `rwb-document` this is the field-extraction capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The extraction path is the only writer of the `document_field` rows of an attached document and of the extraction columns of `document_intake`. It reads `document_type` (the field definitions, `extraction_method`, `review_only` and the optional `pattern`), `document_text` (the OCR page text) and `document_hub_parameter` (the six extraction parameters) inside `rwb_document`, and it writes the `rwb.document.DocumentFieldsExtracted.v1` row to the outbox in the same transaction as the field rows (DP-09).
- The field list, the thresholds, the attempts, the timeout and the Buddhist Era offset are data rows: `document_type.field_definitions` in the version in force (RWB-P5-E1025-APP) and `document_hub_parameter` (DL11). No field code, threshold, pass mark, attempt count or offset is written in code (legacy section 17, BR1 to BR6).
- The document type table is P5's own table, read locally in the version in force by `valid_from` and `valid_to`: the field list of a type is never taken from the caller and never through a contract hop (DP-01). The three lists LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW are read through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON).
- The template extractor (`extraction_method` TEMPLATE) is a local component. The model extractor (`extraction_method` MODEL) is reached through the rwb-agent contract RWB-P10-TE013-CON (DP-20, a C dependency, one hop), never through an in-process agent library and never through a model SDK inside this package; the masked-text rule of RWB-P5-E1050-APP applies to the text it sends. The extractor provider, the model name and the model version behind that contract are Not specified in the source documents (GAP-1005; ASM-1797).
- The extraction step is the `extract` activity of `DocumentIntakeWorkflow` on queue `rwb-document` (DP-10), after `classify` and before `match`. The workflow, its 15-minute Schedule and the OCR and classification steps belong to RWB-P5-E1049-APP and RWB-P5-E1050-CON.
- The legacy in-process published interface `FieldExtraction` becomes the REST contracts of 12.1 (DP-11, DP-13): the extract operation, the extract-state read and the fields read. No caller links against a Java interface of this service across a service boundary.
- The document read that AC13 exercises is the `GET /documents/{documentId}` operation of RWB-P5-E1024-APP, reached through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON); this story adds no read of its own for that screen.

The legacy behaviour is carried unchanged in intent and values: the same user story, business rationale, preconditions, flow, exception paths, business rules, messages, authority, data fields, thirteen acceptance criteria and fourteen test cases, adapted to the target service's schema, topic, API base and workflow template.

### 2. Business rationale

Court dates, case numbers, appraisal values and title numbers are typed by hand from paper today, and a document is found only by the person who filed it. This story reads the agreed fields of each classified intake item and each uploaded document into the index with a confidence score, so the case owner and the litigation officer find a document by its content, the attach step finds the case from the extracted case number, and the low-confidence values go to a person. It meets REQ-DCM-006 and REQ-DCM-001 and feeds the module measure "fields extracted without review", which is to rise each month (FSD P5 A2.9.1).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). The four tables the legacy step touched become P5 tables, and no monolith table name survives.
2. The field list, the method, the `review_only` flag and the pattern come from `document_type` in the version in force, read locally (DP-01); the three value lists come from the reference-data contract of `rwb-case` with a fake (DP-07), so no list value is typed in code and no list table is read across a schema boundary.
3. The step is no longer a Quartz job step: it is the `extract` activity of `DocumentIntakeWorkflow` on the service's own task queue (DP-10), started by the 15-minute Schedule that RWB-P5-E1049-APP owns. One row is locked per activity, so two workers never take the same item.
4. The published Java interface `FieldExtraction` becomes one hop of REST with a mock and a fixed answer shape (DP-11): the extract operation, the extract-state read and the fields read of 12.1. The review queue of RWB-P5-E1054-APP calls the same operation with the type set, instead of an in-process method call.
5. The model extractor is the rwb-agent contract and nothing else (DP-20, C RWB-P10-TE013-CON): the package holds no model client, no prompt and no provider key, and the masked text of the classification step is the only text sent.
6. The event `DocumentFieldsExtracted` (EV-17) is written to the outbox in the same transaction as the field rows (DP-09) and published on `rwb.document.events.v1`, with field names and confidence only and no field value.
7. The migration is one step in the per-service Flyway sequence in `rwb_document` (DP-15), so the extraction columns and indexes belong to this schema and to no shared script.
8. The extraction result reaches SCR-30 through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), one call to the owner; the screen never chains a second service call to render a document.

Two target-service statements fix the shape of the work. The extract operation carries no business value of its own: the type, the field list, the thresholds, the attempts and the timeout are read from data at run time, so a new type version changes behaviour with no deployment. And the extraction path never changes a stored file, so the write-once rule of RWB-P5-E1024-APP holds through extraction as it holds through upload (CTL-12).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1043-CON | The reference-data client library, so LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW are read through a published shape (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library; the DocumentFieldsExtracted row is written in the extraction transaction (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 `DocumentIntakeWorkflow` template, the activity registration and the retry policy that hosts the `extract` activity (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the extraction migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the document and field reads to SCR-30 (DP-19) |
| RWB-P5-E1049-APP | The OCR pipeline, the `DocumentIntakeWorkflow` template instantiation, its 15-minute Schedule and the `document_text` page rows this activity reads |
| RWB-P5-E1025-APP | The document type table `document_type` with version DOCTYPE-2026.11 in force: the six types, the 26 fields, `extraction_method`, `review_only` and the optional pattern of each field |
| RWB-P5-E1050-CON | The classification contract that fixes `predicted_type`, `classification_confidence` and `review_reason` on the intake item, with its fake |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the three lists (DP-07) |
| RWB-P10-TE013-CON | The rwb-agent contract: the field-extraction route that answers a raw value and a confidence per field with the extractor version, and its fake (DP-20) |

Business preconditions carried from RWB-E1-053:

- RWB-E1-049 (OCR text per page through OcrOutputReader) and RWB-E1-050 (predicted_type and classification on the intake item) are done: in the target these are RWB-P5-E1049-APP and RWB-P5-E1050-CON, and the OCR text is read from `document_text` inside `rwb_document` instead of through a reader that crosses a module boundary.
- RWB-E1-025 is done: DOCTYPE-2026.11 is in force with the six types and 26 fields, read through DocumentTypeCatalog in the legacy and read from `document_type` in the target. Each entry of `field_definitions` holds name, data_type, personal, extraction_method (TEMPLATE or MODEL), review_only and an optional pattern (keys recorded in the additions file).
- RWB-E1-024 is done: DocumentStore.store writes the fields passed in StoreRequest as document_field rows; in the target this is RWB-P5-E1024-APP, called by the match step of RWB-P5-E1032-APP.
- Rows in document_hub_parameter: EXTRACT_FIELD_THRESHOLD 0.80; EXTRACT_PRECISION_PASS 0.90; EXTRACT_RECALL_PASS 0.90; EXTRACT_MAX_ATTEMPTS 3; EXTRACT_TIMEOUT_SECONDS 60; BE_YEAR_OFFSET 543. Values assumed until the RWB-E1-060 report (DL11). The rows stay in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5.
- The labeled sample of 180 synthetic documents, 30 per type, holds the true value of every field.
- The step runs as SY-OCR (Documents CRU). The feature flag `rwb.document.extract` is on; the legacy flag name `rwb.dochub.extract` is retired with the monolith.

The extractor provider, the model name and the model version behind the rwb-agent route are Not specified in the source documents (GAP-1005; ASM-1797). No TSD P5 T-A.1 row and no other source names a REST operation or a path for running extraction, so the three operations of 12.1 are the baseline's own choice and are Not specified in the source documents (GAP-1006; ASM-1798).

### 4. Flow

1. `DocumentIntakeWorkflow`: starts on the 15-minute Schedule of RWB-P5-E1049-APP and runs `extract` after `classify` and before `match`; the legacy JOB-12 Document intake step order is unchanged.
2. `extract` activity: selects intake items with `ocr_status` DONE and `extract_status` PENDING that are classified with no `review_reason`, or that carry a document ID with a given type (uploads), locking each row with `FOR UPDATE SKIP LOCKED` (DF-DOC-063, DF-DOC-078).
3. `extract` activity: reads the field definitions of the type from `document_type` in the version in force (`valid_from`, `valid_to`), with the threshold, the pass marks, the attempts, the timeout and the Buddhist Era offset from `document_hub_parameter` (RWB-P5-E1025-APP).
4. `extract` activity: reads the page text and the page quality of the item from `document_text` (DF-DOC-085 to DF-DOC-090) in page order; the OCR text is a P5 table row, so no reader of another module is called.
5. `FieldExtractor`: the extractor named by `extraction_method` returns a raw value and a confidence per field, with the extractor version. A TEMPLATE field runs in `th.co.scb.ace.workbench.recovery.document` on the layout and the anchor text of the page; a MODEL field is one hop to the field-extraction route of the rwb-agent contract RWB-P10-TE013-CON (DP-20) with the masked text, a 60-second budget per attempt and at most EXTRACT_MAX_ATTEMPTS attempts.
6. `ValueNormalizer`: converts each value to its data type: Thai and English dates to ISO dates, Buddhist Era years less BE_YEAR_OFFSET, Thai digits to Arabic digits, amounts to numeric(18,2) baht.
7. `extract` activity: sets each field to state OK, or REVIEW when the confidence is below the threshold, the value cannot be converted, the value fails its pattern, or the field is `review_only`.
8. `extract` activity: for an item with no document, writes the field set to `document_intake.extracted_fields` (DF-DOC-077) and sets `extract_status` DONE (DF-DOC-078); the match step of RWB-P5-E1032-APP then passes the field set to `DocumentStore.store` of RWB-P5-E1024-APP, which writes the `document_field` rows and sets `review_status` PENDING when a field is in REVIEW.
9. `extract` activity: for an item with a document, writes the `document_field` rows directly (DF-DOC-012 to DF-DOC-017, DF-DOC-034, DF-DOC-035), sets `document.review_status` PENDING when a field is in REVIEW (DF-DOC-008), and writes the `rwb.document.DocumentFieldsExtracted.v1` row to the outbox (EV-17) in the same transaction.
10. Outbox relay and screen: the relay publishes `rwb.document.DocumentFieldsExtracted.v1` to `rwb.document.events.v1` once per committed extraction; the case owner opens SCR-30 Case documents through the gateway-bff composite route (DP-19) and sees the fields with their confidence, and a document with `review_status` PENDING shows MSG-P5-003.

The field rows, the intake state and the outbox row commit together or not at all, so an item is never marked DONE with no fields and no event is published for a set of fields that does not exist. The extraction reads and writes only `rwb_document` and calls two contracts: the reference-data contract of `rwb-case` (cached list values) and the rwb-agent contract for a MODEL field.

### 5. Exception paths

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

Two target-service notes:

- X4 is the agent route failing on every attempt: each attempt is one hop to RWB-P10-TE013-CON with the 60-second `EXTRACT_TIMEOUT_SECONDS` budget, retried up to `EXTRACT_MAX_ATTEMPTS` 3, and after the last attempt the activity writes no partial field set. The "review queue" of X4 is read by RWB-P5-E1054-APP through `GET /intake-items/{intakeItemId}/extraction` (12.1), which answers `extractStatus` FAILED and `reviewReason` EXTRACTION_FAILED.
- X8 and X9 stay the shape of the legacy read: the `GET /documents/{documentId}` operation of RWB-P5-E1024-APP answers 404 with MSG-P4-003 and 403 with MSG-P4-002, and this story adds no read of its own for the screen.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds one activity to the workflow of RWB-P5-E1049-APP after the OCR and classification steps of the service |
| Negotiable | Fields, thresholds, methods, patterns and review-only flags are data |
| Valuable | Ends re-keying of court dates, case numbers and appraisal values from paper |
| Estimable | One workflow activity, an extractor interface with two implementations, a normalizer, an evaluation runner |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

### 7. Acceptance criteria

```gherkin
Feature: Field extraction for the six types into the index

  Background:
    Given DOCTYPE-2026.11 is in force
    Given COURT_NOTICE lists court_name (text), black_case_no (text, pattern two to four letters, a space, digits, "/" and four digits), notice_date (date) and hearing_date (date)
    Given EXTRACT_FIELD_THRESHOLD is 0.80
    Given the rwb-case reference-data contract mock returns the lists "LOV-DOC-TYPE", "LOV-EXTRACT-STATUS" and "LOV-INTAKE-REVIEW"
    Given the rwb-agent contract mock answers the field-extraction route within 60 seconds with an extractor version

  Scenario: AC1 Fields extracted (legacy RWB-E1-053 AC1)
    Given intake item "IN-0001" classified "COURT_NOTICE" with confidence 0.9400
    Given its OCR text holds court "Civil Court", black case number "Por 1234/2569", notice date "1 December 2569 BE" and hearing date "15 December 2569 BE"
    When extractStep runs
    Then extracted_fields of "IN-0001" holds court_name "Civil Court" 0.9600, black_case_no "Por 1234/2569" 0.9100, notice_date "2026-12-01" 0.9000 and hearing_date "2026-12-15" 0.8800, each with state "OK" and extractor version "EXT-TPL-1.0"
    Then extract_status is "DONE"
    Then when matchStep stores the document on case "RW-2026-000123" the four fields are in the index and review_status is "NOT_NEEDED"

  Scenario: AC2 Precision and recall (legacy RWB-E1-053 AC2)
    Given the labeled sample of 180 documents and the pass marks precision 0.90 and recall 0.90 per field
    When the extraction evaluation run processes the sample
    Then the report lists precision and recall for each of the 26 fields with the extractor version
    Then the system lists TITLE_DEED area_sq_wa with precision 0.84 as "review-only"
    Then the run writes a proposed DOCTYPE load file with review_only true for area_sq_wa only
    Then the version in force does not change until the proposed version is loaded and approved

  Scenario: AC3 A field below the threshold goes to review (legacy RWB-E1-053 AC3)
    Given intake item "IN-0002" classified "COURT_NOTICE"
    Given the extractor returns hearing_date with confidence 0.6200
    When extractStep runs
    Then hearing_date has state "REVIEW" and the other three fields state "OK"
    Then when the document is stored its review_status is "PENDING" and SCR-30 shows MSG-P5-003

  Scenario: AC4 A review-only field always goes to review (legacy RWB-E1-053 AC4)
    Given TITLE_DEED field area_sq_wa has review_only true
    Given the extractor returns area_sq_wa "940" with confidence 0.9900 on item "IN-0003"
    When extractStep runs
    Then area_sq_wa has state "REVIEW"

  Scenario: AC5 Confidence equal to the threshold passes (legacy RWB-E1-053 AC5)
    Given the extractor returns black_case_no on item "IN-0004" with confidence 0.8000
    When extractStep runs
    Then black_case_no has state "OK"

  Scenario: AC6 A value that cannot be converted goes to review (legacy RWB-E1-053 AC6)
    Given the OCR text of item "IN-0005" holds hearing date "32 December 2569 BE"
    When extractStep runs
    Then hearing_date keeps the value "32 December 2569 BE" with confidence 0.0000 and state "REVIEW"

  Scenario: AC7 The extracted case number and account number are given to matchStep (legacy RWB-E1-053 AC7)
    Given intake item "IN-0006" classified "DEMAND_LETTER" whose text holds case "RW-2026-000123" and an account number
    When extractStep runs
    Then extracted_fields holds case_no "RW-2026-000123" and account_no
    Then the system marks account_no personal and is not written to the job record or the logs

  Scenario: AC8 The extractor does not answer (legacy RWB-E1-053 AC8)
    Given the extractor does not answer within 60 seconds on 3 attempts for item "IN-0007"
    When extractStep runs
    Then extract_status is "FAILED" and review_reason is "EXTRACTION_FAILED"
    Then extracted_fields is empty
    Then matchStep does not attach "IN-0007"

  Scenario: AC9 A repeated run has no effect (legacy RWB-E1-053 AC9)
    Given item "IN-0001" has extract_status "DONE"
    When extractStep runs again
    Then the system does not read "IN-0001" again and extracted_fields is unchanged

  Scenario: AC10 Two workers on the same item (legacy RWB-E1-053 AC10)
    Given two extractStep workers start at the same time
    When both select item "IN-0008"
    Then one worker extracts it and the other skips it
    Then "IN-0008" has one set of fields

  Scenario: AC11 A new version of an uploaded document (legacy RWB-E1-053 AC11)
    Given uploaded court notice "DOC-0001" has four active document_field rows from version 1
    Given version 2 of "DOC-0001" is added with hearing date "20 January 2570 BE"
    When extractStep runs on the intake item for version 2
    Then the system writes four new active rows with hearing_date "2027-01-20"
    Then the four version 1 rows have is_active false and stay readable
    Then one DocumentFieldsExtracted event is in the outbox for "DOC-0001"

  Scenario: AC12 An English document is extracted (legacy RWB-E1-053 AC12)
    Given item "IN-0009" classified "APPRAISAL_REPORT" with English text holding appraisal number "AP-2026-0457", date "3 October 2026" and value "THB 4,250,000"
    When extractStep runs
    Then appraisal_no is "AP-2026-0457", appraisal_date is "2026-10-03" and appraised_value is "4250000.00"

  Scenario: AC13 A document outside the caller's scope (legacy RWB-E1-053 AC13)
    Given a case owner whose scope is team "MTG-BKK"
    Given document "DOC-0010" belongs to a case in team "HP-NE"
    Given the rwb-case contract mock returns the case of document "DOC-0010" in team "HP-NE"
    When the case owner calls GET /api/recovery/document/v1/documents/DOC-0010
    Then the response is 404 with MSG-P4-003 and no field value is returned
```

Every Given, When and Then line above is the legacy line unchanged, with two mocks added for the cross-service part: the reference-data contract of `rwb-case` and the field-extraction route of the rwb-agent contract in the Background, and the case read of AC13. The legacy step names map to the target as follows: `extractStep` is the `extract` activity of `DocumentIntakeWorkflow`; `matchStep` is the match step of RWB-P5-E1032-APP; the document read of AC13 is the target operation `GET /documents/{documentId}` of 12.1 on the base `/api/recovery/document/v1` (DP-13), and its legacy monolith path is retired with the monolith base; and the legacy published interface `FieldExtraction` is the extract operation and the extract-state read of 12.1.

### 8. Business rules

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

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by reading `document_type.field_definitions` for `doc_type_code` in the version in force (`valid_from`, `valid_to`) on the business date; the type row and the field list are P5's own rows in `rwb_document` and are never taken from the request (DP-01).
- BR2, BR3 and BR5 are executed per field inside one extraction: the threshold comes from the `EXTRACT_FIELD_THRESHOLD` row, the `review_only` flag and the pattern from the field definition, and the data type from the field definition. No threshold, pattern or flag is a constant in the package.
- BR4 is executed by the evaluation runner, which writes `evaluation/extraction/{runDate}.json` and a proposed DOCTYPE load file; the version in force changes only through the approved load of RWB-P5-E1025-APP, never by the runner.
- BR6 is executed by `ValueNormalizer`, with `BE_YEAR_OFFSET` 543 from `document_hub_parameter` and convertibility treated as data quality, not as a defect: an unconvertible value is kept and reviewed (AC6).
- BR7 is executed by the activity retry policy on the agent route: `EXTRACT_MAX_ATTEMPTS` 3 and `EXTRACT_TIMEOUT_SECONDS` 60 per attempt, then `extract_status` FAILED with `review_reason` EXTRACTION_FAILED and no field row (AC8). The value EXTRACTION_FAILED is the legacy value and is not one of the LOV-INTAKE-REVIEW values of TSD P5 T3.2 today, so the list is extended by a data load: this is Not specified in the source documents (GAP-1007; ASM-1799).
- BR8 is executed by the selection rule on `extract_status` PENDING and by the unique partial index on `(document_id, field_name)` where `is_active`; a repeated run selects nothing (AC9).
- BR9 is executed by the `personal` flag of the field definition, by the masking of the read operations of 12.1, and by the log rule: a log line carries the intake item ID, the field name and the confidence, never the value.
- BR10 is executed because the extraction writes table rows only: no blob path, no content reference and no container is written, and the write-once rule of RWB-P5-E1024-APP is untouched.

### 9. State transitions

None. This story does not change a case status. It sets document_intake.extract_status (PENDING to DONE or FAILED), document_field.state (OK or REVIEW) and, for attached documents, document.review_status (NOT_NEEDED to PENDING).

| From | Event | To |
|---|---|---|
| `document_intake.extract_status` = PENDING | the activity extracts every field of the type | DONE |
| `document_intake.extract_status` = PENDING | the agent route fails on every attempt | FAILED, with `review_reason` EXTRACTION_FAILED |
| `document_intake.extract_status` = PENDING | the row is locked by another worker | PENDING, skipped by this worker and taken by the next run |
| `document_field.state` = (no row) | the field is written with a confidence at or above the threshold | OK |
| `document_field.state` = (no row) | below the threshold, `review_only`, unconvertible or failing its pattern | REVIEW |
| `document.review_status` = NOT_NEEDED | a field of that document is written in REVIEW | PENDING |
| `document_field.is_active` = true | a new version of the document is extracted | false, and new active rows are written for the new version |

The transitions out of REVIEW, to CONFIRMED or CORRECTED, belong to RWB-P5-E1054-APP; this story writes the state REVIEW and stops there.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs the `extract` activity; writes extracted fields and document_field rows (Documents CRU) |
| RW-CASEOWN, case owner | Reads the document and its fields in scope (Documents R) |
| RW-LITOFF, litigation officer | Reads the document and its fields in scope (Documents R) |
| RW-COE, center of excellence analyst | Reads the evaluation report; prepares the review-only proposal |
| RW-REFADM, reference data administrator | Loads a new DOCTYPE version (Reference data CRUD) |
| Business lead with Legal | Approves the type and field list (DL19) |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds. This story adds no operation and no guard of its own for it: the refusal shape is 403 with MSG-P4-002 or 404 with MSG-P4-003, as in the legacy endpoints. The database login is one per service (DP-02); its name is not named here and the story refers to "the rwb-document login (DP-02)" and never to a shared login.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read |
| DF-DOC-004 | `document` | document_type | Read |
| DF-DOC-008 | `document` | review_status | Write |
| DF-DOC-011 | `document` | doc_version | Read |
| DF-DOC-012 to DF-DOC-017 | `document_field` | id, document_id, field_name, field_value, confidence, confirmed_by | Write |
| DF-DOC-034 | `document_field` | extracted_value | Write |
| DF-DOC-035 | `document_field` | extractor_version | Write |
| Standard column | `document_field` | state, is_active | Write |
| DF-DOC-070 | `document_intake` | predicted_type | Read (columns from RWB-P5-E1049-APP and RWB-P5-E1050-CON) |
| DF-DOC-080 | `document_intake` | review_reason | Read (columns from RWB-P5-E1049-APP and RWB-P5-E1050-CON) |
| DF-DOC-061 | `document_intake` | document_id | Read (columns from RWB-P5-E1049-APP and RWB-P5-E1050-CON) |
| DF-DOC-063 | `document_intake` | ocr_status | Read (columns from RWB-P5-E1049-APP and RWB-P5-E1050-CON) |
| DF-DOC-077 | `document_intake` | extracted_fields | Write |
| DF-DOC-078 | `document_intake` | extract_status | Write |
| DF-DOC-079 | `document_intake` | extract_attempts | Write |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-REF-224 | `document_type` | field_definitions | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read |
| (outbox) | outbox library table in `rwb_document` | the row for DocumentFieldsExtracted (EV-17) | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No foreign-schema table is read (DP-01). Personal data never enters the event payload, the workflow input or the log: a personal field value is masked in a read and replaced by the field name in a log line (BR9).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/extract` | P5 | Runs one extraction for one intake item: type row, field list, page text, extractor, normalizer, field rows and outbox row. Service identity SY-OCR or a caller with Documents U for the type-change path of RWB-P5-E1054-APP; `Idempotency-Key` required; 60-second budget per attempt and at most 3 attempts |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/extraction` | P5 | The extract-state read: `extractStatus`, `extractAttempts`, `reviewReason`, the type and table version used and the field set. Documents right R with scope applied; a personal value is masked |
| GET | `/api/recovery/document/v1/documents/{documentId}/fields` | P5 | The fields read of an attached document: the active `document_field` rows with field name, data type, value, confidence, state, extractor version and personal flag. Documents right R with scope applied |

The three operations are the target shape of the legacy published interface `FieldExtraction` and of the legacy document read of AC13 (DP-11, DP-13). No TSD P5 T-A.1 row names an extract operation, so the path and the operation set are a baseline choice and are Not specified in the source documents (GAP-1006; ASM-1798). The document read `GET /api/recovery/document/v1/documents/{documentId}` is the operation of RWB-P5-E1024-APP; this story adds the fields read beside it and does not re-declare it.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 | RWB-P3-E1043-CON | LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW; read through the reference-data client library, cached, one hop, 2 s timeout (DP-07) |
| POST | the field-extraction route of the rwb-agent contract | P10 | RWB-P10-TE013-CON | A raw value and a confidence per field with the extractor version for `extraction_method` MODEL; one hop, the masked text only, 60-second budget per attempt (DP-20). The path is Not specified in the source documents (GAP-1005; ASM-1797) |

The document type table, the parameter rows and the OCR text are not consumed operations: `document_type`, `document_hub_parameter` and `document_text` are P5 tables in `rwb_document`, read locally (DP-01). The classification answer (`predicted_type`, `classification_confidence`, `review_reason`) is read from the intake row that RWB-P5-E1050-CON fixes, not through a second REST hop.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` (EV-17) | `rwb.document.events.v1` | P5 | documentId, or the intake item ID for an item with no document yet | documentId, intakeId, documentType, tableVersion, extractorVersion, extractedAt, the field names with their confidence and state |

CloudEvents 1.0 envelope, binary mode; no personal data in the payload: field names, codes, confidences, states and identifiers only, never a field value. The row is written to the outbox in the extraction transaction, so the event exists exactly when the field rows exist; the once-per-extraction and no-duplicate guarantees rest on the outbox relay and the consumer inbox of DP-09. `DocumentFieldsExtracted` is consumed by `rwb-case` for the search index of the case screens.

#### 12.4 Events consumed

None. This story consumes no Kafka event: the workflow starts on the Schedule of RWB-P5-E1049-APP and the classification answer is read from the intake row, not from a topic. The `AgentRunCompleted` event that Architecture v5 lists as an input of the service is consumed by the classification story, not by this one.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | OCR, classify, extract, match; owned by RWB-P5-E1049-APP, which registers the workflow and the Schedule |
| `extract` | Activity | `rwb-document` | Contributed by this story: selects the items, extracts the fields of the type, normalizes, sets the states and writes the field rows and the outbox row |
| `evaluateExtraction` | Activity | `rwb-document` | Contributed by this story: runs the labeled sample of 180 documents and writes the report and the proposed DOCTYPE load file |

#### 12.6 Schedules

None in this story. The 15-minute document-intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP; this story contributes the activity the Schedule-started workflow calls.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_field` | P5 | The extracted field rows of an attached document: value, confidence, state, extractor version |
| `document_intake` | P5 | Read for the selection and the type; written for `extracted_fields`, `extract_status` and `extract_attempts` |
| `document_text` | P5 | Read only: the OCR page text and quality of the item |
| `document_type` | P5 | Read only: the field definitions, `extraction_method`, `review_only` and the pattern in the version in force |
| `document_hub_parameter` | P5 | Read only: the six extraction parameters |
| `document` | P5 | Read for the type and the version; written for `review_status` only |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The DocumentFieldsExtracted row and the `Idempotency-Key` row |

No foreign-schema table is read (DP-01). No ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW |
| rwb-agent field-extraction fake | RWB-P10-TE013-CON | The MODEL path: a value and a confidence per field with the extractor version; a 60-second timeout on every attempt for AC8; a low-confidence answer for AC3 |
| classification fake | RWB-P5-E1050-CON | `predicted_type`, `classification_confidence` and `review_reason` on the intake item |
| Drools kit | not used | No rule package is evaluated in this story |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 2 | The extract operation, the extract-state read and the fields read; the reference-list read of `rwb-case` and the field-extraction route of `rwb-agent` |
| Kafka | Published 1, consumed 0 | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1` |
| Temporal | 1 workflow, 2 activities | `DocumentIntakeWorkflow` (kit template, owned by RWB-P5-E1049-APP) with the `extract` and `evaluateExtraction` activities |
| File | None | Extraction reads `document_text` rows; it touches no blob and no container |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/extract`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractionController | Controller | The three operations of 12.1; maps exceptions to RFC 9457 problem responses with the message ID; access check and scope |
| ExtractActivity | Temporal activity | `extract` on queue `rwb-document`: the selection with `FOR UPDATE SKIP LOCKED`, the per-item call, the states, the writes |
| FieldExtractionService | Service | Applies BR1 to BR8 for one item in one transaction, including the outbox row |
| FieldExtractor | Service (interface) | `extract(pages, fieldDefinitions, timeout)` returns a raw value and a confidence per field with the extractor version |
| TemplateFieldExtractor | Service | Layout and anchor-text extractor for `extraction_method` TEMPLATE, local to this package |
| AgentModelFieldExtractor | Client | Calls the field-extraction route of the rwb-agent contract RWB-P10-TE013-CON for `extraction_method` MODEL, with masked text, no model client and no provider key in the package (DP-20) |
| ValueNormalizer | Service | Dates, Buddhist Era years, Thai digits, amounts (BR6) and pattern checks (BR5) |
| ExtractionEvaluationRunner | Service | Runs the labeled sample; writes `evaluation/extraction/{runDate}.json` and the proposed load file |
| IntakeExtractionRepository | Repository | Reads the intake row and `document_text`; writes the extraction columns of `document_intake` |
| DocumentFieldRepository | Repository | Writes `document_field` for attached documents and marks earlier version rows inactive |
| DocumentTypeParameterReader | Library client | Reads `document_type` in the version in force and the six `document_hub_parameter` rows in `rwb_document` |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V1053_1__document_extraction.sql` adds to `document_intake` `extracted_fields` jsonb, `extract_status` varchar(12) default 'PENDING' and `extract_attempts` integer default 0, and adds to `document_field` `extracted_value` varchar(1000) and `extractor_version` varchar(40).
- Index `ix_intake_extract ON document_intake (extract_status) WHERE ocr_status = 'DONE'`; unique partial index `ux_document_field_active ON document_field (document_id, field_name) WHERE is_active`.
- The store of RWB-P5-E1024-APP copies `extracted_value`, `extractor_version` and `state` from the field set it is given into `document_field`, so the attach path and the extraction path write the same columns.

**Configuration and reference data.**

- DOCTYPE-2026.11 field definitions (RWB-P5-E1025-APP) with `extraction_method`, `review_only` and `pattern`, loaded by RW-REFADM and approved by the business lead with Legal (DL19). The 26 field codes are data: DEMAND_LETTER case_no, account_no, letter_date, amount_demanded, pay_by_date; COURT_NOTICE court_name, black_case_no, notice_date, hearing_date; APPRAISAL_REPORT appraisal_no, appraisal_date, appraised_value, title_doc_no; TITLE_DEED title_doc_no, land_office, owner_name, area_sq_wa; SETTLEMENT_AGREEMENT case_no, agreement_date, settlement_amount, installment_count, borrower_name; GUARANTOR_NOTICE case_no, guarantor_name, notice_date, amount_claimed. `account_no`, `owner_name`, `borrower_name` and `guarantor_name` are personal.
- `document_hub_parameter` rows EXTRACT_FIELD_THRESHOLD, EXTRACT_PRECISION_PASS, EXTRACT_RECALL_PASS, EXTRACT_MAX_ATTEMPTS, EXTRACT_TIMEOUT_SECONDS, BE_YEAR_OFFSET (values assumed; DL11).
- Property `rwb.document.extract.model-route` for the route through the rwb-agent contract (DL33). The provider, the model name and the model version behind the route are Not specified in the source documents (GAP-1005; ASM-1797).
- Feature flag `rwb.document.extract`. Off: the `extract` activity sets `extract_status` DONE with no fields, and items continue to the match step with the OCR text only.

**Build steps**

1. Write the migration and the two indexes; repository tests, including the refusal of a second active row for the same document and field name.
2. Build `ValueNormalizer` with unit tests for Thai and English dates, Buddhist Era years, Thai digits, amounts, patterns and the invalid date of AC6.
3. Build `FieldExtractor`, `TemplateFieldExtractor` and `AgentModelFieldExtractor` against fixed OCR pages; timeout and attempts on the agent route, against the rwb-agent fake of 12.8.
4. Build `FieldExtractionService` and the `extract` activity with the skip-locked selection and the skip rules; test AC8 to AC10.
5. Write the field set to `extracted_fields` for unattached items and to `document_field` for attached items with the outbox row; test AC1, AC3 and AC11.
6. Check with RWB-P5-E1024-APP that the field set handed to the store carries `state`, `extracted_value` and `extractor_version`, and that the store sets `review_status` PENDING when a field is in REVIEW.
7. Build `ExtractionEvaluationRunner`; run the 180-document sample in SIT and attach the report.
8. Build the three operations of 12.1 with the access check and the masking; API tests for AC7, AC9 and AC13 and the access test TC-E1-053-14.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

DP-01 moves the four tables the legacy step touched (`document`, `document_field`, `document_intake`, `document_text`) plus the two reference tables into `rwb_document`, and it removes the cross-module read of the OCR output and the type catalog: `document_text` and `document_type` are read locally in the version in force. DP-07 keeps the three lists in reference data behind the `rwb-case` contract and its library, so no list value is typed in code. DP-09 puts `DocumentFieldsExtracted` in the outbox inside the extraction transaction, which is what makes AC11's "one event for DOC-0001" true. DP-10 replaces the Quartz job step with the `extract` activity of the workflow kit template, which is what makes AC10's single-worker guarantee the row lock of the activity rather than a scheduler lock. DP-11 turns the in-process `FieldExtraction` interface into one hop of REST with a mock and a fixed answer, which is the shape the review queue and the match step build against. DP-13 gives the service its own base and removes the monolith path from the contract. DP-15 puts the extraction columns and indexes in the service's own Flyway sequence. DP-19 puts the field reads behind the gateway-bff composite route, so SCR-30 calls the document service once. DP-20 is the agent client: the extraction helper is reached through the rwb-agent contract (C `RWB-P10-TE013-CON`), never through an in-process agent library, so the package holds no model client, no prompt and no provider key, and a change of provider is a contract and configuration change of `rwb-agent` and not a redeployment of this service with new code.

The 2-second one-hop rule of DP-11 applies to the synchronous reads of this story, the reference lists and the classification answer, and not to the agent route: Architecture v5 gives an agent run a 60-second budget before the rule result is used, and that budget is the legacy `EXTRACT_TIMEOUT_SECONDS` 60. Each attempt is one hop, the retry stops at `EXTRACT_MAX_ATTEMPTS` 3, and a failed attempt writes no partial field set.

**Done when.** The tests in section 16 pass, the evaluation report for the 180 sample documents is attached to the story, and `rwb.document.DocumentFieldsExtracted.v1` is on the topic once per extraction with no field value in the payload.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW or extraction failed | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document store is unavailable on read | {system} is not available. Your request is queued and will be retried. |

The message IDs and the wording are copied unchanged from RWB-E1-053 section 14; Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one: 403 for MSG-P4-002, 404 for MSG-P4-003, and 503 for MSG-GEN-006 with {system} naming the failed dependency, "Document storage" for a document read and "Agent service" for the agent route. MSG-P5-003 is not an error response: it is the review notice carried by a 200 answer whose `reviewStatus` is PENDING and whose field list holds at least one REVIEW row, and it is the text SCR-30 shows under the document.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | Loading | Skeleton rows while the documents and fields load through the gateway-bff composite route (DP-19) |
| SCR-30 Case documents | List | Sees each document with its fields, the confidence of each and a mark on fields in REVIEW; a PENDING document shows MSG-P5-003 and a link to SCR-31 |
| SCR-30 Case documents | Fields of one document | Sees the active field rows with data type, value, confidence, state and extractor version; a personal value is masked unless the role may see it |
| SCR-31 Review queue | Item with a failed extraction | Sees the item with `reviewReason` EXTRACTION_FAILED and no field, and the action to re-run the extraction |

The screen, its list, its search and its upload form are RWB-P5-E1026-APP; SCR-31, the correction of a field and the attach from review are RWB-P5-E1054-APP. This story fixes the fields and the states those screens read and adds no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-053-14 | Access | Component | RW-REFADM user (Documents -) calls GET /documents/{documentId}; refused with MSG-P4-002 |
| TC-E1-053-01 | AC1, BR1, BR6 | End to end | Synthetic Thai court notice; case RW-2026-000123 |
| TC-E1-053-02 | AC2, BR4 | End to end | Labeled sample of 180 synthetic documents |
| TC-E1-053-03 | AC3, BR2 | End to end | hearing_date at confidence 0.6200 |
| TC-E1-053-04 | AC4, BR3 | End to end | Title deed with area_sq_wa review-only |
| TC-E1-053-05 | AC5, BR2 | End to end | Confidence exactly 0.8000 |
| TC-E1-053-06 | AC6, BR5 | End to end | Invalid date 32 December 2569 |
| TC-E1-053-07 | AC7, BR9 | End to end | Synthetic demand letter with case and account numbers |
| TC-E1-053-08 | AC8, BR7 | End to end | Extractor stub timing out three times |
| TC-E1-053-09 | AC9, BR8 | End to end | Item already DONE |
| TC-E1-053-10 | AC10 | End to end | Two parallel workers |
| TC-E1-053-11 | AC11 | End to end | Uploaded document, version 2 |
| TC-E1-053-12 | AC12, BR6 | End to end | Synthetic English appraisal report |
| TC-E1-053-13 | AC13, BR9 | End to end | Case owner of team MTG-BKK, document of team HP-NE |

The legacy level System maps to End to end, Access to Component and Resilience to NFR; no legacy test of this key carries the Resilience level. The wave-1 integration harness copies TC-E1-053-01 as a `-ITG` test for RWB-ITG-W1, where the real reference-data contract and the real rwb-agent route replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and document_hub_parameter.
- No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; text sent to the model is masked as in RWB-P5-E1050-APP.
- No read of another module's tables: the model is reached through the rwb-agent contract RWB-P10-TE013-CON (DP-20, C dependency), never through an in-process agent library, a model SDK, a prompt file or a provider key in this package.
- Extraction never writes to a stored file or a container.
- No foreign-schema read (DP-01): `document_type`, `document_text`, `document_intake`, `document_field`, `document` and `document_hub_parameter` are P5 rows in `rwb_document`; the three lists arrive through the `rwb-case` reference-data contract (DP-07).
- No field value in an event, a workflow input or a log line: `rwb.document.DocumentFieldsExtracted.v1` carries field names, confidences, states and identifiers only.
- The extract operation is idempotent twice over: `Idempotency-Key` on the POST and the selection rule on `extract_status` PENDING with the unique partial index on the active field row.
- The feature flag `rwb.document.extract` removes the capability without a rollback of the schema.
- The read operations of 12.1 mask a personal field value by role and never return a field of a document outside the caller's scope.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-38, R-UNI-40 | TC-E1-053-01 to TC-E1-053-12 |
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-053-01, TC-E1-053-11, TC-E1-053-13, TC-E1-053-14 |

| Legacy reference | Where it is kept |
|---|---|
| Document type table version DOCTYPE-2026.11, the six types and the 26 field codes | Background, sections 3, 8, 11, 13, 16 |
| Event DocumentFieldsExtracted (EV-17) | Sections 4, 12.3, 17 |
| Parameters EXTRACT_FIELD_THRESHOLD 0.80, EXTRACT_PRECISION_PASS 0.90, EXTRACT_RECALL_PASS 0.90, EXTRACT_MAX_ATTEMPTS 3, EXTRACT_TIMEOUT_SECONDS 60, BE_YEAR_OFFSET 543 | Background, sections 3, 4, 8, 13 |
| MSG-P5-003, MSG-P4-002, MSG-P4-003, MSG-GEN-006 | Section 14, exception paths |
| Rules R-UNI-32, R-UNI-38, R-UNI-40, CTL-08, CTL-11, CTL-12, DL11, DL19, DL26, DL33, DL10 | Sections 2, 8, 9, 13, 14, 18 |
| Job step JOB-12 Document intake and the step order after classify and before match | Sections 3, 4, 12.5, 12.6 |
| Legacy key RWB-E1-053, story RWB-P5-E1053-APP, self-tests TC-E1-053-01 to TC-E1-053-14 | Metadata, sections 1, 3, 12, 16 |

### 19. Out of scope

- The review queue screen and correction of fields (RWB-P5-E1054-APP).
- Matching the item to its case and storing the document (RWB-P5-E1032-APP, RWB-P5-E1024-APP).
- Search by extracted field (RWB-P5-E1026-APP).
- Extraction for the stage 2 and 3 document types (RWB-E2-025, Epic 2).
- The choice of extraction approach per type (RWB-E1-060).
- The OCR pipeline, the `DocumentIntakeWorkflow` template instantiation and its Schedule (RWB-P5-E1049-APP).
- The classification model, its contract and its fallback (RWB-P5-E1050-APP, RWB-P5-E1050-CON).
- The document type table load and its Legal and NPA sign-off (RWB-P5-E1025-APP).
- The published contract documents of this service, their fakes and their versioning, and the contract of the key in other services (RWB-P5-E1053-CON).
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
