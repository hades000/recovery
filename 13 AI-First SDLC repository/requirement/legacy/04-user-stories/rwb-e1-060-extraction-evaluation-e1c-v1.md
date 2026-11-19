<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 060 Extraction evaluation E1c v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 060 Extraction evaluation E1c v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-060 Extraction evaluation [E1c]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-060 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-04 Evaluate document extraction quality |
| Requirement IDs | REQ-DCM-005, REQ-DCM-006 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-053, RWB-E1-058 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **field extraction for the six document types scored against the labeled sample for three approaches (OCR template, model, and OCR checked by the model)**, so that **the extraction approach and the confidence threshold for each document type are chosen on measured precision and recall**.

## 2. Business rationale

Fields read wrongly from a court notice or a title deed send a case down the wrong step, and fields sent to review without need take officer time. This story measures the three approaches on the same reviewed documents, field by field, and proposes for each document type the approach and the confidence threshold below which a field goes to the review queue. It serves REQ-DCM-006 (fields extracted for the agreed types) and REQ-DCM-005 (confidence score and review queue below the threshold).

## 3. Preconditions

- RWB-E1-053 is done: the P5 pipeline (SY-OCR) writes document_field rows with a confidence per field for the six types in LOV-DOC-TYPE (assumed six types; DL19).
- RWB-E1-058 is done: the gateway, the evaluation harness and the sample loader exist.
- Approved agent_policy "EXTRACT" version "P1" (mode SHADOW, allowed tools read_document_content, read_document_fields) and prompt "PR1".
- Labeled sample "EXTRACT-S1" version 1 is loaded: fields confirmed or corrected by a person (document_field.confirmed_by set), at least 30 documents per type. Personal field values are held as SHA-256 hashes.
- RW-COE holds Rules and parameters C.

## 4. Flow

1. RW-COE: loads sample "EXTRACT-S1" through POST /admin/agent-samples with one row per document and field.
2. RW-COE: starts the evaluation with approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL through POST /admin/agent-evaluations.
3. System: for OCR_TEMPLATE, reads the stored document_field values through the P5 interface; makes no model call.
4. System: for MODEL, calls agent "EXTRACT" in shadow on the document content and reads the fields from its answer.
5. System: for OCR_AND_MODEL, passes the OCR fields with the content to agent "EXTRACT" and takes its checked values.
6. System: compares each value with the label and stores true positives, false positives, false negatives, precision and recall per field and approach.
7. System: for each document type, picks the approach with the highest F1 and proposes the confidence threshold for the review queue.
8. RW-COE: reads the result through GET /admin/agent-evaluations and exports it; the solution architect records the choice as a proposed architecture decision after ADR-009.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A document type has fewer than 30 labeled documents | The type is scored and marked "insufficient sample"; no approach is proposed for it | None to a user | AC3 |
| X2 | The model times out or fails a guardrail on a document | The MODEL value counts as empty (false negative); the failure is counted on the run | None to a user | AC4 |
| X3 | Two approaches have the same F1 for a type | The approach with fewer model calls is proposed (OCR_TEMPLATE before OCR_AND_MODEL before MODEL) | None to a user | AC5 |
| X4 | A sample row names a document or field that does not exist | The sample load is refused in full | MSG-P10-001 | AC6 |
| X5 | No approach reaches precision 0.95 on a field at any confidence | The field is proposed as review-only | None to a user | AC7 |
| X6 | Evaluation started while the same one is running | Refused with 409 | MSG-P10-003 | AC8 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E1-060-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the extraction pipeline (RWB-E1-053) and the harness (RWB-E1-058) |
| Negotiable | Thresholds, sample size floor and the tie order are parameters in the policy row |
| Valuable | Sets the review threshold that decides how many documents an officer checks by hand |
| Estimable | Two scorers and one proposal rule on top of the existing harness |
| Small | Under two weeks with one developer |
| Testable | Each criterion runs on a fixture of labeled documents with known counts |

## 7. Acceptance criteria

```gherkin
Feature: Extraction evaluation [E1c]

  Background:
    Given sample "EXTRACT-S1" version 1 holds 40 court notices of type "COURT_NOTICE" with labels for fields court_name, case_number and hearing_date
    Given the target precision is 0.95 and the minimum labeled documents per type is 30

  Scenario: AC1 Scores per field
    Given the labeled sample
    When the three approaches run
    Then one score row exists per field and approach: 3 fields x 3 approaches for "COURT_NOTICE"
    Then for field hearing_date with approach OCR_TEMPLATE, 34 true positives, 2 false positives and 4 false negatives give precision 0.9444 and recall 0.8947
    Then each score row holds the model version and the prompt version "PR1" where the approach calls the model

  Scenario: AC2 Decision recorded
    Given the scores for "COURT_NOTICE"
    When the proposal is built
    Then the evaluation run names, for "COURT_NOTICE", the approach with the highest mean F1 and its precision and recall per field
    Then it names the proposed confidence threshold: the lowest confidence at which every chosen field reaches precision 0.95
    Then the export lists one row per document type for the solution architect's architecture decision

  Scenario: AC3 A type with too few labels
    Given type "TITLE_DEED" has 12 labeled documents
    When the evaluation runs
    Then the system scores "TITLE_DEED" and marked "insufficient sample"
    Then no approach and no threshold are proposed for "TITLE_DEED"

  Scenario: AC4 A model failure counts against the model approaches
    Given the model stub times out on document 7 of 40
    When the approach MODEL runs
    Then each labeled field of document 7 counts as a false negative for MODEL
    Then the evaluation run holds failure count TIMED_OUT 1

  Scenario: AC5 Equal F1
    Given OCR_TEMPLATE and OCR_AND_MODEL both have mean F1 0.9310 for "COURT_NOTICE"
    When the proposal is built
    Then the system proposes OCR_TEMPLATE

  Scenario: AC6 A sample row for a document that does not exist
    Given the sample file has a row for a document ID that the P5 interface does not return
    When RW-COE loads the file
    Then the system refuses the load with 422 and MSG-P10-001 naming the row number
    Then the system stores no row of the file

  Scenario: AC7 A field that never reaches the target
    Given field case_number reaches at most precision 0.91 for every approach and confidence
    When the proposal is built
    Then the system proposes case_number as review-only for "COURT_NOTICE"

  Scenario: AC8 The same evaluation twice
    Given the evaluation of "EXTRACT" on "EXTRACT-S1" version 1 is running
    When RW-COE starts it again
    Then the system refuses the request with 409 and MSG-P10-003
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A value is a true positive when it equals the label after trim and case folding; dates compare as dates; personal fields compare by SHA-256 hash | agent_sample.expected_value (New); CTL-11 |
| BR2 | Precision = TP / (TP + FP); recall = TP / (TP + FN); F1 = 2PR / (P + R); 4 decimals | agent_evaluation (New) |
| BR3 | A type with fewer labeled documents than the minimum (30, assumed; DL19) gets no proposal | agent_policy row EXTRACT (New) |
| BR4 | The proposed threshold is the lowest confidence where precision reaches the target (0.95, assumed; DL11); a field that never reaches it is review-only | REQ-DCM-005; document_field.confidence |
| BR5 | Ties go to the approach with fewer model calls | agent_policy row EXTRACT (New) |
| BR6 | The OCR_TEMPLATE approach reads stored fields only and makes no model call | DT06 |

## 9. State transitions

None. This story does not change a case status. It writes one evaluation run (RUNNING to DONE) and its score rows. The threshold it proposes takes effect only when P5 loads it as a new reference data version.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Loads the sample, starts the evaluation, reads and exports results (Rules and parameters CRUD) |
| RW-RISK | Reads results (Rules and parameters R) |
| SY-AGENT | Reads document content and fields (Documents R) |
| SY-OCR | Produced the OCR fields earlier; not called here |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-006 | document | storage_ref | Read (content through the P5 interface) |
| DF-DOC-013 | document_field | document_id | Read |
| DF-DOC-014 | document_field | field_name | Read |
| DF-DOC-015 | document_field | field_value | Read |
| DF-DOC-016 | document_field | confidence | Read |
| DF-DOC-017 | document_field | confirmed_by | Read |
| DF-AGT-063 | agent_sample | sample_code | Write |
| DF-AGT-064 | agent_sample | sample_version | Write |
| DF-AGT-065 | agent_sample | subject_type | Write |
| DF-AGT-066 | agent_sample | subject_id | Write |
| DF-AGT-067 | agent_sample | label_key | Write |
| DF-AGT-068 | agent_sample | expected_value | Write |
| DF-AGT-069 | agent_sample | labeled_by | Write |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-044 | agent_run | trigger_event | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-050 | agent_run | confidence | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-052 | agent_run | tokens_in | Write |
| DF-AGT-053 | agent_run | tokens_out | Write |
| DF-AGT-054 | agent_run | cost_thb | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-057 | agent_run | evaluation_run_id | Write |
| DF-AGT-070 | agent_evaluation_run | id | Write |
| DF-AGT-071 | agent_evaluation_run | agent_code | Write |
| DF-AGT-072 | agent_evaluation_run | sample_code | Write |
| DF-AGT-073 | agent_evaluation_run | sample_version | Write |
| DF-AGT-077 | agent_evaluation_run | status | Write |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Write |
| DF-AGT-078 | agent_evaluation_run | started_at | Write |
| DF-AGT-079 | agent_evaluation_run | finished_at | Write |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
| DF-AGT-088 | agent_evaluation | approach | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-091 | agent_evaluation | true_positive | Write |
| DF-AGT-092 | agent_evaluation | false_positive | Write |
| DF-AGT-093 | agent_evaluation | false_negative | Write |
| DF-AGT-095 | agent_evaluation | precision_value | Write |
| DF-AGT-096 | agent_evaluation | recall_value | Write |
| DF-AGT-084 | agent_evaluation_run | proposal | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/agent-samples** (new, RWB-E1-058): multipart file (CSV: subject_type DOCUMENT, subject_id, label_key = field name, expected_value), agent "EXTRACT", sampleCode; 201 AgentSample; errors 401, 403, 422 (MSG-P10-001), 503; Rules and parameters C; each load is a new sample version.

**POST /api/recovery/v1/admin/agent-evaluations** (new): AgentEvaluationRequest with agent "EXTRACT", sampleCode "EXTRACT-S1", sampleVersion 1, approaches ["OCR_TEMPLATE", "MODEL", "OCR_AND_MODEL"]; 202 AgentEvaluationRun; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-002), 503; Rules and parameters C; one RUNNING run per agent and sample version.

**GET /api/recovery/v1/admin/agent-evaluations** (new): query agent, from, to; 200 AgentEvaluationRun[] with score rows and the proposal per document type; errors 401, 403, 503; Rules and parameters R. Export: Accept text/csv returns the proposal rows.

**Interfaces called:** P5 DocumentQueryService.getFields(documentId) and DocumentQueryService.getContent(documentId), as SY-AGENT.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/eval/extraction/`, Java package `recovery.agent.eval.extraction`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractionApproachRunner | Service | Produces field values per document for each of the three approaches |
| FieldMatchScorer | Service | Applies BR1 and BR2 per field and approach |
| ExtractionProposalBuilder | Service | Applies BR3 to BR5 and writes the proposal JSON on the evaluation run |
| SampleRowValidator | Service | Checks each sample row against P5 before the load is stored |
| prompt EXTRACT PR1 and schema extract-fields-v1 | Rule table | Prompt and output schema loaded through the configuration endpoint |

**Database:** adds column proposal jsonb to agent_evaluation_run in migration `V10_003__evaluation_proposal.sql`; writes agent_sample, agent_run, agent_evaluation_run, agent_evaluation.

**Configuration and reference data:** agent_policy EXTRACT P1 holds the target precision 0.95, the minimum sample 30 and the tie order; loaded by RW-COE, approved by RW-RISK. Document types come from LOV-DOC-TYPE through P4.

**Build steps**
1. Build SampleRowValidator and the hash of personal label values (AC6).
2. Build ExtractionApproachRunner for OCR_TEMPLATE over the P5 interface (AC1).
3. Add the MODEL and OCR_AND_MODEL paths through AgentOrchestrator in shadow (AC1, AC4).
4. Build FieldMatchScorer with a fixture of 40 court notices and known counts (AC1).
5. Build ExtractionProposalBuilder and the CSV export (AC2, AC3, AC5, AC7).
6. Add the running-evaluation check (AC8) and the access test.

**Feature flag:** `rwb.agent.extraction-eval`. Off: the approaches list accepts only AGENT and the extraction approaches are refused with 422.

**Done when:** the tests in section 16 pass and a DEV run over the six types produces one proposal row per type.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A sample row fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The sample has no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. RW-COE reads the scores and the proposal through GET /admin/agent-evaluations and exports them as CSV.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-060-01 | AC1, BR1, BR2 | System | 40 COURT_NOTICE documents; hearing_date OCR counts 34, 2, 4 |
| TC-E1-060-02 | AC2, BR4 | System | Scores for COURT_NOTICE across three approaches |
| TC-E1-060-03 | AC3, BR3 | System | TITLE_DEED with 12 labeled documents |
| TC-E1-060-04 | AC4 | System | Model stub times out on document 7 of 40 |
| TC-E1-060-05 | AC5, BR5 | System | Equal mean F1 0.9310 |
| TC-E1-060-06 | AC6 | System | Sample row with an unknown document ID |
| TC-E1-060-07 | AC7, BR4 | System | case_number at most precision 0.91 |
| TC-E1-060-08 | AC8 | System | Evaluation EXTRACT on EXTRACT-S1 version 1 running |
| TC-E1-060-09 | Access | Access | RW-CASEOWN calls POST /admin/agent-evaluations; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: target precision, minimum sample and tie order are policy values.
- No personal data in logs, tests or prompts; personal label values are stored as hashes and documents in tests are synthetic.
- No read of another module's tables; document content and fields come through the P5 interface.
- The evaluation does not change any document_field value or any threshold in force.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified with a confidence score; below the threshold goes to review | Business Requirements Program, section 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-02, TC-E1-060-03, TC-E1-060-05, TC-E1-060-07 |
| REQ-DCM-006 | Fields extracted for the agreed types | Business Requirements Program, section 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | R-UNI-32 | TC-E1-060-01, TC-E1-060-04, TC-E1-060-06, TC-E1-060-08, TC-E1-060-09 |

## 19. Out of scope

- Applying the chosen threshold to the review queue (P5, RWB-E1-054).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- Writing the architecture decision record itself (solution architect, outside the code).
