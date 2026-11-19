# Increment Card — INC-030-epic-1-RWB-E1-019

**RWB-E1-019 — Roles, teams and queues as data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-030` |
| Title | Roles, teams and queues as data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-019` |
| RUN_ID | `INC-030-epic-1-RWB-E1-019` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-038, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template**, so that **the organization changes without a code release**.

**Main flow:**
1. RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls POST /admin/reference-loads once per sheet with valid from 2026-11-30.
2. QueueTableChecks: runs the queue checks on top of the RWB-E1-043 row checks: team code in TEAM, role code in ROLE, method in LOV-ASSIGN, cap range, overflow queue exists and forms no loop, member holds the queue role.
3. ReferenceVersionRegistry (RWB-E1-043): on any failed row refuses the load whole and names every failed row; on a clean file stores the version with status VALIDATED.
4. RW-TEAMMGR: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.
5. QueueVersionApplier: on the valid from date, applies the QUEUE and QUEUE_MEMBER versions in force to the queue and queue_member tables: upsert by queue code keeping the queue ID, replace active member rows, set table_version.
6. CapacityService: answers capacity questions for the allocation engine from the applied version.

**Out of scope:**
- The role list and the permission matrix themselves (RWB-E1-022, RWB-E1-037).
- The reference version store and the load endpoint (RWB-E1-043).
- Allocation and assignment by these tables (RWB-E1-020).
- Administration screens for queues (Epic 8, SCR-42).
- Reallocation when an owner leaves (Epic 2, R-UNI-18).

**Business outcome and value hypothesis:** Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. This story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation (RWB-E1-020), to scope by team (RWB-E1-037) and to control CTL-08.

**Constraints and guardrails:**
- No business value in code: team codes, queue codes, methods, caps and members are data.
- No personal data in logs, tests or prompts; members are named by user ID only.
- No read of another module's tables: roles and lists through P4 interfaces; versions through ReferenceDataService.
- A version applies whole or not at all; the queue record ID never changes, so recovery_case.queue_id stays valid.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 019 Roles teams and queues as data v1.md` |
| Requirement IDs | REQ-CWC-006, REQ-ACA-002 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
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
| RW-REFADM | Loads the sheets and calls rollback (Reference data CRUD) |
| RW-TEAMMGR | Approves a queues version as the Shared operations owner (Reference data A, assumed grant; DL01) |
| RW-COE | Reads versions (Reference data CRUD); may load |
| RW-RISK | No part in queue loads; may not hold RW-REFADM (separation of duty) |
| SY-CASEWF | Applies the version on its valid from date and answers capacity and membership questions |
| No delegation of authority level applies | Queue structure is not a credit decision |

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
- **Feature flag:** `rwb.p3.queuetables`. Off: the applier does not run and the queue rows from the seed migration stay.
- **Critical path:** Yes; **depends on:** RWB-E1-038, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: team codes, queue codes, methods, caps and members are data.
  - No personal data in logs, tests or prompts; members are named by user ID only.
  - No read of another module's tables: roles and lists through P4 interfaces; versions through ReferenceDataService.
  - A version applies whole or not at all; the queue record ID never changes, so recovery_case.queue_id stays valid.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 019 Roles teams and queues as data v1.md` |
| Specification | `output/INC-030-epic-1-RWB-E1-019/specify/spec.md` |
| Compliance validation | `output/INC-030-epic-1-RWB-E1-019/specify/compliance-validation.md` |
| Agent run log | `output/INC-030-epic-1-RWB-E1-019/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-030-epic-1-RWB-E1-019/plan/` (TBC) |
| Implementation evidence | `output/INC-030-epic-1-RWB-E1-019/implement/` (TBC) |
| API / functional test reports | `output/INC-030-epic-1-RWB-E1-019/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-030-epic-1-RWB-E1-019/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-030-epic-1-RWB-E1-019/specify/compliance-validation.md`) |
| Acceptance criteria | 12 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 019 Roles teams and queues as data v1.md` |
| Output run | `output/INC-030-epic-1-RWB-E1-019/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
