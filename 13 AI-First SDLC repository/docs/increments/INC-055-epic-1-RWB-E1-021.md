# Increment Card — INC-055-epic-1-RWB-E1-021

**RWB-E1-021 — Transfer rules and engine v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-055` |
| Title | Transfer rules and engine v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-021` |
| RUN_ID | `INC-055-epic-1-RWB-E1-021` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-028, RWB-E1-020, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the transfer rule table on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without email**.

**Main flow:**
1. Event source: writes a trigger event to the outbox: CaseStateChanged for a stage change or a route decided (rule event ROUTE_APPROVED), TimerDue, DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored or PaymentMissed.
2. TransferListener: receives the event once per event ID; a repeated event ID is ignored (R-UNI-40).
3. TransferRuleEvaluator (SY-RULES): reads the transfer rows in force and returns the first row, in row order, whose trigger and condition match the case.
4. TransferService: skips an automated transfer when legal_hold is true (R-UNI-20) and logs the skip.
5. TransferService: locks the case by its version, picks the owner in the target queue with AssignmentEngine, and checks the move is allowed from the case status.
6. TransferService: in one transaction ends the open assignment, writes the new assignment (reason TRANSFER), updates queue, team and owner, and writes CaseTransferred (EV-04).

**Out of scope:**
- The transfer screen and queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap (Epic 2, R-UNI-18, R-UNI-19).
- Escalation of a breached timer without moving the case (RWB-E1-028).
- The route decision itself (Epic 4).

**Business outcome and value hypothesis:** A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. This story moves the case by rule when one of eight triggers fires, picks the owner in the receiving queue, ends the old assignment and records the rule and version, and gives the team manager a programmatic transfer with a coded reason before the Epic 2 screens. It meets REQ-CWC-010 and REQ-CWC-016.

**Constraints and guardrails:**
- No business value in code: triggers, target queues and the reason list are data.
- No personal data in logs, events, tests or prompts.
- No read of another module's tables: trigger events arrive through the outbox; rule rows through RuleTableReader (P4).
- A transfer never resets the stage clock or the prescription date.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 021 Transfer rules and engine v1 v1.md` |
| Requirement IDs | REQ-CWC-010, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
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
| RW-TEAMMGR | Transfers and reassigns cases in team scope (Queue and allocation U) |
| RW-CAPACITY | Transfers cases (Queue and allocation U) |
| RW-LITOFF and other roles with Case record U | Place and lift a legal hold on a Legal or court instruction (Case record U) |
| RW-CASEOWN | Reads the case; may not transfer (Queue and allocation R) |
| SY-RULES | Evaluates the transfer rows |
| SY-CASEWF | Carries out rule transfers (Queue and allocation CRU) |
| SY-DECLOG | Writes the entries |

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
- **Feature flag:** `rwb.p3.transfer`. Off: no rule transfers and the two endpoints return 404.
- **Critical path:** No; **depends on:** RWB-E1-028, RWB-E1-020, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: triggers, target queues and the reason list are data.
  - No personal data in logs, events, tests or prompts.
  - No read of another module's tables: trigger events arrive through the outbox; rule rows through RuleTableReader (P4).
  - A transfer never resets the stage clock or the prescription date.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 021 Transfer rules and engine v1 v1.md` |
| Specification | `output/INC-055-epic-1-RWB-E1-021/specify/spec.md` |
| Compliance validation | `output/INC-055-epic-1-RWB-E1-021/specify/compliance-validation.md` |
| Agent run log | `output/INC-055-epic-1-RWB-E1-021/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-055-epic-1-RWB-E1-021/plan/` (TBC) |
| Implementation evidence | `output/INC-055-epic-1-RWB-E1-021/implement/` (TBC) |
| API / functional test reports | `output/INC-055-epic-1-RWB-E1-021/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-055-epic-1-RWB-E1-021/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-055-epic-1-RWB-E1-021/specify/compliance-validation.md`) |
| Acceptance criteria | 14 ACs in the current story (AC1–AC14; AC4 is a Scenario Outline) |
| AC numbering | None — AC4 is a Scenario Outline in the current story |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 021 Transfer rules and engine v1 v1.md` |
| Output run | `output/INC-055-epic-1-RWB-E1-021/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
