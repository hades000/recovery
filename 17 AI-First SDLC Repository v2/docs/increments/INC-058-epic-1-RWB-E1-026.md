# Increment Card — INC-058-epic-1-RWB-E1-026

**RWB-E1-026 — Attach and search screen**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-058` |
| Title | Attach and search screen |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-026` |
| RUN_ID | `INC-058-epic-1-RWB-E1-026` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 58 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-025, RWB-E1-024, RWB-E1-041, RWB-E1-045, RWB-E1-030 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to upload, see and search the documents of a case from the case record view**, so that **the case file is complete and I find a document by type and date without leaving the case**.

**Business outcome:** Case owners hold documents in shared drives and email today, so the case file is never complete in one place (FSD P5 A1.3). This story puts the case documents screen SCR-30 on the case record view: upload with a type, a list of every document on the case, a search by type and date, and a checklist placeholder showing which of the six agreed types are present. It meets REQ-DCM-008 (search by case, type and date from the case record view) and REQ-DCM-001 (every document stored against its case with type, date and source). The measure is fields extracted without review (FSD P5 A2.4.1), which needs documents on the case first.

**Main flow:**
1. Case owner: opens case RW-2026-000123 on the case record view (SCR-03) and the Documents tab (SCR-30, state Loading then list).
2. Front end: calls GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist and shows the list and the checklist placeholder.
3. Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB before sending and sends an Idempotency-Key.
4. CaseDocumentUploadService: puts the file in the intake container, calls the malware scan (RWB-E1-041) and, if clean, calls DocumentStore.store with source UPLOAD.
5. DocumentStore (RWB-E1-024): writes the decision log entry, the document row and DocumentStored, then copies the file.
6. Front end: on 201 refreshes the list; the new document shows within 5 seconds of submit.

**Acceptance criteria:**
- AC1: Upload
- AC2: Search
- AC3: Checklist placeholder
- AC4: Upload without a type
- AC5: Upload that fails the malware scan
- AC6: File type not allowed
- AC7: The same file uploaded again
- AC8: Double submit
- AC9: Date range in the wrong order
- AC10: No document matches
- AC11: Case outside the scope

**Out of scope:**
- Required items per case type and the completeness flag (RWB-E1-040).
- Search across cases and free text search (RWB-E1-033).
- Search on extracted fields within a case (RWB-E1-033 builds the field filter).
- OCR, classification and extraction of an uploaded file (RWB-E1-049, RWB-E1-050, RWB-E1-053).
- Upload from the field app (RWB-E2-024) and from partners (Epic 5, DL03).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-026-attach-and-search-screen-v1.md` |
| Requirement IDs | REQ-DCM-008, REQ-DCM-001 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
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
| Roles with Documents C (RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT) | Upload inside their scope |
| Roles with Documents R (for example RW-TEAMMGR, RW-PHONECOL, RW-AUDIT) | List, search and open documents inside their scope |
| Partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in Epic 1; partners reach the Workbench only through the external gateway (DL03) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry for each upload |

## Contract extract

**POST /cases/{caseId}/documents** | Item | Value | |---|---| | Request | multipart/form-data: file (binary), type (doc_type_code, required), source (must be "UPLOAD" for a user call; other values refused with 422) | | Response | 201 Document for a new document; 200 Document with messageCode MSG-P5-024 for a duplicate | | Errors | 401; 403 no Documents C (MSG-P4-002) or case out of scope (MSG-P4-003); 404 case not found; 413 above INTAKE_MAX_FILE_MB (MSG-P5-017); 415 file type (MSG-P5-001); 422 type missing (MSG-GEN-001), type not in the table (MSG-P5-006) or malware found (MSG-P5-016); 503 decision log write failed (MSG-P7-003) | | Authorization | Documents, right C, scope applied | | Idempotency | Idempotency-Key header, kept 24 hours per user; a repeat returns the first response | **GET /cases/{caseId}/documents** | Item | Value | |---|---| | Request | Query type, page, size (api.yam…

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

- No business value in code: the type list, size limit, file types and page size are data or properties. - No personal data in logs, tests or prompts. File names in logs are replaced by the document ID. - No read of another module's tables: the case and the scope come through CaseDirectory and the ACE access check. - The front end size check does not replace the server check.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-026-attach-and-search-screen-v1.md` |
| Specification | `output/INC-058-epic-1-RWB-E1-026/specify/spec.md` |
| Compliance validation | `output/INC-058-epic-1-RWB-E1-026/specify/compliance-validation.md` |
| Agent run log | `output/INC-058-epic-1-RWB-E1-026/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-058-epic-1-RWB-E1-026/plan/` |
| Implementation evidence | `output/INC-058-epic-1-RWB-E1-026/implement/` |
| API / functional test reports | `output/INC-058-epic-1-RWB-E1-026/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-058-epic-1-RWB-E1-026/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-026-attach-and-search-screen-v1.md` |
| Output run | `output/INC-058-epic-1-RWB-E1-026/` |

