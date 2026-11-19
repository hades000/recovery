# Increment Card — INC-071-epic-1-RWB-E1-040

**RWB-E1-040 — Document checklist per case type as reference data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-071` |
| Title | Document checklist per case type as reference data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-040` |
| RUN_ID | `INC-071-epic-1-RWB-E1-040` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-024, RWB-E1-043, RWB-E1-025, RWB-E1-026 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read**, so that **a missing document shows on the case without a person checking a list**.

**Main flow:**
1. Reference data administrator: loads the checklist file with POST /api/recovery/v1/admin/reference-loads, table DOCUMENT_CHECKLIST; the owner approves it.
2. ChecklistLoader: validates every row: stage in LOV-STAGE, route in LOV-ROUTE or empty, document type in the type table in force, no duplicate row; refuses the load whole on any error.
3. ChecklistEvaluator: on DocumentStored (EV-16), on CaseStateChanged (EV-05) and when a checklist version takes effect, takes the case's stage and route through CaseDirectory.
4. ChecklistEvaluator: picks the rows of the version in force for that stage, using the rows for the route where they exist and the rows with no route otherwise.
5. ChecklistEvaluator: counts the active documents of each required type on the case and writes case_document_check: checklist version, required count, present count, missing types and complete.
6. Litigation officer: opens the Documents tab (SCR-30); GET /cases/{caseId}/document-checklist returns each required item marked present or missing.

**Out of scope:**
- The litigation pack check against the defect list and the block at filing (FEAT-LIT-05, Epic 5; CTL-19).
- The guarantee claim checklist (FEAT-GUA-01, Epic 4).
- Retrieval requests for missing documents (R-LIT-17, Epic 5).
- The review queue screen that shows the case checklist (RWB-E1-054).

**Business outcome and value hypothesis:** Litigation packs and guarantee claims fail when a required document is missing, and today the gap is found by a person reading a paper list, often at filing (CTL-19, R-LIT-17). This story holds the checklist per case stage and route as data and keeps a completeness flag per case, recomputed whenever a document is stored or the case changes stage. It meets REQ-DCM-011 and gives the pack checks of Epic 4 and Epic 5 (R-LIT-16, R-GUA-07) one checklist source. The measure is fields extracted without review (FSD P5 A2.16.1).

**Constraints and guardrails:**
- No business value in code: stages, routes and required types are rows in document_checklist_item.
- No personal data in logs, tests or prompts: the flag holds type codes and counts only.
- No read of another module's tables: stage, route and owner come through CaseDirectory; P3 reads the flag through DocumentChecklistService.
- The evaluator never blocks a case move; it reports only.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 040 Document checklist per case type as reference data v1.md` |
| Requirement IDs | REQ-DCM-011 |
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
| RW-REFADM, reference data administrator | Loads the checklist (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the legal counsel as co-owner of the checklist (DL01) |
| RW-LITOFF, RW-CASEOWN and roles with Documents R | Read the checklist and the flag for cases in their scope |
| RW-LEGAL, legal counsel | Agrees the items per stage (DL19) |
| SY-CASEWF | Publishes CaseStateChanged that triggers the recompute |

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
- **Feature flag:** `rwb.dochub.checklist`. Off: the endpoint returns the RWB-E1-026 placeholder and no flag is written.
- **Critical path:** No; **depends on:** RWB-E1-024, RWB-E1-043, RWB-E1-025, RWB-E1-026.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: stages, routes and required types are rows in document_checklist_item.
  - No personal data in logs, tests or prompts: the flag holds type codes and counts only.
  - No read of another module's tables: stage, route and owner come through CaseDirectory; P3 reads the flag through DocumentChecklistService.
  - The evaluator never blocks a case move; it reports only.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 040 Document checklist per case type as reference data v1.md` |
| Specification | `output/INC-071-epic-1-RWB-E1-040/specify/spec.md` |
| Compliance validation | `output/INC-071-epic-1-RWB-E1-040/specify/compliance-validation.md` |
| Agent run log | `output/INC-071-epic-1-RWB-E1-040/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-071-epic-1-RWB-E1-040/plan/` (TBC) |
| Implementation evidence | `output/INC-071-epic-1-RWB-E1-040/implement/` (TBC) |
| API / functional test reports | `output/INC-071-epic-1-RWB-E1-040/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-071-epic-1-RWB-E1-040/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-071-epic-1-RWB-E1-040/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 040 Document checklist per case type as reference data v1.md` |
| Output run | `output/INC-071-epic-1-RWB-E1-040/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
