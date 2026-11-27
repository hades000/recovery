# RWB-P5-E1050-CON Document classification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1050-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P5-E1050-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 on base `/api/recovery/document/v1`; the OpenAPI document version is not specified in the source documents (DOR-RWB-P5-E1050-CON-23) |
| Integration dependencies | None |
| External dependencies | rwb-agent model-gateway satellite, tracked as external work (GAP-1002); no dependency ID assigned |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the classification API of `rwb-document` is split out of legacy RWB-E1-050 and published on base `/api/recovery/document/v1` with the classify command, the classification-state read, the three shapes, the error envelope, the `Idempotency-Key` rule, the `rwb.document.DocumentClassified.v1` schema and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1050-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the Day-1 contract baseline of the classification API of `rwb-document` — the classify command and the classification-state read on base `/api/recovery/document/v1`, the `ClassificationRequest`, `ClassificationResult` and `TypeCandidate` shapes, the type code set taken from the type table in force, the position of the threshold, the review-reason value set, the error envelope with every message ID and its HTTP status, the `Idempotency-Key` rule, and the `rwb.document.DocumentClassified.v1` schema that carries no OCR text and no document content**, so that **the app story of this legacy key, the attach and review stories that read the result, and the wave 1 integration harness build against one fixed, testable contract on Day 1, and a renamed outcome, a lost candidate, a fifth review reason or a text field in the event can never drift between two readers without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the legacy story classification is a step inside one module: it writes five columns on an intake row and exposes a published Java interface, `ClassificationReader`, that attach and the review queue call in process. Under the target architecture the readers are other stories of the same service and, for the event, other services, so the shapes most likely to drift silently are exactly the ones this baseline fixes:

- an outcome renamed or a review reason added, so a held document is filed as classified or the review queue shows a reason no screen knows;
- the two candidates dropped or reordered, so a reviewer sees one candidate or the wrong pair;
- the confidence rounded differently by the step and by the read, so a 0.7999 item is filed as at the threshold;
- the threshold moved into the schema as a default, so a data change needs a deployment;
- an event payload that carries the OCR text or the masked text, so personal data leaves the service on a topic;
- an error returned with the wrong status or without a `messageId`, so a caller cannot tell a refused right from an item that is no longer selectable.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its event names `rwb.document.<Event>.v1`, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`.

It also records the two things the sources do not settle. No source names a classification path or an API identifier for it: TSD P5 appendix T-A runs from API-P5-001 to API-P5-017 and carries no classify operation, and API-P5-011 to API-P5-014 describe the intake-item read, its content, its resolve and the document review, not the classification command. The baseline therefore declares the two operations on the service's own base and records the missing identifier as `GAP-1003` with the assumption `ASM-1792`. The service catalogue in Architecture v5 slide 42 fixes exactly two events for `rwb-document`, `DocumentStored` and `DocumentFieldsExtracted`, so a classification event is a third entry: the baseline declares it because the prompt of this key requires a classification fact, records the collision as the same gap row, and states in `ASM-1794` that the catalogue and the event count of RWB-P5-E2026-CON must be amended in the same change. Nothing else is guessed: the field-level names this key does not settle carry the placeholder `Not specified in the source documents (GAP-1003; ASM-1793)`. The two operations are tagged as baseline only after the architect confirms or renames them (GAP-1003), and the three resource field names are Not specified in the source documents (GAP-1003). The checked-fields read path and its shapes are Not specified in the source documents (GAP-1020); its field names are Not specified in the source documents (GAP-1020), and EXTRACT_ACCURACY_PASS stays in `document_hub_parameter`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope in binary mode, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.2 is in force for the document and intake-item reads whose shapes this baseline reuses: API-P5-003, API-P5-010, API-P5-011 and API-P5-013. TSD P5 T3.1 is in force for `document_intake`, `document_text` and `document_type`, and T3.2 for the LOV-INTAKE-REVIEW and LOV-DOC-TYPE value sets.
- The Ownership Map is the only source of owners: `document`, `document_intake`, `document_field` and `document_type` are P5's in `rwb_document`; `lov_value`, `reference_row` and `parameter_catalog` are P3's; the ACE views and `sys_fields` are P1's.
- The document type table version DOCTYPE-2026.11 carries the six agreed types with their English and Thai labels, and it is a P5 table: this baseline does not declare it as a consumed contract.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No approval of this baseline was available in this run, so it is carried as Status Draft (realignment v1) with the release 30 November 2026 unchanged and marked tentative (ASM-1788).

### 4. Flow

1. Draft the extension of the OpenAPI 3.1 document of `rwb-document` with the two classification operations, the three resources and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the classify command: the path with the intake item, the body `ClassificationRequest`, the `Idempotency-Key` header, the declared service identity, the 200 answer and the conflict and refusal statuses.
3. Fix the classification-state read: the path with the intake item, no request body, the 200 answer `ClassificationResult`, and the scope and masking rule of the Documents right R.
4. Fix the three resources field by field, with the required and optional sets of AC2 and AC3, so a consumer of the previous document keeps working when an optional property is added.
5. Fix the value sets as references, never as enumerations typed in the schema: the type codes from `document_type` in the version in force, the review reasons from LOV-INTAKE-REVIEW, the confidence scale and its four decimals.
6. Fix the threshold position: `CLASSIFY_THRESHOLD`, `CLASSIFY_MAX_PAGES` and `CLASSIFY_TIMEOUT_SECONDS` are read by the operation from the parameters contract, never declared as a property with a default.
7. Map every failure to the error envelope and a message ID, status by status, and carry the not-found message and the field-level names as gap and assumption rows.
8. Declare the `rwb.document.DocumentClassified.v1` schema with its six payload fields and its no-personal-data rule, and state the absence test for a text, candidate or content field.
9. Publish the six fakes, the contract tests and the drift test, tag the baseline, and hand it to RWB-P5-E1050-APP, RWB-P5-E1032-APP, RWB-P5-E1054-APP and the wave 1 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | The threshold, the page bound or the timeout appears as a schema default | The contract test fails: the three values are parameters of the operation, never defaults of the body | None | AC4 |
| X4 | A type code, a review reason or a confidence scale is typed into the schema as an enumeration | The contract test fails: the sets are read from the type table in force and from LOV-INTAKE-REVIEW | None | AC4 |
| X5 | An error is returned without a `messageId`, or with a status that is not the legacy one | The contract test fails on the status and the envelope map | None | AC5 |
| X6 | The event payload gains a seventh field, or carries text, candidates or content | The AsyncAPI schema test and the no-personal-data test fail | None | AC7 |
| X7 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, the Ownership Map and the service catalogue only |
| Negotiable | Pass | The field-level names and the two paths are settled with the consumers and the architect; the outcome set, the status mapping, the event schema and the idempotency rule are fixed by the legacy section 12 and section 14 |
| Valuable | Pass | Unblocks RWB-P5-E1050-APP, the attach and review readers and the wave 1 harness on Day 1 |
| Estimable | Pass | One document extension, two operations, three resources, nine contract tables and six fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the document classification API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the intake-item and document reads of TSD P5 T-A.2 and the intake tables of TSD P5 T3.1 are in force
    Given the document type table version "DOCTYPE-2026.11" with its six agreed types is loaded in rwb_document

  Scenario: AC1 The classify command and the classification-state read are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /api/recovery/document/v1/intake-items/{intakeItemId}/classify as owned by rwb-document, mapped to no API identifier because TSD P5 T-A carries none, and recorded in GAP-1003
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId}/classification as owned by rwb-document and as the classification-state read
    Then each operation declares its access right, the scope rule, the Idempotency-Key header rule and the statuses 200, 401, 403, 404, 409, 422 and 503
    Then the document states that the review list of API-P5-010 and the document read of API-P5-003 are declared by RWB-P5-E1054-APP and RWB-P5-E1024-APP and are only referenced here

  Scenario: AC2 ClassificationRequest fixes the required and optional fields and the page bound (new, D-RCV-60)
    Given the ClassificationRequest resource declared in the document
    When it is compared with the legacy section 12 adapter and section 13 configuration
    Then it carries intakeItemId as a uuid and required
    Then it carries pages as an integer between 1 and CLASSIFY_MAX_PAGES, whose seeded value is 3, and it is optional with the parameter value as its default at run time
    Then it carries typeCodes as an array of string with the minimum 1 and the maximum 6 of the version "DOCTYPE-2026.11", and it is optional
    Then it carries language as TH or EN with the default TH, and no other property is required
    Then it carries no threshold, no timeout and no model name, because those are read from the parameters contract and the configuration
    Then the header Idempotency-Key is required and carries the value "CLS-0501" in the example

  Scenario: AC3 ClassificationResult and TypeCandidate are fixed (new, D-RCV-60)
    Given the ClassificationResult and TypeCandidate resources declared in the document
    When they are compared with the legacy section 11 fields and section 12 published interface
    Then ClassificationResult carries intakeItemId, predictedType, confidence, candidates, classifierVersion, reviewReason, classifyFallback and classifiedAt
    Then predictedType is a type code of the version in force or absent, and confidence is a number from 0 to 1 with four decimals, so 0.62 is answered 0.6200
    Then candidates is a list of TypeCandidate with the code and the score, holds the top two agreed types and is ordered by score descending
    Then reviewReason is absent for a classified item and is one of LOW_CONFIDENCE, MODEL_UNAVAILABLE and UNKNOWN_TYPE for a held item
    Then classifyFallback is true only when the answer was MODEL_UNAVAILABLE
    Then the example answers COURT_NOTICE at 0.6200 with candidates COURT_NOTICE 0.62 and DEMAND_LETTER 0.21 and reason LOW_CONFIDENCE
    Then the example of a confident item answers APPRAISAL_REPORT at 0.80 with no reviewReason, and the example of an unknown type answers no predictedType with reason UNKNOWN_TYPE and the two highest agreed types as candidates

  Scenario: AC4 The type code set and the review reasons are references and the threshold is a parameter (new, D-RCV-60)
    Given the value sets and the parameter positions declared in the document
    When they are compared with the type table in force, LOV-INTAKE-REVIEW and the three legacy parameters
    Then the type codes are read from document_type in the version in force by valid_from and valid_to and are not enumerated in the schema
    Then the review reasons are read from LOV-INTAKE-REVIEW, whose classification values are LOW_CONFIDENCE, MODEL_UNAVAILABLE and UNKNOWN_TYPE, and RESCAN and UNREADABLE_FILE stay with the OCR story
    Then CLASSIFY_THRESHOLD, whose seeded value is 0.80, CLASSIFY_MAX_PAGES, whose seeded value is 3, and CLASSIFY_TIMEOUT_SECONDS, whose seeded value is 60, are parameters read through the rwb-case parameters contract and appear in no schema default
    Then the document records that the threshold comparison is inclusive and that 0.80 classifies while 0.85 under 0.90 does not
    Then the confidence is numeric(5,4) in rwb_document and the document states the four decimals of the stored field

  Scenario: AC5 The error envelope and the status mapping are fixed (new, D-RCV-60)
    Given the error responses declared for the two operations
    When each status is compared with the legacy section 5 exception paths and section 14
    Then 401 answers MSG-P4-001 and 403 answers MSG-P4-002 for a caller without the identity or the Documents right
    Then 404 answers the not-found message, whose identifier is Not specified in the source documents (GAP-1003; ASM-1793)
    Then 409 answers MSG-GEN-004 for two classify commands on the same item at the same time
    Then 422 answers MSG-GEN-001 for a blank identifier or a body that fails the schema
    Then 503 answers MSG-GEN-006 naming the parameters, the reference list or the masking service that failed, and no item is classified
    Then 200 answers the three held outcomes with MSG-P5-003 as the review-queue text the screen shows, never as an error of the command
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal writes no classification column and no event

  Scenario: AC6 The Idempotency-Key rule is fixed (new, D-RCV-60)
    Given the Idempotency-Key rule of the classify command
    When it is compared with the legacy section 12 idempotency key and BR7
    Then the header is required on the POST and a repeat with the same key answers the first stored ClassificationResult with 200
    Then a repeat creates no second classification, no second outbox row and no second DocumentClassified event
    Then a classify command on an item that already carries predictedType or reviewReason answers the stored result with 200 and makes no model call
    Then two commands with different keys on the same item at the same time answer one 200 and one 409 with MSG-GEN-004
    Then the GET declares no Idempotency-Key

  Scenario: AC7 The DocumentClassified event is a declared schema with no personal data (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline
    When it is compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.DocumentClassified.v1 is declared on the topic rwb.document.events.v1, keyed by caseId, with the six payload fields intakeId, caseId, predictedType, confidenceBand, reviewReason and classifiedAt
    Then the envelope is CloudEvents 1.0 in binary mode and the schema declares no OCR text, no masked text, no document content, no candidate list and no personal value
    Then the document states that the event is a third entry for rwb-document beside DocumentStored and DocumentFieldsExtracted, and records the collision in GAP-1003 with ASM-1794
    Then the absence test fails a build that adds a text, content or candidate field, and fails a build that declares a fourth event on this key without a catalogue change

  Scenario: AC8 The six fakes match the document and the drift test blocks a mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the six fakes of 12.8 answer the two operations of 12.1 and the two reads of 12.2 with the legacy values, including COURT_NOTICE 0.62, DEMAND_LETTER 0.21, APPRAISAL_REPORT 0.80, LOAN_CONTRACT 0.91, threshold 0.80 and timeout 60
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name, a required flag or an enum member
    Then the harness refuses a baseline tag while any of the six fakes and the document disagree

  Scenario: AC9 The contract rules of the baseline are declared and checked (new, D-RCV-60)
    Given the naming rule, the ownership rule and the compatibility rule of this baseline are in force
    When the document and its fakes are reviewed against them
    Then every operation, event and topic uses the base /api/recovery/document/v1 or the topic rwb.document.events.v1 with its retry and .dlt topics
    Then a change inside major version 1 is additive, and a removed, renamed or retyped property or a narrowed required set is declared a new major version
    Then the document declares only tables of rwb_document and only operations owned by rwb-document, and describes a consumed operation as consumed and faked
    Then every error uses one envelope and one message ID per condition, with the texts of section 14
    Then the document declares no case state, no document state machine, no rwb-agent operation and no model endpoint as a consumed contract

  Scenario: AC10 A status change the model does not allow is refused and writes nothing (new, D-RCV-60)
    Given an intake item whose classification state does not allow the requested status change
    When the change is requested through the classify command
    Then the command is refused with the error envelope of AC5
    Then no classification column is written and no DocumentClassified event is written
```

The ten criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1050-APP. The legacy AC1 to AC10 of RWB-E1-050 are owned by RWB-P5-E1050-APP, and the wave 1 harness RWB-ITG-W1 consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | The service naming rule of §R4; Template and Rules §R4; Architecture v5 slide 41 |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 11 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | The outcome set is closed: a classified item has no review reason, and a held item has exactly one of LOW_CONFIDENCE, MODEL_UNAVAILABLE and UNKNOWN_TYPE; RESCAN and UNREADABLE_FILE belong to the OCR story | TSD P5 T3.2 LOV-INTAKE-REVIEW; legacy sections 5 and 8 |
| BR6 | The type code set is the type table in force, never an enumeration of the schema; a code absent from the version is UNKNOWN_TYPE and not a validation error | DL19; principle 1; legacy BR3 |
| BR7 | The threshold, the page bound and the timeout are parameters read by the operation; no schema default and no example value is a business value; the rwb-case classification switch is one boolean parameter read by the handler, its key agreed with RW-COE, and the re-drive runs outside the case-creation and allocation windows; the key and the re-drive time of day are Not specified in the source documents (GAP-0766) | DP-06; legacy section 13; AC9 |
| BR8 | The threshold comparison is inclusive at or above, and the stored confidence is numeric(5,4), so the step and the read round the same way | Legacy BR2 and AC3; TSD P5 T3.1 DF-DOC-071 |
| BR9 | No personal data in a schema, an example or a fake: no OCR text, no masked text, no national ID number, no account number and no document content in any payload | CTL-11; DL26; Architecture v5 slide 11; legacy BR6 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E1-050 section 14 and the platform messages it inherits; the texts of MSG-GEN-004 and MSG-GEN-006 are read from the message catalogue at build time with the IDs unchanged, and the Thai text follows DL10 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer, so a repeat inside the window creates nothing; a GET declares none | Architecture v5 slide 11; DP-09; legacy BR7 |
| BR12 | The contract declares no case state and no document state machine; the intake-item outcome values are field values, and a transition belongs to RWB-P5-E1050-APP | Legacy section 9; RWB-P5-E1050-APP section 9 |
| BR13 | The classifier is an internal capability: the document declares no `rwb-agent` operation and no model endpoint as a consumed contract | GAP-1002; ASM-1789 |
| BR14 | A classified item writes its decision record as a local row in the decision-record table of the service schema created by the service baseline; no DecisionRecorded event is published and no platform dependency is claimed | GAP-0767; Ownership Map decision_log_entry owner P7 |

Open decisions that apply to this baseline: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863), DL19 (assumptions ASM-1051, ASM-1164, ASM-1809 and ASM-1810) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355). Each decision is still open, and this baseline rests on its listed assumptions until it closes.

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The two operations, the three resources and the nine sub-tables are described | In review |
| In review | Consumer sign-off | RWB-P5-E1050-APP, RWB-P5-E1032-APP, RWB-P5-E1054-APP and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | An optional property is added within major version 1, for example an optional `language` on the read | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a required set is narrowed, or an outcome value is retired | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The values it fixes are field values:

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `predictedType` = "COURT_NOTICE" | A type code present in the version of `document_type` in force; the other five codes of DOCTYPE-2026.11 are DEMAND_LETTER, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE |
| `confidence` = 0.6200 | The top score of the model, four decimals, the same scale as `document_intake.classification_confidence` numeric(5,4) |
| `candidates` = COURT_NOTICE 0.62, DEMAND_LETTER 0.21 | The top two scores, ordered descending, as the legacy AC2 shows them |
| `reviewReason` = "LOW_CONFIDENCE" | The top score is below the threshold; the item is held and the screen shows MSG-P5-003 |
| `reviewReason` = "MODEL_UNAVAILABLE" | No answer inside `CLASSIFY_TIMEOUT_SECONDS`; `classifyFallback` is true and `predictedType` is absent |
| `reviewReason` = "UNKNOWN_TYPE" | The model named a code outside the version in force; `predictedType` is absent and the candidates are the two highest agreed types |
| `classifyFallback` = false | The normal path; true only with MODEL_UNAVAILABLE |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI extension, the AsyncAPI fragment and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the two declared paths of `GAP-1003` and the third-event position of `ASM-1794` |
| Consuming teams (RWB-P5-E1050-APP, RWB-P5-E1032-APP, RWB-P5-E1054-APP and the wave 1 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |
| RW-RISK, risk and model risk officer | Confirms that the model version is a declared element of the answer and of the event, so an evaluation can name it |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1003; ASM-1793). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here. Each operation calls the rwb-access authorise check of DP-08; its operation name is Not specified in the source documents (DOR-RWB-P5-E1050-CON-6), and this document only references that check and declares none.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| ClassificationRequest | intakeItemId (uuid, required), pages (integer 1 to CLASSIFY_MAX_PAGES, optional), typeCodes (array of string, 1 to 6, optional), language (TH or EN, default TH) | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| ClassificationResult | intakeItemId, predictedType, confidence, candidates (array of TypeCandidate), classifierVersion, reviewReason, classifyFallback, classifiedAt | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| TypeCandidate | code, score; the top two agreed types, ordered by score descending | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Type code set | The six codes of `document_type` in the version in force, with their `label_en` and `label_th`; never enumerated in the schema | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Review reason set | LOV-INTAKE-REVIEW: RESCAN, UNREADABLE_FILE, LOW_CONFIDENCE, MODEL_UNAVAILABLE, UNKNOWN_TYPE; this API produces the last three | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Parameters | `CLASSIFY_THRESHOLD` 0.80, `CLASSIFY_MAX_PAGES` 3, `CLASSIFY_TIMEOUT_SECONDS` 60, read through the parameters contract and never a schema default | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Confidence scale | numeric(5,4) in `rwb_document`, answered with four decimals; the examples are 0.6200, 0.8000 and 0.9100 | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Idempotency record | The platform library row behind `Idempotency-Key`, in `rwb_document` | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Event schema | The six payload fields of `rwb.document.DocumentClassified.v1` and no seventh | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 | Not specified in the source documents (DOR-RWB-P5-E1050-CON-7) |

Every example in the document is synthetic and uses the legacy values: COURT_NOTICE 0.62, DEMAND_LETTER 0.21, APPRAISAL_REPORT 0.80, LOAN_CONTRACT 0.91, the threshold 0.80, the changed threshold 0.90, the page bound 3 and the timeout 60. Every field in the table above is classed as not personal data under BR9; the data steward's confirmation is Not specified in the source documents (DOR-RWB-P5-E1050-CON-11). No example carries a real customer value; the legacy values are examples only. The field-level names of `ClassificationRequest` and `ClassificationResult` beyond what the legacy section 11 names are Not specified in the source documents (GAP-1003; ASM-1793).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/intake-items/{intakeItemId}/classify` | None in TSD P5 T-A (recorded in GAP-1003) | Request `ClassificationRequest`; answer 200 `ClassificationResult` | Service identity SY-OCR; `Idempotency-Key` required | `Idempotency-Key` header, stored answer |
| GET | `/intake-items/{intakeItemId}/classification` | None in TSD P5 T-A (read of the same item as API-P5-011) | Answer 200 `ClassificationResult` | Documents R, scope applied, masking by role | Not applicable |

Error statuses 401, 403, 404, 409, 422 and 503 are those of section 14. The two paths are this baseline's because no source names a classification path: TSD P5 T-A.1 numbers API-P5-001 to API-P5-017 and none of them is a classify operation, while API-P5-011 reads the intake item, API-P5-012 its content, API-P5-013 its resolution and API-P5-014 the document review. The gap `GAP-1003` and the assumption `ASM-1792` carry the position; a rename before the baseline tag is additive to this document and changes no consumer code.

`GET /review-items` (API-P5-010) lists the held items with their two candidates and their reason, and `GET /documents/{documentId}` (API-P5-003) answers the stored document's type and confidence; both are declared by RWB-P5-E1054-APP and RWB-P5-E1024-APP, are referenced here, and are claimed by neither operation of this table.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `CLASSIFY_THRESHOLD`, `CLASSIFY_MAX_PAGES` and `CLASSIFY_TIMEOUT_SECONDS`, faked (C `RWB-P3-E1042-CON` through the platform client library) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-INTAKE-REVIEW, and LOV-DOC-TYPE faked with the same six codes as the type table, faked (C `RWB-P3-E1043-CON`) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a classification on a guessed value. The type table is not a consumed row: `document_type` is a P5 table in `rwb_document` and the operation reads it locally. The classifier and the PII masking service are not consumed REST contracts of this baseline: the classifier is internal and the masking service is the ACE common module's, both named in `ASM-1789`.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentClassified.v1` | `rwb.document.events.v1` | P5 rwb-document | Key caseId; payload intakeId, caseId, predictedType, confidenceBand, reviewReason, classifiedAt; CloudEvents 1.0 binary mode; no text, no masked text, no candidate list and no document content |

This baseline declares the schema because the service owns the topic; the outbox row itself is written by the classification step of RWB-P5-E1050-APP in its own transaction, and this key publishes nothing at run time. The service's other two events, `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, are declared in the same topic by the store and extraction stories and are named here only to fix the count: this baseline makes the count three and records the change in `GAP-1003` and `ASM-1794`. No decision record is declared, because the legacy story writes none: classification is a system step with no decision code of its own.

#### 12.4 Events consumed

None. The classify command is called by `DocumentIntakeWorkflow` and the read answers a screen; the baseline subscribes to no topic. `AgentRunCompleted` is not consumed, because the classifier is internal rather than an `rwb-agent` run (`GAP-1002`; `ASM-1789`).

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `classifyStep` | Activity contract | `rwb-document` | One typed activity with `ClassificationRequest` in and `ClassificationResult` out, idempotent per intake item; called by `DocumentIntakeWorkflow`, which RWB-P5-E1049-APP owns; the classify step runs as a child run of rwb-agent on the rwb-agent task queue (GAP-0363) |
| `evaluateClassifier` | Activity contract | `rwb-document` | The evaluation contract: the labeled sample in and the accuracy, the 6 by 6 confusion matrix and the model version out; started on demand, with no workflow declared here |

No workflow is declared by this baseline. `DocumentIntakeWorkflow` of the L3 workflow kit template "Document intake" is owned by RWB-P5-E1049-APP and only its classify step is named; the 15-minute Schedule that starts it is that story's.

#### 12.6 Schedules

None. This baseline declares no Schedule, no cron entry and no job name; the 15-minute document-intake Schedule and the retention Schedule belong to RWB-P5-E1049-APP and RWB-P5-E1017-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | The five classification columns and `review_reason` behind the `ClassificationResult`, with the keys of RWB-P5-E1050-APP section 11 |
| `document_type` | P5 (`rwb_document`) | Contracted use only: the type codes, the labels and the version in force behind the closed type set |
| `document_text` | P5 (`rwb_document`) | Contracted use only: the pages the request bound reads; no text is declared in any payload |
| `document` | P5 (`rwb_document`) | Contracted use only: the stored document's type and confidence that the read of API-P5-003 answers |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency row behind `Idempotency-Key` and the DocumentClassified envelope |

`lov_value`, `reference_row` and `parameter_catalog` are P3's, and the ACE views, `sys_fields` and `sys_objects` are P1's; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| parameters WireMock | `CLASSIFY_THRESHOLD` 0.80 and 0.90, `CLASSIFY_MAX_PAGES` 3, `CLASSIFY_TIMEOUT_SECONDS` 60, and a refusing read beyond 2 s | App story, contract tests, wave 1 harness |
| reference-data WireMock | LOV-INTAKE-REVIEW with its five values and LOV-DOC-TYPE with the six codes of DOCTYPE-2026.11 | App story, contract tests |
| classifier stub | COURT_NOTICE 0.62 and DEMAND_LETTER 0.21; APPRAISAL_REPORT 0.80; LOAN_CONTRACT 0.91; a model version string; and a stub that does not answer inside 60 seconds | App story, contract tests, wave 1 harness |
| PII masking stub | Tokens in place of the synthetic national ID number "0000000000000" and account number "TEST-ACC-0001" | Contract test of AC7's no-text rule and of the app story's AC10 |
| type-table fixture | DOCTYPE-2026.11 in force on a boundary date, a second version where a code is absent, and a version with a seventh type | Contract test of AC4 and of the closed set |
| intake-item fixture | An item with `ocr_status` DONE and no type; an upload item of type TITLE_DEED; an item in RESCAN; an item already classified | Contract test of AC6 and of the app story's skip cases |

A drifted fake fails the drift test of AC8. The exact response field names of the parameters and reference-data reads are Not specified in the source documents (GAP-1003; ASM-1793).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The classify command and the classification-state read; the parameters read and the list read of `rwb-case`; one hop and 2 s on every consumed call |
| Kafka | 1 event schema declared, 0 consumed | `rwb.document.DocumentClassified.v1` on `rwb.document.events.v1`; DocumentStored and DocumentFieldsExtracted belong to the other keys |
| Temporal | 2 activity contracts | `classifyStep` and `evaluateClassifier` on queue `rwb-document`; no workflow and no Schedule |
| File | None | This baseline carries no byte and no file reference; the evaluation report path is the app story's |

### 13. Solution plan

**Deliverables.** The extension of the OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the two operations and the three resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentClassified.v1`; the contract README rows for the value sets, the parameter positions, the error mapping, the idempotency rule and the event count; and the six WireMock mapping sets of section 12.8.

**Artefact and deployment values.** The classifier artefact is pinned by digest and promoted and rolled back as one (chart, artefact) pair with no schema change; promotion is gated on the evaluation report against the 90 percent target; the alert shares and windows, replica counts, KEDA thresholds, probe timings and the evaluation report container are values entries set at the SIT entry check, and no number is hard-coded (GAP-1004).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 is the reason the type table is read locally and not as a consumed contract, and the reason only `rwb_document` tables appear in 12.7. DP-06 and DP-07 are the reason the threshold and the reason set are positions in the contract and not enumeration members, which is what makes AC4 testable. DP-10 names the two activity contracts and leaves the workflow and its Schedule to the intake story, so the contract jar carries no cron. DP-11 fixes the two consumed reads to one hop with a 2 s timeout and a fake. DP-15 records the migration position for the five classification columns, and DP-19 records that the review-queue reads reach the screen through the composite route and never by a call chain.

**Build steps**

1. Write the two operations with their paths, resources, headers and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and AC3, and the 1 to `CLASSIFY_MAX_PAGES` and 1 to 6 bounds as schema constraints and README rows.
3. Fix the value sets of AC4 as references with their owners, and prove that no parameter and no type code is a schema default or an enumeration member.
4. Map every status and message ID of AC5 and record the RFC 9457 envelope, including the not-found placeholder.
5. Record the `Idempotency-Key` rule of AC6, the stored-answer behaviour and the two-command conflict.
6. Declare the `DocumentClassified` schema of AC7 with its six fields, the no-personal-data rule and the absence test for a seventh field.
7. Publish the six fakes and the contract tests, including the drift test; tag the baseline and collect the sign-off of RWB-P5-E1050-APP, RWB-P5-E1032-APP, RWB-P5-E1054-APP and the wave 1 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the six fakes answer the operations and reads of sections 12.1 and 12.2, the drift test is green, and the three consuming stories and RWB-ITG-W1 have accepted the baseline.

### 14. Validation and messages

| ID | Status | When | Message |
|---|---|---|---|
| MSG-P4-001 | 401 | No identity or an expired token | Not specified in the source documents (GAP-1003; ASM-1793) |
| MSG-P4-002 | 403 | The caller lacks the Documents right, or the scope excludes the case | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | 422 | A blank identifier or a body that fails the schema | Enter {field}. |
| MSG-GEN-004 | 409 | Two classify commands on the same item at the same time | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | 503 | The parameters, the reference list or the masking service does not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P5-003 | 200 | The item is held for type review | Some fields need checking. The document is in the review queue. |

The message IDs and the wording are contract elements copied unchanged from RWB-E1-050 section 14 and the platform messages it inherits; Thai text for each follows decision DL10. MSG-P5-003 is not an error: it is the text SCR-31 shows for a held item, and the command answers 200 with the `reviewReason` and the two candidates that put the item there.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-GEN-006 the {system} value is "Classification parameters", "Reference data" or "PII masking", fixed by the consumed row that failed. The not-found message of a 404 answer is Not specified in the source documents (GAP-1003; ASM-1793).

Screen states of SCR-31 are owned by RWB-P5-E1050-APP. The contract answers the no-access state with 403 and MSG-P4-002, and the error state with 503 and MSG-GEN-006. The empty and loading states are Not specified in the source documents (DOR-RWB-P5-E1050-CON-10).

### 15. Screens and states

SCR-31 Document review queue shows the held items with their two candidates, their reason and MSG-P5-003; the screen, its actions and its review form are RWB-P5-E1054-APP and reach the service through the gateway-bff composite route (DP-19), which calls the owner once and merges the answers into the screen model. This baseline fixes the answer shapes only and declares no screen field list and no route specification. SCR-31 states: no access and error, each answered by the contract (MSG-P4-002 and MSG-GEN-006, see section 14); loading and empty, each Not specified in the source documents (DOR-RWB-P5-E1050-CON-10). The reader states the baseline implies are the ones `ClassificationResult` carries: a confident item with a type and a confidence and no reason; a held item with a reason and two candidates; and a fallback item with the reason MODEL_UNAVAILABLE and `classifyFallback` true.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-11 | Access | Component | RW-CAPACITY user without the Documents right calls the classification-state read; refused with MSG-P4-002 |
| TC-E1-050-01 | AC1, BR7, BR8 | End to end | Labeled sample of 180 synthetic documents; the accuracy and the confusion matrix of the answer |
| TC-E1-050-02 | AC2, AC3, AC5 | End to end | Stub scores COURT_NOTICE 0.62, DEMAND_LETTER 0.21; the LOW_CONFIDENCE answer |
| TC-E1-050-03 | AC3, AC4, BR8 | End to end | Stub score APPRAISAL_REPORT 0.80; the inclusive threshold answer |
| TC-E1-050-04 | AC4, BR5 | End to end | Stub with no answer for 60 seconds; MODEL_UNAVAILABLE and classifyFallback true |
| TC-E1-050-05 | AC5, BR6 | End to end | Stub returns LOAN_CONTRACT 0.91; UNKNOWN_TYPE and the two highest agreed types |
| TC-E1-050-06 | AC2, AC6 | End to end | Upload of type TITLE_DEED; no classify call and no state change |
| TC-E1-050-07 | AC7 | End to end | Item in RESCAN; the read answers no classification |
| TC-E1-050-08 | AC8, BR11 | End to end | 20 classified items and a repeat command with the same Idempotency-Key |
| TC-E1-050-09 | AC9, BR7 | End to end | Parameter CLASSIFY_THRESHOLD changed to 0.90 with no schema change |
| TC-E1-050-10 | AC7, BR9 | End to end | Synthetic page with a national ID number and an account number; the event carries no text |
| TC-E1-050-12 | AC1 | Contract | Contract tests of the operations, events and activities of section 12 against the published yaml and catalog entries |
| TC-E1-050-13 | AC1 | Component | Boundary test of the tables of section 12.7 (ASM-3438) |
| TC-E1-050-14 | AC1 | Contract | OpenAPI 3.1 document of rwb-document validated against the OpenAPI 3.1 schema, with the two operations and their statuses 200, 401, 403, 404, 409, 422 and 503 |
| TC-E1-050-15 | AC9, BR1, BR2, BR3, BR4, BR10, BR12, BR13 | Contract | Contract lint of the document and its fakes against the naming, ownership, compatibility, envelope and no-state rules |
| TC-E1-050-16 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-P5-E1050-CON-AC12) |

This story owns no legacy acceptance criterion; the eleven legacy rows are the test cases of RWB-E1-050 with their IDs kept in legacy order; TC-E1-050-12 to TC-E1-050-15 are added by this story, and the Covers column names this story's own criteria, because the contract is what each case now exercises: the shapes, the value sets, the parameter positions, the envelope, the idempotency rule, the event schema and the fakes. The legacy level System maps to End to end and Access to Component; this story owns no Resilience case. The business outcome of each case is proven by RWB-P5-E1050-APP, and the wave 1 harness copies one of them as `TC-E1-050-01-ITG`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The classifier version is an opaque string, stored as rwb-document returns it with no format imposed by rwb-case; its format is Not specified in the source documents (GAP-0764), and every test uses a synthetic fixture whose ID is Not specified in the source documents (GAP-0764).

### 17. Guardrails

- No business value in the contract: the threshold, the page bound, the timeout, the type codes and the review reasons are parameters and reference rows of the app story, never a schema default or an enumeration member.
- No personal data in a schema, an example or a fake: no OCR text, no masked text, no national ID number, no account number and no document content in any answer; the synthetic values of AC2 and AC10 are examples only.
- No candidate list in the event: the event carries a confidence band and a reason, and the two candidates stay on the read that a reviewer with the Documents right calls.
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- The third event is declared with its catalogue consequence, not silently: a build that adds a fourth event fails the absence test.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no document state machine; the outcome values are field values and the transitions belong to the app story.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | The two operations, `ClassificationRequest`, `ClassificationResult`, `TypeCandidate`, the closed outcome set, the parameter positions, MSG-P5-003, the `DocumentClassified` schema | TC-E1-050-02, TC-E1-050-03, TC-E1-050-04, TC-E1-050-05, TC-E1-050-09, TC-E1-050-10, TC-E1-050-12, TC-E1-050-13 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the type table read locally; the two `rwb-case` reads consumed through the rwb-case login (DP-02) and faked |
| DP-06 | The parameters row of 12.2, the three parameter names and the no-default rule of AC4 |
| DP-07 | The reference-list row of 12.2, the review-reason set and its fake |
| DP-10 | The two activity contracts and the statement that the workflow and its Schedule belong to RWB-P5-E1049-APP |
| DP-11 | Both consumed rows with one hop, a 2 s timeout and a fake |
| DP-15 | The migration position recorded for the five classification columns |
| DP-19 | SCR-31 behind gateway-bff, and the screens story reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E1-050; its AC1 to AC10 are owned by RWB-P5-E1050-APP, the deployment is RWB-P5-E1050-OPS, and the cross-service proof of the same values is RWB-ITG-W1.

### 19. Out of scope

- The build of the classify step, the masking client, the evaluation runner and the classifier itself: RWB-P5-E1050-APP.
- The deployment, the model artefact pinning and promotion, the feature flag, the dashboards, the alerts and the runbook: RWB-P5-E1050-OPS.
- The intake pipeline, the OCR text and the 15-minute Schedule: RWB-P5-E1049-APP.
- The store, the attach path and the document read: RWB-P5-E1024-APP and RWB-P5-E1032-APP.
- The review queue screen, the resolve action and the correction fed back to the labeled set: RWB-P5-E1054-APP.
- Field extraction and its evaluation: RWB-P5-E1053-APP and RWB-P5-E1060-APP.
- The document type table and the load of DOCTYPE-2026.11: RWB-P5-E1025-APP.
- The model provider, the endpoint and the model version behind the internal classifier, and the `rwb-agent` satellite: `GAP-1002` and `ASM-1789`.
- The cross-service proof of these values: RWB-ITG-W1.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook: RWB-P5-E1050-OPS.
