# Increment Card — INC-065-epic-1-RWB-E1-059

**RWB-E1-059 — Case intake agent in shadow [E1b]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-065` |
| Title | Case intake agent in shadow [E1b] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-059` |
| RUN_ID | `INC-065-epic-1-RWB-E1-059` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-030, RWB-E1-058, RWB-TE-013 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode**, so that **the agent is scored against the business analysts' review before any case owner sees its output**.

**Main flow:**
1. SY-CASEWF: creates case "RW-2026-000301" and writes EV-01 CaseCreated to the outbox.
2. System (IntakeShadowListener): receives the event and calls the orchestrator for agent "INTAKE" with key "INTAKE:<caseId>:<businessDate>".
3. System: reads the case, accounts, documents, valuations and contact points through the tool gateway as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer (schema, tools, floor) and stores the summary and gap flags on the agent run with mode SHADOW.
5. System: publishes EV-28 AgentRunCompleted; no screen and no case field changes.
6. RW-COE: starts the evaluation of "INTAKE" on sample "INTAKE-S1" through POST /admin/agent-evaluations.

**Out of scope:**
- The evaluation report and the L1 proposal (RWB-E1-061).
- Showing the summary to the case owner (RWB-E2-028, Epic 3).
- Document classification and field extraction (RWB-E1-053, RWB-E1-060).

**Business outcome and value hypothesis:** A case owner who takes over a case at day 90 reads every account, document and appraisal to find what is missing before deciding the next step. The intake agent prepares that summary and the list of gaps. In Epic 1 it runs in shadow only: its output is stored, compared with the business analysts' review of the same 200 cases and shown to nobody, so the step to autonomy level 1 in RWB-E2-028 is decided on a measured agreement rate. Inputs are masked before the model call (REQ-ACA-005) and the agent reads data as SY-AGENT (REQ-ACA-010).

**Constraints and guardrails:**
- No business value in code: gap types, prompt, timeout and floor are versioned rows.
- No personal data in logs, tests or prompts; the summary holds masking tokens only.
- No read of another module's tables; inputs come through the P1, P3 and P5 interfaces.
- No shadow output in any user-facing response.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 059 Case intake agent in shadow E1b v1.md` |
| Requirement IDs | REQ-ACA-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.4 |
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
| SY-AGENT | Reads case, accounts, documents, valuations and contact points (Case record R, Documents R) |
| SY-CASEWF | Publishes CaseCreated |
| RW-COE | Loads the labeled sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK | Reads scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |
| RW-CASEOWN | Sees nothing from this story |

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
- **Critical path:** Yes; **depends on:** RWB-E1-030, RWB-E1-058, RWB-TE-013.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: gap types, prompt, timeout and floor are versioned rows.
  - No personal data in logs, tests or prompts; the summary holds masking tokens only.
  - No read of another module's tables; inputs come through the P1, P3 and P5 interfaces.
  - No shadow output in any user-facing response.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 059 Case intake agent in shadow E1b v1.md` |
| Specification | `output/INC-065-epic-1-RWB-E1-059/specify/spec.md` |
| Compliance validation | `output/INC-065-epic-1-RWB-E1-059/specify/compliance-validation.md` |
| Agent run log | `output/INC-065-epic-1-RWB-E1-059/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-065-epic-1-RWB-E1-059/plan/` (TBC) |
| Implementation evidence | `output/INC-065-epic-1-RWB-E1-059/implement/` (TBC) |
| API / functional test reports | `output/INC-065-epic-1-RWB-E1-059/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-065-epic-1-RWB-E1-059/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-065-epic-1-RWB-E1-059/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 059 Case intake agent in shadow E1b v1.md` |
| Output run | `output/INC-065-epic-1-RWB-E1-059/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
