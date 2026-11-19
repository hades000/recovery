# Increment Card — INC-053-epic-1-RWB-E1-030

**RWB-E1-030 — Daily rebalancing and queue measures**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-053` |
| Title | Daily rebalancing and queue measures |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-030` |
| RUN_ID | `INC-053-epic-1-RWB-E1-030` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 53 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-020, RWB-E1-027, RWB-E1-028 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a daily job that assigns unassigned cases and moves the newest cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches published to Power BI**, so that **queues stay balanced and every team manager sees the same numbers as the case list**.

**Business outcome:** Team managers rebalance work by hand today and count queues from spreadsheets that do not match. This story moves cases left in overflow or without an owner each morning, takes owners above the cap back inside it (R-UNI-19), and publishes depth, ageing, owner spread and breaches as one snapshot that reconciles to the case list. It meets REQ-CWC-015 and REQ-RDF-012.

**Main flow:**
1. Quartz: starts JOB-06 at 06:30, or when JOB-03 completes for the business date if that is later.
2. RebalanceJob: lists cases in each queue with no owner and status NEW or ASSIGNED, and owners whose open cases exceed their capacity.
3. RebalanceService: for each owner above the cap, selects the newest cases by assignment time until the owner is inside the cap (R-UNI-19).
4. RebalanceService: skips cases with deviation_open or legal_hold true.
5. AssignmentEngine: picks an owner below the cap in the same queue for each selected or unassigned case.
6. RebalanceService: writes the decision log entry, ends the old assignment, writes the new one with reason REBALANCE and publishes CaseTransferred, case by case.

**Acceptance criteria:**
- AC1: Rebalance
- AC2: Measures reconcile
- AC3: Breach alert
- AC4: No member has capacity
- AC5: No cap loaded
- AC6: Decision log unavailable for one case
- AC7: A repeated run
- AC8: Held cases are not moved
- AC9: A count difference holds the snapshot
- AC10: Owner exactly at the cap

**Out of scope:**
- Reallocation when an owner leaves or is absent (R-UNI-18, Epic 2).
- The team queues screen (SCR-07, Epic 2) and the steering dashboard (Epic 2).
- The Power BI report layout (P9, RW-BIANAL).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-030-daily-rebalancing-and-queue-measures-v1.md` |
| Requirement IDs | REQ-CWC-015, REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.1 and 5.3 |
| Decision | None |
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
| SY-CASEWF | Moves cases and takes the snapshot |
| SY-DECLOG | Writes the entries |
| RW-TEAMMGR | Receives the summaries and alerts; reads queues in team scope |
| RW-BIANAL | Builds the Power BI report on the snapshot (Reporting CRUD) |
| RW-DATASTEW | Receives the reconciliation break |
| RW-PLATADM | Reruns JOB-06 (Platform administration U) |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz at 06:30, after JOB-03 completes for the business date | | Job name | JOB-06 Daily rebalancing | | Schedule | Daily 06:30 | | Input | Queues in force, members and capacity, open cases per owner, cases with no owner, EXPIRED service level timers | | Output | Assignments with reason REBALANCE, decision log entries, one queue_measure snapshot per queue | | Events published | CaseTransferred (EV-04) per move | | Idempotency key | caseId and businessDate for a move; queueId and snapshot time for a snapshot | | Restart | Rerun from the job monitor; balanced queues give no moves; managers rebalance by hand if the rerun fails (batch.txt) | **GET /api/recovery/v1/cases** (used for the reconciliation test) | Item | Value | |---|---| | Request | Query queue (uuid), status, page, size | | Response | CasePage: items, page, size, total | | Errors…

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

- No business value in code: caps, methods and measure definitions are data. - No personal data in the snapshot, the alerts, the logs or the tests; the snapshot holds counts only. - No read of another module's tables: P9 reads the snapshot through QueueMeasureService. - A move never resets the stage clock or the prescription date.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-030-daily-rebalancing-and-queue-measures-v1.md` |
| Specification | `output/INC-053-epic-1-RWB-E1-030/specify/spec.md` |
| Compliance validation | `output/INC-053-epic-1-RWB-E1-030/specify/compliance-validation.md` |
| Agent run log | `output/INC-053-epic-1-RWB-E1-030/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-053-epic-1-RWB-E1-030/plan/` |
| Implementation evidence | `output/INC-053-epic-1-RWB-E1-030/implement/` |
| API / functional test reports | `output/INC-053-epic-1-RWB-E1-030/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-053-epic-1-RWB-E1-030/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-030-daily-rebalancing-and-queue-measures-v1.md` |
| Output run | `output/INC-053-epic-1-RWB-E1-030/` |

