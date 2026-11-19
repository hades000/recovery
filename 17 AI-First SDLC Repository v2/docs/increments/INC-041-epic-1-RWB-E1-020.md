# Increment Card — INC-041-epic-1-RWB-E1-020

**RWB-E1-020 — Allocation and assignment engine v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-041` |
| Title | Allocation and assignment engine v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-020` |
| RUN_ID | `INC-041-epic-1-RWB-E1-020` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 41 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056, RWB-E1-072, RWB-E1-073 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **every new recovery case placed in a queue and given an owner by the ALLOCATION and ASSIGNMENT rule packages on the morning it arrives**, so that **each case at 90 days past due has one owner from its first day and nobody allocates cases by hand**.

**Business outcome:** Cases are allocated today from team spreadsheets, and ownership is agreed by email, so a case can wait days with no owner. This story places every new case in a queue and gives it an owner by rule before 07:00 on the morning after case creation, with the rule ID and the package version on a decision log entry. It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016, and serves the business measure "cases inside the service level" (target set with DL22) and control CTL-03.

**Main flow:**
1. Quartz (D-RCV-36 T2): starts JOB-03 Morning allocation after JOB-02 completes for business date 2026-12-01.
2. AllocationJob: selects every case with status NEW whose last allocation date is before the business date.
3. AllocationService: locks the case row and reads deviation_open; a case with an open deviation goes to the deviation handler queue (R-DEV-01).
4. AllocationService: builds `AllocationFacts` from the case and calls `RuleEvaluator.evaluate("ALLOCATION", facts, businessDate)`; the evaluator returns the first matching rule in row order (T5), its rule ID and package version, and the target queue in `outputs`.
5. AllocationService: fills the target queue code and cap in the same facts object and calls `RuleEvaluator.evaluate("ASSIGNMENT", facts, businessDate)` for that queue; the row returns the assignment method, the cap and, for NAMED_OWNER, the owner. AssignmentEngine counts the open cases of each queue member and picks the first owner below the cap by the method.
6. AllocationService: in one transaction sets queue, team, owner, status ASSIGNED, stage clock start, allocation rule ID and package version, writes the assignment with reason ALLOCATION and the assignment rule ID and package version, sets the last allocation date and writes CaseAllocated (EV-02) to the outbox.

**Acceptance criteria:**
- AC1: A new case is placed in the queue its rule names
- AC2: The owner is chosen by the assignment rule
- AC3: An owner at the caseload cap is skipped
- AC4: Every owner is at the cap
- AC5: No allocation rule matches
- AC6: Every allocation is logged
- AC7: A case with an open deviation is not allocated to a case owner
- AC8: A repeated run for the same date has no further effect
- AC9: A run with no new cases
- AC10: The run waits for case creation
- AC11: Two runs at the same time allocate each case once
- AC12: An owner one case below the cap gets the case
- AC13: A queue with no overflow queue sends the case to the exception queue

**Out of scope:**
- Manual transfer and reassignment screens (RWB-E2-011, RWB-E2-012).
- Reallocation when an owner leaves or passes the cap (R-UNI-18 and R-UNI-19, Epic 2; daily rebalancing in RWB-E1-030).
- The values of the caseload caps and the service levels (DL22, DL23).
- Loading, validating, approving and rolling back the ALLOCATION and ASSIGNMENT packages (RWB-E1-073).
- The default row check at load (RWB-E1-073).
- Placement on a queue by a model or an agent (RWB-E2-036).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-020-allocation-and-assignment-engine-v1-v2.md` |
| Requirement IDs | REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| Decision | D-RCV-36; ADR-011; ADR-012 |
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
| SY-RULES, Drools evaluator | Evaluates packages ALLOCATION and ASSIGNMENT through `RuleEvaluator` (Rules and parameters R) |
| SY-CASEWF, case workflow module | Updates the case and writes the assignment (Case record CRU; Queue and allocation CRU) |
| SY-DECLOG, decision log writer | Writes the entry (Decision log C) |
| RW-TEAMMGR, team manager | Reads the queue and the allocation summary for their team (Queue and allocation R) |
| RW-CASEOWN, case owner | Reads the cases given to them (Case record R, scope Own) |
| RW-PLATADM, platform administrator | Reruns JOB-03 from the job monitor (Platform administration U) |
| RW-REFADM, reference data administrator | Prepares the package workbook; the load is RWB-E1-073 |
| Process owner for L1 18, Shared operations | Approves each package version through RWB-E1-073 (reference data change process, step 4). No delegation of authority level applies |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz (D-RCV-36 T2), after JOB-02 completes for the business date | | Job name | JOB-03 Morning allocation | | Schedule | Daily after JOB-02, complete by 07:00 Asia/Bangkok | | Input | Cases with status NEW and last_allocation_date before the business date; ALLOCATION and ASSIGNMENT package versions in force on the business date, through `RuleEvaluator` (RWB-E1-072); queues and queue members | | Output | Case queue, team, owner, status, allocation rule ID and package version; assignment rows with the assignment rule ID and package version; decision log entries; allocation summary per team; job record with counts | | Events published | CaseAllocated (EV-02: caseId, queueId, ownerId, ruleId, ruleVersion), where ruleVersion is the ALLOCATION package version label; CaseAllocationFailed (EV-03: caseId, reason, ruleGap) | | Idempotency key | cas…

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

- No business value in code: product groups, regions, bands, queues, methods, caps and queue codes are data in the packages, the queue table and the parameters. - No personal data in logs, tests, workflow history or prompts. Cases are named by case number only. - No read of another module's tables; ACE data only through `recovery.v_ace_*` views: rule packages come through `RuleEvaluator` (P3, RWB-E1-072); the decision log through `DecisionLogWriter` (P7). - One evaluator: ALLOCATION and ASSIGNMENT are evaluated only through `RuleEvaluator`; no code reads `drl_source`, the workbook or a rule_row row directly (D-RCV-36 T3, T6). - The default row check is not repeated at run time; it is at load in RWB-E1-073 (D-RCV-36 T5). - The decision log entry is written in the same transaction as the case change; a failed write leaves the case unchanged. - JOB-03 stays on Quartz in Epic 1 and Epic 2 (…

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-020-allocation-and-assignment-engine-v1-v2.md` |
| Specification | `output/INC-041-epic-1-RWB-E1-020/specify/spec.md` |
| Compliance validation | `output/INC-041-epic-1-RWB-E1-020/specify/compliance-validation.md` |
| Agent run log | `output/INC-041-epic-1-RWB-E1-020/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-041-epic-1-RWB-E1-020/plan/` |
| Implementation evidence | `output/INC-041-epic-1-RWB-E1-020/implement/` |
| API / functional test reports | `output/INC-041-epic-1-RWB-E1-020/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-041-epic-1-RWB-E1-020/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 13 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-020-allocation-and-assignment-engine-v1-v2.md` |
| Output run | `output/INC-041-epic-1-RWB-E1-020/` |

