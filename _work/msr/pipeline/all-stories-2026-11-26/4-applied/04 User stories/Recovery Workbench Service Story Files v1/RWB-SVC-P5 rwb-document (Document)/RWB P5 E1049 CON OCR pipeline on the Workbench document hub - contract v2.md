# RWB-P5-E1049-CON OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1049-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-016, FR-P5-020, FR-P5-022, FR-P5-023, FR-P5-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the document intake API of `rwb-document` is split out of legacy RWB-E1-049 and published on base `/api/recovery/document/v1` with the four operations, the three shapes, the value sets, the error envelope, the event schema and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1049-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the document intake API of `rwb-document` — the intake submit, the intake item read, the text read and the OCR status operations on base `/api/recovery/document/v1`, the `IntakeItem`, `OcrTextPage` and `IntakeStatus` shapes, the `ocr_status` and `match_status` value sets, the error envelope with every message ID and its HTTP status, the `Idempotency-Key` rule, the `rwb.document.OcrCompleted.v1` schema with no personal data and the `DocumentIntakeWorkflow` input and output shapes**, so that **the app story of this key, the review queue, the classification and extraction steps, the operations story and the wave 1 harness build against one fixed, testable contract on Day 1, and a renamed property, a differently ordered value set or a silently changed event payload can never drift between two consumers without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the OCR step exposed an in-process `OcrOutputReader` with two methods and read its parameters and its case owner from tables in the same schema. Under the target architecture the intake record, its pages and its status are read by three other consumers — the review queue screen through gateway-bff, the classification step and the extraction step — and the parameters and lists arrive from `rwb-case`. That is exactly the shape of dependency where drift is silent:

- a page list returned in an undefined order, so the review queue shows page 3 before page 1;
- a `ocr_status` value spelled `RESCANNED` by one consumer and `RESCAN` by the writer, so a held item never appears in the queue;
- an `ocr_attempts` counter not carried, so the operations alert on a stuck item cannot be built;
- an OCR status read answered 200 with `DONE` while the engine never answered;
- an event payload that grows a page text field, so personal data leaves the service on a topic;
- a workflow input changed without the worker, so a Schedule tick starts a run that no activity can serve.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It declares the C dependencies it relies on for the two client libraries, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`, and it records that the `rwb-case` case contract it also consumes is in no C row of this key, by `ASM-1786`.

Two missing-source facts are recorded rather than filled. The field-level names of the three shapes and the path segment of the OCR status operation are Not specified in the source documents (GAP-0999; ASM-1781): the baseline derives the property names from the field IDs DF-DOC-045 to DF-DOC-090 and the operation paths from the API-P5-011 pattern, and it publishes them for consumer sign-off. And the architecture's service catalogue lists exactly two events for `rwb-document`, `DocumentStored` and `DocumentFieldsExtracted`, while this pipeline needs a completion signal for the classification and extraction steps; the third name `rwb.document.OcrCompleted.v1` is therefore declared with the conflict recorded in `GAP-0998` and `ASM-1780`, never silently.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-011, and TSD P5 T3.1 is in force for the `document_intake` and `document_text` definitions the shapes draw on.
- The Ownership Map is the only source of owners: `document_intake`, `document_text`, `document`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; the outbox, inbox and idempotency tables are the platform library's, created in `rwb_document`.
- The workflow kit L3 template "Document intake" is published (RWB-PLT-E1071-CON), so the workflow input and output this baseline fixes are the shape the worker runs.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the four operations, the three resources and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the intake submit: the multipart or JSON body of the intake paths, the declared service identity, the `Idempotency-Key` header and the 201 answer carrying an `IntakeItem` in PENDING.
3. Fix the `IntakeItem`, `OcrTextPage` and `IntakeStatus` shapes from the field IDs of TSD P5 T3.1, and state which properties are required and which are optional so a consumer of the first version keeps working.
4. Fix the two value sets as closed enumerations: `ocr_status` from LOV-OCR-STATUS and `match_status` from LOV-INTAKE-MATCH, with the note that the match step writes the second and this baseline only declares the values.
5. Map every failure to the error envelope and a message ID, status by status, and declare that the two value sets and the two message sets live in reference data, never in a client.
6. Record the `Idempotency-Key` rule, the window and the stored-answer behaviour of a repeat, and the rule that a DONE item is never read twice.
7. Declare the `rwb.document.OcrCompleted.v1` schema with its payload and the no-personal-data rule, and record the two-event catalogue conflict.
8. Declare the `DocumentIntakeWorkflow` input and output and the five activity contracts it composes; publish the four fakes, the drift test and the baseline tag; hand the baseline to RWB-P5-E1049-APP, RWB-P5-E1049-OPS and RWB-ITG-E1049-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2 |
| X3 | A status or match value outside its value set is written or accepted | The contract test fails on the enumeration; the app answers 422 rather than storing the value | MSG-GEN-001 | AC3 |
| X4 | A value set is copied into client code instead of read from reference data | The review fails: the list is LOV-OCR-STATUS or LOV-INTAKE-MATCH and nothing else | None | AC3, AC8 |
| X5 | An error is returned without a `messageId`, or with the wrong status | The contract test fails on the status-by-status table of AC4 | None | AC4 |
| X6 | The event payload changes, a field is added, or a page text or a personal value appears in it | The AsyncAPI schema test and the no-personal-data test fail | None | AC6 |
| X7 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X8 | The OCR engine answer is modelled in the contract instead of behind the client | The review fails: the engine is external (RWB-P5-E1049-INF) and the contract fixes only the status the service publishes | None | AC2, AC6 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A, the Ownership Map and the workflow kit only |
| Negotiable | Pass | The property names are settled with the four consumers; the operation set, the value sets, the error mapping, the event schema and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks the app story, the operations story and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, three resources, four operations, one event schema, one workflow shape, nine contract tables and four fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the document intake API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document_intake and document_text definitions of TSD P5 T3.1 and the operation API-P5-011 of TSD P5 T-A are in force
    Given the L3 workflow kit template "Document intake" is published

  Scenario: AC1 The four operations are declared on the single base and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /api/recovery/document/v1/intake-items as the intake submit, owned by rwb-document, with the Idempotency-Key header and the statuses 201, 401, 403, 422 and 503
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId} as the intake item read and maps it to API-P5-011
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId}/text as the text read and GET /api/recovery/document/v1/intake-items/{intakeItemId}/ocr-status as the OCR status read
    Then every path carries the single base /api/recovery/document/v1 and no other service's base
    Then the content download API-P5-012 is named as the review queue story's and is not declared here

  Scenario: AC2 IntakeItem, OcrTextPage and IntakeStatus are fixed (new, D-RCV-60)
    Given the three resources declared in the document
    When they are compared with the document_intake and document_text fields of TSD P5 T3.1
    Then IntakeItem carries intakeItemId, source, sourceRef, receivedAt, fileSha256, scanResult, caseId, documentId, ocrRef, ocrStatus, ocrAttempts, pageCount, rescanPages, ocrQuality, languages, ocrEngineVersion, reviewReason and matchStatus
    Then OcrTextPage carries pageNo, textContent and quality, and the text read answers them ordered by pageNo ascending
    Then IntakeStatus carries ocrStatus, ocrAttempts, ocrEngineVersion, rescanPages and reviewReason
    Then intakeItemId and ocrStatus are required on IntakeItem, pageNo and textContent are required on OcrTextPage, and ocrStatus is required on IntakeStatus, so every other property is optional
    Then source is one of "SCAN", "UPLOAD", "GENERATED", "PARTNER" and "EMAIL" of LOV-DOC-SOURCE and scanResult is one of "CLEAN" and "INFECTED" of LOV-SCAN-RESULT
    Then the example carries intakeItemId "INT-000481", pageCount 4, ocrQuality 0.4100, languages "th,en" and rescanPages "3"
    Then the candidate and extracted-field properties of API-P5-011 are named as RWB-P5-E1053-CON's and are not fixed here

  Scenario: AC3 The ocr_status and match_status value sets are closed enumerations (new, D-RCV-60)
    Given the two value sets declared in the document
    When they are compared with the TSD P5 T3.2 lists
    Then ocr_status is exactly "PENDING", "DONE", "RESCAN" and "FAILED" of LOV-OCR-STATUS
    Then match_status is exactly "PENDING", "MATCHED", "NO_MATCH", "MULTIPLE", "CONFLICT", "CASE_CLOSED" and "NO_TYPE" of LOV-INTAKE-MATCH
    Then reviewReason is exactly "RESCAN", "UNREADABLE_FILE", "LOW_CONFIDENCE", "MODEL_UNAVAILABLE" and "UNKNOWN_TYPE" of LOV-INTAKE-REVIEW
    Then the document states that match_status is written by the match step of RWB-P5-E1032-APP and only declared here
    Then a value outside a set is refused by the schema and no client copies a list into code
    Then the baseline states that the values are read from reference data through RWB-P3-E1043-CON

  Scenario: AC4 The error envelope, every message ID and its HTTP status are fixed (new, D-RCV-60)
    Given the error responses declared for the four operations
    When each status is compared with the legacy section 14
    Then 401 is the platform authentication answer before the operation is reached and carries no business message ID
    Then 403 answers MSG-P4-002 for a role without the Documents right and MSG-P4-003 for a case outside the caller's scope
    Then 422 answers MSG-GEN-001 for an empty or malformed submit, with the field named
    Then 503 answers MSG-GEN-006 for a failed engine call or a failed consumed call, naming the system that failed
    Then 404 answers a not-found message whose ID is Not specified in the source documents (GAP-0999; ASM-1781)
    Then every error is an RFC 9457 problem response with messageId, detail and instance
    Then MSG-P5-018 is declared as a notification of the rescan path and not as an HTTP error

  Scenario: AC5 The Idempotency-Key rule and the no-second-read rule are fixed (new, D-RCV-60)
    Given the idempotency rule of the submit operation
    When it is compared with the legacy section 12 idempotency row
    Then the header is required on the POST and a repeat with the same key answers the first stored answer with 201 inside the window
    Then a repeat creates no second intake item, no second text row and no second event
    Then the intake item ID is the idempotency key of the read path: an item that is not PENDING is never read again
    Then the window is a platform value of the idempotency library and is not written in the document as a literal
    Then the concurrent case is answered 409 by the library and never by a second stored item

  Scenario: AC6 rwb.document.OcrCompleted.v1 is a declared schema with no personal data (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline
    When it is compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.OcrCompleted.v1 is declared on the topic rwb.document.events.v1, keyed by caseId where the case is known and by the intake item ID otherwise
    Then the payload carries intakeItemId, documentId, caseId, ocrStatus, pageCount, ocrQuality, ocrEngineVersion and occurredAt, and nothing else
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no page text, no name, no address and no identity number
    Then the document states that the architecture's catalogue lists DocumentStored and DocumentFieldsExtracted for rwb-document only and that this third name is recorded in GAP-0998 with ASM-1780, for consumer sign-off
    Then the retry topics and the .dlt topic of rwb.document.events.v1 are named as RWB-PLT-N002-INF's and are not redefined here

  Scenario: AC7 The DocumentIntakeWorkflow input and output are fixed (new, D-RCV-60)
    Given the workflow section of this baseline and the L3 template "Document intake"
    When it is compared with the legacy section 12 job and the kit's interface
    Then the input carries the business date, the tick time and an optional limit on the number of items per run
    Then the output carries the counts read, done, rescan and failed, and the identifiers of the items whose status changed
    Then the workflow names the five activities ingest, ocr, classify, extract and matchStep on queue rwb-document and names the owning story of each
    Then the input carries no file byte, no page text and no personal value, and the output carries identifiers, statuses and counts only
    Then the document states that the business date is the run unit and that a rerun of a completed business date is refused by the job view
    Then the field-level names of the input and output are the baseline's own and require consumer sign-off, because the sources give no workflow payload (GAP-0999; ASM-1781)

  Scenario: AC8 The four fakes match the document and the drift test fails a mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the OCR engine fake answers a fixed four-page document with page 3 at quality 0.4100, the 503 answer and the unreadable-file answer of the legacy examples
    Then the case fake, the parameters and lists fake and the storage stub answer every consumed read with the values of the legacy examples
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a property name, a required flag or an enumeration value
    Then no fake carries a personal value and no test payload copies a production payload
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1049-APP. The nine legacy acceptance criteria of RWB-E1-049 are owned by RWB-P5-E1049-APP, and the wave 1 harness RWB-ITG-E1049-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01, DP-13; Template and Rules §R4; Architecture v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | `ocr_status`, `match_status` and `review_reason` are closed sets read from LOV-OCR-STATUS, LOV-INTAKE-MATCH and LOV-INTAKE-REVIEW; no client copies a list into code | TSD P5 T3.2; DP-07 |
| BR6 | No business value is fixed in the contract: the quality threshold, the worker count, the timeout, the attempt limit, the idempotency window and the page limit stay parameters of the app story | Template and Rules §R7.2 s17; RWB-E1-049 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, statuses, dates, page numbers and confidences only, and no page text in a payload | Architecture v5 slide 11; RWB-E1-049 section 17 |
| BR8 | No page text and no file byte in an event or a workflow payload: the event carries counts and identifiers, the text is read through the text operation | DP-09; RWB-E1-049 section 17 |
| BR9 | Every consumed row states one hop, a 2 s timeout and a breaker per downstream; a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts of MSG-P5-018 and MSG-P4-002 are copied unchanged from legacy RWB-E1-049 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer, so a repeat inside the window creates nothing; a GET declares none | Architecture v5 slide 11; DP-09 |
| BR12 | The contract declares no case state and no intake state machine beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E1-049 section 9 |
| BR13 | The OCR engine is external: the contract declares the status this service publishes and never models the provider's answer as its own schema | RWB-E1-049 section 12 adapter; RWB-P5-E1049-INF |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The four operations, the three shapes, the two value sets, the event schema and the workflow shape are described | In review |
| In review | Consumer sign-off | RWB-P5-E1049-APP, RWB-P5-E1049-OPS, the classification and extraction owners, the review queue owner and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional field on `IntakeItem` | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a required set is narrowed, or an enumeration value is removed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no intake state machine of its own; the `ocr_status` transitions are RWB-P5-E1049-APP's.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `ocr_status` = "PENDING" | The item is waiting for its first or next read; the selection predicate is this value |
| `ocr_status` = "RESCAN" | A page fell below the threshold; `rescanPages` lists the pages |
| `ocr_status` = "DONE" | Every page was accepted; the item is never selected again |
| `ocr_status` = "FAILED" | The attempt limit was reached or the file could not be opened; `reviewReason` carries UNREADABLE_FILE |
| `match_status` = "PENDING" | The value at creation; the match step moves it and this baseline only declares the set |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment, the fakes and the baseline tag |
| Solution architect | Approves a breaking change, a new major version and the correction of the plan's C list for the case read |
| Consuming teams (RWB-P5-E1049-APP, the review queue owner, the classification and extraction owners, RWB-P5-E1049-OPS and the wave 1 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data property is declared in an answer, an example or a fake, and that the value sets match the reference data |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-0999; ASM-1781). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| IntakeItem | intakeItemId, source, sourceRef, receivedAt, fileSha256, scanResult, caseId, documentId, ocrRef, ocrStatus, ocrAttempts, pageCount, rescanPages, ocrQuality, languages, ocrEngineVersion, reviewReason, matchStatus, from the `document_intake` fields DF-DOC-045 to DF-DOC-084 |
| OcrTextPage | pageNo, textContent, quality, from the `document_text` fields DF-DOC-088 to DF-DOC-090 |
| IntakeStatus | ocrStatus, ocrAttempts, ocrEngineVersion, rescanPages, reviewReason, from DF-DOC-063, -064, -066, -069 and -080 |
| DocumentIntakeWorkflow input | businessDate, scheduledAt, limit |
| DocumentIntakeWorkflow output | read, done, rescan, failed, itemIds |
| OcrCompleted event | intakeItemId, documentId, caseId, ocrStatus, pageCount, ocrQuality, ocrEngineVersion, occurredAt |
| Value sets | ocr_status, match_status and reviewReason as closed enumerations of LOV-OCR-STATUS, LOV-INTAKE-MATCH and LOV-INTAKE-REVIEW |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic: intake item "INT-000481", case "RW-2026-000123", four pages with page 3 at quality 0.4100, the languages "th,en" and the engine version string. No example carries a real customer value and none carries page text. The field-level names of `IntakeItem`, `OcrTextPage` and `IntakeStatus` beyond what the field IDs name, the path segment of the OCR status operation and the workflow payload are Not specified in the source documents (GAP-0999; ASM-1781).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/intake-items` | new, derived from the intake paths of TSD P5 T-A.1 | Request `IntakeSubmit`; answer 201 `IntakeItem` in PENDING | service identity of the intake paths | `Idempotency-Key` header |
| GET | `/intake-items/{intakeItemId}` | API-P5-011 | Answer 200 `IntakeItem` | Documents R, scope applied | Not applicable |
| GET | `/intake-items/{intakeItemId}/text` | API-P5-011 | Answer 200 array of `OcrTextPage`, ordered by `pageNo` | Documents R, scope applied | Not applicable |
| GET | `/intake-items/{intakeItemId}/ocr-status` | derived from API-P5-011 | Answer 200 `IntakeStatus` | Documents R, scope applied | Not applicable |

Error statuses 401, 403, 422 and 503 are those of section 14. `POST /intake-items` carries the required properties source, sourceRef, fileSha256 and the file reference in the intake container; the exact request property names are Not specified in the source documents (GAP-0999; ASM-1781) and the derived names are published for consumer sign-off. `GET /intake-items/{intakeItemId}/content` (API-P5-012) belongs to the review queue story and is declared nowhere in this document.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case and its owner for the rescan notice and the scope check, faked; the plan lists it in no C row of this key (`ASM-1786`) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `OCR_MIN_QUALITY`, `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS` and `OCR_MAX_ATTEMPTS` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-OCR-STATUS, LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-SOURCE and LOV-SCAN-RESULT (C `RWB-P3-E1043-CON`) |

Every row is one hop with a 2 s timeout and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed. The OCR engine is not a row of this table: it is an external provider behind the client of the app story and is provisioned by RWB-P5-E1049-INF.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.OcrCompleted.v1` | `rwb.document.events.v1` | P5 rwb-document | Key caseId where the case is known and the intake item ID otherwise; payload intakeItemId, documentId, caseId, ocrStatus, pageCount, ocrQuality, ocrEngineVersion, occurredAt; CloudEvents 1.0 binary mode; no page text and no personal data |

This baseline declares the event because the service owns the topic; the row itself is written to the outbox by the app story RWB-P5-E1049-APP in the activity transaction, and this key publishes nothing at run time. The service's catalogue events `DocumentStored` and `DocumentFieldsExtracted` are owned by RWB-P5-E1024-APP and the extraction stories; the third name `rwb.document.OcrCompleted.v1` is this baseline's and its conflict with the two-event catalogue is carried by `GAP-0998` and `ASM-1780`, for consumer sign-off and for correction of the catalogue. No decision record is declared: the OCR step writes a fact, not a decision.

#### 12.4 Events consumed

| Event | Topic | Use in the baseline |
|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | Declared as the input of the `ingest` activity: one intake item per stored document with source UPLOAD, dropped on redelivery by the inbox row of DP-09 |

No other event is consumed. The shape of `DocumentStored` belongs to RWB-P5-E1024-APP and is named here only to fix the fact that this pipeline starts from it.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 template "Document intake" | `rwb-document` | Input businessDate, scheduledAt and an optional limit; output the counts read, done, rescan and failed and the identifiers of the items whose status changed; one run per Schedule tick and business date |
| `ingest` | Activity contract | `rwb-document` | Takes the stored document receipt and answers the intake item ID; owned by RWB-P5-E1049-APP |
| `ocr` | Activity contract | `rwb-document` | Takes the intake item ID and answers the `IntakeStatus` result; owned by RWB-P5-E1049-APP |
| `classify` | Activity contract | `rwb-document` | Contracted by RWB-P5-E1050-CON and named here as a step of the same workflow run |
| `extract` | Activity contract | `rwb-document` | Contracted by RWB-P5-E1053-CON and named here as a step of the same workflow run |
| `matchStep` | Activity contract | `rwb-document` | Contracted by RWB-P5-E1032-CON and named here as a step of the same workflow run |

The workflow input and output names are this baseline's own; the sources give no workflow payload, so they are published for consumer sign-off (GAP-0999; ASM-1781). The retry policy is the kit's and is not restated here.

#### 12.6 Schedules

None. This baseline declares no Schedule, no cron entry and no job name; the 15-minute business-hours Schedule of legacy JOB-12 is registered by RWB-P5-E1049-OPS and starts the workflow above.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | The `IntakeItem` and `IntakeStatus` shapes and the columns they carry, with the field IDs of section 11 |
| `document_text` | P5 (`rwb_document`) | The `OcrTextPage` shape and the ordered page read |
| `document` | P5 (`rwb_document`) | Read only: the case, source and storage reference of an attached document, as carried on `IntakeItem` |
| idempotency, outbox and inbox library tables | PLT library, created in `rwb_document` | The stored answer behind `Idempotency-Key`, the OcrCompleted outbox row and the `DocumentStored` inbox row |

`recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's in `rwb_case`; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| OCR engine WireMock | A fixed four-page answer with lines, words, positions, language and word confidence, page 3 at quality 0.4100; a page at exactly 0.7000; an HTTP 503 on every call; a password-protected PDF answer; a delayed answer beyond `OCR_TIMEOUT_SECONDS` | App story, contract tests, wave 1 harness |
| rwb-case case WireMock | `GET /cases/{caseId}` for case "RW-2026-000123" with its owner, a case outside the caller's scope and a delayed answer beyond 2 s | App story, contract tests |
| parameters and reference-data WireMock | `OCR_MIN_QUALITY` 0.70, `OCR_WORKERS` 4, `OCR_TIMEOUT_SECONDS` 120, `OCR_MAX_ATTEMPTS` 3, and the five lists of AC3 | App story, contract tests |
| storage product stub | The intake file read and the OCR JSON write at `ocr/{intakeId}.json`, with a refusing write and an absent file | App story, contract tests |

A drifted fake fails the drift test of AC8. The engine fake models the provider answer only to fix the published status; the provider itself remains external and is provisioned by RWB-P5-E1049-INF.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | The intake submit, the intake item read, the text read and the OCR status read; the case read, the parameters read and the list read; one hop and 2 s on every consumed call |
| Kafka | 1 event schema declared and 1 consumed declared, 0 published at run time | `rwb.document.OcrCompleted.v1` on `rwb.document.events.v1` with its retry and `.dlt` topics, and `DocumentStored` as the input of `ingest` |
| Temporal | 1 workflow and 5 activity contracts | `DocumentIntakeWorkflow` from the kit template on queue `rwb-document`; no Schedule declared |
| File | 2 references | The intake file in the intake container and the OCR JSON at `ocr/{intakeId}.json` in the text container; this baseline carries no byte and no body |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the four operations and the three resources; the AsyncAPI 3.0 fragment for `rwb.document.OcrCompleted.v1`; the workflow interface rows for `DocumentIntakeWorkflow`; the contract README rows for the value sets, the error mapping, the idempotency rule and the event count; and the four WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own, because it is Day 1 by rule, and the platform and service contracts it names are the ones the app story declares. DP-01 and DP-13 appear because the baseline fixes the schema and the base every operation carries; DP-06 and DP-07 because the two value sets and the four parameters are consumed answers rather than literals; DP-09 and DP-10 because the event schema and the workflow shape are declared here; DP-11 because the case read and the two client libraries are consumed with a mock and a 2 s timeout; DP-15 and DP-19 because the migration position and the composite route are recorded here for the app and operations stories.

**Build steps**

1. Write the four operations with their paths, resources, security and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and the closed enumerations of AC3 as schema constraints and README rows.
3. Map every status and message ID of AC4 to the error envelope and record the not-found placeholder.
4. Record the `Idempotency-Key` rule and the no-second-read rule of AC5.
5. Declare the `OcrCompleted` schema of AC6 with the no-personal-data test and the catalogue-conflict row.
6. Declare the workflow input and output of AC7 and the five activity contracts with their owning stories.
7. Publish the four fakes and the contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E1049-APP, RWB-P5-E1049-OPS and the wave 1 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the four fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E1049-APP and RWB-ITG-E1049-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-018 | A page is below the quality threshold on a document of a known case (declared as a notification, not an HTTP error) | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P4-002 | Caller lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The item's case is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | The submit is empty or malformed, or a value outside a set is sent | Enter {field}. |
| MSG-GEN-006 | The OCR engine did not answer, or a consumed call failed | {system} is not available. Your request is queued and will be retried. |

The message IDs and the wording of MSG-P5-018 and MSG-P4-002 are contract elements copied unchanged from RWB-E1-049 section 14; MSG-P4-003, MSG-GEN-001 and MSG-GEN-006 exist in the source documents and are the refusal and unavailability shapes the target operations need. Thai text for each follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is fixed by AC4: 401 by the platform authentication answer, 403 with MSG-P4-002 or MSG-P4-003, 422 with MSG-GEN-001, and 503 with MSG-GEN-006. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed. A not-found answer uses 404 with a message whose ID is Not specified in the source documents (GAP-0999; ASM-1781).

### 15. Screens and states

The baseline serves the review queue screen SCR-31 through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; it fixes the answer shapes only and declares no screen field list and no route specification. The screen states the shapes imply are the ones `IntakeStatus` and `OcrTextPage` carry: an item in PENDING with no page yet, an item in DONE with every page, an item in RESCAN with the page numbers listed, and an item in FAILED with the reason. The screen itself is RWB-E1-054's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-049-10 | Access, AC4 | Component | RW-CAPACITY user (no Documents right) calls the intake item read; refused with MSG-P4-002 |
| TC-E1-049-01 | AC1, AC2, BR1 | Contract | The 180 synthetic sample documents as one intake item per file, Thai and English |
| TC-E1-049-02 | AC1, AC5 | Contract | 500 synthetic pages in 125 items submitted with one idempotency key per file |
| TC-E1-049-03 | AC2, AC3, AC4 | Contract | Four pages with page 3 at quality 0.4100 |
| TC-E1-049-04 | AC2, AC3 | Contract | Two pages with no case, page 1 at 0.3000 |
| TC-E1-049-05 | AC2, AC3 | Contract | One page at exactly 0.7000 |
| TC-E1-049-06 | AC4, AC6 | Contract | Engine fake returning 503 |
| TC-E1-049-07 | AC2, AC3, AC4 | Contract | Password-protected synthetic PDF answer |
| TC-E1-049-08 | AC5, AC6 | Contract | 10 items already DONE with 25 text pages |
| TC-E1-049-09 | AC5, AC7 | Contract | One item and four concurrent workers |

The ten legacy test cases of RWB-E1-049 are listed in the order of the WP and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E1049-APP. TC-E1-049-10 keeps the legacy level Access and maps to Component, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copies end in `-ITG` and belong to RWB-ITG-E1049-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the threshold, the worker count, the timeout, the attempt limit, the idempotency window and the page limit stay parameters of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, statuses, dates, page numbers and confidences only; no page text, name, address or identity number is declared in any answer.
- No page text and no file byte in a payload, an example or a fake; the event carries counts and identifiers and the text is read through the text operation.
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- Only `DocumentStored`, `DocumentFieldsExtracted` and the declared `OcrCompleted` exist for `rwb-document`, and the third name is carried as a signed conflict rather than as a silent addition.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no intake state machine; a transition belongs to the app story that performs it.
- The value sets are read from reference data; a client that copies LOV-OCR-STATUS, LOV-INTAKE-MATCH or LOV-INTAKE-REVIEW into code fails the review.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English, which needs Thai and English text first | The `IntakeItem` languages and the `OcrTextPage` shape, the text read, the OCR status read | TC-E1-049-01, TC-E1-049-03, TC-E1-049-04, TC-E1-049-05, TC-E1-049-07 |
| REQ-DCM-009 | Documents from every path through the same intake | The intake submit, the intake item read, the idempotency rule, the `OcrCompleted` schema | TC-E1-049-02, TC-E1-049-06, TC-E1-049-08, TC-E1-049-09, TC-E1-049-10 |
| REQ-DCM-010 | A file is read only after its malware scan is CLEAN | The `scanResult` property and the LOV-SCAN-RESULT enumeration on `IntakeItem` | TC-E1-049-01, TC-E1-049-07 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the P3 reads consumed and faked |
| DP-06 | The parameters row of 12.2 and the four parameter names |
| DP-07 | The list row of 12.2 and the three value sets |
| DP-09 | The `Idempotency-Key` rule, the `OcrCompleted` schema and the CloudEvents envelope |
| DP-10 | The `DocumentIntakeWorkflow` input and output and the five activity contracts |
| DP-11 | All three consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | The single base `/api/recovery/document/v1` on all four operations |
| DP-15 | The migration position recorded for `document_intake` and `document_text` in the service's own sequence |
| DP-19 | SCR-31 behind gateway-bff, and the review queue story reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E1-049; its AC1 to AC9 are owned by RWB-P5-E1049-APP, and the cross-service proof of the same values is RWB-ITG-E1049-ITG.

### 19. Out of scope

- The build of the pipeline, the activities, the engine client, the quality rule and the notifier: RWB-P5-E1049-APP.
- The OCR engine itself, its capacity, its secret and its network path: RWB-P5-E1049-INF.
- The deployment, the Schedule registration, the dashboards, the alerts and the runbook: RWB-P5-E1049-OPS.
- The store, the containers and `DocumentStored`: RWB-P5-E1024-APP.
- The malware scan, classification, extraction and automatic attach: RWB-E1-041, RWB-P5-E1050-APP, RWB-P5-E1053-APP and RWB-P5-E1032-APP, each with its own contract.
- The review queue screen and the item resolve operation: RWB-E1-054 and the review queue story.
- The cross-service proof of these values: RWB-ITG-E1049-ITG.
