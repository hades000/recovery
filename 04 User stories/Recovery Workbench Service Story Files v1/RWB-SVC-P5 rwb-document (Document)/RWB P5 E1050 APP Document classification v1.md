# RWB-P5-E1050-APP Document classification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1050-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P5-E1050-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the classification step moved into `rwb-document` as the `classifyStep` activity of the intake workflow over the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1` and the queue `rwb-document`; the legacy thresholds, type codes, review reasons, evaluation sample and messages are kept character for character. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **each scanned document classified into one of the six agreed types with a confidence score, and any document below the threshold sent to the review queue with its top two candidate types**, so that **each document is filed under the right type and checklist item without a person typing it**.

Inside `rwb-document` this is the classification capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- Classification is a service-internal capability fed by the intake workflow: the `classifyStep` activity of `DocumentIntakeWorkflow` selects `document_intake` rows, masks the text, calls the internal `ClassifierClient` through `ModelGatewayClassifier`, ranks the scores and writes the classification columns on the intake row. The model provider, the endpoint route and the model version behind `ClassifierClient` are Not specified in the source documents (GAP-1002; ASM-1789): the legacy story reaches a model through the P10 model gateway set under DL33 and Architecture v5 slide 16 draws the classify run as a child of `rwb-agent`, so the satellite is tracked as external work and the plan's C list is not extended with an invented dependency id.
- The type codes and their labels come from `document_type` in the version in force (`valid_from` and `valid_to`, table version DOCTYPE-2026.11), a P5 table read locally with no contract hop (DP-01). The review reasons come from LOV-INTAKE-REVIEW through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); the type list LOV-DOC-TYPE is faked with the same six codes so the two agree at build time and no list value is typed in code.
- `CLASSIFY_THRESHOLD` (0.80), `CLASSIFY_MAX_PAGES` (3) and `CLASSIFY_TIMEOUT_SECONDS` (60, R-UNI-32) are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON). The rows they resolve to live in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5; the legacy table name `document_hub_parameter` is kept.
- The OCR text is masked before the model call by the ACE PII masking service of the ACE common module (CTL-11, DL26, DL33); national ID numbers, account numbers and phone numbers are replaced by tokens, and neither the prompt nor the response is logged.
- The classify step is one step of the 15-minute document-intake Schedule (legacy JOB-12) that RWB-P5-E1049-APP owns; this story contributes the step, the service-internal classifier and the on-demand evaluation runner (DP-10, H RWB-PLT-E1071-CON).
- The classification state is read by attach (RWB-P5-E1032-APP) and by the review queue (RWB-P5-E1054-APP) through the operations of 12.1; the stored document carries `classification_confidence` and `type_candidates` on the `document` row that the store RWB-P5-E1024-APP writes on attach.
- The migration is one step of the per-service Flyway sequence in `rwb_document` (DP-15, H RWB-PLT-E1044-CON): the legacy `V1_5_050__intake_classification.sql` becomes `V1050_1__intake_classification.sql`. The review queue reads reach SCR-31 through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).
- The deployment of the capability, the model artefact pinning and promotion, the configuration reads, the feature flag, the dashboards and the alerts are RWB-P5-E1050-OPS, the X dependency of this story.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, eight exception paths, seven business rules, two messages, authority, twelve data fields, ten acceptance criteria and eleven test cases, adapted to the target service's schema, topic, API base, workflow template and internal classifier.

### 2. Business rationale

A scan arrives with no type; today a person reads it and files it by hand. Classification reads the OCR text and names the type with a confidence, so the document can be attached, extracted and counted against the case checklist (FSD P5 A2.8). A document the model is unsure of goes to a person, so no document is filed under the wrong type. It meets REQ-DCM-005 and serves the measure fields extracted without review (FSD P5 A2.8.1).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` by the service naming rule of §R4 and DP-01. No table of another service is read and no monolith table name survives except the module's own `document_intake`, `document_text`, `document_type` and `document_hub_parameter`.
2. The three thresholds and page bound leave the legacy `document_hub_parameter` read inside the module and arrive through the parameters contract and client library of `rwb-case` (DP-06), while the parameter rows themselves stay in `rwb_document`, which is P5's own store for them.
3. The review reason value set arrives through the reference-data contract (DP-07); the type codes stay in the P5 type table, so a type the business adds is a new table version and never a code change.
4. The Quartz job step becomes the `classifyStep` activity of the `DocumentIntakeWorkflow` template of the workflow kit (DP-10), registered on queue `rwb-document`, so the 15-minute Schedule that starts it belongs to RWB-P5-E1049-APP and this story only contributes one step.
5. The classifier itself is inside the service behind `ClassifierClient`, so the model can change without a contract change, and the evaluation runner is a second activity on the same queue; the legacy P10 model-gateway call is tracked as external work rather than declared as a C dependency the plan does not carry (GAP-1002; ASM-1789).
6. The migration is one step of the per-service Flyway sequence in `rwb_document` (DP-15), and the review queue reads reach SCR-31 through the gateway-bff composite route (DP-19).
7. The stored document's type and confidence are written on attach by RWB-P5-E1024-APP, so the classification result has one owner and one write path; this story never writes the `document` row.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1042-CON | The parameters client library, so `CLASSIFY_THRESHOLD`, `CLASSIFY_MAX_PAGES` and `CLASSIFY_TIMEOUT_SECONDS` are read through a published shape (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-INTAKE-REVIEW and LOV-DOC-TYPE (DP-07) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 `DocumentIntakeWorkflow` template, activity registration and retry policy (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the classification migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the review queue reads to SCR-31 (DP-19) |
| RWB-P5-E1049-APP | The intake pipeline: `document_intake` rows with `ocr_status`, `document_text` pages, the 15-minute Schedule and the workflow that this story adds `classifyStep` to |
| RWB-P5-E1025-APP | The document type table `document_type` with version DOCTYPE-2026.11 in force and the labels of the six types |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the three classification parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves LOV-INTAKE-REVIEW and LOV-DOC-TYPE (DP-07) |
| RWB-P5-E1050-OPS | The deployment of the capability, the classifier and model artefact pinning, the configuration reads, the feature flag, the dashboards, the alerts and the runbook (the X dependency) |

Business preconditions carried from RWB-E1-050:

- RWB-P5-E1049-APP is done: intake items carry OCR text and `ocr_status`.
- RWB-P5-E1025-APP is done: the document type table DOCTYPE-2026.11 is in force.
- Parameter `CLASSIFY_THRESHOLD` = 0.80 loaded in `document_hub_parameter` (assumed until the RWB-P5-E1060-APP report; DL11). RWB-P5-E1054-APP routes to review on the same value.
- Parameters loaded: `CLASSIFY_MAX_PAGES` = 3, `CLASSIFY_TIMEOUT_SECONDS` = 60 (R-UNI-32), assumed.
- The classifier model endpoint is set under DL33 and reachable in SIT through the service-internal client; its provider and model version are Not specified in the source documents (GAP-1002; ASM-1789).
- The labeled sample of 180 synthetic documents, 30 per type, holds the true type of each document.
- Feature flag `rwb.document.classify` is on; the legacy flag name `rwb.dochub.classify` is retired with the monolith (ASM-1790).

The classification capability is deployed by RWB-P5-E1050-OPS, which also owns the model artefact pinning and promotion and the rollback to the previous model version (the X dependency). The report container and account of the evaluation output are Not specified in the source documents (GAP-1002; ASM-1791). No approval of this story was available in this run, so it is carried as Status Draft (realignment v1) with the release 30 November 2026 unchanged and marked tentative (ASM-1788).

### 4. Flow

1. The 15-minute Schedule of RWB-P5-E1049-APP starts `DocumentIntakeWorkflow`; the `ocrStep` activity of the same workflow leaves items with `ocr_status` DONE, and the workflow then calls `classifyStep`.
2. `ClassifyStep`: selects `document_intake` rows with `ocr_status` DONE, no `predicted_type` and no document type given (uploads carry their type and are skipped), locking each row with `version` as the optimistic lock.
3. `TextMasker`: takes the text of the first `CLASSIFY_MAX_PAGES` pages from `document_text` and replaces national ID numbers, account numbers and phone numbers with tokens through the ACE PII masking service.
4. `ClassifierClient`: sends the masked text and the six type codes with their labels from `document_type` in the version in force; receives a score per type and the model version, within `CLASSIFY_TIMEOUT_SECONDS`.
5. `ClassifyStep`: ranks the scores; writes `predicted_type`, `classification_confidence`, the top two candidates in `type_candidates` and `classifier_version` on the intake row.
6. `ClassifyStep`: if the top score is at or above `CLASSIFY_THRESHOLD` and the type is in the table in force, marks the item classified with no `review_reason`; attach (RWB-P5-E1032-APP) stores it with `review_status` NOT_NEEDED.
7. `ClassifyStep`: below the threshold, sets `review_reason` LOW_CONFIDENCE; attach stores the document with `review_status` PENDING and `write_once` false, so it shows on SCR-31 with MSG-P5-003 and its two candidates (RWB-P5-E1054-APP). A type outside the table sets `review_reason` UNKNOWN_TYPE with no predicted type, and attach holds the item for a person.
8. `ClassifyStep`: a model that does not answer inside `CLASSIFY_TIMEOUT_SECONDS` sets `review_reason` MODEL_UNAVAILABLE with no `predicted_type` and `classify_fallback` true, and the fallback is recorded on the item.
9. `ClassifyStep`, one transaction in `rwb_document`: writes the classification columns on the `document_intake` row and, through the event library, the `rwb.document.DocumentClassified` row to the outbox; the event carries the intake ID, the case ID, the predicted type, the confidence band and the review reason, and no text, no candidate list and no personal data.
10. `ClassificationEvaluationRunner`: on demand, runs the labeled sample through the same masked path, writes the accuracy and the 6 by 6 confusion matrix to `evaluation/classification/{runDate}.json` and to the job record, and reports the model version it used. The on-demand trigger is an operator-started workflow on queue `rwb-document`; a named admin operation is Not specified in the source documents (GAP-1002; ASM-1790).

The classification result is written once per item: the selection of step 2 excludes every row that already carries `predicted_type` or `review_reason`, so a repeat run of the workflow makes no second model call (R-UNI-40, BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Top score below the threshold | Item marked LOW_CONFIDENCE with the two candidates; stored for review at attach | MSG-P5-003 | AC2 |
| X2 | Top score exactly at the threshold | Item classified | None | AC3 |
| X3 | Classifier does not answer within CLASSIFY_TIMEOUT_SECONDS | Fallback: item to review with reason MODEL_UNAVAILABLE; the fallback is recorded on the item | MSG-P5-003 | AC4 |
| X4 | The model returns a type code not in the table in force | Item to review with reason UNKNOWN_TYPE | MSG-P5-003 | AC5 |
| X5 | The item already carries a type (upload) | Not classified | None | AC6 |
| X6 | The item is in RESCAN or FAILED | Not classified | None | AC7 |
| X7 | The job runs again over classified items | Not classified again; no second model call | None | AC8 |
| X8 | A user without Documents R reads the classification of a document | Refused with 403 | MSG-P4-002 | TC-E1-050-11 (Access) |

Two target-service notes:

- The threshold is read once per run from the parameters contract and cached for five minutes; a value changed in `document_hub_parameter` is therefore in force on the next run without a deployment (AC9). A parameters read that fails leaves the step unstarted and the items unclassified rather than classified on a guessed threshold, and the run is recorded FAILED for the job monitor of RWB-P5-E1050-OPS.
- The masking call is inside the step and not a separate hop: a masking failure stops the item before the model call and the item keeps `ocr_status` DONE with no `predicted_type`, so the next run retries it and no unmasked text is ever sent (X3 is not used for a masking failure, because no model call was made).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs OCR output (RWB-P5-E1049-APP) and the type table (RWB-P5-E1025-APP); attach (RWB-P5-E1032-APP) reads its result; the classifier is inside the service |
| Negotiable | Thresholds and pages read are data; the model behind `ClassifierClient` can change under DL33 without a contract change |
| Valuable | Removes hand filing for every document the model is sure of |
| Estimable | One workflow step, one internal classifier, one masking client, one evaluation runner, one migration step |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Document classification

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given parameter CLASSIFY_THRESHOLD is 0.80
    Given CLASSIFY_MAX_PAGES is 3 and CLASSIFY_TIMEOUT_SECONDS is 60
    Given the rwb-case contract mock returns the reference-data list "LOV-DOC-TYPE" with the six agreed types of version "DOCTYPE-2026.11"
    Given the rwb-case parameters contract mock returns CLASSIFY_THRESHOLD 0.80, CLASSIFY_MAX_PAGES 3 and CLASSIFY_TIMEOUT_SECONDS 60

  Scenario: AC1 Accuracy (legacy RWB-E1-050 AC1)
    Given the labeled sample of 180 synthetic documents, 30 of each type, with ocr_status "DONE"
    When ClassificationEvaluationRunner runs on the sample
    Then at least 162 of the 180 documents get the labeled type as predicted_type
    Then the report "evaluation/classification/2026-11-20.json" holds the accuracy, the 6 by 6 confusion matrix and the model version

  Scenario: AC2 Low confidence routed (legacy RWB-E1-050 AC2)
    Given a scanned intake item whose scores are COURT_NOTICE 0.62, DEMAND_LETTER 0.21 and the rest below 0.10
    When classification runs
    Then the item has predicted_type "COURT_NOTICE", classification_confidence 0.6200 and review_reason "LOW_CONFIDENCE"
    Then type_candidates holds COURT_NOTICE 0.62 and DEMAND_LETTER 0.21
    Then the system passes the item to attach marked for type review, with write_once to be set false on the stored document

  Scenario: AC3 Score at the threshold (legacy RWB-E1-050 AC3)
    Given a scanned intake item whose top score is APPRAISAL_REPORT 0.80
    When classification runs
    Then the system classifies the item as "APPRAISAL_REPORT" with no review_reason

  Scenario: AC4 Classifier does not answer (legacy RWB-E1-050 AC4)
    Given the classifier stub does not answer within 60 seconds
    When classification runs for one item
    Then the item has review_reason "MODEL_UNAVAILABLE" and no predicted_type
    Then the item records that the fallback was used

  Scenario: AC5 Type not in the table (legacy RWB-E1-050 AC5)
    Given the classifier returns "LOAN_CONTRACT" 0.91 for an item
    When classification runs
    Then the item has review_reason "UNKNOWN_TYPE"
    Then type_candidates holds the two highest agreed types

  Scenario: AC6 Upload with a type given (legacy RWB-E1-050 AC6)
    Given an intake item created from an upload of type "TITLE_DEED"
    When classification runs
    Then the classifier receives no call for it and its type stays "TITLE_DEED"

  Scenario: AC7 Item waiting for rescan (legacy RWB-E1-050 AC7)
    Given an intake item with ocr_status "RESCAN"
    When classification runs
    Then the classifier receives no call for it

  Scenario: AC8 Repeat run (legacy RWB-E1-050 AC8)
    Given 20 items already classified
    When JOB-12 runs again
    Then the classifier receives no call for those 20 items and their results are unchanged

  Scenario: AC9 Threshold changed as data (legacy RWB-E1-050 AC9)
    Given parameter CLASSIFY_THRESHOLD is changed to 0.90 in document_hub_parameter
    Given a scanned item whose top score is COURT_NOTICE 0.85
    When classification runs
    Then the item has review_reason "LOW_CONFIDENCE"
    Then no code or deployment changed between the two values

  Scenario: AC10 Personal identifiers masked before the model call (legacy RWB-E1-050 AC10)
    Given a scanned page holding the synthetic national ID number "0000000000000" and account number "TEST-ACC-0001"
    When classification runs
    Then the text received by the classifier stub holds tokens in place of both values
```

Every Given, When and Then line above is the legacy line unchanged, with every legacy value kept character for character; the only added lines are the two Background Givens that mock the `rwb-case` reference-data and parameters contracts (DP-07, DP-06), and the legacy endpoints of the shell map to the target operations of 12.1: the classification state read is `GET /api/recovery/document/v1/intake-items/{intakeItemId}/classification` (API-P5-011 read of the same item), `GET /api/recovery/document/v1/review-items` (API-P5-010) lists the held candidates, and the access case TC-E1-050-11 is `GET /api/recovery/document/v1/documents/{documentId}` (API-P5-003).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is classified into one of the agreed types with a confidence score | REQ-DCM-005; FEAT-DCM-08 |
| BR2 | Below the threshold the document goes to the review queue; the threshold is inclusive | REQ-DCM-005; parameter CLASSIFY_THRESHOLD in document_hub_parameter (New); DL11 |
| BR3 | The types come from the type table in force and the threshold from document_hub_parameter | DL19; principle 1 |
| BR4 | A model that does not answer within the timeout falls back to review and the fallback is recorded | R-UNI-32 |
| BR5 | Accuracy on the labeled sample is at least 90 percent before the step runs in production | Story acceptance; FEAT-AGT-04 |
| BR6 | Personal identifiers are masked before text leaves the document hub | CTL-11; DL26; DL33 |
| BR7 | An item classified once is not classified again | R-UNI-40 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1, BR2 and BR3 are executed on `document_intake` only: the selected row is locked, the scores are ranked in the step, and the four result columns (`predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version`) plus `review_reason` are written in one transaction. No foreign schema is read (DP-01).
- BR2 keeps the threshold inclusive: the comparison is "top score at or above `CLASSIFY_THRESHOLD`", so AC3 at exactly 0.80 classifies and AC9 at 0.85 under 0.90 routes to review. The value comes from the parameters contract (DP-06) and is never written in code, so the two settings of AC9 differ by one data row.
- BR3 reads `document_type` in the version in force by `valid_from` and `valid_to`, with `table_version` DOCTYPE-2026.11; a type code that is absent from that version is UNKNOWN_TYPE and never a new code (AC5). The review reasons come from LOV-INTAKE-REVIEW through the reference-data contract (DP-07).
- BR4 is executed by the activity timeout and by `classify_fallback`; a timeout is recorded on the item and is not retried for a second model call inside the same run, so AC4 sees one fallback and no predicted type.
- BR5 is executed by the evaluation runner and its 6 by 6 confusion matrix; the report is the evidence the risk and model risk officer reads before production use, and the threshold of 162 of 180 is the story acceptance value.
- BR6 is executed before the call: the masked text is the only text that leaves the step, and the prompt, the response and the candidate list are never logged. The masking service is the ACE common module's, called and never reimplemented.
- BR7 is executed by the selection predicate and by the `ix_intake_classify` partial index on `document_intake (ocr_status) where predicted_type is null and review_reason is null`, so a repeat run finds nothing to do (AC8).
- DP-10 puts the step inside the workflow kit template, DP-15 puts the migration in the per-service sequence, DP-19 puts the review queue reads behind gateway-bff, and DP-11 fixes the 2 s timeout of the reference-data and parameters reads.

### 9. State transitions

No case state machine in this story: classification changes no case status. It moves the intake item:

| From | Event | To |
|---|---|---|
| `ocr_status` DONE, no type given | top score at or above `CLASSIFY_THRESHOLD` and the type is in the table in force | classified, no `review_reason` |
| `ocr_status` DONE, no type given | top score below `CLASSIFY_THRESHOLD` | review with `review_reason` LOW_CONFIDENCE and two candidates |
| `ocr_status` DONE, no type given | the model names a type outside the table in force | review with `review_reason` UNKNOWN_TYPE, no predicted type |
| `ocr_status` DONE, no type given | no answer inside `CLASSIFY_TIMEOUT_SECONDS` | review with `review_reason` MODEL_UNAVAILABLE, no predicted type, `classify_fallback` true |
| `ocr_status` RESCAN, FAILED or PENDING | the classify step selects | unchanged, not classified |
| any item with `predicted_type` or `review_reason` set | a repeat run selects | unchanged, no second model call |

The stored `document` row follows the store's own state machine (RWB-P5-E1024-APP): COPY_PENDING then STORED, with `review_status` NOT_NEEDED for a confident classification and PENDING for a routed one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs classification and writes the result (Documents CRU) |
| SY-AGENT, agent platform | Serves the model call where the deployed model is reached through the agent platform; the call is external work tracked by ASM-1789 |
| RW-CASEOWN and roles with Documents R | Read the type and confidence of documents in their scope |
| RW-COE, center of excellence analyst | Runs the evaluation and reads the report |
| RW-RISK, risk and model risk officer | Reviews the evaluation report before production use |
| SY-DOCUMENT, the rwb-document service identity | Runs the classify and evaluation activities of the queue `rwb-document` |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope and masking in `rwb_access`) and consumed as the cached permission decision the service holds; this story adds no operation and no guard of its own. The refusal shape of X8 is 403 with MSG-P4-002, as in the legacy endpoint, and it is raised by the document read of RWB-P5-E1024-APP. The per-service login is DP-02; this story refers to "the rwb-document login (DP-02)" and never to a shared login.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-063 | `document_intake` | ocr_status | Read |
| DF-DOC-070 | `document_intake` | predicted_type | Write |
| DF-DOC-071 | `document_intake` | classification_confidence | Write |
| DF-DOC-072 | `document_intake` | type_candidates | Write |
| DF-DOC-073 | `document_intake` | classifier_version | Write |
| DF-DOC-080 | `document_intake` | review_reason | Write |
| DF-DOC-074 | `document_intake` | classify_fallback | Write |
| DF-DOC-061 | `document_intake` | document_id | Read |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-DOC-088 | `document_text` | page_no | Read |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-220 | `document_type` | label_en | Read |
| DF-REF-221 | `document_type` | label_th | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-REF-230, DF-REF-231 | `document_type` | valid_from, valid_to | Read |
| DF-REF-245 | `document_hub_parameter` | param_code | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read |
| DF-DOC-004 | `document` | document_type | Read, for uploads |
| DF-DOC-007 | `document` | classification_confidence | Read, for the stored document |
| Standard column | `document_intake` | state, version | Write, read |
| (outbox) | outbox library table in `rwb_document` | the row for DocumentClassified | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and in TSD P5 T3.1. The classification columns keep the legacy physical types: `predicted_type` varchar(30), `classification_confidence` numeric(5,4), `type_candidates` jsonb, `classifier_version` varchar(40), `classify_fallback` boolean default false, and `review_reason` varchar(20) from LOV-INTAKE-REVIEW. No `document` row is written here: the stored document's type, confidence and candidates are written by attach (RWB-P5-E1032-APP) through the store (RWB-P5-E1024-APP). Personal data never enters the event payload, the workflow input or the log; the masked text exists only in the step's memory and the raw text stays in `document_text`.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/classify` | P5 | The classify command: the item, the pages bound, the type codes of the version in force and the timeout; answers the `ClassificationResult`. Service identity only; `Idempotency-Key` required. An item that already carries `predicted_type` or `review_reason` answers the stored result with no second model call. The path is the CON baseline's, because no source names a classification path (GAP-1003; ASM-1792) |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/classification` | P5 | The classification-state read: predicted type, confidence, the top two candidates, `classifier_version`, `review_reason` and `classify_fallback`, masked by role; Documents right R with scope applied |
| GET | `/api/recovery/document/v1/review-items` | P5 | The review queue list (API-P5-010), which shows the two candidates and the reason next to each held item; declared by RWB-P5-E1054-APP and referenced here |

`GET /api/recovery/document/v1/intake-items/{intakeItemId}`, `GET /api/recovery/document/v1/intake-items/{intakeItemId}/content`, `GET /api/recovery/document/v1/documents/{documentId}` and `POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve` are this service's operations built by RWB-P5-E1049-APP, RWB-P5-E1024-APP and RWB-P5-E1054-APP; this story reads their shapes and adds no field to them beyond the classification properties of the `IntakeItem` answer.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 | RWB-P3-E1042-CON | `CLASSIFY_THRESHOLD`, `CLASSIFY_MAX_PAGES` and `CLASSIFY_TIMEOUT_SECONDS`, read through the client library; one hop, 2 s timeout (DP-06, DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 | RWB-P3-E1043-CON | LOV-INTAKE-REVIEW and LOV-DOC-TYPE, read through the client library; one hop, 2 s timeout (DP-07, DP-11) |

The model call is not a REST operation of another service in this story: the classifier is service-internal, and where the deployed model is reached through the `rwb-agent` platform the call is external work tracked by ASM-1789 rather than a declared contract row.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentClassified.v1` | `rwb.document.events.v1` | P5 | caseId | intakeId, caseId, predictedType, confidenceBand, reviewReason, classifiedAt; no text, no candidate list, no personal data |

The event is written to the outbox in the classification transaction, so it exists exactly when the classification columns exist. CloudEvents 1.0 envelope in binary mode; consumers dedupe through their inbox. The schema is declared by RWB-P5-E1050-CON, and the third-event position of `rwb-document` is recorded there (ASM-1794).

#### 12.4 Events consumed

None. The step is called by `DocumentIntakeWorkflow` and reads its data from `rwb_document` and the two `rwb-case` contracts; it subscribes to no topic, and `AgentRunCompleted` is not consumed because the classifier is internal (GAP-1002; ASM-1789).

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | Owned by RWB-P5-E1049-APP; this story contributes one step to it and never changes its Schedule |
| `classifyStep` | Activity | `rwb-document` | Select, mask, call, rank, apply the threshold, write; idempotent per intake item |
| `evaluateClassifier` | Activity | `rwb-document` | The on-demand evaluation: labeled sample, accuracy, 6 by 6 confusion matrix, report and job record |

#### 12.6 Schedules

None in this story. The 15-minute document-intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP and starts the workflow that calls `classifyStep`; this story registers no Schedule and adds no cron entry.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 | Read the selected rows; write the five classification columns and `review_reason` |
| `document_text` | P5 | Read only: the pages of the item, up to `CLASSIFY_MAX_PAGES` |
| `document_type` | P5 | Read only: the type codes and labels in the version in force (RWB-P5-E1025-APP owns the load) |
| `document_hub_parameter` | P5 | Read only: the parameter rows behind the parameters contract |
| `document` | P5 | Read only: the type of an upload; the classification columns of the stored document are written by attach and the store |
| outbox library table | PLT library, created in `rwb_document` | The DocumentClassified row, in the classification transaction |

No foreign-schema table is read (DP-01) and no ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | `CLASSIFY_THRESHOLD` 0.80 and 0.90, `CLASSIFY_MAX_PAGES` 3, `CLASSIFY_TIMEOUT_SECONDS` 60, and a refusing read |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-TYPE with the six agreed types of DOCTYPE-2026.11 and LOV-INTAKE-REVIEW with its five reasons |
| classifier stub | RWB-P5-E1050-CON | Fixed scores per type (COURT_NOTICE 0.62, DEMAND_LETTER 0.21, APPRAISAL_REPORT 0.80, LOAN_CONTRACT 0.91), a model version, and a stub that does not answer inside 60 seconds |
| PII masking stub | ACE common module | The token replacement of AC10 for the synthetic national ID number and account number |
| type-table fixture | RWB-P5-E1025-APP | DOCTYPE-2026.11 in force on a boundary date, and a version where a type code is absent |
| Drools kit | not used | No rule package is evaluated in this story |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 2 | The classify command, the classification-state read and the review list; the parameters and reference-data reads of `rwb-case` |
| Kafka | Published 1, consumed 0 | `rwb.document.DocumentClassified.v1` on `rwb.document.events.v1`, written to the outbox |
| Temporal | 1 workflow step and 1 evaluation activity | `classifyStep` and `evaluateClassifier` on queue `rwb-document`; the workflow and the 15-minute Schedule are RWB-P5-E1049-APP's |
| File | 1 report | The evaluation report at `evaluation/classification/{runDate}.json`, written through the service's configured storage client; container and account Not specified (GAP-1002; ASM-1791) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/classify`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ClassificationController | Controller | The three operations of 12.1; maps exceptions to RFC 9457 problem responses with the message ID; access check and scope |
| ClassifyStep | Temporal activity | Select, mask, call, rank, apply the threshold, write, outbox |
| ClassifierClient, ModelGatewayClassifier | Service | Calls the classifier inside the service boundary with `CLASSIFY_TIMEOUT_SECONDS`; parses the score per type and the model version |
| TextMasker | Service | Calls the ACE PII masking service for national ID, account and phone numbers |
| ClassificationReader | Service | The published read the classification-state operation and attach use; predicted type, confidence, candidates, classifier version, review reason |
| ClassificationEvaluationRunner | Service | The labeled sample, the accuracy, the 6 by 6 confusion matrix, the report and the job record |
| DocumentIntakeRepository | Repository | The intake row, its classification columns and the selection predicate of step 2 |
| DocumentTypeReader | Repository | `document_type` in the version in force by `valid_from` and `valid_to` |
| ClassificationParameters | Library client | The three parameters through the parameters contract of `rwb-case`, cached for 5 minutes |
| ClassifyThresholdPolicy | Service | The inclusive comparison and the three review decisions, as one unit-testable class |

**Database.**

- One migration step in the per-service Flyway sequence (DP-15): `V1050_1__intake_classification.sql` adds to `document_intake` the legacy columns `predicted_type` varchar(30), `classification_confidence` numeric(5,4), `type_candidates` jsonb, `classifier_version` varchar(40), `classify_fallback` boolean default false; the legacy migration `V1_5_050__intake_classification.sql` is not replayed against a foreign schema. `review_reason` varchar(20) is created by the intake migration of RWB-P5-E1049-APP and reused here.
- Index `ix_intake_classify ON document_intake (ocr_status) WHERE predicted_type IS NULL AND review_reason IS NULL`.
- `document.document_type` varchar(30) and `document.type_candidates` jsonb are written by attach (RWB-P5-E1032-APP) through the store and read here; this story adds no column to `document`.

**Configuration and reference data.**

- `CLASSIFY_THRESHOLD` = 0.80, `CLASSIFY_MAX_PAGES` = 3 and `CLASSIFY_TIMEOUT_SECONDS` = 60 in `document_hub_parameter`, loaded by the reference data administrator, read through the parameters contract (DP-06).
- Document type table version DOCTYPE-2026.11 in force, loaded and approved through RWB-P5-E1025-APP.
- LOV-INTAKE-REVIEW and LOV-DOC-TYPE through the reference-data contract (DP-07).
- Property `classify.model-route` naming the internal route; the legacy `rwb.dochub.classify.model-route` key is retired with the monolith (ASM-103).
- Feature flag `rwb.document.classify`. Off: `classifyStep` is skipped, no item is classified, and every scanned item goes to review with reason LOW_CONFIDENCE at attach.

**Build steps**

1. Write the migration step and the index; test the five columns and the partial index on a boundary date.
2. Build `TextMasker` against the masking stub; test AC10 that no national ID number and no account number reaches the client.
3. Build `ClassifierClient` against the stub with fixed scores; contract test the response mapping, the model version and the timeout.
4. Build the selection and skip rules of `ClassifyStep`; test AC6, AC7 and AC8.
5. Add `ClassifyThresholdPolicy` with the inclusive comparison and the three review decisions; test AC2, AC3, AC5 and AC9.
6. Add the timeout fallback and `classify_fallback`; test AC4.
7. Build the outbox write of `DocumentClassified` inside the same transaction; test that a failed write leaves no classification.
8. Build `ClassificationEvaluationRunner` with the 6 by 6 confusion matrix; run the labeled sample in SIT for AC1 and give the report to the risk and model risk officer.
9. Build the three operations with the access check and scope; API test TC-E1-050-11.

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

DP-01 keeps the four document tables in `rwb_document` and removes the module-internal cross-read: the scores are written on `document_intake`, the types are read from the P5 type table, and no other service's table is touched. DP-06 keeps the threshold, the page bound and the timeout out of the code: the client library wraps the `rwb-case` parameters contract while the parameter rows stay in this schema, as the Ownership Map gives them to P5, and the 5-minute cache is what makes AC9 a data change. DP-07 keeps the review-reason set out of the code and fakes LOV-DOC-TYPE with the same six codes as the type table, so a code added to a table version is a data change on both sides. DP-10 replaces the Quartz step with an activity of the workflow kit template, which is what makes the step restartable and observable per run. DP-11 fixes the two consumed reads to one hop with a 2 s timeout and a fake, so the step builds before `rwb-case` is live. DP-15 puts the migration in the service's own sequence and DP-19 puts the review queue reads behind the composite route, so the screen calls the owner once. The model satellite is not a DP row: the legacy `ClassifierClient` behind the P10 gateway is carried as an internal capability with an external satellite, which is the reason the plan's C list stays as it is.

**Done when.** The tests in section 16 pass, the SIT evaluation report shows at least 162 of 180 correct with the model version named, `rwb.document.DocumentClassified.v1` is on the topic once per classified item with no text and no personal data, and the threshold is proven to change by data alone.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Item sent to the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. MSG-P5-003 is not an error of the classify command: it is the text SCR-31 shows for a held item, and the command answers 200 with the `review_reason` and the two candidates that put the item there. A refusal without the Documents right answers 403 with MSG-P4-002, as in the legacy endpoint. The not-found message of the classification-state read and the message of a malformed request are Not specified in the source documents (GAP-1003; ASM-1792).

### 15. Screens and states

No screen in this story. Items sent to review are listed on SCR-31 Document review queue (states Loading; list; reviewed), built in RWB-P5-E1054-APP, with the two candidate types and MSG-P5-003; the reads reach it through the gateway-bff composite route (DP-19). The evaluation report is read from the standard container by the center of excellence analyst.

| State | What the operator or reader sees |
|---|---|
| Classified | The intake item and, after attach, the document carry the type and the confidence of 0 to 1 with four decimals; no review reason |
| Held for type review | The review queue row shows the reason, the predicted type and the two candidates, with MSG-P5-003 |
| Fallback recorded | The item shows MODEL_UNAVAILABLE and the fallback flag, and the reader knows the model did not answer |
| Unknown type | The item shows UNKNOWN_TYPE, no predicted type and the two highest agreed types as candidates |
| Report | The evaluation report of the run date with the accuracy, the 6 by 6 confusion matrix and the model version |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-11 | Access | Component | Capacity and workforce planner (RW-CAPACITY, no Documents right) calls `GET /api/recovery/document/v1/documents/{documentId}` on a classified document; refused with MSG-P4-002 |
| TC-E1-050-01 | AC1, BR1, BR5 | End to end | Labeled sample of 180 synthetic documents |
| TC-E1-050-02 | AC2, BR2 | End to end | Stub scores COURT_NOTICE 0.62, DEMAND_LETTER 0.21 |
| TC-E1-050-03 | AC3, BR2 | End to end | Stub score APPRAISAL_REPORT 0.80 |
| TC-E1-050-04 | AC4, BR4 | End to end | Stub with no answer for 60 seconds |
| TC-E1-050-05 | AC5, BR3 | End to end | Stub returns LOAN_CONTRACT 0.91 |
| TC-E1-050-06 | AC6 | End to end | Upload of type TITLE_DEED |
| TC-E1-050-07 | AC7 | End to end | Item in RESCAN |
| TC-E1-050-08 | AC8, BR7 | End to end | 20 classified items |
| TC-E1-050-09 | AC9, BR3 | End to end | Parameter CLASSIFY_THRESHOLD changed to 0.90 |
| TC-E1-050-10 | AC10, BR6 | End to end | Synthetic page with a national ID number and an account number |

The legacy level System maps to End to end and Access to Component; this story owns no Resilience case. The wave-1 integration harness copies TC-E1-050-01 as `TC-E1-050-01-ITG`, where the real parameters and reference-data services replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: types, thresholds, pages read, the timeout and the review reasons are data rows or parameters.
- No personal data in logs, tests or prompts: text is masked before the model call; prompts and responses are not logged; test documents are synthetic and the national ID number and account number of AC10 are the synthetic values of the legacy story.
- No read of another service's tables (DP-01). The parameters and lists arrive through the `rwb-case` contracts, one hop, 2 s timeout.
- ACE data is reached only through the owner's contract or a `v_ace_*` view; this service reads no view.
- The model stays inside the SCB tenant (DL33): no document text leaves the bank, and the masked text is the only text that reaches the model.
- The classification is written once per item: the selection predicate and the partial index are the guard, not a caller's promise.
- The event carries identifiers, a type code, a confidence band and a reason; no text, no candidate list and no personal value.
- The classifier is inside the service behind one interface, so a model change is a configuration change and not a contract change.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | Business Requirements Epic 1, section 3.5 | FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-40 | TC-E1-050-01 to TC-E1-050-11 |

| Legacy reference | Where it is kept |
|---|---|
| Type table version DOCTYPE-2026.11 and the six types | Background, sections 3, 4, 8, 13, 16 |
| CLASSIFY_THRESHOLD 0.80, CLASSIFY_MAX_PAGES 3, CLASSIFY_TIMEOUT_SECONDS 60 | Background, sections 3, 4, 8, 12.2, 13 |
| The evaluation sample of 180 documents, 30 per type, and the 162 threshold | AC1, BR5, sections 13 and 16 |
| review_reason values LOW_CONFIDENCE, MODEL_UNAVAILABLE, UNKNOWN_TYPE and classify_fallback | AC2, AC4, AC5, sections 4, 8, 9 |
| MSG-P5-003 and MSG-P4-002 | Section 14, exception paths |
| The published read used by attach and review (legacy `ClassificationReader`) | Sections 4, 12.1, 13 |
| Pattern DP-01, DP-06, DP-07, DP-10, DP-11, DP-15, DP-19 | Section 13, section 17 |
| The model satellite and its unnamed provider and version | GAP-1002, ASM-1789 |

### 19. Out of scope

- The review queue screen and the correction fed back to the labeled set (RWB-P5-E1054-APP).
- Field extraction and its evaluation (RWB-P5-E1053-APP, RWB-P5-E1060-APP).
- Attach to the case (RWB-P5-E1032-APP).
- Stage 2 and 3 document types (RWB-P5-E2025-APP).
- The deployment, the model artefact pinning and promotion, the dashboards, the alerts and the runbook (RWB-P5-E1050-OPS).
- The contract baseline, the fakes and the drift test (RWB-P5-E1050-CON).
- The model provider, the endpoint and the model version behind `ClassifierClient`, and the agent-platform satellite where the model is reached through `rwb-agent` (GAP-1002; ASM-1789).
