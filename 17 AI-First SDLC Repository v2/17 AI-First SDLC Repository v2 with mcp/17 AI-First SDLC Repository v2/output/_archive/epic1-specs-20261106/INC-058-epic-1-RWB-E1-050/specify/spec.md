# Technical Specification — RWB-E1-050 Document classification

| Field | Value |
|---|---|
| Story | RWB-E1-050 — Document classification |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-058-epic-1-RWB-E1-050` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-015); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 050 Document classification v1.md`; FSD P5 A2.8; TSD P5 T3.1 |
| Upstream IDs | BRD-RWB-005; FR-RWB-015; REQ-DCM-005; US-RWB-E1-050; CTX-FEATURE-005; CTL-11; DL11, DL19, DL26, DL33; R-UNI-32, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner and risk and model risk officer (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Items sent to review appear on SCR-31, built in RWB-E1-054; the evaluation report is a file in the standard container. |
| Logic In Scope | `YES` — classification selection, PII masking, model call, ranking, threshold, review routing, fallback, idempotency and evaluation. |
| API In Scope | `NO` — no endpoint or contract change. The story adds JOB-12's `classifyStep` and the `ClassifierClient` / `ClassificationReader` interfaces. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-12 Document intake; `document_intake` (RWB-E1-049); `document_text`; document type table (RWB-E1-025); P10 model gateway; ACE PII masking service. |
| New Nodes Required | `YES` — `ClassifyStep`, `ClassifierClient`, `ModelGatewayClassifier`, `TextMasker`, `ClassificationReader`, `ClassificationEvaluationRunner`. |
| Inherited Existing Behavior | OCR output and intake (RWB-E1-049); document types and labels (RWB-E1-025); document hub parameters (RWB-E1-024); ACE PII masking service; P10 model gateway (DL33). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A document is classified into one of the agreed types with a confidence score. | SPEC-RWB-E1-050-004, SPEC-RWB-E1-050-005 | DIRECT | Scores per type and model version. | COVERED |
| BR2 | Below the threshold the document goes to the review queue; the threshold is inclusive. | SPEC-RWB-E1-050-006, SPEC-RWB-E1-050-007 | DIRECT | `score >= threshold` passes; `CLASSIFY_THRESHOLD` 0.80 (assumed; DL11). | COVERED |
| BR3 | The types come from the type table in force and the threshold from `document_hub_parameter`. | SPEC-RWB-E1-050-004, SPEC-RWB-E1-050-013 | DIRECT | Six type codes and labels read per run; threshold is data. | COVERED |
| BR4 | A model that does not answer within the timeout falls back to review and the fallback is recorded. | SPEC-RWB-E1-050-009 | DIRECT | `MODEL_UNAVAILABLE`; `classify_fallback=true`. | COVERED |
| BR5 | Accuracy on the labeled sample is at least 90 percent before the step runs in production. | SPEC-RWB-E1-050-012 | DIRECT | At least 162 of 180; report with confusion matrix and model version. | COVERED |
| BR6 | Personal identifiers are masked before text leaves the document hub. | SPEC-RWB-E1-050-003 | DIRECT | National ID, account and phone numbers replaced with tokens through the ACE masking service. | COVERED |
| BR7 | An item classified once is not classified again. | SPEC-RWB-E1-050-010 | DIRECT | Items with `predicted_type` or `review_reason` are skipped. | COVERED |
| AC1 | At least 162 of 180 labeled documents get the labeled type; the report holds accuracy, the 6 by 6 confusion matrix and the model version. | SPEC-RWB-E1-050-012 | DIRECT | SIT evaluation; report at `evaluation/classification/2026-11-20.json`. | COVERED |
| AC2 | Scores `COURT_NOTICE 0.62` and `DEMAND_LETTER 0.21` give `predicted_type=COURT_NOTICE`, confidence 0.6200, `LOW_CONFIDENCE`; candidates hold both; attach marks for type review with write-once false. | SPEC-RWB-E1-050-005, SPEC-RWB-E1-050-007 | DIRECT | Top two candidates; review reason. | COVERED |
| AC3 | A top score of `APPRAISAL_REPORT 0.80` is classified with no review reason. | SPEC-RWB-E1-050-006 | DIRECT | Inclusive threshold. | COVERED |
| AC4 | A classifier that does not answer in 60 seconds gives `MODEL_UNAVAILABLE`, no predicted type, fallback recorded. | SPEC-RWB-E1-050-009 | DIRECT | Timeout path. | COVERED |
| AC5 | A returned type `LOAN_CONTRACT 0.91` gives `UNKNOWN_TYPE`; candidates hold the two highest agreed types. | SPEC-RWB-E1-050-008 | DIRECT | Unknown type branch. | COVERED |
| AC6 | An upload of type `TITLE_DEED` is not classified and keeps its type. | SPEC-RWB-E1-050-002 | DIRECT | Given type skips classification. | COVERED |
| AC7 | An item in `RESCAN` is not classified. | SPEC-RWB-E1-050-002 | DIRECT | Only `ocr_status='DONE'` is selected. | COVERED |
| AC8 | 20 classified items are not called again and their results are unchanged. | SPEC-RWB-E1-050-010 | DIRECT | Idempotency by result columns. | COVERED |
| AC9 | Changing `CLASSIFY_THRESHOLD` to 0.90 makes a 0.85 item `LOW_CONFIDENCE` with no code or deployment change. | SPEC-RWB-E1-050-013 | DIRECT | Parameter read per run. | COVERED |
| AC10 | National ID `<tokenized>` and account `TEST-ACC-0001` are replaced by tokens before the model call. | SPEC-RWB-E1-050-003 | DIRECT | Masking before the call; prompt not logged. | COVERED |
| X1 | Top score below threshold. | SPEC-RWB-E1-050-007 | DIRECT | `LOW_CONFIDENCE`; two candidates. | COVERED |
| X2 | Top score exactly at threshold. | SPEC-RWB-E1-050-006 | DIRECT | Classified. | COVERED |
| X3 | Classifier timeout. | SPEC-RWB-E1-050-009 | DIRECT | `MODEL_UNAVAILABLE`; fallback recorded. | COVERED |
| X4 | Type code not in the table in force. | SPEC-RWB-E1-050-008 | DIRECT | `UNKNOWN_TYPE`; two agreed candidates. | COVERED |
| X5 | Item already carries a type (upload). | SPEC-RWB-E1-050-002 | DIRECT | Not classified. | COVERED |
| X6 | Item in `RESCAN` or `FAILED`. | SPEC-RWB-E1-050-002 | DIRECT | Not classified. | COVERED |
| X7 | Repeat run over classified items. | SPEC-RWB-E1-050-010 | DIRECT | No second call. | COVERED |
| X8 | User without Documents R reads a classification. | SPEC-RWB-E1-050-015 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **each scanned document classified into one of the six agreed types with a confidence score, and any document below the threshold sent to the review queue with its top two candidate types**, so that **each document is filed under the right type and checklist item without a person typing it**.

The story adds the classification step of JOB-12. It masks personal identifiers, sends the first pages to the classifier through the P10 gateway, ranks the scores and records the result. A confident result is filed automatically; an uncertain result goes to a person with the top two candidates. It adds no screen and no endpoint.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake, `classifyStep` after `ocrStep`; `ClassificationEvaluationRunner` on demand. |
| Preconditions | RWB-E1-049 done (OCR text and status); RWB-E1-025 done (type table in force); `CLASSIFY_THRESHOLD=0.80`, `CLASSIFY_MAX_PAGES=3`, `CLASSIFY_TIMEOUT_SECONDS=60` in `document_hub_parameter` (assumed; DL11); classifier reachable through the P10 gateway under DL33; labeled sample of 180 synthetic documents; `rwb.dochub.classify` flag on. |
| Input | Intake items with `ocr_status='DONE'`, no `predicted_type`, no given type; first `CLASSIFY_MAX_PAGES` pages of text. |
| Output | `predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version`, `review_reason`, `classify_fallback`; evaluation report; job counts. |
| Feature flag | `rwb.dochub.classify`. Off: `classifyStep` is skipped and every scanned item goes to review with reason `LOW_CONFIDENCE`. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `ocr_status` | OCR step | Read-only | Must be `DONE` to classify |
| `document_intake` | `predicted_type` | Classifier | System writes | One of the type codes in force, or null on fallback/unknown |
| `document_intake` | `classification_confidence` | Classifier | System writes | 0.0000..1.0000; top score |
| `document_intake` | `type_candidates` | Classifier | System writes | jsonb with the top two agreed types and scores |
| `document_intake` | `classifier_version` | Classifier response | System writes | Model version from the gateway |
| `document_intake` | `review_reason` | Threshold/fallback | System writes | `LOW_CONFIDENCE`, `MODEL_UNAVAILABLE`, `UNKNOWN_TYPE` |
| `document_intake` | `classify_fallback` | Timeout path | System writes | True when the fallback was used |
| `document` | `document_type` | Attach | System writes | The predicted or confirmed type |
| `document` | `type_candidates` | Attach | System writes | Read by the review queue |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| OCR `DONE` | Classification | Top score at or above the threshold and the type is in force | Classified | `predicted_type`, confidence, candidates, version; no review reason |
| OCR `DONE` | Classification | Top score below the threshold | Review | `LOW_CONFIDENCE`; two candidates; attach stores PENDING with write-once false |
| OCR `DONE` | Classification | Classifier timeout | Review | `MODEL_UNAVAILABLE`; no predicted type; `classify_fallback=true` |
| OCR `DONE` | Classification | Returned type not in force | Review | `UNKNOWN_TYPE`; no predicted type; two agreed candidates |
| Classified | Repeat run | `predicted_type` or `review_reason` set | Unchanged | No second call |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Top score below threshold | `LOW_CONFIDENCE`; two candidates; review at attach | MSG-P5-003 |
| X2 | Top score at threshold | Classified; no review reason | None |
| X3 | Classifier timeout | `MODEL_UNAVAILABLE`; no predicted type; fallback recorded | MSG-P5-003 |
| X4 | Type not in force | `UNKNOWN_TYPE`; two agreed candidates | MSG-P5-003 |
| X5 | Upload with a type | Not classified; type unchanged | None |
| X6 | Item in `RESCAN` or `FAILED` | Not classified | None |
| X7 | Repeat run | No second call; results unchanged | None |
| X8 | User without Documents R | 403; no classification returned | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | None directly. The type and confidence are read through the document read endpoint (RWB-E1-024) and the review queue (RWB-E1-054). |
| Contract delta | None. The job, the classifier adapter and `ClassificationReader` are internal. |
| Backward compatibility | Unchanged. |
| Authorization | SY-OCR under Documents CRU for the job; a reader needs Documents R and case scope through the reading endpoint. |
| Error behaviour | The job falls back to review on timeout; no synchronous API error. An unauthorised read returns 403 MSG-P4-002. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes; SCR-31 is built in RWB-E1-054. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-005; SPEC-RWB-E1-050-001..016 | New job step, masking, classifier adapter, reader and evaluation runner. | Selection and skip rules; masking; ranking; threshold 0.79/0.80/0.81; low confidence; unknown type; timeout; idempotency; threshold change; report content. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ClassifyStep` | Job | Step of JOB-12: select, mask, call, rank, apply the threshold and write. |
| `ClassifierClient`, `ModelGatewayClassifier` | Service | Calls the classifier through the P10 model gateway with the timeout. |
| `TextMasker` | Service | Calls the ACE PII masking service for national ID, account and phone numbers. |
| `ClassificationReader` | Published interface | `forIntake(intakeId)`: predicted type, confidence, candidates, version and review reason. |
| `ClassificationEvaluationRunner` | Service | Runs the labeled sample and writes accuracy and the confusion matrix. |
| `DocumentIntakeRepository` | Repository | From RWB-E1-049; adds the classification columns. |

### Package and boundaries

Folder `recovery/dochub/classify`, Java package `recovery.dochub.classify`. The package reads
`document_text` and writes classification columns on `document_intake`; it reads the type table through
`DocumentTypeCatalog` and the threshold through `DocumentHubParameters`. It calls the model only through
the P10 gateway; no document text leaves the bank.

### Data and migration

Flyway `V1_5_050__intake_classification.sql` adds to `document_intake`: `predicted_type varchar(30)`,
`classification_confidence numeric(5,4)`, `type_candidates jsonb`, `classifier_version varchar(40)`,
`classify_fallback boolean default false`; adds `type_candidates jsonb` to `document`, which
RWB-E1-032 writes on attach and RWB-E1-054 reads (`document.document_type` already exists from
RWB-E1-024). Index `ix_intake_classify` on `document_intake (ocr_status)` where `predicted_type is null`
and `review_reason is null`.

### Classification flow

1. `ClassifyStep` selects items with `ocr_status='DONE'`, no `predicted_type` and no given document type,
   locking each row; uploads carry their type and are skipped.
2. Take the text of the first `CLASSIFY_MAX_PAGES` pages; replace national ID numbers, account numbers
   and phone numbers with tokens through the ACE PII masking service.
3. Send the masked text and the six type codes with their labels from the type table in force to the
   classifier; receive a score per type and the model version.
4. Rank the scores; write `predicted_type`, `classification_confidence`, the top two candidates in
   `type_candidates` and `classifier_version`.
5. If the top score is at or above `CLASSIFY_THRESHOLD` and the type is in force, mark classified with no
   `review_reason`; attach stores the document with `review_status='NOT_NEEDED'`.
6. Below the threshold, set `review_reason='LOW_CONFIDENCE'`; attach stores the document with
   `review_status='PENDING'` and `write_once=false`, so it appears on SCR-31 with its two candidates.
7. A type outside the table sets `review_reason='UNKNOWN_TYPE'` with no predicted type; attach holds the
   item for a person.
8. A timeout sets `review_reason='MODEL_UNAVAILABLE'`, no predicted type and `classify_fallback=true`.

### Evaluation

`ClassificationEvaluationRunner` runs the labeled sample of 180 synthetic documents (30 per type) and
writes `evaluation/classification/{runDate}.json` to the standard container and the job record. The
report holds accuracy, the 6 by 6 confusion matrix and the model version. The step is not promoted to
production unless at least 162 of 180 are correct (90 percent; story BR5).

### Transaction and events

Each item is one transaction: classification columns and review reason commit together. A timeout
commits the fallback marker. No event is published; RWB-E1-032 and RWB-E1-054 read the result through
`ClassificationReader`.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR OCR and extraction pipeline | Documents CRU; runs classification and writes the result | All |
| SY-AGENT Agent platform | Serves the model call through the gateway | All |
| RW-CASEOWN and roles with Documents R | Read type and confidence in scope | Own/team |
| RW-COE Center of excellence analyst | Runs the evaluation and reads the report | All |
| RW-RISK Risk and model risk officer | Reviews the evaluation report before production use | All |

### Observability and operations

- Job record: items classified, low confidence, unknown type, fallback, timeout, model version, duration.
- Metrics: classification rate, review rate by reason, mean confidence, model latency, fallback rate.
- Alerts: timeout rate above threshold; accuracy below 90 percent; model route unavailable.
- Prompts and responses are not logged; logs carry intake ID and scores only.

### Performance

- Up to 3 pages per item; one model call per item; 60-second timeout.
- Classification runs in the existing JOB-12 worker model; no extra queue.
- The evaluation run is on demand and does not block intake.

### Feature flag and rollback

- `rwb.dochub.classify`. Off: `classifyStep` is skipped and every scanned item goes to review with
  `LOW_CONFIDENCE`.
- Rollback: turn the flag off; redeploy the previous tag. Classification columns are additive and
  nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-050-01 | AC1, BR1, BR5 | System | Labeled sample of 180 synthetic documents | At least 162 correct; report with accuracy, matrix and version |
| TC-E1-050-02 | AC2, BR2 | System | Stub scores `COURT_NOTICE 0.62`, `DEMAND_LETTER 0.21` | `LOW_CONFIDENCE`; both candidates; attach PENDING, write-once false |
| TC-E1-050-03 | AC3, BR2 | System | Stub score `APPRAISAL_REPORT 0.80` | Classified; no review reason |
| TC-E1-050-04 | AC4, BR4 | System | Stub does not answer for 60 seconds | `MODEL_UNAVAILABLE`; no type; fallback true |
| TC-E1-050-05 | AC5, BR3 | System | Stub returns `LOAN_CONTRACT 0.91` | `UNKNOWN_TYPE`; two highest agreed types |
| TC-E1-050-06 | AC6 | System | Upload of type `TITLE_DEED` | No call; type unchanged |
| TC-E1-050-07 | AC7 | System | Item in `RESCAN` | No call |
| TC-E1-050-08 | AC8, BR7 | System | 20 classified items | No call; results unchanged |
| TC-E1-050-09 | AC9, BR3 | System | Threshold 0.90; item 0.85 | `LOW_CONFIDENCE`; no deployment |
| TC-E1-050-10 | AC10, BR6 | System | Synthetic national ID and account number | Tokens in the text received by the stub |
| TC-E1-050-11 | X8 | Security | RW-CAPACITY (no Documents right) reads a classified document | 403 MSG-P4-002 |
| TC-E1-050-U1 | BR2, BR4, BR6, AC3, AC4, AC10 | Unit | Scores 0.79/0.80/0.81; timeout; national ID and account number | Threshold boundary; fallback recorded; tokens in the masked text |

## Guardrails

- No business value in code: types, thresholds, pages read and the timeout are data.
- No personal data in logs, tests or prompts: text is masked before the model call; prompts and
  responses are not logged; test documents are synthetic.
- No read of another module's tables.
- The model endpoint is inside the SCB tenant (DL33); no document text leaves the bank.

## Out of scope

- The review queue screen and the correction fed back to the labeled set (RWB-E1-054).
- Field extraction and its evaluation (RWB-E1-053, RWB-E1-060).
- Attach to the case (RWB-E1-032).
- Stage 2 and 3 document types (RWB-E2-025).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | Business Requirements Epic 1, section 3.5 | FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-40 | TC-E1-050-01..11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2; SPEC-013 | Is `CLASSIFY_THRESHOLD` 0.80? | Decides what goes to review. | Assumed 0.80 until the RWB-E1-060 report (DL11); it is a parameter, and RWB-E1-054 routes on the same value. | RESOLVED | SPEC-013 |
| CLAR-002 | Preconditions; SPEC-004 | Are the page limit and timeout fixed? | Cost and latency. | `CLASSIFY_MAX_PAGES=3` and `CLASSIFY_TIMEOUT_SECONDS=60` are assumed (DL11) and loaded as data. | RESOLVED | SPEC-004 |
| CLAR-003 | Preconditions; SPEC-004 | Which classifier is used? | Adapter target. | The model endpoint is set under DL33 and reached through the P10 model gateway; the route is a property. | RESOLVED | SPEC-004 |
| CLAR-004 | AC5; SPEC-008 | What are "the two highest agreed types" when the model returns an unknown type? | Candidate list. | The two highest scores among the six type codes in the version in force, excluding the unknown code. | RESOLVED | SPEC-008 |
| CLAR-005 | AC4; SPEC-009 | How is "the fallback was used" recorded? | Field choice. | `document_intake.classify_fallback` boolean, set true on the timeout path. | RESOLVED | SPEC-009 |
| CLAR-006 | AC2; SPEC-007 | Why does a low-confidence document set write-once false? | Correction path. | The type is not confirmed, so the document must stay correctable until review; the story states this in AC2. | RESOLVED | SPEC-007 |
| CLAR-007 | BR5; SPEC-012 | Is the accuracy gate 90 percent? | Promotion decision. | Yes: at least 162 of 180 correct, with the report reviewed by the risk and model risk officer. | RESOLVED | SPEC-012 |
| CLAR-008 | AC1; SPEC-012 | Where is the evaluation report written? | Evidence location. | `evaluation/classification/{runDate}.json` in the standard container and on the job record (story AC1). | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story or the named decision log
entries. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this batch story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New JOB-12 classification step with masking, threshold and evaluation; no screen and no contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: batch classification step with internal interfaces only]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 10 acceptance criteria, 8 exception paths and 5 classification states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
