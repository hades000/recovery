# Increment Card — INC-049-epic-1-RWB-E1-028

**RWB-E1-028 — Service levels, timers, escalation and prescription dates**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-049` |
| Title | Service levels, timers, escalation and prescription dates |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-028` |
| RUN_ID | `INC-049-epic-1-RWB-E1-028` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-045, RWB-E1-020, RWB-E1-027, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a service level per queue and status, a timer on every case, a warning to the owner and a breach raised to the named escalation point by rule, and a prescription date set from the legal periods**, so that **no case waits past its limit unseen and no legal claim expires unnoticed**.

**Main flow:**
1. TimerStarter: on CaseAllocated, CaseTransferred or CaseStateChanged, stops the running SERVICE_LEVEL timer of the case.
2. TimerStarter: reads the service level for the new queue and status and starts a SERVICE_LEVEL timer with started_at, expires_at in working days and warn_at at the warning percentage.
3. PrescriptionService: on CaseCreated, reads the last payment date of each linked account through the P1 interface and the legal period for the product, and sets the earliest result as the prescription date.
4. PrescriptionService: starts a PRESCRIPTION timer with expires_at on the prescription date and warn_at 180 days before; a PRESCRIPTION timer never pauses.
5. TimerCheckJob (JOB-05): every 5 minutes finds RUNNING timers whose warn_at or expires_at has passed.
6. TimerCheckJob: for a passed warn_at, writes the decision log entry and sends MSG-P3-003 to the case owner once.

**Out of scope:**
- The prescription warning forcing a litigation review (R-UNI-31, CTL-18, Epic 2).
- The timer panel and escalation state on the case view (RWB-E2-015).
- The notice period, cure period, offer validity and other stage-specific timers (their route stories, Epic 3 to Epic 6).
- The service level values themselves (DL22).

**Business outcome and value hypothesis:** Deadlines are tracked in personal diaries today, and audit found litigation not filed for debtors meeting the criteria (CTL-18). This story starts a service level timer each time a case enters a queue and status, warns the owner at the warning point, raises a breach to the escalation role without moving the case, and sets the prescription date at case creation from the legal period for the product. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 and serves the measure "cases inside the service level" (target set with DL22).

**Constraints and guardrails:**
- No business value in code: service levels, the warning point, escalation roles, legal periods and holidays are data.
- No personal data in logs, tests, events or notifications; cases are named by case number.
- No read of another module's tables: account dates through RecoveryDataQuery (P1).
- A breach never moves the case; the prescription timer never pauses.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 028 Service levels timers escalation and prescription dates v1.md` |
| Requirement IDs | REQ-CWC-011, REQ-CWC-012, REQ-CWC-016 |
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
| SY-CASEWF | Starts, pauses, stops and expires timers; sets the prescription date |
| SY-DECLOG | Writes the entries |
| RW-CASEOWN | Reads the timers on their cases and receives the warning |
| RW-TEAMMGR | Receives the breach as the escalation point; reads timers in team scope |
| RW-LEGAL | Owns the LEGAL_PERIOD rows; they are loaded through RWB-E1-043 |
| Business lead | Owns the service level values (DL22) |
| Every role with Case record R | Reads the timers within scope |

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
- **Feature flag:** `rwb.p3.timers`. Off: no timers start and JOB-05 does nothing.
- **Critical path:** Yes; **depends on:** RWB-E1-045, RWB-E1-020, RWB-E1-027, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: service levels, the warning point, escalation roles, legal periods and holidays are data.
  - No personal data in logs, tests, events or notifications; cases are named by case number.
  - No read of another module's tables: account dates through RecoveryDataQuery (P1).
  - A breach never moves the case; the prescription timer never pauses.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 028 Service levels timers escalation and prescription dates v1.md` |
| Specification | `output/INC-049-epic-1-RWB-E1-028/specify/spec.md` |
| Compliance validation | `output/INC-049-epic-1-RWB-E1-028/specify/compliance-validation.md` |
| Agent run log | `output/INC-049-epic-1-RWB-E1-028/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-049-epic-1-RWB-E1-028/plan/` (TBC) |
| Implementation evidence | `output/INC-049-epic-1-RWB-E1-028/implement/` (TBC) |
| API / functional test reports | `output/INC-049-epic-1-RWB-E1-028/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-049-epic-1-RWB-E1-028/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-049-epic-1-RWB-E1-028/specify/compliance-validation.md`) |
| Acceptance criteria | 11 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 028 Service levels timers escalation and prescription dates v1.md` |
| Output run | `output/INC-049-epic-1-RWB-E1-028/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
