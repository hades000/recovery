# Increment Card — INC-070-epic-1-RWB-E1-034

**RWB-E1-034 — Letter template management**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-070` |
| Title | Letter template management |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-034` |
| RUN_ID | `INC-070-epic-1-RWB-E1-034` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-046, RWB-E1-015 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications. **Build group:** P6.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **a screen to upload a template version, have Legal counsel record the approval and set it current**, so that **templates are managed without a developer**.

**Main flow:**
1. Litigation officer: opens SCR-33 Template approval and chooses the template code and language, or a new code.
2. Litigation officer: uploads the DOCX body and enters product group, channel, notice type, signature basis and the merge codes used.
3. System: checks the role (Documents C), the required fields, the file type and size, and every merge code against the catalog (MergeCodeScanner from RWB-E1-046).
4. System: stores the body write-once, creates the next version number in state Draft and shows it in the list.
5. Legal counsel: opens the Draft version, reads the body and the merge codes, enters the valid from date and approves.
6. System: checks the role (Documents A), that the approver is not the uploader (CTL-05), that the version is Draft and that valid from is not before today; sets state Approved with approver and approval time.

**Out of scope:**
- The catalog tables, load checks and TemplateCatalog interface (RWB-E1-046).
- Generating notices from a template (RWB-E1-052) and resuming held notices when a new version is approved (R-LIT-06, RWB-E2-021).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).
- Thai labels on SCR-33 beyond the standard messages (DL10).

**Business outcome and value hypothesis:** A template change today needs a person outside Legal to edit a file and send it round, and nothing records which wording was approved. This story gives the litigation officer an upload and Legal counsel an approve and withdraw action on SCR-33 Template approval, with the approver and date held on the version. It serves REQ-OCC-002 and control CTL-14 (every notice from the current Legal-approved version), and removes the developer from template changes.

**Constraints and guardrails:**
- No business value in code: file types, size limit, merge codes and the template list are data or configuration.
- No personal data in logs, tests or prompts. Template bodies in tests carry synthetic wording; the audit entry holds user IDs, template code and version only.
- No read of another module's tables. Roles come from the ACE access check; storage through the ACE storage pattern.
- A stored body is never overwritten; a correction is a new version.
- The screen hides actions the role does not hold, and the server checks the right on every call.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 034 Letter template management v1.md` |
| Requirement IDs | REQ-OCC-002 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
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
| RW-LITOFF, litigation officer | Uploads a version (Documents C), reads templates (Documents R) |
| RW-LEGAL, Legal counsel | Uploads, approves and withdraws a version (Documents CRUA); cannot approve own upload |
| RW-CASEOWN, RW-TEAMMGR and other roles with Documents R | Read templates on SCR-33 |
| RW-COMPLY, Compliance and PDPA officer | Reads templates (Documents R) |

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
- **Feature flag:** `rwb.comms.template-admin`.
- **Critical path:** No; **depends on:** RWB-E1-046, RWB-E1-015.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: file types, size limit, merge codes and the template list are data or configuration.
  - No personal data in logs, tests or prompts. Template bodies in tests carry synthetic wording; the audit entry holds user IDs, template code and version only.
  - No read of another module's tables. Roles come from the ACE access check; storage through the ACE storage pattern.
  - A stored body is never overwritten; a correction is a new version.
  - The screen hides actions the role does not hold, and the server checks the right on every call.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 034 Letter template management v1.md` |
| Specification | `output/INC-070-epic-1-RWB-E1-034/specify/spec.md` |
| Compliance validation | `output/INC-070-epic-1-RWB-E1-034/specify/compliance-validation.md` |
| Agent run log | `output/INC-070-epic-1-RWB-E1-034/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-070-epic-1-RWB-E1-034/plan/` (TBC) |
| Implementation evidence | `output/INC-070-epic-1-RWB-E1-034/implement/` (TBC) |
| API / functional test reports | `output/INC-070-epic-1-RWB-E1-034/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-070-epic-1-RWB-E1-034/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-070-epic-1-RWB-E1-034/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 034 Letter template management v1.md` |
| Output run | `output/INC-070-epic-1-RWB-E1-034/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
