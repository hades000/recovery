# Increment Card — INC-043-epic-1-RWB-E1-062

**RWB-E1-062 — Deviation screening agent in shadow [E2b]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-043` |
| Title | Deviation screening agent in shadow [E2b] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-062` |
| RUN_ID | `INC-043-epic-1-RWB-E1-062` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Build order | 43 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-058, RWB-TE-013 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the deviation screening agent to propose X1 to X7 with reasons from case data, call notes and documents, in shadow on Epic 1 cases**, so that **the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type**.

**Business outcome:** A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the interaction ledger and the documents at entry and when a document arrives, and proposes deviations with reasons. In Epic 1 the proposals are stored only, scored against the business analysts' review and shown to nobody. The story measures detection from case data, call notes and documents (REQ-DVH-001), the named owner each code would route to (REQ-DVH-003) and the contact that preceded a complaint (REQ-DVH-007).

**Main flow:**
1. SY-CASEWF or P5: writes EV-01 CaseCreated for a new case, or EV-16 DocumentStored for a document on an open case.
2. System (ScreeningShadowListener): calls the orchestrator for agent "SCREENING" with key "SCREENING:<caseId>:<eventId>".
3. System: reads the case, the interaction ledger entries, the documents and their fields as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer: each proposal has a code in X1 to X7, reasons, source references and a confidence.
5. System: reads the owner role each proposed code routes to from the rule catalog (RuleCatalog, RWB-E1-072) (R-DEV-02 to R-DEV-06) and stores it with the proposal.
6. System: marks proposals below the confidence floor as "review"; stores everything on the agent run in mode SHADOW. No deviation record, contact stop or clock change is made.

**Acceptance criteria:**
- AC1: Shadow flags
- AC2: Compared
- AC3: A new document starts a run
- AC4: The owner role comes from the rule rows
- AC5: A complaint names the contact before it
- AC6: A low-confidence proposal is marked for review
- AC7: A repeated event
- AC8: A code outside the list
- AC9: Timeout

**Out of scope:**
- Showing proposals to the owner and raising the deviation at L1 on one segment (RWB-E2-029).
- Raising, routing and clearing a deviation (RWB-E2-015, S8).
- The full deviation flows (Epic 7).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-062-deviation-screening-agent-in-shadow-e2b-v1.md` |
| Requirement IDs | REQ-DVH-001, REQ-DVH-003, REQ-DVH-007 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.15 |
| Decision | X1 to X7 |
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
| SY-AGENT | Reads case, interactions, documents and fields (Case record R, Documents R) |
| SY-RULES | Evaluates R-DEV-02 to R-DEV-06 for the owner role |
| RW-COE | Loads the sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK, RW-CONDUCT | Read scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |

## Contract extract

**Events consumed:** EV-01 CaseCreated and EV-16 DocumentStored (documentId, caseId, type, source); idempotent on event ID. **Event published:** EV-28 AgentRunCompleted (runId, agent "SCREENING", caseId, outcome, fallback). **Output schema "screening-v1":** proposals (array of {code in X1..X7, reasons (array of strings, masked), sourceRefs (interaction or document IDs), precedingContactId (X1 only), confidence}). **Interfaces called:** P3 CaseQueryService.getCase, P7 InteractionLedgerReader.list(caseId, from, to), P5 DocumentQueryService.listByCase and getFields, P3 RuleEvaluator.ownerFor(routeSet "Deviations", event "OWNER_ASSIGNED", deviationCode); all as SY-AGENT or SY-RULES. **POST /api/recovery/v1/admin/agent-evaluations** and **GET /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): agent "SCREENING", sample "SCREEN-S1"; Rules and parameters C and R; errors 401, 403, 409…

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

- No business value in code: codes, owner roles, floor and look-back are data rows. - No personal data in logs, tests or prompts; call note summaries are masked before the model call. - No read of another module's tables; ledger, case, documents and rules come through their interfaces. - The agent never calls the S8 deviation service in shadow mode.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-062-deviation-screening-agent-in-shadow-e2b-v1.md` |
| Specification | `output/INC-043-epic-1-RWB-E1-062/specify/spec.md` |
| Compliance validation | `output/INC-043-epic-1-RWB-E1-062/specify/compliance-validation.md` |
| Agent run log | `output/INC-043-epic-1-RWB-E1-062/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-043-epic-1-RWB-E1-062/plan/` |
| Implementation evidence | `output/INC-043-epic-1-RWB-E1-062/implement/` |
| API / functional test reports | `output/INC-043-epic-1-RWB-E1-062/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-043-epic-1-RWB-E1-062/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-062-deviation-screening-agent-in-shadow-e2b-v1.md` |
| Output run | `output/INC-043-epic-1-RWB-E1-062/` |

