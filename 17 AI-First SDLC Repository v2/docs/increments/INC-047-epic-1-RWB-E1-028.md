# Increment Card — INC-047-epic-1-RWB-E1-028

**RWB-E1-028 — Service levels, timers, escalation and prescription dates**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-047` |
| Title | Service levels, timers, escalation and prescription dates |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-028` |
| RUN_ID | `INC-047-epic-1-RWB-E1-028` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 47 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-045, RWB-E1-020, RWB-E1-027, RWB-E1-043 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a service level per queue and status, a timer on every case, a warning to the owner and a breach raised to the named escalation point by rule, and a prescription date set from the legal periods**, so that **no case waits past its limit unseen and no legal claim expires unnoticed**.

**Business outcome:** Deadlines are tracked in personal diaries today, and audit found litigation not filed for debtors meeting the criteria (CTL-18). This story starts a service level timer each time a case enters a queue and status, warns the owner at the warning point, raises a breach to the escalation role without moving the case, and sets the prescription date at case creation from the legal period for the product. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 and serves the measure "cases inside the service level" (target set with DL22).

**Main flow:**
1. TimerStarter: on CaseAllocated, CaseTransferred or CaseStateChanged, cancels the running SERVICE_LEVEL timer of the case through TimerScheduler.cancel(timerId).
2. TimerStarter: reads the service level for the new queue and status and calls TimerScheduler.schedule(TimerSpec) with started_at, expires_at in working days and warn_at at the warning percentage; the port writes the timer row.
3. PrescriptionService: on CaseCreated, reads the last payment date of each linked account through the P1 interface and the legal period for the product, and sets the earliest result as the prescription date.
4. PrescriptionService: schedules a PRESCRIPTION timer through TimerScheduler.schedule with expires_at on the prescription date and warn_at 180 days before; a PRESCRIPTION timer never pauses.
5. TimerCheckJob (JOB-05): every 5 minutes finds RUNNING timers whose warn_at or expires_at has passed.
6. TimerCheckJob: for a passed warn_at, writes the decision log entry and sends MSG-P3-003 to the case owner once.

**Acceptance criteria:**
- AC1: Timer starts
- AC2: Warning and escalation
- AC3: Prescription date
- AC4: No service level for the queue and status
- AC5: No legal period for the product
- AC6: No payment ever made
- AC7: Missed timer check runs
- AC8: A breach is raised once
- AC9: Decision log unavailable at a breach
- AC10: A deviation pauses the stage clock and not the prescription clock
- AC11: The warning point on a 5-day service level
- AC12: Timer scheduling goes only through TimerScheduler

**Out of scope:**
- The prescription warning forcing a litigation review (R-UNI-31, CTL-18, Epic 2).
- The timer panel and escalation state on the case view (RWB-E2-015).
- The notice period, cure period, offer validity and other stage-specific timers (their route stories, Epic 3 to Epic 6).
- Temporal durable timers replace the Quartz implementation in Epic 3 (ADR-011).
- The service level values themselves (DL22).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-028-service-levels-timers-escalation-and-prescription-dates-v2.md` |
| Requirement IDs | REQ-CWC-011, REQ-CWC-012, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
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
| SY-CASEWF | Starts, pauses, resumes, stops and expires timers through TimerScheduler; sets the prescription date |
| SY-DECLOG | Writes the entries |
| RW-CASEOWN | Reads the timers on their cases and receives the warning |
| RW-TEAMMGR | Receives the breach as the escalation point; reads timers in team scope |
| RW-LEGAL | Owns the LEGAL_PERIOD rows; they are loaded through RWB-E1-043 |
| Business lead | Owns the service level values (DL22) |
| Every role with Case record R | Reads the timers within scope |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz schedule | | Job name | JOB-05 Timer check | | Engine | Quartz; this job is the Epic 1 implementation of the TimerScheduler port (D-RCV-36 T2), with no Temporal schedule | | Schedule | Every 5 minutes | | Input | RUNNING timers with warn_at or expires_at before now (index ix_timer_due) | | Output | Warnings, breaches, expired timers, decision log entries | | Events published | TimerBreached (EV-19: timerId, caseId, escalateTo); TimerDue (EV-18: timerId, caseId, timerType) | | Idempotency key | timerId and the point (WARN or EXPIRE); a timer already EXPIRED or already warned is skipped | | Restart | The next run picks up every missed timer (batch.txt JOB-05) | **Events consumed.** CaseCreated (EV-01), CaseAllocated (EV-02), CaseTransferred (EV-04), CaseStateChanged (EV-05), DeviationRaised (EV-06), DeviationCleared (EV-07). **GET /api…

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

- No business value in code: service levels, the warning point, escalation roles, legal periods and holidays are data. - No personal data in logs, tests, workflow history or prompts; cases are named by case number. - No read of another module's tables; ACE data only through recovery.v_ace_* views: account dates through RecoveryDataQuery (P1). - A breach never moves the case; the prescription timer never pauses. - Timer scheduling goes only through TimerScheduler; no class outside recovery.casewf.timers writes or updates the timer table. - No Temporal schedule and no Temporal durable timer in Epic 1: JOB-05 stays on Quartz behind the port (D-RCV-36 T2).

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-028-service-levels-timers-escalation-and-prescription-dates-v2.md` |
| Specification | `output/INC-047-epic-1-RWB-E1-028/specify/spec.md` |
| Compliance validation | `output/INC-047-epic-1-RWB-E1-028/specify/compliance-validation.md` |
| Agent run log | `output/INC-047-epic-1-RWB-E1-028/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-047-epic-1-RWB-E1-028/plan/` |
| Implementation evidence | `output/INC-047-epic-1-RWB-E1-028/implement/` |
| API / functional test reports | `output/INC-047-epic-1-RWB-E1-028/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-047-epic-1-RWB-E1-028/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 12 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-028-service-levels-timers-escalation-and-prescription-dates-v2.md` |
| Output run | `output/INC-047-epic-1-RWB-E1-028/` |

