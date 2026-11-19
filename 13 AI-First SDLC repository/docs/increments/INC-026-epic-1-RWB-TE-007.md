# Increment Card — INC-026-epic-1-RWB-TE-007

**RWB-TE-007 — Scheduled jobs on Quartz**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-026` |
| Title | Scheduled jobs on Quartz |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-007` |
| RUN_ID | `INC-026-epic-1-RWB-TE-007` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-044, RWB-E1-056 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each**, so that **scheduled work runs once, on time and visibly, and a missed run is caught up for its business date**.

**Main flow:**
1. Scheduler: on LoadCompleted for business date D, and on completion of JOB-02 for D, fires JOB-03 Morning allocation and JOB-04 Daily reconciliation for D.
2. Scheduler: fires JOB-05 Timer check every 5 minutes on cron `0 0/5 * * * ?` in Asia/Bangkok.
3. Job runner: takes the cluster lock so only one instance runs a job at a time.
4. Job runner: checks the job run log for job and business date; if a successful run exists, records the skip and stops.
5. Job runner: checks the job's dependency (JOB-02 succeeded for D); if not met, records WAITING and stops.
6. Job runner: records the run start through the P1 job monitor, runs the job body, records the end with status SUCCEEDED or FAILED and the counts.

**Out of scope:**
- The job bodies: allocation (RWB-E1-020), reconciliation (RWB-E1-011), timer check (RWB-E1-028).
- The COLLINS load and case creation jobs JOB-01 and JOB-02 (P1).
- Daily rebalancing JOB-06 (RWB-E1-030).
- The job monitor screen and the operations alert channel (RWB-E1-056).

**Business outcome and value hypothesis:** The morning allocation must finish by 07:00 so no new case waits for a person (JOB-03), the timer check must find every due timer every 5 minutes (JOB-05), and the reconciliation must compare the case list with the core bank every day (JOB-04). The ACE service runs on more than one instance, so without a shared schedule a job runs twice or not at all, and an outage loses a day's run. This story runs the three jobs on the clustered ACE Quartz scheduler with one run per business date, catch-up after an outage and a run book for each. It meets REQ-CWC-007, REQ-CWC-011 and REQ-RDF-007. The measure is one successful run per job per business date, and JOB-03 complete by 07:00 (NFR-013).

**Constraints and guardrails:**
- No business value in code. Schedules, limits and deadlines come from the configuration service.
- No personal data in job logs, run books, alerts, tests or prompts. Logs carry job IDs, dates and counts.
- No read of another module's tables. The job run log is written through the P1 interface; the Quartz tables are used only through the ACE scheduler API.
- A job body never decides its own business date from the clock; it takes the date it is given.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 007 Scheduled jobs on Quartz v1.md` |
| Requirement IDs | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.1, 5.3 and 6.3 |
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
| RW-PLATADM, platform administrator | Reads runs and reruns a failed run (Platform administration CRUD) |
| RW-DATASTEW, data steward | Reads runs; owns JOB-04 (Platform administration R) |
| RW-TEAMMGR, team manager | Owns JOB-03 per batch.txt; is told by the allocation summary (RWB-E1-020) |
| SY-CASEWF, case workflow module | Runs JOB-03 and JOB-05 |
| SY-DATALOAD, data load from COLLINS | Runs JOB-04 inputs from the COLLINS load |

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
- **Feature flag:** `rwb.p3.quartz-jobs`. Off: the three jobs are not scheduled and the job bodies can be run only through the rerun endpoint.
- **Critical path:** No; **depends on:** RWB-E1-044, RWB-E1-056.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code. Schedules, limits and deadlines come from the configuration service.
  - No personal data in job logs, run books, alerts, tests or prompts. Logs carry job IDs, dates and counts.
  - No read of another module's tables. The job run log is written through the P1 interface; the Quartz tables are used only through the ACE scheduler API.
  - A job body never decides its own business date from the clock; it takes the date it is given.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 007 Scheduled jobs on Quartz v1.md` |
| Specification | `output/INC-026-epic-1-RWB-TE-007/specify/spec.md` |
| Compliance validation | `output/INC-026-epic-1-RWB-TE-007/specify/compliance-validation.md` |
| Agent run log | `output/INC-026-epic-1-RWB-TE-007/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-026-epic-1-RWB-TE-007/plan/` (TBC) |
| Implementation evidence | `output/INC-026-epic-1-RWB-TE-007/implement/` (TBC) |
| API / functional test reports | `output/INC-026-epic-1-RWB-TE-007/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-026-epic-1-RWB-TE-007/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-026-epic-1-RWB-TE-007/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 007 Scheduled jobs on Quartz v1.md` |
| Output run | `output/INC-026-epic-1-RWB-TE-007/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
