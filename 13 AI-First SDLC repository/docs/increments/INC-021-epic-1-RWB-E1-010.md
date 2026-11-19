# Increment Card — INC-021-epic-1-RWB-E1-010

**RWB-E1-010 — Excel and SharePoint loads**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-021` |
| Title | Excel and SharePoint loads |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-010` |
| RUN_ID | `INC-021-epic-1-RWB-E1-010` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-005, RWB-E1-003 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **every inventoried tracker with a load decision loaded into its data product, with the row counts reconciled and the team manager's sign-off**, so that **the teams' own lists are held in the Workbench data store**.

**Main flow:**
1. Data steward: calls `POST /admin/trackers/{trackerId}/loads` with the tracker file.
2. System: checks the tracker has decision LOAD and status LISTED or LOADED, the file type, and that the file hash has not been loaded before.
3. System: stores the file in the write-once tracker file store, opens a load_run for the tracker and returns 202 with the Job.
4. System: checks that the header columns match the field list; a mismatch refuses the file.
5. System: for each row, rejects it if the account number is empty (TRK-01) or not in loan_account (TRK-02), and writes the rejection to dq_exception with the row number.
6. System: drops every field tagged as personal data and writes the other fields of each accepted row to tracker_row with the target data product, the file name and the row number, in one transaction; rows of an earlier load of the same tracker are replaced.

**Out of scope:**
- Retiring the local copy and the business sign-off (RWB-E1-012).
- Mapping tracker content into legal_action, asset or treatment records (S4, S5 and S2 in their epics).
- A screen for tracker loads (SCR-44 Interface and job monitor, Epic 2).
- Trackers with a KEEP decision.

**Business outcome and value hypothesis:** The recovery teams hold case facts in trackers that only they can see, so the facts are lost when the tracker is retired unless they are loaded first. This story loads each tracker file with a LOAD decision into the tracker content of its target data product, rejects rows that cannot be matched to an account, drops fields tagged as personal data, and records the team manager's sign-off that the counts match the file. It meets the load and reconcile part of REQ-RDF-006; the retirement is RWB-E1-012.

**Constraints and guardrails:**
- No business value in code: field lists, target products and the size limit are data.
- No personal data in logs, tests or prompts. Personal fields are dropped before storage; rejected rows are named by tracker code and row number only; test files are synthetic.
- No read of another module's tables. Tracker rows stay in tracker_row; no write to legal_action or any other module's table.
- The stored tracker file is never changed or deleted by the Workbench.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 010 Excel and SharePoint loads v1.md` |
| Requirement IDs | REQ-RDF-006 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
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
| RW-DATASTEW, data steward and data product owner | Uploads a tracker file (Reference data U) |
| RW-TEAMMGR, team manager of the tracker's team | Signs off the counts (Queue and allocation A, scope Team) |
| SY-DATALOAD, data load from COLLINS | Runs the load; writes tracker_row, load_run, dq_exception and the tracker counts |
| RW-COE, RW-DATASTEW, RW-PLATADM, RW-AUDIT | List the runs (Platform administration R) and the rejected rows |

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
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p1.tracker-load`.
- **Critical path:** No; **depends on:** RWB-E1-005, RWB-E1-003.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: field lists, target products and the size limit are data.
  - No personal data in logs, tests or prompts. Personal fields are dropped before storage; rejected rows are named by tracker code and row number only; test files are synthetic.
  - No read of another module's tables. Tracker rows stay in tracker_row; no write to legal_action or any other module's table.
  - The stored tracker file is never changed or deleted by the Workbench.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 010 Excel and SharePoint loads v1.md` |
| Specification | `output/INC-021-epic-1-RWB-E1-010/specify/spec.md` |
| Compliance validation | `output/INC-021-epic-1-RWB-E1-010/specify/compliance-validation.md` |
| Agent run log | `output/INC-021-epic-1-RWB-E1-010/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-021-epic-1-RWB-E1-010/plan/` (TBC) |
| Implementation evidence | `output/INC-021-epic-1-RWB-E1-010/implement/` (TBC) |
| API / functional test reports | `output/INC-021-epic-1-RWB-E1-010/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-021-epic-1-RWB-E1-010/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-021-epic-1-RWB-E1-010/specify/compliance-validation.md`) |
| Acceptance criteria | 13 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 010 Excel and SharePoint loads v1.md` |
| Output run | `output/INC-021-epic-1-RWB-E1-010/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
