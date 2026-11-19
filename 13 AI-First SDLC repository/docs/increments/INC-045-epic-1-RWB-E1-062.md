# Increment Card — INC-045-epic-1-RWB-E1-062

**RWB-E1-062 — Deviation screening agent in shadow [E2b]**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-045` |
| Title | Deviation screening agent in shadow [E2b] |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-062` |
| RUN_ID | `INC-045-epic-1-RWB-E1-062` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-058, RWB-TE-013 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P10 Agent runtime. **Build group:** P10.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the deviation screening agent to propose X1 to X7 with reasons from case data, call notes and documents, in shadow on Epic 1 cases**, so that **the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type**.

**Main flow:**
1. SY-CASEWF or P5: writes EV-01 CaseCreated for a new case, or EV-16 DocumentStored for a document on an open case.
2. System (ScreeningShadowListener): calls the orchestrator for agent "SCREENING" with key "SCREENING:<caseId>:<eventId>".
3. System: reads the case, the interaction ledger entries, the documents and their fields as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer: each proposal has a code in X1 to X7, reasons, source references and a confidence.
5. System: asks the rules component which owner role each proposed code routes to (R-DEV-02 to R-DEV-06) and stores it with the proposal.
6. System: marks proposals below the confidence floor as "review"; stores everything on the agent run in mode SHADOW. No deviation record, contact stop or clock change is made.

**Out of scope:**
- Showing proposals to the owner and raising the deviation at L1 on one segment (RWB-E2-029).
- Raising, routing and clearing a deviation (RWB-E2-015, S8).
- The full deviation flows (Epic 7).

**Business outcome and value hypothesis:** A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the interaction ledger and the documents at entry and when a document arrives, and proposes deviations with reasons. In Epic 1 the proposals are stored only, scored against the business analysts' review and shown to nobody. The story measures detection from case data, call notes and documents (REQ-DVH-001), the named owner each code would route to (REQ-DVH-003) and the contact that preceded a complaint (REQ-DVH-007).

**Constraints and guardrails:**
- No business value in code: codes, owner roles, floor and look-back are data rows.
- No personal data in logs, tests or prompts; call note summaries are masked before the model call.
- No read of another module's tables; ledger, case, documents and rules come through their interfaces.
- The agent never calls the S8 deviation service in shadow mode.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 062 Deviation screening agent in shadow E2b v1.md` |
| Requirement IDs | REQ-DVH-001, REQ-DVH-003, REQ-DVH-007 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.15 |
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
| SY-AGENT | Reads case, interactions, documents and fields (Case record R, Documents R) |
| SY-RULES | Evaluates R-DEV-02 to R-DEV-06 for the owner role |
| RW-COE | Loads the sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK, RW-CONDUCT | Read scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |

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
- **Critical path:** No; **depends on:** RWB-E1-058, RWB-TE-013.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: codes, owner roles, floor and look-back are data rows.
  - No personal data in logs, tests or prompts; call note summaries are masked before the model call.
  - No read of another module's tables; ledger, case, documents and rules come through their interfaces.
  - The agent never calls the S8 deviation service in shadow mode.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 062 Deviation screening agent in shadow E2b v1.md` |
| Specification | `output/INC-045-epic-1-RWB-E1-062/specify/spec.md` |
| Compliance validation | `output/INC-045-epic-1-RWB-E1-062/specify/compliance-validation.md` |
| Agent run log | `output/INC-045-epic-1-RWB-E1-062/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-045-epic-1-RWB-E1-062/plan/` (TBC) |
| Implementation evidence | `output/INC-045-epic-1-RWB-E1-062/implement/` (TBC) |
| API / functional test reports | `output/INC-045-epic-1-RWB-E1-062/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-045-epic-1-RWB-E1-062/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-045-epic-1-RWB-E1-062/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 062 Deviation screening agent in shadow E2b v1.md` |
| Output run | `output/INC-045-epic-1-RWB-E1-062/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
