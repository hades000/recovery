# Increment Card — INC-069-epic-1-RWB-E1-033

**RWB-E1-033 — Search across cases**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-069` |
| Title | Search across cases |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-033` |
| RUN_ID | `INC-069-epic-1-RWB-E1-033` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-024, RWB-E1-053, RWB-E1-049 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log**, so that **I find a document in seconds without opening cases one by one, and every look at personal data can be audited**.

**Main flow:**
1. Litigation officer: opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value) and or a free text term.
2. Front end: calls GET /documents with the criteria.
3. DocumentSearchService: validates the criteria: at least one criterion, date order, free text length, field in the type's field list.
4. DocumentSearchService: checks with the masking policy that the role may search a personal field or free text; refuses otherwise.
5. DocumentSearchService: gets the case IDs in the user's scope through CaseDirectory.caseIdsInScope (all cases for scope ALL).
6. DocumentSearchRepository: queries active documents in those cases by type and stored date, joined to document_field for the field condition and to document_text for the free text, newest first, up to SEARCH_MAX_RESULTS.

**Out of scope:**
- Answering a legal or audit document request with an export (FEAT-COM-07, Epic 4) and electronic discovery (Epic 2, REQ-DCM-017).
- Search within one case (RWB-E1-026).
- The access log query screen and its copy to the decision log (RWB-E1-039).
- Search on dates read from the document content, beyond field conditions (Epic 2).

**Business outcome and value hypothesis:** Legal, audit and recovery questions span many cases: every appraisal above a value, every notice from one court, every document naming a guarantor. Today each case folder is opened by hand (FSD P5 A2.6). This story searches the document index, the extracted fields and the OCR text across the cases the user may see, masks personal data the role may not see, and logs each search. It meets REQ-DCM-001 (documents found by their type, date and extracted fields) and REQ-ACA-006 (every read of the document store written to the access log), under control CTL-09 and CTL-11.

**Constraints and guardrails:**
- No business value in code: limits, page size, text length and masking are data.
- No personal data in logs, tests or prompts: the free text term is logged as a hash; names in tests are synthetic.
- No read of another module's tables: scope and case numbers come through CaseDirectory, masking through the P4 interface.
- A result is never returned before its access event is confirmed.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 033 Search across cases v1.md` |
| Requirement IDs | REQ-DCM-001, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.5 and 3.4; Business Requirements Program, sections 5.5 and 5.4 |
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
| RW-LITOFF, litigation officer | Searches by type, date, field and free text in their scope |
| RW-LEGAL, legal counsel; RW-AUDIT, internal audit | Search across all cases (scope ALL); free text allowed under the assumed masking rule |
| RW-COMPLY, compliance and PDPA officer | Searches by type, date and non-personal fields; reads the access log |
| Other roles with Documents R | Search by type, date and non-personal fields in their scope |
| RW-CAPACITY and other roles without Documents R | No search |

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
- **Feature flag:** `rwb.dochub.search`. Off: GET /documents/search returns 404 and the menu item is hidden.
- **Critical path:** No; **depends on:** RWB-E1-024, RWB-E1-053, RWB-E1-049.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: limits, page size, text length and masking are data.
  - No personal data in logs, tests or prompts: the free text term is logged as a hash; names in tests are synthetic.
  - No read of another module's tables: scope and case numbers come through CaseDirectory, masking through the P4 interface.
  - A result is never returned before its access event is confirmed.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 033 Search across cases v1.md` |
| Specification | `output/INC-069-epic-1-RWB-E1-033/specify/spec.md` |
| Compliance validation | `output/INC-069-epic-1-RWB-E1-033/specify/compliance-validation.md` |
| Agent run log | `output/INC-069-epic-1-RWB-E1-033/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-069-epic-1-RWB-E1-033/plan/` (TBC) |
| Implementation evidence | `output/INC-069-epic-1-RWB-E1-033/implement/` (TBC) |
| API / functional test reports | `output/INC-069-epic-1-RWB-E1-033/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-069-epic-1-RWB-E1-033/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-069-epic-1-RWB-E1-033/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 033 Search across cases v1.md` |
| Output run | `output/INC-069-epic-1-RWB-E1-033/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
