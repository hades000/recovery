# RWB-P5-E2017-CON Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the generation-screens API of `rwb-document` is split out of legacy RWB-E2-017 and published on base `/api/recovery/document/v1` with the two screen reads, the regenerate and send operations, the three signature-request operations `rwb-comms` calls, the shapes, the state values, the error envelope, the decision-record declaration, the fakes and the drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the generation-screens API of `rwb-document` — the set read and the merge-value read of the two screens, the regenerate operation API-P5-017, the send operation, the three signature-request operations `rwb-comms` calls, with the `GeneratedDocumentSetPage`, `MergeValuePage`, `RegenerateRequest`, `SendForSignatureRequest`, `Document` and `SignatureRequest` shapes, the three document state values and the write-once switch, the error envelope with every message ID of section 14 and its status, the `Idempotency-Key` rule, the `rwb.decision-record.DecisionRecorded.v1` declaration with no personal data, the fakes and their drift test**, so that **the app story of this legacy key, the generation engine, the review operation, `rwb-comms` and the wave 2 integration harness build against a fixed, testable contract on Day 1, and a renamed field, a different state value, a send answered with the wrong status or a second `rwb.document` event can never drift between two builds without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E2-017 carries its four endpoints in a section 12 of prose beside an in-process `SignatureRequests` interface and a `DocumentGenerator` call, and it adds a fifth endpoint in its section 13 without a definition. Under the target architecture the parts most likely to drift silently are exactly the ones this baseline fixes:

- a field renamed in the set read or the merge-value read, so SCR-14 shows a set without its template versions or SCR-30 shows merge values without the locked flag;
- a document state value widened or reworded, so the send check of BR6 and the read-only state of SCR-30 disagree;
- a regenerate answered 201 where the legacy contract answers 200, or a send answered 200 where the caller expects a page of sent documents;
- a `version` that is not the optimistic lock, so two officers both correct the same draft;
- a send that creates a second signature request, so one treatment carries two requests;
- a decision record or an event changed, or a personal value put into it, so a consumer cannot read it and a data steward cannot approve it.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependency of the app story explicit - the P3 reference-data contract `RWB-P3-E1043-CON` - and it records that the P6 catalog, the S2 treatment, the P3 case, the P7 ledger and the P6 signature operations are consumed and faked although the plan lists none of them in a C row (`ASM-1869`).

It also records the naming conflicts the sources carry. The legacy section 13 names `POST /cases/{caseId}/generated-documents/send` and the legacy section 12 names `POST /treatments/{treatmentId}/signature-requests`; in the target the first is this key's send operation and the second is `rwb-comms`'s API-P6-009, which this key consumes (`ASM-1870`). The legacy flow has no endpoint for the set or for the merge values at all, so the two screen reads are fixed by this baseline and not copied from a source (`ASM-1869`). Nothing else is guessed: the field-level names this key does not settle carry the placeholder `Not specified in the source documents (GAP-1017; ASM-1876)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-017, and TSD P5 T3.1 and T3.2 are in force for the `document` and `document_type` definitions and the lists of section 11.
- TSD P6 T3.1 is in force for `signature_request` (DF-DOC-096 to DF-DOC-107) and T3.2 for LOV-SIGN-METHOD and LOV-SIGN-STATUS.
- The Ownership Map is the only source of owners: `document`, `document_type`, `signature_request`, `document_hub_parameter` and `document_field` are P5's in `rwb_document`; `template` and `merge_field` are P6's in `rwb_comms`; `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; `treatment` is S2's; `decision_log_entry` is P7's; the ACE views are P1's.
- The generation baseline RWB-P5-E2026-CON and the review baseline RWB-P5-E1054-CON are published, so the `GenerateRequest` and `GenerationResult` of the engine and the `Document` answer of the review operation have one owner document each.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7; `ASM-1874`), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 31 December 2026 is the legacy one and is tentative (`ASM-1876`), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (`ASM-1876`).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the seven operations, the shapes of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the two screen reads: the set read with its `treatmentId` and `state` filters and the merge-value read with the locked flag, the format and the masked value.
3. Fix the regenerate operation API-P5-017: the `overrides` array with its 1 to 10 bound, the `version` lock, the 200 answer and the new `doc_version`.
4. Fix the send operation: the request with `treatmentId` and `documentIds`, the header `Idempotency-Key`, the 200 `DocumentPage` answer and the state SENT with `writeOnce` true.
5. Fix the three signature-request operations `rwb-comms` calls, with their status, their `SignatureRequest` shape and their service-identity access.
6. Fix the three document state values, the write-once switch and the `reviewStatus` values, and state that no list enumerates the states.
7. Map every failure to the error envelope and a message ID, status by status, and carry the missing C rows as a gap and an assumption.
8. Record the `Idempotency-Key` rule and the first-answer behaviour of a repeat, with the 24-hour window named as a parameter and not as a number.
9. Declare the record on `rwb.decision-record.v1`, state that no new `rwb.document.*` event exists, and publish the ten fakes, the drift test and the baseline tag; hand the baseline to RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P5-E1054-APP, `rwb-comms` and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | A document state value outside the three declared values is written or answered | The contract test fails on the enum and on the state check of the send | None | AC4 |
| X4 | The merge-value answer hides or drops the locked flag, or a locked field is answered as editable | The contract test fails: every value carries `locked` and a locked field can never be overridden | MSG-P5-014 | AC2, AC5 |
| X5 | An error carries no `messageId`, or a message ID with the wrong status | The contract test fails on the error envelope and on the status mapping of section 14 | MSG-GEN-004 | AC5 |
| X6 | A repeat of the same `Idempotency-Key` creates a second signature request, or the `version` is not the lock | The contract test fails, and the concurrency case answers two 200 where it must answer one change and one 409 | MSG-GEN-004 | AC6 |
| X7 | A new `rwb.document.*` event appears, or a personal value appears in the record | The AsyncAPI schema test and the absence test fail | None | AC7 |
| X8 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A and T3, TSD P6 T3, the Ownership Map and the two in-service baselines only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operations, the state values, the status mapping, the record declaration and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E2017-APP, the screens, `rwb-comms` and the wave 2 harness on Day 1 |
| Estimable | Pass | One document, seven operations, the shapes of section 11, ten consumed rows, nine contract tables and ten fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the generation-screens API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document and document_type definitions of TSD P5 T3.1, the lists of TSD P5 T3.2 and the signature_request definition of TSD P6 T3.1 are in force
    Given the generation baseline RWB-P5-E2026-CON and the review baseline RWB-P5-E1054-CON are published with their fakes

  Scenario: AC1 The seven operations are declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/cases/{caseId}/generated-documents as the set read of SCR-14
    Then it declares GET /api/recovery/document/v1/documents/{documentId}/merge-values as the review read of SCR-30
    Then it declares POST /api/recovery/document/v1/documents/{documentId}/regenerate and maps it to API-P5-017
    Then it declares POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send as the send, with no API ID in TSD P5 T-A.1
    Then it declares the three signature-request operations rwb-comms calls and marks them service identity only
    Then every operation carries the Documents area, its right, the scope rule and the statuses 200 or 201, 401, 403, 404, 409, 422 and 503 as section 14 fixes them
    Then the document states that the legacy P5 path /treatments/{treatmentId}/signature-requests is rwb-comms's provided operation API-P6-009 and is consumed by this key, recorded in GAP-1017
    Then no operation of another service's base is declared as provided

  Scenario: AC2 The set and merge-value shapes are fixed (new, D-RCV-60)
    Given the GeneratedDocumentSetPage, GeneratedDocumentSummary and MergeValuePage resources declared in the document
    When they are compared with the legacy flow of section 4 of the story
    Then GeneratedDocumentSetPage carries items, page, size and total, and each item carries documentId, treatmentId, documentType, templateCode, templateVersion, state, writeOnce, docVersion and reviewStatus
    Then the set query declares treatmentId and state, and state takes only the three declared values
    Then MergeValuePage carries documentId, docVersion, templateCode, templateVersion, state, writeOnce and values
    Then each value carries mergeCode, label, value, formattedValue, locked and reason, and locked is required on every value
    Then a page of a masked value is returned only for a role whose masking rule allows it, and each read is declared as written to the access log
    Then the example carries case "RW-2026-000401", treatment "TRT-0401", the document "DOC-0411" at doc_version 1 and the merge code contract_date with the value "2026-12-10"

  Scenario: AC3 The regenerate and send requests and answers are fixed (new, D-RCV-60)
    Given the RegenerateRequest, SendForSignatureRequest, Document and DocumentPage resources declared in the document
    When they are compared with legacy section 12 and section 13 and with the Document shape of the engine
    Then RegenerateRequest carries overrides as an array of mergeField, value and reason with the minimum 1 and the maximum 10, and version as an integer and required
    Then the regenerate operation answers 200 with the Document of the store, carrying documentId, caseId, documentType, source, storageRef, retentionClass, writeOnce, docVersion, templateCode, templateVersion, treatmentId, state and reviewStatus
    Then SendForSignatureRequest carries treatmentId as a uuid and required, documentIds as an array of uuid and required, and no approver field
    Then the send operation answers 200 with DocumentPage holding the sent documents, and each document carries state SENT and writeOnce true
    Then documentId, caseId, documentType, source and docVersion are required and every other property is optional, so a consumer of the previous version keeps working
    Then the header Idempotency-Key is required on the regenerate, the send and the three signature-request operations, and carries "S-0401" in the send example
    Then an empty reason answers 422 with MSG-GEN-001 naming Reason and an empty documentIds answers 422 with MSG-GEN-001

  Scenario: AC4 The three state values, the write-once switch and the signature shapes are fixed (new, D-RCV-60)
    Given the state, reviewStatus and writeOnce declarations of the document
    When they are compared with the legacy section 9 transitions and TSD P5 T3.2 and TSD P6 T3.2
    Then state carries exactly DRAFT, REVIEWED and SENT, and the document states that no list enumerates these three values
    Then reviewStatus carries the four values of LOV-REVIEW and writeOnce is false for a DRAFT and true for a SENT document
    Then SignatureRequest carries id, caseId, treatmentId, documentId, partyId, method, status, externalRef, sentAt, signedAt, signedDocumentId and expiresAt
    Then method carries the three values of LOV-SIGN-METHOD and status the five values of LOV-SIGN-STATUS
    Then the document states that SENT, SIGNED, DECLINED and EXPIRED of a request are written by rwb-comms and that this baseline declares the values only
    Then a state value outside the three answers fails the schema and the contract test

  Scenario: AC5 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the seven operations
    When each status is compared with legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 for the right and MSG-P4-003 for a document or a treatment outside the scope
    Then 404 answers the not-found message whose ID is Not specified in the source documents (GAP-1017; ASM-1876)
    Then 409 answers MSG-P5-002 for a sent document, MSG-P5-011 for a treatment that is not approved and MSG-GEN-004 for a changed version
    Then 422 answers MSG-GEN-001 for an empty reason, MSG-P5-013 for a document not reviewed or on an old template version, and MSG-P5-014 for a locked field
    Then 503 answers MSG-P7-003 for a failed decision record and MSG-GEN-006 naming the system that failed, and its value is "e-signature" for a refused signature request
    Then MSG-P5-012 is declared as the confirmation of a completed send and not as an error response
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal returns no document change

  Scenario: AC6 The Idempotency-Key rule and the optimistic lock are fixed (new, D-RCV-60)
    Given the Idempotency-Key rule of the regenerate, the send and the three signature-request operations
    When it is compared with legacy section 12 and the criteria AC10 and AC11
    Then the header is required on every POST and PATCH and a repeat with the same key returns the first answer and creates no second version, no second request and no second record
    Then the stored answer is kept for the window the parameter GEN_IDEMPOTENCY_HOURS fixes; its value is a parameter and never a number in the document
    Then version is required in RegenerateRequest and a document whose version changed answers 409 with MSG-GEN-004
    Then a send whose set already holds a request for the treatment answers the first result and starts no second request
    Then the two GET operations declare no Idempotency-Key and no side effect

  Scenario: AC7 The decision record is declared and no new rwb.document event exists (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline and the record declaration of the document
    When they are compared with the service catalogue and Architecture v5 slide 42
    Then the decision record is declared on rwb.decision-record.v1 with decision code D6.4, the final call the legacy criteria name and the inputs reference of an override
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no merge value, no personal value and no file byte
    Then the document states that only rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1 exist for rwb-document and that this key declares neither
    Then the absence test fails a build that adds a third rwb.document event or a renamed record
    Then the document states that the record is written by the app story inside its transaction and that this key publishes nothing itself

  Scenario: AC8 The ten fakes answer the document and the drift test fails on any mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the ten fakes of 12.8 answer the seven operations of 12.1 and the ten reads of 12.2 with the values of the legacy examples, including case "RW-2026-000401", treatment "TRT-0401", the document "DOC-0411", the key "S-0401" and the template "DIL-CONTRACT" version 2
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name or a required flag
    Then the absence test fails a build that declares an eighth operation, a foreign base or a foreign event name
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E2017-APP. The legacy AC1 to AC13 are owned by RWB-P5-E2017-APP, and the wave 2 harness RWB-ITG-E2017-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-13; Template and Rules §R4; Architecture v5 slide 41 notes |
| BR2 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR3 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR4 | This key publishes no event of its own: the service has exactly `DocumentStored` and `DocumentFieldsExtracted`, and the state change of this key is read back through the contract | Architecture v5 slides 16 and 42 |
| BR5 | No business value is fixed in the contract: the template set, the merge codes, the locked flag, the type mapping, the decision code, the parameter window and the paging default stay data rows, catalog properties or parameters of the app story | Template and Rules §R7.2 s17; RWB-E2-017 section 17 |
| BR6 | No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and amounts only, and no customer name, address, national ID number, merge value or file byte in any payload | Architecture v5 slide 11; RWB-E2-017 section 17 |
| BR7 | Every list value declared is a list of its owner: the product group, document type, review, source, signature method and signature status values belong to `rwb-case`'s reference data and are named, never typed | DP-07; TSD P5 T3.2; TSD P6 T3.2 |
| BR8 | The three document state values are declared by this baseline as the values of the field, because no list enumerates them, and the app story owns every transition between them | RWB-E2-017 section 9; `ASM-1875` |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E2-017 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST or PATCH requires `Idempotency-Key` and stores its answer; a GET declares none; the regenerate carries the optimistic lock in the body as `version` | Architecture v5 slide 11; legacy AC10 and AC11 |
| BR12 | The contract declares no case state, no document state machine and no rule evaluation beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E2-017 section 9; RWB-P5-E2017-APP owns review and send |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The seven operations, the six resources, the ten consumed rows and the record declaration are described | In review |
| In review | Consumer sign-off | RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P5-E1054-APP, `rwb-comms` and the wave 2 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `label` on a merge value | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a required set is narrowed, or a state value is added | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The transition into and out of DRAFT, REVIEWED and SENT belongs to RWB-P5-E2017-APP and the review operation of RWB-P5-E1054-APP, and the request lifecycle of `signature_request` belongs to `rwb-comms`.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `state` = "DRAFT" | A generated draft created by the engine of RWB-P5-E2026-APP; `writeOnce` false |
| `state` = "REVIEWED" | A draft the officer marked reviewed through the review operation API-P5-014; `writeOnce` false |
| `state` = "SENT" | A document sent for signature, with the file in `rwb-docs-legal` and `writeOnce` true |
| `reviewStatus` = "NOT_NEEDED" | A generated document whose values need no field review |
| `reviewStatus` = "CONFIRMED" or "CORRECTED" | A draft whose values were reviewed, with a correction recorded where one was made |
| `signature_request.status` = "QUEUED" | A request `rwb-comms` accepted and has not yet sent |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment and the ten fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the resolution of `GAP-1017` and the correction of the plan's C list |
| Consuming teams (RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P5-E1054-APP, `rwb-comms`, the wave 2 harness) | Review and sign off the parts they consume |
| RW-RESTRUCT and RW-CASEOWN, the officer roles | Confirm that the set read, the merge-value read and the send answer carry what the two screens need (Documents CRU on the case) |
| RW-LEGAL, Legal counsel | Confirms that the locked flag of a merge value is the catalog's and never a request option (Documents CRUA) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field and no merge value is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1017; ASM-1876). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| GeneratedDocumentSummary | documentId, treatmentId, documentType, templateCode, templateVersion, state (one of the three declared values), writeOnce, docVersion, reviewStatus; from the `document` fields DF-DOC-001 to DF-DOC-011, DF-DOC-032 and DF-DOC-033 |
| GeneratedDocumentSetPage | items (array of GeneratedDocumentSummary), page, size, total; the query takes treatmentId and state |
| MergeValuePage | documentId, docVersion, templateCode, templateVersion, state, writeOnce, values (array of MergeValue) |
| MergeValue | mergeCode, label, value, formattedValue, locked (required), reason; read through the P6 catalog contract and the store's merge snapshot, masked by role and never persisted by the contract |
| RegenerateRequest | overrides (array of MergeOverride: mergeField, value, reason; 1 to 10, required), version (integer, required) |
| SendForSignatureRequest | treatmentId (uuid, required), documentIds (array of uuid, required) |
| Document | documentId, caseId, documentType, source, storageRef, retentionClass, writeOnce, docVersion, templateCode, templateVersion, treatmentId, state, reviewStatus; the shape of the store and of RWB-P5-E2026-CON |
| DocumentPage | items (array of Document), page, size, total |
| SignatureRequest | id, caseId, treatmentId, documentId, partyId, method (LOV-SIGN-METHOD), status (LOV-SIGN-STATUS), externalRef, sentAt, signedAt, signedDocumentId, expiresAt; from `signature_request` DF-DOC-096 to DF-DOC-107 |
| DecisionRecord | decisionCode D6.4, finalCall, inputsRef, decidedAt and the chain fields of the library |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: case "RW-2026-000401", treatment "TRT-0401" and "TRT-0402", the documents "DOC-0411", the templates "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, the date 2026-12-10, the amount 1250000.00, the key "S-0401", the decision code "D6.4" and the final call "SENT_FOR_SIGNATURE". No example carries a real customer value; the legacy values are examples only. The field-level names of MergeValue, SendForSignatureRequest, SignatureRequest and the two page shapes beyond the legacy list are Not specified in the source documents (GAP-1017; ASM-1876), and the baseline fixes them as the smallest superset of that list. The format element `formattedValue` carries the catalog format of a value (the Thai long date in Buddhist Era, an amount with two decimals) and its element name is fixed here (ASM-1871).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/cases/{caseId}/generated-documents` | none in TSD P5 T-A.1 | 200 `GeneratedDocumentSetPage`; query `treatmentId`, `state`, `page`, `size` 50, newest first, scope applied | Documents R, scope applied | None |
| GET | `/documents/{documentId}/merge-values` | none in TSD P5 T-A.1 | 200 `MergeValuePage` with the values of the draft, masked by role; each read to the access log | Documents R, scope applied | None |
| POST | `/documents/{documentId}/regenerate` | API-P5-017 | Request `RegenerateRequest`; answer 200 `Document` | Documents U, scope applied | `Idempotency-Key` header plus the `version` lock |
| POST | `/cases/{caseId}/generated-documents/send` | none in TSD P5 T-A.1 | Request `SendForSignatureRequest`; answer 200 `DocumentPage` | Documents U, scope applied | `Idempotency-Key` header, first answer stored |
| POST | `/treatments/{treatmentId}/signature-requests` | none | Request `SignatureRequestCreate`; answer 201 `SignatureRequest` | Service identity only | `Idempotency-Key` header |
| GET | `/signature-requests` | none | 200 `SignatureRequest` for an `externalRef`, or 404 | Service identity only | None |
| PATCH | `/signature-requests/{requestId}` | none | Request `SignatureRequestUpdate`; answer 200 `SignatureRequest` | Service identity only | `Idempotency-Key` header |

Error statuses 401, 403, 404, 409, 422 and 503 are those of T-A.2 and section 14. The regenerate is the only operation with an API ID in TSD P5 T-A.1; the other six are fixed by this baseline because no source names them (GAP-1017; ASM-1869, ASM-1870, ASM-1871). The legacy `POST /treatments/{treatmentId}/signature-requests` of the story's section 12 is `rwb-comms`'s API-P6-009 in the target and is declared in 12.2 as consumed, never as provided here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | The generation engine of RWB-P5-E2026-CON: `GenerateRequest` in, `GenerationResult` out; same service, one hop, 2 s, faked |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | P5 rwb-document | API-P5-014 action COMPLETE of RWB-P5-E1054-CON; sets REVIEWED; same service, faked |
| POST | `/api/recovery/document/v1/documents/{documentId}/store` | P5 rwb-document | The store command of RWB-P5-E1024-APP: the row, the write-once promotion and `storage_ref`; same service, faked |
| GET | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | The current version, its Legal approval, its product group and its valid-from date; C `RWB-P6-E1046-CON` in the app story and in no C row here (`ASM-1869`) |
| GET | the template catalog merge field list of a version | P6 rwb-comms | The merge codes, their required flag, their format and their locked flag; path Not specified in the source documents (GAP-1017; ASM-1869) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, its approval, its `decision_log_id` and its outcome; consumed and faked, in no C row (`ASM-1869`) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case and its product group; consumed and faked, in no C row (`ASM-1869`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The product group, document type, review, document source and signature lists (C `RWB-P3-E1043-CON`, DP-07) |
| POST | `/api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | P6 rwb-comms | API-P6-009: starts the request and answers `ACCEPTED` with a request ID or `UNAVAILABLE`; consumed and faked, in no C row (`ASM-1870`) |
| POST | the central ledger sealing operation | P7 rwb-decision | The seal of the local D6.4 record (C `RWB-P7-E1027-CON` in the app story; consumed and faked here) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to an accepted send. The plan's C list names the reference-data contract only, so the six other consumed rows carry `ASM-1869` and no row is added to the metadata C list.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Key caseId; payload with the decision code D6.4, the final call (`GENERATED`, the override final call or `SENT_FOR_SIGNATURE`), the inputs reference, the decided-at time and the chain fields; CloudEvents 1.0 binary mode; no merge value, no personal value and no file byte |

This baseline declares the record because the two writes of this key are decisions (ASM-1873); the row itself is written by RWB-P5-E2017-APP inside its transaction and this key publishes nothing at run time. No `rwb.document.*` event is declared for this key: Architecture v5 slide 42 gives this service exactly `DocumentStored` and `DocumentFieldsExtracted`, neither of which is this key's state change, so the record is the only declaration and the state is read back through 12.1 (GAP-1017; ASM-1874). The absence test of AC7 fails a build that adds a third event to the topic.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This baseline consumes no event: the trigger is the officer's request, the signature result arrives through the `rwb-comms` contract, and the catalog, treatment, case and lists are synchronous reads |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `generate` | Activity contract | `rwb-document` | The engine's activity, owned by RWB-P5-E2026-CON: `GenerationRequest` in and `GenerationResult` out; named here only, called synchronously by the generate and the regenerate operations; no workflow is declared here |

No workflow, no child workflow and no Schedule is declared by this baseline. The review action and the send are synchronous REST operations whose durability is the idempotency row, and JOB-12 and JOB-17 belong to other keys.

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | — | `rwb-document` | — | This baseline declares no Schedule, no cron entry and no job name; retention is RWB-P5-E1017-APP's and intake is RWB-P5-E1032-APP's |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document` | P5 (`rwb_document`) | The `Document` and summary shapes, through the store of RWB-P5-E1024-APP |
| `document_type` | P5 (`rwb_document`) | Contracted use only: the legal flag and the retention class of a generated type |
| `signature_request` | P5 (`rwb_document`) | The `SignatureRequest` shape behind the three service operations (DF-DOC-096 to DF-DOC-107) |
| `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the row behind the `GEN_IDEMPOTENCY_HOURS` name |
| decision-record library table | PLT library, created in `rwb_document` | The D6.4 record a correction and a send write |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency row behind `Idempotency-Key` and the record envelope |

`template` and `merge_field` are P6's, `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `treatment` is S2's, `decision_log_entry` is P7's and the ACE views are P1's; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| screen baseline fake | The seven operations with a set of three documents in DRAFT, one REVIEWED and one SENT, a merge-value page with a locked `transfer_price` and an overridable `contract_date`, and a regenerate answering doc_version 2 | App story, contract tests, wave 2 harness |
| rwb-comms template catalog WireMock | "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, each with `approvedByLegal` true; version 3 current from 2026-12-15; a withdrawn and an unapproved version; the merge field list with the locked flag of `transfer_price` | App story, contract tests |
| rwb-treatment WireMock | Treatment "TRT-0401" approved with `decisionLogId` set and no outcome, and "TRT-0402" with no `decisionLogId` | App story, contract tests |
| rwb-case case and reference-data WireMock | Case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK", and the five lists as data rows | App story, contract tests |
| rwb-comms signature WireMock | `ACCEPTED` with request "RS-0301" for the three documents, `UNAVAILABLE` for AC12, and a delayed answer beyond 2 s | App story, contract tests, wave 2 harness |
| decision-record and central ledger fake | The local D6.4 record with final call `SENT_FOR_SIGNATURE` and a ledger reference; a refusing write for AC9 and TC-E2-017-15 | App story, contract tests |
| store stub | The `Document` answer, the copy-pending state and the write-once promotion | App story, contract tests |
| generation engine stub | The `GenerationResult` of AC1 and the regenerate answer of AC2 | App story, contract tests |
| review operation stub | The REVIEWED state and the refusal of a change to a sent document | App story, contract tests |
| error envelope fake | One answer per message ID of section 14 with its status and its `detail` text | Contract tests, both screens |

A drifted fake fails the drift test of AC8. The exact response field names of the catalog and the merge field list are Not specified in the source documents (GAP-1017; ASM-1876).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 7 provided, 10 consumed | The two reads, the regenerate, the send and the three signature-request operations; the engine, the review action, the store, the catalog (twice), the treatment, the case, the lists, the signature start and the ledger seal; one hop and 2 s on every consumed call |
| Kafka | 1 record declared, 0 events and 0 consumed | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; no `rwb.document.*` event of this key |
| Temporal | 1 activity contract named | `generate` on queue `rwb-document`, owned by RWB-P5-E2026-CON; no workflow and no Schedule |
| File | 1 reference | `storageRef` points at the blob the store writes; the write-once container is `rwb-docs-legal`; this baseline carries no byte |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the seven operations and the shapes of section 11; the AsyncAPI 3.0 fragment of the decision record; the contract README rows for the state values, the error mapping, the idempotency rule and the event count; and the ten WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 is applied because every shape derives from `rwb_document` and the five consumed services are declared as consumed and faked, never as provided. DP-03 is applied because the record declaration of 12.3 and the ledger fake are fixed here, although the row is written by the app story. DP-07 is the reference-data row of 12.2 and the six lists it resolves: the contract names the list codes and never their values. DP-11 fixes the ten consumed rows to one hop with 2 s and a fake each, including the three in-service calls, so a screen can be tested before the engine or the review operation lands. DP-13 is the single rebased base: every declared path hangs below `/api/recovery/document/v1` and no legacy `/api/recovery/v1` path survives. DP-19 records that the two reads are reached through the gateway-bff composite route; this baseline fixes the answer shapes only and no route specification.

**Build steps**

1. Write the seven operations with their paths, queries, resources and error responses; validate the document in the pipeline.
2. Fix the two page shapes and the locked flag of AC2 as schema constraints and README rows.
3. Fix `RegenerateRequest`, `SendForSignatureRequest`, `Document` and `DocumentPage` of AC3, with the 1 to 10 bound and the required sets.
4. Declare the three state values, the write-once rule and the `SignatureRequest` shape of AC4, with the two list enums.
5. Map every status and message ID of AC5 and record the RFC 9457 envelope, including the not-found placeholder.
6. Record the `Idempotency-Key` rule, the first-answer behaviour and the `version` lock of AC6.
7. Declare the record and the absence test of AC7.
8. Publish the ten fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E2017-APP, RWB-P5-E2026-APP, RWB-P5-E1054-APP, `rwb-comms` and the wave 2 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the ten fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E2017-APP and RWB-ITG-E2017-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-011 | Treatment not approved or not open | Documents can be generated only for an approved {treatment} that is still open. | 409 |
| MSG-P5-012 | Set sent for signature (a confirmation, not an error) | {count} documents were sent for signature. | 200 |
| MSG-P5-013 | Send with a document not reviewed or on an old template version | {document} cannot be sent yet: {reason}. | 422 |
| MSG-P5-014 | Correction to a locked merge field | {field} comes from the approved treatment and cannot be changed here. | 422 |
| MSG-P5-002 | Change to a sent document | Legal documents cannot be changed. Add a new version instead. | 409 |
| MSG-GEN-001 | Correction without a reason, or a request that fails validation | Enter {field}. | 422 |
| MSG-GEN-004 | Saved against an old version, or a concurrent request | Someone else changed this record. Reload it to see their change. | 409 |
| MSG-GEN-006 | The signature service is unavailable | {system} is not available. Your request is queued and will be retried. | 503 |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Document or treatment outside the scope | This case is not in your scope. | 403 |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-1017; ASM-1876) | 401 |
| not-found message | A document, a treatment or a signature request that does not exist | Not specified in the source documents (GAP-1017; ASM-1876) | 404 |

The message IDs and the wording are contract elements copied unchanged from RWB-E2-017 section 14; Thai text for each follows decision DL10. MSG-P4-001 and the not-found message are named by the target error envelope and are copied from the platform set, and their exact texts are recorded as the placeholder above.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one plus the two platform rows (ASM-1872): 401 with MSG-P4-001, 403 with MSG-P4-002 or MSG-P4-003, 404 with the not-found message, 409 with MSG-P5-002, MSG-P5-011 or MSG-GEN-004, 422 with MSG-GEN-001, MSG-P5-013 or MSG-P5-014, and 503 with MSG-P7-003 or MSG-GEN-006. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed and is "e-signature" for the refused signature request.

### 15. Screens and states

SCR-14 Treatment record and SCR-30 Case documents are the screens these operations serve, reached through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model. The screens, their forms and their actions are RWB-P5-E2017-APP; this baseline fixes the answer shapes only and declares no screen field list and no route specification. The states its shapes imply are: a set in Loading then list; a document in each of the three state values; a merge-value page with locked and overridable values; a refused send naming the document and the reason; and a read-only view for a role with Documents R only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | AC1, AC5 | Contract | A caller with Documents R only calls the send; refused with 403 and MSG-P4-002 |
| TC-E2-017-01 | AC1, AC2, AC7 | Contract | The set read of treatment "TRT-0401" answers three documents with template versions 2, 1 and 1 |
| TC-E2-017-02 | AC2, AC3 | Contract | A correction of contract_date from "2026-12-10" to "2026-12-12" answers doc_version 2 and "12 December 2569 BE" |
| TC-E2-017-03 | AC3, AC4, AC7 | Contract | Three REVIEWED drafts; the send answers SENT with writeOnce true; the record carries SENT_FOR_SIGNATURE |
| TC-E2-017-04 | AC5 | Contract | The generate operation of "TRT-0402" answers 409 with MSG-P5-011 |
| TC-E2-017-05 | AC3, AC5 | Contract | An empty reason answers 422 with MSG-GEN-001 naming Reason |
| TC-E2-017-06 | AC2, AC5 | Contract | A locked transfer_price answered 422 with MSG-P5-014 naming Transfer price |
| TC-E2-017-07 | AC5 | Contract | A send with one DRAFT document answers 422 with MSG-P5-013 naming the document |
| TC-E2-017-08 | AC4, AC5 | Contract | A change to a SENT document answers 409 with MSG-P5-002 |
| TC-E2-017-09 | AC5, AC6 | Contract | The decision-record fake refuses the write; the correction answers 503 with MSG-P7-003 |
| TC-E2-017-10 | AC6 | Contract | The same `Idempotency-Key` "S-0401" twice answers the first page and starts one request |
| TC-E2-017-11 | AC3, AC5 | Contract | Two regenerates at version 4 answer one 200 and one 409 with MSG-GEN-004 |
| TC-E2-017-12 | AC5, AC6 | Contract | The signature fake answers UNAVAILABLE then ACCEPTED; the states stay REVIEWED then SENT |
| TC-E2-017-13 | AC2, AC5 | Contract | A send whose draft carries template version 2 and a current version 3 answers 422 with MSG-P5-013 |
| TC-E2-017-15 | AC5, AC7 | Contract | The record write is forced to fail on the send; the answer is 503 with MSG-P7-003 and no document changes state |

The fifteen legacy test cases of RWB-E2-017 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E2017-APP. TC-E2-017-14 keeps the legacy level Access and maps to Component in the app story and to Contract here, TC-E2-017-15 keeps the legacy level Resilience and maps to NFR in the app story and to Contract here, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copy ends in `-ITG` and belongs to RWB-ITG-E2017-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the template set, the merge codes, the locked flag, the type mapping, the decision code, the parameter window and the paging default stay data rows, catalog properties or parameters of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and amounts only, and no customer name, address, national ID number, merge value or file byte in any answer.
- No merge value and no merge snapshot is declared in a payload: the record carries `inputsRef` and the document carries `storageRef`.
- The lists are named and never enumerated as values of this service: the product group, document type, review, source, signature method and signature status values belong to `rwb-case`'s reference data (DP-07).
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base, one topic per service and one rebased path set: a document that names another service's base or a legacy `/api/recovery/v1` path as its own fails the review (DP-13).
- Only the two events of `rwb-document` exist and this key declares neither; the absence test of AC7 fails a build that declares a third (DP-03).
- The three state values are declared with their meaning and no transition: a document that declares a fourth value fails the review.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state, no rule evaluation and no document state machine; a transition belongs to RWB-P5-E2017-APP and the review operation of RWB-P5-E1054-APP.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | The set read, the merge-value read, the regenerate and send operations, the `RegenerateRequest` and `SendForSignatureRequest` shapes, MSG-P5-013 and MSG-P5-014 | TC-E2-017-01, TC-E2-017-02, TC-E2-017-05, TC-E2-017-06, TC-E2-017-13 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | The `templateVersion` and `templateCode` of the set item and of `Document`, and MSG-P5-013 for an old version | TC-E2-017-01, TC-E2-017-13 |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it | The `SignatureRequest` shape with its method and status enums, the send operation and the consumed API-P6-009 row | TC-E2-017-03, TC-E2-017-12 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the six other services' reads consumed and faked |
| DP-03 | The record declaration of 12.3 and the ledger fake |
| DP-07 | The reference-list row of 12.2 and the six list codes |
| DP-11 | All ten consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | The single base `/api/recovery/document/v1` and the rebased legacy paths |
| DP-19 | SCR-14 and SCR-30 behind gateway-bff, and the two panel reads |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E2-017; its AC1 to AC13 are owned by RWB-P5-E2017-APP, and the cross-service proof of the same values is RWB-ITG-E2017-ITG.

### 19. Out of scope

- The build of the two reads, the regenerate, the send, the three signature-request operations and the two screens: RWB-P5-E2017-APP.
- The generation engine and its activity: RWB-P5-E2026-APP and RWB-P5-E2026-CON.
- The review queue, the field review and the review operation API-P5-014: RWB-P5-E1054-APP and RWB-P5-E1054-CON.
- The store, the write-once container policy and the version history: RWB-P5-E1024-APP; the storage product itself: RWB-PLT-TE012-APP.
- The e-signature flow, its dispatch and the result of a signature: `rwb-comms` (legacy RWB-E2-018).
- The template catalog, the merge field catalog and the Legal approval of a version: P6 `rwb-comms`, RWB-P6-E1046-CON and RWB-P6-E1046-APP.
- The case documents list, the search and the upload form: RWB-P5-E1026-APP.
- The parameters and reference-data catalogues themselves and their admin operations: P3 rwb-case.
- The cross-service proof of these values: RWB-ITG-E2017-ITG.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
