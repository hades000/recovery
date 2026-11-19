# Technical Specification — RWB-E1-053 Field extraction for the six types into the index

| Field | Value |
|---|---|
| Story | RWB-E1-053 — Field extraction for the six types into the index |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-063-epic-1-RWB-E1-053` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-006, REQ-DCM-001); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 053 Field extraction for the six types into the index v1.md`; FSD P5 A2.9; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-001, REQ-DCM-006; FEAT-DCM-09; US-RWB-E1-053; D7.2; DL11, DL19, DL33; CTL-08, CTL-11, CTL-12; R-UNI-32, R-UNI-38, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-30 Case documents adds the confidence per field, the REVIEW mark and the MSG-P5-003 state. No new route or screen. |
| Logic In Scope | `YES` — selection, extraction, normalization, threshold and review-only rules, persistence, evaluation and idempotency. |
| API In Scope | `NO` — no new or changed contract. Reuses `GET /api/recovery/v1/documents/{documentId}` (API-P5-003). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-12 Document intake (new `extractStep`); `DocumentIntakeRepository` (extraction columns); `DocumentFieldRepository`; SCR-30 Case documents. |
| New Nodes Required | `YES` — `ExtractStep`, `FieldExtraction`, `FieldExtractionService`, `FieldExtractor`, `TemplateFieldExtractor`, `ModelFieldExtractor`, `ValueNormalizer`, `ExtractionEvaluationRunner`. |
| Inherited Existing Behavior | OCR text per page (RWB-E1-049); classification (RWB-E1-050); document type catalog (RWB-E1-025); document store and `document_field` (RWB-E1-024); JOB-12 (RWB-E1-049); parameters and reference data (RWB-E1-042, RWB-E1-043); decision log (RWB-E1-027). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The fields extracted are those listed for the type in the document type table version in force on the business date. | SPEC-RWB-E1-053-002 | DIRECT | `DocumentTypeCatalog` returns `field_definitions` for the version in force; names, types, methods, patterns and `review_only` come from data. | COVERED |
| BR2 | A field at or above the threshold has state OK; below it has state REVIEW. | SPEC-RWB-E1-053-005 | DIRECT | `confidence >= EXTRACT_FIELD_THRESHOLD`; the boundary 0.8000 passes. | COVERED |
| BR3 | A `review_only` field has state REVIEW whatever its confidence. | SPEC-RWB-E1-053-006 | DIRECT | `review_only` short-circuits the threshold check. | COVERED |
| BR4 | A field below the precision or recall pass mark is proposed as review-only; it takes effect only through an approved load. | SPEC-RWB-E1-053-013 | DIRECT | Evaluation report and proposed DOCTYPE load; the version in force is not changed in place. | COVERED |
| BR5 | A value that cannot be converted or fails its pattern has state REVIEW; the conversion case carries confidence 0.0000. | SPEC-RWB-E1-053-004, SPEC-RWB-E1-053-007 | DIRECT | `ValueNormalizer` returns a failure; the raw value is kept. | COVERED |
| BR6 | Dates are stored as ISO dates; a Buddhist Era year is converted by subtracting `BE_YEAR_OFFSET`; amounts are baht with two decimals. | SPEC-RWB-E1-053-004 | DIRECT | Thai and English dates, Thai digits and `numeric(18,2)` amounts; offset is a parameter. | COVERED |
| BR7 | An extractor that does not answer within the timeout is retried to the attempt limit; then the item goes to review with no partial fields. | SPEC-RWB-E1-053-010 | DIRECT | `EXTRACT_TIMEOUT_SECONDS`, `EXTRACT_MAX_ATTEMPTS`; `extract_status FAILED`. | COVERED |
| BR8 | An item already extracted for the table version is not extracted again. | SPEC-RWB-E1-053-011 | DIRECT | `extract_status DONE` or `FAILED` is skipped; idempotency key is item ID and table version. | COVERED |
| BR9 | A personal field value is masked in every response unless the role may see it, and is never logged. | SPEC-RWB-E1-053-014 | DIRECT | `personal` flag from `field_definitions`; logs carry field names and confidence only. | COVERED |
| BR10 | Extraction never changes the stored file, so a write-once document is not altered. | SPEC-RWB-E1-053-009 | DIRECT | Only `document_field` and intake rows are written; no container write. | COVERED |
| AC1 | The four COURT_NOTICE fields are extracted with states, confidence and extractor version; the stored document carries them and `review_status NOT_NEEDED`. | SPEC-RWB-E1-053-001..005, SPEC-RWB-E1-053-008, SPEC-RWB-E1-053-009 | DIRECT | Extraction after classification; fields written to the intake item then to the document on store. | COVERED |
| AC2 | The evaluation report lists precision and recall per field; `TITLE_DEED.area_sq_wa` at 0.84 is proposed review-only; the version in force is unchanged. | SPEC-RWB-E1-053-013 | DIRECT | `ExtractionEvaluationRunner` writes the report and a proposed load file. | COVERED |
| AC3 | A field below the threshold is REVIEW, the stored document is PENDING and SCR-30 shows MSG-P5-003. | SPEC-RWB-E1-053-005, SPEC-RWB-E1-053-009 | DIRECT | One REVIEW field sets the document review status. | COVERED |
| AC4 | A review-only field is REVIEW at confidence 0.9900. | SPEC-RWB-E1-053-006 | DIRECT | Rule applies before the threshold. | COVERED |
| AC5 | A confidence equal to the threshold passes as OK. | SPEC-RWB-E1-053-005 | DIRECT | Greater-than-or-equal comparison. | COVERED |
| AC6 | An unconvertible date keeps the raw value, confidence 0.0000 and state REVIEW. | SPEC-RWB-E1-053-007 | DIRECT | Normalizer failure path; raw value preserved. | COVERED |
| AC7 | `case_no` and `account_no` are passed to `matchStep`; `account_no` is personal and is not logged. | SPEC-RWB-E1-053-014 | DIRECT | Extraction output feeds the matcher; personal fields are excluded from logs and job records. | COVERED |
| AC8 | A timeout on every attempt sets FAILED and `EXTRACTION_FAILED`, with no fields, and the item is not attached. | SPEC-RWB-E1-053-010 | DIRECT | No partial fields; `matchStep` skips the item. | COVERED |
| AC9 | A repeated run does not read an item already DONE. | SPEC-RWB-E1-053-011 | DIRECT | Status filter and idempotency key. | COVERED |
| AC10 | Two workers on one item produce one set of fields. | SPEC-RWB-E1-053-011 | DIRECT | `SELECT ... FOR UPDATE SKIP LOCKED`. | COVERED |
| AC11 | A new document version writes new active rows, leaves the old rows inactive and readable, and emits one event. | SPEC-RWB-E1-053-012 | DIRECT | Supersession by `document_id` and `doc_version`. | COVERED |
| AC12 | An English appraisal report yields `AP-2026-0457`, `2026-10-03` and `4250000.00`. | SPEC-RWB-E1-053-004 | DIRECT | English date and amount formats. | COVERED |
| AC13 | A document outside the caller's scope returns 404 with MSG-P4-003 and no field value. | SPEC-RWB-E1-053-015 | DIRECT | Scope filter before any field read. | COVERED |
| X1, X2 | Low confidence or a review-only field. | SPEC-RWB-E1-053-005, SPEC-RWB-E1-053-006 | DIRECT | REVIEW state; document PENDING when stored. | COVERED |
| X3 | A value cannot be converted to its data type. | SPEC-RWB-E1-053-007 | DIRECT | Raw value, 0.0000, REVIEW. | COVERED |
| X4 | The extractor does not answer within the timeout on every attempt. | SPEC-RWB-E1-053-010 | DIRECT | FAILED, `EXTRACTION_FAILED`, no fields. | COVERED |
| X5, X6 | A repeated run or two workers on the same item. | SPEC-RWB-E1-053-011 | DIRECT | Skip; row lock. | COVERED |
| X7 | A new version of an uploaded document is added. | SPEC-RWB-E1-053-012 | DIRECT | New active rows; old rows inactive. | COVERED |
| X8, X9 | A read outside scope, or a caller without Documents R. | SPEC-RWB-E1-053-015 | DIRECT | 404 MSG-P4-003; 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner**, I want **the key fields of each of the six document types extracted and written to the document index with a confidence per field**, so that **documents are searchable by their content**. The story is a backend extraction step on JOB-12 with a narrow SCR-30 presentation: the case owner sees each field, its confidence and a REVIEW mark, and a PENDING document points to SCR-31. It ends the manual re-keying of court dates, case numbers and appraisal values and feeds the matcher (RWB-E1-032) and the review queue (RWB-E1-054).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake: `extractStep` after `classifyStep` and before `matchStep`. |
| Schedule | Every 15 minutes in business hours, as set by RWB-E1-049. |
| Preconditions | RWB-E1-049, RWB-E1-050, RWB-E1-025 and RWB-E1-024 done; DOCTYPE-2026.11 in force with the six types and 26 fields; `EXTRACT_FIELD_THRESHOLD`, `EXTRACT_PRECISION_PASS`, `EXTRACT_RECALL_PASS`, `EXTRACT_MAX_ATTEMPTS`, `EXTRACT_TIMEOUT_SECONDS` and `BE_YEAR_OFFSET` loaded; 180-document labeled sample available; run as SY-OCR. |
| Input | Intake items with `ocr_status DONE` and `extract_status PENDING` that are classified with no `review_reason`, or that carry a document ID with a given type (uploads); field definitions in force; OCR page text. |
| Output | `document_intake.extracted_fields` and `extract_status`; `document_field` rows for attached documents; `document.review_status PENDING` when a field is in REVIEW; `DocumentFieldsExtracted` (EV-17); job counts. |
| Feature flag | `rwb.dochub.extract`. Off: `extractStep` sets `extract_status DONE` with no fields and items continue to `matchStep` with the OCR text only. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `extracted_fields` | Empty | System writes the field set as JSON | Field name, value, confidence, state and extractor version per field. |
| `document_intake` | `extract_status` | `PENDING` | System writes `DONE` or `FAILED` | One value at a time. |
| `document_intake` | `extract_attempts` | `0` | System increments | Stops at `EXTRACT_MAX_ATTEMPTS`. |
| `document_field` | `field_value` | Extractor output after normalization | System writes | Must match `field_definitions.data_type`; masked on read by role. |
| `document_field` | `extracted_value` | Raw extractor output | System writes | Kept when a reviewer later corrects the value. |
| `document_field` | `confidence` | Extractor confidence | System writes | `numeric(5,4)`; `0.0000` on a conversion failure. |
| `document_field` | `state` | None | System writes `OK` or `REVIEW` | Standard column; no other value in this story. |
| `document_field` | `extractor_version` | Extractor version | System writes | Recorded per field. |
| `document_field` | `is_active` | `true` | System writes `false` on supersession | One active row per document and field name. |
| `document` | `review_status` | `NOT_NEEDED` | System writes `PENDING` when any field is REVIEW | LOV-REVIEW. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `document_intake.extract_status PENDING` | `extractStep` completes | Fields written, with or without REVIEW | `DONE` | Item continues to `matchStep`; fields available. |
| `document_intake.extract_status PENDING` | Extractor timeout on every attempt | Attempt limit reached | `FAILED` | `review_reason EXTRACTION_FAILED`; no fields; item held. |
| `document.review_status NOT_NEEDED` | Attached document extracted | At least one field is REVIEW | `PENDING` | SCR-30 mark; MSG-P5-003; SCR-31 link. |
| `document_field.state` (new row) | Field extracted | Confidence at or above threshold and not review-only | `OK` | Active row. |
| `document_field.state` (new row) | Field extracted | Below threshold, review-only, conversion or pattern failure | `REVIEW` | Active row; document PENDING. |
| `document_field.is_active true` | New document version extracted | New active row for the same field name | `false` | Old row stays readable; new row active. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Field confidence below `EXTRACT_FIELD_THRESHOLD` | State REVIEW; document `review_status PENDING` when stored | MSG-P5-003 |
| X2 | Field is `review_only` in the type table | State REVIEW whatever the confidence | MSG-P5-003 |
| X3 | Value cannot be converted to its data type | Raw value kept; confidence 0.0000; state REVIEW | MSG-P5-003 |
| X4 | Extractor does not answer within the timeout on every attempt | `extract_status FAILED`; `review_reason EXTRACTION_FAILED`; no fields; not attached | MSG-P5-003 |
| X5 | Job runs again over extracted items | Not extracted again; no second set of fields | None |
| X6 | Two workers start on the same item | Row lock lets one take it; the other skips | None |
| X7 | New version of an uploaded document | New active rows; old rows inactive and readable; one event | None |
| X8 | Document read outside the caller's scope | 404; no field value returned | MSG-P4-003 |
| X9 | Caller without Documents R reads the document | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/documents/{documentId}` (API-P5-003) returns the document with its fields. |
| Contract delta | None. The Document response already carries extracted fields; this story populates them. `DocumentFieldsExtracted` (EV-17) is an internal outbox event, not an API. |
| Backward compatibility | Unchanged. |
| Authorization | Documents R with scope; 403 MSG-P4-002; 404 MSG-P4-003. |
| Error behaviour | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001, REQ-DCM-006; SPEC-RWB-E1-053-005, -009, -014 | SCR-30 adds the confidence, the REVIEW mark and the MSG-P5-003 state; no new route. | Component tests for OK/REVIEW/PENDING display, masking and the SCR-31 link. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001, REQ-DCM-006; SPEC-RWB-E1-053-001..016 | New job step, extraction service, two extractors, normalizer, repositories and evaluation runner. | Positive, negative, boundary and error-path tests for selection, thresholds, review-only, conversion, timeout, idempotency, concurrency, versioning, evaluation and access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ExtractStep` | Job step | Selects items with `SKIP LOCKED`, calls the service, writes counts. |
| `FieldExtraction` | Published interface | `extractIntake(intakeId)` and `fieldsForIntake(intakeId)`; used by `matchStep` and RWB-E1-054. |
| `FieldExtractionService` | Service | Applies BR1 to BR8 for one item in one transaction. |
| `FieldExtractor` | Service interface | Returns a raw value, a confidence and the extractor version per field. |
| `TemplateFieldExtractor` | Service | Layout and anchor-text extraction for `TEMPLATE`. |
| `ModelFieldExtractor` | Service | Calls the model through the P10 gateway for `MODEL`, with masked text as in RWB-E1-050. |
| `ValueNormalizer` | Service | Dates, Buddhist Era years, Thai digits, amounts and pattern checks. |
| `ExtractionEvaluationRunner` | Service | Runs the labeled sample, writes the report and the proposed load file. |
| `DocumentIntakeRepository` | Repository | Reads and writes the intake extraction columns. |
| `DocumentFieldRepository` | Repository | Writes `document_field` rows for attached documents. |

### Package and boundaries

`recovery/dochub/extract`, Java package `recovery.dochub.extract`. The service is published through `FieldExtraction`; other modules do not read `document_intake` or `document_field`. OCR text comes through `OcrOutputReader` (RWB-E1-049); the type catalog through `DocumentTypeCatalog` (RWB-E1-025); the model through the P10 gateway. Extraction never writes to a container.

### Data and migration

- Reads: `document_intake` (`id`, `document_id`, `predicted_type`, `review_reason`, `ocr_status`, `extract_status`, `extract_attempts`), `document_text` (`page_no`, `text_content`, `quality`), `document_type` (`field_definitions`, `table_version`), `document` (`id`, `document_type`, `review_status`, `doc_version`), `document_hub_parameter`.
- Writes: `document_intake` (`extracted_fields`, `extract_status`, `extract_attempts`), `document_field` (all extraction columns, `state`, `is_active`), `outbox`.
- Migration `V1_5_053__extraction.sql` adds `document_intake.extracted_fields jsonb`, `extract_status varchar(12) default 'PENDING'`, `extract_attempts integer default 0`; adds `document_field.extracted_value varchar(1000)` and `extractor_version varchar(40)`.
- Indexes: `ix_intake_extract ON document_intake (extract_status) WHERE ocr_status = 'DONE'`; unique `ux_document_field_active ON document_field (document_id, field_name) WHERE is_active`.
- No business value is hard-coded: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset are reference data or parameters.

### Extraction rules

1. Select items with `ocr_status DONE`, `extract_status PENDING`, classified with no `review_reason`, or carrying a document with a given type; lock each row.
2. Read the field definitions, threshold and attempts for the type from the version in force on the business date.
3. Dispatch on `extraction_method`: `TEMPLATE` uses layout and anchors; `MODEL` uses the P10 gateway with masked text.
4. Normalize each value; check the data type and pattern; set `OK` at or above the threshold, otherwise `REVIEW`; `review_only` always `REVIEW`.
5. For an unattached item, write `extracted_fields` and set `extract_status DONE`; `matchStep` passes the fields to `DocumentStore.store`.
6. For an attached document, write `document_field` rows, set `document.review_status PENDING` when any field is REVIEW, and write EV-17 in the same transaction.

### Transaction, events and idempotency

- One transaction per intake item; the row lock is held for the item only.
- A failure rolls back the item; it stays `PENDING` and the next run retries.
- `DocumentFieldsExtracted` (EV-17) carries `documentId`, field names and confidence; it carries no values.
- An item with `extract_status DONE` or `FAILED` is not read again. A new document version is a new extraction for the new version, not a repeat.
- The attach decision log entry is written by RWB-E1-032/RWB-E1-024, not by extraction.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR | Documents CRU | All intake items |
| RW-CASEOWN | Documents R | Own cases |
| RW-LITOFF | Documents R | Team or all |
| RW-COE | Documents R | Evaluation report |
| RW-REFADM | Reference data CRUD | All |
| Business lead with Legal | Approval of the type and field list (DL19) | All |

Personal fields are masked on read by the P4 masking policy. Logs and the job record carry item IDs, field names, states and confidence only; `account_no`, OCR text and field values are never logged.

### Observability, performance and operations

- Job counts: items read, extracted, fields OK, fields REVIEW, failed, skipped; per document type.
- Metrics: extraction duration, timeout count, review rate per field, evaluation precision and recall.
- Alerts: extraction failure rate above the run book threshold; repeated timeouts; an evaluation below the pass mark.
- Run book: JOB-12 `extractStep` in RWB-E1-056.
- Volume: about 860,000 documents in 2027 (NFR-004); 15-minute cadence; 60-second timeout and 3 attempts per item; template extraction is attempted before the model path.

### Feature flag and rollback

`rwb.dochub.extract`. Off: `extractStep` sets `extract_status DONE` with no fields; items continue to `matchStep` with the OCR text only. Rollback: turn the flag off and redeploy the previous tag; the migration is forward-only and its columns are nullable or defaulted.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-053-01 | AC1, BR1, BR6 | System | Synthetic Thai court notice; case RW-2026-000123 | Four fields with confidence and state OK; `extract_status DONE`; stored document NOT_NEEDED. |
| TC-E1-053-02 | AC2, BR4 | System | 180 labeled synthetic documents | Report lists precision and recall per field; `area_sq_wa` proposed review-only; version unchanged. |
| TC-E1-053-03 | AC3, BR2 | System | `hearing_date` confidence 0.6200 | REVIEW; document PENDING; MSG-P5-003. |
| TC-E1-053-04 | AC4, BR3 | System | TITLE_DEED `area_sq_wa` review-only at 0.9900 | REVIEW. |
| TC-E1-053-05 | AC5, BR2 | System | Confidence exactly 0.8000 | OK. |
| TC-E1-053-06 | AC6, BR5 | System | Hearing date 32 December 2569 | Raw value kept; confidence 0.0000; REVIEW. |
| TC-E1-053-07 | AC7, BR9 | System | Demand letter with case and account numbers | `case_no` and `account_no` present; account number absent from logs and job record. |
| TC-E1-053-08 | AC8, BR7 | System | Extractor stub times out three times | FAILED; EXTRACTION_FAILED; no fields; not attached. |
| TC-E1-053-09 | AC9, BR8 | System | Item already DONE | Not read again; fields unchanged. |
| TC-E1-053-10 | AC10 | System | Two parallel workers on one item | One set of fields; one worker skips. |
| TC-E1-053-11 | AC11 | System | Uploaded document, version 2 | New active rows; old rows inactive; one EV-17. |
| TC-E1-053-12 | AC12, BR6 | System | English appraisal report | `AP-2026-0457`, `2026-10-03`, `4250000.00`. |
| TC-E1-053-13 | AC13, BR9 | System | Case owner team MTG-BKK; document team HP-NE | 404 MSG-P4-003; no field value. |
| TC-E1-053-14 | X9 | Security | RW-REFADM user without Documents R | 403 MSG-P4-002. |

## Guardrails

- No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and `document_hub_parameter`.
- No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; model text is masked as in RWB-E1-050.
- No read of another module's tables: the model is reached through the P10 gateway; the type catalog and OCR output through their published interfaces.
- Extraction never writes to a stored file or a container.

## Out of scope

- The review queue screen and correction of fields (RWB-E1-054).
- Matching the item to its case and storing the document (RWB-E1-032, RWB-E1-024).
- Search by extracted field (RWB-E1-033).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- The choice of extraction approach per type (RWB-E1-060).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-38, R-UNI-40 | TC-E1-053-01..12 |
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | FEAT-DCM-09 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-053-01, TC-E1-053-11, TC-E1-053-13, TC-E1-053-14 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC8; SPEC-010 | TSD `LOV-INTAKE-REVIEW` lists RESCAN, UNREADABLE_FILE, LOW_CONFIDENCE, MODEL_UNAVAILABLE and UNKNOWN_TYPE, but AC8 requires `EXTRACTION_FAILED`. | The review queue must recognise the value. | The story adds `EXTRACTION_FAILED`; extend the LOV with the migration and reference data. The TSD list is stale. | RESOLVED | SPEC-RWB-E1-053-010 |
| CLAR-002 | BR2, BR7; SPEC-005, SPEC-010 | Are the 0.80 threshold, 3 attempts, 60-second timeout and 543 offset approved? | They drive the state and retry behaviour. | They are the assumed values under DL11; load them as parameters and confirm before go-live. | RESOLVED | SPEC-RWB-E1-053-005, SPEC-RWB-E1-053-010 |
| CLAR-003 | AC11; SPEC-012 | Does extraction apply to uploaded documents as well as intake items? | Determines whether a version 2 is extracted. | Yes: flow step 2 includes an item that carries a document with a given type, and AC11 tests version 2. | RESOLVED | SPEC-RWB-E1-053-012 |
| CLAR-004 | API assessment; SPEC-009 | Is a new endpoint needed to read the extracted fields? | Would create a contract delta. | No: API-P5-003 already returns the document with its extracted fields; EV-17 is an internal event. | RESOLVED | SPEC-RWB-E1-053-009 |
| CLAR-005 | AC2; SPEC-013 | Who approves the proposed review-only load, and when does it take effect? | Determines whether the evaluation can change extraction behaviour. | RW-REFADM loads it and the business lead with Legal approves it under DL19; the version in force changes only after the approved load. | RESOLVED | SPEC-RWB-E1-053-013 |
| CLAR-006 | BR5; SPEC-007 | Which values may `document_field.state` hold? | The builder needs the allowed values. | `OK` and `REVIEW` in this story; `CONFIRMED` and `CORRECTED` are added by RWB-E1-054. The column is the standard `state` varchar(40). | RESOLVED | SPEC-RWB-E1-053-007 |
| CLAR-007 | BR1; SPEC-002 | 025 describes `field_definitions` with name, label, type and personal flag; 053 also needs `extraction_method`, `review_only` and `pattern`. | Extraction cannot choose a method or flag a review-only field without the keys. | The 053 precondition states the keys are in the additions file; 025 owns the column and loads them. Add the keys to the DOCTYPE load; no behaviour change. | RESOLVED | SPEC-RWB-E1-053-002 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD, the API specification or the decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend extraction step on JOB-12 with a narrow SCR-30 confidence and review-mark change; no API contract delta.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new extraction capability reusing the existing document read endpoint]
REQUIREMENT_COVERAGE_SUMMARY: All 10 business rules, 13 acceptance criteria and 9 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
