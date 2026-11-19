# Increment Card — INC-043-epic-1-RWB-E1-020

**RWB-E1-020 — Allocation and assignment engine v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-043` |
| Title | Allocation and assignment engine v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-020` |
| RUN_ID | `INC-043-epic-1-RWB-E1-020` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **every new recovery case placed in a queue and given an owner by the allocation and assignment rule tables on the morning it arrives**, so that **each case at 90 days past due has one owner from its first day and nobody allocates cases by hand**.

**Main flow:**
1. Quartz: starts JOB-03 Morning allocation after JOB-02 completes for business date 2026-12-01.
2. AllocationJob: selects every case with status NEW whose last allocation date is before the business date.
3. AllocationService: locks the case row and reads deviation_open; a case with an open deviation goes to the deviation handler queue (R-DEV-01).
4. AllocationRuleEvaluator (SY-RULES): reads the allocation rows in force on the business date and returns the first row, in row order, whose product group, region and exposure band match the case.
5. AssignmentEngine: reads the target queue's method (DF-WRK-006) and cap (DF-WRK-007), counts the open cases of each queue member and picks the owner below the cap by the method.
6. AllocationService: in one transaction sets queue, team, owner, status ASSIGNED, stage clock start and rule version, writes the assignment with reason ALLOCATION, sets the last allocation date and writes CaseAllocated (EV-02) to the outbox.

**Out of scope:**
- Manual transfer and reassignment screens (RWB-E2-011, RWB-E2-012).
- Reallocation when an owner leaves or passes the cap (R-UNI-18 and R-UNI-19, Epic 2; daily rebalancing in RWB-E1-030).
- The values of the caseload caps and the service levels (DL22, DL23).
- Loading and validating the allocation table (RWB-E1-029).
- Placement on a queue by a model or an agent (RWB-E2-036).

**Business outcome and value hypothesis:** Cases are allocated today from team spreadsheets, and ownership is agreed by email, so a case can wait days with no owner. This story places every new case in a queue and gives it an owner by rule before 07:00 on the morning after case creation, with the rule row and version on a decision log entry. It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016, and serves the business measure "cases inside the service level" (target set with DL22) and control CTL-03.

**Constraints and guardrails:**
- No allocation value is written in code. Product groups, regions, bands, queues, methods, caps and queue codes are read from tables and parameters.
- No personal data in the allocation summary, the logs, the events or the test data. Cases are named by case number only.
- The service never reads tables owned by another module. Rule rows come through RuleTableReader (P4); the decision log through DecisionLogWriter (P7).
- The decision log entry is written in the same transaction as the case change; a failed write leaves the case unchanged.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 020 Allocation and assignment engine v1 v1.md` |
| Requirement IDs | REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016 |
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
| SY-RULES, rules component | Evaluates the allocation table (Rules and parameters R) |
| SY-CASEWF, case workflow module | Updates the case and writes the assignment (Case record CRU; Queue and allocation CRU) |
| SY-DECLOG, decision log writer | Writes the entry (Decision log C) |
| RW-TEAMMGR, team manager | Reads the queue and the allocation summary for their team (Queue and allocation R) |
| RW-CASEOWN, case owner | Reads the cases given to them (Case record R, scope Own) |
| RW-PLATADM, platform administrator | Reruns JOB-03 from the job monitor (Platform administration U) |
| RW-REFADM, reference data administrator | Prepares the allocation table load file; the load is RWB-E1-029 |
| Process owner for L1 18, Shared operations | Approves each allocation table version (reference data change process, step 4). No delegation of authority level applies |

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
- **Feature flag:** `rwb.p3.allocation`. Off: JOB-03 does not run and cases stay NEW.
- **Critical path:** Yes; **depends on:** RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056.
- **Stop signals:** see the epic card; story guardrails are:
  - No allocation value is written in code. Product groups, regions, bands, queues, methods, caps and queue codes are read from tables and parameters.
  - No personal data in the allocation summary, the logs, the events or the test data. Cases are named by case number only.
  - The service never reads tables owned by another module. Rule rows come through RuleTableReader (P4); the decision log through DecisionLogWriter (P7).
  - The decision log entry is written in the same transaction as the case change; a failed write leaves the case unchanged.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 020 Allocation and assignment engine v1 v1.md` |
| Specification | `output/INC-043-epic-1-RWB-E1-020/specify/spec.md` |
| Compliance validation | `output/INC-043-epic-1-RWB-E1-020/specify/compliance-validation.md` |
| Agent run log | `output/INC-043-epic-1-RWB-E1-020/agent-run-log.md` |
| Plan and tasks | `output/INC-043-epic-1-RWB-E1-020/plan/` (TBC) |
| Implementation evidence | `output/INC-043-epic-1-RWB-E1-020/implement/` (TBC) |
| API / functional test reports | `output/INC-043-epic-1-RWB-E1-020/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-043-epic-1-RWB-E1-020/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-043-epic-1-RWB-E1-020/specify/compliance-validation.md`) |
| Acceptance criteria | 13 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 020 Allocation and assignment engine v1 v1.md` |
| Output run | `output/INC-043-epic-1-RWB-E1-020/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
