# RWB-P5-E1054-CON Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1054-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-024) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the review-queue API of `rwb-document` is split out of legacy RWB-E1-054 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the seven operations, the nine shapes, the three resolve actions, the two outcome values, the two review status values a person sets, the error envelope, the event schema, the decision-record position, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1054-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the review-queue API of `rwb-document` — the queue, item read, item content, resolve, field patch, review completion and document read operations on base `/api/recovery/document/v1` with the `ReviewItem`, `ReviewItemPage`, `IntakeItem`, `IntakeResolveRequest`, `IntakeResolution`, `DocumentField`, `FieldReview`, `DocumentReviewRequest` and `Document` shapes, the three resolve actions with their two outcome values and their status codes, the four review statuses and the ten review reasons, the error envelope with every message ID of section 14 and its HTTP status, the `Idempotency-Key` rule with the `If-Match` document lock, the `rwb.document.DocumentFieldsExtracted.v1` schema with no personal data, the DOCATT decision-record position, the fakes with their drift test**, so that **the app story of this legacy key, the store and the extraction inside the same service, the review screens of this service and the wave 1 integration harness build against a fixed, testable contract on Day 1, and a renamed field, a different held set, an action answered with the wrong status or an event carrying a field value can never drift between two builds without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E1-054 carries its six endpoints and its two published Java interfaces in a section 12 of prose, with `CaseDirectory`, `DocumentStore`, `DocumentTypeCatalog`, `FieldExtraction` and `LabeledSetReader` beside them, and it leaves the consumer to infer the exact shapes. Under the target architecture the parts most likely to drift silently are exactly the ones this baseline fixes:

- a field renamed in `ReviewItem` or `ReviewItemPage`, so the review queue on SCR-31 renders without its candidates, its confidence or its age;
- a different held set in the query default, so an item in REVIEW or a document in PENDING disappears from the officer's queue;
- `review_outcome` or `review_status` widened to the values of another list, so the queue half and the document half no longer agree;
- the resolve answer changed from the item to the document for one action only, so a screen that reads the item after SET_TYPE or DISCARD breaks;
- a field patch that is not idempotent, so the second confirmation of AC17 writes a second `confirmed_by` stamp;
- a closed case answered 409 or a stale version answered 422, so the officer reloads instead of re-choosing a case;
- the `DocumentFieldsExtracted` payload changed, or a field value put into it, so a consumer cannot read it and a data steward cannot approve it.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. By rule a CON story has no build dependency, so its H, C, I and X columns are empty (Template and Rules §R5.7; ASM-1817), and the two consumed P3 rows are declared as consumed and faked although the C list of this key belongs to the app story — `RWB-P3-E1035-CON` for the case and `RWB-P3-E1043-CON` for the lists (ASM-1821).

The baseline also records what the sources leave open, and it copies a legacy number into no new place:

- The legacy section 12 answers `IntakeItem` for SET_TYPE and DISCARD and `Document` for ATTACH, while TSD P5 API-P5-013 answers `IntakeResolution` for the one operation. The baseline declares one `IntakeResolution` envelope for all three actions, carrying the item always and the stored document for ATTACH, so one operation has one answer shape (GAP-1011; ASM-1819).
- The legacy field patch carries `If-Match` with the document version and answers `DocumentField`; TSD P5 API-P5-006 answers `DocumentField` and marks idempotency "Not applicable", while the legacy AC17 requires the repeat to change nothing. The baseline declares both: the header lock and an idempotent repeat (ASM-1822).
- The document read behind AC16 and behind a stored letter is the document read of RWB-P5-E1024-APP. The baseline declares it as a reference row so that AC16's 404, the review-completion answer and the read RWB-P6-E1055-CON relies on are tested against one shape (ASM-1820).
- Arch v5 slides 16 and 42 give `rwb-document` exactly two events, `DocumentStored` (EV-16) and `DocumentFieldsExtracted` (EV-17). This baseline declares EV-17 only, because EV-16 belongs to the store, and it declares no third event (ASM-1825).

Nothing else is guessed: the field-level names this key does not settle carry the placeholder `Not specified in the source documents (GAP-1011; ASM-1818)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-003, API-P5-006 and API-P5-010 to API-P5-014, and TSD P5 T3.1 and T3.2 are in force for the `document`, `document_field`, `document_intake`, `document_text` and `document_type` definitions and for the LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE lists.
- The Ownership Map is the only source of owners: `document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; `decision_log_entry` is P7's; the ACE views are P1's.
- The classification, extraction, intake and match baselines are published (RWB-P5-E1050-CON, RWB-P5-E1053-CON, RWB-P5-E1049-APP, RWB-P5-E1032-APP), so `predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version`, `review_reason`, `review_outcome`, `candidate_case_ids`, `extracted_value` and `state` each have one owner document.
- The store baseline of this service (RWB-P5-E1024-APP) is in force, so the `Document` answer of an attach and the `Document` answer of a review completion are the store's shape and not a second one.
- The case and reference-data contracts of `rwb-case` are in force as consumed rows: the case read RWB-P3-E1035-CON and the reference-data read RWB-P3-E1043-CON, both faked in the baseline (ASM-1821).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7; ASM-1817), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1818), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1817).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the seven review operations, the nine resources and the error responses of section 14, on the single base `/api/recovery/document/v1`, on the paths of TSD P5 T-A.1 rebased by DP-13.
2. Fix the queue operation: `kind` with its three values and the ALL default, `reason`, `page`, `size` with the REVIEW_PAGE_SIZE default of 50, the oldest-first order and the two scope halves of BR2.
3. Fix `ReviewItem` and `ReviewItemPage`, so one queue answer carries the kind, the item or document ID, the case number when there is one, the reason, the predicted type, the candidates with their confidence, the received time and the version.
4. Fix `IntakeItem` and `IntakeResolution`, so one read carries the file reference, the OCR pages, the candidates, the candidate cases with their status, the extracted fields with their state, the outcome and the version, and one resolve answer carries the item always and the document for ATTACH.
5. Fix `IntakeResolveRequest` with the three actions, the optional type, case number, field list and discard reason, and the required version.
6. Fix `FieldReview`, `DocumentField` and `DocumentReviewRequest`, with the `If-Match` document lock, the value-required-when-unconfirmed rule and the COMPLETE action.
7. Fix the value sets: the ten review reasons of LOV-INTAKE-REVIEW, the two outcome values ATTACHED and DISCARDED, the four review statuses of LOV-REVIEW, the three field states REVIEW, CONFIRMED and CORRECTED, and the three actions.
8. Map every failure to the error envelope and a message ID, status by status, and carry the placeholder for the three platform rows and the field-level names this key does not settle.
9. Declare the event position and the record position, publish the fakes, the drift test and the baseline tag, then hand the baseline to RWB-P5-E1054-APP, the store and extraction owners inside the service, RWB-P3-E1054-APP, RWB-P4-E1054-APP, RWB-P7-E1054-APP, RWB-P6-E1055-CON and RWB-ITG-E1054-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3, AC4 |
| X3 | The held set of the queue default differs from the two scope halves of BR2 | The contract test fails: the default carries every item with a review reason and no outcome and every document in PENDING, and nothing else | None | AC2 |
| X4 | An action, an outcome value, a review status or a field state is answered with a value outside its declared set | The contract test fails on the enum and on the status of the operation | None | AC4 |
| X5 | An error carries no `messageId`, or a message ID with the wrong status | The contract test fails on the error envelope and on the status mapping of section 14 | MSG-GEN-004 | AC5 |
| X6 | A repeat of the same `Idempotency-Key` attaches a second document, or a repeated field patch writes a second `confirmed_by` stamp | The contract test fails, and the concurrency case answers two 201 where it must answer one 201 and one 409 | MSG-GEN-004 | AC6 |
| X7 | The event payload changes, an eighth field is added, or a field value or a page of text appears in it | The AsyncAPI schema test and the no-personal-data test fail | None | AC7 |
| X8 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, the Ownership Map, the store shape and the two consumed P3 contracts only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operations, the actions, the value sets, the status mapping, the event schema and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E1054-APP, the two review screens, the read of RWB-P6-E1055-CON and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, nine resources, seven operations, two consumed rows, nine contract tables and eight fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the review-queue API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the review, field and document definitions of TSD P5 T3.1 and T3.2 and the operations API-P5-003, API-P5-006 and API-P5-010 to API-P5-014 of TSD P5 T-A are in force
    Given the store baseline RWB-P5-E1024-APP is published with its Document shape and its DOCATT record

  Scenario: AC1 The seven review operations are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/review-items as the review queue and maps it to API-P5-010
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId} and GET /api/recovery/document/v1/intake-items/{intakeItemId}/content and maps them to API-P5-011 and API-P5-012
    Then it declares POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve and maps it to API-P5-013
    Then it declares PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} and maps it to API-P5-006 with the base rebased by DP-13
    Then it declares POST /api/recovery/document/v1/documents/{documentId}/review and maps it to API-P5-014
    Then it declares GET /api/recovery/document/v1/documents/{documentId} as the read of RWB-P5-E1024-APP behind AC16 and the review answer
    Then every operation carries the Documents area, its right, the scope rule and the statuses 200, 401, 403, 404, 409, 422 and 503 as section 14 fixes them
    Then no operation of another service's base is declared as provided

  Scenario: AC2 The ReviewItem and ReviewItemPage shapes and the queue query are fixed (new, D-RCV-60)
    Given the ReviewItem and ReviewItemPage resources declared in the document
    When they are compared with the legacy section 12 response and the TSD P5 T3.1 intake and document fields
    Then ReviewItem carries kind, intakeId or documentId, caseNo, reason, predictedType, candidates, confidence, receivedAt and version
    Then kind is one of INTAKE, DOCUMENT or ALL, candidates is an array of the type code with its confidence, and caseNo is absent for an item with no case
    Then ReviewItemPage carries items, page, size and total and lists the items oldest first
    Then the queue query declares kind with ALL as its default, reason, page and size with the default of the REVIEW_PAGE_SIZE row, and nothing else
    Then the default of the queue carries every intake item with a review_reason and no review_outcome and every document with review_status PENDING, and nothing else
    Then a row an officer may not see is filtered by the scope rule before the page is cut, so total counts only the rows in scope
    Then the example carries an INTAKE row with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21"

  Scenario: AC3 The IntakeItem, IntakeResolveRequest and IntakeResolution shapes are fixed (new, D-RCV-60)
    Given the IntakeItem, IntakeResolveRequest and IntakeResolution resources declared in the document
    When they are compared with the legacy section 12 request and response and the TSD P5 T3.1 columns
    Then IntakeItem carries intakeItemId, source, receivedAt, reviewReason, predictedType, candidates, candidateCases, pages, fields, reviewOutcome, resolvedBy, resolvedAt and version
    Then candidateCases is an array of the case reference with caseNo and status, pages is an array of pageNo and text, and fields is an array of fieldName, extractedValue, fieldValue, state, confidence and personal and is masked by role
    Then IntakeResolveRequest carries action as one of SET_TYPE, ATTACH or DISCARD, documentType, caseNo, fields as an array of fieldName, value and confirmed, discardReason and version, with version required
    Then IntakeResolution carries intakeItem always, document only for ATTACH, and a repeat of the same Idempotency-Key returns the first answer
    Then the same resolve operation answers the item for SET_TYPE and DISCARD and the item with the document for ATTACH, which is the one envelope the baseline declares for the one TSD operation
    Then the example carries action ATTACH, caseNo "RW-2026-000201", documentType "COURT_NOTICE" and version 3

  Scenario: AC4 The DocumentField, FieldReview and DocumentReviewRequest shapes and every value set are fixed (new, D-RCV-60)
    Given the three resources and the five value sets declared in the document
    When they are compared with the legacy exception paths X1 to X11 and the four lists of TSD P5 T3.2
    Then FieldReview carries value, required when confirmed is false, and confirmed, and the request carries If-Match with the document version
    Then DocumentField carries fieldId, fieldName, extractedValue, fieldValue, state, confidence, confirmedBy, updatedAt and version
    Then state carries the three values REVIEW, CONFIRMED and CORRECTED and a confirm or a correct moves a field out of REVIEW
    Then DocumentReviewRequest carries action as COMPLETE and version, and answers the Document shape of the store with reviewStatus CONFIRMED or CORRECTED
    Then reviewReason carries the ten values of LOV-INTAKE-REVIEW and reviewStatus the four values of LOV-REVIEW, of which a person sets PENDING only through the store
    Then reviewOutcome carries the two values ATTACHED and DISCARDED, and an outcome outside the two fails the schema
    Then a value outside any of the five sets fails the schema and the contract test

  Scenario: AC5 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the seven operations
    When each status is compared with the legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 for the right and 404 answers MSG-P4-003 for a case or a document outside the scope
    Then 404 also answers the not-found message whose ID is Not specified in the source documents (GAP-1011; ASM-1823)
    Then 409 answers MSG-GEN-004 for a stale version, an item already resolved or a field changed by another caller
    Then 422 answers MSG-GEN-001 for an empty value, an empty reason or a field still in review, MSG-GEN-002 for a date outside REVIEW_DATE_MIN to REVIEW_DATE_MAX, MSG-P5-005 for a closed case and MSG-P5-006 for a type not in force
    Then 503 answers MSG-P7-003 for a failed decision record and MSG-GEN-006 naming the system that failed
    Then MSG-P5-003 is declared as the label of a held item and MSG-GEN-005 as the confirmation of a saved action, and neither as an error response
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal stores nothing and publishes nothing

  Scenario: AC6 The Idempotency-Key rule, the If-Match lock and the repeat rules are fixed (new, D-RCV-60)
    Given the idempotency and locking declarations of the document
    When they are compared with the legacy section 12 rows and AC9 and AC17
    Then the header is required on the resolve and the review completion and a repeat with the same key returns the first answer and creates no second document, record or event
    Then the header is not declared on the three GET operations and not on the field patch
    Then the field patch declares If-Match with the document version, and a stale document version answers 409 with MSG-GEN-004
    Then the resolve and the review completion require version in the body, and a stale item or document version answers 409 with MSG-GEN-004
    Then the field patch with the same value and the same confirmed flag answers 200 with the saved field and changes neither confirmedBy nor updatedAt
    Then the stored answer of a repeat is kept for the window the platform rule fixes; its exact length is Not specified in the source documents (GAP-1011; ASM-1823)
    Then a repeat never writes a second DOCATT record and never publishes a second event

  Scenario: AC7 The DocumentFieldsExtracted event and the DOCATT record are declared schemas (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline and the record declaration of the document
    When they are compared with the service catalogue, the Event and Messaging design and the record of the store
    Then rwb.document.DocumentFieldsExtracted.v1 is declared on the topic rwb.document.events.v1 with its retry topics at 1 min, 10 min and 1 h and its .dlt topic
    Then the event is keyed by caseId and carries documentId, caseId, documentType, intakeItemId, fieldCount, reviewStatus and extractedAt
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no field value, no page of text and no personal value
    Then rwb.document.DocumentStored.v1 is not declared here, because the store of RWB-P5-E1024-APP declares and writes it for the same document
    Then the document states that rwb-document publishes exactly the two catalogue events and no third event
    Then the decision record is declared on rwb.decision-record.v1 with the decision code DOCATT, the confirmed or corrected type, the item ID as inputsRef and the reviewer where a person decided
    Then the document states that the store writes the record and the event in its own transaction and that this baseline publishes nothing itself

  Scenario: AC8 The eight fakes answer the document and the drift test fails on any mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the eight fakes of 12.8 answer the seven operations of 12.1 and the two reads of 12.2 with the values of the legacy examples, including case "RW-2026-000201", document "DOC-0103", the confidence 0.6200 and the version 3
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name, a required flag or an enum value
    Then the absence test fails a build that declares an eighth review operation, a third event for rwb-document or an event name outside rwb.document.<Event>.v1
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1054-APP. The legacy AC1 to AC17 are owned by RWB-P5-E1054-APP, and the wave 1 harness RWB-ITG-E1054-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation, and the legacy `/api/recovery/v1` prefix is declared nowhere | DP-13; Template and Rules §R4; Arch v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Arch v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property, a narrowed required set or a changed enum is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | The event names of this service follow `rwb.document.<Event>.v1` on its own topic, and the baseline declares EV-17 and no third event, because EV-16 belongs to the store | Arch v5 slides 16 and 42; DP-09; DP-14 |
| BR6 | No business value is fixed in the contract: the review team, the date limits, the page size, the type list, the decision code and the review labels are parameters, reference rows or document defaults | Template and Rules §R7.2 s17; RWB-E1-054 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, versions, confidences, dates and the text of synthetic documents only, and no customer name, address or national ID number in any payload | Arch v5 slide 11; RWB-E1-054 section 17 |
| BR8 | No field value and no page of OCR text in the event or the decision record: the payload carries the item ID, the document ID, the type, the field count and the review status, and the values stay behind the read operations with masking and the access log | DP-09; RWB-E1-054 sections 8 and 17 |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Arch v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E1-054 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer; a GET declares none; the field patch is idempotent on the same value and flag and carries the `If-Match` document lock | Architecture v5 slide 11; DP-09; legacy AC9 and AC17 |
| BR12 | The contract declares no case state and no review workflow beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E1-054 section 9; RWB-P5-E1054-APP owns the review transitions |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The seven operations, the nine resources, the two consumed rows and the event schema are described | In review |
| In review | Consumer sign-off | RWB-P5-E1054-APP, the two review screens, the store owner, the extraction owner and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `ageDays` on a queue row | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a required set is narrowed or an enum value changes | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no review workflow of its own. The states of the five sets it does declare are field values, and the transitions between them belong to RWB-P5-E1054-APP.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `reviewReason` = "LOW_CONFIDENCE" | Classification returned a type below the threshold of the type in force |
| `reviewReason` = "UNKNOWN_TYPE" | Classification named no agreed type |
| `reviewReason` = "MODEL_UNAVAILABLE" | The classifier did not answer and the fallback value was used |
| `reviewReason` = "EXTRACTION_FAILED" | The extractor did not answer on every attempt |
| `reviewReason` = "RESCAN" | The file cannot be read and a new scan is needed |
| `reviewReason` = "UNREADABLE_FILE" | The file is blank or corrupt |
| `reviewReason` = "NO_MATCH" | No case and no account number resolved |
| `reviewReason` = "MULTIPLE" | Two or more open cases for the account number |
| `reviewReason` = "CONFLICT" | The case number and the account number point to different cases |
| `reviewReason` = "CASE_CLOSED" | The only candidate is closed |
| `reviewOutcome` = "ATTACHED" | The item was attached to a case, by a person or by the matcher, and a document exists |
| `reviewOutcome` = "DISCARDED" | The item was discarded with a reason, and its file stays in the intake container |
| `reviewStatus` = "NOT_NEEDED" | A stored document no person must check |
| `reviewStatus` = "PENDING" | A stored document with a field below its threshold, waiting for a person |
| `reviewStatus` = "CONFIRMED" | The review completed with type, case and values kept |
| `reviewStatus` = "CORRECTED" | The review completed with the type, the case or a value changed |
| `document_field.state` = "REVIEW" | A field a person must confirm or correct |
| `document_field.state` = "CONFIRMED" | A field a person confirmed as extracted |
| `document_field.state` = "CORRECTED" | A field a person corrected, with the extracted value kept beside it |

The ten `reviewReason` values of legacy section 3 are the ten values of LOV-INTAKE-REVIEW; the baseline declares all ten so that a consumer can read the field in every state (ASM-1824). The four `reviewStatus` values and the three field states are the lists of TSD P5 T3.2 and LOV-REVIEW, and only PENDING is written by the store while a person writes CONFIRMED or CORRECTED through this API.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment and the eight fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the resolution of GAP-1011 |
| Consuming teams (RWB-P5-E1054-APP, the two review screens, the store owner, the extraction owner, RWB-ITG-E1054-ITG) | Review and sign off the parts they consume |
| RW-LITOFF and RW-CASEOWN, the reviewer roles | Confirm that the queue, the item read and the resolve answer carry what the review screen needs (Documents CRU on the chosen case) |
| RW-TEAMMGR, the reading role | Confirms that the queue and the item read answer a Documents R caller and that the resolve answers 403 (TC-E1-054-18) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1011; ASM-1823). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| ReviewItem | kind (one of INTAKE, DOCUMENT, ALL), intakeId or documentId (uuid), caseNo, reason (one of LOV-INTAKE-REVIEW), predictedType, candidates (typeCode, confidence), confidence (numeric(5,4)), receivedAt, version (integer), from the `document_intake` and `document` fields DF-DOC-001 to DF-DOC-011 and DF-DOC-045 to DF-DOC-084 |
| ReviewItemPage | items (array of ReviewItem), page, size, total; the list is oldest first by receivedAt and created_at |
| IntakeItem | intakeItemId, source, receivedAt, reviewReason, predictedType, candidates, candidateCases (caseNo, status), pages (pageNo, text), fields (fieldName, extractedValue, fieldValue, state, confidence, personal), reviewOutcome, resolvedBy, resolvedAt, version; from `document_intake`, `document_text` and `document_field` |
| IntakeResolveRequest | action (SET_TYPE, ATTACH, DISCARD; required), documentType, caseNo, fields (fieldName, value, confirmed), discardReason, version (integer, required) |
| IntakeResolution | intakeItem (required), document (only for ATTACH), from the item read and the store answer |
| FieldReview | value (required when confirmed is false), confirmed (boolean); the request carries `If-Match` with the document version |
| DocumentField | fieldId, fieldName, extractedValue, fieldValue, state (REVIEW, CONFIRMED, CORRECTED), confidence, confirmedBy, updatedAt, version; from the `document_field` fields DF-DOC-015, DF-DOC-017 and DF-DOC-034 |
| DocumentReviewRequest | action (COMPLETE, required), version (integer, required) |
| Document | documentId, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion; the store's shape, from `document` DF-DOC-001 to DF-DOC-011 |
| Value sets | The ten review reasons, the two outcomes, the four review statuses, the three field states and the three actions of section 9 |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: case "RW-2026-000201", cases "RW-2026-000202" and "RW-2026-000203", the closed case "RW-2026-000150", items "IN-0101" to "IN-0112", documents "DOC-0103" to "DOC-0111", the confidences 0.6200 and 0.2100, the hash "H109", the type codes "COURT_NOTICE", "DEMAND_LETTER", "GUARANTOR_NOTICE" and "PAYSLIP", the field name black_case_no with the value "Por 2001/2569" and the versions 3 and 4. No example carries a real customer value. The field-level names of the nine resources beyond the legacy list are Not specified in the source documents (GAP-1011; ASM-1822), and the baseline fixes them as the smallest superset of that list.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/review-items` | API-P5-010 | 200 `ReviewItemPage`; query `kind` default ALL, `reason`, `page`, `size` 50, oldest first, both scope halves applied | Documents R, scope applied | None |
| GET | `/intake-items/{intakeItemId}` | API-P5-011 | 200 `IntakeItem` with the candidates, the candidate cases, the OCR pages and the masked fields; each read to the access log | Documents R, scope applied | None |
| GET | `/intake-items/{intakeItemId}/content` | API-P5-012 | 200 `application/octet-stream`, the file of the held or discarded item | Documents R, scope applied | None |
| POST | `/intake-items/{intakeItemId}/resolve` | API-P5-013 | Request `IntakeResolveRequest` with action SET_TYPE, ATTACH or DISCARD; answer 200 `IntakeResolution` | Documents U, scope applied to the chosen case | `Idempotency-Key` header plus the `version` lock |
| PATCH | `/documents/{documentId}/fields/{fieldId}` | API-P5-006 | Request `FieldReview`; answer 200 `DocumentField`; `If-Match` carries the document version | Documents U, scope applied | Idempotent on the same value and flag; no header |
| POST | `/documents/{documentId}/review` | API-P5-014 | Request `DocumentReviewRequest` with action COMPLETE; answer 200 `Document` | Documents U, scope applied | `Idempotency-Key` header plus the `version` lock |
| GET | `/documents/{documentId}` | API-P5-003 | 200 `Document`; declared as the reference to the document read of RWB-P5-E1024-APP | Documents R, scope applied | None |

Error statuses 401, 403, 404, 409, 422 and 503 are those of T-A.2 and section 14. The six operations of this key are the ones RWB-ITG-E1054-ITG consumes and the ones RWB-P3-E1054-APP, RWB-P4-E1054-APP and RWB-P7-E1054-APP build against. The seventh row is a declared reference and not a second owner: the document read belongs to RWB-P5-E1024-APP, this baseline restates its shape so that AC16's 404, the review-completion answer and the read RWB-P6-E1055-CON relies on are tested against one shape, and this key changes none of its fields (ASM-1820). The legacy field-patch path under the base `/api/recovery/v1` is declared nowhere in the document; it is rebased by DP-13 and recorded in GAP-1011.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E1035-CON) | The case, its status, its team and its owner behind the closed-case refusal and the scope filter; one hop, 2 s, faked (ASM-1821) |
| GET | `/api/recovery/case/v1/cases/by-no/{caseNo}` | P3 rwb-case (RWB-P3-E1035-CON) | The case a reviewer types on the screen; the same owner document, one hop and 2 s; the path is the one RWB-P5-E1032-APP consumes and this key's sources do not restate it (GAP-1011; ASM-1821) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE (ASM-1824) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a refusal answered as a success. The three rows are declared as consumed and faked and are named in no C row of this story, whose C list is empty by the Day-1 rule; the C rows of this legacy key belong to RWB-P5-E1054-APP and are `RWB-P3-E1043-CON` and `RWB-P3-E1035-CON`.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 rwb-document | Key caseId; payload documentId, caseId, documentType, intakeItemId, fieldCount, reviewStatus, extractedAt; CloudEvents 1.0 binary mode; no field value, no page of text and no personal value |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | The hash-chained record with decision code DOCATT, the confirmed or corrected type, the item ID as `inputsRef` and the reviewer where a person decided |

This baseline declares the event schema and the record declaration because the service owns the topic; the event row and the record are written by the attach path of RWB-P5-E1054-APP inside the store transaction of RWB-P5-E1024-APP, and this key publishes nothing at run time. `rwb.document.DocumentStored.v1` (EV-16) is declared and written by the store of RWB-P5-E1024-APP for the same document and is not re-declared here, so `rwb-document` keeps exactly the two events of Arch v5 slides 16 and 42 and no third event exists for this key (ASM-1825).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This baseline consumes no event: the queue is read on demand and the item enters it when the classification, extraction and match stories write `review_reason` and the field states in `rwb_document`. `AgentRunCompleted`, which Arch v5 slide 16 gives `rwb-document`, is consumed by the classification path of RWB-P5-E1050-APP and not here |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| None | — | — | The seven operations are synchronous and no durable step, activity interface or child workflow belongs to this key. The items of the queue are produced by `DocumentIntakeWorkflow` of RWB-P5-E1049-APP and by the `matchStep` activity of RWB-P5-E1032-APP, which this baseline neither contracts nor changes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | — | — | — | This baseline declares no Schedule and no cron entry: the legacy story has no job and no timer, and the person opens the queue |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | The item, its reason, its candidates, its outcome, its resolved person and time and its version behind `IntakeItem`, `ReviewItem` and `IntakeResolution` |
| `document_text` | P5 (`rwb_document`) | The pages behind `IntakeItem.pages` and the content read |
| `document` | P5 (`rwb_document`) | The `Document` shape and the queue half behind `review_status`, written by the store |
| `document_field` | P5 (`rwb_document`) | The fields behind `DocumentField`, `FieldReview` and the review completion |
| `document_type` | P5 (`rwb_document`) | The type list in force behind the `documentType` values a request may carry |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the rows behind `REVIEW_TEAM_UNATTACHED`, `REVIEW_DATE_MIN`, `REVIEW_DATE_MAX` and `REVIEW_PAGE_SIZE` |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record the store writes |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency rows behind `Idempotency-Key` and the event envelope objects |

`recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's and are named as consumed answers and never declared as this service's tables; `decision_log_entry` is P7's; the ACE views are P1's and are not read here (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| review-queue WireMock | `GET /review-items` with an INTAKE row in each of the ten reasons and a DOCUMENT row in PENDING, oldest first; the item read with the file reference, the pages and the masked fields; the content read as bytes | App story, review screens, contract tests |
| resolve WireMock | Each of the three actions with its `IntakeResolution`; a stale version answered 409 with MSG-GEN-004; a closed case answered 422 with MSG-P5-005; a type not in force answered 422 with MSG-P5-006; a field still in review answered 422 with MSG-GEN-001 | App story, contract tests |
| field and review WireMock | The confirm, the correct, the empty value, the out-of-range date, the repeated patch answered 200 unchanged, and the review completion answered with CONFIRMED and with CORRECTED | App story, contract tests |
| rwb-case case WireMock | Case "RW-2026-000201", "RW-2026-000202" and "RW-2026-000203" open and in scope, case "RW-2026-000150" closed, a case of team "HP-NE" for the 404 of AC16 and a delayed answer beyond 2 s | App story, contract tests |
| rwb-access session fake | RW-LITOFF with Documents CRU and team scope, RW-CASEOWN with own cases only and RW-TEAMMGR with Documents R only | App story, contract tests, TC-E1-054-18 |
| reference-data WireMock | LOV-INTAKE-REVIEW with its ten values, LOV-INTAKE-OUTCOME with ATTACHED and DISCARDED, LOV-REVIEW with its four values and LOV-DOC-TYPE with the type codes of the fixtures | App story, contract tests |
| decision-record and central ledger fake | The local DOCATT record with the confirmed or corrected type, and a refusing write for TC-E1-054-19 | App story, contract tests, wave 1 harness |
| error envelope fake | One answer per message ID of section 14 with its status and its `detail` text | Contract tests, review screens |

A drifted fake fails the drift test of AC8. The exact response field names of the three consumed reads are Not specified in the source documents (GAP-1011; ASM-1821).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 7 provided (6 of this key and 1 declared reference), 3 consumed | The queue, the item read, the content read, the resolve, the field patch, the review completion and the document read; the case read by ID and by number and the lists read; one hop and 2 s on every consumed call |
| Kafka | 1 event schema and 1 record declared, 0 consumed | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1` and the DOCATT record on `rwb.decision-record.v1`; EV-16 is declared by the store |
| Temporal | 0 | No workflow, no activity and no Schedule; the queue is filled by RWB-P5-E1049-APP and RWB-P5-E1032-APP |
| File | 1 reference and 1 read | `storageRef` points at the blob the store writes; the content read returns the file of the intake container `rwb-quarantine`, and this baseline carries no byte |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the seven review operations and the nine resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentFieldsExtracted.v1` and the record declaration; the contract README rows for the three actions, the five value sets, the error mapping, the idempotency and locking rule and the event count; and the eight WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own because it is Day 1 by rule, and the platform and service contracts it names are the ones the app story declares (ASM-1817). DP-01 is applied because every shape derives from a table of `rwb_document` and no other schema is declared. DP-03 is applied because the DOCATT record of an attach is declared and faked here, although the row is written by the store inside the app story's transaction. DP-07 is applied because the four value sets are read through the `rwb-case` reference-data contract and never typed into the document. DP-09 is applied because the event schema, the CloudEvents envelope and the `Idempotency-Key` rule are declared here and written by the app story. DP-11 fixes the three consumed rows to one hop with 2 s and a fake each. DP-13 is applied because the legacy field-patch path and the document read of AC16 carried `/api/recovery/v1` and are declared on `/api/recovery/document/v1`. DP-15 records that the six tables behind the shapes belong to this service's own migration sequence, and the review-outcome columns of the app story are its step. DP-19 records that the queue and the item read are reached through the gateway-bff composite route; this baseline fixes the answer shapes only and no route specification.

**Build steps**

1. Write the seven operations with their paths, queries, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets and the defaults of AC2 to AC4 as schema constraints and README rows.
3. Declare the five value sets of AC4 as enums, with the ten review reasons and the two outcomes spelled out.
4. Map every status and message ID of AC5 and record the RFC 9457 envelope, including the three placeholders.
5. Record the `Idempotency-Key` rule, the `If-Match` lock and the repeat rules of AC6.
6. Declare the event and the record of AC7, with the no-personal-data test and the absence test for an eighth operation and a third event.
7. Publish the eight fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E1054-APP, the two screens, the store owner, the extraction owner and RWB-ITG-E1054-ITG.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the eight fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E1054-APP, RWB-P3-E1054-APP, RWB-P4-E1054-APP, RWB-P7-E1054-APP and RWB-ITG-E1054-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-003 | An item or document is in the review queue (a label, not an error) | Some fields need checking. The document is in the review queue. | 200 |
| MSG-P5-005 | The chosen case is closed | Case {case} is closed. Choose an open case. | 422 |
| MSG-P5-006 | The chosen type is not in force | {value} is not a document type in force. Choose a type from the list. | 422 |
| MSG-P5-024 | The file is already on the case | This file is already on the case as {document}. | 200 |
| MSG-GEN-001 | Empty value, empty reason, field still in review, or a response body that fails validation | Enter {field}. | 422 |
| MSG-GEN-002 | Date outside the allowed range | {field} must be between {min} and {max}. | 422 |
| MSG-GEN-004 | Stale version, item already resolved, field changed by another caller | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-GEN-005 | Field, attach or discard saved (a confirmation, not an error) | Saved. | 200 |
| MSG-P7-003 | Decision record write failed on attach | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 |
| MSG-P4-002 | Caller lacks Documents U | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Item, case or document outside the caller's scope | This case is not in your scope. | 403 or 404 |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-1011; ASM-1823) | 401 |
| MSG-GEN-006 | A consumed read failed or timed out | Not specified in the source documents (GAP-1011; ASM-1823) | 503 |
| not-found message | An intake item or a document that does not exist | Not specified in the source documents (GAP-1011; ASM-1823) | 404 |

The message IDs and the wording of MSG-P5-003 to MSG-P4-003 are contract elements copied unchanged from RWB-E1-054 section 14, and Thai text for each follows decision DL10. MSG-P4-001, MSG-GEN-006 and the not-found message are named by the target error envelope and copied from the platform set; their exact texts are recorded as the placeholder above.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one plus the two platform rows: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003 for an out-of-scope item or document and with the not-found message for an absent one, 409 with MSG-GEN-004, 422 with MSG-GEN-001, MSG-GEN-002, MSG-P5-005 or MSG-P5-006, and 503 with MSG-P7-003 or MSG-GEN-006. The 404 of MSG-P4-003 is deliberate on a document read, so that a document outside the scope is indistinguishable from an absent one; the same message keeps 403 on an item read, where the item itself is in the caller's queue. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed and is "Case service" for all three.

### 15. Screens and states

SCR-31 Document review queue and SCR-30 Case documents are the screens these operations serve, reached through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; the screens themselves, their states and their dialogs are RWB-P5-E1054-APP and the case document list is RWB-P5-E1026-APP. This baseline fixes the answer shapes only and declares no screen field list and no route specification. The states its shapes imply are: a queue row for an intake item in each of the ten reasons, a queue row for a document in PENDING, an item whose panel shows the file, the masked pages, the candidates and the fields in REVIEW, a resolve answered with the item alone or with the item and the document, a field patch answered 200 unchanged on a repeat, a review completion answered CONFIRMED or CORRECTED, an empty queue, and an item or document that is no longer in the caller's scope or no longer exists.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1054-CON-01 | AC1, BR1, BR4 | Contract | The OpenAPI 3.1 document validates; the seven operations and their statuses are declared; no foreign base is provided and the legacy prefix is absent |
| TC-P5-E1054-CON-02 | AC2, BR3 | Contract | A queue with an INTAKE row in each of the ten reasons and a DOCUMENT row in PENDING; a renamed field and a changed default fail the lint |
| TC-P5-E1054-CON-03 | AC3, BR6 | Contract | The resolve request with action ATTACH, case "RW-2026-000201", type "COURT_NOTICE" and version 3; SET_TYPE and DISCARD answer the item alone |
| TC-P5-E1054-CON-04 | AC4, BR5 | Contract | The five value sets; a value outside any enum fails the schema |
| TC-P5-E1054-CON-05 | AC5, BR10 | Contract | One answer per message ID of section 14 with its status; a missing `messageId` fails the test |
| TC-P5-E1054-CON-06 | AC6, BR11 | Contract | The same `Idempotency-Key` twice on the resolve, a stale `If-Match`, a stale version and the repeated field patch |
| TC-P5-E1054-CON-07 | AC7, BR7, BR8 | Contract | The AsyncAPI fragment; an eighth field added to the payload fails the test; a field value in the payload fails the no-personal-data test; a third event fails the absence test |
| TC-P5-E1054-CON-08 | AC8, BR2, BR9 | Contract | The eight fakes run against the document; a drifted path, status, field name, required flag or enum fails the drift test |
| TC-E1-054-18 | Access (legacy), BR2 | Contract | An RW-TEAMMGR caller with Documents R only calls the resolve; refused with 403 and MSG-P4-002 |
| TC-E1-054-19 | Principle 5 (legacy), BR11 | Contract | The decision-record fake refuses the write; the attach answers 503 with MSG-P7-003 and no document |
| TC-E1-054-01 | AC1, BR1 | Contract | An INTAKE row with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21" |
| TC-E1-054-02 | AC2, BR4, BR5 | Contract | The ATTACH resolve answers the item with reviewOutcome ATTACHED and the document with reviewStatus CORRECTED and the corrected hearing_date |
| TC-E1-054-03 | AC3, BR4 | Contract | The field patch on black_case_no and the COMPLETE action answer reviewStatus CONFIRMED |
| TC-E1-054-04 | AC4 | Contract | An empty correction answers 422 with MSG-GEN-001 naming "Court name" |
| TC-E1-054-05 | AC5, BR3 | Contract | The SET_TYPE resolve with "PAYSLIP" answers 422 with MSG-P5-006 naming the value |
| TC-E1-054-06 | AC6 | Contract | The corrected date "2569-12-16" answers 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31" |
| TC-E1-054-07 | AC7, BR3 | Contract | An ATTACH with one field still in REVIEW answers 422 with MSG-GEN-001 naming the field |
| TC-E1-054-08 | AC8, BR3 | Contract | The ATTACH on case "RW-2026-000150" answers 422 with MSG-P5-005 naming the case |
| TC-E1-054-09 | AC9, BR8 | Contract | Two resolves at version 3 answer one 200 and one 409 with MSG-GEN-004 |
| TC-E1-054-10 | AC10 | Contract | The SET_TYPE resolve to "GUARANTOR_NOTICE" answers the item with the four new fields in REVIEW and none of the five DEMAND_LETTER fields |
| TC-E1-054-11 | AC11 | Contract | The ATTACH of an item whose hash is already "H109" answers the item linked to "DOC-0109" with MSG-P5-024 and no second document |
| TC-E1-054-12 | AC12, BR9 | Contract | The DISCARD with a reason answers reviewOutcome DISCARDED with the reason, the caller and the time, and the content read still answers |
| TC-E1-054-13 | AC13 | Contract | The DISCARD with an empty reason answers 422 with MSG-GEN-001 naming "Reason" |
| TC-E1-054-14 | AC14, BR2 | Contract | Five rows across two teams answer three rows oldest first and never the rows of the other team |
| TC-E1-054-15 | AC15 | Contract | An empty queue answers an empty page with total 0 |
| TC-E1-054-16 | AC16, BR10 | Contract | The document read of a document of team "HP-NE" answers 404 with MSG-P4-003 |
| TC-E1-054-17 | AC17 | Contract | The same field patch twice answers 200 with the saved field and unchanged confirmedBy and updatedAt |

The nineteen legacy test cases of RWB-E1-054 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E1054-APP. TC-E1-054-18 keeps the legacy level Access and maps to Component in the app story and to Contract here, TC-E1-054-19 keeps the legacy level Resilience and maps to NFR in the app story and to Contract here, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copies end in `-ITG` and belong to RWB-ITG-E1054-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the review team, the date limits, the page size, the type list, the decision code and the review labels stay parameters, reference rows or document defaults of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, confidences and dates only, and the text of a synthetic document only.
- No field value and no page of OCR text in the event or the decision record: the payload carries the item ID, the document ID, the type, the field count and the review status, and the values stay behind the read operations with masking and the access log.
- The three consumed rows are declared as consumed and faked and never as provided; the lists arrive through their client library (DP-07).
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; a foreign base or a foreign table fails the review except the one declared reference to the document read of RWB-P5-E1024-APP, which is named as a reference and not as a second owner (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- The event name carries the service short and the topic is the service's own; `rwb-document` keeps exactly the two catalogue events, and a third fails the absence test (DP-14, ASM-1825).
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no review workflow; a transition belongs to RWB-P5-E1054-APP.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue, checked by a person | The queue and the item read, the five value sets, the resolve operation, the field patch and the review completion | TC-P5-E1054-CON-01, TC-P5-E1054-CON-02, TC-P5-E1054-CON-03, TC-P5-E1054-CON-04, TC-E1-054-01 to TC-E1-054-11, TC-E1-054-14 to TC-E1-054-19 |
| REQ-DCM-019 | A discarded document is never removed silently; the reason and the person are kept with the file | The DISCARD action, the `discardReason`, `resolvedBy` and `resolvedAt` fields and the content read of a discarded item | TC-P5-E1054-CON-03, TC-P5-E1054-CON-05, TC-E1-054-12, TC-E1-054-13 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the case and the lists consumed and faked |
| DP-03 | The DOCATT record declaration of 12.3 and the ledger fake |
| DP-07 | The three consumed rows and the four value sets |
| DP-09 | The `Idempotency-Key` rule, the event schema and the CloudEvents envelope |
| DP-11 | All three consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | The field patch and the document read on `/api/recovery/document/v1` |
| DP-15 | The migration position recorded for the six tables and the review columns |
| DP-19 | SCR-31 and SCR-30 behind gateway-bff, and the review screen reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E1-054; its AC1 to AC17 are owned by RWB-P5-E1054-APP, its cross-service proof is RWB-ITG-E1054-ITG, and the case-side review task that reads this baseline is RWB-P3-E1054-APP.

### 19. Out of scope

- The build of the queue, the item panel, the three resolve actions, the field services and the two screens: RWB-P5-E1054-APP.
- The store, the `document` and `document_field` rows, the write-once container and the DOCATT row: RWB-P5-E1024-APP.
- OCR, classification, extraction and matching: RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP and RWB-P5-E1032-APP.
- The case-side review task, its queue codes, its task codes and its outcome codes: RWB-P3-E1054-APP.
- The roles, the rights, the team scope and the masking rules: RWB-P4-E1054-APP and `rwb-access`.
- The collection of the DOCATT record into the central ledger: RWB-P7-E1054-APP.
- The parameters and reference-data catalogues themselves and their admin operations: P3 rwb-case.
- The composite route specification and the screen field list: RWB-PLT-N001-CON; the compute, storage, topic and ACL provisioning and the chart, dashboards, alerts and runbook of this service, which this key does not raise as a separate story.
- The cross-service proof of these values: RWB-ITG-E1054-ITG.
