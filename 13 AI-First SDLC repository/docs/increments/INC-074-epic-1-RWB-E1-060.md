# Increment Card — INC-074-epic-1-RWB-E1-060

**RWB-E1-060 — Extraction evaluation [E1c]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-074` |
| Title | Extraction evaluation [E1c] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-060` |
| RUN_ID | `INC-074-epic-1-RWB-E1-060` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | Spike |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-053, RWB-E1-058 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Spike. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **field extraction for the six document types scored against the labeled sample for three approaches (OCR template, model, and OCR checked by the model)**, so that **the extraction approach and the confidence threshold for each document type are chosen on measured precision and recall**.

**Main flow:**
1. RW-COE: loads sample "EXTRACT-S1" through POST /admin/agent-samples with one row per document and field.
2. RW-COE: starts the evaluation with approaches OCR_TEMPLATE, MODEL and OCR_AND_MODEL through POST /admin/agent-evaluations.
3. System: for OCR_TEMPLATE, reads the stored document_field values through the P5 interface; makes no model call.
4. System: for MODEL, calls agent "EXTRACT" in shadow on the document content and reads the fields from its answer.
5. System: for OCR_AND_MODEL, passes the OCR fields with the content to agent "EXTRACT" and takes its checked values.
6. System: compares each value with the label and stores true positives, false positives, false negatives, precision and recall per field and approach.

**Out of scope:**
- Applying the chosen threshold to the review queue (P5, RWB-E1-054).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- Writing the architecture decision record itself (solution architect, outside the code).

**Business outcome and value hypothesis:** Fields read wrongly from a court notice or a title deed send a case down the wrong step, and fields sent to review without need take officer time. This story measures the three approaches on the same reviewed documents, field by field, and proposes for each document type the approach and the confidence threshold below which a field goes to the review queue. It serves REQ-DCM-006 (fields extracted for the agreed types) and REQ-DCM-005 (confidence score and review queue below the threshold).

**Constraints and guardrails:**
- No business value in code: target precision, minimum sample and tie order are policy values.
- No personal data in logs, tests or prompts; personal label values are stored as hashes and documents in tests are synthetic.
- No read of another module's tables; document content and fields come through the P5 interface.
- The evaluation does not change any document_field value or any threshold in force.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 060 Extraction evaluation E1c v1.md` |
| Requirement IDs | REQ-DCM-005, REQ-DCM-006 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.5 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| RW-COE | Loads the sample, starts the evaluation, reads and exports results (Rules and parameters CRUD) |
| RW-RISK | Reads results (Rules and parameters R) |
| SY-AGENT | Reads document content and fields (Documents R) |
| SY-OCR | Produced the OCR fields earlier; not called here |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Optional | Throwaway spike; not merged. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-053, RWB-E1-058.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: target precision, minimum sample and tie order are policy values.
  - No personal data in logs, tests or prompts; personal label values are stored as hashes and documents in tests are synthetic.
  - No read of another module's tables; document content and fields come through the P5 interface.
  - The evaluation does not change any document_field value or any threshold in force.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 060 Extraction evaluation E1c v1.md` |
| Specification | `output/INC-074-epic-1-RWB-E1-060/specify/spec.md` |
| Compliance validation | `output/INC-074-epic-1-RWB-E1-060/specify/compliance-validation.md` |
| Agent run log | `output/INC-074-epic-1-RWB-E1-060/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-074-epic-1-RWB-E1-060/plan/` (TBC) |
| Implementation evidence | `output/INC-074-epic-1-RWB-E1-060/implement/` (TBC) |
| API / functional test reports | `output/INC-074-epic-1-RWB-E1-060/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-074-epic-1-RWB-E1-060/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-074-epic-1-RWB-E1-060/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 060 Extraction evaluation E1c v1.md` |
| Output run | `output/INC-074-epic-1-RWB-E1-060/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
