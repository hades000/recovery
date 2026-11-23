# RWB-P3-E1019-APP Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E1019-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1019-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-008, FR-P3-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-019 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data in rwb-case, loaded from the Excel template through the rwb-case admin endpoints, and served to the engines from rwb-case's own schema**, so that **the organization changes without a code release, even though the roles and permissions it refers to now live in another service**.

The legacy story held the queues, the members, the roles and the lists in one monolith. The D-RCV-60 split keeps the behaviour and moves the ownership:

- **Stays in rwb-case (P3), schema `rwb_case`:** the tables `queue`, `queue_member`, `queue_measure`, `task` and `assignment` (queues, teams, queue membership, queue measures, the work that sits on a queue), and the reference data that describes them: `lov_value`, `reference_row` and `reference_version` (DP-01, DP-07).
- **Moves to rwb-access (P4), schema `rwb_access`:** the Recovery roles, the permission matrix, scope, masking and the delegation-of-authority table. rwb-case reads them through the rwb-access authorise contract and caches the answer (DP-08; contract dependency RWB-P4-E1037-CON; build dependency RWB-PLT-E1037-CON). rwb-case never reads `rwb_access` tables.
- **Stays in rwb-case but is a separate legacy key:** parameters (`parameter_catalog`, `parameter_value`, DP-06; the E1-042 stories). This story reads the parameter `queue.cap.max` through the parameters contract; it does not create the parameter tables.
- **Served at the rwb-case base:** `/api/recovery/case/v1` (DP-13), with the queues, the list of values and the reference loads as the rwb-case admin surface. `GET /admin/roles` is **not** served here: it is a rwb-access operation.
- **Database access:** through the rwb-case login (DP-02). The login name is Not specified in the source documents (GAP-0678; ASM-1225).
- **Events:** the queue and owner codes travel inside `rwb.case.events.v1` on topic naming `rwb.case.<Event>.v1` (DP-14). This story publishes no event of its own; the schemas are contracted in RWB-P3-E1019-CON and the publishing behaviour belongs to RWB-P3-E1020-APP.
- **Screens:** through the gateway-bff composite route (DP-19); this story adds no screen.

### 2. Business rationale

Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. This story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation (RWB-P3-E1020-APP), to scope by team (the rwb-access scope contract) and to control CTL-08.

The realignment does not change that rationale; it changes where the data lives and who may change it. Queues, teams, membership and the measures taken from them are rwb-case data, so the case engines (allocation, transfer, rebalance) read them without a cross-service hop. Roles and permissions are rwb-access data, so one role change reaches every service that authorises, and the queues table keeps only the role **code** it points at. The separation is what makes "no code release" true for the whole organization, not only for the queue table: the queue change is a rwb-case reference load, the role change is a rwb-access change, and the queue load re-checks its role codes against rwb-access on every load.

### 3. Preconditions

- RWB-P3-E1019-CON is published: the OpenAPI 3.1 documents for `/queues`, `/queues/{queueId}/cases`, `/queues/{queueId}/placements`, `/admin/lists/{listCode}` and the two reference-load operations, the AsyncAPI schemas of the `rwb.case.events.v1` events that carry queue and owner codes, and the contract fake. The build runs against the fake from Day 1 (DP-11).
- RWB-P3-E1043-CON and RWB-PLT-E1043-CON are in place: the reference-data contract of rwb-case holds versions of reference tables, `reference_version` and `reference_row` exist in `rwb_case`, and the load and approve operations are served. QUEUE is a LOV-REF-TABLE code and QUEUE_MEMBER is in that list (LOV-REF-TABLE in TSD P3 v3 T3.2).
- The reference approval pattern is in force: an author cannot approve their own load (legacy RWB-E1-038 pattern; control CTL-08).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are in place, so the parameter `queue.cap.max` = 500 (assumed; DL23) is read through the parameters contract, not written in code (DP-06).
- RWB-PLT-E1037-CON and RWB-P4-E1037-CON are in place: the guard library and the rwb-access authorise contract answer role, permission and scope questions, cached, with a 2 s timeout (DP-08). The loader holds RW-REFADM (Reference data C) and the approver holds RW-TEAMMGR with Reference data A (assumed grant; DL01; see GAP-0683; ASM-1230).
- The TEAM versions are in force inside rwb-case reference data: TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK" (assumed codes; owner Shared operations), each with its region code.
- Queue member user IDs are Entra ID object IDs of people who hold the queue's role; rwb-case stores the object ID only, never a name.
- RWB-P3-E1019-DB is tracked separately: the tables and the indexes arrive with that story (external dependency X).
- The per-service login of rwb-case exists in the ACE database. Its name is Not specified in the source documents (GAP-0678; ASM-1225).

### 4. Flow

1. RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls `POST /api/recovery/case/v1/admin/reference-loads` once per sheet with valid from 2026-11-30. The request is `multipart/form-data` (file, table, validFrom) and carries an `Idempotency-Key`. The template format (column order and required columns per sheet) is Not specified in the source documents (GAP-0681; ASM-1228).
2. QueueTableChecks: runs the queue checks on top of the reference-row checks: team code in TEAM, role code in the rwb-access role list, method in LOV-ASSIGN, cap range, overflow queue exists and forms no loop, member holds the queue role. The role checks call the rwb-access contract once per distinct role code and cache the answer.
3. The reference registry: on any failed row refuses the load whole and names every failed row; on a clean file stores the version with status VALIDATED in `reference_version` and `reference_row`.
4. RW-TEAMMGR: approves through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`; refused if the approver is the author. The approver's right is read from the rwb-access authorise contract (Reference data A).
5. QueueVersionApplier: on approval and on rollback, applies the QUEUE and QUEUE_MEMBER versions in force to the `queue` and `queue_member` tables in one transaction: upsert by queue code keeping the queue ID, replace active member rows, set `table_version`. The version in force is re-checked when the service starts, so a restart never leaves a stale queue table. The legacy daily 00:05 sweep is not part of this story: the schedule pattern (DP-10) is not in this story's pattern set.
6. CapacityService: answers capacity questions for the allocation engine from the applied version, as the lower of the member capacity and the queue cap (BR6).
7. QueueMembershipQuery: answers the teams and regions of a user for scope by team; the caller combines it with the rwb-access scope contract.
8. RW-REFADM: if the version is wrong, calls rollback for the load; the previous version is in force again and QueueVersionApplier re-applies it in one transaction. The rollback operation is listed as P3 in the ownership map but is outside the rwb-case operation set given for this story (GAP-0682; ASM-1229); the two legacy criteria that use it are kept and tested against the contract fake.
9. Every step authorises through the guard library, one hop, 2 s timeout (DP-08, DP-11); no step reads another service's tables (DP-01).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A queue names a team code not in TEAM | Load refused in full; the row is named | MSG-P1-002 | AC4 |
| X2 | A cap outside 1 to 500 | Load refused in full | MSG-GEN-002 | AC5 |
| X3 | The approver is the author | Approval refused; version stays VALIDATED | MSG-P7-002 | AC6 |
| X4 | Rollback with no earlier version | Refused; current version unchanged | MSG-P3-015 | AC7 |
| X5 | The same file is loaded again for the same valid from | The existing load is returned; nothing new is written | None | AC8 |
| X6 | Valid from is in the future | The version waits; the current version stays in force until that date | None | AC9 |
| X7 | A member does not hold the queue's role | Load refused in full; the member row is named | MSG-P1-002 | AC10 |
| X8 | Overflow queues form a loop | Load refused in full | MSG-P1-002 | AC11 |
| X9 | A required column is empty | Load refused in full | MSG-GEN-001 | AC12 |
| X10 | A role without Reference data C loads a file | Refused with 403 | MSG-P4-002 | Access test TC-E1-019-13 |
| X11 | The rwb-access contract does not answer inside 2 s | The load is refused with 503 and nothing is written; no role answer is guessed from cache past its time-to-live | MSG-P4-002 | Not a legacy AC; TC-P3-E1019-CON-04 covers the 503 |
| X12 | The queue applies but the member replace fails | The whole apply rolls back; the previous version stays in force | None | Not a legacy AC; TC-P3-E1019-DB-06 covers the rollback |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the rwb-case reference-data and parameter contracts, adds the queue checks, the apply step and two read interfaces; roles arrive over the rwb-access contract |
| Negotiable | Team codes, queues, caps and members are data; the template layout can change with the checks |
| Valuable | A team change takes one load and one approval instead of a release, and a role change no longer touches the queue table |
| Estimable | One check set, one applier, two read services, one contract, one DB story |
| Small | Fits two weeks with its tests, its contract fake and its DB story |
| Testable | Every criterion has a test case in section 16, and every legacy test case is carried |

### 7. Acceptance criteria

```gherkin
Feature: Roles, teams and queues as data

  Background:
    Given TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK"
    Given the loader holds RW-REFADM and the approver holds RW-TEAMMGR
    Given the rwb-access contract mock returns RW-REFADM for the loader and RW-TEAMMGR for the approver

  Scenario: AC1 Tables loaded (legacy RWB-E1-019 AC1)
    Given the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows
    Given the rwb-access contract mock returns role code RW-LITOFF for the litigation officers
    When the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved
    Then 12 queue rows are in force with table version 1
    Then each queue holds its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF
    Then 48 member rows are in force
    Then the reference version holds the author, the approver and the approval time

  Scenario: AC2 Rollback (legacy RWB-E1-019 AC2)
    Given QUEUE version 3 is in force with an error in queue "DIL-BKK-CO"
    Given QUEUE version 2 was in force before it
    When rollback is called once for version 3
    Then QUEUE version 2 is in force for every queue row
    Then each queue keeps its record ID, so cases in the queue keep their queue
    Then the system records the rollback with the caller, the time and the reason

  Scenario: AC3 Capacity (legacy RWB-E1-019 AC3)
    Given member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases
    When a 41st case is offered for U-11
    Then the capacity service answers "AT_CAP" for U-11
    Then names the overflow queue "TDR-BKK-OVF" for the case

  Scenario: AC4 Unknown team code (legacy RWB-E1-019 AC4)
    Given the QUEUE sheet has queue "XYZ-CO" on row 7 with team code "XYZ"
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming row 7 and check "team code not in TEAM"
    Then no queue or member row changes

  Scenario: AC5 Cap outside its range (legacy RWB-E1-019 AC5)
    Given queue "NPA-BKK-CO" has capacity cap 0
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-002 for capacity cap with minimum 1 and maximum 500

  Scenario: AC6 Author cannot approve (legacy RWB-E1-019 AC6)
    Given QUEUE version 4 was loaded by user U-90
    Given the rwb-access contract mock returns RW-TEAMMGR with Reference data A for user U-90
    When U-90 approves it
    Then the system refuses the approval with MSG-P7-002
    Then version 4 stays VALIDATED and is not in force

  Scenario: AC7 Rollback with no earlier version (legacy RWB-E1-019 AC7)
    Given QUEUE version 1 is the only version
    When rollback is called for version 1
    Then the system refuses the call with MSG-P3-015
    Then version 1 stays in force

  Scenario: AC8 The same file loaded twice (legacy RWB-E1-019 AC8)
    Given the QUEUE sheet for valid from 2026-12-15 was loaded as version 5
    When the same file is loaded again for valid from 2026-12-15
    Then the response returns version 5
    Then the system writes no new version

  Scenario: AC9 A version with a future valid from (legacy RWB-E1-019 AC9)
    Given QUEUE version 2 is in force and version 3 is approved with valid from 2026-12-15
    When the capacity service is asked on 2026-12-14
    Then it answers from version 2
    Then on 2026-12-15 it answers from version 3

  Scenario: AC10 Member without the queue role (legacy RWB-E1-019 AC10)
    Given member U-12 on row 22 of the QUEUE_MEMBER sheet is listed on queue "LIT-BKK-OFF" and does not hold RW-LITOFF
    Given the rwb-access contract mock returns that U-12 holds no role code RW-LITOFF
    When the sheet is loaded
    Then the system refuses the load with MSG-P1-002 naming row 22 and check "member does not hold the queue role"

  Scenario: AC11 Overflow loop (legacy RWB-E1-019 AC11)
    Given queue "DS-BKK-CO" overflows to "DS-BKK-OVF" and "DS-BKK-OVF" overflows to "DS-BKK-CO"
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-P1-002 and check "overflow queues form a loop"

  Scenario: AC12 Required column empty (legacy RWB-E1-019 AC12)
    Given queue row 3 has no assignment method
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-001 for assignment method on row 3
```

Every AC above is the legacy AC, value for value, with its origin tag. The only additions are the origin tag on the Scenario line and one "Given the rwb-access contract mock returns ..." line where the AC reaches into rwb-access for a role or a permission; no legacy line was changed or dropped.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every queue belongs to one team and one role | queue.team_code (DF-WRK-004), queue.role_code (DF-WRK-005); LOV-TEAM, LOV-ROLE |
| BR2 | A load with any failed row is refused in full | Reference data change process, step 3; CTL-08 |
| BR3 | A version takes effect on its valid from date after approval; open cases keep the queue they are in | Reference data change process, steps 5 and 6; R-UNI-38 |
| BR4 | The author of a load cannot approve it | Separation of duty table; CTL-08 |
| BR5 | Rollback returns the previous version in one call | Reference data change process, step 7; REQ-CWC-006 |
| BR6 | A person's capacity is the lower of their member capacity and the queue cap | queue.capacity_cap (DF-WRK-007); DL23 |
| BR7 | Assignment method is one of ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL | LOV-ASSIGN |
| BR8 | Cap range 1 to 500 | Parameter `queue.cap.max` = 500 (assumed; DL23), RWB-P3-E1042-CON |
| BR9 | A member must hold the queue's role | The rwb-access role list over the authorise contract (DP-08); legacy ROLE table |

Where each rule lives in the target: nothing in this table changes. What changes is the source of the last one. BR9 is now answered by the rwb-access contract, cached for the life of the call, 2 s timeout, with no read of `rwb_access` tables and no assumption from a stale cache (DP-01, DP-08, DP-11). BR8 is answered by the parameter contract, not by a constant in code (DP-06). BR1, BR3, BR5 and BR6 are answered from `rwb_case` only.

### 9. State transitions

None. This story does not change a case status. It changes the status of a reference version: VALIDATED, APPROVED, ROLLED_BACK, and the table_version applied to the queue rows.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every row passes | VALIDATED |
| VALIDATED | Approve | Approver is not the author | APPROVED; applied on its valid from date |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK; the earlier version is applied |

The version status vocabulary is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) in TSD P3 v3 T3.2; the three states above are the ones this story moves through, and the rest are written by the reference-data story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM | Loads the sheets and calls rollback (Reference data CRUD) |
| RW-TEAMMGR | Approves a queues version as the Shared operations owner (Reference data A, assumed grant; DL01) |
| RW-COE | Reads versions (Reference data CRUD); may load |
| RW-RISK | No part in queue loads; may not hold RW-REFADM (separation of duty) |
| SY-CASEWF | Applies the version on its valid from date and answers capacity and membership questions |
| No delegation of authority level applies | Queue structure is not a credit decision |

Every "who" in this table is a **role code**, and the role codes, their permissions and their separation-of-duty conflicts are held as data in rwb-access (P4). rwb-case asks the rwb-access authorise contract at the start of each operation through the guard library, caches the answer and never reads `rwb_access` tables (DP-01, DP-08; RWB-P4-E1037-CON). The exact column-level split of the legacy role and permission tables between rwb-case and rwb-access is not stated by any source (GAP-0679; ASM-1226); what this story fixes is the boundary: rwb-case keeps the team codes and the role codes, rwb-access keeps the roles and their grants. The approver grant for the queues table (RW-TEAMMGR with Reference data A) is assumed in the legacy story and is carried as an assumption here (GAP-0683; ASM-1230). Table-level authorisation for the reference loads is Reference data C to load, A to approve and U to roll back, per the legacy contract.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-WRK-001 to DF-WRK-008 | queue | all fields | Write |
| DF-WRK-038 | queue | table_version | Write |
| DF-WRK-045 to DF-WRK-052 | queue_member | all fields | Write |
| DF-REF-159 | reference_version | id | Read |
| DF-REF-161 | reference_version | version_no | Read |
| DF-REF-184 | reference_row | row_data | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |

Where the data lives now: `queue`, `queue_member`, `queue_measure`, `assignment`, `task`, `lov_value`, `reference_row` and `reference_version` are in schema `rwb_case`, owned by rwb-case (P3, ownership map). DF-REF-035 (`role.role_code`) is in schema `rwb_access`, owned by rwb-access (P4), and is read over the authorise contract with the role list, never by SQL (DP-01, DP-08). `recovery_case` is read inside `rwb_case`, indexed `ix_case_owner_status`, for the open-case counts behind CapacityService.

Two values are not fixed by any source and are carried as placeholders: the column-level definition of `queue_measure` and of the remaining `lov_value` columns — Not specified in the source documents (GAP-0680; ASM-1227); and the Queues template layout — Not specified in the source documents (GAP-0681; ASM-1228). The legacy physical names are kept: QUEUE, QUEUE_MEMBER, `queue.table_version`, DF-WRK-001 to DF-WRK-008, DF-WRK-045 to DF-WRK-052, DF-REF-028, DF-REF-029.

### 12. Contract

**12.1 REST operations provided**

| Operation | Purpose | Owner (ownership map) |
|---|---|---|
| GET /api/recovery/case/v1/queues | The queue list in force: queue code, name, team code, role code, assignment method, cap, overflow queue, table version | P3 |
| GET /api/recovery/case/v1/admin/lists/{listCode} | One list of values in force, for example LOV-ASSIGN or LOV-REF-TABLE | P3 |
| POST /api/recovery/case/v1/admin/reference-loads | Loads one sheet of the Queues template as a version: multipart file, table, validFrom; `Idempotency-Key` | P3 |
| POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve | Approves a loaded version; refused when the approver is the author | P3 |

`GET /api/recovery/case/v1/admin/roles` is **not** provided by rwb-case: it is a rwb-access (P4) operation. Queue membership and queue measures are read through `GET /api/recovery/case/v1/queues/{queueId}/cases` and the capacity and membership interfaces; the case-list operations are contracted in RWB-P3-E1020-CON.

**12.2 REST operations consumed**

| Operation | Provider | Why | Pattern |
|---|---|---|---|
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | Role, permission and scope answer for the caller and for each role code in a load; cached, one hop, 2 s timeout | DP-08, DP-11 |
| GET /api/recovery/access/v1/admin/roles | rwb-access (P4) | The role list a queue or a member row points at, for the load checks and for the queue list display | DP-08, DP-11 |
| GET /api/recovery/case/v1/admin/parameters/{paramKey} | rwb-case (P3), parameters contract | `queue.cap.max` = 500 (assumed; DL23), read as data | DP-06 |

**12.3 Events published**

None. This story publishes no event. The queue and owner codes travel inside `rwb.case.events.v1` on `rwb.case.CaseAllocated.v1` and `rwb.case.CaseAllocationFailed.v1`; those schemas are contracted in RWB-P3-E1019-CON and published by RWB-P3-E1020-APP (DP-14).

**12.4 Events consumed**

None. A queue change is a synchronous reference load; no event starts it.

**12.5 Workflows and activities**

None. The apply step is a synchronous service step on approval and on rollback, plus a start-up re-check; no Temporal workflow or activity is in this story (DP-10 is not in its pattern set).

**12.6 Schedules**

None. The legacy daily 00:05 job is not carried by this story; the schedule pattern is DP-10, which this story does not apply.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| queue | rwb_case | P3 | Writes every field and `table_version` |
| queue_member | rwb_case | P3 | Writes every field; replaces active rows |
| queue_measure | rwb_case | P3 | Reads; the measure snapshot is taken from the queue and the case counts |
| lov_value | rwb_case | P3 | Reads; lists served through `GET /admin/lists/{listCode}` |
| reference_row | rwb_case | P3 | Writes through the reference registry |
| reference_version | rwb_case | P3 | Writes the version status |
| assignment, task | rwb_case | P3 | Read only, for the member and queue counts |
| role, permission, masking_rule, delegation_limit | rwb_access | P4 | **Never read.** Reached over the rwb-access contract only (DP-01, DP-08) |

Database access uses the rwb-case login (DP-02). Its name is Not specified in the source documents (GAP-0678; ASM-1225). No statement in this story names a table in another schema.

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| rwb-access contract fake (RWB-PLT-E1037-CON, RWB-P4-E1037-CON) | POST /authorise, GET /admin/roles | Every role, permission and approver check, including AC6 and AC10, from Day 1 |
| rwb-case queue and reference fake (RWB-P3-E1019-CON) | GET /queues, GET /admin/lists/{listCode}, POST /admin/reference-loads, POST .../approve | Consumers (gateway-bff, allocation, transfer) build against it before the service is built |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/case/v1` | 3 operations (2 to rwb-access, 1 to the rwb-case parameters contract) | OpenAPI 3.1, one hop, 2 s timeout, `Idempotency-Key` on every POST |
| Kafka | None | None | Queue and owner codes travel in `rwb.case.events.v1`; no produce or consume in this story |
| Temporal | None | None | No workflow, activity or schedule in this story |
| File | 1 (the Queues template as `multipart/form-data` on the load operation) | 0 | The file is read in the request; no claim-check store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case.queues`, with the published types in `...case.queues.api`. Service base `/api/recovery/case/v1`, schema `rwb_case`, topic `rwb.case.events.v1`, Temporal task queue `rwb-case` (not used by this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| QueueTableChecks | Service | Reference-table check for QUEUE and QUEUE_MEMBER: team, role, method, cap range, overflow loop, member role |
| QueueVersionApplier | Service | Applies the QUEUE and QUEUE_MEMBER versions in force to `queue` and `queue_member` on approval, on rollback and at start-up, in one transaction |
| CapacityService | Published interface | Open cases against capacity for the applied version; the lower of member capacity and queue cap |
| QueueMembershipQuery | Published interface | Teams, regions and queues of a user, for scope |
| ReferenceRollbackHandler | Service | Marks the version ROLLED_BACK through the registry and triggers the applier |
| CaseAndWorkflowRepository | Repository | `queue`, `queue_member`, open case counts; no cross-schema SQL |
| AccessGuardClient | Client | The rwb-access authorise contract through the guard library: cached, one hop, 2 s timeout (DP-08, DP-11) |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Database**

- Writes `queue` (all columns plus `table_version`) and `queue_member`; reads `queue_measure`, `lov_value`, `reference_row`, `reference_version`, `assignment`, `task`.
- Reads `recovery_case` (`owner_user_id`, `queue_id`, `status`) for open case counts, index `ix_case_owner_status`.
- The tables, keys and indexes arrive with RWB-P3-E1019-DB, on the per-service Flyway sequence after the V0001 baseline (DP-15). The legacy migration `V019_1__queue_member.sql` maps into that sequence; no monolith migration name is reused.
- DB access uses the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0678; ASM-1225). No grant on `rwb_access` and no grant to any other service's login.

**Configuration and reference data**

- TEAM, ROLE, QUEUE and QUEUE_MEMBER through the rwb-case reference registry (DP-07, DP-15); LOV-ASSIGN through `GET /admin/lists/{listCode}`.
- Parameter `queue.cap.max` = 500 (assumed; DL23) from the rwb-case parameters contract (DP-06).
- The Queues template, owned by Shared operations; its layout is Not specified in the source documents (GAP-0681; ASM-1228).
- Role codes and the approver grant from rwb-access (DP-08), cached, 2 s timeout.

**Build steps**

1. QueueTableChecks with one check per rule; unit tests for AC4, AC5, AC10, AC11, AC12, with the rwb-access fake answering the role questions.
2. Register the checks for QUEUE and QUEUE_MEMBER on the reference contract; test AC8 through the registry's idempotency.
3. Approval through the registry, authorised by the rwb-access guard; test AC6.
4. QueueVersionApplier: upsert queues by queue code keeping the ID, replace member rows in one transaction; tests AC1, AC9.
5. ReferenceRollbackHandler and the rollback path; tests AC2, AC7 against the contract fake.
6. CapacityService with the lower of member capacity and queue cap; test AC3.
7. QueueMembershipQuery for scope.
8. Access test on the load operation (TC-E1-019-13), and the 2 s timeout path (X11).

**Feature flag.** `rwb.case.queuetables`, from the platform flag library. Off: the applier does not run and the queue rows from the seed migration stay.

**Done when.** The tests in section 16 pass; the SIT queue set for six teams loads, approves and applies; the rwb-access fake answers every role check; and no statement in the service names a table outside `rwb_case`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A queue check fails on a row (team code, member role, overflow loop) | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Required column empty, or no rollback reason | Enter {field}. |
| MSG-GEN-002 | Cap outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The message IDs and texts are the legacy ones, unchanged. MSG-P4-002 is now raised by the rwb-access guard library, so the refusal is identical in every service. A refusal from the rwb-access contract (no answer inside 2 s) returns 503 with no message body from this service and writes nothing (X11). Field-level validation is answered as a 422 with the failing rows in the problem detail, per the contract in RWB-P3-E1019-CON.

### 15. Screens and states

No screen in this story. The administrator loads by file through the reference load operation; SCR-42 Queues and service levels (states Versions; load) comes in Epic 8 and reaches rwb-case through the gateway-bff composite route (DP-19). The result of each load is returned as the ReferenceLoad response: id, table, validFrom, status, rows.

States the operator sees on a version: VALIDATED (loaded, checked, waiting for approval), APPROVED (approved and waiting for, or on, its valid from date) and ROLLED_BACK (superseded by its predecessor). A version with a future valid from date shows APPROVED and does not change any queue row until that date (AC9).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-019-13 | Access | Component | RW-CASEOWN calls POST /admin/reference-loads and is refused with MSG-P4-002 |
| TC-E1-019-01 | AC1, BR1, BR3 | End to end | Template with 12 queues and 48 members |
| TC-E1-019-02 | AC2, BR5 | End to end | QUEUE versions 2 and 3 |
| TC-E1-019-03 | AC3, BR6 | End to end | Member U-11 with capacity 40 and 40 open cases |
| TC-E1-019-04 | AC4, BR2 | End to end | Queue with team code XYZ |
| TC-E1-019-05 | AC5, BR8 | End to end | Cap 0 |
| TC-E1-019-06 | AC6, BR4 | End to end | Load and approval by U-90 |
| TC-E1-019-07 | AC7, BR5 | End to end | Only one version |
| TC-E1-019-08 | AC8 | End to end | Same file twice for 2026-12-15 |
| TC-E1-019-09 | AC9, BR3 | End to end | Version 3 with valid from 2026-12-15 |
| TC-E1-019-10 | AC10, BR9 | End to end | Member U-12 without RW-LITOFF |
| TC-E1-019-11 | AC11, BR2 | End to end | Overflow loop between DS-BKK-CO and DS-BKK-OVF |
| TC-E1-019-12 | AC12, BR2 | End to end | Row 3 with no assignment method |

The legacy TC IDs, Covers and Data are kept character for character. The legacy Level "System" maps to "End to end" and "Access" maps to "Component", because the access test now exercises the guard library and the rwb-access contract fake in one component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: team codes, queue codes, methods, caps and members are data; the cap range comes from the parameter `queue.cap.max` (DP-06).
- No personal data in logs, tests or prompts; members are named by user ID only, and no name is stored in `queue_member`.
- No read of another schema: roles, permissions and scope through the rwb-access contract (DP-01, DP-08); lists and versions through the rwb-case reference contract (DP-07); ACE data only through its owner's contract or the `v_ace_*` views.
- One hop and 2 s timeout on every call; a slow rwb-access answer refuses the load and writes nothing (DP-11).
- A version applies whole or not at all; the queue record ID never changes, so `recovery_case.queue_id` stays valid.
- No event carries a personal name; the queue and owner codes travel in `rwb.case.events.v1` under the schema of RWB-P3-E1019-CON (DP-14).
- The queue tables are in `rwb_case` only; the rwb-case login is the only grantee, and its name is Not specified in the source documents (GAP-0678; ASM-1225).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-06 | All recovery processes | R-UNI-38 | TC-E1-019-01 to TC-E1-019-12 |
| REQ-ACA-002 | Roles held as data; a change without a release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03 | All recovery processes | None | TC-E1-019-01, TC-E1-019-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1019-CON | Contract | H build dependency: the OpenAPI 3.1 and AsyncAPI documents and the contract fake |
| RWB-P3-E1019-DB | ACE DB | X external dependency: the tables, keys, indexes and grants |
| RWB-P3-E1043-CON, RWB-PLT-E1043-CON | Contract | H: the reference-data contract and the version store |
| RWB-P3-E1042-CON, RWB-PLT-E1042-CON | Contract | H: the parameters contract, `queue.cap.max` |
| RWB-PLT-E1037-CON | Contract | H: the guard library |
| RWB-P4-E1037-CON | Contract | C: the rwb-access authorise and roles contract this story calls |
| RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON | Contract | H: Flyway sequence, topic naming, gateway-bff composite route |
| RWB-P3-E1020-APP, RWB-P3-E1021-APP | App development | Consumers: allocation and transfer read the applied queue version |

### 19. Out of scope

- The role list, the permission matrix, scope, masking and the delegation-of-authority table themselves: these are rwb-access (P4) and the E1-022, E1-037 and E1-038 legacy content.
- The reference version store and the load and approve operations themselves: RWB-P3-E1043-CON and its DB story.
- The parameter tables `parameter_catalog` and `parameter_value`: the E1-042 stories.
- Allocation and assignment by these tables: RWB-P3-E1020-APP.
- Publishing queue measures to the case list and to reporting (FEAT-CWC-18): the table and its indexes only here.
- Administration screens for queues (Epic 8, SCR-42).
- Reallocation when an owner leaves (Epic 2, R-UNI-18).
- The rollback and verify operations for reference loads: listed as P3 in the ownership map but outside the rwb-case operation set given for this story (GAP-0682; ASM-1229).
