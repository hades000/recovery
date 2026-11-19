# Increment Card — INC-004-epic-1-RWB-TE-002

**RWB-TE-002 — Code owners for the recovery module**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-004` |
| Title | Code owners for the recovery module |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-002` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-TE-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

**Main flow:**
1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
2. Squad member: adds the code owners validation step to the pull request pipeline.
3. ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.
4. Developer: opens a pull request that changes a recovery folder.
5. Repository host: requests review from the owning team named for each changed path.
6. Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.

**Out of scope:**
- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).

**Business outcome and value hypothesis:** The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.

**Constraints and guardrails:**
- No business value in code; the file holds paths and team names only.
- No personal data in logs, tests or prompts; test pull requests change fixture files only.
- No read of another module's tables; the file is the review control for the boundary of RWB-TE-001.
- Team handles are teams, never single people, so absence of one person does not block a merge.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 002 Code owners for the recovery module v1.md` |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraints Built on ACE and Modular monolith) |
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
| TechX recovery tech leads | Approve changes to recovery folders and the module map |
| ACE team | Approves changes to the common module and the code owners file; sets the branch rule on main |
| RW-TRIBE, tribe lead and squad members | Open pull requests; cannot satisfy a code owner review unless in the owning team |
| No Workbench capability area applies | Access is a repository right, not a Workbench role right |

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
- **Feature flag:** None. The file and the branch rule have no runtime path.
- **Critical path:** No; **depends on:** RWB-TE-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code; the file holds paths and team names only.
  - No personal data in logs, tests or prompts; test pull requests change fixture files only.
  - No read of another module's tables; the file is the review control for the boundary of RWB-TE-001.
  - Team handles are teams, never single people, so absence of one person does not block a merge.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 002 Code owners for the recovery module v1.md` |
| Specification | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` |
| Compliance validation | `output/INC-004-epic-1-RWB-TE-002/specify/compliance-validation.md` |
| Agent run log | `output/INC-004-epic-1-RWB-TE-002/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-004-epic-1-RWB-TE-002/plan/` (TBC) |
| Implementation evidence | `output/INC-004-epic-1-RWB-TE-002/implement/` (TBC) |
| API / functional test reports | `output/INC-004-epic-1-RWB-TE-002/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-004-epic-1-RWB-TE-002/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-004-epic-1-RWB-TE-002/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 002 Code owners for the recovery module v1.md` |
| Output run | `output/INC-004-epic-1-RWB-TE-002/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
