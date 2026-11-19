# Increment Card — INC-018-epic-1-RWB-E1-056

**RWB-E1-056 — Run books and monitoring for every Epic 1 Workbench job**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-018` |
| Title | Run books and monitoring for every Epic 1 Workbench job |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-056` |
| RUN_ID | `INC-018-epic-1-RWB-E1-056` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 18 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-007, RWB-E1-015, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **a run book for every Workbench job, the agent runtime and the view conformance check (purpose, schedule, owner, dependencies, failure signs, checks, restart steps, escalation) and monitoring of each job's last run, status and duration beside the last complete ACE business date per source**, so that **the operations team can restart any Epic 1 job without the developer and can tell a late ACE batch from a failed Workbench job**.

**Business outcome:** The Workbench loads no source data (D-RCV-35 U1; ADR-010). Its scheduled work is the case list chain, the timer check, daily rebalancing, payment matching, booking confirmation, the WIN notice file, the outbox sender, document intake, the decision log copy and its hash chain check, the reporting extract, retention, the agent runtime and the view conformance test. A failed job that only its developer can restart holds the case list and the morning allocation; a late ACE batch looks exactly like a failed Workbench job unless the monitor shows the ACE business date beside it.

**Main flow:**
1. Platform administrator: confirms one `job_catalog` row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold. V0004 seeds the 16 Epic 1 rows; later changes are data rows, not code.
2. Squad member (RW-TRIBE): writes the run book at `docs/operations/runbooks/<job ID>.md` with eight sections: purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation.
3. Squad member: names the ACE sources the job reads through `recovery.v_ace_*` and the upstream Workbench job in Dependencies; names the stale marker on `data_product_load` and EV-27 AceDataLate in Failure signs when the job reads ACE; the view conformance run book names CHK-01 and the dictionary load through RWB-E1-043 in Checks and Restart steps.
4. Pipeline: `RunbookCompletenessTest` checks that every Quartz job and every catalog row has a run book with the eight headings, that no run book names an inbound load job, a file arrival, a load rerun or a data quality exception console, and that no run book names a table in schema `public`.
5. Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.
6. Platform administrator: opens the Log Analytics workbook "Recovery jobs" or calls GET /admin/jobs and sees last run, status and duration per job, and the last complete ACE business date per source from `v_ace_batch_status`.

**Acceptance criteria:**
- AC1: Run book present
- AC2: Restart by run book
- AC3: Monitoring in place
- AC4: Missing run book blocks the build
- AC5: Rerun while running refused
- AC6: Job running past its threshold
- AC7: Rerun of a completed job changes nothing
- AC8: A late ACE batch holds the job
- AC9: The view conformance test has a run book

**Out of scope:**
- The SCR-44 screen: Epic 2; full monitor in Epic 8.
- Incident handling after a job failure: FEAT-ADM-12, Epic 8.
- ACE's own ingestion monitoring and alerting: RWB-ACE-001. The Workbench watches the business date, not the ACE job.
- The freshness stamp, the stale marker and EV-27: RWB-E1-015.
- The 30 views and the view conformance test: RWB-E1-069.
- The job bodies and the agent runtime: their own stories.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-056-run-books-and-monitoring-for-every-epic-1-job-v1.md` |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
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
| RW-PLATADM, platform administrator | Maintains job_catalog rows; reruns a job (Platform administration, U); owns JOB-10, JOB-11, JOB-12 and CHK-01 |
| RW-DATASTEW, data steward | Reads job runs; owns JOB-02, JOB-04 and JOB-13; receives their alerts (Platform administration, R) |
| RW-TEAMMGR, team manager | Owns JOB-03 and JOB-06; receives their alerts by email; no endpoint right |
| RW-CREDITAD, credit administration | Owns JOB-07 and JOB-08; receives their alerts by email |
| RW-BIANAL, reporting and BI analyst | Owns JOB-15; receives its alerts by email |
| RW-COE, center of excellence analyst | Owns AGT-01; receives its alerts by email |
| RW-COMPLY, compliance | Owns JOB-14 and JOB-17; receives their alerts by email |
| RW-TRIBE, squad member | Writes and maintains the run books and RunbookCompletenessTest; reads job runs (Platform administration, R) |
| RW-AUDIT and RW-SECADM | Read job runs (Platform administration, R) |

## Contract extract

| Method and path | Request | Response | Errors | Authorization | Idempotency | |---|---|---|---|---|---| | GET /admin/jobs | Query: type (job ID), status, from, to | Array of Job: id, type, businessDate, status, startedAt, endedAt, runbookPath, checks | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only | | POST /admin/jobs/{jobId}/rerun | Path: jobId (the failed execution) | Job | 401; 403 (MSG-P4-002); 404 unknown execution (MSG-P4-003); 409 job running (MSG-P2-006) or run already completed (MSG-GEN-004); 503 | Platform administration, U | Per job and business date | | GET /admin/scheduled-jobs | None | JobCatalogResponse: entries of JobCatalogEntry (jobId, jobName, ownerRole, schedule, runbookPath, expectedMinutes, alertAfterMinutes, firstRelease) and aceBatchStatus of AceBatchStatus (sourceSystem, businessDate, startedAt, completedAt, status, isComplet…

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

- No business value in code: owners, thresholds and paths are catalog rows. - No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only. - No read of another module's tables and no read of a table in schema `public`: ACE data comes through `recovery.v_ace_*` only. The Quartz tables are read through the scheduler API. - A run book names roles and service identities, never a person. - No run book describes an inbound load, file arrival or load rerun; the Workbench has none.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-056-run-books-and-monitoring-for-every-epic-1-job-v1.md` |
| Specification | `output/INC-018-epic-1-RWB-E1-056/specify/spec.md` |
| Compliance validation | `output/INC-018-epic-1-RWB-E1-056/specify/compliance-validation.md` |
| Agent run log | `output/INC-018-epic-1-RWB-E1-056/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-018-epic-1-RWB-E1-056/plan/` |
| Implementation evidence | `output/INC-018-epic-1-RWB-E1-056/implement/` |
| API / functional test reports | `output/INC-018-epic-1-RWB-E1-056/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-018-epic-1-RWB-E1-056/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-056-run-books-and-monitoring-for-every-epic-1-job-v1.md` |
| Output run | `output/INC-018-epic-1-RWB-E1-056/` |

