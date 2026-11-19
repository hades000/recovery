# Increment Card — INC-064-epic-1-RWB-E1-057

**RWB-E1-057 — Intake from branches, mailroom, partner SFTP and email**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-064` |
| Title | Intake from branches, mailroom, partner SFTP and email |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-057` |
| RUN_ID | `INC-064-epic-1-RWB-E1-057` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-049, RWB-TE-012, RWB-E1-041 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5b.

## Scope

**Story:** As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**.

**Main flow:**
1. Scheduler: JOB-12 Document intake fires every 15 minutes in business hours on one service instance; intakeStep runs first, before scanStep.
2. IntakeStep: lists new files in each branch scanner folder and the mailroom folder, in each partner subfolder of the SFTP inbound folder, and new messages in each recovery mailbox.
3. IntakeStep: for each file or email attachment computes the SHA-256 hash and checks document_intake for the same channel and hash inside the duplicate window.
4. IntakeStep: checks the file type by content and extension, and the size, against the parameters.
5. IntakeStep: for a partner file, reads the partner by the subfolder's partner_code and checks that its panel_status is ACTIVE.
6. IntakeStep: copies an accepted file to the intake container and writes one document_intake row with source, channel code, source reference, file name, size, hash, received time, scanner time (scanner files), partner ID (partner files) or sender address (email), and the run ID; scan_result is left empty for scanStep.

**Out of scope:**
- The malware scan and quarantine (RWB-E1-041), OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching to a case (RWB-E1-032).
- Uploads from the case documents screen (RWB-E1-026).
- Field app photos and bills (RWB-E2-024).
- Partner uploads through the partner portal (Epic 4, PRT-03; partner access DL03).

**Business outcome and value hypothesis:** Documents reach recovery today by courier, shared folders and personal email, and an original that goes to the wrong desk is rebuilt for each audit. This story reads the four inbound paths every 15 minutes into the document intake, records where each file came from, refuses files that are not allowed or come from an unknown partner, and leaves every accepted file for the malware scan and OCR steps, so a document received in the morning is on the case the same day. It meets REQ-DCM-009 and puts every inbound file through the virus scan of REQ-DCM-010, and removes email hand-offs of customer documents (CTL-11).

**Constraints and guardrails:**
- No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters.
- No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders.
- No read of another module's tables: partners come through PartnerDirectory.
- A file is never removed from a channel before its document_intake row is committed.
- Storage is reached by managed identity only, never by key or shared access signature (RWB-TE-012).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md` |
| Requirement IDs | REQ-DCM-009, REQ-DCM-010 |
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
| SY-OCR, OCR and extraction pipeline | Runs intakeStep; reads the channels; writes document_intake and the intake container (Documents CRU) |
| RW-PLATADM, platform administrator | Sees runs on SCR-44 and reruns JOB-12 (Platform administration CRUD); sets the channel properties |
| RW-AGENCYMG, partner and agency manager | Keeps the partner codes and panel status that BR4 reads (Partner portal CRUDA) |
| RW-CASEOWN, case owner | Reads documents from intake once attached (Documents R) |

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
- **Critical path:** No; **depends on:** RWB-E1-049, RWB-TE-012, RWB-E1-041.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters.
  - No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders.
  - No read of another module's tables: partners come through PartnerDirectory.
  - A file is never removed from a channel before its document_intake row is committed.
  - Storage is reached by managed identity only, never by key or shared access signature (RWB-TE-012).

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md` |
| Specification | `output/INC-064-epic-1-RWB-E1-057/specify/spec.md` |
| Compliance validation | `output/INC-064-epic-1-RWB-E1-057/specify/compliance-validation.md` |
| Agent run log | `output/INC-064-epic-1-RWB-E1-057/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-064-epic-1-RWB-E1-057/plan/` (TBC) |
| Implementation evidence | `output/INC-064-epic-1-RWB-E1-057/implement/` (TBC) |
| API / functional test reports | `output/INC-064-epic-1-RWB-E1-057/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-064-epic-1-RWB-E1-057/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-064-epic-1-RWB-E1-057/specify/compliance-validation.md`) |
| Acceptance criteria | 16 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md` |
| Output run | `output/INC-064-epic-1-RWB-E1-057/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
