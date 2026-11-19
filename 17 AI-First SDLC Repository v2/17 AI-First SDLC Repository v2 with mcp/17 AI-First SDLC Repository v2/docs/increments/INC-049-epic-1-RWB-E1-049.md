# Increment Card — INC-049-epic-1-RWB-E1-049

**RWB-E1-049 — OCR pipeline on the Workbench document hub**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-049` |
| Title | OCR pipeline on the Workbench document hub |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-049` |
| RUN_ID | `INC-049-epic-1-RWB-E1-049` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 49 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-012, RWB-E1-024, RWB-E1-045 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document**, so that **classification and extraction can start and an unreadable page is sent back for rescan the same day**.

**Business outcome:** Scanned documents arrive as images; nothing in them can be classified, extracted or searched until the text is read (FSD P5 A2.7). This story builds the OCR step of the document intake: one intake record per file, the text and layout of every page, a quality check per page and a rescan request when a page cannot be read. It meets REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first) and REQ-DCM-009 (every path ends in the same intake). The measure is fields extracted without review (FSD P5 A2.7.1).

**Main flow:**
1. JOB-12 Document intake: starts every 15 minutes in business hours and runs the OCR step after the intake and scan steps.
2. DocumentStoredListener: for each DocumentStored event with source UPLOAD, creates an intake item with the case ID, the document ID and scan_result CLEAN (the upload was scanned before storage).
3. OcrStep: selects intake items with scan_result CLEAN and ocr_status PENDING, oldest first, locking each row so that no two workers take the same item; runs up to OCR_WORKERS items in parallel.
4. OcrClient: sends the file to the OCR service with the languages Thai and English and receives, per page, the lines, words, positions, language and word confidence.
5. OcrStep: computes the page quality as the mean word confidence of the page; stores the full output as JSON at ocr/{intakeId}.json in the standard container and sets ocr_ref.
6. OcrStep: writes one document_text row per page with the page text and quality, with the document ID where the item is already attached.

**Acceptance criteria:**
- AC1: Sample processed
- AC2: Throughput
- AC3: Unreadable page on a known case
- AC4: Unreadable page with no case yet
- AC5: Quality at the threshold
- AC6: OCR service unavailable
- AC7: File that cannot be read
- AC8: Repeat run
- AC9: Two workers on one item

**Out of scope:**
- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-049-ocr-pipeline-on-the-workbench-document-hub-v1.md` |
| Requirement IDs | REQ-DCM-006, REQ-DCM-009 |
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
| SY-OCR, OCR and extraction pipeline | Reads intake files, writes OCR output and text rows (Documents CRU) |
| RW-CASEOWN | Receives the rescan notice for their case |
| RW-PLATADM, platform administrator | Sees the job counts and alerts in the job monitor; reruns JOB-12 |
| Roles with Documents R | Read the OCR text of documents in their scope through RWB-E1-033 |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz schedule of JOB-12 Document intake | | Job name | JOB-12 Document intake; this story adds the step ocrStep | | Schedule | Every 15 minutes in business hours, Asia/Bangkok | | Input | Intake items with scan_result CLEAN and ocr_status PENDING | | Output | OCR JSON per item in the standard container; document_text rows; ocr_status per item; run counts on the job record | | Events consumed | DocumentStored (EV-16), source UPLOAD, creates the intake item | | Events published | None | | Idempotency key | Intake item ID; an item not PENDING is not read | | Restart behavior | A stopped run leaves unfinished items PENDING; the next run or a rerun from the job monitor (POST /api/recovery/v1/admin/jobs/{jobId}/rerun) picks them up | **Published interface (P5, used by RWB-E1-050, RWB-E1-053 and RWB-E1-033)** ```java public interface OcrOutputRe…

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

- No business value in code: threshold, workers, timeout and attempts are parameters. - No personal data in logs, tests or prompts. OCR text is never written to application logs; logs carry the intake ID and counts only. Test documents are synthetic. - No read of another module's tables: the case owner comes through CaseDirectory. - OCR text is held only in document_text and the standard container; it is not sent to any service other than the OCR service and the classifier.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-049-ocr-pipeline-on-the-workbench-document-hub-v1.md` |
| Specification | `output/INC-049-epic-1-RWB-E1-049/specify/spec.md` |
| Compliance validation | `output/INC-049-epic-1-RWB-E1-049/specify/compliance-validation.md` |
| Agent run log | `output/INC-049-epic-1-RWB-E1-049/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-049-epic-1-RWB-E1-049/plan/` |
| Implementation evidence | `output/INC-049-epic-1-RWB-E1-049/implement/` |
| API / functional test reports | `output/INC-049-epic-1-RWB-E1-049/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-049-epic-1-RWB-E1-049/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-049-ocr-pipeline-on-the-workbench-document-hub-v1.md` |
| Output run | `output/INC-049-epic-1-RWB-E1-049/` |

