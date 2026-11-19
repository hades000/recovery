# Increment Card — INC-041-epic-1-RWB-TE-013

**RWB-TE-013 — Agent runtime client with fallback**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-041` |
| Title | Agent runtime client with fallback |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-013` |
| RUN_ID | `INC-041-epic-1-RWB-TE-013` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-TE-007, RWB-E1-058, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result**, so that **agents are added to a case step without changing the case flow, and every step records what the agent did**.

**Main flow:**
1. Calling step (for example SY-CASEWF): evaluates its rule and builds the rule result (rule ID, rule version, next state).
2. Calling step: calls AgentStepClient.runStep with the agent code, case ID, decision code, step key and rule result.
3. Client: reads the autonomy mode from the agent policy in force; if it is OFF or the flag is off, it skips the agent.
4. Client: calls AgentOrchestrator.run with the idempotency key built from the step key and waits at most timeout_seconds.
5. Client: in SHADOW mode, keeps the rule result as the applied result and records the agent answer only.
6. Client: in L1 mode, keeps the rule result as the applied result and returns the checked agent answer as the recommendation for the person who decides.

**Out of scope:**
- The orchestrator, gateway and guardrail checker (RWB-E1-058).
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029).

**Business outcome and value hypothesis:** A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The client puts every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

**Constraints and guardrails:**
- No business value in code: mode and timeout come from the approved agent policy.
- No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced.
- No read of another module's tables; the decision log is written only through the P7 interface.
- The client never applies an agent answer as the case result in SHADOW or L1.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 013 Agent runtime client with fallback v1.md` |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 |
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
| SY-CASEWF and other calling module identities | Call AgentStepClient; write the decision log entry through P7 (Decision log C) |
| SY-AGENT | Runs the agent and its tools (read only) |
| SY-DECLOG | Writes the entry |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through GET /admin/agent-runs (Platform administration R) |

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
- **Critical path:** No; **depends on:** RWB-TE-007, RWB-E1-058, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: mode and timeout come from the approved agent policy.
  - No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced.
  - No read of another module's tables; the decision log is written only through the P7 interface.
  - The client never applies an agent answer as the case result in SHADOW or L1.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 013 Agent runtime client with fallback v1.md` |
| Specification | `output/INC-041-epic-1-RWB-TE-013/specify/spec.md` |
| Compliance validation | `output/INC-041-epic-1-RWB-TE-013/specify/compliance-validation.md` |
| Agent run log | `output/INC-041-epic-1-RWB-TE-013/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-041-epic-1-RWB-TE-013/plan/` (TBC) |
| Implementation evidence | `output/INC-041-epic-1-RWB-TE-013/implement/` (TBC) |
| API / functional test reports | `output/INC-041-epic-1-RWB-TE-013/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-041-epic-1-RWB-TE-013/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-041-epic-1-RWB-TE-013/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 013 Agent runtime client with fallback v1.md` |
| Output run | `output/INC-041-epic-1-RWB-TE-013/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
