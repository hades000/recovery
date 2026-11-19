# Increment Card — INC-050-epic-1-RWB-E1-031

**RWB-E1-031 — Queue and owner on the case list with filters**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-050` |
| Title | Queue and owner on the case list with filters |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-031` |
| RUN_ID | `INC-050-epic-1-RWB-E1-031` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-020, RWB-E1-039 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **the queue and owner columns on the case list, with filters by queue, team and status and an export to Excel**, so that **I see my queues and who owns each case without a new screen**.

**Main flow:**
1. Team manager: opens SCR-02 Case list; the screen shows the Loading state.
2. CaseListPage: calls GET /cases with page 0 and size 50; the service applies the caller's scope.
3. CaseListPage: shows each row with case number, product, status, stage, queue, owner and entry date (list state).
4. Team manager: picks queue "DIL-BKK-CO", team "DIL-BKK" and status "ASSIGNED"; the page calls GET /cases with the filters (filtered state).
5. CaseQueryService: returns only cases inside the caller's scope that meet every filter, with the total.
6. Team manager: chooses Export.

**Out of scope:**
- My queue and team queue screens (RWB-E2-011, SCR-07 in Epic 2).
- The base case list with filters by product, stage, age and deviation (RWB-E1-002, FEAT-RDF-18).
- The masking rules themselves (RWB-E1-037, DL26).

**Business outcome and value hypothesis:** Today a team manager asks each collector for their list to know who holds which case. With allocation by rule (RWB-E1-020), every case has a queue and an owner; this story shows both on the case list, filters by queue, team and status inside the manager's scope, and exports the filtered list with the export written to the access log for PDPA. It meets REQ-CWC-007 (the result of allocation is visible) and REQ-ACA-009 (a user sees only the cases their scope allows).

**Constraints and guardrails:**
- No business value in code: the export limit and the lists come from data.
- No personal data in logs, tests or prompts; the export applies masking by role and holds no customer name or ID number.
- No read of another module's tables: the access log is written through AccessEventPublisher (P4); owner names come from the ACE user directory interface.
- The export is never made when its access log entry cannot be written.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 031 Queue and owner on the case list with filters v1.md` |
| Requirement IDs | REQ-CWC-007, REQ-ACA-009 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
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
| RW-TEAMMGR | Lists, filters and exports cases in team scope (Case record R) |
| RW-CASEOWN | Lists and exports their own cases (Case record R, scope Own) |
| Every role with Case record R | Lists cases in its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| RW-COMPLY | Reads the access log entries for exports |

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
- **Feature flag:** `rwb.p3.caselistqueue`. Off: the list hides the queue and owner columns and the export.
- **Critical path:** No; **depends on:** RWB-E1-020, RWB-E1-039.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the export limit and the lists come from data.
  - No personal data in logs, tests or prompts; the export applies masking by role and holds no customer name or ID number.
  - No read of another module's tables: the access log is written through AccessEventPublisher (P4); owner names come from the ACE user directory interface.
  - The export is never made when its access log entry cannot be written.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 031 Queue and owner on the case list with filters v1.md` |
| Specification | `output/INC-050-epic-1-RWB-E1-031/specify/spec.md` |
| Compliance validation | `output/INC-050-epic-1-RWB-E1-031/specify/compliance-validation.md` |
| Agent run log | `output/INC-050-epic-1-RWB-E1-031/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-050-epic-1-RWB-E1-031/plan/` (TBC) |
| Implementation evidence | `output/INC-050-epic-1-RWB-E1-031/implement/` (TBC) |
| API / functional test reports | `output/INC-050-epic-1-RWB-E1-031/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-050-epic-1-RWB-E1-031/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-050-epic-1-RWB-E1-031/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 031 Queue and owner on the case list with filters v1.md` |
| Output run | `output/INC-050-epic-1-RWB-E1-031/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
