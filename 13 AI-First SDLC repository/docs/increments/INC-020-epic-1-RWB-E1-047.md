# Increment Card — INC-020-epic-1-RWB-E1-047

**RWB-E1-047 — Feature flags for module release with a removal date**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-020` |
| Title | Feature flags for module release with a removal date |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-047` |
| RUN_ID | `INC-020-epic-1-RWB-E1-047` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **a feature flag service with each flag held as data (key, owner, value per environment, removal date) and read by the service and the front end at run time**, so that **a feature can be released switched off and switched on without a deployment, and no flag stays after its removal date without its owner being told**.

**Main flow:**
1. Platform administrator: creates a flag with key, description, owner, default value and removal date.
2. System: validates the key pattern `rwb.<module>.<short-name>`, the removal date and the owner, and writes the flag row with every environment set to the default.
3. Service code: calls FeatureFlags.isOn(key) at each request; the value comes from a cache refreshed every 30 seconds (assumed; DL11).
4. Front end: reads GET /feature-flags at page load and hides or shows the component.
5. Platform administrator: switches the flag on for one environment with a reason.
6. System: checks the version, writes the new value and a feature_flag_change row with user, time, old and new value, and writes the ACE audit log entry.

**Out of scope:**
- The admin console screen for flags: SCR-44, Epic 8.
- Release and merge ownership: DL04.
- The queue write flag for models and agents: RWB-E2-036.

**Business outcome and value hypothesis:** Two squads release monthly from one repository, and one squad's unfinished change must not hold the other's release (ADR-008, DT11). A flag held as a data row lets the platform administrator switch a change off in SIT or UAT and let the release go ahead, with every change logged. A weekly report lists flags past their removal date so old code paths are removed. It meets REQ-DRI-010 (configuration changed without a code release).

**Constraints and guardrails:**
- No business value in code: flag values, owners and dates are rows; code holds only the key.
- No personal data in logs, tests or prompts; the change log holds user IDs, never names.
- No read of another module's tables; other modules call FeatureFlags.isOn.
- Every flag that is off runs the previous code path; a test covers both paths of every flag.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 047 Feature flags for module release with a removal date v1.md` |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.7 |
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
| RW-PLATADM, platform administrator | Creates flags, changes values, retires flags (Platform administration, CRUD) |
| RW-SECADM, security administrator | Reads and changes flags (Platform administration, CRUDA) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read flags and their change history (Platform administration, R) |
| RW-TRIBE, tribe lead and squad members | Receive the weekly report as flag owners; no change right |
| Every signed-in Workbench role | Reads the effective values through GET /feature-flags |

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
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: flag values, owners and dates are rows; code holds only the key.
  - No personal data in logs, tests or prompts; the change log holds user IDs, never names.
  - No read of another module's tables; other modules call FeatureFlags.isOn.
  - Every flag that is off runs the previous code path; a test covers both paths of every flag.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 047 Feature flags for module release with a removal date v1.md` |
| Specification | `output/INC-020-epic-1-RWB-E1-047/specify/spec.md` |
| Compliance validation | `output/INC-020-epic-1-RWB-E1-047/specify/compliance-validation.md` |
| Agent run log | `output/INC-020-epic-1-RWB-E1-047/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-020-epic-1-RWB-E1-047/plan/` (TBC) |
| Implementation evidence | `output/INC-020-epic-1-RWB-E1-047/implement/` (TBC) |
| API / functional test reports | `output/INC-020-epic-1-RWB-E1-047/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-020-epic-1-RWB-E1-047/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-020-epic-1-RWB-E1-047/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 047 Feature flags for module release with a removal date v1.md` |
| Output run | `output/INC-020-epic-1-RWB-E1-047/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
