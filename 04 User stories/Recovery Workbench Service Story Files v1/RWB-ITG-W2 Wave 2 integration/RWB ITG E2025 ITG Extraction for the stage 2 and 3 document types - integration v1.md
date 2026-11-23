# RWB-ITG-E2025-ITG Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-025 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2025-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E2025-APP, RWB-P7-E2025-APP, RWB-S4-E2025-APP, RWB-S2-E2025-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-005, REQ-DCM-017, REQ-DCM-018) |
| Status | Draft (realignment v1) |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service journey harness for the extraction of the stage 2 and 3 document types, with the extraction, review and reader evidence attached to the wave 2 release**, so that **the journey of a contract, credit approval, mortgage document, court filing, hearing notice or judgment, from intake through classification and field extraction to the litigation reader and the treatment reader, is proven end to end across rwb-document, rwb-decision, rwb-litigation and rwb-treatment before the app stories of RWB-E2-025 are signed off**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, screen, table or migration. The classifier, the extractor and the review queue stand behind the rwb-document contract; the harness proves that the values those steps produce arrive at the readers of the two route services with a confidence, in the right state and in the right form.

### 2. Business rationale

RWB-E2-025 splits into four app stories and this integration story. RWB-P5-E2025-APP extends classification and extraction inside rwb-document to the new types, adds the field patterns, the review queue and the reader. RWB-S4-E2025-APP consumes the checked fields in rwb-litigation to fill legal actions, hearings and judgments. RWB-S2-E2025-APP consumes them in rwb-treatment for the contract and mortgage values of the treatment record. RWB-P7-E2025-APP records the decisions those steps take. Not one of them can prove on its own that a value read off a scanned court notice travels from intake to the litigation pack, or that a judgment amount read at low confidence is withheld from a reader until a person has checked it. That proof is this story.

The journey is the one the business cares about. A contract, a credit approval, a mortgage document, a court filing, a hearing notice or a judgment arrives; it is classified into one of the eleven types with a confidence; each field is extracted with its own confidence and checked against the pattern held in the type table; a person checks only the uncertain ones; and the checked values reach the case index, the litigation reader and the treatment reader without anyone typing an amount or a date (REQ-DCM-006, REQ-DCM-005). The harness runs that journey against the published contracts of the four services on one business date and produces evidence that can be re-run for any build. REQ-DCM-017 and REQ-DCM-018 enter only as the shape of the journey: the documents, their versions and their dates are the inputs the harness stages, and the electronic discovery answer and the court evidence attributes are not extracted fields and are not asserted here.

The architecture changes the path, not the business. The monolith wrote document_field rows and handed them to the litigation and treatment modules inside one process and one schema. In the target, rwb-document owns the metadata, the OCR text, the fields and the retention (DP-01, schema `rwb_document`); every other service reads fields through the document contract, one hop on `/api/recovery/document/v1` with a 2 s timeout (DP-11, DP-13); the case facts behind the journey come from rwb-case through its contract, including the parameters and the reference data of the type table (DP-06, DP-07); JOB-12 Document intake runs as an event-started workflow, `DocumentIntakeWorkflow` on queue `rwb-document`, so OCR, classification and extraction happen off the request path (DP-10); the document events leave through the outbox on `rwb.document.events.v1` (DP-09); and the screens the officers use are composite routes of gateway-bff, so the same bases the harness calls are the ones the screens call (DP-19). The harness is the place where those boundaries are exercised together, so a broken boundary is found in SIT and not by a litigation officer who cannot see the judgment date.

The measure is the journey evidence: for each owned criterion, one pass or fail with the intake request, the document read, the field rows and their states, the review item, the reader answer at rwb-litigation and at rwb-treatment, and the decision log entry captured in one report.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topics `rwb.document.events.v1` and `rwb.decision-record.v1`, the task queue `rwb-document` and the Azure Blob write-once container behind rwb-document. The harness environment, its seeding and its evidence format: Not specified in the source documents (GAP-0407; ASM-0582).
- The four integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P5-E2025-APP (rwb-document), RWB-P7-E2025-APP (rwb-decision), RWB-S4-E2025-APP (the rwb-litigation reader) and RWB-S2-E2025-APP (the rwb-treatment reader).
- Document type table version DOCTYPE-2026.12 is in force from 2026-12-31 with the eleven types, each with its classify_threshold and its field_definitions. Hearing notices stay under the Epic 1 type COURT_NOTICE. Types and fields: CONTRACT (contract_no, party_names, contract_amount, contract_date); CREDIT_APPROVAL (approval_no, approved_amount, approval_date, approval_level); MORTGAGE_DOCUMENT (title_doc_no, mortgage_amount, registration_date, land_office); COURT_FILING (court_name, black_case_no, filing_date, claim_amount); JUDGMENT (court_name, red_case_no, judgment_date, judgment_amount); COURT_NOTICE (court_name, black_case_no, notice_date, hearing_date). Each field carries data type, extraction method, review_only and an optional pattern (legacy section 13; DL19).
- The field threshold is 0.80 and the accuracy pass mark is 0.90 per field on the sample; document_hub_parameter row EXTRACT_ACCURACY_PASS holds 0.90 (legacy sections 3, 7 and 13; DL11).
- The masked sample of 60 documents is staged and masked: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE (legacy section 7 Background; RWB-TE-004).
- The classifier version that knows the eleven types is selected through the P10 agent runtime, so the classification run has a version to name in the evidence (legacy section 3).
- The feature switch `rwb.dochub.extraction-stage23` is on in the harness profile (legacy section 13).
- Synthetic and masked documents only: no real party name, account number or case document enters the harness or its evidence (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the four contracts it is about to exercise.
2. Harness: seeds the 60-document masked sample and the DOCTYPE-2026.12 rows (the eleven types, their thresholds, field definitions and patterns in force on the business date) through the seed pack.
3. Harness: records the session it runs under for each test officer (RW-LITOFF of team "LIT-BKK", RW-RESTRUCT, RW-REFADM), with the role, the scope and the Documents right it will exercise.
4. Harness: calls the P3 case operation and records the case state of "RW-2026-000601" and of the team each document belongs to, as the journey starts from it.
5. Harness: uploads each sample document through the P5 intake operation, `POST /api/recovery/document/v1/cases/{caseId}/documents`, and records the document ID and the returned upload reference; the file itself is handed to Azure Blob through the link rwb-document returns, never by the harness writing a blob.
6. Harness: waits for the extraction window (JOB-12, `DocumentIntakeWorkflow` on queue `rwb-document`) and records the intake state, the predicted type, the classification confidence and the review reason the intake read returns.
7. Harness: reads each document through `GET /api/recovery/document/v1/documents/{documentId}` and records the type, the review status, the write-once flag, the storage reference and every field with its value, confidence and state.
8. Harness: reads the review items of the run through `GET /api/recovery/document/v1/review-items` and records which fields of which document are waiting, with the message the read carries.
9. Harness: confirms or corrects one marked field through `POST /api/recovery/document/v1/documents/{documentId}/review` and, where the correction changes a value, through `PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId}`, then records the state the field moves to.
10. Harness: reads the checked fields as the rwb-litigation reader does, for case "RW-2026-000601" and type "JUDGMENT", and again as the rwb-treatment reader does for the contract values, and records exactly which fields each answer holds and which it withholds.
11. Harness: reads the decision log through `GET /api/recovery/decision/v1/decision-log` and records whether the decision entry of the reviewed field exists with its decision code and final call.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record and releases the run lock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field is below the threshold of 0.80 | The field gets state REVIEW and one review item appears on the P5 review operation for the document | MSG-P5-003 | AC3 |
| X2 | A field's accuracy on the sample is below the pass mark of 0.90 | The field is proposed as review_only in the next table version; the version in force does not change until it is loaded | None | Legacy AC4 (RWB-P5-E2025-APP) |
| X3 | A value does not match the pattern of its field | The field gets state REVIEW and one review item appears | MSG-P5-003 | AC6 |
| X4 | A document arrives before the valid-from date of DOCTYPE-2026.12 | It is classified against the earlier version and goes to review with review_reason UNKNOWN_TYPE | MSG-P5-003 | Legacy AC6 (RWB-P5-E2025-APP) |
| X5 | A reader asks for fields still in REVIEW | The answer holds only fields in state OK, CONFIRMED or CORRECTED; the review field is absent, not blank | None | AC4 |
| X6 | The document is write-once | The field rows are written; the file hash, the storage_ref and write_once are unchanged | None | AC7 |
| X7 | The document is outside the caller's scope | The P5 read answers 404 and the harness records it as the expected answer, not as a run failure | MSG-P4-003 | AC8 |
| X8 | A role without Documents R reads the document | The read answers 403 | MSG-P4-002 | TC-E2-025-12-ITG |
| X9 | The seeded data cannot be loaded (type table row missing, sample document absent, case not as the scenario states) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X10 | The evidence pack cannot be attached to the release record | The run is marked failed; the local evidence file is kept for the rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four published contracts or their fakes and the SIT harness profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded sample values and the type table rows are data files, never code |
| Valuable | The extraction journey is proven once across four services, before the app stories claim Done |
| Estimable | One journey runner, one fake set, one sample pack, one assertion set per reader and one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded result in the run report |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types

  Background:
    Given the harness runs in SIT with the contract of rwb-document, rwb-case and rwb-decision, or their fakes
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the masked sample holds 60 documents: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE

  Scenario: AC1 Court notice accuracy across the service boundary (new, D-RCV-60)
    Given the 10 masked court notices of the sample with 30 labelled values of court_name, black_case_no and hearing_date
    When the sample is taken through the P5 intake operation and the extraction window of JOB-12 closes
    Then court_name, black_case_no and hearing_date are on the case index read through the P5 document operation
    Then at least 27 of the 30 values match the labels, which is 0.90 field accuracy on the sample

  Scenario: AC2 Contract fields on the case index (new, D-RCV-60)
    Given a signed contract "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300
    Given its text names two parties, amount "2,400,000.00 baht" and date "1 December 2569 BE"
    When extraction runs and the harness reads the document through the P5 document operation
    Then contract_amount is "2400000.00" and contract_date is "2026-11-01"
    Then party_names holds the two party names, masked in the answer for a role without the right

  Scenario: AC3 A field below the threshold goes to review (new, D-RCV-60)
    Given a judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100
    When extraction runs
    Then judgment_amount has state "REVIEW"
    Then the P5 review operation returns one review item for "DOC-0602" with judgment_amount marked
    Then the document read carries MSG-P5-003 on "DOC-0602"

  Scenario: AC4 The S4 reader gets only checked values (new, D-RCV-60)
    Given judgment "DOC-0602" has red_case_no in state "OK" and judgment_amount in state "REVIEW"
    When the rwb-litigation reader asks for the checked fields of case "RW-2026-000601" and type "JUDGMENT"
    Then the answer holds red_case_no
    Then the answer holds no judgment_amount until it is confirmed or corrected

  Scenario: AC5 A Thai judgment date in Buddhist Era (new, D-RCV-60)
    Given a judgment whose text reads "Judgment at 5 March 2570 BE"
    When extraction runs and the harness reads the document through the P5 document operation
    Then judgment_date is "2027-03-05"

  Scenario: AC6 A value that does not match its pattern (new, D-RCV-60)
    Given the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits
    Given the extractor reads red_case_no "Por345-2570" with confidence 0.9200
    When extraction runs
    Then red_case_no has state "REVIEW"
    Then a value "Por 345/2570" with confidence 0.9200 has state "OK"

  Scenario: AC7 A write-once document is not altered (new, D-RCV-60)
    Given judgment "DOC-0604" is held write-once with write_once true
    When the sample is taken through the P5 intake operation and extraction runs
    Then the document read holds four document_field rows for "DOC-0604"
    Then the file hash, the storage_ref and write_once are unchanged

  Scenario: AC8 A document outside the caller's scope (new, D-RCV-60)
    Given a litigation officer with scope team "LIT-BKK"
    Given document "DOC-0605" belongs to a case of team "LIT-NE"
    When the officer calls GET /api/recovery/document/v1/documents/DOC-0605
    Then the response is 404 with MSG-P4-003
```

The legacy ACs of RWB-E2-025 are owned by the four app stories of this legacy key. Legacy AC4 (a field below the pass mark proposed as review-only), legacy AC5 (classification into the new types with the confusion matrix) and legacy AC6 (a document before the valid-from date) are cited in the flow and exception table because the harness stages their inputs, and they stay with RWB-P5-E2025-APP. The eight criteria above are the ones this ITG story owns, and each tests only the integration deliverable.

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

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code.

### 9. State transitions

None. This story does not change a case status and no service state moves because of the harness. It observes document_field.state (OK, REVIEW, CONFIRMED, CORRECTED) and document.review_status as the P5 operations set them, and it asserts the state a field is in after each read.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Classifies and extracts the new types as the P5 contract describes (Documents CRU); the harness asserts the answer and never calls the classifier directly |
| RW-LITOFF, litigation officer | Reads and checks the fields in scope as the test officer of team "LIT-BKK" (Documents CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads and checks the contract, credit approval and mortgage fields in scope (Documents CRU) |
| RW-REFADM, reference data administrator | Loads DOCTYPE-2026.12 and holds the Reference data right; the negative access case runs under this role |
| RW-COE, center of excellence analyst | Reads the run report and the field accuracy it records |
| Business lead with Legal | Approves the type and field list the sample is labelled against (DL19) |
| Integration lead | Agrees the fake versions of the four contracts with the owning service teams and signs off the boundary assertions |
| QA lead | Owns the sample pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read through the P5 document operation |
| DF-DOC-002 | document | case_id | Read through the P5 document operation |
| DF-DOC-004 | document | document_type | Read through the P5 document operation |
| DF-DOC-006 | document | storage_ref | Read through the P5 document operation; compared before and after extraction in AC7 |
| DF-DOC-008 | document | review_status | Read through the P5 document and review operations |
| DF-DOC-010 | document | write_once | Read through the P5 document operation |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Read through the P5 document operation; written by rwb-document, never by the harness |
| DF-DOC-034 | document_field | extracted_value | Read through the P5 document operation |
| DF-DOC-035 | document_field | extractor_version | Read through the P5 document operation |
| DF-DOC-070 | document_intake | predicted_type | Read through the P5 intake read |
| DF-DOC-071 | document_intake | classification_confidence | Read through the P5 intake read |
| DF-DOC-077 | document_intake | extracted_fields | Read through the P5 intake read |
| DF-DOC-078 | document_intake | extract_status | Read through the P5 intake read |
| DF-DOC-080 | document_intake | review_reason | Read through the P5 intake read |
| DF-REF-219, DF-REF-224, DF-REF-233 | document_type | doc_type_code, field_definitions, classify_threshold | Seeded for the rwb-document fake from the type table; read through the P5 contract when the real service is in the harness |
| DF-REF-246 | document_hub_parameter | param_value | Read through the P5 contract as the pass mark of the evaluation |
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |

The harness owns no table in any schema (DP-01). It reads and writes only through the published operations of section 12, and its evidence holds identifiers, statuses, confidences and timestamps only, never personal data. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | Reads the document, its type, its review status, its write-once flag and every field with its state (AC2, AC3, AC5, AC6, AC7) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Reads the document set of the case and the index the litigation reader sees (AC1, AC4) |
| GET | `/api/recovery/document/v1/review-items` | P5 rwb-document | Asserts that the low-confidence field produced one review item (AC3) |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | P5 rwb-document | Confirms or corrects a marked field and records the state it moves to (AC4) |
| PATCH | `/api/recovery/document/v1/documents/{documentId}/fields/{fieldId}` | P5 rwb-document | Corrects the value of one field where the scenario corrects rather than confirms (AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case state the journey starts from and the team the case belongs to (AC8) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the decision entry of the reviewed field with its decision code and final call (flow step 11) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout and the breaker of DP-11, and the two write calls carry an Idempotency-Key per scenario. The case document set read, `GET /api/recovery/document/v1/cases/{caseId}/documents`, is the index that the SCR-30 list consumes, so AC1 and AC4 assert it and not only the single-document read. The harness also reads the session of each test officer through `GET /api/recovery/access/v1/me/session` (P4 rwb-access) to record the role, the scope and the Documents right the journey runs under; that call is the harness's identity step, is not asserted as a journey outcome, and is therefore not one of the seven rows above. The intake upload of flow step 5 is `POST /api/recovery/document/v1/cases/{caseId}/documents`, the operation named by RWB-P5-E2025-APP; the harness uses it to stage the sample and does not assert it beyond the document ID it returns.

#### 12.3 Events published

None. The harness publishes no Kafka event; the evidence goes to the release record through its pipeline integration.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Confirms that the intake of each sample document reached the topic inside the run window, so the extraction window of JOB-12 can be waited on deterministically |
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` | P5 rwb-document | Confirms that the field rows of each document were written and offered to the consumers, alongside the document read of 12.2 (DP-09) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | Confirms that the reviewed field's decision reached the shared ledger topic inside the run window |

The harness subscribes with its own consumer group and asserts the event, never the producer's table. A duplicate is expected and deduplicated on the harness side, so a re-run of the same business date is deterministic.

#### 12.5 Workflows and activities

JOB-12 Document intake is observed, not built. The harness waits for the `DocumentIntakeWorkflow` on queue `rwb-document` to finish OCR, classification and extraction for the sample, and records the intake state and the time the window took. JOB-11 Outbox sender is observed too: the harness waits for the relay window and records that the two document events and the decision record left their outboxes.

No workflow is built, no activity is added and no schedule is created by this story. The classifier and extractor runs behind `DocumentIntakeWorkflow` belong to RWB-P5-E2025-APP; the harness records their version from the field rows it reads.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow. JOB-12's own trigger is rwb-document's and is only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-document | The five document operations of 12.2 | OpenAPI of P5 | The document with its type, review status, write-once flag and fields at the confidences and states of the scenario; 404 with MSG-P4-003 for the out-of-scope document; 403 with MSG-P4-002 for the role without Documents R; the review item and the state after a confirm or a correction |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | Case "RW-2026-000601", its team and its state, and the team of the case that holds "DOC-0605" |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The decision entry of the reviewed field with its decision code and final call |
| Classifier stand-in | The classify step inside `DocumentIntakeWorkflow` | The P5 internal contract, not in this workspace | A type and a confidence per sample document, with "JUDGMENT" for "DOC-0602" and "DOC-0603" and "CONTRACT" at 0.9300 for "DOC-0601" |
| Extractor stand-in | The extract step inside `DocumentIntakeWorkflow` | The P5 internal contract, not in this workspace | The field values, confidences and states of the scenario, including judgment_amount at 0.7100, red_case_no at 0.9200 and judgment_date "2027-03-05" |
| rwb-litigation reader consumer | The reader contract RWB-S4-E2025-APP publishes | OpenAPI of S4 | The checked fields it received for case "RW-2026-000601" and type "JUDGMENT", recorded in the evidence |
| rwb-treatment reader consumer | The reader contract RWB-S2-E2025-APP publishes | OpenAPI of S2 | The checked contract fields it received for the case, recorded in the evidence |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. The harness repository, its environment, the fake versions and the evidence format: Not specified in the source documents (GAP-0407; ASM-0582).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed and asserted, one hop on the owner's base with the 2 s timeout of DP-11, plus the P4 session identity step |
| Kafka | 3 events consumed, two on `rwb.document.events.v1` and one on `rwb.decision-record.v1`; none published |
| Temporal | Observed only: JOB-12 `DocumentIntakeWorkflow` and JOB-11 outbox relay on queue `rwb-document`; no workflow, activity or schedule added |
| File | No service file interface is called. The masked sample files are harness test data, uploaded through the P5 intake operation; the harness writes no blob and reads no blob |

### 13. Solution plan

**Package.** Folder `integration/recovery-document-extraction` in the ACE repository, package `<ACE base package>.recovery.integration.documentextraction`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every field value in the evidence comes from a P5 operation, never from `rwb_document` |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The threshold and the pass mark the harness asserts are read as parameters, so a change is a parameter load and not a harness release |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The eleven types, their thresholds, field definitions and patterns are seeded reference data, never values in the harness code |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness consumes `DocumentStored`, `DocumentFieldsExtracted` and `DecisionRecorded` with its own consumer group and asserts the events, never the producer's table |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 is observed as the event-started `DocumentIntakeWorkflow` on queue `rwb-document`; the harness waits for its window and adds no Schedule and no workflow |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | Each consumed operation is called once from the harness with a 2 s timeout, so the boundary a screen would cross is the one under test |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base and the reader paths of S4 and S2 are the target ones |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real screens use, on the same bases, so a routing defect fails the harness before an officer sees it |

The platform H dependencies in the table (H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the four I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date, and stops at the first failed assertion with the trace |
| FakeRegistry | Configuration | WireMock mappings for rwb-document, rwb-case and rwb-decision, one set per contract version |
| SamplePack | Data | The 60 masked documents, their labels, and the type table rows of DOCTYPE-2026.12 with the patterns and the pass mark as data |
| FieldAssertion | Service | Compares the type, the value, the confidence and the state of every field of a document with the scenario |
| ReaderAssertion | Service | Compares the checked fields the rwb-litigation and rwb-treatment readers received with what they may see (BR5, BR7) |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the intake request, the document read, the review item, the reader answers and the decision entry |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached to the release record |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, the 60-document masked sample and synthetic case "RW-2026-000601". The seeded values are the legacy Background and the state each scenario names; no other value is added, and no production record is copied. A run starts from the seeded state, so a repeated run is deterministic and produces the same report. The harness environment, the seeding and the evidence format: Not specified in the source documents (GAP-0407; ASM-0582).

**Build steps**

1. Write SamplePack with the 60 masked documents, their labels and the DOCTYPE-2026.12 rows; test that a bad seed stops the run (X9).
2. Write FakeRegistry for the three services and the classifier and extractor stand-ins behind the P5 contract, and prove the harness runs green on the fakes alone from Day 1.
3. Write JourneyRunner for AC1 and AC2: intake, the JOB-12 window, the document read and the field assertion on value, confidence and state.
4. Add AC5 and AC6 with the Buddhist Era normalisation and the pattern check, both asserted from the field rows the P5 read returns.
5. Add AC3 and AC7: the review item and MSG-P5-003 on the low-confidence field, and the unchanged file hash, storage_ref and write_once on the write-once document.
6. Add AC4 and AC8: the confirm and correct path through the review and field operations, then the reader answers at rwb-litigation and rwb-treatment, and the out-of-scope 404.
7. Write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record, and rerun the eight scenarios on the release build; replace each fake with the real service as its I story lands.

**Feature switch.** `rwb.dochub.extraction-stage23` is on in the harness profile, as the legacy story sets it; off, the new types are not offered to classification and the reader returns nothing for them, and the harness records that state rather than failing. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all eight owned scenarios, the field accuracy of the court notices is at or above 0.90 on the sample, and each fake has been replaced by the real service where its I story has landed in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in REVIEW | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Caller lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Document outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document store is unavailable | {system} is not available. Your request is queued and will be retried. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-30 Case documents | List | The new types with their fields and confidence; MSG-P5-003 on documents with fields in review; the write-once document without an edit affordance |
| SCR-31 Document review queue | List; reviewed | The review item of the marked field, and the state the field moves to after a confirm or a correction |

No screen is built by this story. The harness drives the operations behind those screens and asserts the states above through the contracts; the screens themselves belong to RWB-P5-E2025-APP and to the review story of the document hub.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12-ITG | Access, BR7 | Component | RW-REFADM user (Documents -) calls GET /api/recovery/document/v1/documents/DOC-0605; refused with MSG-P4-002 |
| TC-E2-025-01-ITG | AC1, BR1 | Integration | 10 masked court notices from the sample |
| TC-E2-025-02-ITG | AC2, BR7, BR8 | Integration | Synthetic signed contract with two parties |
| TC-E2-025-03-ITG | AC3, BR2 | Integration | Judgment with amount at confidence 0.71 |
| TC-E2-025-04-ITG | Legacy AC4, BR3 (stays with RWB-P5-E2025-APP) | Integration | 10 sample judgments, 8 amounts correct |
| TC-E2-025-05-ITG | Legacy AC5 (stays with RWB-P5-E2025-APP) | Integration | 50 sample documents of the new types |
| TC-E2-025-06-ITG | Legacy AC6, BR1 (stays with RWB-P5-E2025-APP) | Integration | Judgment received the day before the valid-from date |
| TC-E2-025-07-ITG | AC5, BR8 | Integration | Judgment dated 5 March 2570 |
| TC-E2-025-08-ITG | AC6, BR4 | Integration | Red case numbers with and without the pattern |
| TC-E2-025-09-ITG | AC4, BR5 | Integration | Judgment with one OK and one REVIEW field |
| TC-E2-025-10-ITG | AC7, BR6 | Integration | Write-once judgment |
| TC-E2-025-11-ITG | AC8 | Integration | Document of team LIT-NE |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the four contracts and the fakes. The app stories keep the unit and component copies of the same cases. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the types, the fields, the patterns, the threshold of 0.80 and the pass mark of 0.90 are data and parameters; no class per document type and no pattern in the harness source.
- No personal data in logs, events, evidence or prompts: party names, amounts and case documents never enter a log or an event, the sample is masked, and the report holds identifiers, confidences and states only.
- No read of another service's tables, and no schema of the harness's own: every read and write goes through the operations of 12.2 (DP-01). The harness writes nothing to legal_action, hearing or treatment.
- The Epic 1 results are unchanged: the RWB-E1-053 regression set runs beside the harness and the six Epic 1 types keep their results.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and an exception is never added to a scenario; a value that must change changes in the sample pack or the type table through a reviewed change.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, R-LIT-16 | TC-E2-025-01-ITG, TC-E2-025-02-ITG, TC-E2-025-04-ITG to TC-E2-025-12-ITG |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38 | TC-E2-025-03-ITG, TC-E2-025-05-ITG, TC-E2-025-06-ITG, TC-E2-025-09-ITG |

### 19. Out of scope

- Writing extracted values into legal_action, hearing or treatment (S4 in Epic 5, S2 in Epic 3). The harness proves what the readers receive, not what they store.
- Litigation pack assembly and the defect list check (FEAT-LIT-04, FEAT-LIT-05, Epic 5).
- Generation of contract, credit approval and mortgage documents (RWB-E2-026).
- Electronic discovery and court evidence attributes (REQ-DCM-017, REQ-DCM-018); they enter only as journey inputs, not as extracted fields.
- The production code of any service: the classifier version, the extractor, the review queue, the reader implementations and every screen stay with their app stories.

The harness, the fakes and the evidence pack cover the items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
