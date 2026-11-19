# Increment Card — INC-023-epic-1-RWB-E1-056

**RWB-E1-056 — Run books and monitoring for every Epic 1 job**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-023` |
| Title | Run books and monitoring for every Epic 1 job |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-056` |
| RUN_ID | `INC-023-epic-1-RWB-E1-056` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-007 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **a run book for every scheduled job (purpose, schedule, owner, failure signs, restart steps, escalation) and monitoring of each job's last run, status and duration**, so that **the operations team can restart any Epic 1 job without the developer**.

**Main flow:**
1. Platform administrator: adds a job_catalog row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold.
2. Squad member (RW-TRIBE): writes the run book at `docs/operations/runbooks/<job ID>.md` with the six sections.
3. Pipeline: RunbookCompletenessTest checks that every Quartz job and Spring Batch job in the service has a catalog row and a run book with the six headings; it fails the build if one is missing.
4. Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.
5. Platform administrator: opens the Log Analytics workbook "Recovery jobs" or calls GET /admin/jobs and sees last run, status and duration per job.
6. Alert rule: a job with status FAILED, or running longer than its alert threshold, emails the owner role and RW-PLATADM with MSG-P2-004.

**Out of scope:**
- The SCR-44 screen: Epic 2; full monitor in Epic 8.
- Incident handling after a job failure: FEAT-ADM-12, Epic 8.
- The feeds on Control-M and ADF: RWB-E1-051.

**Business outcome and value hypothesis:** Epic 1 runs its loads, case creation, allocation, timers and copies as unattended jobs. A failed job that only its developer can restart holds the case list and the morning allocation. This story gives each job a catalog row with an owner and a run book, checks in the pipeline that both exist, and shows each job's last run, status and duration, so a failed job is noticed and restarted on the same day. It meets REQ-DRI-007 (a named owner for every failure).

**Constraints and guardrails:**
- No business value in code: owners, thresholds and paths are catalog rows.
- No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only.
- No read of another module's tables; the Spring Batch tables are read through the framework job repository.
- A run book names roles and service identities, never a person.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 056 Run books and monitoring for every Epic 1 job v1.md` |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
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
| RW-PLATADM, platform administrator | Maintains job_catalog rows; reruns a job (Platform administration, U) |
| RW-DATASTEW, data steward | Reads job runs; receives alerts for JOB-01, JOB-02, JOB-04, JOB-09, JOB-13 (Platform administration, R) |
| RW-TEAMMGR, team manager | Receives alerts for JOB-03 and JOB-06 by email; no endpoint right |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read job runs (Platform administration, R) |

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
- **Critical path:** Yes; **depends on:** RWB-E1-007.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: owners, thresholds and paths are catalog rows.
  - No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only.
  - No read of another module's tables; the Spring Batch tables are read through the framework job repository.
  - A run book names roles and service identities, never a person.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 056 Run books and monitoring for every Epic 1 job v1.md` |
| Specification | `output/INC-023-epic-1-RWB-E1-056/specify/spec.md` |
| Compliance validation | `output/INC-023-epic-1-RWB-E1-056/specify/compliance-validation.md` |
| Agent run log | `output/INC-023-epic-1-RWB-E1-056/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-023-epic-1-RWB-E1-056/plan/` (TBC) |
| Implementation evidence | `output/INC-023-epic-1-RWB-E1-056/implement/` (TBC) |
| API / functional test reports | `output/INC-023-epic-1-RWB-E1-056/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-023-epic-1-RWB-E1-056/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-023-epic-1-RWB-E1-056/specify/compliance-validation.md`) |
| Acceptance criteria | 5 ACs in the current story (AC2, AC3, AC5, AC6, AC7) |
| AC numbering | Intentional gaps: AC1, AC4 (removed by the 4 November 2026 cleanup) |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 056 Run books and monitoring for every Epic 1 job v1.md` |
| Output run | `output/INC-023-epic-1-RWB-E1-056/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
