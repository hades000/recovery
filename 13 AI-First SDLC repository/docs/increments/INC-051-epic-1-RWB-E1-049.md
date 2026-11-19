# Increment Card — INC-051-epic-1-RWB-E1-049

**RWB-E1-049 — OCR pipeline on the Workbench document hub**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-051` |
| Title | OCR pipeline on the Workbench document hub |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-049` |
| RUN_ID | `INC-051-epic-1-RWB-E1-049` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-TE-012, RWB-E1-024, RWB-E1-045 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document**, so that **classification and extraction can start and an unreadable page is sent back for rescan the same day**.

**Main flow:**
1. JOB-12 Document intake: starts every 15 minutes in business hours and runs the OCR step after the intake and scan steps.
2. DocumentStoredListener: for each DocumentStored event with source UPLOAD, creates an intake item with the case ID, the document ID and scan_result CLEAN (the upload was scanned before storage).
3. OcrStep: selects intake items with scan_result CLEAN and ocr_status PENDING, oldest first, locking each row so that no two workers take the same item; runs up to OCR_WORKERS items in parallel.
4. OcrClient: sends the file to the OCR service with the languages Thai and English and receives, per page, the lines, words, positions, language and word confidence.
5. OcrStep: computes the page quality as the mean word confidence of the page; stores the full output as JSON at ocr/{intakeId}.json in the standard container and sets ocr_ref.
6. OcrStep: writes one document_text row per page with the page text and quality, with the document ID where the item is already attached.

**Out of scope:**
- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).

**Business outcome and value hypothesis:** Scanned documents arrive as images; nothing in them can be classified, extracted or searched until the text is read (FSD P5 A2.7). This story builds the OCR step of the document intake: one intake record per file, the text and layout of every page, a quality check per page and a rescan request when a page cannot be read. It meets REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first) and REQ-DCM-009 (every path ends in the same intake). The measure is fields extracted without review (FSD P5 A2.7.1).

**Constraints and guardrails:**
- No business value in code: threshold, workers, timeout and attempts are parameters.
- No personal data in logs, tests or prompts. OCR text is never written to application logs; logs carry the intake ID and counts only. Test documents are synthetic.
- No read of another module's tables: the case owner comes through CaseDirectory.
- OCR text is held only in document_text and the standard container; it is not sent to any service other than the OCR service and the classifier.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 049 OCR pipeline on the Workbench document hub v1.md` |
| Requirement IDs | REQ-DCM-006, REQ-DCM-009 |
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
| SY-OCR, OCR and extraction pipeline | Reads intake files, writes OCR output and text rows (Documents CRU) |
| RW-CASEOWN | Receives the rescan notice for their case |
| RW-PLATADM, platform administrator | Sees the job counts and alerts in the job monitor; reruns JOB-12 |
| Roles with Documents R | Read the OCR text of documents in their scope through RWB-E1-033 |

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
- **Feature flag:** `rwb.dochub.ocr`. Off: ocrStep is skipped and items stay PENDING.
- **Critical path:** No; **depends on:** RWB-TE-012, RWB-E1-024, RWB-E1-045.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: threshold, workers, timeout and attempts are parameters.
  - No personal data in logs, tests or prompts. OCR text is never written to application logs; logs carry the intake ID and counts only. Test documents are synthetic.
  - No read of another module's tables: the case owner comes through CaseDirectory.
  - OCR text is held only in document_text and the standard container; it is not sent to any service other than the OCR service and the classifier.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 049 OCR pipeline on the Workbench document hub v1.md` |
| Specification | `output/INC-051-epic-1-RWB-E1-049/specify/spec.md` |
| Compliance validation | `output/INC-051-epic-1-RWB-E1-049/specify/compliance-validation.md` |
| Agent run log | `output/INC-051-epic-1-RWB-E1-049/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-051-epic-1-RWB-E1-049/plan/` (TBC) |
| Implementation evidence | `output/INC-051-epic-1-RWB-E1-049/implement/` (TBC) |
| API / functional test reports | `output/INC-051-epic-1-RWB-E1-049/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-051-epic-1-RWB-E1-049/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-051-epic-1-RWB-E1-049/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 049 OCR pipeline on the Workbench document hub v1.md` |
| Output run | `output/INC-051-epic-1-RWB-E1-049/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
