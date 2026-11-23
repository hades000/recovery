# RWB-P5-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2025-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P5-Y |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P5-E2025-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P5-E1053-CON, RWB-P5-E1050-CON, RWB-P5-E1054-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P5-E2025-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-015, FR-P5-016, FR-P5-017, FR-P5-018, FR-P5-027, FR-P5-028, FR-P5-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the stage 2 and 3 extraction extension of RWB-E2-025 moves into `rwb-document` with the schema `rwb_document`, the REST base `/api/recovery/document/v1`, the topic `rwb.document.events.v1`, the `extract` and `evaluateExtraction` activities of `DocumentIntakeWorkflow` on queue `rwb-document` and the contract baseline RWB-P5-E2025-CON; the eleven legacy criteria, the twelve exception paths, the eight business rules, the seven messages and the twelve test cases are kept word for word in intent and values, and the legacy published interface `DocumentFieldReader` becomes the checked-fields read of the published contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **field extraction extended to the stage 2 and 3 types: contracts, credit approvals, mortgage documents, court filings, hearing notices and judgments**, so that **the litigation pack and the treatment record fill themselves**.

Inside `rwb-document` this is the stage 2 and 3 extension of the field-extraction capability, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document` (DP-01, DP-13).
- The five new types and the extended hearing-notice field list are rows of `document_type` in the version in force, not code and not a deployment: version DOCTYPE-2026.12 is loaded and signed off through the type table of RWB-P5-E1025-APP and is read locally by `valid_from` and `valid_to`, because the type table is P5's own table (DP-01, ASM-1896).
- The extraction parameters `EXTRACT_FIELD_THRESHOLD` = 0.80, `EXTRACT_ACCURACY_PASS` = 0.90, `EXTRACT_PRECISION_PASS` = 0.90, `EXTRACT_RECALL_PASS` = 0.90, `EXTRACT_MAX_ATTEMPTS` = 3, `EXTRACT_TIMEOUT_SECONDS` = 60 and `BE_YEAR_OFFSET` = 543 stay rows of `document_hub_parameter` in `rwb_document`, and are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON; ASM-1897).
- The value lists LOV-DOC-TYPE with the eleven types, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW are read as reference data through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON). No list value is typed in code.
- The extension runs inside the Epic 1 extraction path unchanged: the `extract` activity of `DocumentIntakeWorkflow` reads the field definitions of the type in the version in force, calls the extractor named by `extraction_method`, normalizes the value and writes `document_field` rows (RWB-P5-E1053-CON, H). This story adds the field definitions of the new types; it adds no code per type and no second extractor (ASM-1896).
- A MODEL field is reached only through the rwb-agent contract route that RWB-P5-E1053-CON already consumes, with the masked text of the classification step; this package holds no model client, no prompt and no provider key, and the provider, the model name and the model version behind the route are Not specified in the source documents (ASM-1902).
- The classifier version that knows the eleven types is the one RWB-P5-E1050-CON fixes; this story runs no training and holds no classifier (ASM-1900).
- The legacy published interface `DocumentFieldReader` becomes the checked-fields read of the contract: `GET /api/recovery/document/v1/cases/{caseId}/checked-fields` on the service base, consumed by S4 `rwb-litigation` and S2 `rwb-treatment` through RWB-P5-E2025-CON, one hop with a 2 s timeout, never an in-process Java call across a service boundary (DP-11, DP-13, ASM-1898).
- The case, its queue and its team behind the scope check arrive through the `rwb-case` contract `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E1018-CON, one hop, 2 s timeout, DP-11), never from a case table of another service; the case read is consumed and faked although the plan lists it in no C row of this key (ASM-1899).
- The extraction writes `rwb.document.DocumentFieldsExtracted.v1` (EV-17) to the outbox in the same transaction as the field rows (DP-09, H RWB-PLT-TE006-CON); the event carries field names, confidences and states, never a field value and never a personal value.
- JOB-12 Document intake stays a Temporal Schedule started through the workflow kit (DP-10, H RWB-PLT-E1071-CON); `extract` and `evaluateExtraction` are activities of `DocumentIntakeWorkflow` on queue `rwb-document`, owned and registered by RWB-P5-E1049-APP, and this story extends the two activities and creates no Schedule of its own.
- The extension adds one index and no table and no column; the index is created by this service's own per-service Flyway step in `rwb_document` (DP-15 is not in this key's pattern list because the legacy plan adds no column; the index is carried by the sequence of RWB-P5-E1053-CON). The checked fields of a document and the new types on SCR-30 and SCR-31 reach the screens through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (ASM-1747); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.
- The legacy feature flag `rwb.dochub.extraction-stage23` is retired with the monolith and replaced by `rwb.document.extract-stage23` (ASM-1901).

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, eight exception paths, eight business rules, four messages, authority, data fields, eleven acceptance criteria and twelve test cases, adapted to the target service's schema, topic, API base, activity names and contract baseline.

### 2. Business rationale

The litigation pack and the treatment record need the contract amount, the mortgage registration, the black and red case numbers, the hearing dates and the judgment amount, which officers read from paper and type in today. This story adds five document types to classification and extraction and extends the hearing notice fields, using the Epic 1 extraction and review path, so these values reach the case index with a confidence and a person checks only the uncertain ones. It meets REQ-DCM-006 and REQ-DCM-005 for the stage 2 and 3 types, and prepares the pack assembly of R-LIT-16 and the treatment documents of FEAT-TRT-18 (FSD P5 A2.22).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). The four tables the legacy step touched are P5 tables, the case is never read from a case table, and the monolith document read of legacy AC11 is replaced by the document read of the service base.
2. The five new types and their fields are data rows of `document_type` in the version in force and never a class per type: DOCTYPE-2026.12 is prepared through the type table of RWB-P5-E1025-APP and signed off by legal counsel and the Head of NPA (DL19; ASM-1896).
3. The step is no longer a Quartz job step inside `ExtractStep`: it is the `extract` activity of `DocumentIntakeWorkflow` on the service's own task queue, started by the 15-minute Schedule that RWB-P5-E1049-APP owns, and the row lock of the activity is what keeps two workers off one item (DP-10).
4. The published Java interface `DocumentFieldReader` becomes one hop of REST with a mock and a fixed answer shape (DP-11): the checked-fields read of 12.1. S4 and S2 read the checked fields of a case and a type through that operation and never through an in-process call (ASM-1898).
5. The parameters and the three lists come from the parameters and reference-data contracts of `rwb-case` through the client libraries of DP-06 and DP-07, so neither the pass mark nor a type code is written in code.
6. `DocumentFieldsExtracted` (EV-17) stays the one event of the extraction path and is written to the outbox in the same transaction as the new field rows (DP-09); the new type codes travel in `documentType` and the payload still carries no value.
7. The five new types reach SCR-30 and SCR-31 through the gateway-bff composite route (DP-19), one call to the owner, exactly as the Epic 1 types do.
8. The release date 31 December 2026 is the legacy date and is tentative (ASM-1895), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1747).

Two target-service statements fix the shape of the work. No code path is added per type: a new type is a load with its fields, its `classify_threshold`, its `extraction_method`, its `review_only` flag and its optional pattern, so a new version changes behaviour with no deployment. And the extension never changes a stored file: it writes table rows only, so the write-once rule of RWB-P5-E1024-APP holds through the new types as it holds through the six Epic 1 types (CTL-12).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2025-CON | The published baseline of the checked-fields read, the `CheckedField` and `CheckedFieldSet` shapes, the eleven-type field code fixture, the state filter and masking rule, the error envelope and the fakes |
| RWB-P5-E1053-CON | The extraction operations and the field set fixture of the Epic 1 path: the extract operation, the extract-state read, the fields read, the `FieldSet` shape and the event schema this story extends |
| RWB-P5-E1050-CON | The classification contract with `predicted_type`, `classification_confidence`, `review_reason` and the classifier version that knows the eleven types |
| RWB-P5-E1054-CON | The review contract, which reads an extraction state and corrects a field in REVIEW; this story writes the REVIEW state and stops there |
| RWB-PLT-E1042-CON | The parameters client library for the seven extraction parameters of section 13 (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-DOC-TYPE, LOV-EXTRACT-STATUS and LOV-INTAKE-REVIEW (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so the field rows and the event share one transaction (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 "Document intake" template, the activity registration and the retry policy that host `extract` and `evaluateExtraction` (DP-10) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the checked fields to SCR-30 and SCR-31 (DP-19) |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the seven parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the three lists (DP-07) |
| RWB-P3-E1018-CON | The `rwb-case` contract `GET /cases/{caseId}`, with its fake, for the case, its queue and its team behind the scope check; consumed and faked, and in no C row of the plan (ASM-1899) |
| RWB-P5-E2025-OPS | The Helm release, the values, the service identity credential of the agent route, the dashboards, the alerts and the runbook (the X dependency) |

Business preconditions carried from RWB-E2-025, in the target wording:

- RWB-E1-050 (classifyStep), RWB-E1-053 (extractStep, extractors, normalizer, evaluation runner) and RWB-E1-054 (review queue) are done. In the target these are RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1054-CON in the same service, and the classification answer is read from the intake row instead of through an in-process call.
- A document type table version DOCTYPE-2026.12 is prepared through the RWB-E1-025 loader with the five new types, their classify_threshold and their field_definitions (section 13), signed by legal counsel and the Head of NPA (assumed list; DL19). Hearing notices stay under the Epic 1 type COURT_NOTICE. The load is applied through the type table of RWB-P5-E1025-APP (ASM-1896).
- A labeled sample of 60 documents, 10 for each of the five new types and 10 court notices, is in the SIT test data store, masked (RWB-TE-004) (ASM-1903).
- The classifier version that knows the new types is trained on the sample and selected through the agent runtime (P10); in the target it is the version RWB-P5-E1050-CON fixes (ASM-1900).
- The pass mark for field accuracy is 0.90 per field on the sample (`document_hub_parameter` EXTRACT_ACCURACY_PASS, assumed; DL11); the row stays in `rwb_document` and is read through DP-06 (ASM-1897).
- DL30 names the Workbench squads as the builder of stage 2 and 3 extraction where no bank-wide service exists; this story assumes option A.
- Feature flag `rwb.document.extract-stage23` is on; it replaces the legacy `rwb.dochub.extraction-stage23` (ASM-1901).
- The release date 31 December 2026 is the legacy one and is tentative (ASM-1895), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1747).

The path and the shapes of the checked-fields read, and the precise field-level names of the checked-field set beyond the legacy interface list, are Not specified in the source documents (ASM-1898); the baseline RWB-P5-E2025-CON fixes the names this story is built against.

### 4. Flow

1. Reference data administrator: loads DOCTYPE-2026.12 with valid from 2026-12-31 after approval, through the type table of RWB-P5-E1025-APP; the rows carry the five new types, their `classify_threshold` and their field definitions.
2. JOB-12 Document intake: the 15-minute business-hours Schedule starts `DocumentIntakeWorkflow` on queue `rwb-document`; the workflow runs `ingest`, `ocr`, `classify`, `extract` and `matchStep` in that order (DP-10). An inbound contract, credit approval, mortgage document, court filing, hearing notice or judgment passes the scan and OCR steps of RWB-P5-E1049-APP.
3. `classify` (RWB-P5-E1050-CON): the classifier version for the eleven types returns a type and a confidence; below the `classify_threshold` of the type the item goes to the review queue with reason LOW_CONFIDENCE.
4. `extract` activity (RWB-P5-E1053-CON, extended by this story): reads the field definitions of the type from `document_type` in the version in force on the business date (`valid_from`, `valid_to`) and calls the extractor named by `extraction_method`; a TEMPLATE field runs in this package, a MODEL field is one hop to the rwb-agent route the Epic 1 baseline already consumes.
5. System: normalizes each value (`ValueNormalizer`, `BE_YEAR_OFFSET` 543), checks it against the field pattern held in the type table, and writes `document_field` rows with confidence and state.
6. System: a field below the threshold, failing its pattern or marked `review_only` gets state REVIEW, the document gets `review_status` PENDING and the document goes to the review queue.
7. `matchStep` (RWB-P5-E1032-APP): stores the document with its fields through the store of RWB-P5-E1024-APP; for a document already attached the extraction writes its field rows directly and `DocumentFieldsExtracted` (EV-17) is written to the outbox in the same transaction (DP-09).
8. Litigation officer: sees the fields on SCR-30 through the gateway-bff composite route, and checks the marked ones on SCR-31 in the review queue of RWB-P5-E1054-APP (DP-19).
9. S4 and S2: read confirmed field values through the checked-fields read of 12.1 on the contract RWB-P5-E2025-CON to fill the pack and the treatment record (from Epic 3 and Epic 5), one hop with a 2 s timeout and no in-process call (DP-11).
10. Outbox relay: publishes `rwb.document.DocumentFieldsExtracted.v1` to `rwb.document.events.v1` once per committed extraction, keyed by the document ID or the intake item ID, with field names, confidences and states and no value.

The field rows and the outbox row commit together or not at all, so an item is never marked DONE with no fields and no event is published for a set of fields that does not exist. The extraction reads and writes only `rwb_document` and calls two contracts of other services: the reference data and parameters of `rwb-case`, and the case behind the scope check; the model path is the Epic 1 agent route and not a new client of this story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field is below the threshold | Field state REVIEW; document in the review queue with the field marked | MSG-P5-003 | AC3 |
| X2 | A field's accuracy on the sample is below the pass mark | Field proposed as review-only in the next table version | None | AC4 |
| X3 | A value does not match the field pattern | Field state REVIEW | MSG-P5-003 | AC8 |
| X4 | A document arrives before the new table version is in force | Classified against the earlier version; goes to review with reason UNKNOWN_TYPE | MSG-P5-003 | AC6 |
| X5 | A reader asks for fields still in REVIEW | Only fields in state OK, CONFIRMED or CORRECTED are returned | None | AC9 |
| X6 | The document is write-once | Fields are written; the file and write_once are unchanged | None | AC10 |
| X7 | The document is outside the caller's scope | 404 | MSG-P4-003 | AC11 |
| X8 | A role without Documents R reads the document | 403 | MSG-P4-002 | Access test TC-E2-025-12 |

Three target-service notes:

- X4 is executed by the version rule of `document_type`: a document received on 2026-12-26 is classified and extracted against DOCTYPE-2026.11, the classifier answers a type that version does not hold, and the item reaches the review queue with `review_reason` UNKNOWN_TYPE. No fallback type is invented and no later version is applied to an earlier date.
- X2 is executed by `evaluateExtraction`, which writes the report and a proposed DOCTYPE load file against `EXTRACT_ACCURACY_PASS` 0.90; the version in force changes only through the approved load of RWB-P5-E1025-APP, never by the activity, so AC4's "the version in force does not change until it is loaded" holds.
- A `rwb-case` read that times out at 2 s, answers 503 or meets an open breaker fails the checked-fields read with 503 and MSG-GEN-006 naming "Case service"; the extraction itself is unaffected because it reads its case from the intake row and never makes that call (ASM-1899).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the Epic 1 extraction and review path (RWB-P5-E1053-CON, RWB-P5-E1050-CON, RWB-P5-E1054-CON) and adds data, a classifier version and one published reader |
| Negotiable | Types, fields, patterns and pass marks are data rows and parameters; the shapes come from the contract baseline |
| Valuable | Pack and treatment values reach the case without typing, for the types the litigation and treatment stages use |
| Estimable | One table version, one classifier version, field patterns, two extended activities, one published read |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with the labeled sample or synthetic documents |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types

  Background:
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the labeled sample holds 60 documents: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE
    Given the rwb-case contract mock returns the parameters EXTRACT_FIELD_THRESHOLD 0.80 and EXTRACT_ACCURACY_PASS 0.90
    Given the rwb-case contract mock returns LOV-DOC-TYPE with the eleven types, LOV-EXTRACT-STATUS with PENDING, DONE and FAILED, and LOV-INTAKE-REVIEW
    Given the rwb-agent field-extraction fake of RWB-P5-E1053-CON answers a value and a confidence per field with the extractor version
    Given the rwb-document classification contract mock of RWB-P5-E1050-CON answers the classifier version for the eleven types
    Given the rwb-case contract mock returns the case of document "DOC-0605" in team "LIT-NE"

  Scenario: AC1 Court notice (legacy RWB-E2-025 AC1)
    Given the 10 scanned court notices of the sample with 30 labeled values of court_name, black_case_no and hearing_date
    When extraction runs
    Then court, case number and hearing date are on the index
    Then at least 27 of the 30 values match the labels, which is 90% field accuracy on the sample

  Scenario: AC2 Contract (legacy RWB-E2-025 AC2)
    Given a signed contract "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300
    Given its text names two parties, amount "2,400,000.00 baht" and date "1 December 2569 BE"
    When extraction runs
    Then party_names holds the two party names, masked in responses for roles without the right
    Then contract_amount is "2400000.00" and contract_date is "2026-11-01"

  Scenario: AC3 Low confidence (legacy RWB-E2-025 AC3)
    Given a judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100
    When extraction runs
    Then judgment_amount has state "REVIEW"
    Then the document is in the review queue on SCR-31 with judgment_amount marked
    Then SCR-30 shows MSG-P5-003 on "DOC-0602"

  Scenario: AC4 A field below the pass mark is proposed as review-only (legacy RWB-E2-025 AC4)
    Given judgment_amount matches the labels on 8 of the 10 sample judgments
    When the extraction evaluation run processes the sample
    Then the report lists judgment_amount at 0.80, below the pass mark 0.90
    Then the proposed table version marks judgment_amount review_only = true
    Then the version in force does not change until it is loaded

  Scenario: AC5 Classification into the new types (legacy RWB-E2-025 AC5)
    Given the 50 sample documents of the five new types
    When classification runs with the new classifier version
    Then the system gives each document one of the eleven types with a confidence
    Then the report shows the confusion matrix and at least 45 of 50 correct

  Scenario: AC6 A document before the new version is in force (legacy RWB-E2-025 AC6)
    Given a judgment "DOC-0603" received on 2026-12-26, before the valid-from date of "DOCTYPE-2026.12"
    Given the rwb-case reference-data contract mock returns the six types of "DOCTYPE-2026.11" for that date
    When it is classified and extracted
    Then the system classifies it against the six types of "DOCTYPE-2026.11"
    Then the classifier returns "JUDGMENT", which is not in that version, so the item goes to the review queue with review_reason "UNKNOWN_TYPE"

  Scenario: AC7 A Thai judgment date in Buddhist Era (legacy RWB-E2-025 AC7)
    Given a judgment whose text reads "Judgment at 5 March 2570 BE"
    When extraction runs
    Then judgment_date is "2027-03-05"

  Scenario: AC8 A value that does not match its pattern (legacy RWB-E2-025 AC8)
    Given the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits
    Given the extractor reads red_case_no "Por345-2570" with confidence 0.9200
    When extraction runs
    Then red_case_no has state "REVIEW"
    Then a value "Por 345/2570" with confidence 0.9200 has state "OK"

  Scenario: AC9 Readers get only checked or confident values (legacy RWB-E2-025 AC9)
    Given judgment "DOC-0602" has red_case_no in state "OK" and judgment_amount in state "REVIEW"
    When the S4 litigation reader calls the checked-fields read of the rwb-document contract for case "RW-2026-000601" and type "JUDGMENT"
    Then the system returns red_case_no
    Then the system does not return judgment_amount until it is confirmed or corrected

  Scenario: AC10 A write-once document is not altered (legacy RWB-E2-025 AC10)
    Given judgment "DOC-0604" is held write-once with write_once true
    When extraction runs
    Then the system writes four document_field rows
    Then the stored file hash, storage_ref and write_once are unchanged

  Scenario: AC11 A document outside the caller's scope (legacy RWB-E2-025 AC11)
    Given a litigation officer with scope team "LIT-BKK"
    Given document "DOC-0605" belongs to a case of team "LIT-NE"
    When the officer calls GET /api/recovery/document/v1/documents/DOC-0605
    Then the response is 404 with MSG-P4-003
```

Every Given, When and Then line above is the legacy line unchanged. The added lines are the six Background mock Givens on the parameters, reference-data, agent, classification and `rwb-case` parts that are mocked in this build, the one reference-data Given in AC6 that fixes the version in force on the earlier date, and two mechanic rebases: the AC9 When line names the checked-fields read instead of the in-process `DocumentFieldReader`, and the AC11 When line carries the service base `/api/recovery/document/v1` instead of the monolith base. The legacy AC2 pairs the text "1 December 2569 BE" with contract_date "2026-11-01" and AC7 converts "5 March 2570 BE" to "2027-03-05"; both values are copied character for character from the legacy story and the normalisation rule of BR8 is the only conversion this story applies. The legacy step names map as follows: `ExtractStep` is the `extract` activity of `DocumentIntakeWorkflow`; `classifyStep` is the classification of RWB-P5-E1050-CON; `MatchStep` and `DocumentStore` are RWB-P5-E1032-APP and RWB-P5-E1024-APP; `DocumentFieldReader` is the checked-fields read of 12.1; and `Scr-30`/`SCR-31` are reached through the gateway-bff composite route.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the extraction date | Document types reference table; DL19; R-UNI-38 |
| BR2 | A field below the threshold, failing its pattern, or marked review-only has state REVIEW and sends the document to the review queue | RWB-E1-053 BR2, BR3; REQ-DCM-005 |
| BR3 | A field whose accuracy on the sample is below the pass mark is proposed as review-only; the proposal takes effect only when loaded | EXTRACT_ACCURACY_PASS (0.90 assumed); DL11; CTL-08 |
| BR4 | Each field may carry a pattern in field_definitions; the pattern is data | Principle 1; RWB-E1-053 BR5 |
| BR5 | Readers in other modules receive only fields in state OK, CONFIRMED or CORRECTED | FEAT-DCM-10 |
| BR6 | Extraction never changes the stored file of a write-once document | CTL-12 |
| BR7 | Party names and other personal field values are masked unless the role may see them | DF-DOC-015; CTL-11; DL26 |
| BR8 | Dates read in Buddhist Era are stored as ISO dates | RWB-E1-053 BR6 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by reading `document_type.field_definitions` for the type in the version in force (`valid_from`, `valid_to`) on the business date, locally in `rwb_document` (DP-01); the type row and the field list are never taken from the caller and never through a contract hop, which is why a new version changes behaviour with no deployment (ASM-1896).
- BR2, BR3 and BR5 are executed per field inside one extraction of the Epic 1 path: the threshold and the pass marks come from `document_hub_parameter` through DP-06, the `review_only` flag, the `extraction_method` and the pattern come from the field definition, and the data type comes from the field definition. No threshold, pattern or flag is a constant in the package.
- BR3 is executed by `evaluateExtraction`, which writes the evaluation report and a proposed DOCTYPE load file; the version in force changes only through the approved load of RWB-P5-E1025-APP (AC4).
- BR4 is executed by `ValueNormalizer`, which applies the optional pattern of the field definition and treats a failed pattern as REVIEW with the confidence kept (AC8).
- BR5 is executed twice: in the extraction, where only OK, CONFIRMED or CORRECTED rows are active for a reader, and in the checked-fields read, whose query filters on those three states and never returns a REVIEW row (AC9).
- BR6 is executed because the extension writes table rows only: no blob path, no content reference and no container is written, and the write-once rule of RWB-P5-E1024-APP is untouched (AC10).
- BR7 is executed by the `personal` flag of the field definition, by the masking rule the cached permission decision of `rwb-access` holds, and by the read operations of 12.1; a log line carries the intake item ID, the field name and the confidence, never the value.
- BR8 is executed by `ValueNormalizer` with `BE_YEAR_OFFSET` 543 read through DP-06; an unconvertible value is kept and reviewed and is never silently dropped (AC7).
- The three lists arrive through DP-07, so a type code, a state or a review reason is a reference row and never a constant in this package.

### 9. State transitions

None for the case. This story does not change a case status. It sets document_field.state and document.review_status as in RWB-E1-053.

| From | Event | Condition | To |
|---|---|---|---|
| `document_field.state` = (no row) | `extract` writes a field of a type in the version in force | The confidence is at or above `EXTRACT_FIELD_THRESHOLD` and the value converts and matches its pattern | OK |
| `document_field.state` = (no row) | `extract` writes a field of a type in the version in force | Below the threshold, `review_only`, unconvertible or failing its pattern | REVIEW |
| `document.review_status` = NOT_NEEDED | A field of that document is written in REVIEW | The document is already attached | PENDING |
| `document_intake.extract_status` = PENDING | `extract` processes an item of a new type | The field set is written | DONE |
| `document_intake.extract_status` = PENDING | The model route fails on every attempt | No partial field set is written | FAILED, with `review_reason` EXTRACTION_FAILED |
| `document_field.is_active` = true | A new version of the document is extracted | The type is one of the eleven | false, and new active rows are written for the new version |

The transitions out of REVIEW, to CONFIRMED or CORRECTED, belong to RWB-P5-E1054-APP; this story writes the state REVIEW and stops there. The document state machine COPY_PENDING to STORED belongs to RWB-P5-E1024-APP and is not changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Classifies and extracts the new types (Documents CRU) |
| RW-LITOFF, litigation officer | Reads and checks the fields in scope (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads and checks contract, credit approval and mortgage fields in scope (Documents CRU) |
| RW-REFADM, reference data administrator | Loads DOCTYPE-2026.12 (Reference data CRUD) |
| Business lead with Legal | Approves the new type and field list (DL19) |
| RW-COE, center of excellence analyst | Reads the evaluation report |

In the target the authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds behind gateway-bff; this story adds no guard of its own and inherits the 403 shape of MSG-P4-002 and the 404 shape of MSG-P4-003. The type load of RW-REFADM is applied through the type table of RWB-P5-E1025-APP and not by this story. The extraction and the checked-fields read run as the rwb-document service identity (DP-02), carried by the chart as a secret reference; the login name is Not specified in the source documents (ASM-1747). S4 `rwb-litigation` and S2 `rwb-treatment` call the checked-fields read under their own service identity through the contract RWB-P5-E2025-CON.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read |
| DF-DOC-002 | `document` | case_id | Read |
| DF-DOC-004 | `document` | document_type | Read |
| DF-DOC-006 | `document` | storage_ref | Read |
| DF-DOC-008 | `document` | review_status | Write |
| DF-DOC-010 | `document` | write_once | Read |
| DF-DOC-012 to DF-DOC-017 | `document_field` | all fields | Write |
| DF-DOC-034 | `document_field` | extracted_value | Write |
| DF-DOC-035 | `document_field` | extractor_version | Write |
| Standard column | `document_field` | state, is_active | Write |
| DF-DOC-070 | `document_intake` | predicted_type | Write (by the classification of RWB-P5-E1050-CON with the new classifier version) |
| DF-DOC-071 | `document_intake` | classification_confidence | Write (by the classification of RWB-P5-E1050-CON with the new classifier version) |
| DF-DOC-080 | `document_intake` | review_reason | Write (by the classification of RWB-P5-E1050-CON with the new classifier version) |
| DF-DOC-077 | `document_intake` | extracted_fields | Write |
| DF-DOC-078 | `document_intake` | extract_status | Write |
| DF-DOC-063 | `document_intake` | ocr_status | Read |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-224 | `document_type` | field_definitions | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-REF-230 | `document_type` | valid_from | Read |
| DF-REF-231 | `document_type` | valid_to | Read |
| DF-REF-233 | `document_type` | classify_threshold | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read, resolved through DP-06 |
| (outbox) | outbox library table in `rwb_document` | the row for DocumentFieldsExtracted (EV-17) | Write, through the library |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `recovery_case` row is copied and no ACE view is read by this service: the case, its queue and its team arrive inside the `rwb-case` contract answer for the scope check, and DP-01 forbids a foreign-schema read. Personal data never enters the event payload, the workflow input or the log: `party_names` and the other personal values of a type are masked in a read by role and replaced by the field name in a log line, and the event carries field names, confidences and states only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E2025-CON.

| Method | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/checked-fields` | P5 | The checked fields of a case and a document type for S4 and S2 (the legacy `DocumentFieldReader.checkedFields`): query `documentType` required and `documentVersion` optional; answer 200 `CheckedFieldSet` of the fields in state OK, CONFIRMED or CORRECTED, personal values masked by role, Documents R with scope applied, each read written to the access log. The path is the baseline's own choice and is Not specified in the source documents (ASM-1898) |

The extract operation, the extract-state read and the fields read of the Epic 1 path are declared by RWB-P5-E1053-CON and implemented by RWB-P5-E1053-APP; this story extends the field set they run against and declares no second copy of them. The document read `GET /documents/{documentId}` and the content read are the operations of RWB-P5-E1024-APP.

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1018-CON | The case, its queue and its team behind the scope check of the checked-fields read; one hop, 2 s timeout, breaker per downstream, one GET retry with jitter (DP-11); consumed and faked and in no C row of the plan (ASM-1899) |
| GET | the parameters read of DP-06 | P3 behind the client library | RWB-P3-E1042-CON | `EXTRACT_FIELD_THRESHOLD`, `EXTRACT_ACCURACY_PASS`, `EXTRACT_PRECISION_PASS`, `EXTRACT_RECALL_PASS`, `EXTRACT_MAX_ATTEMPTS`, `EXTRACT_TIMEOUT_SECONDS`, `BE_YEAR_OFFSET`, cached for 5 minutes |
| GET | the reference-data read of DP-07 | P3 behind the client library | RWB-P3-E1043-CON | LOV-DOC-TYPE with the eleven types, LOV-EXTRACT-STATUS, LOV-INTAKE-REVIEW |
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/extract` | P5 rwb-document, same service | RWB-P5-E1053-CON | Re-runs one extraction with the type given, which is the review queue's type-change path on a new type |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/extraction` | P5 rwb-document, same service | RWB-P5-E1053-CON | The extract state and field set the review queue of RWB-P5-E1054-APP reads |
| POST | the field-extraction route of the rwb-agent contract | P10 rwb-agent | RWB-P10-TE013-CON | A raw value and a confidence per field with the extractor version for a MODEL field; consumed through the client of RWB-P5-E1053-CON only, with the masked text and the 60-second budget; this story adds no client and no provider key (ASM-1902) |

Every consumed cross-service row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020); the agent route is the one declared exception, with the 60-second `EXTRACT_TIMEOUT_SECONDS` budget per attempt and at most `EXTRACT_MAX_ATTEMPTS` 3 attempts, because the Epic 1 baseline fixes it. A failed case read maps to 503 with MSG-GEN-006 naming "Case service" and returns no field.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` (EV-17), one per committed extraction of an item of any of the eleven types | `rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 | documentId, or the intake item ID when the item is not yet attached | intakeId, documentId, documentType with the new type code, tableVersion, extractorVersion, extractedAt, fieldCount and the field entries of fieldName, confidence and state; CloudEvents 1.0 envelope, binary mode; no field value, no personal value and no document text |

The event schema is the one RWB-P5-E1053-CON declares; this story adds the type codes of the new version to the values that travel in `documentType` and adds no event, no payload property and no topic. The row is written to the outbox inside the extraction transaction, so the event exists exactly when the field rows exist, and the once-per-extraction guarantee rests on the outbox relay and the consumer inbox of DP-09.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The extension is started by the intake Schedule and the HTTP request, not by an event: the classification answer is read from the intake row, and the OCR text is a `document_text` row. `rwb.document.DocumentFieldsExtracted.v1` is consumed by `rwb-case` for the search index, not by this story |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | Observed: OCR, classify, extract, match; owned and registered by RWB-P5-E1049-APP, which also owns its 15-minute Schedule |
| `extract` | Activity | `rwb-document` | Extended by this story: the field list of the eleven types comes from `document_type` in the version in force; the Epic 1 code path, the extractor interface and the normalizer are unchanged |
| `evaluateExtraction` | Activity | `rwb-document` | Extended by this story: field accuracy against `EXTRACT_ACCURACY_PASS` and the confusion matrix of the classifier over the 60-document sample |

This story registers no workflow and no activity of its own: both activities exist in the Epic 1 path and are extended in place, so the queue, the retry policy and the build ID remain the ones of RWB-P5-E1049-APP and RWB-P5-E2025-OPS.

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None in this story | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | The intake Schedule is registered and monitored by RWB-P5-E1049-OPS and RWB-P5-E2025-OPS; this story contributes the extended activities the Schedule-started workflow calls and registers no timer of its own |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_type` | P5 | Read only: the five new types, their `classify_threshold`, their field definitions, `extraction_method`, `review_only` and the optional pattern in the version in force |
| `document_field` | P5 | Written: the field rows of the new types with value, confidence, state, extractor version and `is_active` |
| `document_intake` | P5 | Read for the selection, the type and the OCR state; written for `extracted_fields`, `extract_status` and `extract_attempts` |
| `document_text` | P5 | Read only: the OCR page text and quality of the item |
| `document_hub_parameter` | P5 | Read only through the parameters contract of DP-06; the rows are P5's |
| `document` | P5 | Read for the type, the write-once flag and the version; written for `review_status` only |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The DocumentFieldsExtracted row and the `Idempotency-Key` row of the extract operation |

No foreign-schema table is read (DP-01) and no ACE view is read by this service. `document_type`, `document_field` and `document_hub_parameter` are P5's under the Ownership Map; the `agent_*` tables, the prompts and the model route are P10's and are named as consumed answers only.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | `EXTRACT_FIELD_THRESHOLD` 0.80, `EXTRACT_ACCURACY_PASS` 0.90, the two pass marks, the three attempts, the 60-second timeout and the offset 543 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-TYPE with the eleven types and, on the earlier date, the six types of DOCTYPE-2026.11; LOV-EXTRACT-STATUS; LOV-INTAKE-REVIEW |
| classification fake | RWB-P5-E1050-CON | `predicted_type`, `classification_confidence`, `review_reason` and the classifier version for the eleven types |
| agent field-extraction fake | RWB-P10-TE013-CON through RWB-P5-E1053-CON | A value and a confidence per field with the extractor version for a MODEL field; the 60-second timeout path |
| extraction baseline fake and field set fixture | RWB-P5-E1053-CON | The three extraction operations and the `FieldSet` shape the new types are written through |
| rwb-case case fake | RWB-P3-E1018-CON | The case, its queue and its team behind the scope check of AC11 and the 2 s timeout path |
| type table fixture | This story's test harness | DOCTYPE-2026.12 with the five new types and the extended COURT_NOTICE field list, and DOCTYPE-2026.11 for AC6 |
| checked-fields baseline fake | RWB-P5-E2025-CON | The single read and the `CheckedFieldSet` shape, so the tests build before the app code lands |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 2 cross-service plus 2 in-service plus 1 through the Epic 1 client | The checked-fields read; the `rwb-case` case read, the parameters read and the lists read; the extract operation and the extract-state read of the same service; the agent route through the Epic 1 client for a MODEL field |
| Kafka | Published 1, consumed 0 | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1`, with the new type codes in `documentType` |
| Temporal | 1 workflow observed, 2 activities extended, 0 Schedules | `DocumentIntakeWorkflow` with `extract` and `evaluateExtraction` on queue `rwb-document` |
| File | None | The extension reads `document_text` rows and touches no blob and no container, so the write-once rule is untouched |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, modules `document/extract` and `document/checkedfields`, Java package `th.co.scb.ace.workbench.recovery.document`, extending RWB-E1-053 and RWB-P5-E1053-CON.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentFieldController | Controller | The checked-fields read of 12.1: the Documents R check, the scope filter, the masking and the RFC 9457 error mapping |
| CheckedFieldService | Service | Applies BR5 and BR7: only OK, CONFIRMED or CORRECTED rows, personal values masked by role, each read written to the PII access log |
| StageTypeCatalog | Library client | Reads `document_type` in the version in force for the eleven types and the seven parameter rows in `rwb_document`; the Epic 1 reader extended, with no code per type |
| ExtractActivity (extended) | Temporal activity | The `extract` activity of the Epic 1 path with the field definitions of the new versions; the selection lock, the states and the writes are unchanged |
| ExtractionEvaluationRunner (extended) | Service | Field accuracy against `EXTRACT_ACCURACY_PASS` and the confusion matrix for the classifier over the 60-document sample; writes the report and the proposed load file |
| DocumentFieldRepository (extended) | Repository | Query by case, type and state for the reader; writes `document_field` for the new types and marks earlier version rows inactive |

**Database.**

- No new table and no new column: the extension writes `document_field`, `document_intake` and `document` as the Epic 1 path does (RWB-E1-053 section 13).
- One index in the per-service Flyway sequence of RWB-P5-E1053-CON, applied by the release of RWB-P5-E2025-OPS: `ix_document_type_case ON document (case_id, document_type)` for the checked-fields read.
- The type table version DOCTYPE-2026.12 is a data load, not a migration: it is applied through the type table of RWB-P5-E1025-APP and changes no schema (ASM-1896).

**Configuration and reference data.**

- Document type table version DOCTYPE-2026.12 (RWB-E1-025 loader, now the type table of RWB-P5-E1025-APP), loaded by RW-REFADM, signed by legal counsel and the Head of NPA (DL19). Assumed new types and fields: CONTRACT (contract_no, party_names, contract_amount, contract_date); CREDIT_APPROVAL (approval_no, approved_amount, approval_date, approval_level); MORTGAGE_DOCUMENT (title_doc_no, mortgage_amount, registration_date, land_office); COURT_FILING (court_name, black_case_no, filing_date, claim_amount); JUDGMENT (court_name, red_case_no, judgment_date, judgment_amount). COURT_NOTICE keeps court_name, black_case_no, notice_date and hearing_date from DOCTYPE-2026.11. Each field has data type, method, review_only and an optional pattern (ASM-1896).
- `document_hub_parameter` row `EXTRACT_ACCURACY_PASS` 0.90 (assumed; DL11), loaded by the reference data administrator and read through DP-06 together with the six Epic 1 extraction parameters (ASM-1897).
- Classifier version for the eleven types, selected through the agent runtime (P10) and fixed by RWB-P5-E1050-CON, which this story runs unchanged (ASM-1900).
- Feature flag `rwb.document.extract-stage23` (ASM-1901). Off: the new types are not offered to classification and the checked-fields read returns nothing for them; the six Epic 1 types are unaffected.

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

DP-01 moves the four tables the legacy step touched (`document`, `document_field`, `document_intake`, `document_text`) plus the two reference tables into `rwb_document`, and it removes the cross-module read of the OCR output, the type catalogue and the case: the type table and the text are read locally in the version in force and the case arrives through its contract. DP-06 keeps the pass mark and the six Epic 1 parameters out of the code through the client library, while the rows stay in `rwb_document` as the Ownership Map gives them to P5. DP-07 keeps the three lists behind the `rwb-case` contract, so a type code or a review reason is a reference row and never a constant. DP-09 puts `DocumentFieldsExtracted` in the outbox inside the extraction transaction and fixes the CloudEvents envelope and the one-event rule. DP-10 replaces the legacy `ExtractStep` job step with the `extract` activity of the kit's "Document intake" template, started by the Schedule that RWB-P5-E1049-APP owns, so the legacy Quartz job, its scheduler row and its second timer do not exist. DP-11 turns the in-process `DocumentFieldReader` into the checked-fields read: one hop, a published shape, a fake in the build and a 2 s timeout, so S4 and S2 build against the contract on Day 1 and never link a Java interface of this service. DP-13 gives the service its own base and removes the monolith path from AC11. DP-19 puts SCR-30 and SCR-31 behind the gateway-bff composite route, so the screens call the document service once.

**Build steps**

1. Prepare the load file for DOCTYPE-2026.12 with a test case per new row; validate it in SIT against the type table of RWB-P5-E1025-APP.
2. Add the patterns of the new fields to the load file; unit test the two red-case-number values of AC8 against `ValueNormalizer` of the Epic 1 path.
3. Add the new types to the extractor configuration through the type table only; prove with a regression run of the RWB-E1-053 tests that the six Epic 1 types are unchanged.
4. Extend `evaluateExtraction` with field accuracy against the pass mark and the confusion matrix; run it on the 60-document sample in SIT and attach the report (AC1, AC4, AC5).
5. Build the checked-fields read and `CheckedFieldService` with the state filter, the scope filter and the masking; test AC9 and AC11 against the case fake and the access test TC-E2-025-12.
6. Confirm the REVIEW path of AC3 and the write-once path of AC10 against the Epic 1 extraction and store stubs, and confirm that the event payload of a new type carries no value.
7. Test the flag-off path (ASM-1901) and confirm that the Epic 1 types still extract with the flag off.

**Done when.** The tests in section 16 pass, the evaluation report for the 60-document sample is attached to the story, the regression set of RWB-E1-053 is green for the six Epic 1 types, and `rwb.document.DocumentFieldsExtracted.v1` is on the topic once per extraction of a new type with no field value in the payload.

### 14. Validation and messages

| ID | When | Message | HTTP status |
|---|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW, or an item went to review for UNKNOWN_TYPE | Some fields need checking. The document is in the review queue. | 200 |
| MSG-P4-001 | No authenticated caller | You have no Recovery Workbench role. Ask your team manager to request one. | 401 |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. | 404 |
| MSG-P5-006 | The checked-fields read is asked for a type that is not in the version in force | {value} is not a document type in force. Choose a type from the list. | 422 |
| MSG-GEN-001 | A required query parameter is empty | Enter {field}. | 422 |
| MSG-GEN-006 | The case read fails or times out | {system} is not available. Your request is queued and will be retried. | 503 |

MSG-P5-003, MSG-P4-002, MSG-P4-003 and MSG-GEN-006 are the legacy texts of RWB-E2-025 section 14 and are unchanged; Thai text for each message follows decision DL10. MSG-P4-001, MSG-P5-006 and MSG-GEN-001 are the service and platform messages already in force in this service, used here with their agreed wording, and none of them adds a business value.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one, fixed by AC11 and the baseline RWB-P5-E2025-CON: 401 with MSG-P4-001, 403 with MSG-P4-002, 404 with MSG-P4-003, 422 with MSG-P5-006 or MSG-GEN-001, and 503 with MSG-GEN-006 naming "Case service". MSG-P5-003 is not an error response: it is the review notice carried by a 200 answer whose field list holds at least one REVIEW row, and it is the text SCR-30 and SCR-31 show.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-30 Case documents | List | Sees the new types with their fields and confidence; MSG-P5-003 on documents with fields in review |
| SCR-30 Case documents | Fields of one document | Sees the active field rows of a new type with data type, value, confidence, state and extractor version; a personal value is masked unless the role may see it |
| SCR-31 Document review queue | List; reviewed | Checks and corrects marked fields of the new types (RWB-E1-054, now RWB-P5-E1054-APP) |
| SCR-31 Document review queue | Item of a new type with no agreed type | Sees the item with `reviewReason` UNKNOWN_TYPE and no field, and the action to set the type and re-run the extraction through the extract operation of RWB-P5-E1053-CON |

The case document list, its search and its upload form are RWB-P5-E1026-APP; the correction of a field and the review states CONFIRMED and CORRECTED are RWB-P5-E1054-APP. This story fixes the fields and the states those screens read and adds no screen of its own; both screens are reached through the gateway-bff composite route (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12 | X8, Access | Component | RW-REFADM user (Documents -) calls GET /documents/{documentId}; refused with MSG-P4-002 |
| TC-E2-025-01 | AC1, BR1 | End to end | 10 masked court notices from the sample, 30 labeled values |
| TC-E2-025-02 | AC2, BR7, BR8 | End to end | Synthetic signed contract with two parties, amount 2,400,000.00 and date 1 December 2569 BE |
| TC-E2-025-03 | AC3, BR2 | End to end | Judgment with amount at confidence 0.71 |
| TC-E2-025-04 | AC4, BR3 | End to end | 10 sample judgments, 8 amounts correct, pass mark 0.90 |
| TC-E2-025-05 | AC5 | End to end | 50 sample documents of the five new types; classifier version for the eleven types |
| TC-E2-025-06 | AC6, BR1 | End to end | Judgment received 2026-12-26, the day before the valid-from date |
| TC-E2-025-07 | AC7, BR8 | End to end | Judgment dated 5 March 2570 BE |
| TC-E2-025-08 | AC8, BR4 | End to end | Red case numbers "Por345-2570" and "Por 345/2570" |
| TC-E2-025-09 | AC9, BR5 | End to end | Judgment with one OK field and one REVIEW field, read through the checked-fields read |
| TC-E2-025-10 | AC10, BR6 | End to end | Write-once judgment "DOC-0604" |
| TC-E2-025-11 | AC11 | End to end | Document "DOC-0605" of team LIT-NE, officer of team LIT-BKK |

The legacy level System maps to End to end and the legacy level Access maps to Component. The same twelve test case IDs are answered at contract level by RWB-P5-E2025-CON, and the wave 2 integration harness RWB-ITG-E2025-ITG copies the cross-service proof with the `-ITG` suffix. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: types, fields, patterns, thresholds and pass marks are data and parameters, read through DP-06 and DP-07; there is no class per document type.
- No personal data in logs, tests or prompts: party names and amounts never enter a log or an event, the sample is masked (RWB-TE-004), and a log line carries the intake ID, the field name and the confidence only.
- No read of another module's tables: S4 and S2 read through the checked-fields read, this service reads the case through the P3 contract, and P5 writes nothing to `legal_action`, `hearing` or `treatment` (DP-01).
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this story declares no ACE view and no cross-schema join.
- No model client, prompt or provider key in this package: a MODEL field is the rwb-agent route already consumed by RWB-P5-E1053-CON (ASM-1902).
- The extraction writes table rows only: a write-once document is never altered (BR6, CTL-12).
- The event carries no field value and no personal value, and the type codes of the new version travel in `documentType` only.
- The Epic 1 types keep their results: the RWB-E1-053 tests run unchanged in the regression suite, and the flag of this story does not touch them.
- The feature flag `rwb.document.extract-stage23` removes the new types without a rollback of the schema or of the type table (ASM-1901).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, R-LIT-16 | TC-E2-025-01, TC-E2-025-02, TC-E2-025-04 to TC-E2-025-12 |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38 | TC-E2-025-03, TC-E2-025-05, TC-E2-025-06, TC-E2-025-09 |
| REQ-DCM-017 | The hub answers an electronic discovery request with every document of a named population, its metadata and its version history | Business Requirements Epic 2, section 3.5 (carried by the plan for this key) | FEAT-DCM-22 | 13 Manage documents and correspondence | R-LIT-16 | Carried as the boundary of section 19; the discovery response itself is out of scope |
| REQ-DCM-018 | A document produced from the hub carries what a court needs to accept it: origin, entry date, alteration status and readers | Business Requirements Epic 2, section 3.5 (carried by the plan for this key) | FEAT-DCM-22 | 13 Manage documents and correspondence | R-LIT-16 | Carried as the boundary of section 19; the court-evidence attributes are out of scope |

| Legacy reference | Where it is kept |
|---|---|
| `DocumentFieldReader.checkedFields(UUID caseId, String documentType)` and `CheckedField` | Sections 1, 4, 12.1, 13 |
| DocumentFieldsExtracted (EV-17) | Sections 1, 4, 12.3, 17 |
| The document read of AC11 on the legacy monolith base | Section 7, rebased to `/api/recovery/document/v1/documents/{documentId}` |
| MSG-P5-003, MSG-P4-002, MSG-P4-003, MSG-GEN-006 | Section 14 and the exception paths |
| Parameters EXTRACT_FIELD_THRESHOLD 0.80 and EXTRACT_ACCURACY_PASS 0.90 | Background, sections 1, 3, 8, 13 |
| Type table version DOCTYPE-2026.12 with the five new types and the extended COURT_NOTICE list | Background, sections 3, 7, 13 |
| Rules R-UNI-38, R-LIT-16, CTL-08, CTL-11, CTL-12, DL10, DL11, DL19, DL26, DL30 | Sections 2, 8, 17, 18 |
| Legacy key RWB-E2-025, AC1 to AC11, TC-E2-025-01 to TC-E2-025-12 | Metadata, section 7, section 16 |

### 19. Out of scope

- Writing extracted values into `legal_action`, `hearing` or `treatment` (S4 in Epic 5, S2 in Epic 3); this story serves those reads through the checked-fields read only.
- Litigation pack assembly and the defect list check (FEAT-LIT-04, FEAT-LIT-05, Epic 5).
- Generation of contract, credit approval and mortgage documents (RWB-P5-E2026-APP).
- Electronic discovery and the court evidence attributes (REQ-DCM-017, REQ-DCM-018).
- The type table itself, its Legal and NPA sign-off and the review-only proposal load (RWB-P5-E1025-APP).
- OCR, classification and the Epic 1 extraction code path (RWB-P5-E1049-APP, RWB-P5-E1050-APP or RWB-P5-E1053-CON), which this story extends only through data.
- The correction of a field in REVIEW and the states CONFIRMED and CORRECTED (RWB-P5-E1054-APP).
- The published contract documents, the fakes and their versioning (RWB-P5-E2025-CON).
- The `rwb-agent` runtime, the prompts, the model route and the provider (P10 `rwb-agent` and RWB-P10-TE013-CON).
- The store, the document read and the content read (RWB-P5-E1024-APP); the match and attach step (RWB-P5-E1032-APP).
- The chart, the values, the Schedule verification, the dashboards, the alerts and the runbook (RWB-P5-E2025-OPS).
- The cross-service proof of these values with S4 and S2 live (RWB-ITG-E2025-ITG).
