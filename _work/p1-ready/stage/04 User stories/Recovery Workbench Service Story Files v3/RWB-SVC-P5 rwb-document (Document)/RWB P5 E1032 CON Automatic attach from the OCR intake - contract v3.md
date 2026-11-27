# RWB-P5-E1032-CON Automatic attach from the OCR intake

**Version 3 changes.**

- MSG-GEN-006 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1032-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P5-E1032-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1042-CON; RWB-P3-E1043-CON; two rwb-case case reads (case by number and open cases by account), faked; exact paths Not specified in the source documents (GAP-0992) |
| Shared platform baseline (wave 0; H stays empty) | RWB-PLT-E1027-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-TE006-CON; RWB-PLT-E1071-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON, held as the wave-0 shared baseline (GAP-3140) |
| Contract version | v1 on base `/api/recovery/document/v1`; baseline tag Not specified in the source documents (DOR-RWB-P5-E1032-CON-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-019, FR-P5-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the intake-match API of `rwb-document` is split out of legacy RWB-E1-032 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the four operations, the four shapes, the five match outcomes, the error envelope, the event schema, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1032-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 39 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the intake-match API of `rwb-document` — the list, read, content and resolve operations on base `/api/recovery/document/v1` with the `IntakeItem`, `IntakeItemPage`, `Document` and `IntakeAttachRequest` shapes, the five match outcomes and their status codes with the `match_status`, `review_status`, `candidate_case_ids` and classification fields, the error envelope with every message ID of section 14 and its HTTP status, the `Idempotency-Key` rule, the `rwb.document.DocumentAttached.v1` schema with no personal data, the decision-record position and the fakes with their drift test**, so that **the app story of this legacy key, the review screen, the store inside the same service and the wave 1 integration harness build against a fixed, testable contract on Day 1, and a renamed field, a different held-status list or an attach answered with the wrong status can never drift between two builds without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E1-032 carries its four endpoints in a section 12 of prose, with an in-process `CaseDirectory` and a `DocumentStore` interface beside them, and it leaves the consumer to infer the exact shapes. Under the target architecture the parts most likely to drift silently are exactly the ones this baseline fixes:

- a field renamed in `IntakeItem` or `IntakeItemPage`, so the Unmatched list on SCR-31 renders without its candidates or its OCR pages;
- a different list of held statuses in the query default, so an item in CONFLICT or NO_TYPE disappears from the reviewer's queue;
- `match_status` widened to the values of another list, so `rwb-case` and `rwb-agent`, which read the attach event, see a value they cannot interpret;
- an attach answered 200 where the legacy contract answers 201, or a concurrent attach answered 409 without `MSG-GEN-004`;
- a `version` that is not the optimistic lock, so two reviewers both attach the same item;
- the attach event changed, or a personal value put into it, so a consumer cannot read it and a data steward cannot approve it.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit - the P3 parameters contract `RWB-P3-E1042-CON` and the P3 reference-data contract `RWB-P3-E1043-CON` - and it records that the two `rwb-case` reads, the case by number and the open cases by account, are consumed and faked although the plan lists them in no C row (`ASM-1758`).

It also records the naming conflict the sources carry. The legacy story publishes `POST /intake-items/{intakeItemId}/attach` with the Documents right C and a `201 Document` answer; TSD P5 API-P5-013 names `POST /intake-items/{intakeItemId}/resolve` with the right U and an `IntakeResolution` answer; Arch v5 slide 42 lists two events for this service and neither is called `DocumentAttached`. The baseline declares the TSD path and the legacy answer shape, keeps the Documents right C on the chosen case, and records the losers as `GAP-0991` with `ASM-1755` and `ASM-1759`. Nothing else is guessed: the field-level names this key does not settle carry the placeholder `Not specified in the source documents (GAP-0992; ASM-1755)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-010, API-P5-011, API-P5-012 and API-P5-013, and TSD P5 T3.1 and T3.2 are in force for the `document`, `document_intake` and `document_text` definitions and the seven-value LOV-INTAKE-MATCH list.
- The Ownership Map is the only source of owners: `document`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; `decision_log_entry` is P7's; the ACE views are P1's.
- The classification and extraction baselines are published (RWB-P5-E1050-CON, RWB-P5-E1053-CON), so the fields `predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version`, `review_reason`, `case_no` and `account_no` have one owner document each.
- The store baseline of this service (RWB-P5-E1024-APP) is in force, so the `Document` answer of the resolve operation is the store's shape and not a second one.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7; `ASM-1753`), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 30 November 2026 is the legacy one and is tentative (`ASM-1756`), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (`ASM-1757`).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the four intake operations, the four resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the list operation: the `matchStatus` default of the five held values, `page`, `size` with its default 50, the oldest-first order and the scope filter that keeps only items whose candidates are in the caller's scope, plus the items with no candidate for scope ALL.
3. Fix the `IntakeItem` and `IntakeItemPage` shapes, so the screen reads one answer with the item, its OCR pages, its type candidates and its candidate cases, and the page carries its own paging fields.
4. Fix the `Document` and `IntakeAttachRequest` shapes, so the resolve operation answers exactly what the store returns and the optimistic lock travels in the request rather than in a header.
5. Fix the five match outcomes, their status values and the fields that carry them, together with the seven values of LOV-INTAKE-MATCH and the five values of LOV-INTAKE-REVIEW.
6. Map every failure to the error envelope and a message ID, status by status, and carry the naming conflict and the missing C row as a gap and an assumption.
7. Record the `Idempotency-Key` rule, the stored answer of a repeat and the `version` lock of the resolve operation.
8. Declare the event position: `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1` with its seven payload fields and no personal data, the record on `rwb.decision-record.v1`, and no third event of this key.
9. Publish the seven fakes, the drift test and the baseline tag, then hand the baseline to RWB-P5-E1032-APP, RWB-P5-E1026-APP, the store story and the wave 1 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | The list of held statuses differs between the query default and the coverage rule | The contract test fails: the default carries NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE and nothing else | None | AC4 |
| X4 | An outcome is answered with a status outside the declared set, or `match_status` carries a value outside LOV-INTAKE-MATCH | The contract test fails on the enum and on the status of the operation | None | AC4, AC5 |
| X5 | An error carries no `messageId`, or a message ID with the wrong status | The contract test fails on the error envelope and on the status mapping of section 14 | MSG-GEN-004 | AC5 |
| X6 | A repeat of the same `Idempotency-Key` creates a second document, or the `version` is not the lock | The contract test fails, and the concurrency case answers two 201 where it must answer one 201 and one 409 | MSG-GEN-004 | AC6 |
| X7 | The event payload changes, an eighth field is added, or a personal value appears in it | The AsyncAPI schema test and the no-personal-data test fail | None | AC7 |
| X8 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |

### 6. INVEST check

| Criterion | Result | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, the Ownership Map and the two P5 baselines only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operations, the held-status list, the status mapping, the event schema and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E1032-APP, the review screen and the wave 1 harness on Day 1 |
| Estimable | Pass | One document, four resources, four operations, four consumed rows, nine contract tables and seven fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the intake-match API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the intake item, text and document definitions of TSD P5 T3.1 and the operations API-P5-010 to API-P5-013 of TSD P5 T-A are in force
    Given the store baseline RWB-P5-E1024-APP is published with its Document shape

  Scenario: AC1 The four intake operations are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/intake-items as the Unmatched list and maps it to API-P5-010
    Then it declares GET /api/recovery/document/v1/intake-items/{intakeItemId} and GET /api/recovery/document/v1/intake-items/{intakeItemId}/content and maps them to API-P5-011 and API-P5-012
    Then it declares POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve and maps it to API-P5-013
    Then every operation carries the Documents area, its right, the scope rule and the statuses 200, 401, 403, 404, 409, 422 and 503 as section 14 fixes them
    Then the document states that the legacy path /intake-items/{intakeItemId}/attach is not declared and is recorded in GAP-0991
    Then no operation of another service's base is declared as provided

  Scenario: AC2 The IntakeItem and IntakeItemPage shapes are fixed (new, D-RCV-60)
    Given the IntakeItem and IntakeItemPage resources declared in the document
    When they are compared with the legacy section 12 answer and the TSD P5 T3.1 intake fields
    Then IntakeItem carries intakeItemId, source, receivedAt, matchStatus, predictedType, classificationConfidence, typeCandidates, candidateCases, pages, version and reviewReason
    Then candidateCases is an array of the case reference with caseId and caseNo, and pages is an array of pageNo and text
    Then IntakeItemPage carries items, page, size and total and lists the items oldest first
    Then the list query declares matchStatus with the five held values as its default, page and size with the default 50
    Then intakeItemId is a uuid and version is an integer, because the version is the optimistic lock of the resolve operation
    Then a page of text is returned only for a role whose masking rule allows it, and each read is declared as written to the access log
    Then the example carries intake item "II-2026-000123", source "SCAN" and matchStatus "MULTIPLE"

  Scenario: AC3 The Document shape and the IntakeAttachRequest are fixed (new, D-RCV-60)
    Given the Document and IntakeAttachRequest resources declared in the document
    When they are compared with the legacy section 12 request and the store answer
    Then IntakeAttachRequest carries caseId as a uuid and required, documentType as a string and required, and version as an integer and required
    Then the resolve operation answers 201 with the Document shape of the store, carrying documentId, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce and docVersion
    Then documentId, caseId, documentType, source and docVersion are required and every other property is optional, so a consumer of the previous version keeps working
    Then the request declares no approver field, because the approver is the authenticated caller
    Then the example carries caseId of case "RW-2026-000654", documentType "GUARANTOR_NOTICE" and version 3
    Then an empty caseId or an empty documentType answers 422 with MSG-GEN-001 naming the field

  Scenario: AC4 The five match outcomes, the status values and the match fields are fixed (new, D-RCV-60)
    Given the outcome and status declarations of the document
    When they are compared with the legacy exception paths X1 to X9 and the two lists of TSD P5 T3.2
    Then matchStatus carries the seven values of LOV-INTAKE-MATCH: PENDING, MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE
    Then the five outcomes of the matcher are NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE, and MATCHED is the decided value and PENDING the selected value
    Then an automatic attach answers MATCHED with the document ID and candidateCaseIds empty
    Then a held item answers its outcome with candidateCaseIds holding every candidate the matcher found
    Then reviewStatus carries the four values of LOV-REVIEW and reviewReason the five values of LOV-INTAKE-REVIEW
    Then the classification fields classificationConfidence and typeCandidates are declared on the item and on the stored document, with four decimal places on the confidence
    Then an outcome outside the seven values fails the schema and the contract test

  Scenario: AC5 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the four operations
    When each status is compared with the legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 for the right and MSG-P4-003 for a case outside the scope
    Then 404 answers the not-found message whose ID is Not specified in the source documents (GAP-0992; ASM-1755)
    Then 409 answers MSG-GEN-004 for an item no longer held or a changed version
    Then 422 answers MSG-P5-006 for a type not in force and MSG-GEN-001 for a missing field
    Then 503 answers MSG-P7-003 for a failed decision record and MSG-GEN-006 naming the system that failed
    Then MSG-P5-003 is declared as the label of a held item and of a document stored for review and not as an error response
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal returns no document

  Scenario: AC6 The Idempotency-Key rule and the optimistic lock are fixed (new, D-RCV-60)
    Given the Idempotency-Key rule of the resolve operation
    When it is compared with the legacy section 12 idempotency row and the concurrency criterion AC15
    Then the header is required on the POST and a repeat with the same key returns the first answer with 201 and creates no second document
    Then the stored answer is kept for the window the platform rule fixes; its exact length is Not specified in the source documents (GAP-0992; ASM-1755)
    Then version is required in the body and an item whose version changed answers 409 with MSG-GEN-004
    Then the three GET operations declare no Idempotency-Key and no side effect
    Then a repeat never writes a second decision record and never publishes a second event

  Scenario: AC7 The DocumentAttached event and the decision record are declared schemas (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline and the record declaration of the document
    When they are compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.DocumentAttached.v1 is declared on the topic rwb.document.events.v1 with its retry topics at 1 min, 10 min and 1 h and its .dlt topic
    Then the event is keyed by caseId and carries documentId, caseId, documentType, source, intakeItemId, matchMethod and attachedAt
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no personal value, no OCR text and no file byte
    Then the decision record is declared on rwb.decision-record.v1 with the decision code DOCATT, the match method and the classifier version
    Then the document states that the legacy DocumentStored (EV-16) is carried inside this event and that Arch v5 slide 42 names it DocumentStored, which is recorded in GAP-0991
    Then the document states that the store writes the event in its own transaction and that this baseline publishes nothing itself

  Scenario: AC8 The seven fakes answer the document and the drift test fails on any mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the seven fakes of 12.8 answer the four operations of 12.1 and the four reads of 12.2 with the values of the legacy examples, including case "RW-2026-000123", account "TEST-ACC-0002", the confidence 0.9300 and the threshold 0.80
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name or a required flag
    Then the absence test fails a build that declares a fourth intake operation or an event name outside rwb.document.<Event>.v1

  Scenario: AC16 The contract declares no case state and no document state machine (new, D-RCV-60)
    Given the enumerated fields of the document and the values each may take
    When the document is searched for a case state key and a document state machine key
    Then no case state key and no document state machine key is declared
    Then every enumerated field takes only the values declared on that field
    Then no transition between statuses is declared, because a transition belongs to RWB-P5-E1032-APP

  Scenario: AC17 A status change the model does not allow is refused (new, D-RCV-60)
    Given the resolve operation of the document and the 409 answer of AC5 and AC6
    When a resolve is sent for an item that is no longer held
    Then it answers 409 with MSG-GEN-004
    Then no document is stored
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E1032-APP. The legacy AC1 to AC15 are owned by RWB-P5-E1032-APP, and the wave 1 harness RWB-ITG-E1032-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Arch v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Arch v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | The event names of this service follow `rwb.document.<Event>.v1` on its own topic, and the baseline declares one event and one record and no third event | Arch v5 slides 16 and 42; DP-09; DP-14 |
| BR6 | No business value is fixed in the contract: the patterns, the threshold, the type list, the decision code, the review labels and the paging defaults are parameters, reference rows or document defaults | Template and Rules §R7.2 s17; RWB-E1-032 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, versions, confidences, dates and page text of synthetic documents only, and no customer name, address or national ID number in any payload | Arch v5 slide 11; RWB-E1-032 section 17 |
| BR8 | No OCR text and no file byte in the event or the decision record: the payload carries the item ID and the match method, and the text stays behind the read operation with masking and the access log | DP-09; RWB-E1-032 section 17 |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Arch v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E1-032 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer; a GET declares none; the resolve operation carries the optimistic lock in the body as `version` | Architecture v5 slide 11; DP-09; legacy AC15 |
| BR12 | The contract declares no case state and no document state machine beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E1-032 section 9; RWB-P5-E1032-APP owns the match transitions |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The four operations, the four resources, the four consumed rows and the event schema are described | In review |
| In review | Consumer sign-off | RWB-P5-E1032-APP, the review screen, the store owner and the wave 1 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `reviewReason` on the page item | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The intake item states PENDING, MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE are field values of `matchStatus`, and the transitions between them belong to RWB-P5-E1032-APP. The seven values are the whole of LOV-INTAKE-MATCH and the baseline declares all of them, including PENDING and MATCHED, so a consumer can read the field in every state (`ASM-1754`).

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `matchStatus` = "PENDING" | An item the matcher has not decided yet; the selected value of the next run |
| `matchStatus` = "MATCHED" | An item attached to exactly one case, automatically or by a person |
| `matchStatus` = "NO_MATCH" | No case and no account number resolved, or the case number does not exist |
| `matchStatus` = "MULTIPLE" | Two or more open cases for the account number |
| `matchStatus` = "CONFLICT" | The case number and the account number point to different cases |
| `matchStatus` = "CASE_CLOSED" | The only candidate is closed |
| `matchStatus` = "NO_TYPE" | Classification named no agreed type, or the model was unavailable |
| `reviewStatus` = "PENDING" | A stored document whose type a person must confirm; `write_once` is false |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment and the seven fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the resolution of `GAP-0991` |
| Consuming teams (RWB-P5-E1032-APP, the review screen, the store owner, the wave 1 harness) | Review and sign off the parts they consume |
| RW-LITOFF and RW-CASEOWN, the reviewer roles | Confirm that the list, the item read and the resolve answer carry what the review queue needs (Documents C on the chosen case) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-0992; ASM-1755). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here; the authorise check on the declared area and right is consumed from rwb-access (DP-08), and its operation name is Not specified in the source documents (DOR-RWB-P5-E1032-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| IntakeItem | intakeItemId (uuid), source (one of LOV-DOC-SOURCE), receivedAt, matchStatus (one of LOV-INTAKE-MATCH), predictedType, classificationConfidence (numeric(5,4)), typeCandidates, candidateCases (caseId, caseNo), pages (pageNo, text), reviewReason (one of LOV-INTAKE-REVIEW), version, from the `document_intake` fields DF-DOC-045 to DF-DOC-084 | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| IntakeItemPage | items (array of IntakeItem), page, size, total; the list is oldest first by receivedAt | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| Document | documentId, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion, from the `document` fields DF-DOC-001 to DF-DOC-011 and the store answer of RWB-P5-E1024-APP | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| IntakeAttachRequest | caseId (uuid, required), documentType (string, required), version (integer, required) | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| DocumentText page | pageNo (integer), text (string); read from `document_text` DF-DOC-088 and DF-DOC-089, masked by role | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| Match outcome set | MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED (the legacy five) with NO_TYPE and PENDING as the additional values of LOV-INTAKE-MATCH | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| DecisionRecord | decisionCode DOCATT, finalCall, inputsRef, decidedAt and the chain fields of the library; the match method and the classifier version are inputsRef content and not a copy of the text | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 | Not specified in the source documents (DOR-RWB-P5-E1032-CON-7) |

Every example in the document is synthetic and uses the legacy values: case "RW-2026-000123", account "TEST-ACC-0002", the confidence 0.9300 and 0.62, the threshold 0.80, the classifier version "CLS-1.0" and the decision code "DOCATT". No example carries a real customer value; the legacy values are examples only. Fields classed as personal data are `partyId` in `Document` and `text` in `pages` of `IntakeItem` and in `DocumentText`; they carry an identifier and masked page text read behind the read operation (BR7, BR8), and no field carries a name, address or national ID number. The field-level names of `IntakeItem`, `IntakeItemPage` and `IntakeAttachRequest` beyond the legacy list are Not specified in the source documents (GAP-0992; ASM-1755), and the baseline fixes them as the smallest superset of that list.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/intake-items` | API-P5-010 | 200 `IntakeItemPage`; query `matchStatus` default NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE, `page`, `size` 50, oldest first, scope applied | Documents R, scope applied | None |
| GET | `/intake-items/{intakeItemId}` | API-P5-011 | 200 `IntakeItem` with the OCR pages, masked by role; each read to the access log | Documents R, scope applied | None |
| GET | `/intake-items/{intakeItemId}/content` | API-P5-012 | 200 `application/octet-stream`, the file of the held item | Documents R, scope applied | None |
| POST | `/intake-items/{intakeItemId}/resolve` | API-P5-013 | Request `IntakeAttachRequest`; answer 201 `Document` | Documents C, scope applied to the chosen case | `Idempotency-Key` header plus the `version` lock |

Error statuses 401, 403, 404, 409, 422 and 503 are those of T-A.2 and section 14. The TSD path is declared; the legacy `POST /intake-items/{intakeItemId}/attach` is recorded as the loser of the conflict `GAP-0991` with the assumption `ASM-1755`, and it is declared nowhere in the document.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/by-no/{caseNo}` | P3 rwb-case | The case, its status and its owner for the match by case number; one hop, 2 s, faked; the contract is RWB-P3-E1018-CON and the plan lists it in no C row (`ASM-1758`) |
| GET | the open-cases-by-account read of rwb-case | P3 rwb-case | The open cases of an account number for the MULTIPLE outcome; same owner document; the path is Not specified in the source documents (GAP-0992; ASM-1758) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW (C `RWB-P3-E1043-CON`) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a held item answered as matched. The two case reads are consumed and faked and are named in no C row of the plan, so they carry `ASM-1758` and no row is added to the metadata C list.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentAttached.v1` | `rwb.document.events.v1` with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 rwb-document | Key caseId; payload documentId, caseId, documentType, source, intakeItemId, matchMethod, attachedAt; CloudEvents 1.0 binary mode; no personal data, no OCR text, no file byte |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | The hash-chained record with decision code DOCATT, the match method CASE_ID, ACCOUNT_NO or PERSON, the classifier version and the confidence, and `inputsRef` naming the intake item |

This baseline declares the event schema and the record declaration because the service owns the topic; the event row itself is written by the attach path of RWB-P5-E1032-APP inside the store transaction, and this key publishes nothing at run time. Arch v5 slide 42 lists `DocumentStored` and `DocumentFieldsExtracted` for this service and not the name above; the difference is recorded as `GAP-0991` with `ASM-1759`, and the event catalogue owner confirms the final name before the wave 1 release. No third event exists for this key.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This baseline consumes no event: the trigger is the intake Schedule, and the classification and extraction output arrives inside the same workflow |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `matchStep` | Activity contract | `rwb-document` | One typed activity interface with the intake item ID in and the outcome out, idempotent by the item ID; called by `DocumentIntakeWorkflow`; no workflow is declared here |
| `DocumentIntakeWorkflow` | Workflow, from the L3 "Document intake" template | `rwb-document` | Owned by RWB-P5-E1049-APP; this baseline names only the step it contributes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This baseline declares no Schedule and no cron entry; the Schedule is registered from the values of RWB-P5-E1032-OPS |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | The item, its statuses, its candidates and its version behind the four shapes |
| `document_text` | P5 (`rwb_document`) | The pages behind `IntakeItem.pages` and the content read |
| `document` | P5 (`rwb_document`) | The `Document` shape the resolve operation answers, written by the store |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the rows behind the three parameters |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record the attach writes |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency row behind `Idempotency-Key` and the event envelope objects |

`recovery_case`, `case_account`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `decision_log_entry` is P7's, `document_type` is P5's and is read through its own table; the ACE views are P1's and are named as consumed answers and never declared as this service's tables (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case WireMock | `GET /cases/by-no/{caseNo}` for case "RW-2026-000123" open with account "TEST-ACC-0001", case "RW-2026-000456" open with account "TEST-ACC-0002", case "RW-2026-000789" closed and no case for "RW-2026-999999"; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case open-cases WireMock | Account "TEST-ACC-0003" with two open cases, account "TEST-ACC-0002" with one, an account with none and an account whose only case is closed | App story, contract tests |
| parameters and reference-data WireMock | `CASE_NO_PATTERN` "RW-[0-9]{4}-[0-9]{6}", `ACCOUNT_NO_PATTERN` "[0-9]{10}", `CLASSIFY_THRESHOLD` 0.80; the five lists with the seven match statuses and the four review statuses | App story, contract tests |
| intake item fake | The four operations with an item in each held status, one MATCHED item and one page of synthetic OCR text in Thai and English | App story, review screen, contract tests |
| document store fake | The `Document` answer, the duplicate answer with the existing document ID, and the COPY_PENDING state | App story, contract tests |
| decision-record and central ledger fake | The local DOCATT record with match method CASE_ID, ACCOUNT_NO or PERSON and a ledger reference; a refusing write for TC-E1-032-17 | App story, contract tests, wave 1 harness |
| error envelope fake | One answer per message ID of section 14 with its status and its `detail` text | Contract tests, review screen |

A drifted fake fails the drift test of AC8. The exact response field names of the two case reads are Not specified in the source documents (GAP-0992; ASM-1758).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 4 consumed | The list, the item read, the content read and the resolve; the case by number, the open-cases read, the parameters read and the lists read; one hop and 2 s on every consumed call |
| Kafka | 1 event schema and 1 record declared, 0 consumed | `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1` and the record on `rwb.decision-record.v1` |
| Temporal | 1 activity contract, 1 workflow named | `matchStep` on queue `rwb-document`, called by `DocumentIntakeWorkflow`, which is owned by RWB-P5-E1049-APP; no Schedule |
| File | 1 reference and 1 read | `storageRef` points at the blob the store writes; the content read returns the file of the hold container `rwb-quarantine`; this baseline carries no byte |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the four intake operations and the four resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentAttached.v1` and the record declaration; the contract README rows for the outcome set, the error mapping, the idempotency rule and the event count; and the seven WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 is applied because every shape derives from a table of `rwb_document` and no other schema is declared. DP-03 is applied because the resolve operation's record is declared and faked here, although the row is written by the app story. DP-05 is applied by removal: the legacy ACE view read behind `CaseDirectory` is not part of the baseline and the account arrives inside the `rwb-case` answer. DP-06 and DP-07 are the two C rows: the three parameters and the five lists are read through the `rwb-case` contracts and never typed into the document. DP-09 fixes the topic, the envelope and the `Idempotency-Key` rule. DP-10 names the `matchStep` activity contract and the workflow that calls it, without declaring a Schedule. DP-11 fixes the four consumed rows to one hop with 2 s and a fake each. DP-15 records that the three tables behind the shapes belong to this service's own migration sequence. DP-19 records that the list and the item read are reached through the gateway-bff composite route; this baseline fixes the answer shapes only and no route specification.

**Build steps**

1. Write the four operations with their paths, queries, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and AC3 and the paging default as schema constraints and README rows.
3. Declare the outcome set and the four status and list fields of AC4, with the seven values of LOV-INTAKE-MATCH as an enum.
4. Map every status and message ID of AC5 and record the RFC 9457 envelope, including the not-found placeholder.
5. Record the `Idempotency-Key` rule and the `version` lock of AC6.
6. Declare the event and the record of AC7, with the no-personal-data test and the absence test for a fourth operation and a foreign event name.
7. Publish the seven fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E1032-APP, the review screen and the wave 1 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the seven fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E1032-APP and RWB-ITG-E1032-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-003 | Item held for a person or document stored for review (a label, not an error) | Some fields need checking. The document is in the review queue. | 200 |
| MSG-P5-006 | Reviewer picks a type not in force | {value} is not a document type in force. Choose a type from the list. | 422 |
| MSG-GEN-001 | Case or type missing on attach, or a response body that fails validation | Enter {field}. | 422 |
| MSG-GEN-004 | Item attached by someone else, or a changed version | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Chosen case outside the scope | This case is not in your scope. | 403 |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-0992; ASM-1755) | 401 |
| MSG-GEN-006 | The case read failed or timed out | {system} is not available. Try again in a few minutes. | 503 |
| not-found message | An intake item or a document that does not exist | Not specified in the source documents (GAP-0992; ASM-1755) | 404 |

The message IDs and the wording are contract elements copied unchanged from RWB-E1-032 section 14; Thai text for each follows decision DL10. Decision DL10 is open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863. MSG-P4-001, MSG-GEN-006 and the not-found message are named by the target error envelope and are copied from the platform set, and their exact texts are recorded as the placeholder above.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one plus the two platform rows: 401 with MSG-P4-001, 403 with MSG-P4-002 or MSG-P4-003, 404 with the not-found message, 409 with MSG-GEN-004, 422 with MSG-P5-006 or MSG-GEN-001, and 503 with MSG-P7-003 or MSG-GEN-006. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed, and it is "Case service" for both `rwb-case` reads.

Screen states of SCR-31 (the review screen behind gateway-bff, DP-19): empty is a 200 IntakeItemPage with an empty items array; error is 503 with MSG-GEN-006; no access is 403 with MSG-P4-002; loading is the pending request and has no answer in this contract.

### 15. Screens and states

SCR-31 Document review queue is the screen these operations serve, reached through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; the screen itself and its attach dialog are RWB-P5-E1032-APP and the case document list is RWB-P5-E1026-APP. This baseline fixes the answer shapes only and declares no screen field list and no route specification. The states its shapes imply are: an item in each of the seven match statuses, a page of OCR text masked by role, a candidate list of one or more cases, and a held item that no longer exists when a second reviewer resolves it. Empty, error and no-access states are the answers of section 14 (200 with an empty items array, 503 with MSG-GEN-006, 403 with MSG-P4-002). Loading state: as Screen Specifications v1 section SCR-31 states it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1032-CON-01 | AC1, BR1, BR4 | Contract | The OpenAPI 3.1 document validates; the four operations and their statuses are declared; no foreign base is provided |
| TC-P5-E1032-CON-02 | AC2, BR3 | Contract | An item in each held status and one page of synthetic Thai and English text; a renamed field fails the lint |
| TC-P5-E1032-CON-03 | AC3, BR6 | Contract | The resolve request with case "RW-2026-000654", type "GUARANTOR_NOTICE" and version 3; an empty field answers 422 |
| TC-P5-E1032-CON-04 | AC4, BR5 | Contract | The seven match statuses and the four review statuses; a value outside the enum fails the schema |
| TC-P5-E1032-CON-05 | AC5, BR10 | Contract | One answer per message ID of section 14 with its status; a missing `messageId` fails the test |
| TC-P5-E1032-CON-06 | AC6, BR11 | Contract | The same `Idempotency-Key` twice, and two parallel resolves at version 3 |
| TC-P5-E1032-CON-07 | AC7, BR7, BR8 | Contract | The AsyncAPI fragment; a sixth field added to the payload fails the test; a personal value in the payload fails the no-personal-data test |
| TC-P5-E1032-CON-08 | AC8, BR2, BR9 | Contract | The seven fakes run against the document; a drifted path, status, field name or required flag fails the drift test |
| TC-P5-E1032-CON-09 | BR4 | Contract | Boundary of the six tables of section 12.7: each is accepted at its boundary; a table of P3, P7 or the ACE views is rejected by the contract check |
| TC-P5-E1032-CON-10 | BR12 | Contract | The field values are the only values declared; a case state or document state machine key fails the contract check |
| TC-P5-E1032-CON-11 | AC16, BR12 | Contract | A transition between two statuses declared in the contract fails the contract check |
| TC-P5-E1032-CON-12 | AC17, BR12 | Contract | A resolve for an item no longer held answers 409 with MSG-GEN-004 and no document |
| TC-E1-032-17 | X13, BR5 (legacy Principle 5) | Contract | The decision-record fake refuses the write; the resolve answers 503 with MSG-P7-003 and no document |
| TC-E1-032-16 | X14, BR7 (legacy Access) | Contract | A caller with Documents R only calls the resolve; refused with 403 and MSG-P4-002 |
| TC-E1-032-01 | AC1, BR1, BR5 | Contract | Notice with RW-2026-000123 at 0.93 answered with matchStatus MATCHED and the document ID |
| TC-E1-032-02 | AC2, BR3 | Contract | An item with no identifiers answered with matchStatus NO_MATCH and its pages |
| TC-E1-032-03 | AC3, BR3 | Contract | Account TEST-ACC-0003 on two open cases answered with MULTIPLE and both candidates |
| TC-E1-032-04 | AC4, BR2 | Contract | Account TEST-ACC-0002 only, answered with MATCHED and one candidate |
| TC-E1-032-05 | AC5, BR3 | Contract | Case ID and account on different cases answered with CONFLICT and two candidates |
| TC-E1-032-06 | AC6, BR3 | Contract | Case ID RW-2026-999999 answered with NO_MATCH and no candidate |
| TC-E1-032-07 | AC7, BR3 | Contract | Closed case RW-2026-000789 answered with CASE_CLOSED and one candidate |
| TC-E1-032-08 | AC8, BR6 | Contract | Two items with the same hash answered with one document ID |
| TC-E1-032-09 | AC9, BR6 | Contract; run by RWB-P5-E1032-APP | A list of 15 MATCHED items returns no item to the held default |
| TC-E1-032-10 | AC10, BR4 | Contract; run by RWB-P5-E1032-APP | A document at 0.62 answered with reviewStatus PENDING and writeOnce false |
| TC-E1-032-11 | AC11, BR3 | Contract; run by RWB-P5-E1032-APP | An item with review_reason UNKNOWN_TYPE answered with NO_TYPE |
| TC-E1-032-12 | AC12, BR5 | Contract; run by RWB-P5-E1032-APP | A resolve of a MULTIPLE item answers 201 with the Document and the approver taken from the caller |
| TC-E1-032-13 | AC13, BR7 | Contract; run by RWB-P5-E1032-APP | A resolve on a case outside the scope answers 403 with MSG-P4-003 |
| TC-E1-032-14 | AC14 | Contract; run by RWB-P5-E1032-APP | A resolve with type PAYSLIP answers 422 with MSG-P5-006 naming the value |
| TC-E1-032-15 | AC15 | Contract; run by RWB-P5-E1032-APP | Two parallel resolves at version 3 answer one 201 and one 409 with MSG-GEN-004 |

The seventeen legacy test cases of RWB-E1-032 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E1032-APP. TC-E1-032-16 keeps the legacy level Access and maps to Component in the app story and to Contract here, TC-E1-032-17 keeps the legacy level Resilience and maps to NFR in the app story and to Contract here, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copies end in `-ITG` and belong to RWB-ITG-E1032-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the patterns, the threshold, the type list, the decision code, the review labels and the paging default stay parameters, reference rows or document defaults of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, confidences and dates only, and the page text of a synthetic document only.
- No OCR text and no file byte in the event or the decision record: the payload carries the item ID and the match method, and the text stays behind the read operation with masking and the access log.
- The two `rwb-case` reads are consumed and faked and never declared as provided; the parameters and the lists arrive through their client libraries (DP-06, DP-07).
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view and no cross-schema join (DP-05).
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; a foreign base or a foreign table fails the review (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- The event name carries the service short and the topic is the service's own; the difference from the catalogued DocumentStored is recorded in `GAP-0991` and never hidden (DP-14).
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no intake state machine; a transition belongs to RWB-P5-E1032-APP.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | The resolve operation, the outcome set, the `matchStatus` field and the `DocumentAttached` schema | TC-P5-E1032-CON-01, TC-P5-E1032-CON-04, TC-E1-032-01, TC-E1-032-04 |
| REQ-DCM-005 | An uncertain match is held for a person | The five held outcomes, the list default and the `candidateCaseIds` field | TC-P5-E1032-CON-02, TC-P5-E1032-CON-04, TC-E1-032-02 to TC-E1-032-07 |
| REQ-DRI-004 | Every decision is recorded before it takes effect | The DOCATT record declaration, MSG-P7-003 and its 503 | TC-P5-E1032-CON-07, TC-E1-032-17 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the case reads consumed and faked |
| DP-03 | The decision record declaration of 12.3 and the ledger fake |
| DP-05 | The removal of the ACE view read behind `CaseDirectory` |
| DP-06 | The parameters row of 12.2 and the three parameter names |
| DP-07 | The reference-list row of 12.2 and the five lists |
| DP-09 | The `Idempotency-Key` rule, the event schema and the CloudEvents envelope |
| DP-10 | The `matchStep` activity contract and the workflow that calls it |
| DP-11 | All four consumed rows with one hop, a 2 s timeout and a fake |
| DP-15 | The migration position recorded for the three tables |
| DP-19 | SCR-31 behind gateway-bff, and the review screen reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E1-032; its AC1 to AC15 are owned by RWB-P5-E1032-APP, and the cross-service proof of the same values is RWB-ITG-E1032-ITG.

### 19. Out of scope

- The build of the matcher, the activity, the two attach services, the four operations and the Unmatched tab: RWB-P5-E1032-APP.
- The store, the write-once container and the version history: RWB-P5-E1024-APP.
- OCR, classification and field extraction: RWB-P5-E1049-APP, RWB-P5-E1050-APP and RWB-P5-E1053-APP.
- The review of a stored document's type and fields: RWB-P5-E1054-APP.
- The compute, the storage, the topic and the ACL provisioning: RWB-P5-E1032-INF.
- The chart, the Schedule registration, the dashboards, the alerts and the runbook: RWB-P5-E1032-OPS.
- The parameters and reference-data catalogues themselves and their admin operations: P3 rwb-case.
- The cross-service proof of these values: RWB-ITG-E1032-ITG.
