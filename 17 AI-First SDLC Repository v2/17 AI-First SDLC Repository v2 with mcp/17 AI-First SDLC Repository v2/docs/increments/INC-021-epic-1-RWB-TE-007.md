# Increment Card — INC-021-epic-1-RWB-TE-007

**RWB-TE-007 — Scheduled jobs on Quartz**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-021` |
| Title | Scheduled jobs on Quartz |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-007` |
| RUN_ID | `INC-021-epic-1-RWB-TE-007` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 21 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044, RWB-E1-056, RWB-E1-028 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each**, so that **scheduled work runs once, on time and visibly, and a missed run is caught up for its business date**.

**Business outcome:** The morning allocation must finish by 07:00 so no new case waits for a person (JOB-03), the timer check must find every due timer every 5 minutes (JOB-05), and the reconciliation must compare the case list with the core bank every day (JOB-04). The ACE service runs on more than one instance, so without a shared schedule a job runs twice or not at all, and an outage loses a day's run. This story runs the three jobs on the clustered ACE Quartz scheduler with one run per business date, catch-up after an outage and a run book for each. It meets REQ-CWC-007, REQ-CWC-011 and REQ-RDF-007. The measure is one successful run per job per business date, and JOB-03 complete by 07:00 (NFR-013).

**Main flow:**
1. Scheduler: on LoadCompleted for business date D, and on completion of JOB-02 for D, fires JOB-03 Morning allocation and JOB-04 Daily reconciliation for D.
2. Scheduler: fires JOB-05 Timer check every 5 minutes on cron `0 0/5 * * * ?` in Asia/Bangkok. JOB-05 is the Quartz implementation of the TimerScheduler port of RWB-E1-028: schedule, cancel, pause and resume write the timer row, and the fire runs the warning, breach and expiry check.
3. Job runner: takes the cluster lock so only one instance runs a job at a time.
4. Job runner: checks the job run log for job and business date; if a successful run exists, records the skip and stops.
5. Job runner: checks the job's dependency (JOB-02 succeeded for D); if not met, records WAITING and stops.
6. Job runner: records the run start through the P1 job monitor, runs the job body, records the end with status SUCCEEDED or FAILED and the counts.

**Acceptance criteria:**
- AC1: Runs once
- AC2: Missed run
- AC3: Repeated run for the same date
- AC4: Timer check does not overlap
- AC5: Several missed dates
- AC6: More missed dates than the limit
- AC7: Dependency not met
- AC8: Instance stops part way
- AC9: Allocation late
- AC10: Run book for every job
- AC11: No new Quartz job holds a case wait

**Out of scope:**
- The job bodies: allocation (RWB-E1-020), reconciliation (RWB-E1-011), timer check (RWB-E1-028).
- The COLLINS load and case creation jobs JOB-01 and JOB-02 (P1).
- Daily rebalancing JOB-06 (RWB-E1-030).
- The job monitor screen and the operations alert channel (RWB-E1-056).
- Temporal Schedules (Epic 3+): durable timers and case waits move to Temporal then (ADR-011).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-007-scheduled-jobs-on-quartz-v2.md` |
| Requirement IDs | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.1, 5.3 and 6.3 |
| Decision | D-RCV-36 (T1, T2); ADR-011 |
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
| RW-PLATADM, platform administrator | Reads runs and reruns a failed run (Platform administration CRUD) |
| RW-DATASTEW, data steward | Reads runs; owns JOB-04 (Platform administration R) |
| RW-TEAMMGR, team manager | Owns JOB-03 per batch.txt; is told by the allocation summary (RWB-E1-020) |
| SY-CASEWF, case workflow module | Runs JOB-03 and JOB-05; JOB-05 is the TimerScheduler implementation |
| SY-DATALOAD, data load from COLLINS | Runs JOB-04 inputs from the COLLINS load |

## Contract extract

**Jobs** | Item | JOB-03 Morning allocation | JOB-04 Daily reconciliation | JOB-05 Timer check | |---|---|---|---| | Trigger | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | Cron `0 0/5 * * * ?`, Asia/Bangkok | | Schedule | Daily after JOB-02, by 07:00 | Daily after JOB-02 | Every 5 minutes | | Runs on | Quartz (D-RCV-36 T2) | Quartz (D-RCV-36 T2) | Quartz; the Epic 1 implementation of TimerScheduler (D-RCV-36 T2) | | Input | New cases of D | Accounts at 90 days past due in the load of D and open cases | Timers with `expires_at` or `warn_at` before now | | Output | Cases placed and owners given (RWB-E1-020) | Reconciliation breaks (RWB-E1-011) | Warnings, escalations, timer events (RWB-E1-028) | | Events published | CaseAllocated (EV-02), CaseAllocationFailed (EV-03), by the job body | None | TimerDue (EV-18), TimerBreac…

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

- No business value in code. Schedules, limits and deadlines come from the configuration service. - No personal data in logs, tests, workflow history or prompts. Job logs, run books and alerts carry job IDs, dates and counts. - No read of another module's tables; ACE data only through recovery.v_ace_* views. The job run log is written through the P1 interface; the Quartz tables are used only through the ACE scheduler API. - A job body never decides its own business date from the clock; it takes the date it is given. - No new Quartz job holds a case wait; case waits move to Temporal in Epic 3 (D-RCV-36 T1, T2; ADR-011). - No Temporal schedule is registered in Epic 1 or Epic 2.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-007-scheduled-jobs-on-quartz-v2.md` |
| Specification | `output/INC-021-epic-1-RWB-TE-007/specify/spec.md` |
| Compliance validation | `output/INC-021-epic-1-RWB-TE-007/specify/compliance-validation.md` |
| Agent run log | `output/INC-021-epic-1-RWB-TE-007/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-021-epic-1-RWB-TE-007/plan/` |
| Implementation evidence | `output/INC-021-epic-1-RWB-TE-007/implement/` |
| API / functional test reports | `output/INC-021-epic-1-RWB-TE-007/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-021-epic-1-RWB-TE-007/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-007-scheduled-jobs-on-quartz-v2.md` |
| Output run | `output/INC-021-epic-1-RWB-TE-007/` |

