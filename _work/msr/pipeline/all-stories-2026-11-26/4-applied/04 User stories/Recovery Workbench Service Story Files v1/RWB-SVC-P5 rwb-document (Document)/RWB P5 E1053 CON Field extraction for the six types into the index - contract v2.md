# RWB-P5-E1053-CON Field extraction for the six types into the index

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1053-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-001, FR-P5-002, FR-P5-013, FR-P5-014, FR-P5-016, FR-P5-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the field-extraction API of `rwb-document` is split out of legacy RWB-E1-053 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the rwb-agent contract it consumes, its fakes and its drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1053-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the field-extraction API of `rwb-document` — the extract operation, the extract-state read and the fields read on base `/api/recovery/document/v1`, the `ExtractionRequest`, `ExtractedField` and `FieldSet` shapes, the field code set of each of the six document types, the confidence and confirmed rules, the error envelope with every message ID and its status, the `Idempotency-Key` rule, the `rwb.document.DocumentFieldsExtracted.v1` schema with no personal value, and the rwb-agent contract it consumes with its fake —**, so that **the app story of this legacy key, the review queue, the match and store path, the search of `rwb-case` and the wave 1 integration harness build against a fixed, testable contract on Day 1, and a renamed field, a differently read field list or a personal value leaking into an event can never drift between two services without a failing build**.

### 2. Business rationale

Contract-first REST with one hop is the decoupling decision (DP-11, ADR-020). Legacy RWB-E1-053 exposes extraction as an in-process `FieldExtraction` interface inside one module, with a `FieldExtractor`, a `TemplateFieldExtractor` and a `ModelFieldExtractor` implemented in the same process, and it reads the OCR text, the document type catalog and the intake row across module boundaries. Under the target architecture those reads become a P5 schema read, a contract of `rwb-case` for the lists and a contract of `rwb-agent` for the model path, and the shapes most likely to drift silently are exactly the ones this baseline must fix:

- a field renamed in `ExtractionRequest`, `ExtractedField` or `FieldSet`, so the review queue reads a confidence it cannot attribute to a field;
- a field code set read from a different place by the extractor and by the review queue, so the same type yields two different field lists on the same date;
- a confidence read with a different scale or precision, so 0.8000 passes for one consumer and 0.8 fails for another;
- a personal field value written into `rwb.document.DocumentFieldsExtracted.v1`, so a customer account number reaches `rwb-case` and the event log;
- an error returned with the wrong status or without a `messageId`, so a caller cannot tell a document outside its scope from an item that was already extracted.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1`, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit — the P3 reference lists (C `RWB-P3-E1043-CON`) and the P10 agent contract that carries the model path (C `RWB-P10-TE013-CON`, DP-20) — and it records that the classification answer is a same-service contract (H `RWB-P5-E1050-CON` on the app story) and is therefore consumed without a second REST hop.

It also records what the sources leave open. No TSD P5 T-A.1 row and no Architecture v5 slide names a REST operation or a path for running extraction, and no source fixes the field-level names of the request, the field resource, the field set or the event payload: those names are settled here and are Not specified in the source documents (GAP-1008; ASM-1802). The field-extraction route of the rwb-agent contract, the extractor provider, the model name and the model version behind it are Not specified in the source documents (GAP-1009; ASM-1805). Nothing else is guessed: the field codes, the confidence values, the states, the parameter values and the message IDs are copied character for character from RWB-E1-053, the document type table of RWB-P5-E1025-APP and TSD P5 T3.1 and T3.2.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 T3.1 is in force for `document_intake`, `document_field`, `document_text`, `document_type` and `document_hub_parameter`, and TSD P5 T3.2 is in force for LOV-EXTRACT-STATUS, LOV-INTAKE-REVIEW and LOV-DOC-TYPE.
- The Ownership Map is the only source of owners: `document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `lov_value`, `reference_row` and `parameter_catalog` are P3's; the `agent_*` tables, the prompts and the model route are P10's in `rwb_agent`.
- The `rwb-case` reference-data baseline RWB-P3-E1043-CON and the `rwb-agent` contract RWB-P10-TE013-CON are published with their fakes, so the three lists and the model path have one owner document each.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the three operations of section 12.1, the three resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the extract operation: the path on the intake item, the `Idempotency-Key` header, the declared Documents right, the 200 answer carrying the `FieldSet`, and the refusal statuses of AC6.
3. Fix the extract-state read and the fields read, so the review queue and the screens read the same `FieldSet` shape the extract operation answers, including the personal-flag masking rule.
4. Fix `ExtractionRequest`, `ExtractedField` and `FieldSet` field by field, with the required set, the types, the confidence precision and the state values of AC2, AC3 and AC5.
5. Fix the field code set of each of the six types from the type table, with the 26 codes and the four personal fields of AC4, and the mapping of each code to `document_field.field_name`.
6. Map every failure to the error envelope and a message ID, status by status, and carry the open names as gap rows (AC6).
7. Declare the event position: `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`, keyed per document, with field names and codes only and no personal value (AC7).
8. Publish the three fakes and the drift test, tag the baseline, and hand it to RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1032-APP and RWB-ITG-W1.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | A consumer reads a field code set that is not in the type table version in force | The contract test fails against the published field set fixture | None | AC4 |
| X4 | A confidence is read on another scale or precision, or the threshold is read from the contract | The contract test fails: the confidence is numeric(5,4) and the threshold is a parameter, never a contract value | None | AC5 |
| X5 | An error returns a wrong status, no `messageId`, or a package body | The contract test fails on the error envelope and the message table | MSG-P4-001 | AC6 |
| X6 | A personal field value or a field value appears in the event payload | The AsyncAPI schema test and the no-personal-data test fail | None | AC7 |
| X7 | A fake drifts from the document, or the agent contract answer loses its extractor version | The drift test fails the build and the merge is blocked | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T3, the Ownership Map, the P3 list baseline and the P10 agent baseline only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operation set, the shapes, the field code set, the error mapping, the event schema and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E1053-APP, RWB-P5-E1054-APP, the match and store path and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, three operations, three resources, one activity contract, nine contract tables and three fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the field-extraction API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document_intake, document_field, document_text, document_type and document_hub_parameter definitions of TSD P5 T3.1 are in force
    Given the document type table version "DOCTYPE-2026.11" is published with the six types and their 26 fields
    Given the rwb-case reference-data baseline RWB-P3-E1043-CON and the rwb-agent contract RWB-P10-TE013-CON are published with their fakes

  Scenario: AC1 The three operations are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract as owned by rwb-document with a 200 answer of FieldSet
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction and GET /api/recovery/document/v1/documents/{documentId}/fields as owned by rwb-document
    Then the extract operation declares the Documents right U for the type-change caller and a service identity for SY-OCR, the scope rule, the Idempotency-Key header and the statuses 200, 401, 403, 404, 409, 422 and 503
    Then the document states that the paths are its own choice because no TSD P5 T-A.1 row names an extract operation, and records GAP-1008

  Scenario: AC2 ExtractionRequest fixes the required and optional fields (new, D-RCV-60)
    Given the ExtractionRequest resource declared in the document
    When it is compared with the legacy section 12 job step input and the intake columns of TSD P5 T3.1
    Then it carries intakeItemId as a uuid and required
    Then it carries documentId as an optional uuid, present when the item is already attached to a document
    Then it carries documentType as an optional string of the LOV-DOC-TYPE values, used only for the type-change path of the review queue
    Then it carries tableVersion as an optional string, and the version in force is used when it is absent
    Then an absent intakeItemId answers 422 with MSG-GEN-001 and a documentType outside LOV-DOC-TYPE answers 422 with MSG-P5-006
    Then the header Idempotency-Key is required on the POST and carries the value "K-1053-01" in the example

  Scenario: AC3 ExtractedField and FieldSet are fixed (new, D-RCV-60)
    Given the ExtractedField and FieldSet resources declared in the document
    When they are compared with the document_field columns of TSD P5 T3.1 and the legacy section 12 published interface
    Then ExtractedField carries fieldName, dataType, extractedValue, fieldValue, confidence, state, extractorVersion, personal and reviewOnly
    Then fieldName, dataType, confidence, state and extractorVersion are required and every other property is optional
    Then confidence is a number of numeric(5,4) with four decimals, so 0.9600 and 0.0000 are valid and 0.96 is read as 0.9600
    Then state is one of "OK" and "REVIEW" in this baseline, and the values "CONFIRMED" and "CORRECTED" belong to RWB-P5-E1054-APP
    Then FieldSet carries intakeId, documentId, documentType, tableVersion, extractorVersion, extractStatus, reviewReason, fields and fieldCount
    Then the example carries intakeId "IN-0001", documentType "COURT_NOTICE", tableVersion "DOCTYPE-2026.11", extractorVersion "EXT-TPL-1.0" and four ExtractedField entries
    Then a value that cannot be converted keeps extractedValue and answers confidence 0.0000 with state "REVIEW", as in the legacy AC6 of the app story

  Scenario: AC4 The field code set of each type is fixed from the type table (new, D-RCV-60)
    Given the field set fixture of the baseline, built from document_type.field_definitions of version "DOCTYPE-2026.11"
    When it is compared with the six types and the 26 fields of the type table
    Then DEMAND_LETTER carries case_no, account_no, letter_date, amount_demanded and pay_by_date
    Then COURT_NOTICE carries court_name, black_case_no, notice_date and hearing_date
    Then APPRAISAL_REPORT carries appraisal_no, appraisal_date, appraised_value and title_doc_no
    Then TITLE_DEED carries title_doc_no, land_office, owner_name and area_sq_wa
    Then SETTLEMENT_AGREEMENT carries case_no, agreement_date, settlement_amount, installment_count and borrower_name
    Then GUARANTOR_NOTICE carries case_no, guarantor_name, notice_date and amount_claimed
    Then exactly 26 field codes exist across the six types, and account_no, owner_name, borrower_name and guarantor_name carry personal true
    Then each field code maps to document_field.field_name varchar(60), DF-DOC-014, and no code is declared in the contract as a value of another service

  Scenario: AC5 The confidence, the threshold and the confirmed flags are fixed (new, D-RCV-60)
    Given the confidence and state rules declared in the document
    When they are compared with the legacy BR2, BR3, BR5 and BR6 of RWB-E1-053
    Then a confidence at or above the threshold answers state "OK" and below it answers state "REVIEW", with the fixture of 0.8000 as OK and 0.6200 as REVIEW
    Then a field with reviewOnly true answers state "REVIEW" at every confidence, with the fixture of area_sq_wa at 0.9900
    Then a value that cannot be converted answers confidence 0.0000 and state "REVIEW"
    Then the threshold, the pass marks, the attempts, the timeout and the Buddhist Era offset are parameters and appear in the document as names only, never as values
    Then confirmedBy and confirmedAt are declared as optional answer properties and belong to RWB-P5-E1054-APP, and the field that carries a confirmed value is document_field.confirmed_by, DF-DOC-017
    Then a personal field answers extractedValue only when the caller's masking rule allows it, and the personal flag is always present

  Scenario: AC6 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the three operations
    When each status is compared with the legacy section 14 and the service messages of rwb-document
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 and 404 answers MSG-P4-003 for a document or an item that is not found or lies outside the scope
    Then 409 answers MSG-GEN-004 for a concurrent extraction of the same item and for an item whose extractStatus is already DONE
    Then 422 answers MSG-GEN-001 for an absent intakeItemId and MSG-P5-006 for a documentType that is not in the type table in force
    Then 503 answers MSG-GEN-006 with {system} naming "Agent service" for a failed agent route and "Reference data" for a failed list read
    Then MSG-P5-003 is declared as the review notice of a 200 answer whose extractStatus is DONE and whose field list holds at least one REVIEW row, and never as an error
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal returns no partial FieldSet and publishes no event

  Scenario: AC7 The DocumentFieldsExtracted schema carries no personal value (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline
    When it is compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.DocumentFieldsExtracted.v1 is declared on the topic rwb.document.events.v1, keyed by documentId and by intakeId when the item has no document
    Then the payload carries intakeId, documentId, documentType, tableVersion, extractorVersion, extractedAt, fieldCount and fields
    Then each entry of fields carries fieldName, confidence and state, and no entry carries a value, an extractedValue or a fieldValue
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no personal field value, no personal name, no account number and no document text
    Then the document states that only rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1 exist for rwb-document, and the absence test fails a build that declares a third event

  Scenario: AC8 The agent contract and the three fakes match the document (new, D-RCV-60)
    Given the consumed rows of 12.2 and the fakes of 12.8
    When the fakes are run against the document and the drift test compares each one with it
    Then the rwb-agent fake answers the field-extraction route with a value and a confidence per field and an extractor version, and with a 60-second time-out on every attempt for the OUT_OF_TIME case
    Then the rwb-case reference-data fake answers LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW with the values of TSD P5 T3.2
    Then the classification fake answers predicted_type, classification_confidence and review_reason on the intake item
    Then the drift test fails on any mismatch of a path, a status, a field name, a required flag or an enum value
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1053-APP. The legacy AC1 to AC13 of RWB-E1-053 are owned by RWB-P5-E1053-APP, and the wave 1 harness RWB-ITG-W1 consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Architecture v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | This key publishes no event of its own invention: the service has exactly `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, and this key declares the second | TSD P5 T5.3; Architecture v5 slides 16, 41 and 43 |
| BR6 | No business value is fixed in the contract: field codes, extraction methods, patterns, the threshold, the pass marks, the attempts, the timeout, the Buddhist Era offset and the type field set stay data rows of the type table and the parameter table | Template and Rules §R7.2 s17; RWB-E1-053 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, versions, dates, confidences and states only, and no account number, guarantor name, owner name or borrower name in any payload | Architecture v5 slide 11; RWB-E1-053 BR9 and section 17 |
| BR8 | No field value and no document text in an event, an example or a log: the event carries field names, confidences and states only | DP-09; RWB-E1-053 section 12 |
| BR9 | Every consumed row states one hop, a fake and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from RWB-E1-053 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer, so a repeat inside the window creates nothing; a GET declares none | Architecture v5 slide 11; DP-09 |
| BR12 | The contract declares no case state and no document state machine beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E1-053 section 9; RWB-P5-E1053-APP owns the states it writes |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The three operations, the three resources, the field set fixture and the three fakes are described | In review |
| In review | Consumer sign-off | RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1032-APP and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional field on `ExtractedField` | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The values below are the values the fields may carry; the writing of them is the app story's, and the correction out of REVIEW belongs to RWB-P5-E1054-APP.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `state` = "OK" | A field whose confidence is at or above the threshold and whose value converted and matched its pattern |
| `state` = "REVIEW" | A field below the threshold, a `review_only` field, a value that could not be converted, or a value that failed its pattern |
| `extractStatus` = "PENDING", "DONE", "FAILED" | The LOV-EXTRACT-STATUS values of TSD P5 T3.2, carried as an answer property |
| `reviewReason` = "EXTRACTION_FAILED" | The legacy value of RWB-E1-053 X4 for an extractor that does not answer on every attempt; it is not one of the LOV-INTAKE-REVIEW values of TSD P5 T3.2 today, and the list is extended by a data load (GAP-1007; ASM-1799) |
| `confidence` = 0.0000 | The value written with a value that could not be converted, as in the legacy AC6 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment, the field set fixture and the three fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the operation names of GAP-1008 and the agent route of GAP-1009 |
| Consuming teams (RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1032-APP, the P3 list owner, the P10 agent owner and the wave 1 harness) | Review and sign off the parts they consume |
| RW-REFADM, reference data administrator | Loads the type table version the field set fixture is built from (Reference data CRUD) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)". The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here. The model route is not this service's secret: the provider, the model and the key belong to `rwb-agent`, and this baseline declares only the consumed route.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| ExtractionRequest | intakeItemId (uuid, required), documentId (uuid, optional), documentType (optional, LOV-DOC-TYPE), tableVersion (optional); header `Idempotency-Key` (required) |
| ExtractedField | fieldName, dataType, extractedValue, fieldValue, confidence (numeric(5,4)), state (OK or REVIEW), extractorVersion, personal, reviewOnly, confirmedBy (optional), confirmedAt (optional) |
| FieldSet | intakeId, documentId, documentType, tableVersion, extractorVersion, extractStatus, reviewReason, fields (array of ExtractedField), fieldCount |
| Field set fixture | The 26 field codes of version DOCTYPE-2026.11: DEMAND_LETTER case_no, account_no, letter_date, amount_demanded, pay_by_date; COURT_NOTICE court_name, black_case_no, notice_date, hearing_date; APPRAISAL_REPORT appraisal_no, appraisal_date, appraised_value, title_doc_no; TITLE_DEED title_doc_no, land_office, owner_name, area_sq_wa; SETTLEMENT_AGREEMENT case_no, agreement_date, settlement_amount, installment_count, borrower_name; GUARANTOR_NOTICE case_no, guarantor_name, notice_date, amount_claimed. personal true for account_no, owner_name, borrower_name and guarantor_name |
| Field code source | `document_type.field_definitions` (DF-REF-224) in the version in force, with name, data_type, personal, extraction_method, review_only and the optional pattern; the contract declares the codes and never the values of the table |
| document_field shape | field_name (DF-DOC-014, varchar(60)), field_value (DF-DOC-015), confidence (DF-DOC-016, numeric(5,4)), confirmed_by (DF-DOC-017), extracted_value (DF-DOC-034), extractor_version (DF-DOC-035) |
| Event payload | `rwb.document.DocumentFieldsExtracted.v1`: intakeId, documentId, documentType, tableVersion, extractorVersion, extractedAt, fieldCount, fields [fieldName, confidence, state] |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: intake item "IN-0001", type "COURT_NOTICE", extractor version "EXT-TPL-1.0", confidence 0.9600 and 0.6200, the threshold 0.80, the type table version "DOCTYPE-2026.11" and the case "RW-2026-000123" of the legacy story. No example carries a customer value: the account number of the legacy AC7 is declared as the field code `account_no` with no value, and the field values of the legacy examples are examples only. The field-level names of `ExtractionRequest`, `ExtractedField`, `FieldSet` and the event payload beyond the names this baseline fixes are Not specified in the source documents (GAP-1008; ASM-1802).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/intake-items/{intakeItemId}/extract` | no TSD row; the baseline's own path (GAP-1008; ASM-1802) | Request `ExtractionRequest`; answer 200 `FieldSet` | Documents U with scope applied for the type-change caller; the SY-OCR service identity for the intake path | `Idempotency-Key` header, the platform window |
| GET | `/intake-items/{intakeItemId}/extraction` | no TSD row; the baseline's own path (same gap) | Answer 200 `FieldSet` with `extractStatus`, `reviewReason` and the fields | Documents R with scope applied | Not applicable |
| GET | `/documents/{documentId}/fields` | no TSD row; the baseline's own path (same gap) | Answer 200 `FieldSet` of the active fields of the document | Documents R with scope applied | Not applicable |

Error statuses 401, 403, 404, 409, 422 and 503 are those of section 14. The document read `GET /documents/{documentId}` and the content read are the operations of RWB-P5-E1024-APP and are declared there, not here. The three paths above are the baseline's own choice because no TSD P5 T-A.1 row and no Architecture v5 slide names an extract operation; the choice and its reason are recorded as GAP-1008 with the assumption ASM-1802.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW (C `RWB-P3-E1043-CON` through the library of RWB-PLT-E1043-CON) |
| POST | the field-extraction route of the `rwb-agent` contract | P10 rwb-agent | A value and a confidence per field with the extractor version for `extraction_method` MODEL, with the masked text; the path is Not specified in the source documents (GAP-1009; ASM-1805); the owner document is C `RWB-P10-TE013-CON` (DP-20) |

Every row is one hop with a breaker per downstream (DP-11, ADR-020). A failed list read maps to 503 with MSG-GEN-006 naming "Reference data"; a failed agent route is retried to `EXTRACT_MAX_ATTEMPTS` and then maps to the FAILED answer of the extract operation with `reviewReason` EXTRACTION_FAILED, and to 503 with MSG-GEN-006 naming "Agent service" only for the synchronous read of an extraction that has not started. The synchronous reads of this baseline keep the 2 s one-hop budget; the agent route carries the platform's 60-second agent budget, which is the legacy `EXTRACT_TIMEOUT_SECONDS` 60, and each attempt is one hop.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` | P5 rwb-document | Key documentId, or intakeId when the item has no document; payload intakeId, documentId, documentType, tableVersion, extractorVersion, extractedAt, fieldCount and fields [fieldName, confidence, state]; CloudEvents 1.0 binary mode; no field value, no personal value and no document text |

This baseline declares the event schema because the service owns the topic; the row itself is written by the extraction transaction of RWB-P5-E1053-APP, and this key publishes nothing at run time. The service's other event, `rwb.document.DocumentStored.v1`, is declared by the store baseline RWB-P5-E1024-APP; no third event exists for `rwb-document`, and the absence test of AC7 fails a build that declares one.

#### 12.4 Events consumed

None. The extraction path subscribes to no topic: the reference lists are synchronous cached reads, the classification answer is read from the intake row, and the trigger is the Schedule-started workflow of RWB-P5-E1049-APP and the HTTP request of the review queue. A change of a type table version reaches this API on its next read, not on an event.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `extract` | Activity contract | `rwb-document` | One typed activity interface with `ExtractionRequest` in and `FieldSet` out, idempotent by the intake item and the table version; called by `DocumentIntakeWorkflow` and, on the type-change path, by the controller |
| `evaluateExtraction` | Activity contract | `rwb-document` | The labeled-sample run: `FieldSet` evaluation in and the report reference out; no business value in the contract beyond the field codes |

No workflow is declared by this baseline. `DocumentIntakeWorkflow` of the L3 workflow kit template "Document intake" is owned by RWB-P5-E1049-APP and only its `extract` step is named here.

#### 12.6 Schedules

None. This baseline declares no Schedule, no cron entry and no job name; the 15-minute document-intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_field` | P5 (`rwb_document`) | The ExtractedField and FieldSet shapes and the columns of DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 |
| `document_intake` | P5 (`rwb_document`) | Contracted use only: `predicted_type` (DF-DOC-070), `document_id` (DF-DOC-061), `ocr_status` (DF-DOC-063), `extracted_fields` (DF-DOC-077), `extract_status` (DF-DOC-078), `extract_attempts` (DF-DOC-079) and `review_reason` (DF-DOC-080) |
| `document_type` | P5 (`rwb_document`) | Contracted use only: `field_definitions` (DF-REF-224) and `table_version` (DF-REF-229) behind the field set fixture |
| `document_text` | P5 (`rwb_document`) | Contracted use only: `text_content` (DF-DOC-089) as the input of an extraction |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the six parameter names behind the threshold, the pass marks, the attempts, the timeout and the offset |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The event envelope object and the `Idempotency-Key` row |

`lov_value`, `reference_row` and `parameter_catalog` are P3's and the `agent_*` tables, the prompts and the model route are P10's; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-agent extraction WireMock | The field-extraction route answering a value and a confidence per field with extractor version "EXT-MDL-1.0" for a model field; a confidence 0.6200 for `hearing_date`; an absent answer beyond 60 seconds on every attempt for the OUT_OF_TIME case | App story, contract tests, wave 1 harness |
| rwb-case reference-data WireMock | LOV-DOC-TYPE with the six types, LOV-EXTRACT-STATUS with PENDING, DONE and FAILED, LOV-INTAKE-REVIEW with the five values of TSD P5 T3.2 plus the legacy EXTRACTION_FAILED; a delayed answer beyond 2 s and a 503 | App story, contract tests |
| classification fake (same service) | `predicted_type` "COURT_NOTICE" with `classification_confidence` 0.9400, and an item with `review_reason` "LOW_CONFIDENCE" and one with "UNKNOWN_TYPE" | App story, contract tests |
| drift test | Compares each fake with the document and fails on a mismatch of a path, a status, a field name, a required flag or an enum value | Build pipeline |

The exact response field names of the agent route are Not specified in the source documents (GAP-1009; ASM-1805); the fake fixes the names this baseline declares and the drift test of AC8 holds the two together.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The extract operation, the extract-state read and the fields read; the list read of `rwb-case` and the field-extraction route of `rwb-agent`, one hop each |
| Kafka | 1 event schema declared, 0 consumed | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`; `DocumentStored` is the service's other event and is not this key's |
| Temporal | 2 activity contracts | `extract` and `evaluateExtraction` on queue `rwb-document`; no workflow and no Schedule |
| File | None | The contract carries no byte and no body: an extraction reads `document_text` rows and touches no blob |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the three operations and the three resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentFieldsExtracted.v1`; the field set fixture `contract/field-set-DOCTYPE-2026.11.json` for the six types and 26 codes; the contract README rows for the owner, the error mapping, the idempotency rule and the event count; and the three WireMock mapping sets of section 12.8.

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

DP-01 is why the document declares six tables of `rwb_document` and no table of another service: the field set, the state and the confidence are answered from this schema and never from a view or a copy. DP-07 is why the three lists are a consumed row and a fake rather than enum values in the document. DP-09 is why the event is a declared schema with the outbox in the app story and the one-event rule of AC7. DP-10 is why the contract names activity contracts on queue `rwb-document` and no Quartz job. DP-11 is why the extract operation and the two reads are one-hop shapes with a mock and a fixed answer, and why the case of a document is never resolved by a second call from inside this service. DP-13 gives the three paths the service base and removes the monolith base from the contract. DP-15 records the migration position of the extraction columns for the app story. DP-19 puts the field reads behind the gateway-bff composite route for SCR-30 and SCR-31. DP-20 is the agent client: the extraction helper is reached through the rwb-agent contract (C `RWB-P10-TE013-CON`), never through an in-process agent library, so the contract declares a consumed route with a fake and the model, the prompt and the provider stay with `rwb-agent`.

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. The 2-second one-hop budget of DP-11 is stated for the synchronous list read; the agent route carries the platform's 60-second agent budget, which is the legacy `EXTRACT_TIMEOUT_SECONDS` 60, and the document states that deviation explicitly rather than narrowing the agent budget to 2 s.

**Build steps**

1. Write the three operations with their paths, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and AC3 and the four-decimal confidence as a schema constraint and a README row.
3. Publish the field set fixture of AC4 from the type table version in force, with the 26 codes and the four personal flags.
4. Record the confidence, threshold and confirmed rules of AC5 as schema constraints and README rows, and state that the threshold and the pass marks are parameters.
5. Map every status and message ID of AC6 and record the RFC 9457 envelope.
6. Declare the event schema of AC7 with the absence test for a third event and the no-personal-value test.
7. Publish the three fakes and the contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E1053-APP, RWB-P5-E1054-APP, RWB-P5-E1032-APP and RWB-ITG-W1.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the three fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E1053-APP and RWB-ITG-W1 have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW or extraction failed | Some fields need checking. The document is in the review queue. |
| MSG-P4-001 | No valid session, or the person holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | Caller lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document or intake item outside the caller's scope | This case is not in your scope. |
| MSG-P5-006 | documentType is not in the type table in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent extraction of the same item, or an item already extracted | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The agent route or the reference-data read fails | {system} is not available. Your request is queued and will be retried. |

The message IDs and the wording are contract elements copied unchanged from RWB-E1-053 section 14 and the service messages of `rwb-document`; Thai text for each follows decision DL10. MSG-P5-006 and MSG-GEN-004 are the service messages of the type table and of a concurrent change, and neither adds a business value to the contract.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping fixed by AC6 is: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004, 422 with MSG-GEN-001 or MSG-P5-006, and 503 with MSG-GEN-006. MSG-P5-003 is not an error response: it is the review notice carried by a 200 answer whose `extractStatus` is DONE and whose `fields` hold at least one REVIEW entry, and it is the text the screens show. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed: "Agent service" for the agent route and "Reference data" for a list read.

### 15. Screens and states

SCR-30 Case documents and SCR-31 Document review queue read the answers this baseline fixes, through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model. The screens, their forms and their actions are RWB-P5-E1026-APP and RWB-P5-E1054-APP; this baseline fixes the answer shapes only and declares no screen field list and no route specification.

| Screen state implied by the contract | What the answer carries |
|---|---|
| Document with fields | A `FieldSet` whose entries carry field name, value, confidence, state and extractor version |
| Document with a field in review | A `FieldSet` with at least one state REVIEW and the review notice of MSG-P5-003 |
| Item with a failed extraction | A `FieldSet` with `extractStatus` FAILED, `reviewReason` EXTRACTION_FAILED and no field entry |
| Personal field | An entry whose `personal` flag is true; the value is present only when the caller's masking rule allows it |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-053-14 | Access | Component | RW-REFADM user (Documents -) calls the three operations; refused with MSG-P4-002 and the problem envelope, and nothing returned |
| TC-E1-053-01 | AC1, AC2, AC3, AC4, AC5 | Contract | Synthetic Thai court notice, item IN-0001, type COURT_NOTICE, four fields at OK (the legacy AC1 answered against the contract) |
| TC-E1-053-02 | AC4, AC5 | Contract | The 26-code field set fixture of DOCTYPE-2026.11 and the evaluation report reference (the legacy AC2 answered against the contract) |
| TC-E1-053-03 | AC3, AC5 | Contract | `hearing_date` at confidence 0.6200 with state REVIEW (the legacy AC3) |
| TC-E1-053-04 | AC4, AC5 | Contract | TITLE_DEED `area_sq_wa` with reviewOnly true and confidence 0.9900 (the legacy AC4) |
| TC-E1-053-05 | AC5 | Contract | Confidence exactly 0.8000 with state OK (the legacy AC5) |
| TC-E1-053-06 | AC3, AC5 | Contract | An unconvertible value with confidence 0.0000 and state REVIEW (the legacy AC6) |
| TC-E1-053-07 | AC4, AC7 | Contract | The `account_no` code with personal true in the field set and absent from the event payload (the legacy AC7) |
| TC-E1-053-08 | AC6, AC8 | Contract | The agent fake answering beyond 60 seconds on every attempt; `extractStatus` FAILED and `reviewReason` EXTRACTION_FAILED (the legacy AC8) |
| TC-E1-053-09 | AC6 | Contract | A repeat of the extract operation with the same `Idempotency-Key`; one field set, one event (the legacy AC9) |
| TC-E1-053-10 | AC6 | Contract | Two parallel extract operations on one item; one 200 and one 409 with MSG-GEN-004 (the legacy AC10) |
| TC-E1-053-11 | AC3, AC7 | Contract | Document DOC-0001 with version 2 fields and one event for the document (the legacy AC11) |
| TC-E1-053-12 | AC3, AC5 | Contract | An English appraisal report with appraisal_no, appraisal_date and appraised_value (the legacy AC12) |
| TC-E1-053-13 | AC6 | Contract | A document of team HP-NE read by a caller of team MTG-BKK; 404 with MSG-P4-003 (the legacy AC13) |

The fourteen legacy test cases of RWB-E1-053 are listed in the order of the WP and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E1053-APP. The legacy `Level` of System maps to End to end for the end-to-end copies in the app story and is answered here as Contract, because the artefact under test is the contract; the legacy level Access maps to Component. The integration harness copies end in `-ITG` and belong to RWB-ITG-W1. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: field codes, extraction methods, patterns, the threshold, the pass marks, the attempts, the timeout and the Buddhist Era offset stay data rows of the type table and the parameter table.
- No personal data in a schema, an example or a fake: field names, codes, confidences, states, dates and identifiers only; no account number, guarantor name, owner name or borrower name is declared in any answer.
- No field value and no document text in an event, an example or a log; the event carries field names, confidences and states.
- No model client, prompt or provider key is declared or implied by this baseline: the model path is the consumed route of RWB-P10-TE013-CON (DP-20).
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- Only the two events of `rwb-document` exist, and this key declares one of them; the absence test of AC7 fails a build that declares a third.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no document state machine; a transition belongs to the app story that performs it.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | The extract operation, `ExtractionRequest`, `ExtractedField`, `FieldSet`, the 26-code field set fixture, MSG-P5-003, the `DocumentFieldsExtracted` schema | TC-E1-053-01, TC-E1-053-02, TC-E1-053-04, TC-E1-053-05, TC-E1-053-06, TC-E1-053-12 |
| REQ-DCM-001 | Every document stored against its case with type, date, source and extracted fields | The fields read, the `FieldSet` of an attached document, the `account_no` personal rule of the event and the scope refusal of MSG-P4-003 | TC-E1-053-07, TC-E1-053-11, TC-E1-053-13, TC-E1-053-14 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Six `rwb_document` tables declared; the P3 and P10 reads consumed and faked |
| DP-07 | The three lists of 12.2 and their fake |
| DP-09 | The event schema of 12.3, the CloudEvents envelope and the `Idempotency-Key` rule |
| DP-10 | The two activity contracts of 12.5 on queue `rwb-document` |
| DP-11 | The consumed rows of 12.2 with one hop and a fake, and the synchronous 2 s budget |
| DP-13 | The base `/api/recovery/document/v1` of the three operations |
| DP-15 | The migration position of the extraction columns recorded for the app story |
| DP-19 | SCR-30 and SCR-31 behind gateway-bff |
| DP-20 | The agent route of 12.2, its fake and the no-in-process-agent-library rule |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, and the agent budget stated as its own case |

The legacy key is RWB-E1-053; its AC1 to AC13 are owned by RWB-P5-E1053-APP, and the cross-service proof of the same values is RWB-ITG-W1.

### 19. Out of scope

- The build of the extraction activity, the two extractors, the normalizer, the evaluation runner and the field writes: RWB-P5-E1053-APP.
- The review queue screen, the correction of a field and the states CONFIRMED and CORRECTED: RWB-P5-E1054-APP.
- The match step that passes an extracted field set to the store: RWB-P5-E1032-APP.
- The store, the document read and the content read: RWB-P5-E1024-APP.
- The OCR pipeline, the workflow template and its 15-minute Schedule: RWB-P5-E1049-APP.
- The classification model, its contract and its fallback: RWB-P5-E1050-APP and RWB-P5-E1050-CON.
- The document type table load, the Legal and NPA sign-off and the review-only proposal load: RWB-P5-E1025-APP.
- The `rwb-agent` runtime, the prompts, the model route and the provider: P10 `rwb-agent` and RWB-P10-TE013-CON.
- The cross-service proof of these values: RWB-ITG-W1.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
