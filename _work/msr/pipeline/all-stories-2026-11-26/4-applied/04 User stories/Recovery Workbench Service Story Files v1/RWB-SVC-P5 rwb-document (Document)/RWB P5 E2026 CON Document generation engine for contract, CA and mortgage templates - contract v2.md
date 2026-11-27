# RWB-P5-E2026-CON Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2026-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the generation API of `rwb-document` is split out of legacy RWB-E2-026 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the provider contracts and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E2026-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the generation API of `rwb-document` — the generate operation on base `/api/recovery/document/v1` with its `GenerateRequest`, `GenerationResult` and `Document` shapes, the four provider interfaces it consumes with their owner and their fake, the error envelope with its message IDs, the `Idempotency-Key` rule, the `rwb.document.DocumentStored.v1` event schema and the decision record on `rwb.decision-record.v1`**, so that **the app story of this legacy key, the screens story, the template catalog consumers and the wave 2 integration harness build against a fixed, testable contract on Day 1, and a renamed field, a differently read template version or a silent missing merge value can never drift between two services without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E2-026 exposes the generation engine as an in-process `DocumentGenerator` interface inside one module, with a `TemplateCatalog`, a `TreatmentReader` and a `MergeFieldProvider` implemented by other modules, and reads the template catalog, the case facts, the treatment, the party and collateral facts and the decision log across module boundaries. Under the target architecture each of those becomes a contract of another service, and the shapes most likely to drift silently are exactly the ones this engine depends on:

- a field renamed in `GenerateRequest`, `GenerationResult` or the `Document` answer, so the screens story reads a document without its version;
- a template version read differently by two consumers, so the same case yields two different Legal-approved versions on the same date;
- a missing merge field answered 200 with an empty value, so a document reaches a customer with a blank amount;
- an event payload changed, so `rwb-case` or `rwb-agent` receives a `DocumentStored` it cannot read;
- an error returned with the wrong status or without a `messageId`, so a caller cannot tell a withdrawn template from a missing one.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1`, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit - the P6 template catalog (C `RWB-P6-E1046-CON`), the P3 parameters and reference lists (C `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`) and the P7 central ledger (C `RWB-P7-E1027-CON`) - and it records that the P3 case contract, the S2 treatment contract and the P1 source-data contract are consumed and faked although the plan lists them in no C row (`ASM-1933`).

It also records the naming conflict the sources carry: the Ownership Map and TSD P5 API-P5-016 name `POST /cases/{caseId}/generated-documents`, while Architecture v5 slide 16 names `POST /documents/generate`. The baseline declares the Ownership Map name and records the loser as `GAP-1024` and `ASM-1934`. Nothing else is guessed: the field-level names this key does not settle carry the placeholder `Not specified in the source documents (GAP-1024; ASM-1930)`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 appendix T-A.1 and T-A.2 are in force for API-P5-016, and TSD P5 T3.1 is in force for the `document` and `document_type` definitions the `Document` shape draws on.
- The Ownership Map is the only source of owners: `document`, `document_type`, `document_hub_parameter` and `document_field` are P5's in `rwb_document`; `template` and `merge_field` are P6's in `rwb_comms`; `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; `treatment` is S2's; `decision_log_entry` is P7's; the ACE views and `sys_fields` are P1's.
- The `rwb-comms` template catalog baseline RWB-P6-E1046-CON is published, so the template version and the merge field list this generation API consumes have one owner document and one fake.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the generate operation, the three resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`.
2. Fix the generate resource: the path, the `treatmentId` and `templateCodes` parameters with the 1 to 10 bound, the `language` default, the 201 answer, the `Idempotency-Key` header and the declared Documents right C.
3. Fix the `Document` shape, so the screens story reads one answer with the document identifier, the case, the type, the source, the storage reference, the retention class, the write-once flag, the document version and the template code, version and treatment.
4. Fix the four provider interfaces with their owners and their typed answers: the template catalog current version and merge field list, the treatment read, the merge field provider and the decision record.
5. Map every failure to the error envelope and a message ID, status by status, and carry the naming conflict and the missing C rows as gap rows.
6. Record the `Idempotency-Key` rule and the 24-hour window, and state the stored-answer behaviour of a repeat.
7. Declare the event position: `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` with five payload fields and no personal data, the record on `rwb.decision-record.v1`, and no third event for this key.
8. Publish the six fakes, the drift test and the baseline tag, then hand the baseline to RWB-P5-E2026-APP, RWB-P5-E2017-APP and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | The template version is read on a different rule by two consumers | The contract test fails on the date, language and product group rule | None | AC4 |
| X4 | A provider answers an unknown or missing merge field with 200 | The contract test fails: the answer must name the field as missing, and the app answers 422 with MSG-P5-009 | MSG-P5-009 | AC4, AC5 |
| X5 | The event payload changes, a sixth field is added, or a personal value appears in it | The AsyncAPI schema test and the no-personal-data test fail | None | AC7 |
| X6 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X7 | A third event is declared for this key | The absence test fails: only `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` exist for `rwb-document`, and this key publishes the first of them | None | AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T-A, the Ownership Map and the P6 catalog baseline only |
| Negotiable | Pass | The field-level names are settled with the consumers; the operation shape, the provider set, the error mapping, the event schema and the idempotency rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E2026-APP, RWB-P5-E2017-APP and the wave 2 harness on Day 1 |
| Estimable | Pass | One document, three resources, one operation, four provider interfaces, nine contract tables and six fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the document generation API of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document and document_type definitions of TSD P5 T3.1 and the operation API-P5-016 of TSD P5 T-A are in force
    Given the rwb-comms template catalog baseline RWB-P6-E1046-CON is published with its fake

  Scenario: AC1 The generate operation is declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /api/recovery/document/v1/cases/{caseId}/generated-documents as owned by rwb-document and maps it to API-P5-016
    Then the document states that the path of Architecture v5 slide 16, POST /documents/generate, is not declared here and is recorded in GAP-1024
    Then the operation declares the Documents right C, the scope rule, the Idempotency-Key header and the statuses 201, 401, 403, 404, 409, 422 and 503
    Then POST /api/recovery/document/v1/documents/{documentId}/regenerate is declared as the operation of RWB-P5-E2017-APP and not as part of this baseline

  Scenario: AC2 GenerateRequest fixes the required and optional fields and the template bound (new, D-RCV-60)
    Given the GenerateRequest resource declared in the document
    When it is compared with the legacy section 12 request
    Then it carries treatmentId as a uuid and required
    Then it carries templateCodes as an array of string with the minimum 1 and the maximum 10, and it is required
    Then it carries language as TH or EN with the default TH
    Then it carries overrides as an optional list for the screens story of RWB-P5-E2017-APP
    Then an empty templateCodes answers 422 with MSG-GEN-001 and a list of 11 codes is refused by the schema
    Then the header Idempotency-Key is required and carries the value "K-0301" in the example

  Scenario: AC3 GenerationResult and the Document shape are fixed (new, D-RCV-60)
    Given the GenerationResult and Document resources declared in the document
    When they are compared with the legacy section 12 answer and the TSD P5 T3.1 document fields
    Then GenerationResult carries decisionLogEntryId and documents as an array of Document
    Then Document carries documentId, caseId, documentType, source, storageRef, retentionClass, writeOnce, docVersion, templateCode, templateVersion, treatmentId and state
    Then documentId, caseId, documentType, source and docVersion are required and every other property is optional, so a consumer of the previous version keeps working
    Then source is one of "SCAN", "UPLOAD", "GENERATED", "PARTNER" and "EMAIL" of LOV-DOC-SOURCE and state is "DRAFT" for a generated document
    Then the example carries templateCode "DIL-CONTRACT", templateVersion 2, treatmentId "TRT-0301", documentType "CONTRACT", source "GENERATED" and docVersion 1
    Then a generated document declares writeOnce false, so the write-once switch on send belongs to RWB-P5-E2017-APP

  Scenario: AC4 The four provider interfaces carry their owner and their typed answer (new, D-RCV-60)
    Given the provider interfaces declared in the document
    When they are compared with the legacy section 12 published interfaces and the Ownership Map
    Then TemplateCatalog.current(templateCode, language, productGroup, asOf) answers a TemplateVersion with the version, its Legal approval, its valid-from date and its product group, and names P6 rwb-comms as its owner
    Then TemplateCatalog.mergeFields(templateId) answers a list of MergeField with the code, the required flag and the format, and names P6 rwb-comms as its owner
    Then TreatmentReader.find(treatmentId) answers a TreatmentSummary with the type, the approval and the decision log reference, and names S2 rwb-treatment as its owner
    Then MergeFieldProvider.resolve(caseId, treatmentId, mergeFieldCodes) answers the values by code and names P3 rwb-case, S2 rwb-treatment and P1 rwb-source-data as its owners
    Then DecisionRecord writes the record with decision code "D6.4" and final call "GENERATED" and names P7 rwb-decision as the owner of the central ledger
    Then every provider answer marks a missing required field as missing and never as an empty value
    Then the case read, the treatment read, the source-data read and the ledger read are recorded in GAP-1024 because the plan lists them in no C row

  Scenario: AC5 The error envelope and the status mapping are fixed (new, D-RCV-60)
    Given the error responses declared for the generate operation
    When each status is compared with the legacy section 12 errors and section 14
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002, and 404 answers MSG-P4-003 for a case or a treatment that is not found or lies outside the scope
    Then 409 answers MSG-P5-011 for a treatment that is not approved or not open, and MSG-GEN-004 for a concurrent request
    Then 422 answers MSG-P5-009 for a missing merge value, MSG-P5-010 for a template that is not approved or not found, MSG-P6-003 for a withdrawn template and MSG-GEN-001 for empty templateCodes
    Then 503 answers MSG-P7-003 for a failed decision record and MSG-GEN-006 for a failed render or a failed consumed call
    Then every error is an RFC 9457 problem response with messageId, detail and instance, and a refusal returns no partial document set and no decision record

  Scenario: AC6 The Idempotency-Key rule and the 24-hour window are fixed (new, D-RCV-60)
    Given the Idempotency-Key rule of the generate operation
    When it is compared with the legacy section 12 idempotency row and the parameter GEN_IDEMPOTENCY_HOURS
    Then the header is required on the POST and a repeat with the same key inside the window answers the first stored answer with 201
    Then a repeat creates no second document, no second decision record and no second event
    Then the window is the parameter GEN_IDEMPOTENCY_HOURS, whose value is 24, read through the parameters contract and never written in code
    Then the template bound of the request is the parameter GEN_MAX_TEMPLATES, whose value is 10, read the same way
    Then the concurrent case is answered 409 with MSG-GEN-004 and never by a second stored set

  Scenario: AC7 The DocumentStored event and the decision record are declared schemas (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline and the record declaration of the document
    When they are compared with the service catalogue and TSD P5 T5.3
    Then rwb.document.DocumentStored.v1 is declared on the topic rwb.document.events.v1, keyed by caseId, with the five payload fields documentId, caseId, documentType, source and storedAt
    Then the envelope is CloudEvents 1.0 in binary mode and the payload carries no personal value, no merge value and no file byte
    Then the decision record is declared on rwb.decision-record.v1 with the decision code D6.4, the final call GENERATED and a reference to the merge snapshot rather than the snapshot itself
    Then the document states that the store RWB-P5-E1024-APP writes the DocumentStored row per stored document and that this key declares the schema and publishes nothing itself

  Scenario: AC8 The six fakes match the document and no third event is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the six fakes of 12.8 answer the operation of 12.1 and the eight reads of 12.2 with the values of the legacy examples, including template "DIL-CONTRACT" version 2, treatment "TRT-0301" and the date 2026-12-10
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name or a required flag
    Then only rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1 exist for rwb-document, and the absence test fails a build that declares a third event on this key
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E2026-APP. The legacy AC1 to AC14 of RWB-E2-026 are owned by RWB-P5-E2026-APP, and the wave 2 harness RWB-ITG-E2026-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Architecture v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-01 |
| BR5 | This key publishes no event of its own invention: the service has exactly `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`, and this key declares the first | TSD P5 T5.3; Architecture v5 slides 16, 41 and 43 |
| BR6 | No business value is fixed in the contract: template codes, merge codes, type mapping, decision code, dates, the idempotency window and the template bound stay data rows or parameters of the app story | Template and Rules §R7.2 s17; RWB-E2-026 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and amounts only, and no customer name, address, national ID number or title-doc number in any payload | Architecture v5 slide 11; RWB-E2-026 BR11 and section 17 |
| BR8 | No file byte, merge value or merge snapshot in any payload: the record carries the reference to the snapshot and the document carries `storageRef` only | DP-09; RWB-E2-026 section 17 |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from legacy RWB-E2-026 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | A POST requires `Idempotency-Key` and stores its answer, so a repeat inside the window creates nothing; a GET declares none | Architecture v5 slide 11; DP-09 |
| BR12 | The contract declares no case state and no document state machine beyond the values the fields may take; a transition belongs to the app story that performs it | RWB-E2-026 section 9; RWB-P5-E2017-APP owns send and review |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The operation, the three resources, the four provider interfaces and the eight consumed rows are described | In review |
| In review | Consumer sign-off | RWB-P5-E2026-APP, RWB-P5-E2017-APP, the P6 catalog owner and the wave 2 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional field on `Document` | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake, or a retired element returns | A contract test fails | In review |

This baseline declares no case state machine and no document state machine of its own. The value `DRAFT` is the value of the `state` property of a generated document; the creation of that state, the review out of it and the write-once switch on send are the app stories', and the treatment state and the template state belong to `rwb-treatment` and `rwb-comms`.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `source` = "GENERATED" | A document produced by this engine; the other values of LOV-DOC-SOURCE belong to the intake paths |
| `state` = "DRAFT" | A generated document that is not yet sent and is therefore not write-once |
| `writeOnce` = false | The value of a generated draft; the switch on send is RWB-P5-E2017-APP |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the naming resolution of GAP-1024 and the correction of the plan's C list for the case, S2, P1 and P7 reads |
| Consuming teams (RWB-P5-E2026-APP, RWB-P5-E2017-APP, the P6 catalog owner, the P3 and P1 owners, the P7 owner and the wave 2 harness) | Review and sign off the parts they consume |
| RW-LEGAL, Legal counsel | Confirms that the approved version of a template is a precondition of the answer and never an option of the request (Documents A on the P6 catalog) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (GAP-1024; ASM-1928). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| GenerateRequest | treatmentId (uuid, required), templateCodes (array of string, 1 to 10, required), language (TH or EN, default TH), overrides (optional, used by RWB-P5-E2017-APP) |
| GenerationResult | decisionLogEntryId, documents (array of Document) |
| Document | documentId, caseId, documentType, source, storageRef, retentionClass, writeOnce, docVersion, templateCode, templateVersion, treatmentId, state, from the `document` fields DF-DOC-001 to DF-DOC-011, DF-DOC-032 and DF-DOC-033 |
| TemplateVersion | version, approvedByLegal, validFrom, productGroup, language, mergeFieldCodes; read through C `RWB-P6-E1046-CON` and never copied |
| MergeField | mergeCode, required, format, sourceEntity and sourceField; read through C `RWB-P6-E1046-CON` |
| TreatmentSummary | treatmentId, treatmentType, approved, decisionLogId, outcome; read through the S2 contract |
| MergeFieldValue set | The values by merge code answered by the P3, S2 and P1 providers; never persisted by this service |
| DecisionRecord | decisionCode, finalCall, inputsRef, decidedAt and the chain fields of the library; decision code D6.4, final call GENERATED |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: template "DIL-CONTRACT" version 2, treatment "TRT-0301", the date 2026-12-10, the decision code "D6.4", the parameter values 24 and 10 and the identifiers of the legacy cases. No example carries a real customer value; the legacy values are examples only. The field-level names of `TemplateVersion`, `MergeField`, `TreatmentSummary` and `DecisionRecord` beyond what the legacy section 12 names are Not specified in the source documents (GAP-1024; ASM-1930).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/generated-documents` | API-P5-016 | Request `GenerateRequest`; answer 201 `GenerationResult` | Documents C, scope applied | `Idempotency-Key` header, 24-hour window |

Error statuses 401, 403, 404, 409, 422 and 503 are those of T-A.2 and section 14. The path is the Ownership Map and TSD P5 API-P5-016 name; the Architecture v5 slide 16 name `POST /documents/generate` is recorded as the loser of the conflict `GAP-1024` with the assumption `ASM-1934`, and it is declared nowhere in the document.

`POST /documents/{documentId}/regenerate` (API-P5-017) is this service's operation and belongs to the contract of RWB-P5-E2017-CON; this baseline references it and claims neither its shape nor its path as its own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the template catalog current version | P6 rwb-comms | `TemplateCatalog.current`: the version, its Legal approval, its valid-from date and its product group; the path is Not specified in the source documents (GAP-1024; ASM-1921); the owner document is C `RWB-P6-E1046-CON` |
| GET | the template catalog merge field list | P6 rwb-comms | `TemplateCatalog.mergeFields`: the merge codes, their required flag and their format; same owner document |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts of the merge fields, faked (C `RWB-P3-E1042-CON` is the parameters contract of the app story; the case contract `RWB-P3-E1018-CON` is in no C row and is carried by `ASM-1933`) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, approval and `decision_log_id`; consumed and faked, and in no C row of the plan (`ASM-1933`) |
| GET | the party and collateral read of the source data | P1 rwb-source-data | The customer name and the title-doc number, masked by policy; consumed and faked, path Not specified in the source documents (GAP-1024; ASM-1933) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `GEN_IDEMPOTENCY_HOURS` and `GEN_MAX_TEMPLATES` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The type mapping and language lists (C `RWB-P3-E1043-CON`) |
| POST | the central ledger sealing operation | P7 rwb-decision | The seal of the local D6.4 record (C `RWB-P7-E1027-CON`) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to an accepted generation. The case contract, the S2 treatment contract, the P1 source-data contract and the P7 read are consumed by the generation API; the plan's C list names the P6 catalog, the P3 parameters and lists and the P7 ledger only, so those four rows carry `ASM-1933` and no row is added to the metadata C list.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Key caseId; payload documentId, caseId, documentType, source, storedAt; CloudEvents 1.0 binary mode; no personal data, no merge value, no file byte |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | The hash-chained record with decision code D6.4, final call GENERATED and `inputsRef` naming the merge snapshot, never the snapshot |

This baseline declares the event schema and the record declaration because the service owns the topic; the `DocumentStored` row itself is written by the store RWB-P5-E1024-APP in its own transaction, and this key publishes nothing at run time. The service's other event, `rwb.document.DocumentFieldsExtracted.v1`, is declared in the same topic by the extraction stories and is named here only to fix the count. No third event exists for `rwb-document`.

#### 12.4 Events consumed

None. The generation path subscribes to no topic: the treatment, the case, the source data, the parameters, the lists and the catalog are synchronous reads, and the trigger is the HTTP request. A change of a template version reaches this engine on its next read.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `generate` | Activity contract | `rwb-document` | One typed activity interface with `GenerationRequest` in and `GenerationResult` out, idempotent by the request key; called synchronously by the controller and by the screens story; no workflow is declared here |

No workflow is declared by this baseline. `DocumentIntakeWorkflow` of the L3 workflow kit template "Document intake" is owned by RWB-P5-E1049-APP and only its generate step is named.

#### 12.6 Schedules

None. This baseline declares no Schedule, no cron entry and no job name; JOB-17 retention belongs to RWB-P5-E1017-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document` | P5 (`rwb_document`) | The `Document` shape and the columns the answer carries, with the keys of RWB-P5-E2026-APP section 11 |
| `document_type` | P5 (`rwb_document`) | Contracted use only: the document type and the retention class behind the template-to-type mapping |
| decision-record library table | PLT library, created in `rwb_document` | The D6.4 record the operation writes |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The idempotency row behind `Idempotency-Key` and the service's event envelope objects |

`template` and `merge_field` are P6's, `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `treatment` is S2's, `decision_log_entry` is P7's and the ACE views, `sys_fields` and `sys_objects` are P1's; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms template catalog WireMock | The current version for code "DIL-CONTRACT", language TH and product group "MORTGAGE" as version 2 with `approvedByLegal` true and a valid-from date; a version 3 valid from 2026-12-15; an unapproved version of "DIL-CA"; a withdrawn "DIL-MORTGAGE" with no approved successor; no template for product group "HIRE_PURCHASE"; the merge field list with the required flags and the formats | App story, contract tests, wave 2 harness |
| rwb-case case WireMock | `GET /cases/{caseId}` for case "RW-2026-000301" and a delayed answer beyond 2 s | App story, contract tests |
| rwb-treatment WireMock | Treatment "TRT-0301" of type "DEED_IN_LIEU", approved, with `decisionLogId` set and no outcome; treatment "TRT-0302" with no `decisionLogId` | App story, contract tests |
| rwb-source-data WireMock | The party and collateral values of the merge fields of case "RW-2026-000301", and an answer with `titleDocNo` absent | App story, contract tests |
| parameters and reference-data WireMock | `GEN_IDEMPOTENCY_HOURS` 24, `GEN_MAX_TEMPLATES` 10 and `GEN_FONT` "TH Sarabun New"; the type mapping and the language list | App story, contract tests |
| decision-record and central ledger fake | The local D6.4 record with final call GENERATED and a ledger reference; a refusing write for the AC7 case | App story, contract tests, wave 2 harness |

A drifted fake fails the drift test of AC8. The exact response field names of the catalog and the source-data reads are Not specified in the source documents (GAP-1024; ASM-1930).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 8 consumed | The generate operation; the two catalog reads, the case read, the treatment read, the source-data read, the parameters read, the list read and the ledger seal; one hop and 2 s on every consumed call |
| Kafka | 1 event schema and 1 record declared, 0 consumed | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` and the record on `rwb.decision-record.v1`; `DocumentFieldsExtracted` is the service's other event and is not this key's |
| Temporal | 1 activity contract | `generate` on queue `rwb-document`; no workflow and no Schedule |
| File | 1 reference | `storageRef` points at the blob the store writes at `{container}/{caseId}/{documentId}/v1`; this baseline carries no byte and no body |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the generate operation and the three resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentStored.v1` and the record declaration; the contract README rows for the provider ownership, the error mapping, the idempotency window and the event count; and the six WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-05 appears because the legacy `AceSourceQuery` read is replaced by the P1 contract; DP-15 and DP-19 appear because the migration step and the screen route are recorded here for the app story to use.

**Build steps**

1. Write the generate operation with its path, parameters, resources and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and AC3 and the 1 to 10 bound as schema constraints and README rows.
3. Declare the four provider interfaces with their owners, their typed answers and the missing-field rule of AC4.
4. Map every status and message ID of AC5 and record the RFC 9457 envelope.
5. Record the `Idempotency-Key` rule and the 24-hour window of AC6, and the two parameter names as parameters rather than values.
6. Declare the `DocumentStored` schema and the record of AC7, with the absence test for a third event.
7. Publish the six fakes and the eight contract tests, including the drift test; tag the baseline and collect the consumer sign-off of RWB-P5-E2026-APP, RWB-P5-E2017-APP and the wave 2 harness.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the six fakes answer every operation and read of sections 12.1 and 12.2, the drift test is green, and RWB-P5-E2026-APP and RWB-ITG-E2026-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | A required merge field has no value (new) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal (new) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P5-011 | The treatment is not approved or not open (new) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | templateCodes is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same treatment and template | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The renderer fails | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Caller lacks Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

The message IDs and the wording are contract elements copied unchanged from RWB-E2-026 section 14; Thai text for each follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one, fixed by AC5: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-P5-011 or MSG-GEN-004, 422 with MSG-P5-009, MSG-P5-010, MSG-P6-003 or MSG-GEN-001, and 503 with MSG-P7-003 or MSG-GEN-006. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed.

### 15. Screens and states

SCR-30 Case documents is the screen the generated drafts appear on, in state DRAFT; the generation screens, their overrides form and the review and send actions are RWB-P5-E2017-APP. The contract serves them through the gateway-bff composite route (DP-19), which calls the owner once and merges the answers into the screen model; this baseline fixes the answer shapes only and declares no screen field list and no route specification. The screen states the baseline implies are the ones the `Document` shape carries: a generated document in DRAFT with `writeOnce` false, a version number, and the template code and version it was produced from.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | Access | Component | RW-TEAMMGR user (Documents R) calls the generate operation; refused with MSG-P4-002 |
| TC-E2-026-01 | AC2, AC3, AC4, BR1, BR6 | Contract | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02 | AC4, AC5 | Contract | Case with no title deed number |
| TC-E2-026-03 | AC4, AC8 | Contract | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC4, AC5 | Contract | DIL-CA v1 not approved |
| TC-E2-026-05 | AC4, AC5 | Contract | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC4, AC5 | Contract | Treatment with no decision_log_id |
| TC-E2-026-07 | AC5, AC7 | Contract | Decision log stub refusing writes |
| TC-E2-026-08 | AC6 | Contract | Same Idempotency-Key twice |
| TC-E2-026-09 | AC6, AC5 | Contract | Two parallel requests |
| TC-E2-026-10 | AC5, AC7 | Contract | Damaged template body |
| TC-E2-026-11 | AC4, AC5 | Contract | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC1, AC5 | Contract | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC2, AC3, AC7 | Contract | Three current templates |
| TC-E2-026-14 | AC2, AC5, AC8 | Contract | Three templates, DIL-CA not approved |
| TC-E2-026-16 | AC5, AC7 | NFR | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

The sixteen legacy test cases of RWB-E2-026 are listed in the order of the WP and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E2026-APP. TC-E2-026-15 keeps the legacy level Access and maps to Component, TC-E2-026-16 keeps the legacy level Resilience and maps to NFR, and the System level of the others maps to Contract because the artefact under test is the contract. The integration harness copies end in `-ITG` and belong to RWB-ITG-E2026-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: template codes, merge codes, the type mapping, the decision code, the dates, the idempotency window and the template bound stay data rows or parameters of the app story.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, dates and amounts only; no customer name, address, national ID number or title-doc number is declared in any answer.
- No merge value, no merge snapshot and no file byte in a payload, an example, a fake or a log; the record carries `inputsRef` and the document carries `storageRef`.
- No template body is declared: the catalog answer names a version and a merge field list, and the body stays behind the P6 owner's claim-check reference.
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- Only the two events of `rwb-document` exist, and this key declares one of them; the absence test of AC8 fails a build that declares a third.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no document state machine; a transition belongs to the app story that performs it.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | The generate operation, `GenerateRequest`, `GenerationResult`, the `Document` shape, the `TemplateCatalog` and `MergeFieldProvider` interfaces, MSG-P5-009 and MSG-P5-010, the `DocumentStored` schema | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06, TC-E2-026-13, TC-E2-026-14 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | The `TemplateCatalog.current` contract with its `approvedByLegal` and `validFrom`, the `TemplateVersion` shape, MSG-P5-010 and MSG-P6-003 | TC-E2-026-03, TC-E2-026-04, TC-E2-026-05, TC-E2-026-11 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the six other services' reads consumed and faked |
| DP-03 | The decision record declaration of 12.3 and the ledger fake |
| DP-05 | The source-data row of 12.2 and its fake |
| DP-06 | The parameters row of 12.2, the two parameter names and the 24-hour window |
| DP-07 | The reference-list row of 12.2 and its fake |
| DP-09 | The `Idempotency-Key` rule, the `DocumentStored` schema and the CloudEvents envelope |
| DP-11 | All eight consumed rows with one hop, a 2 s timeout and a fake |
| DP-15 | The migration position recorded for `document` in the service's own sequence |
| DP-19 | SCR-30 behind gateway-bff, and the screens story reference |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |

The legacy key is RWB-E2-026; its AC1 to AC14 are owned by RWB-P5-E2026-APP, and the cross-service proof of the same values is RWB-ITG-E2026-ITG.

### 19. Out of scope

- The build of the generate operation, the renderer, the resolver, the formatter and the store call: RWB-P5-E2026-APP.
- The build of the P6 template catalog and the Legal approval of a template version: RWB-P6-E1046-APP and the `rwb-comms` stories.
- The generation, review and send screens, the overrides form and `POST /documents/{documentId}/regenerate`: RWB-P5-E2017-APP and RWB-P5-E2017-CON.
- The e-signature flow: RWB-P5-E2018-APP.
- Template upload and approval by Legal within this service's own admin surface: P6 `rwb-comms` and RWB-P5-E1046-APP.
- Debt sale agreements and notices (FEAT-DBS-10, Epic 6).
- The retention Schedule and disposal: RWB-P5-E1017-APP.
- The cross-service proof of these values: RWB-ITG-E2026-ITG.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
