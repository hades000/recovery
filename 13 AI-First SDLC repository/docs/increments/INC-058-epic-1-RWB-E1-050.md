# Increment Card — INC-058-epic-1-RWB-E1-050

**RWB-E1-050 — Document classification**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-058` |
| Title | Document classification |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-050` |
| RUN_ID | `INC-058-epic-1-RWB-E1-050` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-049, RWB-E1-025 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **each scanned document classified into one of the six agreed types with a confidence score, and any document below the threshold sent to the review queue with its top two candidate types**, so that **each document is filed under the right type and checklist item without a person typing it**.

**Main flow:**
1. JOB-12 Document intake: runs classifyStep after ocrStep.
2. ClassifyStep: selects intake items with ocr_status DONE, no predicted_type and no document type given (uploads carry their type and are skipped), locking each row.
3. ClassifyStep: takes the text of the first CLASSIFY_MAX_PAGES pages and replaces national ID numbers, account numbers and phone numbers with tokens through the ACE PII masking service.
4. ClassifierClient: sends the masked text and the six type codes with their labels from the type table in force; receives a score per type and the model version.
5. ClassifyStep: ranks the scores; writes predicted_type, classification_confidence, the top two candidates in type_candidates and classifier_version.
6. ClassifyStep: if the top score is at or above CLASSIFY_THRESHOLD and the type is in the table in force, marks the item classified with no review_reason; attach (RWB-E1-032) stores it with review_status NOT_NEEDED.

**Out of scope:**
- The review queue screen and the correction fed back to the labeled set (RWB-E1-054).
- Field extraction and its evaluation (RWB-E1-053, RWB-E1-060).
- Attach to the case (RWB-E1-032).
- Stage 2 and 3 document types (RWB-E2-025).

**Business outcome and value hypothesis:** A scan arrives with no type; today a person reads it and files it by hand. Classification reads the OCR text and names the type with a confidence, so the document can be attached, extracted and counted against the case checklist (FSD P5 A2.8). A document the model is unsure of goes to a person, so no document is filed under the wrong type. It meets REQ-DCM-005 and serves the measure fields extracted without review (FSD P5 A2.8.1).

**Constraints and guardrails:**
- No business value in code: types, thresholds, pages read and the timeout are data.
- No personal data in logs, tests or prompts: text is masked before the model call; prompts and responses are not logged; test documents are synthetic.
- No read of another module's tables.
- The model endpoint is inside the SCB tenant (DL33); no document text leaves the bank.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 050 Document classification v1.md` |
| Requirement IDs | REQ-DCM-005 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
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
| SY-OCR, OCR and extraction pipeline | Runs classification and writes the result (Documents CRU) |
| SY-AGENT, agent platform | Serves the model call through the gateway |
| RW-CASEOWN and roles with Documents R | Read the type and confidence of documents in their scope |
| RW-COE, center of excellence analyst | Runs the evaluation and reads the report |
| RW-RISK, risk and model risk officer | Reviews the evaluation report before production use |

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
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dochub.classify`. Off: classifyStep is skipped and every scanned item goes to review with reason LOW_CONFIDENCE.
- **Critical path:** No; **depends on:** RWB-E1-049, RWB-E1-025.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: types, thresholds, pages read and the timeout are data.
  - No personal data in logs, tests or prompts: text is masked before the model call; prompts and responses are not logged; test documents are synthetic.
  - No read of another module's tables.
  - The model endpoint is inside the SCB tenant (DL33); no document text leaves the bank.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 050 Document classification v1.md` |
| Specification | `output/INC-058-epic-1-RWB-E1-050/specify/spec.md` |
| Compliance validation | `output/INC-058-epic-1-RWB-E1-050/specify/compliance-validation.md` |
| Agent run log | `output/INC-058-epic-1-RWB-E1-050/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-058-epic-1-RWB-E1-050/plan/` (TBC) |
| Implementation evidence | `output/INC-058-epic-1-RWB-E1-050/implement/` (TBC) |
| API / functional test reports | `output/INC-058-epic-1-RWB-E1-050/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-058-epic-1-RWB-E1-050/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-058-epic-1-RWB-E1-050/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 050 Document classification v1.md` |
| Output run | `output/INC-058-epic-1-RWB-E1-050/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
