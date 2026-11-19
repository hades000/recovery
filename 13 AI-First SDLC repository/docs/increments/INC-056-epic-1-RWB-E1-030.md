# Increment Card — INC-056-epic-1-RWB-E1-030

**RWB-E1-030 — Daily rebalancing and queue measures**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-056` |
| Title | Daily rebalancing and queue measures |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-030` |
| RUN_ID | `INC-056-epic-1-RWB-E1-030` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-020, RWB-E1-027, RWB-E1-028 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a daily job that assigns unassigned cases and moves the newest cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches published to Power BI**, so that **queues stay balanced and every team manager sees the same numbers as the case list**.

**Main flow:**
1. Quartz: starts JOB-06 at 06:30, or when JOB-03 completes for the business date if that is later.
2. RebalanceJob: lists cases in each queue with no owner and status NEW or ASSIGNED, and owners whose open cases exceed their capacity.
3. RebalanceService: for each owner above the cap, selects the newest cases by assignment time until the owner is inside the cap (R-UNI-19).
4. RebalanceService: skips cases with deviation_open or legal_hold true.
5. AssignmentEngine: picks an owner below the cap in the same queue for each selected or unassigned case.
6. RebalanceService: writes the decision log entry, ends the old assignment, writes the new one with reason REBALANCE and publishes CaseTransferred, case by case.

**Out of scope:**
- Reallocation when an owner leaves or is absent (R-UNI-18, Epic 2).
- The team queues screen (SCR-07, Epic 2) and the steering dashboard (Epic 2).
- The Power BI report layout (P9, RW-BIANAL).

**Business outcome and value hypothesis:** Team managers rebalance work by hand today and count queues from spreadsheets that do not match. This story moves cases left in overflow or without an owner each morning, takes owners above the cap back inside it (R-UNI-19), and publishes depth, ageing, owner spread and breaches as one snapshot that reconciles to the case list. It meets REQ-CWC-015 and REQ-RDF-012.

**Constraints and guardrails:**
- No business value in code: caps, methods and measure definitions are data.
- No personal data in the snapshot, the alerts, the logs or the tests; the snapshot holds counts only.
- No read of another module's tables: P9 reads the snapshot through QueueMeasureService.
- A move never resets the stage clock or the prescription date.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 030 Daily rebalancing and queue measures v1.md` |
| Requirement IDs | REQ-CWC-015, REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.1 and 5.3 |
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
| SY-CASEWF | Moves cases and takes the snapshot |
| SY-DECLOG | Writes the entries |
| RW-TEAMMGR | Receives the summaries and alerts; reads queues in team scope |
| RW-BIANAL | Builds the Power BI report on the snapshot (Reporting CRUD) |
| RW-DATASTEW | Receives the reconciliation break |
| RW-PLATADM | Reruns JOB-06 (Platform administration U) |

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
- **Feature flag:** `rwb.p3.rebalance`. Off: JOB-06 does not move cases; the snapshot still runs.
- **Critical path:** Yes; **depends on:** RWB-E1-020, RWB-E1-027, RWB-E1-028.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: caps, methods and measure definitions are data.
  - No personal data in the snapshot, the alerts, the logs or the tests; the snapshot holds counts only.
  - No read of another module's tables: P9 reads the snapshot through QueueMeasureService.
  - A move never resets the stage clock or the prescription date.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 030 Daily rebalancing and queue measures v1.md` |
| Specification | `output/INC-056-epic-1-RWB-E1-030/specify/spec.md` |
| Compliance validation | `output/INC-056-epic-1-RWB-E1-030/specify/compliance-validation.md` |
| Agent run log | `output/INC-056-epic-1-RWB-E1-030/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-056-epic-1-RWB-E1-030/plan/` (TBC) |
| Implementation evidence | `output/INC-056-epic-1-RWB-E1-030/implement/` (TBC) |
| API / functional test reports | `output/INC-056-epic-1-RWB-E1-030/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-056-epic-1-RWB-E1-030/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-056-epic-1-RWB-E1-030/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 030 Daily rebalancing and queue measures v1.md` |
| Output run | `output/INC-056-epic-1-RWB-E1-030/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
