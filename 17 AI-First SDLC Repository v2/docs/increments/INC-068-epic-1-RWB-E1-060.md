# Increment Card — INC-068-epic-1-RWB-E1-060

**RWB-E1-060 — Extraction evaluation [E1c]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-068` |
| Title | Extraction evaluation [E1c] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-060` |
| RUN_ID | `INC-068-epic-1-RWB-E1-060` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | Spike |
| Priority | Must |
| Build order | 68 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-053, RWB-E1-058 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Spike. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **field extraction for the six document types scored against the labeled sample for three approaches (OCR template, model, and OCR checked by the model)**, so that **the extraction approach and the confidence threshold for each document type are chosen on measured precision and recall**.

**Business outcome:** Fields read wrongly from a court notice or a title deed send a case down the wrong step, and fields sent to review without need take officer time. This story measures the three approaches on the same reviewed documents, field by field, and proposes for each document type the approach and the confidence threshold below which a field goes to the review queue. It serves REQ-DCM-006 (fields extracted for the agreed types) and REQ-DCM-005 (confidence score and review queue below the threshold).

**Main flow:**
1. RW-COE: loads sample "EXTRACT-S1" through POST /admin/agent-samples with one row per document and field.
2. RW-COE: starts the evaluation with approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL through POST /admin/agent-evaluations.
3. System: for OCR_TEMPLATE, reads the stored document_field values through the P5 interface; makes no model call.
4. System: for MODEL, calls agent "EXTRACT" in shadow on the document content and reads the fields from its answer.
5. System: for OCR_AND_MODEL, passes the OCR fields with the content to agent "EXTRACT" and takes its checked values.
6. System: compares each value with the label and stores true positives, false positives, false negatives, precision and recall per field and approach.

**Acceptance criteria:**
- AC1: Scores per field
- AC2: Decision recorded
- AC3: A type with too few labels
- AC4: A model failure counts against the model approaches
- AC5: Equal F1
- AC6: A sample row for a document that does not exist
- AC7: A field that never reaches the target
- AC8: The same evaluation twice

**Out of scope:**
- Applying the chosen threshold to the review queue (P5, RWB-E1-054).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- Writing the architecture decision record itself (solution architect, outside the code).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-060-extraction-evaluation-e1c-v1.md` |
| Requirement IDs | REQ-DCM-005, REQ-DCM-006 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.5 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Loads the sample, starts the evaluation, reads and exports results (Rules and parameters CRUD) |
| RW-RISK | Reads results (Rules and parameters R) |
| SY-AGENT | Reads document content and fields (Documents R) |
| SY-OCR | Produced the OCR fields earlier; not called here |

## Contract extract

**POST /api/recovery/v1/admin/agent-samples** (new, RWB-E1-058): multipart file (CSV: subject_type DOCUMENT, subject_id, label_key = field name, expected_value), agent "EXTRACT", sampleCode; 201 AgentSample; errors 401, 403, 422 (MSG-P10-001), 503; Rules and parameters C; each load is a new sample version. **POST /api/recovery/v1/admin/agent-evaluations** (new): AgentEvaluationRequest with agent "EXTRACT", sampleCode "EXTRACT-S1", sampleVersion 1, approaches ["OCR_TEMPLATE", "MODEL", "OCR_AND_MODEL"]; 202 AgentEvaluationRun; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-002), 503; Rules and parameters C; one RUNNING run per agent and sample version. **GET /api/recovery/v1/admin/agent-evaluations** (new): query agent, from, to; 200 AgentEvaluationRun[] with score rows and the proposal per document type; errors 401, 403, 503; Rules and parameters R. Export: Accept text/csv returns the…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: target precision, minimum sample and tie order are policy values. - No personal data in logs, tests or prompts; personal label values are stored as hashes and documents in tests are synthetic. - No read of another module's tables; document content and fields come through the P5 interface. - The evaluation does not change any document_field value or any threshold in force.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-060-extraction-evaluation-e1c-v1.md` |
| Specification | `output/INC-068-epic-1-RWB-E1-060/specify/spec.md` |
| Compliance validation | `output/INC-068-epic-1-RWB-E1-060/specify/compliance-validation.md` |
| Agent run log | `output/INC-068-epic-1-RWB-E1-060/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-068-epic-1-RWB-E1-060/plan/` |
| Implementation evidence | `output/INC-068-epic-1-RWB-E1-060/implement/` |
| API / functional test reports | `output/INC-068-epic-1-RWB-E1-060/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-068-epic-1-RWB-E1-060/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-060-extraction-evaluation-e1c-v1.md` |
| Output run | `output/INC-068-epic-1-RWB-E1-060/` |

