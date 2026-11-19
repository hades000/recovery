# Increment Card — INC-039-epic-1-RWB-E1-058

**RWB-E1-058 — Agent platform set-up [E1a]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-039` |
| Title | Agent platform set-up [E1a] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-058` |
| RUN_ID | `INC-039-epic-1-RWB-E1-058` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-001, RWB-E1-003, RWB-E1-037 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **the model gateway, the prompt and policy store, the guardrail checker and the evaluation harness deployed in the recovery module**, so that **every Workbench agent is built, called, checked and scored through one path with its versions recorded**.

**Main flow:**
1. RW-COE: loads a prompt file and a policy file for agent "INTAKE" through POST /admin/agent-configs.
2. System: validates each file, stores it as a new version with status "LOADED" and keeps every earlier version readable.
3. RW-RISK: approves the version through POST /admin/agent-configs/{versionId}/approve; the version takes effect on its valid from date.
4. Calling step (any module, through RWB-TE-013): asks the orchestrator to run agent "INTAKE" for one case with an idempotency key.
5. System: reads the approved policy and prompt in force, reads the inputs through the tool gateway, masks personal fields through the P4 masking service and calls the model endpoint with the policy timeout.
6. System: runs the guardrail checker on the answer: output schema, allowed tool list and confidence floor.

**Out of scope:**
- The rule fallback inside a case step and the decision log entry for that step (RWB-TE-013).
- The case intake agent (RWB-E1-059), the extraction evaluation (RWB-E1-060) and the deviation screening agent (RWB-E1-062).
- The monitoring dashboard and cost alert (RWB-E1-063, RWB-E2-031).
- Changing an autonomy level through a screen (FEAT-AGT-12, Epic 3) and drift detection (FEAT-AGT-13, Epic 3).
- The choice of model endpoint (DL33).

**Business outcome and value hypothesis:** Officers gather and check case facts by hand before every decision, and no agent can help until there is one controlled way to call a model. This story gives every later agent the same gateway, the same versioned prompts and policies, the same output checks and the same scoring, so that an agent runs under a service identity (REQ-ACA-010), sees only masked personal data (REQ-ACA-005) and reads every threshold from a versioned row (REQ-DRI-010). The measure is the agent fallback rate, target below 10 percent per month, read from the agent run table.

**Constraints and guardrails:**
- No business value in code: model, prompt, timeout, confidence floor, tool list, price and cap are read from approved version rows.
- No personal data in logs, tests or prompts; test data is synthetic in DEV and masked in SIT.
- No read of another module's tables; case and document facts come through the P3 and P5 published interfaces.
- The model endpoint is reached only through ModelGatewayClient and only on the private endpoint.
- Prompt text and model answers never appear in the application log or in an API response of this story.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 058 Agent platform set up E1a v1.md` |
| Requirement IDs | REQ-ACA-010, REQ-ACA-005, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
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
| RW-COE, center of excellence analyst | Loads prompt, policy and sample files; starts evaluations; reads versions and scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves prompt and policy versions (Rules and parameters A); reads scores |
| RW-PLATADM, platform administrator | Reads agent runs (Platform administration CRUD; R used here); runs the gateway configuration per environment |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs (Platform administration R) |
| SY-AGENT, agent platform | Runs agents; reads case, documents and reference data through the tool gateway (R) |
| Approval levels | No delegation of authority level applies; the approval is the Rules and parameters A right |

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
- **Critical path:** No; **depends on:** RWB-E1-001, RWB-E1-003, RWB-E1-037.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: model, prompt, timeout, confidence floor, tool list, price and cap are read from approved version rows.
  - No personal data in logs, tests or prompts; test data is synthetic in DEV and masked in SIT.
  - No read of another module's tables; case and document facts come through the P3 and P5 published interfaces.
  - The model endpoint is reached only through ModelGatewayClient and only on the private endpoint.
  - Prompt text and model answers never appear in the application log or in an API response of this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 058 Agent platform set up E1a v1.md` |
| Specification | `output/INC-039-epic-1-RWB-E1-058/specify/spec.md` |
| Compliance validation | `output/INC-039-epic-1-RWB-E1-058/specify/compliance-validation.md` |
| Agent run log | `output/INC-039-epic-1-RWB-E1-058/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-039-epic-1-RWB-E1-058/plan/` (TBC) |
| Implementation evidence | `output/INC-039-epic-1-RWB-E1-058/implement/` (TBC) |
| API / functional test reports | `output/INC-039-epic-1-RWB-E1-058/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-039-epic-1-RWB-E1-058/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-039-epic-1-RWB-E1-058/specify/compliance-validation.md`) |
| Acceptance criteria | 15 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 058 Agent platform set up E1a v1.md` |
| Output run | `output/INC-039-epic-1-RWB-E1-058/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
