# Increment Card — INC-068-epic-1-RWB-E1-032

**RWB-E1-032 — Automatic attach from the OCR intake**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-068` |
| Title | Automatic attach from the OCR intake |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-032` |
| RUN_ID | `INC-068-epic-1-RWB-E1-032` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-024, RWB-E1-050, RWB-E1-053 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **documents from the OCR intake attached to their case automatically when the case ID or the account number is read, with unmatched or ambiguous documents held for a person who sees the OCR text and the candidate cases and attaches the document**, so that **no document is filed by hand when the case is clear and none is filed on the wrong case when it is not**.

**Main flow:**
1. JOB-12 Document intake: runs matchStep after the extraction step.
2. MatchStep: selects intake items with ocr_status DONE, match_status PENDING, no document_id and a predicted type (review_reason empty or LOW_CONFIDENCE), locking each row; items with review_reason UNKNOWN_TYPE or MODEL_UNAVAILABLE get match_status NO_TYPE and are held for a person.
3. CaseMatcher: collects case numbers from the extracted field case_no and from the OCR text with CASE_NO_PATTERN, and account numbers from the extracted field account_no and the text with ACCOUNT_NO_PATTERN.
4. CaseMatcher: resolves each case number with CaseDirectory.findByCaseNo and each account number with CaseDirectory.findOpenCasesByAccountNo, and returns one of MATCHED, NO_MATCH, MULTIPLE, CONFLICT or CASE_CLOSED with the candidates.
5. MatchStep: for MATCHED, calls DocumentStore.store with the case ID, predicted_type, the intake source, the file, its hash and the extracted fields; the store writes the DOCATT entry with the classifier version, the confidence and the match method, the document row and DocumentStored.
6. MatchStep: on the stored document sets classification_confidence, document_type and type_candidates; for review_reason LOW_CONFIDENCE sets review_status PENDING and write_once false, so it is held in rwb-docs and listed on SCR-31 (RWB-E1-054).

**Out of scope:**
- Confirming or correcting the type and the fields of a document stored for review (RWB-E1-054).
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record (RWB-E1-057).
- Moving an attached document to another case (Epic 2).
- Attach of field app photos (RWB-E2-024).

**Business outcome and value hypothesis:** Scans, partner files and emails arrive without a case link; today a person reads each one and files it. This story matches each classified intake item to one open case by the case ID or the account number in its text and stores it on that case with no person involved (FSD P5 A2.12). An item that matches no case, more than one case, a closed case or no agreed type is held as unmatched, and a person attaches it from the review queue with the OCR text and the candidates in front of them. It meets REQ-DCM-007 and writes the document attached record required from Epic 1 (REQ-DRI-004, RWB-E1-027). The measure is fields extracted without review (FSD P5 A2.12.1).

**Constraints and guardrails:**
- No business value in code: the case number and account number patterns and the threshold are parameters.
- No personal data in logs, tests or prompts: account numbers and OCR text are never logged; logs carry the intake ID and the outcome; test accounts are synthetic.
- No read of another module's tables: cases and accounts are resolved through CaseDirectory.
- The matcher never picks one of several candidates; any doubt goes to a person.
- A document stored for type review is never put in the write-once container before its type is confirmed (RWB-E1-054).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 032 Automatic attach from the OCR intake v1.md` |
| Requirement IDs | REQ-DCM-007 |
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
| SY-OCR, OCR and extraction pipeline | Matches and attaches automatically (Documents C) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Roles with Documents C and the candidate case in scope (for example RW-LITOFF, RW-CASEOWN) | See and attach unmatched items that name a candidate in their scope |
| Roles with Documents C and scope ALL (for example RW-LEGAL) | See and attach unmatched items with no candidate |
| Roles with Documents R only (for example RW-TEAMMGR) | See attached documents on cases in their scope; no attach |

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
- **Feature flag:** `rwb.dochub.autoattach`. Off: matchStep sets every classified item to match_status NO_MATCH, and reviewers attach them by hand.
- **Critical path:** No; **depends on:** RWB-E1-024, RWB-E1-050, RWB-E1-053.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the case number and account number patterns and the threshold are parameters.
  - No personal data in logs, tests or prompts: account numbers and OCR text are never logged; logs carry the intake ID and the outcome; test accounts are synthetic.
  - No read of another module's tables: cases and accounts are resolved through CaseDirectory.
  - The matcher never picks one of several candidates; any doubt goes to a person.
  - A document stored for type review is never put in the write-once container before its type is confirmed (RWB-E1-054).

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 032 Automatic attach from the OCR intake v1.md` |
| Specification | `output/INC-068-epic-1-RWB-E1-032/specify/spec.md` |
| Compliance validation | `output/INC-068-epic-1-RWB-E1-032/specify/compliance-validation.md` |
| Agent run log | `output/INC-068-epic-1-RWB-E1-032/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-068-epic-1-RWB-E1-032/plan/` (TBC) |
| Implementation evidence | `output/INC-068-epic-1-RWB-E1-032/implement/` (TBC) |
| API / functional test reports | `output/INC-068-epic-1-RWB-E1-032/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-068-epic-1-RWB-E1-032/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-068-epic-1-RWB-E1-032/specify/compliance-validation.md`) |
| Acceptance criteria | 15 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 032 Automatic attach from the OCR intake v1.md` |
| Output run | `output/INC-068-epic-1-RWB-E1-032/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
