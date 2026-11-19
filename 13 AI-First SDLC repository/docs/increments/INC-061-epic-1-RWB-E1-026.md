# Increment Card — INC-061-epic-1-RWB-E1-026

**RWB-E1-026 — Attach and search screen**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-061` |
| Title | Attach and search screen |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-026` |
| RUN_ID | `INC-061-epic-1-RWB-E1-026` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-025, RWB-E1-024, RWB-E1-041, RWB-E1-045, RWB-E1-030 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to upload, see and search the documents of a case from the case record view**, so that **the case file is complete and I find a document by type and date without leaving the case**.

**Main flow:**
1. Case owner: opens case RW-2026-000123 on the case record view (SCR-03) and the Documents tab (SCR-30, state Loading then list).
2. Front end: calls GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist and shows the list and the checklist placeholder.
3. Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB before sending and sends an Idempotency-Key.
4. CaseDocumentUploadService: puts the file in the intake container, calls the malware scan (RWB-E1-041) and, if clean, calls DocumentStore.store with source UPLOAD.
5. DocumentStore (RWB-E1-024): writes the decision log entry, the document row and DocumentStored, then copies the file.
6. Front end: on 201 refreshes the list; the new document shows within 5 seconds of submit.

**Out of scope:**
- Required items per case type and the completeness flag (RWB-E1-040).
- Search across cases and free text search (RWB-E1-033).
- Search on extracted fields within a case (RWB-E1-033 builds the field filter).
- OCR, classification and extraction of an uploaded file (RWB-E1-049, RWB-E1-050, RWB-E1-053).
- Upload from the field app (RWB-E2-024) and from partners (Epic 5, DL03).

**Business outcome and value hypothesis:** Case owners hold documents in shared drives and email today, so the case file is never complete in one place (FSD P5 A1.3). This story puts the case documents screen SCR-30 on the case record view: upload with a type, a list of every document on the case, a search by type and date, and a checklist placeholder showing which of the six agreed types are present. It meets REQ-DCM-008 (search by case, type and date from the case record view) and REQ-DCM-001 (every document stored against its case with type, date and source). The measure is fields extracted without review (FSD P5 A2.4.1), which needs documents on the case first.

**Constraints and guardrails:**
- No business value in code: the type list, size limit, file types and page size are data or properties.
- No personal data in logs, tests or prompts. File names in logs are replaced by the document ID.
- No read of another module's tables: the case and the scope come through CaseDirectory and the ACE access check.
- The front end size check does not replace the server check.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 026 Attach and search screen v1.md` |
| Requirement IDs | REQ-DCM-008, REQ-DCM-001 |
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
| Roles with Documents C (RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT) | Upload inside their scope |
| Roles with Documents R (for example RW-TEAMMGR, RW-PHONECOL, RW-AUDIT) | List, search and open documents inside their scope |
| Partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in Epic 1; partners reach the Workbench only through the external gateway (DL03) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry for each upload |

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
- **Feature flag:** `rwb.dochub.casedocs`. Off: the Documents tab is hidden and the endpoints return 404.
- **Critical path:** No; **depends on:** RWB-E1-025, RWB-E1-024, RWB-E1-041, RWB-E1-045, RWB-E1-030.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the type list, size limit, file types and page size are data or properties.
  - No personal data in logs, tests or prompts. File names in logs are replaced by the document ID.
  - No read of another module's tables: the case and the scope come through CaseDirectory and the ACE access check.
  - The front end size check does not replace the server check.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 026 Attach and search screen v1.md` |
| Specification | `output/INC-061-epic-1-RWB-E1-026/specify/spec.md` |
| Compliance validation | `output/INC-061-epic-1-RWB-E1-026/specify/compliance-validation.md` |
| Agent run log | `output/INC-061-epic-1-RWB-E1-026/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-061-epic-1-RWB-E1-026/plan/` (TBC) |
| Implementation evidence | `output/INC-061-epic-1-RWB-E1-026/implement/` (TBC) |
| API / functional test reports | `output/INC-061-epic-1-RWB-E1-026/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-061-epic-1-RWB-E1-026/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-061-epic-1-RWB-E1-026/specify/compliance-validation.md`) |
| Acceptance criteria | 11 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 026 Attach and search screen v1.md` |
| Output run | `output/INC-061-epic-1-RWB-E1-026/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
