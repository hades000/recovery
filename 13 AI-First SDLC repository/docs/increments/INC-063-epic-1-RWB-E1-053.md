# Increment Card — INC-063-epic-1-RWB-E1-053

**RWB-E1-053 — Field extraction for the six types into the index**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-063` |
| Title | Field extraction for the six types into the index |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-053` |
| RUN_ID | `INC-063-epic-1-RWB-E1-053` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-049, RWB-E1-050, RWB-E1-025 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **case owner**, I want **the key fields of each of the six document types extracted and written to the document index with a confidence per field**, so that **documents are searchable by their content**.

**Main flow:**
1. JOB-12 Document intake: runs extractStep after classifyStep and before matchStep.
2. ExtractStep: selects intake items with ocr_status DONE and extract_status PENDING that are classified with no review_reason, or that carry a document ID with a given type (uploads), locking each row.
3. ExtractStep: reads the field definitions of the type from the version of DocumentTypeCatalog in force, the threshold and the attempts.
4. ExtractStep: reads the page text and layout through OcrOutputReader.
5. FieldExtractor: the extractor named by extraction_method returns a raw value and a confidence per field, with the extractor version.
6. ValueNormalizer: converts each value to its data type: Thai and English dates to ISO dates, Buddhist Era years less BE_YEAR_OFFSET, Thai digits to Arabic digits, amounts to numeric(18,2) baht.

**Out of scope:**
- The review queue screen and correction of fields (RWB-E1-054).
- Matching the item to its case and storing the document (RWB-E1-032, RWB-E1-024).
- Search by extracted field (RWB-E1-033).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
- The choice of extraction approach per type (RWB-E1-060).

**Business outcome and value hypothesis:** Court dates, case numbers, appraisal values and title numbers are typed by hand from paper today, and a document is found only by the person who filed it. This story reads the agreed fields of each classified intake item and each uploaded document into the index with a confidence score, so the case owner and the litigation officer find a document by its content, the attach step finds the case from the extracted case number, and the low-confidence values go to a person. It meets REQ-DCM-006 and REQ-DCM-001 and feeds the module measure "fields extracted without review", which is to rise each month.

**Constraints and guardrails:**
- No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and document_hub_parameter.
- No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; text sent to the model is masked as in RWB-E1-050.
- No read of another module's tables: the model is reached through the P10 gateway.
- Extraction never writes to a stored file or a container.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 053 Field extraction for the six types into the index v1.md` |
| Requirement IDs | REQ-DCM-006, REQ-DCM-001 |
| BRD section | Business Requirements Epic 1, section 3.5 |
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
| SY-OCR, OCR and extraction pipeline | Runs extractStep; writes extracted fields and document_field rows (Documents CRU) |
| RW-CASEOWN, case owner | Reads the document and its fields in scope (Documents R) |
| RW-LITOFF, litigation officer | Reads the document and its fields in scope (Documents R) |
| RW-COE, center of excellence analyst | Reads the evaluation report; prepares the review-only proposal |
| RW-REFADM, reference data administrator | Loads a new DOCTYPE version (Reference data CRUD) |
| Business lead with Legal | Approves the type and field list (DL19) |

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
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-049, RWB-E1-050, RWB-E1-025.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: fields, methods, patterns, thresholds, pass marks, attempts and the Buddhist Era offset come from the type table and document_hub_parameter.
  - No personal data in logs, tests or prompts: logs and the job record hold item IDs, field names and confidence only; text sent to the model is masked as in RWB-E1-050.
  - No read of another module's tables: the model is reached through the P10 gateway.
  - Extraction never writes to a stored file or a container.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 053 Field extraction for the six types into the index v1.md` |
| Specification | `output/INC-063-epic-1-RWB-E1-053/specify/spec.md` |
| Compliance validation | `output/INC-063-epic-1-RWB-E1-053/specify/compliance-validation.md` |
| Agent run log | `output/INC-063-epic-1-RWB-E1-053/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-063-epic-1-RWB-E1-053/plan/` (TBC) |
| Implementation evidence | `output/INC-063-epic-1-RWB-E1-053/implement/` (TBC) |
| API / functional test reports | `output/INC-063-epic-1-RWB-E1-053/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-063-epic-1-RWB-E1-053/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-063-epic-1-RWB-E1-053/specify/compliance-validation.md`) |
| Acceptance criteria | 13 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 053 Field extraction for the six types into the index v1.md` |
| Output run | `output/INC-063-epic-1-RWB-E1-053/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
