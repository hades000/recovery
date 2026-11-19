# Increment Card — INC-062-epic-1-RWB-E1-035

**RWB-E1-035 — Case record view v1.1 with documents and history timeline**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-062` |
| Title | Case record view v1.1 with documents and history timeline |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-035` |
| RUN_ID | `INC-062-epic-1-RWB-E1-035` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-021, RWB-E1-023, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **a timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order, each with who or which rule caused it**, so that **I see what happened to the case without asking anyone**.

**Main flow:**
1. Case owner: opens SCR-03 for case RW-2026-000801 and selects the Timeline panel.
2. TimelinePanel: calls GET /cases/{caseId}/timeline with page 0 and size 50.
3. CaseAndWorkflowController: checks Case record R and the scope.
4. TimelineService: reads interactions and assignments from P3 tables, documents through the P5 interface and decision log entries through the P7 interface, for the case.
5. TimelineService: maps each record to a TimelineItem with time, type, summary, by and reference.
6. TimelineService: sorts by time, then by a fixed type order for equal times, then by record ID, and returns the page with the total.

**Out of scope:**
- The full timeline screen with filters and queue history (RWB-E2-016).
- The full case record view with collateral, decisions and timers (Epic 2, FEAT-WKM-08).
- Communications and notices on the timeline (Epic 2, P6).

**Business outcome and value hypothesis:** A case that changes owner today arrives with no history except what the last owner remembers. This story adds a timeline panel to SCR-03 that merges the interaction ledger, the documents, the assignments and the decision log entries for the case in time order, and shows the person or the rule and version behind each event, including the coded reason of a manual transfer. It meets REQ-CWC-016 (every workflow event carries its rule ID and version, now visible) and REQ-OCC-007 (contact history and documents on the case view).

**Constraints and guardrails:**
- No business value in code: the type order and labels are data.
- No personal data in logs, tests or prompts; contact summaries follow masking by role.
- No read of another module's tables: documents through DocumentQuery (P5), decisions through DecisionLogQuery (P7).
- The timeline never writes; it shows records as they were written.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 035 Case record view v1 1 with documents and history timeline v1.md` |
| Requirement IDs | REQ-CWC-016, REQ-OCC-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.6; Business Requirements Program, sections 5.3 and 5.6 |
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
| RW-CASEOWN | Reads the timeline of own cases (Case record R) |
| RW-TEAMMGR | Reads the timeline of team cases |
| RW-CONDUCT, RW-AUDIT | Read the timeline of every case |
| RW-REFADM | No Case record right; refused |

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
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p3.timeline`. Off: SCR-03 hides the Timeline panel and the endpoint returns 404.
- **Critical path:** No; **depends on:** RWB-E1-021, RWB-E1-023, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the type order and labels are data.
  - No personal data in logs, tests or prompts; contact summaries follow masking by role.
  - No read of another module's tables: documents through DocumentQuery (P5), decisions through DecisionLogQuery (P7).
  - The timeline never writes; it shows records as they were written.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 035 Case record view v1 1 with documents and history timeline v1.md` |
| Specification | `output/INC-062-epic-1-RWB-E1-035/specify/spec.md` |
| Compliance validation | `output/INC-062-epic-1-RWB-E1-035/specify/compliance-validation.md` |
| Agent run log | `output/INC-062-epic-1-RWB-E1-035/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-062-epic-1-RWB-E1-035/plan/` (TBC) |
| Implementation evidence | `output/INC-062-epic-1-RWB-E1-035/implement/` (TBC) |
| API / functional test reports | `output/INC-062-epic-1-RWB-E1-035/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-062-epic-1-RWB-E1-035/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-062-epic-1-RWB-E1-035/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 035 Case record view v1 1 with documents and history timeline v1.md` |
| Output run | `output/INC-062-epic-1-RWB-E1-035/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
