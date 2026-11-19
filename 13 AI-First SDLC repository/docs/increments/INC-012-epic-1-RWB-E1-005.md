# Increment Card — INC-012-epic-1-RWB-E1-005

**RWB-E1-005 — Excel and SharePoint inventory**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-012` |
| Title | Excel and SharePoint inventory |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-005` |
| RUN_ID | `INC-012-epic-1-RWB-E1-005` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-001, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **every recovery team's Excel files, SharePoint lists and local files listed with owner, fields, update cycle and a load, retire or keep decision**, so that **each file can be loaded into its data product and then retired**.

**Main flow:**
1. Data steward: fills the inventory template, one row per tracker, with the decision and reason for each.
2. Reference data administrator: loads the file through `POST /admin/reference-loads` with table code `tracker_inventory`, version "TRK-2026.11" and valid from 2026-11-16.
3. System: `TrackerInventoryHandler.validate` checks every row: required fields, list values, a unique tracker code, a target data product for each LOAD decision, and at least one row for each of the six teams.
4. System: refuses the whole file and returns the row errors if any check fails.
5. Data steward: confirms the version as its owner through the reference data change process.
6. System: `TrackerInventoryHandler.apply` writes the rows in one transaction; a tracker already in the previous version keeps its status; a new tracker gets status LISTED, or KEPT for a KEEP decision.

**Out of scope:**
- Loading the trackers with a LOAD decision (RWB-E1-010).
- Retiring the local copies (RWB-E1-012).
- A screen for the inventory (SCR-40 Reference data, Epic 8).
- Mapping tracker fields into the proper data product tables, such as legal_action (S4, Epic 5).

**Business outcome and value hypothesis:** The TDR, deed in lieu, litigation, NPA, debt sale and write-off teams each keep their own trackers, and no list says which trackers exist, who owns them or what replaces them. This story holds the tracker inventory as a versioned table in the Workbench, refuses an inventory that leaves out a team or a decision, and gives every tracker the status that the load (RWB-E1-010) and the retirement (RWB-E1-012) move forward. It meets REQ-RDF-005 and is the first step of REQ-RDF-006.

**Constraints and guardrails:**
- No business value in code: the team list is a parameter; decisions and owners are data.
- No personal data in logs, tests or prompts. The inventory lists field names, never field values.
- No read of another module's tables. Team codes are checked through the P4 published interface.
- The Workbench does not open, copy or change any tracker in this story.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 005 Excel and SharePoint inventory v1.md` |
| Requirement IDs | REQ-RDF-005 |
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
| RW-REFADM, reference data administrator | Loads the inventory file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Prepares the file; confirms the version as owner; lists trackers (Reference data R) |
| RW-COE, center of excellence analyst | Lists trackers (Reference data R) |
| RW-TEAMMGR, team manager | Supplies the team's rows; lists trackers (Reference data R) |
| Partner users | Refused with MSG-P4-002 |

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
- **Feature flag:** `rwb.p1.tracker-inventory`.
- **Critical path:** No; **depends on:** RWB-E1-001, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the team list is a parameter; decisions and owners are data.
  - No personal data in logs, tests or prompts. The inventory lists field names, never field values.
  - No read of another module's tables. Team codes are checked through the P4 published interface.
  - The Workbench does not open, copy or change any tracker in this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 005 Excel and SharePoint inventory v1.md` |
| Specification | `output/INC-012-epic-1-RWB-E1-005/specify/spec.md` |
| Compliance validation | `output/INC-012-epic-1-RWB-E1-005/specify/compliance-validation.md` |
| Agent run log | `output/INC-012-epic-1-RWB-E1-005/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-012-epic-1-RWB-E1-005/plan/` (TBC) |
| Implementation evidence | `output/INC-012-epic-1-RWB-E1-005/implement/` (TBC) |
| API / functional test reports | `output/INC-012-epic-1-RWB-E1-005/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-012-epic-1-RWB-E1-005/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-012-epic-1-RWB-E1-005/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 005 Excel and SharePoint inventory v1.md` |
| Output run | `output/INC-012-epic-1-RWB-E1-005/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
