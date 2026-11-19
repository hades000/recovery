# Increment Card — INC-044-epic-1-RWB-E1-024

**RWB-E1-024 — Document store and index**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-044` |
| Title | Document store and index |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-024` |
| RUN_ID | `INC-044-epic-1-RWB-E1-024` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept**, so that **I find a document by case ID, type and date, and a legal document cannot be changed after it is stored**.

**Main flow:**
1. Caller: calls DocumentStore.store with the case ID, the document type, the source, the file in the intake container, its SHA-256 hash and any extracted fields.
2. DocumentStoreService: gets the case through CaseDirectory.findById and refuses the call if the case does not exist.
3. DocumentStoreService: reads the type row from the document type table version in force: write_once and retention_class.
4. DocumentStoreService: checks the file type by its content signature and the file size against INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB.
5. DocumentStoreService: looks for an active document on the case with the same type and hash; if one exists, returns it and stops.
6. DocumentStoreService: in one transaction, writes the decision log entry (decision code DOCATT, final call STORED) through DecisionLogWriter, inserts the document row with doc_version 1 and state COPY_PENDING, inserts the document_field rows and writes DocumentStored (EV-16) to the outbox.

**Out of scope:**
- The upload form, the case document list and the search within a case (RWB-E1-026).
- Classification, field extraction and automatic attach from the OCR intake (RWB-E1-050, RWB-E1-053, RWB-E1-032).
- Confirming or correcting an extracted field with PATCH /documents/{documentId}/fields/{fieldId} (RWB-E1-054).
- Retention periods, the retention job and the virus scan (RWB-E1-041).
- Container creation, backup and restore tests (RWB-TE-012; REQ-DCM-015).
- Custody of originals (Epic 2, SCR-32) and electronic discovery (Epic 2, REQ-DCM-017).

**Business outcome and value hypothesis:** Recovery documents are held today in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit (FSD P5 A1.3). This story builds the store and the index that every other document story writes to: one document record in the Workbench document hub per file, the file in blob storage, legal types write-once (DT06, ADR-007, control CTL-12). It meets REQ-DCM-001, REQ-DCM-002, REQ-DCM-003 and REQ-DCM-008. The module measure is fields extracted without review (FSD P5 A2.1.1), which can only be counted once every document is indexed against its case.

**Constraints and guardrails:**
- No business value in code: file types, size limit, write-once flag, retention class and container names are data rows or properties.
- No personal data in logs, tests or prompts. Test files are synthetic; extracted field values in logs are replaced by the field name.
- No read of another module's tables: the case is read through CaseDirectory, the decision log is written through DecisionLogWriter.
- The service never overwrites a blob; every version is a new blob path.
- The PII access log entry for each read is written by the ACE common module, never by this package.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 024 Document store and index v1.md` |
| Requirement IDs | REQ-DCM-001, REQ-DCM-002, REQ-DCM-003, REQ-DCM-008 |
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
| SY-OCR, OCR and extraction pipeline | Stores documents through DocumentStore (Documents C) |
| RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and the other roles with Documents C | Store through the upload in RWB-E1-026 |
| Roles with Documents U (for example RW-CASEOWN, RW-LITOFF, RW-LEGAL, RW-COMPLY) | Add a new version |
| Roles with Documents R (for example RW-TEAMMGR, RW-AUDIT, RW-PHONECOL) | Read metadata and content inside their scope |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Nobody | Deletes or changes a write-once document |

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
- **Feature flag:** `rwb.dochub.store`. Off: the endpoints return 404 and DocumentStore.store refuses with a feature-off error.
- **Critical path:** No; **depends on:** RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: file types, size limit, write-once flag, retention class and container names are data rows or properties.
  - No personal data in logs, tests or prompts. Test files are synthetic; extracted field values in logs are replaced by the field name.
  - No read of another module's tables: the case is read through CaseDirectory, the decision log is written through DecisionLogWriter.
  - The service never overwrites a blob; every version is a new blob path.
  - The PII access log entry for each read is written by the ACE common module, never by this package.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 024 Document store and index v1.md` |
| Specification | `output/INC-044-epic-1-RWB-E1-024/specify/spec.md` |
| Compliance validation | `output/INC-044-epic-1-RWB-E1-024/specify/compliance-validation.md` |
| Agent run log | `output/INC-044-epic-1-RWB-E1-024/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-044-epic-1-RWB-E1-024/plan/` (TBC) |
| Implementation evidence | `output/INC-044-epic-1-RWB-E1-024/implement/` (TBC) |
| API / functional test reports | `output/INC-044-epic-1-RWB-E1-024/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-044-epic-1-RWB-E1-024/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-044-epic-1-RWB-E1-024/specify/compliance-validation.md`) |
| Acceptance criteria | 12 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 024 Document store and index v1.md` |
| Output run | `output/INC-044-epic-1-RWB-E1-024/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
