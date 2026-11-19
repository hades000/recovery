# Increment Card — INC-076-epic-1-RWB-E1-054

**RWB-E1-054 — Review queue for low-confidence documents**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-076` |
| Title | Review queue for low-confidence documents |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-054` |
| RUN_ID | `INC-076-epic-1-RWB-E1-054` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-049, RWB-E1-035, RWB-E1-050, RWB-E1-053, RWB-E1-032 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **litigation officer**, I want **a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set**, so that **no document is attached wrongly and the models improve**.

**Main flow:**
1. Litigation officer: opens SCR-31 Document review queue.
2. System: lists, oldest first, the intake items with a review_reason and no case that belong to the officer's review team, the intake items whose candidate cases are in the officer's scope, and the stored documents with review_status PENDING on cases in scope; each row shows the reason, the proposed type, the two candidates, confidence and age.
3. Litigation officer: opens an item; the system shows the file, the OCR text, the type with its candidates, the candidate cases and the fields, with fields in REVIEW marked.
4. Litigation officer: keeps the type or chooses another type from the list in force; a new type re-runs extraction for that type and shows the new fields.
5. Litigation officer: chooses the case from the candidates, or enters a case number that the system looks up through CaseDirectory.
6. Litigation officer: confirms each marked field with Confirm, or enters the value with Correct; the system checks it against the field data type and range.

**Out of scope:**
- Setting the review reasons: OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching (RWB-E1-032).
- The model evaluations that read the labeled examples (RWB-E1-060).
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040).

**Business outcome and value hypothesis:** A wrong type or a wrong hearing date on a court notice puts the wrong date on the case and the litigation timers run from it. This story shows in one queue every intake item the pipeline could not type, read or match, and every stored document with a field below its threshold; one officer confirms or corrects the type, the case and the fields on one screen, and each correction is kept as a labeled example for the model evaluations. It meets REQ-DCM-005 and moves the measure "fields extracted without review", because each correction improves the next model version.

**Constraints and guardrails:**
- No business value in code: the review team, date limits, page size and the type list come from document_hub_parameter and the type table.
- No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; the labeled examples stay inside the bank.
- No read of another module's tables: cases come through CaseDirectory; scope comes from the ACE common access check.
- Attach goes only through DocumentStore, so a document never exists without its decision log entry.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 054 Review queue for low confidence documents v1.md` |
| Requirement IDs | REQ-DCM-005 |
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
| RW-LITOFF, litigation officer | Lists, reads, corrects, attaches and discards review items in scope (Documents CRU) |
| RW-CASEOWN, case owner | Lists, reads, corrects and attaches review items of own cases (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the queue for the team (Documents R); cannot correct or attach |
| SY-OCR, OCR and extraction pipeline | Re-runs extraction on a type change (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-COE, center of excellence analyst | Reads the labeled examples through the model evaluations (Documents R) |

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
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-049, RWB-E1-035, RWB-E1-050, RWB-E1-053, RWB-E1-032.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the review team, date limits, page size and the type list come from document_hub_parameter and the type table.
  - No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; the labeled examples stay inside the bank.
  - No read of another module's tables: cases come through CaseDirectory; scope comes from the ACE common access check.
  - Attach goes only through DocumentStore, so a document never exists without its decision log entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 054 Review queue for low confidence documents v1.md` |
| Specification | `output/INC-076-epic-1-RWB-E1-054/specify/spec.md` |
| Compliance validation | `output/INC-076-epic-1-RWB-E1-054/specify/compliance-validation.md` |
| Agent run log | `output/INC-076-epic-1-RWB-E1-054/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-076-epic-1-RWB-E1-054/plan/` (TBC) |
| Implementation evidence | `output/INC-076-epic-1-RWB-E1-054/implement/` (TBC) |
| API / functional test reports | `output/INC-076-epic-1-RWB-E1-054/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-076-epic-1-RWB-E1-054/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-076-epic-1-RWB-E1-054/specify/compliance-validation.md`) |
| Acceptance criteria | 17 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 054 Review queue for low confidence documents v1.md` |
| Output run | `output/INC-076-epic-1-RWB-E1-054/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
