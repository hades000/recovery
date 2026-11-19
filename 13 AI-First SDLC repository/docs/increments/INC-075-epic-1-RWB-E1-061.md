# Increment Card — INC-075-epic-1-RWB-E1-061

**RWB-E1-061 — Intake agent evaluation and L1 proposal [E2a]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-075` |
| Title | Intake agent evaluation and L1 proposal [E2a] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-061` |
| RUN_ID | `INC-075-epic-1-RWB-E1-061` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-059 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built from the stored shadow results**, so that **the risk and model risk officer approves the step to L1 on measured results**.

**Main flow:**
1. RW-COE: requests the report for the evaluation run through GET /admin/agent-evaluations/{evaluationId}/report.
2. System: builds the report from the stored runs and scores: sample size, agreement rate per gap type, failure counts by type, total and per-case cost, median and 95th percentile latency, policy, prompt and model versions.
3. RW-COE: exports the report as CSV and PDF for the steering committee pack.
4. RW-COE: loads policy "INTAKE" version "P2" with autonomy mode L1, the evaluation run ID, the conditions, the fallback and the measures to watch through POST /admin/agent-configs.
5. System: checks that the evaluation run is DONE, that its scores meet every stated condition and that the fallback and measures are present; stores the version as LOADED.
6. RW-RISK: approves version "P2" with a valid from date through POST /admin/agent-configs/{versionId}/approve after the committee agrees.

**Out of scope:**
- Showing the intake summary to case owners at L1 (RWB-E2-028).
- Changing an autonomy level from a screen (FEAT-AGT-12, Epic 3).
- The steering committee meeting itself and its minutes.

**Business outcome and value hypothesis:** The step from shadow to L1 puts agent output in front of case owners, so the approver needs the agreement rate, the failure types, the cost and the latency on a stated sample before deciding. This story produces that report from the evaluation run of RWB-E1-059 and holds the L1 proposal as a versioned policy row with its conditions, fallback and measures to watch (REQ-DRI-010), approved and dated like any other reference row (REQ-DRI-011). Nothing goes to L1 until RW-RISK approves the row.

**Constraints and guardrails:**
- No business value in code: conditions, measures and the minimum sample are row values.
- No personal data in logs, tests or the report; the report holds counts and rates only.
- No read of another module's tables.
- A proposal never changes the mode in force before it is approved and its valid from date is reached.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md` |
| Requirement IDs | REQ-DRI-010, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.7 |
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
| RW-COE | Requests and exports the report; loads the proposal (Rules and parameters CRUD) |
| RW-RISK | Reads the report; approves the proposal (Rules and parameters A) |
| RW-AUDIT | Reads the report and the versions (Rules and parameters R) |
| Approval levels | No delegation of authority level applies |

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
- **Feature flag:** None.
- **Critical path:** Yes; **depends on:** RWB-E1-059.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: conditions, measures and the minimum sample are row values.
  - No personal data in logs, tests or the report; the report holds counts and rates only.
  - No read of another module's tables.
  - A proposal never changes the mode in force before it is approved and its valid from date is reached.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md` |
| Specification | `output/INC-075-epic-1-RWB-E1-061/specify/spec.md` |
| Compliance validation | `output/INC-075-epic-1-RWB-E1-061/specify/compliance-validation.md` |
| Agent run log | `output/INC-075-epic-1-RWB-E1-061/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-075-epic-1-RWB-E1-061/plan/` (TBC) |
| Implementation evidence | `output/INC-075-epic-1-RWB-E1-061/implement/` (TBC) |
| API / functional test reports | `output/INC-075-epic-1-RWB-E1-061/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-075-epic-1-RWB-E1-061/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-075-epic-1-RWB-E1-061/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md` |
| Output run | `output/INC-075-epic-1-RWB-E1-061/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
