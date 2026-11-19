# Increment Card — INC-077-epic-1-RWB-E1-063

**RWB-E1-063 — Agent monitoring dashboard v1 [E2c]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-077` |
| Title | Agent monitoring dashboard v1 [E2c] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-063` |
| RUN_ID | `INC-077-epic-1-RWB-E1-063` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-061, RWB-E1-007, RWB-E1-014, RWB-E1-058 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **risk and model risk officer (RW-RISK)**, I want **a dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and an alert when an agent's daily cost passes its limit**, so that **every agent is watched from its first shadow run**.

**Main flow:**
1. JOB-15 Reporting extract: at 01:30 calls the P10 step AgentRunExtractStep for the previous business date.
2. System: groups the agent runs of that date by agent, policy version, prompt version and model version: runs, answered, fallback, median and 95th percentile latency, tokens and cost.
3. System: adds the latest DONE evaluation score per agent and version.
4. System: writes the rows to the data lake table agent_run_daily and checks that the row count and the sum of runs match the source.
5. System: compares each agent's cost for the date with daily_cost_cap_thb of its policy; for each breach writes one agent alert and sends MSG-P10-004 through the P6 notification interface to the alert role and to RW-RISK.
6. RW-RISK: opens the Power BI report "Agent monitor v1" and reads each agent by version and date.

**Out of scope:**
- Acceptance and override per segment, drift alerts and the SCR-46 agent monitor screen (RWB-E2-031).
- Drift detection with a raised decision (FEAT-AGT-13, Epic 3).
- The steering dashboard (RWB-E2-009).

**Business outcome and value hypothesis:** An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week, not at the L1 review. This story copies daily agent run figures to the data lake with the nightly reporting extract, matched by row count (REQ-DRI-009), so the Power BI dashboard reads the copy and not the live tables. A daily check sends an alert when the cost of an agent on a business date is above its policy limit.

**Constraints and guardrails:**
- No business value in code: caps and alert roles come from the agent policy.
- No personal data in logs, tests, the data lake table or the alert; rows hold counts, times and amounts only.
- No read of another module's tables; JOB-15 calls the P10 interface.
- The dashboard never reads the live agent tables.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 063 Agent monitoring dashboard v1 E2c v1.md` |
| Requirement IDs | REQ-DRI-009 |
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
| RW-RISK | Reads the dashboard (Reporting R); receives alerts |
| RW-COE | Reads the dashboard (Reporting R); receives alerts as the policy alert role |
| RW-BIANAL | Builds and maintains the Power BI report (Reporting CRUD) |
| RW-PLATADM | Reruns JOB-15 (Platform administration U through POST /admin/jobs/{jobId}/rerun) |
| RW-DATASTEW | Receives the count mismatch alert |

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
- **Critical path:** Yes; **depends on:** RWB-E1-061, RWB-E1-007, RWB-E1-014, RWB-E1-058.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: caps and alert roles come from the agent policy.
  - No personal data in logs, tests, the data lake table or the alert; rows hold counts, times and amounts only.
  - No read of another module's tables; JOB-15 calls the P10 interface.
  - The dashboard never reads the live agent tables.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 063 Agent monitoring dashboard v1 E2c v1.md` |
| Specification | `output/INC-077-epic-1-RWB-E1-063/specify/spec.md` |
| Compliance validation | `output/INC-077-epic-1-RWB-E1-063/specify/compliance-validation.md` |
| Agent run log | `output/INC-077-epic-1-RWB-E1-063/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-077-epic-1-RWB-E1-063/plan/` (TBC) |
| Implementation evidence | `output/INC-077-epic-1-RWB-E1-063/implement/` (TBC) |
| API / functional test reports | `output/INC-077-epic-1-RWB-E1-063/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-077-epic-1-RWB-E1-063/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-077-epic-1-RWB-E1-063/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 063 Agent monitoring dashboard v1 E2c v1.md` |
| Output run | `output/INC-077-epic-1-RWB-E1-063/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
