# Increment Card — INC-069-epic-1-RWB-E1-061

**RWB-E1-061 — Intake agent evaluation and L1 proposal [E2a]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-069` |
| Title | Intake agent evaluation and L1 proposal [E2a] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-061` |
| RUN_ID | `INC-069-epic-1-RWB-E1-061` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Build order | 69 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-059 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built from the stored shadow results**, so that **the risk and model risk officer approves the step to L1 on measured results**.

**Business outcome:** The step from shadow to L1 puts agent output in front of case owners, so the approver needs the agreement rate, the failure types, the cost and the latency on a stated sample before deciding. This story produces that report from the evaluation run of RWB-E1-059 and holds the L1 proposal as a versioned policy row with its conditions, fallback and measures to watch (REQ-DRI-010), approved and dated like any other reference row (REQ-DRI-011). Nothing goes to L1 until RW-RISK approves the row.

**Main flow:**
1. RW-COE: requests the report for the evaluation run through GET /admin/agent-evaluations/{evaluationId}/report.
2. System: builds the report from the stored runs and scores: sample size, agreement rate per gap type, failure counts by type, total and per-case cost, median and 95th percentile latency, policy, prompt and model versions.
3. RW-COE: exports the report as CSV and PDF for the steering committee pack.
4. RW-COE: loads policy "INTAKE" version "P2" with autonomy mode L1, the evaluation run ID, the conditions, the fallback and the measures to watch through POST /admin/agent-configs.
5. System: checks that the evaluation run is DONE, that its scores meet every stated condition and that the fallback and measures are present; stores the version as LOADED.
6. RW-RISK: approves version "P2" with a valid from date through POST /admin/agent-configs/{versionId}/approve after the committee agrees.

**Acceptance criteria:**
- AC1: Report
- AC2: Proposal
- AC3: Report on an unfinished evaluation
- AC4: A proposal without its measures
- AC5: Scores below a stated condition
- AC6: Sample below the minimum
- AC7: The loader cannot approve the proposal

**Out of scope:**
- Showing the intake summary to case owners at L1 (RWB-E2-028).
- Changing an autonomy level from a screen (FEAT-AGT-12, Epic 3).
- The steering committee meeting itself and its minutes.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-061-intake-agent-evaluation-and-l1-proposal-e2a-v1.md` |
| Requirement IDs | REQ-DRI-010, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.7 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Requests and exports the report; loads the proposal (Rules and parameters CRUD) |
| RW-RISK | Reads the report; approves the proposal (Rules and parameters A) |
| RW-AUDIT | Reads the report and the versions (Rules and parameters R) |
| Approval levels | No delegation of authority level applies |

## Contract extract

**GET /api/recovery/v1/admin/agent-evaluations/{evaluationId}/report** (new, see additions) - Request: path runId (uuid); Accept application/json, text/csv or application/pdf. - Response: 200 AgentEvaluationReport (agent, sampleSize, versions, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms). - Errors: 401; 403; 404 unknown run; 409 run not DONE (MSG-P10-008); 503. - Authorization: Rules and parameters, R. Idempotency: read only; the same run gives the same report. **POST /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): kind POLICY, agent "INTAKE"; this story adds the L1 checks (BR1 to BR3); 201 AgentConfigVersion; errors 401, 403, 409, 422 (MSG-P10-001), 503; Rules and parameters C. **POST /api/recovery/v1/admin/agent-configs/{versionId}/approve** (new): 200; errors 401, 403, 404, 409 (MSG-P7-002, MSG-GEN-004), 503; Rules and paramet…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: conditions, measures and the minimum sample are row values. - No personal data in logs, tests or the report; the report holds counts and rates only. - No read of another module's tables. - A proposal never changes the mode in force before it is approved and its valid from date is reached.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-061-intake-agent-evaluation-and-l1-proposal-e2a-v1.md` |
| Specification | `output/INC-069-epic-1-RWB-E1-061/specify/spec.md` |
| Compliance validation | `output/INC-069-epic-1-RWB-E1-061/specify/compliance-validation.md` |
| Agent run log | `output/INC-069-epic-1-RWB-E1-061/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-069-epic-1-RWB-E1-061/plan/` |
| Implementation evidence | `output/INC-069-epic-1-RWB-E1-061/implement/` |
| API / functional test reports | `output/INC-069-epic-1-RWB-E1-061/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-069-epic-1-RWB-E1-061/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-061-intake-agent-evaluation-and-l1-proposal-e2a-v1.md` |
| Output run | `output/INC-069-epic-1-RWB-E1-061/` |

