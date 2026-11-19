<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 050 Document classification v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 050 Document classification v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-050 Document classification

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-050 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-08 Classify a document into one of the six types |
| Requirement IDs | REQ-DCM-005 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-049, RWB-E1-025 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **each scanned document classified into one of the six agreed types with a confidence score, and any document below the threshold sent to the review queue with its top two candidate types**, so that **each document is filed under the right type and checklist item without a person typing it**.

## 2. Business rationale

A scan arrives with no type; today a person reads it and files it by hand. Classification reads the OCR text and names the type with a confidence, so the document can be attached, extracted and counted against the case checklist (FSD P5 A2.8). A document the model is unsure of goes to a person, so no document is filed under the wrong type. It meets REQ-DCM-005 and serves the measure fields extracted without review (FSD P5 A2.8.1).

## 3. Preconditions

- RWB-E1-049 is done: intake items carry OCR text and ocr_status.
- RWB-E1-025 is done: document type table DOCTYPE-2026.11 is in force.
- Parameter CLASSIFY_THRESHOLD = 0.80 loaded in document_hub_parameter (assumed until the RWB-E1-060 report; DL11). RWB-E1-054 routes to review on the same value.
- Parameters loaded: CLASSIFY_MAX_PAGES = 3, CLASSIFY_TIMEOUT_SECONDS = 60 (R-UNI-32), assumed.
- The classifier model endpoint is set under DL33 and reachable through the P10 model gateway in SIT; its model version is known.
- The labeled sample of 180 synthetic documents, 30 per type, holds the true type of each document.
- Feature flag rwb.dochub.classify is on.

## 4. Flow

1. JOB-12 Document intake: runs classifyStep after ocrStep.
2. ClassifyStep: selects intake items with ocr_status DONE, no predicted_type and no document type given (uploads carry their type and are skipped), locking each row.
3. ClassifyStep: takes the text of the first CLASSIFY_MAX_PAGES pages and replaces national ID numbers, account numbers and phone numbers with tokens through the ACE PII masking service.
4. ClassifierClient: sends the masked text and the six type codes with their labels from the type table in force; receives a score per type and the model version.
5. ClassifyStep: ranks the scores; writes predicted_type, classification_confidence, the top two candidates in type_candidates and classifier_version.
6. ClassifyStep: if the top score is at or above CLASSIFY_THRESHOLD and the type is in the table in force, marks the item classified with no review_reason; attach (RWB-E1-032) stores it with review_status NOT_NEEDED.
7. ClassifyStep: below the threshold, sets review_reason LOW_CONFIDENCE; attach (RWB-E1-032) stores the document with review_status PENDING and write_once false, so it shows on SCR-31 with MSG-P5-003 and its two candidates (RWB-E1-054). A type outside the table sets review_reason UNKNOWN_TYPE with no predicted type, and attach holds the item for a person.
8. ClassificationEvaluationRunner: on demand, runs the labeled sample, writes the accuracy and the 6 by 6 confusion matrix to evaluation/classification/{runDate}.json in the standard container and to the job record.

## 5. Exception paths

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

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs OCR output (RWB-E1-049) and the type table (RWB-E1-025); attach (RWB-E1-032) reads its result |
| Negotiable | Thresholds and pages read are data; the model behind ClassifierClient can change under DL33 |
| Valuable | Removes hand filing for every document the model is sure of |
| Estimable | One job step, one adapter, one evaluation runner |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Document classification

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given parameter CLASSIFY_THRESHOLD is 0.80
    Given CLASSIFY_MAX_PAGES is 3 and CLASSIFY_TIMEOUT_SECONDS is 60

  Scenario: AC1 Accuracy
    Given the labeled sample of 180 synthetic documents, 30 of each type, with ocr_status "DONE"
    When ClassificationEvaluationRunner runs on the sample
    Then at least 162 of the 180 documents get the labeled type as predicted_type
    Then the report "evaluation/classification/2026-11-20.json" holds the accuracy, the 6 by 6 confusion matrix and the model version

  Scenario: AC2 Low confidence routed
    Given a scanned intake item whose scores are COURT_NOTICE 0.62, DEMAND_LETTER 0.21 and the rest below 0.10
    When classification runs
    Then the item has predicted_type "COURT_NOTICE", classification_confidence 0.6200 and review_reason "LOW_CONFIDENCE"
    Then type_candidates holds COURT_NOTICE 0.62 and DEMAND_LETTER 0.21
    Then the system passes the item to attach marked for type review, with write_once to be set false on the stored document

  Scenario: AC3 Score at the threshold
    Given a scanned intake item whose top score is APPRAISAL_REPORT 0.80
    When classification runs
    Then the system classifies the item as "APPRAISAL_REPORT" with no review_reason

  Scenario: AC4 Classifier does not answer
    Given the classifier stub does not answer within 60 seconds
    When classification runs for one item
    Then the item has review_reason "MODEL_UNAVAILABLE" and no predicted_type
    Then the item records that the fallback was used

  Scenario: AC5 Type not in the table
    Given the classifier returns "LOAN_CONTRACT" 0.91 for an item
    When classification runs
    Then the item has review_reason "UNKNOWN_TYPE"
    Then type_candidates holds the two highest agreed types

  Scenario: AC6 Upload with a type given
    Given an intake item created from an upload of type "TITLE_DEED"
    When classification runs
    Then the classifier receives no call for it and its type stays "TITLE_DEED"

  Scenario: AC7 Item waiting for rescan
    Given an intake item with ocr_status "RESCAN"
    When classification runs
    Then the classifier receives no call for it

  Scenario: AC8 Repeat run
    Given 20 items already classified
    When JOB-12 runs again
    Then the classifier receives no call for those 20 items and their results are unchanged

  Scenario: AC9 Threshold changed as data
    Given parameter CLASSIFY_THRESHOLD is changed to 0.90 in document_hub_parameter
    Given a scanned item whose top score is COURT_NOTICE 0.85
    When classification runs
    Then the item has review_reason "LOW_CONFIDENCE"
    Then no code or deployment changed between the two values

  Scenario: AC10 Personal identifiers masked before the model call
    Given a scanned page holding the synthetic national ID number "0000000000000" and account number "TEST-ACC-0001"
    When classification runs
    Then the text received by the classifier stub holds tokens in place of both values
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is classified into one of the agreed types with a confidence score | REQ-DCM-005; FEAT-DCM-08 |
| BR2 | Below the threshold the document goes to the review queue; the threshold is inclusive | REQ-DCM-005; parameter CLASSIFY_THRESHOLD in document_hub_parameter (New); DL11 |
| BR3 | The types come from the type table in force and the threshold from document_hub_parameter | DL19; principle 1 |
| BR4 | A model that does not answer within the timeout falls back to review and the fallback is recorded | R-UNI-32 |
| BR5 | Accuracy on the labeled sample is at least 90 percent before the step runs in production | Story acceptance; FEAT-AGT-04 |
| BR6 | Personal identifiers are masked before text leaves the document hub | CTL-11; DL26; DL33 |
| BR7 | An item classified once is not classified again | R-UNI-40 |

## 9. State transitions

None. This story does not change a case status. It changes the intake item: OCR DONE to CLASSIFIED when the top score meets the threshold; OCR DONE to review with review_reason LOW_CONFIDENCE, MODEL_UNAVAILABLE or UNKNOWN_TYPE otherwise.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs classification and writes the result (Documents CRU) |
| SY-AGENT, agent platform | Serves the model call through the gateway |
| RW-CASEOWN and roles with Documents R | Read the type and confidence of documents in their scope |
| RW-COE, center of excellence analyst | Runs the evaluation and reads the report |
| RW-RISK, risk and model risk officer | Reviews the evaluation report before production use |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-063 | document_intake | ocr_status | Read |
| DF-DOC-070 | document_intake | predicted_type | Write |
| DF-DOC-071 | document_intake | classification_confidence | Write |
| DF-DOC-072 | document_intake | type_candidates | Write |
| DF-DOC-073 | document_intake | classifier_version | Write |
| DF-DOC-080 | document_intake | review_reason | Write |
| DF-DOC-074 | document_intake | classify_fallback | Write |
| DF-DOC-061 | document_intake | document_id | Read |
| DF-DOC-089 | document_text | text_content | Read |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |
| DF-DOC-004 | document | document_type | Read, for uploads |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake, step classifyStep after ocrStep |
| Job name | JOB-12 Document intake |
| Schedule | Every 15 minutes in business hours |
| Input | Intake items with ocr_status DONE, no predicted_type and no given type |
| Output | Classification fields on each item; review_reason where needed; counts on the job record |
| Events published | None |
| Idempotency key | Intake item ID; an item with predicted_type or review_reason set is not classified again |
| Restart behavior | Unfinished items stay unclassified and are taken by the next run |

**Adapter**

```java
public interface ClassifierClient {
    ClassificationResult classify(String maskedText, List<TypeLabel> types, Duration timeout); // scores per type, modelVersion; throws ClassifierTimeoutException
}
```

**Published interface (P5, used by RWB-E1-032 and RWB-E1-054)**

```java
public interface ClassificationReader {
    Optional<Classification> forIntake(UUID intakeId);   // predictedType, confidence, candidates, classifierVersion, reviewReason
}
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/classify`, Java package `recovery.dochub.classify`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| ClassifyStep | Job | Step of JOB-12: select, mask, call, rank, apply the threshold, write |
| ClassifierClient, ModelGatewayClassifier | Service | Calls the classifier through the P10 model gateway with the timeout |
| TextMasker | Service | Calls the ACE PII masking service for national ID, account and phone numbers |
| ClassificationReader | Published interface | Section 12 |
| ClassificationEvaluationRunner | Service | Runs the labeled sample and writes accuracy and the confusion matrix |
| DocumentIntakeRepository | Repository | From RWB-E1-049; adds the classification columns |

**Database.**
- Flyway migration `V1_5_050__intake_classification.sql` adds to document_intake: predicted_type varchar(30), classification_confidence numeric(5,4), type_candidates jsonb, classifier_version varchar(40), classify_fallback boolean default false; adds to document: document_type varchar(30), type_candidates jsonb, which RWB-E1-032 writes on attach and RWB-E1-054 reads.
- Index ix_intake_classify on document_intake (ocr_status) where predicted_type is null and review_reason is null.

**Configuration and reference data.**
- CLASSIFY_THRESHOLD in document_hub_parameter, loaded by the reference data administrator.
- CLASSIFY_MAX_PAGES and CLASSIFY_TIMEOUT_SECONDS in document_hub_parameter, loaded by the reference data administrator.
- Property rwb.dochub.classify.model-route naming the gateway route set under DL33.

**Build steps.**
1. Write the migration; test the new columns and index.
2. Build TextMasker; test AC10.
3. Build ClassifierClient against a stub with fixed scores; contract test of the response mapping and the timeout.
4. Build ClassifyStep selection and skip rules; test AC6, AC7 and AC8.
5. Add ranking, threshold and review rules; test AC2, AC3, AC5 and AC9.
6. Add the fallback on timeout; test AC4.
7. Build ClassificationEvaluationRunner; run the labeled sample in SIT for AC1 and give the report to the risk and model risk officer.

**Feature flag.** `rwb.dochub.classify`. Off: classifyStep is skipped and every scanned item goes to review with reason LOW_CONFIDENCE.

**Done when.** The tests in section 16 pass and the SIT evaluation report shows at least 162 of 180 correct.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Item sent to the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. Items sent to review are listed on SCR-31 Document review queue (states Loading; list; reviewed), built in RWB-E1-054, with the two candidate types and MSG-P5-003. The evaluation report is read from the standard container by the center of excellence analyst.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-01 | AC1, BR1, BR5 | System | Labeled sample of 180 synthetic documents |
| TC-E1-050-02 | AC2, BR2 | System | Stub scores COURT_NOTICE 0.62, DEMAND_LETTER 0.21 |
| TC-E1-050-03 | AC3, BR2 | System | Stub score APPRAISAL_REPORT 0.80 |
| TC-E1-050-04 | AC4, BR4 | System | Stub with no answer for 60 seconds |
| TC-E1-050-05 | AC5, BR3 | System | Stub returns LOAN_CONTRACT 0.91 |
| TC-E1-050-06 | AC6 | System | Upload of type TITLE_DEED |
| TC-E1-050-07 | AC7 | System | Item in RESCAN |
| TC-E1-050-08 | AC8, BR7 | System | 20 classified items |
| TC-E1-050-09 | AC9, BR3 | System | Parameter CLASSIFY_THRESHOLD changed to 0.90 |
| TC-E1-050-10 | AC10, BR6 | System | Synthetic page with a national ID number and an account number |
| TC-E1-050-11 | Access | Access | Capacity and workforce planner (RW-CAPACITY, no Documents right) calls GET /documents/{documentId} on a classified document; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: types, thresholds, pages read and the timeout are data.
- No personal data in logs, tests or prompts: text is masked before the model call; prompts and responses are not logged; test documents are synthetic.
- No read of another module's tables.
- The model endpoint is inside the SCB tenant (DL33); no document text leaves the bank.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | Business Requirements Epic 1, section 3.5 | FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-40 | TC-E1-050-01 to TC-E1-050-11 |

## 19. Out of scope

- The review queue screen and the correction fed back to the labeled set (RWB-E1-054).
- Field extraction and its evaluation (RWB-E1-053, RWB-E1-060).
- Attach to the case (RWB-E1-032).
- Stage 2 and 3 document types (RWB-E2-025).
