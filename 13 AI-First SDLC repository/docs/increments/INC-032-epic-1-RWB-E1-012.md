# Increment Card — INC-032-epic-1-RWB-E1-012

**RWB-E1-012 — Retire local copies**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-032` |
| Title | Retire local copies |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-012` |
| RUN_ID | `INC-032-epic-1-RWB-E1-012` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-022, RWB-E1-010 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **to confirm in the Workbench that my team's Excel or SharePoint tracker is replaced by the case list, with the location of the read-only archive recorded**, so that **there is one list and no shadow copy**.

**Main flow:**
1. Team manager: works from the case list for at least two working days after the tracker's load is signed off.
2. Team manager: sets the tracker read-only in SharePoint or moves it to the archive location.
3. Team manager: calls `POST /admin/trackers/{trackerId}/retire` with the archive location.
4. System: checks the caller belongs to the tracker's team and holds Queue and allocation A.
5. System: checks the tracker can be retired: decision LOAD with status SIGNED_OFF and at least two working days since sign-off, or decision RETIRE with status LISTED.
6. System: lists the fields of the tracker's field list that are not personal and have no data product field mapped to them.

**Out of scope:**
- Setting the tracker read-only in SharePoint, which the team does in SharePoint.
- Loading the tracker content (RWB-E1-010).
- Feeding the fields no feed carries into a data product (the owning module, in the epic that needs the field).
- A screen for the inventory and retirement (SCR-40 Reference data, Epic 8).

**Business outcome and value hypothesis:** A tracker that stays in use after its data is loaded becomes a second version of the truth, and the two drift apart within days. This story lets the team manager retire each tracker after its load is signed off and the team has worked from the case list for two working days, records where the read-only archive is, logs the tracker fields that no data product carries, and gives the Tribe lead one report of the six teams for the business sign-off before the release. It completes REQ-RDF-006 (local copy retired with the owner's confirmation and a read-only archive kept).

**Constraints and guardrails:**
- No business value in code: the parallel period and the team list are parameters.
- No personal data in logs, tests or prompts. Archive locations in tests use the example domain.
- No read of another module's tables. Team names come through the P4 published interface.
- The Workbench does not change, move or delete the team's tracker; the team makes it read-only, and the Workbench records the location.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 012 Retire local copies v1.md` |
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
| RW-TEAMMGR, team manager of the tracker's team | Confirms the retirement (Queue and allocation A, scope Team) |
| RW-DATASTEW, data steward and data product owner | Reads the trackers and the retirement report (Reference data R) |
| RW-COE, RW-TEAMMGR, RW-AUDIT | Read the trackers and the report (Reference data R) |
| RW-TRIBE, Tribe lead and squad members | Read the report for the release checklist (Reference data R) |

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
- **Feature flag:** `rwb.p1.tracker-retire`.
- **Critical path:** No; **depends on:** RWB-E1-022, RWB-E1-010.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the parallel period and the team list are parameters.
  - No personal data in logs, tests or prompts. Archive locations in tests use the example domain.
  - No read of another module's tables. Team names come through the P4 published interface.
  - The Workbench does not change, move or delete the team's tracker; the team makes it read-only, and the Workbench records the location.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 012 Retire local copies v1.md` |
| Specification | `output/INC-032-epic-1-RWB-E1-012/specify/spec.md` |
| Compliance validation | `output/INC-032-epic-1-RWB-E1-012/specify/compliance-validation.md` |
| Agent run log | `output/INC-032-epic-1-RWB-E1-012/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-032-epic-1-RWB-E1-012/plan/` (TBC) |
| Implementation evidence | `output/INC-032-epic-1-RWB-E1-012/implement/` (TBC) |
| API / functional test reports | `output/INC-032-epic-1-RWB-E1-012/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-032-epic-1-RWB-E1-012/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-032-epic-1-RWB-E1-012/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 012 Retire local copies v1.md` |
| Output run | `output/INC-032-epic-1-RWB-E1-012/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
