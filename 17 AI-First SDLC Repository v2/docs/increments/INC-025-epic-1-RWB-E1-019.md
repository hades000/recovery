# Increment Card — INC-025-epic-1-RWB-E1-019

**RWB-E1-019 — Roles, teams and queues as data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-025` |
| Title | Roles, teams and queues as data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-019` |
| RUN_ID | `INC-025-epic-1-RWB-E1-019` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 25 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-038, RWB-E1-043 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template**, so that **the organization changes without a code release**.

**Business outcome:** Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. This story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation (RWB-E1-020), to scope by team (RWB-E1-037) and to control CTL-08.

**Main flow:**
1. RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls POST /admin/reference-loads once per sheet with valid from 2026-11-30.
2. QueueTableChecks: runs the queue checks on top of the RWB-E1-043 row checks: team code in TEAM, role code in ROLE, method in LOV-ASSIGN, cap range, overflow queue exists and forms no loop, member holds the queue role.
3. ReferenceVersionRegistry (RWB-E1-043): on any failed row refuses the load whole and names every failed row; on a clean file stores the version with status VALIDATED.
4. RW-TEAMMGR: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.
5. QueueVersionApplier: on the valid from date, applies the QUEUE and QUEUE_MEMBER versions in force to the queue and queue_member tables: upsert by queue code keeping the queue ID, replace active member rows, set table_version.
6. CapacityService: answers capacity questions for the allocation engine from the applied version.

**Acceptance criteria:**
- AC1: Tables loaded
- AC2: Rollback
- AC3: Capacity
- AC4: Unknown team code
- AC5: Cap outside its range
- AC6: Author cannot approve
- AC7: Rollback with no earlier version
- AC8: The same file loaded twice
- AC9: A version with a future valid from
- AC10: Member without the queue role
- AC11: Overflow loop
- AC12: Required column empty

**Out of scope:**
- The role list and the permission matrix themselves (RWB-E1-022, RWB-E1-037).
- The reference version store and the load endpoint (RWB-E1-043).
- Allocation and assignment by these tables (RWB-E1-020).
- Administration screens for queues (Epic 8, SCR-42).
- Reallocation when an owner leaves (Epic 2, R-UNI-18).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-019-roles-teams-and-queues-as-data-v1.md` |
| Requirement IDs | REQ-CWC-006, REQ-ACA-002 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
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
| RW-REFADM | Loads the sheets and calls rollback (Reference data CRUD) |
| RW-TEAMMGR | Approves a queues version as the Shared operations owner (Reference data A, assumed grant; DL01) |
| RW-COE | Reads versions (Reference data CRUD); may load |
| RW-RISK | No part in queue loads; may not hold RW-REFADM (separation of duty) |
| SY-CASEWF | Applies the version on its valid from date and answers capacity and membership questions |
| No delegation of authority level applies | Queue structure is not a credit decision |

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint, RWB-E1-043) | Item | Value | |---|---| | Request | multipart/form-data: file (xlsx sheet), table = "QUEUE" or "QUEUE_MEMBER", validFrom (date) | | Response | 201 ReferenceLoad: id, table, validFrom, status, rows | | Errors | 401 (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 422 a row fails (MSG-GEN-001, MSG-GEN-002; queue checks as MSG-P1-002 with the rows in Problem.detail); 503 | | Authorization | Reference data, right C | | Idempotency | Table code, valid from and content hash (RWB-E1-043) | **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint) | Item | Value | |---|---| | Response | 200 ReferenceLoad with status APPROVED | | Errors | 401; 403 no Reference data A; 404; 409 approver is the author (MSG-P7-002) or the version changed (MSG-GEN-004); 503 | | Authorization | Reference data, right A…

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

- No business value in code: team codes, queue codes, methods, caps and members are data. - No personal data in logs, tests or prompts; members are named by user ID only. - No read of another module's tables: roles and lists through P4 interfaces; versions through ReferenceDataService. - A version applies whole or not at all; the queue record ID never changes, so recovery_case.queue_id stays valid.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-019-roles-teams-and-queues-as-data-v1.md` |
| Specification | `output/INC-025-epic-1-RWB-E1-019/specify/spec.md` |
| Compliance validation | `output/INC-025-epic-1-RWB-E1-019/specify/compliance-validation.md` |
| Agent run log | `output/INC-025-epic-1-RWB-E1-019/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-025-epic-1-RWB-E1-019/plan/` |
| Implementation evidence | `output/INC-025-epic-1-RWB-E1-019/implement/` |
| API / functional test reports | `output/INC-025-epic-1-RWB-E1-019/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-025-epic-1-RWB-E1-019/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-019-roles-teams-and-queues-as-data-v1.md` |
| Output run | `output/INC-025-epic-1-RWB-E1-019/` |

