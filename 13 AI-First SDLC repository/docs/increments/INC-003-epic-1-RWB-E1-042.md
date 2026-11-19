# Increment Card — INC-003-epic-1-RWB-E1-042

**RWB-E1-042 — Central configuration service and parameter catalog**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-003` |
| Title | Central configuration service and parameter catalog |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-042` |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | Yes |
| Depends on | RWB-E1-044 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.

**Main flow:**
1. Squad member: adds a parameter to `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used by; the pull request is reviewed by the owner.
2. Build: generates the `ParameterKeys` class from the catalog file; code reads a value only through ParameterService with a generated key.
3. Build: runs the magic number check over the recovery packages and the catalog completeness check.
4. Flyway: loads the catalog rows and the default values into parameter_catalog and parameter_value at deployment.
5. RW-COE: loads a new value version through POST /admin/reference-loads with table "PARAMETER", for example `case.entry.dpd` = 91 in PROD valid from 2026-12-10.
6. ParameterLoadChecks: checks key in catalog, type, range, environment and required values; refuses the load whole on any failure.

**Out of scope:**
- The reference data service for the other tables (RWB-E1-043).
- Product-specific parameters and service levels (RWB-E1-045).
- Dated feature flags (FEAT-CWC-26).
- The administration screen for parameters (Epic 8, FEAT-ADM-01).
- The change checklist and audit report (RWB-E1-048).

**Business outcome and value hypothesis:** Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.

**Constraints and guardrails:**
- No business value in code: every limit, threshold, name and timer is a catalog entry with a value row; the build check enforces it.
- No personal data in parameters, logs, tests or prompts; no secret value in the tables, the logs or any response.
- No read of another module's tables: other modules read values only through ParameterService.
- A value change never needs a deployment; a new parameter needs a reviewed catalog entry.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 042 Central configuration service and parameter catalog v1.md` |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
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
| RW-COE | Owns the catalog; loads value versions (Reference data C; Rules and parameters CRUD) |
| RW-RISK | Approves a value version where a threshold or a limit moves (Reference data A, assumed grant; DL01) |
| RW-PLATADM | Owns environment settings; reads the catalog (Rules and parameters R) |
| RW-TRIBE | Adds catalog entries through reviewed pull requests |
| Every role with Rules and parameters R | Reads the catalog |
| RW-PHONECOL | No Rules and parameters right; refused |
| No delegation of authority level applies | A parameter is not a credit decision |

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
- **Feature flag:** `rwb.p3.configservice`. Off: services read the defaults from the generated keys only, and value loads are refused.
- **Critical path:** Yes; **depends on:** RWB-E1-044.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: every limit, threshold, name and timer is a catalog entry with a value row; the build check enforces it.
  - No personal data in parameters, logs, tests or prompts; no secret value in the tables, the logs or any response.
  - No read of another module's tables: other modules read values only through ParameterService.
  - A value change never needs a deployment; a new parameter needs a reviewed catalog entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 042 Central configuration service and parameter catalog v1.md` |
| Specification | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` |
| Compliance validation | `output/INC-003-epic-1-RWB-E1-042/specify/compliance-validation.md` |
| Agent run log | `output/INC-003-epic-1-RWB-E1-042/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-003-epic-1-RWB-E1-042/plan/` (TBC) |
| Implementation evidence | `output/INC-003-epic-1-RWB-E1-042/implement/` (TBC) |
| API / functional test reports | `output/INC-003-epic-1-RWB-E1-042/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-003-epic-1-RWB-E1-042/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-003-epic-1-RWB-E1-042/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | Intentional gaps: AC2, AC3 (removed by the 4 November 2026 cleanup) |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 042 Central configuration service and parameter catalog v1.md` |
| Output run | `output/INC-003-epic-1-RWB-E1-042/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
