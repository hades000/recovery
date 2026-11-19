# Increment Card — INC-071-epic-1-RWB-E1-063

**RWB-E1-063 — Agent monitoring dashboard v1 [E2c]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-071` |
| Title | Agent monitoring dashboard v1 [E2c] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-063` |
| RUN_ID | `INC-071-epic-1-RWB-E1-063` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Should |
| Build order | 71 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-061, RWB-E1-007, RWB-E1-014, RWB-E1-058 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **risk and model risk officer (RW-RISK)**, I want **a dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and an alert when an agent's daily cost passes its limit**, so that **every agent is watched from its first shadow run**.

**Business outcome:** An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week, not at the L1 review. This story copies daily agent run figures to the data lake with the nightly reporting extract, matched by row count (REQ-DRI-009), so the Power BI dashboard reads the copy and not the live tables. A daily check sends an alert when the cost of an agent on a business date is above its policy limit.

**Main flow:**
1. JOB-15 Reporting extract: at 01:30 calls the P10 step AgentRunExtractStep for the previous business date.
2. System: groups the agent runs of that date by agent, policy version, prompt version and model version: runs, answered, fallback, median and 95th percentile latency, tokens and cost.
3. System: adds the latest DONE evaluation score per agent and version.
4. System: writes the rows to the data lake table agent_run_daily and checks that the row count and the sum of runs match the source.
5. System: compares each agent's cost for the date with daily_cost_cap_thb of its policy; for each breach writes one agent alert and sends MSG-P10-004 through the P6 notification interface to the alert role and to RW-RISK.
6. RW-RISK: opens the Power BI report "Agent monitor v1" and reads each agent by version and date.

**Acceptance criteria:**
- AC1: Per agent
- AC2: Alert
- AC3: A copy that does not match is held
- AC4: A rerun for the same date
- AC5: An agent with no runs
- AC6: Cost equal to the cap
- AC7: The notification path is down

**Out of scope:**
- Acceptance and override per segment, drift alerts and the SCR-46 agent monitor screen (RWB-E2-031).
- Drift detection with a raised decision (FEAT-AGT-13, Epic 3).
- The steering dashboard (RWB-E2-009).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-063-agent-monitoring-dashboard-v1-e2c-v1.md` |
| Requirement IDs | REQ-DRI-009 |
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
| RW-RISK | Reads the dashboard (Reporting R); receives alerts |
| RW-COE | Reads the dashboard (Reporting R); receives alerts as the policy alert role |
| RW-BIANAL | Builds and maintains the Power BI report (Reporting CRUD) |
| RW-PLATADM | Reruns JOB-15 (Platform administration U through POST /admin/jobs/{jobId}/rerun) |
| RW-DATASTEW | Receives the count mismatch alert |

## Contract extract

**Job:** JOB-15 Reporting extract (batch.txt), nightly 01:30 Asia/Bangkok. This story adds step "agentRunDaily" after the existing steps. - Trigger: Quartz schedule of JOB-15; manual rerun through POST /admin/jobs/{jobId}/rerun. - Input: agent_run rows with run_at on the business date; agent_policy in force; latest DONE agent_evaluation per agent and version. - Output: data lake table agent_run_daily (business_date, agent_code, policy_version, prompt_version, model_version, runs, answered, fallback, latency_p50_ms, latency_p95_ms, tokens, cost_thb, eval_score); agent_alert rows. - Events published: none from events.txt; alerts go through the P6 notification interface and the outbox (JOB-11 Outbox sender). - Idempotency key: business_date for the data lake rows (replace); agent_code, alert_type, segment and business_date for alerts. - Restart: the step restarts from the start for the dat…

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

- No business value in code: caps and alert roles come from the agent policy. - No personal data in logs, tests, the data lake table or the alert; rows hold counts, times and amounts only. - No read of another module's tables; JOB-15 calls the P10 interface. - The dashboard never reads the live agent tables.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-063-agent-monitoring-dashboard-v1-e2c-v1.md` |
| Specification | `output/INC-071-epic-1-RWB-E1-063/specify/spec.md` |
| Compliance validation | `output/INC-071-epic-1-RWB-E1-063/specify/compliance-validation.md` |
| Agent run log | `output/INC-071-epic-1-RWB-E1-063/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-071-epic-1-RWB-E1-063/plan/` |
| Implementation evidence | `output/INC-071-epic-1-RWB-E1-063/implement/` |
| API / functional test reports | `output/INC-071-epic-1-RWB-E1-063/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-071-epic-1-RWB-E1-063/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-063-agent-monitoring-dashboard-v1-e2c-v1.md` |
| Output run | `output/INC-071-epic-1-RWB-E1-063/` |

