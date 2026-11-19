# Technical Specification — RWB-E1-060 Extraction evaluation [E1c]

| Field | Value |
|---|---|
| Story | RWB-E1-060 — Extraction evaluation [E1c] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-074-epic-1-RWB-E1-060` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 060 Extraction evaluation E1c v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-DCM-005, REQ-DCM-006; US-RWB-E1-060; FEAT-AGT-04; R-UNI-32; DL11, DL19; ADR-009 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen; results are read and exported through the API. |
| Logic In Scope | `YES` — three extraction approaches, field matching, precision/recall, proposal, threshold, insufficient sample and tie-break. |
| API In Scope | `YES` — the RWB-E1-058 evaluation endpoints are reused, but `GET /admin/agent-evaluations` gains a `text/csv` representation for the proposal export. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `agent_sample`, `agent_run`, `agent_evaluation_run`, `agent_evaluation` (from RWB-E1-058); `agent_policy.config` (design extension); P5 `DocumentQueryService`. |
| New Nodes Required | `YES` — `ExtractionApproachRunner`, `FieldMatchScorer`, `ExtractionProposalBuilder`, `SampleRowValidator`, `extract-fields-v1` schema and EXTRACT prompt. |
| Inherited Existing Behavior | Agent platform (RWB-E1-058), agent client (RWB-TE-013), OCR pipeline and document fields (RWB-E1-053), documents and fields (RWB-E1-024/025/050), masking (RWB-E1-037), migrations (RWB-E1-044). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A value is a true positive when it equals the label after trim and case folding; dates compare as dates; personal fields compare by SHA-256 hash. | SPEC-RWB-E1-060-002, SPEC-RWB-E1-060-006 | DIRECT | `FieldMatchScorer` comparator per field type. | COVERED |
| BR2 | Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2PR/(P+R); 4 decimals. | SPEC-RWB-E1-060-007 | DIRECT | `BigDecimal`, 4 decimals, divide-by-zero guarded. | COVERED |
| BR3 | A type with fewer labeled documents than the minimum (30, assumed; DL19) gets no proposal. | SPEC-RWB-E1-060-012 | DIRECT | Count distinct labeled documents per type. | COVERED |
| BR4 | The proposed threshold is the lowest confidence where precision reaches the target (0.95, assumed; DL11); a field that never reaches it is review-only. | SPEC-RWB-E1-060-010, SPEC-RWB-E1-060-011 | DIRECT | Sweep observed confidence values; per-field check. | COVERED |
| BR5 | Ties go to the approach with fewer model calls. | SPEC-RWB-E1-060-013 | DIRECT | OCR_TEMPLATE < OCR_AND_MODEL < MODEL. | COVERED |
| BR6 | OCR_TEMPLATE reads stored fields only and makes no model call. | SPEC-RWB-E1-060-003 | DIRECT | P5 `getFields` only. | COVERED |
| AC1 | One score row per field and approach (3 × 3 for COURT_NOTICE); hearing_date OCR_TEMPLATE 34/2/4 gives 0.9444 and 0.8947; versions on model rows. | SPEC-RWB-E1-060-006, SPEC-RWB-E1-060-007, SPEC-RWB-E1-060-008 | DIRECT | Score rows per label key and approach. | COVERED |
| AC2 | The proposal names the highest mean F1 approach with per-field precision/recall, the lowest threshold where every chosen field reaches 0.95, and one export row per type. | SPEC-RWB-E1-060-009, SPEC-RWB-E1-060-010, SPEC-RWB-E1-060-015 | DIRECT | Proposal JSON and CSV export. | COVERED |
| AC3 | TITLE_DEED with 12 labeled documents is scored and marked insufficient sample; no approach or threshold proposed. | SPEC-RWB-E1-060-012 | DIRECT | Minimum 30 distinct documents. | COVERED |
| AC4 | A model timeout on document 7 counts each labeled field as a false negative for MODEL; failure count TIMED_OUT 1. | SPEC-RWB-E1-060-014 | DIRECT | Failure counted on the evaluation run. | COVERED |
| AC5 | Equal mean F1 0.9310 for OCR_TEMPLATE and OCR_AND_MODEL proposes OCR_TEMPLATE. | SPEC-RWB-E1-060-013 | DIRECT | Fewer model calls wins. | COVERED |
| AC6 | A sample row for an unknown document refuses the whole load 422 MSG-P10-001 with the row number. | SPEC-RWB-E1-060-001 | DIRECT | Validate every row against P5 before insert. | COVERED |
| AC7 | A field that never reaches 0.95 is proposed review-only. | SPEC-RWB-E1-060-011 | DIRECT | No threshold for that field. | COVERED |
| AC8 | A second evaluation while one is running is refused 409 MSG-P10-003. | SPEC-RWB-E1-060-016 | DIRECT | Partial unique index from RWB-E1-058. | COVERED |
| X1 | Type has fewer than 30 labeled documents. | SPEC-RWB-E1-060-012 | DIRECT | Scored; `insufficient sample`; no proposal. | COVERED |
| X2 | Model timeout or guardrail failure on a document. | SPEC-RWB-E1-060-014 | DIRECT | Empty value = false negative; failure counted. | COVERED |
| X3 | Two approaches have the same F1. | SPEC-RWB-E1-060-013 | DIRECT | Fewer model calls. | COVERED |
| X4 | Sample row names an unknown document or field. | SPEC-RWB-E1-060-001 | DIRECT | Whole load refused 422. | COVERED |
| X5 | No approach reaches 0.95 for a field. | SPEC-RWB-E1-060-011 | DIRECT | Review-only. | COVERED |
| X6 | Same evaluation already running. | SPEC-RWB-E1-060-016 | DIRECT | 409 MSG-P10-003. | COVERED |
| X7 | Role without the right. | SPEC-RWB-E1-060-017 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **field extraction for the six document types scored against the labeled sample for three approaches (OCR template, model, and OCR checked by the model)**, so that **the extraction approach and the confidence threshold for each document type are chosen on measured precision and recall**.

The story adds no screen and changes no document. It runs three approaches over the same reviewed
documents, scores each field, and writes one proposal per document type. The proposal is evidence for
the solution architect's architecture decision; the threshold takes effect only when P5 loads it as a
new reference version.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/agent-samples` to load the sample; `POST /admin/agent-evaluations` to start the run. |
| Preconditions | RWB-E1-053 done (six types, `document_field` with confidence); RWB-E1-058 done; approved policy `EXTRACT` P1 (SHADOW, tools read_document_content/read_document_fields) and prompt PR1; sample `EXTRACT-S1` v1 with at least 30 labeled documents per type; RW-COE holds Rules and parameters C. |
| Input | Labeled sample rows (document, field, expected value), stored OCR fields, document content, policy config. |
| Output | One evaluation run, one score row per field and approach, one proposal per document type, CSV export. |
| Feature flag | `rwb.agent.extraction-eval`. Off: only `AGENT` is accepted and extraction approaches are refused 422. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_sample` | `subject_type` | CSV | System-written | `DOCUMENT`. |
| `agent_sample` | `label_key` | CSV | System-written | Field name for the type. |
| `agent_sample` | `expected_value` | CSV | System-written | Personal values stored as SHA-256; dates as ISO dates. |
| `agent_evaluation` | `approach` | Request | System-written | `AGENT`, `OCR_TEMPLATE`, `MODEL`, `OCR_AND_MODEL`. |
| `agent_evaluation` | `true_positive`, `false_positive`, `false_negative` | Scorer | System-written | Non-negative integers. |
| `agent_evaluation` | `precision_value`, `recall_value` | Scorer | System-written | 4 decimals; null when denominator 0. |
| `agent_evaluation_run` | `proposal` | Builder | System-written | jsonb: approach, per-field metrics, threshold, review-only fields, sample size, insufficient flag. |
| `agent_evaluation_run` | `status` | Harness | `RUNNING` → `DONE` / `FAILED` | One RUNNING per agent/sample/version. |
| `agent_policy` | `config` | Policy file | Read-only | Target precision 0.95, minimum sample 30, tie order. |
| `document_field` | `field_value`, `confidence` | P5 | Read-only | Read through the interface only. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Evaluation started | Sample has labels; none running | `RUNNING` | Evaluation run row. |
| `RUNNING` | All approaches scored | No error | `DONE` | Score rows and proposal. |
| `RUNNING` | Unrecoverable error | Error | `FAILED` | Failure recorded; no proposal. |

This story changes no case status and no document field or threshold in force.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Fewer than 30 labeled documents | Scored; `insufficient sample`; no proposal | None to a user |
| X2 | Model timeout or guardrail failure | Each labeled field is a false negative; failure counted | None to a user |
| X3 | Equal F1 | Fewer model calls wins | None to a user |
| X4 | Unknown document or field in the sample | Whole load refused 422; row number named | MSG-P10-001 |
| X5 | No approach reaches 0.95 for a field | Field proposed review-only | None to a user |
| X6 | Same evaluation running | 409; one RUNNING row remains | MSG-P10-003 |
| X7 | Role without the right | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` — `text/csv` representation on an existing endpoint. |
| Existing endpoints used | `POST /api/recovery/v1/admin/agent-samples`; `POST /api/recovery/v1/admin/agent-evaluations`; `GET /api/recovery/v1/admin/agent-evaluations`. |
| Contract delta | `GET /admin/agent-evaluations` with `Accept: text/csv` returns one proposal row per document type. The TSD already describes the endpoint as JSON or CSV; `api.yaml` lists only JSON and is updated. |
| Backward compatibility | Additive representation; JSON unchanged. |
| Authorization | Rules and parameters C/R. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P10-003; 422 MSG-P10-001/002; 503. |
| Versioning | No version change; content negotiation only. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-060-001..020 | New approach runner, scorer, proposal builder and sample validator. | Positive, negative, boundary and error-path tests: 3×3 scores, precision/recall/F1, threshold sweep, 29/30 documents, tie, timeout, unknown row, CSV, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ExtractionApproachRunner` | Service | Produces field values per document for each of the three approaches. |
| `FieldMatchScorer` | Service | Applies BR1 and BR2 per field and approach. |
| `ExtractionProposalBuilder` | Service | Applies BR3..BR5 and writes the proposal JSON. |
| `SampleRowValidator` | Service | Checks every row against P5 before the load is stored. |
| `extract-fields-v1.json`, prompt `EXTRACT` PR1 | Rule table | Output schema and prompt loaded through the configuration endpoint. |

### Package and boundaries

`recovery.agent.eval.extraction`. Document content and fields are read only through P5
`DocumentQueryService.getFields` and `getContent` as `SY-AGENT`. No P5 table is read.

### Data and migration

`V10_003__evaluation_proposal.sql` adds `proposal` jsonb to `agent_evaluation_run` (already in the
logical data model, DF-AGT-084) and records the policy `config` key names. Reads: `document`,
`document_field`, `agent_sample`. Writes: `agent_sample`, `agent_run`, `agent_evaluation_run`,
`agent_evaluation`.

### Approaches

| Approach | Input | Model call | Value source |
|---|---|---|---|
| `OCR_TEMPLATE` | Stored `document_field` | No | `field_value` and `confidence` from P5. |
| `MODEL` | Document content | Yes, one per document | Agent answer fields. |
| `OCR_AND_MODEL` | Content + stored fields | Yes, one per document | Agent checked values. |

All three run over the same documents and labels. A model failure on a document gives every labeled
field of that document a false negative for the model approaches and increments the failure count.

### Metrics and proposal

- Match: trim and case-fold strings; compare dates as dates; compare personal values by SHA-256.
- Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2PR/(P+R); 4 decimals.
- Mean F1 per approach across the type's fields; highest wins; tie order `OCR_TEMPLATE`,
  `OCR_AND_MODEL`, `MODEL`.
- Threshold: sort the observed confidence values descending; for each candidate, compute precision for
  every chosen field using values at or above it; the lowest candidate where every field reaches 0.95
  is the proposal. A field that never reaches 0.95 is `reviewOnly`.
- A type with fewer than 30 distinct labeled documents is scored and marked `insufficientSample`; no
  approach and no threshold are proposed.

### Transaction and export

The evaluation run and score rows are written in the harness transaction; the proposal is written on
the run when scoring completes. The CSV export reads the stored proposal and writes one row per document
type with the approach, mean F1, per-field precision/recall, threshold, review-only fields, sample size
and insufficient flag. No document field or threshold in force is changed.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Rules and parameters CRUD | All |
| RW-RISK | Rules and parameters R | All |
| `SY-AGENT` | Documents R | All |
| `SY-OCR` | Produced the fields earlier; not called here | All |

### Observability, performance and rollback

- Metrics: documents per approach, model calls, failures by type, runtime, cost, proposal coverage.
- Alerts: evaluation FAILED, model failure rate, no proposal for a type.
- Performance: 40 court notices × 3 approaches in the fixture; model calls only for MODEL and
  OCR_AND_MODEL; 60-second timeout per call.
- Feature flag `rwb.agent.extraction-eval`: off refuses extraction approaches with 422.
- Rollback: flag off; redeploy the previous tag; `proposal` is nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-060-01 | AC1, BR1, BR2 | System | 40 COURT_NOTICE; hearing_date OCR 34/2/4 | 9 score rows; precision 0.9444; recall 0.8947 |
| TC-E1-060-02 | AC2, BR4 | System | Scores for COURT_NOTICE | Proposal names best mean F1, per-field metrics and threshold |
| TC-E1-060-03 | AC3, BR3 | System | TITLE_DEED with 12 documents | Scored; `insufficient sample`; no proposal |
| TC-E1-060-04 | AC4 | System | Model timeout on document 7 of 40 | Each labeled field a false negative; TIMED_OUT 1 |
| TC-E1-060-05 | AC5, BR5 | System | Equal mean F1 0.9310 | OCR_TEMPLATE proposed |
| TC-E1-060-06 | AC6 | System | Row with unknown document ID | 422 MSG-P10-001 with row number; no row stored |
| TC-E1-060-07 | AC7, BR4 | System | case_number max precision 0.91 | `reviewOnly` for case_number |
| TC-E1-060-08 | AC8 | System | EXTRACT on EXTRACT-S1 v1 running | 409 MSG-P10-003 |
| TC-E1-060-09 | X7 | Security | RW-CASEOWN starts an evaluation | 403 MSG-P4-002 |
| TC-E1-060-10 | AC2, SPEC-015 | System | `Accept: text/csv` | One row per document type with the proposal fields |
| TC-E1-060-11 | BR3 | Unit | 29 and 30 labeled documents | 29 insufficient; 30 proposed |
| TC-E1-060-12 | BR4 | Unit | Confidence sweep with a gap | Lowest threshold meeting 0.95 chosen |

## Guardrails and out of scope

- No business value in code: target precision, minimum sample and tie order are policy values.
- No personal data in logs, tests or prompts; personal label values are hashes and documents are synthetic.
- No read of another module's table; content and fields come through P5.
- The evaluation does not change any `document_field` value or any threshold in force.
- Out of scope: applying the chosen threshold to the review queue (P5, RWB-E1-054); stage 2/3 document
  types (RWB-E2-025); writing the architecture decision record (solution architect).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified with a confidence score; below the threshold goes to review | Program 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | None | TC-E1-060-02, 03, 05, 07, 12 |
| REQ-DCM-006 | Fields extracted for the agreed types | Program 5.5 | FEAT-AGT-04 | 13 Manage documents and correspondence | R-UNI-32 | TC-E1-060-01, 04, 06, 08, 09, 10, 11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3..BR5; SPEC-019 | Where do target precision 0.95, minimum sample 30 and tie order live? TSD `agent_policy` has no columns. | Proposal behaviour. | `agent_policy.config` jsonb (`target_precision` 0.95, `min_sample_documents` 30, `tie_order`), loaded and approved with the policy; TSD T3 update required (F-02). | RESOLVED | SPEC-019 |
| CLAR-002 | AC1, AC4; SPEC-004 | Does the harness call the model once per document or once per field row? | Cost and run count. | Once per document for MODEL and OCR_AND_MODEL; all labeled fields are scored from that one answer. | RESOLVED | SPEC-004 |
| CLAR-003 | BR4, AC2; SPEC-010 | How is "the lowest confidence at which every chosen field reaches 0.95" computed? | Threshold value. | Sweep the observed confidence values descending; at each candidate compute precision for every chosen field using values at or above it; take the lowest candidate meeting 0.95 for all. | RESOLVED | SPEC-010 |
| CLAR-004 | BR3, AC3; SPEC-012 | Does the 30-document minimum count documents or field rows? | Insufficient-sample decision. | Distinct labeled documents per type, not rows. | RESOLVED | SPEC-012 |
| CLAR-005 | BR1; SPEC-002 | How are personal label values stored and compared? | PDPA and matching. | SHA-256 of the normalized value; compare hashes only. | RESOLVED | SPEC-002 |
| CLAR-006 | BR5, X3; SPEC-013 | What is the exact tie order? | Proposal choice. | `OCR_TEMPLATE` before `OCR_AND_MODEL` before `MODEL`. | RESOLVED | SPEC-013 |
| CLAR-007 | AC2; SPEC-015 | What columns does the CSV export carry? | Export contract. | One row per document type: type, approach, mean F1, per-field precision/recall, threshold, review-only fields, sample size, insufficient flag. | RESOLVED | SPEC-015 |
| CLAR-008 | AC1; SPEC-008 | Are score rows written for fields with no value? | Denominator. | Yes, a missing value is a false negative; every labeled field gets a row for every approach. | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the TSD or the build notes.
No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this evaluation story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New extraction evaluation over three approaches; CSV export on the existing evaluation endpoint; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: text/csv representation added to GET /admin/agent-evaluations]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria, 7 exception paths and 3 evaluation states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
