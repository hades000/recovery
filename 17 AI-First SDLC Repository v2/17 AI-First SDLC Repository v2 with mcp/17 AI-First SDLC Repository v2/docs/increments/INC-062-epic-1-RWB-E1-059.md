# Increment Card — INC-062-epic-1-RWB-E1-059

**RWB-E1-059 — Case intake agent in shadow [E1b]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-062` |
| Title | Case intake agent in shadow [E1b] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-059` |
| RUN_ID | `INC-062-epic-1-RWB-E1-059` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Build order | 62 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-030, RWB-E1-058, RWB-TE-013 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode**, so that **the agent is scored against the business analysts' review before any case owner sees its output**.

**Business outcome:** A case owner who takes over a case at day 90 reads every account, document and appraisal to find what is missing before deciding the next step. The intake agent prepares that summary and the list of gaps. In Epic 1 it runs in shadow only: its output is stored, compared with the business analysts' review of the same 200 cases and shown to nobody, so the step to autonomy level 1 in RWB-E2-028 is decided on a measured agreement rate. Inputs are masked before the model call (REQ-ACA-005) and the agent reads data as SY-AGENT (REQ-ACA-010).

**Main flow:**
1. SY-CASEWF: creates case "RW-2026-000301" and writes EV-01 CaseCreated to the outbox.
2. System (IntakeShadowListener): receives the event and calls the orchestrator for agent "INTAKE" with key "INTAKE:<caseId>:<businessDate>".
3. System: reads the case, accounts, documents, valuations and contact points through the tool gateway as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer (schema, tools, floor) and stores the summary and gap flags on the agent run with mode SHADOW.
5. System: publishes EV-28 AgentRunCompleted; no screen and no case field changes.
6. RW-COE: starts the evaluation of "INTAKE" on sample "INTAKE-S1" through POST /admin/agent-evaluations.

**Acceptance criteria:**
- AC1: Shadow run
- AC2: Agreement rate
- AC3: A new case starts one shadow run
- AC4: A failed run is counted and not retried
- AC5: Stale input is flagged
- AC6: A repeated event has no further effect
- AC7: Partly labeled sample
- AC8: Empty sample

**Out of scope:**
- The evaluation report and the L1 proposal (RWB-E1-061).
- Showing the summary to the case owner (RWB-E2-028, Epic 3).
- Document classification and field extraction (RWB-E1-053, RWB-E1-060).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-059-case-intake-agent-in-shadow-e1b-v1.md` |
| Requirement IDs | REQ-ACA-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.4 |
| Decision | D6 entry |
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
| SY-AGENT | Reads case, accounts, documents, valuations and contact points (Case record R, Documents R) |
| SY-CASEWF | Publishes CaseCreated |
| RW-COE | Loads the labeled sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK | Reads scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |
| RW-CASEOWN | Sees nothing from this story |

## Contract extract

**Event consumed:** EV-01 CaseCreated (caseId, caseNo, productGroup, accounts, businessDate). Listener is idempotent on the event ID and on the run key "INTAKE:<caseId>:<businessDate>". **Event published:** EV-28 AgentRunCompleted (runId, agent "INTAKE", caseId, outcome, fallback). **Tools on the allowed list** (each calls a published interface as SY-AGENT): read_case (P3 CaseQueryService.getCase), read_accounts (P3 CaseQueryService.getAccounts), read_documents (P5 DocumentQueryService.listByCase), read_valuations (P1 CollateralQueryService.listValuations), read_contact_points (P3 CaseQueryService.getContactPoints). **Output schema "intake-summary-v1":** summary (string, at most 1,500 characters, masked tokens only), gaps (array of {gapType from the enum, reason, sourceRef}), confidence (0 to 1). **POST /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): request agent "INTAKE"…

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

- No business value in code: gap types, prompt, timeout and floor are versioned rows. - No personal data in logs, tests or prompts; the summary holds masking tokens only. - No read of another module's tables; inputs come through the P1, P3 and P5 interfaces. - No shadow output in any user-facing response.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-059-case-intake-agent-in-shadow-e1b-v1.md` |
| Specification | `output/INC-062-epic-1-RWB-E1-059/specify/spec.md` |
| Compliance validation | `output/INC-062-epic-1-RWB-E1-059/specify/compliance-validation.md` |
| Agent run log | `output/INC-062-epic-1-RWB-E1-059/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-062-epic-1-RWB-E1-059/plan/` |
| Implementation evidence | `output/INC-062-epic-1-RWB-E1-059/implement/` |
| API / functional test reports | `output/INC-062-epic-1-RWB-E1-059/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-062-epic-1-RWB-E1-059/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-059-case-intake-agent-in-shadow-e1b-v1.md` |
| Output run | `output/INC-062-epic-1-RWB-E1-059/` |

