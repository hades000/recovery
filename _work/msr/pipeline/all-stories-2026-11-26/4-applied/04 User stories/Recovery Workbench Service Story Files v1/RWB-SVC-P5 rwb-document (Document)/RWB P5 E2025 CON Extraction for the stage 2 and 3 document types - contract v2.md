# RWB-P5-E2025-CON Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2025-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-015, FR-P5-016, FR-P5-017, FR-P5-018, FR-P5-027, FR-P5-028, FR-P5-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the stage 2 and 3 extraction extension of `rwb-document` is split out of legacy RWB-E2-025 and published on base `/api/recovery/document/v1` with the topic `rwb.document.events.v1`, the checked-fields read, the checked-field shapes, the eleven-type field code fixture, the state filter and masking rule, the error envelope, the event declaration and the fakes with their drift test. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E2025-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the stage 2 and 3 extraction extension of `rwb-document` — the checked-fields read on base `/api/recovery/document/v1` with the `CheckedField` and `CheckedFieldSet` shapes, the state filter and masking rule, the eleven-type field code fixture with the five new types and the extended hearing-notice list, the error envelope with every message ID and its status, the `rwb.document.DocumentFieldsExtracted.v1` declaration with no field value, and the fakes with their drift test —**, so that **the app story of this legacy key, the S4 litigation reader, the S2 treatment reader, the review queue of `rwb-document` and the wave 2 integration harness build against a fixed, testable contract on Day 1, and a renamed checked field, a different state filter, an extra payload property or a personal value in an event can never drift between two services without a failing test**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Legacy RWB-E2-025 hands the litigation and treatment modules a Java interface inside the same process — `DocumentFieldReader.checkedFields(UUID caseId, String documentType)` returning `CheckedField` — together with an in-process `ExtractStep`, an in-process `DocumentTypeCatalog` and a document read on the monolith base. Under the target architecture S4 and S2 are separate services that cannot link a Java interface of `rwb-document`, the extraction is an activity of a workflow on the owner's own task queue, and the parts most likely to drift silently are exactly the ones this baseline fixes:

- a checked field renamed or dropped, so the litigation pack renders a judgment amount it cannot attribute to a field or a document version;
- a state filter widened to REVIEW, so an unchecked value reaches the pack and the treatment record with no person having seen it;
- a personal value such as `party_names` returned without its flag or without masking, so a contract's parties reach a role that may not see them;
- an extraction event carrying a field value, so a contract amount leaves the service in a Kafka payload;
- an error answered with the wrong status or without a `messageId`, so a reader cannot tell a document outside its scope from a type that is not in force;
- a field code set read from a different place by the extraction and by the reader, so the same judgment yields two different field lists on the same date.

The baseline fixes the names the checks require: schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue `rwb-document` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document`. It makes the C dependencies of the app story explicit — the P3 parameters contract `RWB-P3-E1042-CON` and the P3 reference-data contract `RWB-P3-E1043-CON` — and it records that the `rwb-case` case read is consumed and faked although the plan lists it in no C row of this key (`ASM-1906`).

It also records what the sources leave open. No TSD P5 T-A.1 row and no Architecture v5 slide names a REST operation or a path for reading checked fields, so the operation, the path and the field-level names of `CheckedField` and `CheckedFieldSet` are the baseline's own choice and are Not specified in the source documents (`ASM-1904`). The extraction operations themselves are not this key's: they are published by RWB-P5-E1053-CON and this baseline consumes and references them without declaring a second copy (`ASM-1905`). Nothing else is guessed: the five new types, their fields, the pattern of `red_case_no`, the pass mark 0.90, the field threshold 0.80 and the message IDs are copied character for character from RWB-E2-025, FSD P5 A2.22 and TSD P5 T3.1.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the operation, topic, event and queue names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` rule and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- TSD P5 T3.1 is in force for `document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter`, and TSD P5 T3.2 is in force for LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW.
- The extraction baseline RWB-P5-E1053-CON is published with the extract operation, the extract-state read, the fields read, the `FieldSet` shape, the field set fixture of DOCTYPE-2026.11 and the agent route it consumes, so this baseline extends a contract that exists and declares no second extraction operation (`ASM-1905`).
- The classification baseline RWB-P5-E1050-CON and the review baseline RWB-P5-E1054-CON are published, so `predicted_type`, `classification_confidence`, `review_reason` and the states CONFIRMED and CORRECTED have one owner document each (`ASM-1910`).
- The Ownership Map is the only source of owners: `document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's; the `agent_*` tables and the model route are P10's.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), so its four H, C, I and X columns are empty and every dependant builds against the published baseline and its fakes.
- The release date 31 December 2026 is the legacy one and is tentative (`ASM-1908`), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (`ASM-1909`).

### 4. Flow

1. Draft the OpenAPI 3.1 document of `rwb-document` with the checked-fields read, the two resources of section 11 and the error responses of section 14, on the single base `/api/recovery/document/v1`, beside the operations RWB-P5-E1053-CON and RWB-P5-E1024-APP already declare.
2. Fix the read: the case path parameter, the required `documentType` query, the optional `documentVersion`, the declared Documents right R, the scope rule and the access log on every read.
3. Fix `CheckedField` and `CheckedFieldSet` field by field, with the required set, the confidence precision, the `state` values OK, CONFIRMED and CORRECTED and the `personal` flag.
4. Publish the field code fixture of the eleven types from the type table version DOCTYPE-2026.12: the 26 codes of the six Epic 1 types and the 20 codes of the five new types, with `party_names` marked personal.
5. Fix the state filter and the masking rule: only OK, CONFIRMED or CORRECTED rows are returned; a REVIEW row is never returned; a personal value is returned only when the caller's masking rule allows it.
6. Map every failure to the error envelope and a message ID, status by status, and record the absent operation name and the absent C row as a gap and its assumptions.
7. Declare the event position: the one extraction event `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`, with the new type codes in `documentType`, no field value and no personal value; no third event of this key.
8. Publish the fakes, the drift test and the absence test, then hand the baseline to RWB-P5-E2025-APP, the S4 and S2 readers, the review queue and RWB-ITG-E2025-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a corrected document or a new major version | None | AC2, AC3 |
| X3 | The state filter returns a REVIEW field, or a fourth state appears | The contract test fails: the answer carries OK, CONFIRMED and CORRECTED only | None | AC4 |
| X4 | A personal value is returned without its flag or without masking | The contract test and the no-personal-data test fail | None | AC4 |
| X5 | A field code set is read from a different place by the extraction and by the reader | The contract test fails against the published fixture of the version in force | None | AC3, AC7 |
| X6 | An error returns a wrong status or no `messageId` | The contract test fails on the error envelope and the message table | MSG-P4-001 | AC5 |
| X7 | A field value or a personal value appears in the event payload, or a fourth event is declared | The AsyncAPI schema test, the no-personal-data test and the absence test fail | None | AC6, AC8 |
| X8 | A fake drifts from the document, or a second extraction operation is declared | The drift test or the absence test fails the build and the merge is blocked | None | AC7, AC8 |

### 6. INVEST check

| Criterion | Verdict | Note |
|---|---|---|
| Independent | Pass | No build dependency; reads the platform envelopes, TSD P5 T3, the Ownership Map and the two same-service baselines it extends |
| Negotiable | Pass | The field-level names are settled with S4, S2 and the review queue; the operation set, the state filter, the fixture, the error mapping, the event declaration and the absence rule are fixed by the target architecture and the legacy section 12 |
| Valuable | Pass | Unblocks RWB-P5-E2025-APP, the S4 and S2 readers and the wave 2 harness on Day 1 |
| Estimable | Pass | One document, one operation, two resources, one fixture, nine contract tables and seven fakes |
| Small | Pass | Fits one sprint with its contract tests |
| Testable | Pass | Every criterion in section 7 is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the extraction extension and the checked-field reader of rwb-document

  Background:
    Given the service naming rule of the platform library is in force
    Given the document, document_field, document_intake, document_text, document_type and document_hub_parameter definitions of TSD P5 T3.1 are in force
    Given the extraction baseline RWB-P5-E1053-CON is published with its three operations, its FieldSet shape and its field set fixture of DOCTYPE-2026.11
    Given the type table version "DOCTYPE-2026.12" is published with the eleven types and their field definitions

  Scenario: AC1 The checked-fields read is declared and the document validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-document is published with this baseline
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /api/recovery/document/v1/cases/{caseId}/checked-fields as owned by rwb-document with a 200 answer of CheckedFieldSet
    Then the operation declares the Documents right R, the scope rule and the statuses 200, 401, 403, 404, 422 and 503 as section 14 fixes them
    Then the document states that the path is its own choice because no TSD P5 T-A.1 row and no Architecture v5 slide names a checked-field read, and records it as a gap with its assumption
    Then it declares POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract, GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction and GET /api/recovery/document/v1/documents/{documentId}/fields as consumed from RWB-P5-E1053-CON and not as its own
    Then no operation of another service's base is declared as provided

  Scenario: AC2 CheckedField and CheckedFieldSet are fixed (new, D-RCV-60)
    Given the CheckedField and CheckedFieldSet resources declared in the document
    When they are compared with the legacy section 12 interface comment and the document_field columns of TSD P5 T3.1
    Then CheckedField carries documentId as a uuid and required, docVersion as an integer and required, fieldName as a string and required, value as a string, state as a string and required, and confidence as a number of numeric(5,4)
    Then CheckedField also carries dataType, personal, extractorVersion and tableVersion as optional properties, so a consumer of the previous version keeps working
    Then state carries exactly the three legacy values OK, CONFIRMED and CORRECTED, and REVIEW is declared as a state the read never returns
    Then CheckedFieldSet carries caseId, documentType, documentVersion, tableVersion, fieldCount and fields as an array of CheckedField
    Then caseId, documentType and fields are required and the set is ordered by documentId and fieldName
    Then the example carries caseId of case "RW-2026-000601", documentType "JUDGMENT", a field red_case_no in state OK and a field judgment_amount absent because it is in REVIEW
    Then a documentType outside LOV-DOC-TYPE answers 422 with MSG-P5-006 and an absent documentType answers 422 with MSG-GEN-001

  Scenario: AC3 The eleven-type field code fixture is fixed from the type table (new, D-RCV-60)
    Given the field code fixture of the baseline, built from document_type.field_definitions of version "DOCTYPE-2026.12"
    When it is compared with the five new types of the legacy section 13, the four COURT_NOTICE fields and the 26 codes of DOCTYPE-2026.11
    Then CONTRACT carries contract_no, party_names, contract_amount and contract_date
    Then CREDIT_APPROVAL carries approval_no, approved_amount, approval_date and approval_level
    Then MORTGAGE_DOCUMENT carries title_doc_no, mortgage_amount, registration_date and land_office
    Then COURT_FILING carries court_name, black_case_no, filing_date and claim_amount
    Then JUDGMENT carries court_name, red_case_no, judgment_date and judgment_amount
    Then COURT_NOTICE keeps court_name, black_case_no, notice_date and hearing_date, so hearing notices stay under the Epic 1 type
    Then exactly 46 field codes exist across the eleven types: the 26 of DOCTYPE-2026.11 and the 20 of the five new types
    Then party_names carries personal true, because the legacy AC2 asserts that it is masked for roles without the right
    Then the fixture declares no pattern, no threshold and no method as a value: those are properties of the type table the extraction reads at run time
    Then each code maps to document_field.field_name varchar(60), DF-DOC-014

  Scenario: AC4 The state filter, the version rule and the masking are fixed (new, D-RCV-60)
    Given the read semantics declared in the document
    When they are compared with the legacy BR1, BR5, BR7 and BR8 and with AC9, AC10 and AC11 of the app story
    Then only fields in state OK, CONFIRMED or CORRECTED are returned and a field in REVIEW is never returned
    Then a field of a type is returned only when the type is in the version in force on the extraction date, read by valid_from and valid_to, so a document received on 2026-12-26 is read against DOCTYPE-2026.11
    Then documentVersion narrows the answer to one version of one document and its absence returns the active rows of every version of that type on the case
    Then a personal value is returned only when the caller's masking rule allows it, and the personal flag is present on the entry in every case
    Then each read is declared as written to the access log and the answer carries no field of a document outside the caller's scope, which is a 404 with MSG-P4-003
    Then the read declares no write and no side effect, and no Idempotency-Key
    Then the threshold and the pass mark are named as parameters, never as values of the contract

  Scenario: AC5 The error envelope and every message ID with its status are fixed (new, D-RCV-60)
    Given the error responses declared for the checked-fields read
    When each status is compared with the legacy section 14 and the service messages of rwb-document
    Then 401 answers MSG-P4-001, 403 answers MSG-P4-002 and 404 answers MSG-P4-003 for a case or a document that is not found or lies outside the scope
    Then 422 answers MSG-P5-006 for a documentType that is not in the version in force and MSG-GEN-001 for an absent or empty documentType
    Then 503 answers MSG-GEN-006 with {system} naming "Case service" for a failed case read and "Reference data" for a failed list read
    Then MSG-P5-003 is declared as the label of a document with a field in review and never as an error response of this operation
    Then every error is an RFC 9457 problem response with messageId, detail and instance
    Then a refusal returns no CheckedFieldSet and no partial field list

  Scenario: AC6 The event and the consumed extraction operations are named and not re-declared (new, D-RCV-60)
    Given the AsyncAPI fragment of this baseline and the consumed rows of 12.2
    When they are compared with the service catalogue of TSD P5 T5.3 and with the extraction baseline
    Then rwb.document.DocumentFieldsExtracted.v1 is declared on the topic rwb.document.events.v1 with the retry topics at 1 min, 10 min and 1 h and the .dlt topic
    Then the payload carries intakeId, documentId, documentType, tableVersion, extractorVersion, extractedAt, fieldCount and fields of fieldName, confidence and state
    Then the declaration states that documentType carries the codes of the new types and that the payload carries no field value, no personal value and no document text
    Then the document states that the schema and the writing of the row belong to the extraction of RWB-P5-E1053-CON and that this key declares the extension and publishes nothing at run time
    Then only rwb.document.DocumentStored.v1 and rwb.document.DocumentFieldsExtracted.v1 exist for rwb-document, and this key declares no third event

  Scenario: AC7 The seven fakes answer the document and the drift test fails on any mismatch (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed and the fakes are run against the document
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the seven fakes of 12.8 answer the operation of 12.1 and the four reads of 12.2 with the values of the legacy examples, including case "RW-2026-000601", document "DOC-0602", the type "JUDGMENT", the confidence 0.7100 and the pass mark 0.90
    Then the drift test compares each fake with the document and fails on any mismatch of a path, a status, a field name, a required flag or an enum value
    Then the field code fixture is compared with the fixture of RWB-P5-E1053-CON and a missing Epic 1 code fails the test

  Scenario: AC8 The absence test refuses a second operation, a fourth event or a forty-seventh code (new, D-RCV-60)
    Given the published document, its AsyncAPI fragment and its fixture
    When the absence test runs
    Then it fails a build that declares a second checked-field operation or a checked-field write
    Then it fails a build that declares an operation outside /api/recovery/document/v1 or an event outside rwb.document.<Event>.v1
    Then it fails a build that declares a third event for rwb-document
    Then it fails a build whose fixture declares a 47th field code or drops one of the 46
    Then it passes on this baseline
```

The eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P5-E2025-APP. The legacy AC1 to AC11 of RWB-E2-025 are owned by RWB-P5-E2025-APP, and the wave 2 harness RWB-ITG-E2025-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/document/v1` on every declared operation | DP-01; Template and Rules §R4; Architecture v5 slide 41 notes |
| BR2 | One topic per service: `rwb.document.events.v1`, with the retry and `.dlt` topics of the platform convention | DP-09; Architecture v5 slides 16 and 42 |
| BR3 | A change inside major version 1 is additive; a removed, renamed or retyped property and a narrowed required set are a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR4 | The document declares only tables of `rwb_document` and only operations owned by `rwb-document`; an operation of the same service that another baseline owns is described as consumed and referenced, never re-declared | Ownership Map; DP-01; `ASM-1905` |
| BR5 | The service has exactly two events, `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1`; this key declares the second and adds no type, topic or payload property | TSD P5 T5.3; Architecture v5 slide 42; `ASM-1907` |
| BR6 | No business value is fixed in the contract: the types, the field codes, the patterns, the threshold, the pass mark, the extraction methods and the review-only flags stay rows of the type table and the parameter table | Template and Rules §R7.2 s17; RWB-E2-025 section 17 |
| BR7 | No personal data in a schema, an example or a fake: identifiers, codes, versions, dates, confidences and states only, and no party name, customer name, account number or title-doc number in clear | Architecture v5 slide 11; RWB-E2-025 BR7 and section 17 |
| BR8 | No field value and no document text in the event or a log: the payload carries field names, confidences and states, and the read carries a value only behind masking and the access log | DP-09; RWB-E2-025 section 12 |
| BR9 | Every consumed row states one hop, a 2 s timeout, a GET retry once with jitter and a breaker per downstream, and a failed read maps to MSG-GEN-006 naming the system that failed | DP-11, ADR-020; Architecture v5 slide 11 |
| BR10 | Every error uses one envelope and one message ID per condition; the message texts are copied unchanged from RWB-E2-025 section 14 | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR11 | The checked-field read is a GET: it declares no `Idempotency-Key`, writes nothing and has no side effect; the extraction operation that may follow keeps the `Idempotency-Key` of its own baseline | Architecture v5 slide 11; DP-09; `ASM-1905` |
| BR12 | The contract declares no case state and no extraction state machine beyond the values the fields may take; a transition belongs to the app story that performs it, and CONFIRMED and CORRECTED belong to RWB-P5-E1054-APP | RWB-E2-025 section 9; `ASM-1910` |

### 9. State transitions

| Baseline state | Event | Condition | Next state |
|---|---|---|---|
| Draft | Review opened | The read, the two resources, the fixture, the four consumed rows and the event declaration are described | In review |
| In review | Consumer sign-off | RWB-P5-E2025-APP, the S4 and S2 readers, the review queue and the wave 2 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional `extractorVersion` on `CheckedField` | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a required set is narrowed | New major version drafted |
| Baselined | Drift in a fake or in the fixture | A contract test fails | In review |

This baseline declares no case state machine and no extraction state machine of its own. The values below are the values the fields may carry; the writing of them is the extraction's, and the move out of REVIEW belongs to RWB-P5-E1054-APP.

| Field value in the baseline | Meaning declared by this document |
|---|---|
| `state` = "OK" | A field whose confidence is at or above the threshold and whose value converted and matched its pattern |
| `state` = "REVIEW" | A field below the threshold, a `review_only` field, a value that could not be converted or a value that failed its pattern; declared and never returned by the read |
| `state` = "CONFIRMED" | A field a person accepted in the review queue of RWB-P5-E1054-APP |
| `state` = "CORRECTED" | A field a person corrected in the review queue of RWB-P5-E1054-APP, with the stored value the corrected one |
| `extractStatus` = "PENDING", "DONE", "FAILED" | The LOV-EXTRACT-STATUS values of TSD P5 T3.2, carried by the extraction baseline this key consumes |
| `personal` = true | A value masked for a role without the right; `party_names` is the one code this baseline asserts it for |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-document | Owns the OpenAPI document, the AsyncAPI fragment, the fixture and the seven fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the operation name of the single gap this baseline records |
| Consuming teams (RWB-P5-E2025-APP, the S4 litigation reader, the S2 treatment reader, the review queue and the wave 2 harness) | Review and sign off the parts they consume |
| RW-LITOFF, litigation officer; RW-RESTRUCT, restructuring officer (FCR) | Confirm that the read carries what the pack and the treatment record need (Documents CRU on the case in scope) |
| RW-REFADM, reference data administrator | Loads the type table version the fixture is built from (Reference data CRUD) |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the `Idempotency-Key` rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an example or a fake |

The per-service login behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-document login (DP-02)" and the name is Not specified in the source documents (`ASM-1904`). The declared area and right are enforced at gateway-bff (DP-19); no `rwb-access` contract is declared here. The model route is not this service's secret: the provider, the model and the key belong to `rwb-agent` and are consumed through RWB-P5-E1053-CON.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| CheckedField | documentId (uuid, required), docVersion (integer, required), fieldName (string, required), value (string), state (OK, CONFIRMED or CORRECTED, required), confidence (numeric(5,4)), dataType, personal, extractorVersion, tableVersion, from the `document_field` fields DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 |
| CheckedFieldSet | caseId, documentType, documentVersion, tableVersion, fieldCount, fields (array of CheckedField); ordered by documentId and fieldName |
| Field code fixture | The 46 codes of version DOCTYPE-2026.12: the 26 codes of the six Epic 1 types of DOCTYPE-2026.11 and the 20 codes of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING and JUDGMENT of section 13 of the app story; `party_names` carries personal true |
| Field code source | `document_type.field_definitions` (DF-REF-224) in the version in force by `valid_from` and `valid_to`, with name, data_type, personal, extraction_method, review_only and the optional pattern; the fixture declares the codes and never the values of the table |
| Read semantics | Only OK, CONFIRMED and CORRECTED; the version in force on the extraction date; masking by role; the access log on every read |
| Event payload | `rwb.document.DocumentFieldsExtracted.v1`: intakeId, documentId, documentType, tableVersion, extractorVersion, extractedAt, fieldCount, fields [fieldName, confidence, state] |
| Error envelope | RFC 9457 problem details with `messageId`, `detail`, `instance` and the status of section 14 |

Every example in the document is synthetic and uses the legacy values: case "RW-2026-000601", documents "DOC-0602" and "DOC-0605", the types "CONTRACT", "JUDGMENT" and "COURT_NOTICE", the confidence 0.7100 and 0.9200, the field threshold 0.80, the pass mark 0.90, the type table versions "DOCTYPE-2026.11" and "DOCTYPE-2026.12" and the extractor versions of the Epic 1 baseline. No example carries a customer value: the party names of the legacy AC2 are declared as the field code `party_names` with no value, and the field values of the legacy examples are examples only. The field-level names of `CheckedField` and `CheckedFieldSet` beyond the legacy interface comment are Not specified in the source documents (`ASM-1904`).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/cases/{caseId}/checked-fields` | no TSD row; the baseline's own path (`ASM-1904`) | Query `documentType` required and `documentVersion` optional; answer 200 `CheckedFieldSet` | Documents R with scope applied; each read to the access log | Not applicable |

The read is the target shape of the legacy Java interface `DocumentFieldReader.checkedFields(UUID caseId, String documentType)`. The path is the baseline's own choice because no TSD P5 T-A.1 row and no Architecture v5 slide names a checked-field read, and the choice is recorded with its assumption.

The extract operation, the extract-state read and the fields read are declared by RWB-P5-E1053-CON with their own paths, rights and `Idempotency-Key` rule; the document read and the content read are RWB-P5-E1024-APP's. This baseline references them, consumes them as rows of 12.2 and re-declares none of them.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its queue and its team behind the scope filter of the read; one hop, 2 s, faked, and in no C row of the plan (`ASM-1906`) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | `EXTRACT_FIELD_THRESHOLD`, `EXTRACT_ACCURACY_PASS`, `EXTRACT_PRECISION_PASS`, `EXTRACT_RECALL_PASS`, `EXTRACT_MAX_ATTEMPTS`, `EXTRACT_TIMEOUT_SECONDS` and `BE_YEAR_OFFSET` (C `RWB-P3-E1042-CON`) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DOC-TYPE with the eleven types, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW (C `RWB-P3-E1043-CON`) |
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/extract` | P5 rwb-document, same service | The extraction of an item of a new type, consumed from RWB-P5-E1053-CON and never re-declared (`ASM-1905`) |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/extraction` | P5 rwb-document, same service | The extract state and the field set of an item, consumed from RWB-P5-E1053-CON |
| GET | `/api/recovery/document/v1/documents/{documentId}/fields` | P5 rwb-document, same service | The active fields of a document at the document level, consumed from RWB-P5-E1053-CON |

Every cross-service row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed case read maps to 503 with MSG-GEN-006 naming "Case service" and a failed list read to 503 with MSG-GEN-006 naming "Reference data", and a refusal never returns a partial field set. The case read is consumed and faked and is named in no C row of the plan, so it carries `ASM-1906` and no row is added to the metadata C list.

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 rwb-document | Key documentId, or intakeId when the item has no document; payload intakeId, documentId, documentType (with the codes of the new types), tableVersion, extractorVersion, extractedAt, fieldCount and fields [fieldName, confidence, state]; CloudEvents 1.0 binary mode; no field value, no personal value and no document text |

This baseline declares the event schema because the service owns the topic, and it declares no new property, no new type and no new topic for the new document types: the type codes travel in `documentType` (`ASM-1907`). The row itself is written by the extraction of RWB-P5-E1053-CON inside its own transaction, and this key publishes nothing at run time. The service's other event, `rwb.document.DocumentStored.v1`, is declared by the store baseline RWB-P5-E1024-APP; no third event exists for `rwb-document`.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The read is triggered by the S4 or S2 request, and the extraction by the intake Schedule and the HTTP request: nothing in this baseline subscribes to a topic. A change of the type table version reaches the read on its next call |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| None in this baseline | — | — | The checked-fields read is synchronous and declares no workflow and no activity. The `extract` and `evaluateExtraction` activity contracts and the `DocumentIntakeWorkflow` that calls them belong to RWB-P5-E1053-CON and RWB-P5-E1049-APP, and this key names them without declaring a second copy |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This baseline declares no Schedule and no cron entry; the intake Schedule is registered by RWB-P5-E1049-OPS and verified by RWB-P5-E2025-OPS |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `document_field` | P5 (`rwb_document`) | The `CheckedField` shape and the columns DF-DOC-012 to DF-DOC-017, DF-DOC-034 and DF-DOC-035 |
| `document_type` | P5 (`rwb_document`) | Contracted use only: `field_definitions` (DF-REF-224), `table_version` (DF-REF-229), `valid_from` (DF-REF-230), `valid_to` (DF-REF-231) and `classify_threshold` (DF-REF-233) behind the fixture and the version rule |
| `document` | P5 (`rwb_document`) | Contracted use only: `case_id` (DF-DOC-002) and `document_type` (DF-DOC-004) behind the read and the scope filter |
| `document_intake`, `document_text`, `document_hub_parameter` | P5 (`rwb_document`) | Contracted use only: the extraction state, the page text and the seven parameter names the extraction baseline and this read draw on |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The event envelope object behind the extraction declaration |

`recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `decision_log_entry` is P7's and the `agent_*` tables and the model route are P10's; they are named as consumed answers and never declared as this service's tables (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| checked-fields fake | The read for case "RW-2026-000601" and type "JUDGMENT" with `red_case_no` in OK, `judgment_amount` absent because it is in REVIEW, and a document of team "LIT-NE" for the 404 case | App story, S4 and S2 readers, contract tests |
| parameters and reference-data WireMock | `EXTRACT_FIELD_THRESHOLD` 0.80, `EXTRACT_ACCURACY_PASS` 0.90, the two pass marks, the three attempts, the 60-second timeout and the offset 543; LOV-DOC-TYPE with the eleven types and, on the earlier date, the six of DOCTYPE-2026.11; a delayed answer beyond 2 s and a 503 | App story, contract tests |
| rwb-case case WireMock | The case, its queue and its team for "RW-2026-000601" and for the document of team "LIT-NE", and a delayed answer beyond 2 s | App story, contract tests |
| extraction baseline fake | The three operations of RWB-P5-E1053-CON and the `FieldSet` shape, with the field set fixture of DOCTYPE-2026.11 | App story, contract tests |
| classification fake | `predicted_type` with the confidence and `review_reason` of an item of a new type, and the item with `review_reason` UNKNOWN_TYPE of the earlier date | App story, contract tests |
| agent field-extraction fake | Through RWB-P5-E1053-CON: a value and a confidence per field with the extractor version for a MODEL field, and the 60-second timeout on every attempt | App story, contract tests |
| drift and absence tests | Compare each fake and the fixture with the document and fail on a mismatch of a path, a status, a field name, a required flag, an enum value or a code count | Build pipeline |

A drifted fake fails the drift test of AC7, and a second operation or a fourth event fails the absence test of AC8. The exact response field names of the case read are Not specified in the source documents (`ASM-1906`); the fake fixes the names this baseline declares.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 cross-service consumed and 3 same-service consumed | The checked-fields read; the case read, the parameters read and the lists read; the three extraction operations of RWB-P5-E1053-CON; one hop and 2 s on every cross-service call |
| Kafka | 1 event schema declared, 0 consumed | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`; `DocumentStored` is the service's other event and is not this key's |
| Temporal | 0 declared, 2 named | The `extract` and `evaluateExtraction` activity contracts of RWB-P5-E1053-CON on queue `rwb-document`; no workflow and no Schedule |
| File | None | The contract carries no byte and no body: the field set is read from table rows and no blob is touched |

### 13. Solution plan

**Deliverables.** The OpenAPI 3.1 document `openapi/rwb-document-v1.yaml` with the checked-fields read and the two resources; the AsyncAPI 3.0 fragment for `rwb.document.DocumentFieldsExtracted.v1` with the eleven type codes; the field code fixture `contract/field-set-DOCTYPE-2026.12.json` with the 46 codes and the personal flag of `party_names`; the contract README rows for the state filter, the version rule, the masking rule, the error mapping and the event count; and the seven WireMock mapping sets of section 12.8.

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
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C, I and X lists of the metadata table are empty: this baseline adds no build dependency of its own (it is Day 1 by rule), and the platform and service contracts it names are the ones the app story declares. DP-01 is why the document declares six tables of `rwb_document` and no table of another service: the field rows, the type table and the parameter rows are this schema's and the case is a consumed answer. DP-06 and DP-07 are the two C rows: the seven parameters and the three lists are read through the `rwb-case` contracts and never typed into the document. DP-09 fixes the topic, the envelope and the one-event rule, so the new type codes travel in an existing payload property and no new schema is invented. DP-10 names the two activity contracts the extraction runs in and declares no timer. DP-11 is the whole point of this baseline: the Java interface `DocumentFieldReader` becomes one hop with a published shape, a fake and a 2 s timeout, so S4 and S2 build on Day 1 and the case scope arrives through a second consumed row rather than a cross-schema join. DP-13 gives the read the service base and removes the monolith base from the contract. DP-19 records that the checked fields reach SCR-30 and SCR-31 through the gateway-bff composite route; this baseline fixes the answer shape only and no route specification.

**Build steps**

1. Write the read with its path, parameters, resource and error responses; validate the document in the pipeline.
2. Fix the required and optional sets of AC2 and the four-decimal confidence as schema constraints and README rows.
3. Publish the field code fixture of AC3 from the type table version in force, with the 46 codes and the single personal flag, and compare it with the fixture of RWB-P5-E1053-CON.
4. Record the state filter, the version rule and the masking rule of AC4 as schema constraints and README rows.
5. Map every status and message ID of AC5 and record the RFC 9457 envelope.
6. Declare the event of AC6 with the absence test for a third event and the no-personal-value test.
7. Publish the seven fakes and the eight contract tests, including the drift and absence tests; tag the baseline and collect the consumer sign-off of RWB-P5-E2025-APP, the S4 and S2 readers and RWB-ITG-E2025-ITG.

**Done when.** The OpenAPI artefact and the AsyncAPI fragment validate in the pipeline, the eight contract tests pass, the seven fakes answer every operation and read of sections 12.1 and 12.2, the fixture carries the 46 codes, the drift and absence tests are green, and RWB-P5-E2025-APP and RWB-ITG-E2025-ITG have accepted the baseline.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-003 | A document has a field in review (a label, not an error) | Some fields need checking. The document is in the review queue. | 200 |
| MSG-P4-001 | No authenticated caller | You have no Recovery Workbench role. Ask your team manager to request one. | 401 |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Case or document outside the caller's scope | This case is not in your scope. | 404 |
| MSG-P5-006 | documentType is not in the version in force | {value} is not a document type in force. Choose a type from the list. | 422 |
| MSG-GEN-001 | An absent or empty documentType, or a body that fails validation | Enter {field}. | 422 |
| MSG-GEN-006 | The case read or the list read fails | {system} is not available. Your request is queued and will be retried. | 503 |

The message IDs and the wording are contract elements copied unchanged from RWB-E2-025 section 14 and the service messages of `rwb-document`; Thai text for each follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping fixed by AC5 is: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003, 422 with MSG-P5-006 or MSG-GEN-001, and 503 with MSG-GEN-006. For MSG-GEN-006 the {system} value is fixed by the consumed row that failed: "Case service" for the case read and "Reference data" for a list read. MSG-P5-003 is not an error response: it is the review label the screens show for a document with a field in REVIEW.

### 15. Screens and states

SCR-30 Case documents and SCR-31 Document review queue read the answers this baseline fixes, through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model; the screens, their forms and their actions are RWB-P5-E1026-APP and RWB-P5-E1054-APP. This baseline fixes the answer shapes only and declares no screen field list and no route specification.

| Screen state implied by the contract | What the answer carries |
|---|---|
| Case with checked fields of a stage 2 or 3 type | A `CheckedFieldSet` with the OK, CONFIRMED and CORRECTED fields of each document of the requested type |
| Document with a field in review | No REVIEW entry in the set, and the review label of MSG-P5-003 on the document |
| Personal field | An entry with `personal` true, and its value present only when the caller's masking rule allows it |
| Document of a type not in force | No entry, and the 422 of MSG-P5-006 when the requested type is not in the version in force |
| Document outside the caller's scope | No entry, and the 404 of MSG-P4-003 |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12 | AC1, AC5, X1 (legacy Access) | Contract | RW-REFADM user (Documents -) calls the checked-fields read; refused with 403 and MSG-P4-002, and nothing returned |
| TC-E2-025-01 | AC3, AC4 (legacy AC1) | Contract | The 10 court-notice labels of the sample answered by the fixture of the 46 codes; the accuracy pass mark 0.90 declared as a parameter name |
| TC-E2-025-02 | AC2, AC3, AC4 (legacy AC2) | Contract | Contract "DOC-0601" on case "RW-2026-000601": `party_names` present with personal true and masked, `contract_amount` 2400000.00 and `contract_date` 2026-11-01 |
| TC-E2-025-03 | AC2, AC4 (legacy AC3) | Contract | Judgment "DOC-0602" whose `judgment_amount` is at confidence 0.7100: the entry is absent from the set and the document carries the review label |
| TC-E2-025-04 | AC3, AC4 (legacy AC4) | Contract | 10 sample judgments, 8 amounts correct; the evaluation report reference and the proposed load file name, with no value in the contract |
| TC-E2-025-05 | AC3 (legacy AC5) | Contract | The classifier answer of the eleven types and the confusion-matrix report reference |
| TC-E2-025-06 | AC3, AC4 (legacy AC6) | Contract | A document received 2026-12-26 read against DOCTYPE-2026.11; a JUDGMENT code absent from that version answers 422 with MSG-P5-006 |
| TC-E2-025-07 | AC2, AC4 (legacy AC7) | Contract | A judgment date read as "2027-03-05" in `judgment_date` of the set |
| TC-E2-025-08 | AC3, AC4 (legacy AC8) | Contract | `red_case_no` "Por345-2570" absent from the set as REVIEW and "Por 345/2570" present as OK, both at confidence 0.9200 |
| TC-E2-025-09 | AC2, AC4 (legacy AC9) | Contract | A judgment with `red_case_no` in OK and `judgment_amount` in REVIEW; the set carries the first and never the second |
| TC-E2-025-10 | AC2, AC4 (legacy AC10) | Contract | A write-once judgment: the read returns its fields and the answer carries no storage reference, no hash and no write-once switch |
| TC-E2-025-11 | AC4, AC5 (legacy AC11) | Contract | Document "DOC-0605" of team "LIT-NE" read by an officer of team "LIT-BKK"; 404 with MSG-P4-003 |

The twelve legacy test cases of RWB-E2-025 are listed in the order of the work package and the legacy story; each is answered here at contract level against the artefact and the fakes, and its business outcome is proved by RWB-P5-E2025-APP. The legacy level System maps to Contract because the artefact under test is the contract, and the legacy level Access maps to Contract likewise; the app story answers the two at End to end and Component. The integration harness copies end in `-ITG` and belong to RWB-ITG-E2025-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the types, the 46 field codes, the patterns, the threshold, the pass mark, the extraction methods and the review-only flags stay rows of the type table and the parameter table.
- No personal data in a schema, an example or a fake: identifiers, codes, versions, dates, confidences and states only; `party_names` is declared as a code with no value, and no customer name, account number or title-doc number is declared in clear.
- No field value and no document text in an event, an example or a log: the payload carries field names, confidences and states; the read carries a value only behind masking and the access log.
- The extraction operations are consumed from RWB-P5-E1053-CON and never re-declared; a second extract operation fails the absence test.
- Only the two events of `rwb-document` exist; the new type codes travel in `documentType` and no fourth event or payload property is added.
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this document declares no ACE view and no cross-schema join.
- The contract names only `rwb_document` tables and only operations owned by `rwb-document`; every other read is consumed and faked, never declared as provided (DP-01, DP-11).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review.
- Every example in the document is synthetic and the legacy values are examples only; no production payload is copied into a schema or a fake.
- The contract declares no case state and no extraction state machine; a transition belongs to the app story that performs it.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | The checked-fields read, `CheckedField`, `CheckedFieldSet`, the 46-code fixture, the state filter and the event declaration | TC-E2-025-01, TC-E2-025-02, TC-E2-025-04, TC-E2-025-05, TC-E2-025-07, TC-E2-025-09 |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | The REVIEW exclusion of the read, the version rule of the type table and MSG-P5-003 as a label | TC-E2-025-03, TC-E2-025-06, TC-E2-025-08 |
| REQ-DCM-017 | The discovery response for a named population, with metadata and version history | The version rule (`documentVersion`, `docVersion`) declared on the shapes the discovery read will use | TC-E2-025-10, TC-E2-025-11 |
| REQ-DCM-018 | What a court needs to accept a document: origin, entry date, alteration status and readers | Declared as the boundary of section 19: the contract fixes the field shapes and adds no court-evidence attribute | TC-E2-025-12 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables declared; the case read consumed and faked |
| DP-06 | The parameters row of 12.2 and the seven parameter names |
| DP-07 | The reference-list row of 12.2 and the three lists |
| DP-09 | The event declaration of 12.3, the CloudEvents envelope and the no-field-value rule |
| DP-10 | The two activity contracts named from RWB-P5-E1053-CON and no Schedule |
| DP-11 | The four consumed rows with one hop, a 2 s timeout and a fake |
| DP-13 | The base `/api/recovery/document/v1` of the read |
| DP-19 | SCR-30 and SCR-31 behind gateway-bff |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E2-025; its AC1 to AC11 are owned by RWB-P5-E2025-APP, and the cross-service proof of the same values is RWB-ITG-E2025-ITG.

### 19. Out of scope

- The build of the extraction extension, the checked-fields read and the evaluation runner: RWB-P5-E2025-APP.
- The three extraction operations, the `FieldSet` shape and the field set fixture of the Epic 1 types: RWB-P5-E1053-CON and RWB-P5-E1053-APP.
- The type table itself, the DOCTYPE-2026.12 load, its Legal and NPA sign-off and the review-only proposal load: RWB-P5-E1025-APP and the reference data administrator.
- The classification model, its contract and its classifier version: RWB-P5-E1050-APP and RWB-P5-E1050-CON.
- The review queue, the correction of a field and the states CONFIRMED and CORRECTED: RWB-P5-E1054-APP and RWB-P5-E1054-CON.
- The store, the document read and the content read: RWB-P5-E1024-APP.
- OCR, the workflow template and its 15-minute Schedule: RWB-P5-E1049-APP and RWB-P5-E1049-OPS.
- The `rwb-agent` runtime, the prompts, the model route and the provider: P10 `rwb-agent` and RWB-P10-TE013-CON.
- The chart, the values, the Schedule verification, the dashboards, the alerts and the runbook: RWB-P5-E2025-OPS.
- The cross-service proof of these values with S4 and S2 live: RWB-ITG-E2025-ITG.
