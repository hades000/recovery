# Increment Card — INC-057-epic-1-RWB-E1-041

**RWB-E1-041 — Retention classes and virus scan on intake**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-057` |
| Title | Retention classes and virus scan on intake |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-041` |
| RUN_ID | `INC-057-epic-1-RWB-E1-041` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-024, RWB-E1-049 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **compliance and PDPA officer (RW-COMPLY)**, I want **every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on**, so that **the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place**.

**Main flow:**
1. JOB-12 Document intake: runs scanStep first, before ocrStep.
2. ScanStep: selects intake items with no scan_result and sends each file to MalwareScanClient.
3. ScanStep: on CLEAN, sets scan_result CLEAN and scanned_at, so ocrStep may read the item; on INFECTED, moves the file to the quarantine container, sets scan_result INFECTED, writes the audit event MALWARE_BLOCKED and alerts the platform administrator; the file is never stored.
4. Upload (RWB-E1-026): calls MalwareScanService.scanNow before DocumentStore.store; INFECTED returns 422 MSG-P5-016; if the scanning service does not answer, the call returns 503 MSG-P5-022 and nothing is kept.
5. DocumentStore (RWB-E1-024): stores clean files with the retention class of the type; legal types go to the write-once container.
6. JOB-17 Retention job: runs on the first Sunday of each month; for each active document computes expiry date = stored date plus period_months of its class.

**Out of scope:**
- Disposal or extension of a document at the end of its class by a recorded decision (Epic 2, REQ-DCM-019).
- Applying retention on case closure (FEAT-COM-08, Epic 4).
- Placing or lifting a legal hold (P3, POST /api/recovery/v1/cases/{caseId}/legal-hold).
- The retention and personal data screen SCR-47 (Epic 8).
- Retention of the decision log and the interaction ledger (RWB-E1-014, RWB-E2-034).

**Business outcome and value hypothesis:** Files reach the bank from branches, partners and email; one infected file in the store reaches every user who opens it. Documents also have no retention rule today, so nothing shows when a document may be archived (FSD P5 A2.17, A2.18). This story scans every file before storage and quarantines a failed file, holds the retention classes as data, and runs JOB-17 to archive documents past their class or list them for the Compliance review. It meets REQ-DCM-010 and REQ-DCM-016 (legal hold overrides retention), with NFR-028, NFR-072 and NFR-074.

**Constraints and guardrails:**
- No business value in code: periods, end actions and the scan timeout are data or properties.
- No personal data in logs, tests or prompts: audit events carry the intake ID and the source, never the file name or content; test files are synthetic.
- No read of another module's tables: legal hold comes through CaseDirectory.
- The retention job never deletes a blob and never changes a write-once blob's content.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 041 Retention classes and virus scan on intake v1.md` |
| Requirement IDs | REQ-DCM-010, REQ-DCM-016 |
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
| SY-OCR, OCR and extraction pipeline | Runs the scan step (Documents CRU) |
| RW-COMPLY, compliance and PDPA officer | Owns the retention classes; reads the review list and the job counts |
| RW-REFADM, reference data administrator | Loads the retention class table (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the compliance and PDPA officer as table owner (DL01) |
| RW-PLATADM, platform administrator | Receives scan alerts; reruns JOB-12 and JOB-17 |
| SY-DECLOG, decision log writer | Writes the DOCRET entry |

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
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-024, RWB-E1-049.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: periods, end actions and the scan timeout are data or properties.
  - No personal data in logs, tests or prompts: audit events carry the intake ID and the source, never the file name or content; test files are synthetic.
  - No read of another module's tables: legal hold comes through CaseDirectory.
  - The retention job never deletes a blob and never changes a write-once blob's content.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 041 Retention classes and virus scan on intake v1.md` |
| Specification | `output/INC-057-epic-1-RWB-E1-041/specify/spec.md` |
| Compliance validation | `output/INC-057-epic-1-RWB-E1-041/specify/compliance-validation.md` |
| Agent run log | `output/INC-057-epic-1-RWB-E1-041/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-057-epic-1-RWB-E1-041/plan/` (TBC) |
| Implementation evidence | `output/INC-057-epic-1-RWB-E1-041/implement/` (TBC) |
| API / functional test reports | `output/INC-057-epic-1-RWB-E1-041/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-057-epic-1-RWB-E1-041/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-057-epic-1-RWB-E1-041/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 041 Retention classes and virus scan on intake v1.md` |
| Output run | `output/INC-057-epic-1-RWB-E1-041/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
