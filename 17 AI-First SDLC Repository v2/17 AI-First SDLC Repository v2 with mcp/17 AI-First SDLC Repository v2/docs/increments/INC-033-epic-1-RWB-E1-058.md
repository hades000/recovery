# Increment Card — INC-033-epic-1-RWB-E1-058

**RWB-E1-058 — Agent platform set-up [E1a]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-033` |
| Title | Agent platform set-up [E1a] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-058` |
| RUN_ID | `INC-033-epic-1-RWB-E1-058` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Build order | 33 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-037 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **the model gateway, the prompt and policy store, the guardrail checker and the evaluation harness deployed in the recovery module**, so that **every Workbench agent is built, called, checked and scored through one path with its versions recorded**.

**Business outcome:** Officers gather and check case facts by hand before every decision, and no agent can help until there is one controlled way to call a model. This story gives every later agent the same gateway, the same versioned prompts and policies, the same output checks and the same scoring, so that an agent runs under a service identity (REQ-ACA-010), sees only masked personal data (REQ-ACA-005) and reads every threshold from a versioned row (REQ-DRI-010). The measure is the agent fallback rate, target below 10 percent per month, read from the agent run table.

**Main flow:**
1. RW-COE: loads a prompt file and a policy file for agent "INTAKE" through POST /admin/agent-configs.
2. System: validates each file, stores it as a new version with status "LOADED" and keeps every earlier version readable.
3. RW-RISK: approves the version through POST /admin/agent-configs/{versionId}/approve; the version takes effect on its valid from date.
4. Calling step (any module, through RWB-TE-013): asks the orchestrator to run agent "INTAKE" for one case with an idempotency key.
5. System: reads the approved policy and prompt in force, reads the inputs through the tool gateway, masks personal fields through the P4 masking service and calls the model endpoint with the policy timeout.
6. System: runs the guardrail checker on the answer: output schema, allowed tool list and confidence floor.

**Acceptance criteria:**
- AC1: Approved endpoint
- AC2: Prompt versions
- AC3: Schema check
- AC4: Evaluation suite
- AC5: Guardrails
- AC6: The model does not answer inside the timeout
- AC7: Personal data is masked before the model call
- AC8: A configuration file that fails a check is refused
- AC9: The loader cannot approve their own version
- AC10: An answer below the confidence floor falls back
- AC11: A repeated run request has no further effect
- AC12: Two approvals of one version at the same time
- AC13: An evaluation on an empty sample is refused
- AC14: A second evaluation while one is running is refused
- AC15: Agent runs are listed without their content

**Out of scope:**
- The rule fallback inside a case step and the decision log entry for that step (RWB-TE-013).
- The case intake agent (RWB-E1-059), the extraction evaluation (RWB-E1-060) and the deviation screening agent (RWB-E1-062).
- The monitoring dashboard and cost alert (RWB-E1-063, RWB-E2-031).
- Changing an autonomy level through a screen (FEAT-AGT-12, Epic 3) and drift detection (FEAT-AGT-13, Epic 3).
- The choice of model endpoint (DL33).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-058-agent-platform-set-up-e1a-v1.md` |
| Requirement IDs | REQ-ACA-010, REQ-ACA-005, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
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
| RW-COE, center of excellence analyst | Loads prompt, policy and sample files; starts evaluations; reads versions and scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves prompt and policy versions (Rules and parameters A); reads scores |
| RW-PLATADM, platform administrator | Reads agent runs (Platform administration CRUD; R used here); runs the gateway configuration per environment |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs (Platform administration R) |
| SY-AGENT, agent platform | Runs agents; reads case, documents and reference data through the tool gateway (R) |
| Approval levels | No delegation of authority level applies; the approval is the Rules and parameters A right |

## Contract extract

**GET /api/recovery/v1/admin/agent-runs** (API-P10-001, in api.yaml) - Request: query agent, from, to (dates, ISO 8601). - Response: 200, array of AgentRun (id, agent, agentVersion, caseId, outcome, fallback, latencyMs). outcome carries agent_run.status. agentVersion is "<agent>@<policy_version>/<prompt_version>", for example "ECHO@P1/PR1". - Errors: 401 no session (MSG-P4-001); 403 role without Platform administration R (MSG-P4-002); 503 store unavailable. - Authorization: Platform administration, R, scope applied. - Idempotency: not applicable (read). **GET /api/recovery/v1/admin/agent-configs** (new, see additions) - Request: query agent, kind (PROMPT or POLICY), status. - Response: 200, array of AgentConfigVersion (versionId, agent, kind, version, status, validFrom, validTo, loadedBy, approvedBy, bodyHash). - Errors: 401, 403, 503. Authorization: Rules and parameters, R. **POST /api…

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

- No business value in code: model, prompt, timeout, confidence floor, tool list, price and cap are read from approved version rows. - No personal data in logs, tests or prompts; test data is synthetic in DEV and masked in SIT. - No read of another module's tables; case and document facts come through the P3 and P5 published interfaces. - The model endpoint is reached only through ModelGatewayClient and only on the private endpoint. - Prompt text and model answers never appear in the application log or in an API response of this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-058-agent-platform-set-up-e1a-v1.md` |
| Specification | `output/INC-033-epic-1-RWB-E1-058/specify/spec.md` |
| Compliance validation | `output/INC-033-epic-1-RWB-E1-058/specify/compliance-validation.md` |
| Agent run log | `output/INC-033-epic-1-RWB-E1-058/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-033-epic-1-RWB-E1-058/plan/` |
| Implementation evidence | `output/INC-033-epic-1-RWB-E1-058/implement/` |
| API / functional test reports | `output/INC-033-epic-1-RWB-E1-058/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-033-epic-1-RWB-E1-058/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 15 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-058-agent-platform-set-up-e1a-v1.md` |
| Output run | `output/INC-033-epic-1-RWB-E1-058/` |

