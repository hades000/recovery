# Technical Specification — RWB-E1-019 Roles, teams and queues as data

| Field | Value |
|---|---|
| Story | RWB-E1-019 — Roles, teams and queues as data |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-030-epic-1-RWB-E1-019` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-005, FR-RWB-012); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 019 Roles teams and queues as data v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-004; FR-RWB-005, FR-RWB-012; REQ-CWC-006, REQ-ACA-002; US-RWB-E1-019; CTX-FEATURE-003; CTL-08; R-UNI-38; DF-WRK-001..008, DF-WRK-045..052 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The administrator loads by file; SCR-42 Queues and service levels is Epic 8. |
| Logic In Scope | `YES` — queue checks, version apply, capacity, membership, rollback and effective dating. |
| API In Scope | `NO` — no new or changed contract. The story reuses `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve` and `POST /admin/reference-loads/{loadId}/rollback` (P4, delivered by RWB-E1-043). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `queue` (EXTEND ACE work queue); `queue_member` (new); `recovery_case` open-case counts; RWB-E1-043 registry; RWB-E1-037 scope query. |
| New Nodes Required | `YES` — `QueueTableChecks`, `QueueVersionApplier`, `CapacityService`, `QueueMembershipQuery`, `ReferenceRollbackHandler`, `queue_member` table and `queue.table_version`. |
| Inherited Existing Behavior | RWB-E1-043 versioned reference store and load/approve/rollback endpoints; RWB-E1-038 approval pattern; RWB-E1-042 `queue.cap.max`; RWB-E1-020 allocation consumer. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every queue belongs to one team and one role. | SPEC-RWB-E1-019-001, SPEC-RWB-E1-019-002 | DIRECT | `queue.team_code`, `queue.role_code`; both checked against the version in force. | COVERED |
| BR2 | A load with any failed row is refused in full. | SPEC-RWB-E1-019-003 | DIRECT | `QueueTableChecks` returns every failed row; registry writes nothing. | COVERED |
| BR3 | A version takes effect on its valid from date after approval; open cases keep the queue they are in. | SPEC-RWB-E1-019-005, SPEC-RWB-E1-019-008 | DIRECT | Applier upserts by queue code and keeps the queue ID. | COVERED |
| BR4 | The author of a load cannot approve it. | SPEC-RWB-E1-019-004 | DIRECT | Registry approval check; MSG-P7-002. | COVERED |
| BR5 | Rollback returns the previous version in one call. | SPEC-RWB-E1-019-007 | DIRECT | Registry rollback plus applier in one transaction. | COVERED |
| BR6 | A person's capacity is the lower of their member capacity and the queue cap. | SPEC-RWB-E1-019-006 | DIRECT | `CapacityService`; cap and member capacity are data. | COVERED |
| BR7 | Assignment method is one of ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL. | SPEC-RWB-E1-019-002 | DIRECT | LOV-ASSIGN check. | COVERED |
| BR8 | Cap range is 1 to 500. | SPEC-RWB-E1-019-002 | DIRECT | `queue.cap.max` = 500 (assumed; DL23); minimum 1. | COVERED |
| BR9 | A member must hold the queue's role. | SPEC-RWB-E1-019-002 | DIRECT | ROLE table plus P4 role directory check. | COVERED |
| AC1 | 12 queues and 48 members load as version 1 from 2026-11-30 and are approved; each queue holds team and role; the version holds author, approver and time. | SPEC-RWB-E1-019-001, SPEC-RWB-E1-019-005 | DIRECT | LIT-BKK-OFF / LIT-BKK / RW-LITOFF example. | COVERED |
| AC2 | Rollback of version 3 returns version 2 for every queue, keeps each queue ID and records caller, time and reason. | SPEC-RWB-E1-019-005, SPEC-RWB-E1-019-007 | DIRECT | Queue IDs stable. | COVERED |
| AC3 | A member at capacity 40 with 40 open cases answers AT_CAP and names the overflow queue. | SPEC-RWB-E1-019-006, SPEC-RWB-E1-019-010 | DIRECT | TDR-BKK-CO / TDR-BKK-OVF. | COVERED |
| AC4 | An unknown team code refuses the load naming row 7 and the check; nothing changes. | SPEC-RWB-E1-019-002, SPEC-RWB-E1-019-003 | DIRECT | MSG-P1-002. | COVERED |
| AC5 | A cap of 0 refuses the load with minimum 1 and maximum 500. | SPEC-RWB-E1-019-002 | DIRECT | MSG-GEN-002. | COVERED |
| AC6 | The author cannot approve; version 4 stays VALIDATED and is not in force. | SPEC-RWB-E1-019-004 | DIRECT | MSG-P7-002. | COVERED |
| AC7 | Rollback of the only version is refused and version 1 stays in force. | SPEC-RWB-E1-019-007 | DIRECT | MSG-P3-015. | COVERED |
| AC8 | The same file for the same valid from returns version 5 and writes no new version. | SPEC-RWB-E1-019-009 | DIRECT | Registry idempotency. | COVERED |
| AC9 | A future version 3 is not used on 2026-12-14 but is used on 2026-12-15. | SPEC-RWB-E1-019-005, SPEC-RWB-E1-019-008 | DIRECT | Capacity reads the applied version for the date. | COVERED |
| AC10 | A member without the queue role refuses the load naming row 22 and the check. | SPEC-RWB-E1-019-002, SPEC-RWB-E1-019-003 | DIRECT | MSG-P1-002. | COVERED |
| AC11 | An overflow loop refuses the load with the loop check. | SPEC-RWB-E1-019-002, SPEC-RWB-E1-019-003 | DIRECT | DS-BKK-CO / DS-BKK-OVF. | COVERED |
| AC12 | A missing assignment method refuses the load naming row 3. | SPEC-RWB-E1-019-002, SPEC-RWB-E1-019-003 | DIRECT | MSG-GEN-001. | COVERED |
| X1..X10 | Exceptional paths in the table below map to SPEC-002..009 and the access rule. | SPEC-RWB-E1-019-002..009 | DIRECT | Team, cap, author, rollback, duplicate, future, member role, loop, required, access. | COVERED |

## User story intent interpretation

As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template**, so that **the organization changes without a code release**.

The story turns the queue structure into data. It adds the queue checks on top of the RWB-E1-043 row checks, applies an approved version to the queue tables the engines read, and answers two questions for the rest of the module: can this person take another case, and which teams, regions and queues does this user belong to.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/reference-loads` for `QUEUE` or `QUEUE_MEMBER`; approval; rollback; daily applier at 00:05; capacity or membership query. |
| Preconditions | RWB-E1-043 done and `QUEUE` is a LOV-REF-TABLE code; `QUEUE_MEMBER` added to the list; RWB-E1-038 approval pattern in use; ROLE and TEAM have a version in force; loader holds RW-REFADM; approver holds Reference data A; member user IDs are Entra ID object IDs. |
| Input | Queues template (QUEUE and QUEUE_MEMBER sheets), valid from, caller identity, queue ID and user ID for queries. |
| Output | `queue` and `queue_member` rows with `table_version`; capacity answers; membership; rollback record. |
| Feature flag | `rwb.p3.queuetables`. Off: the applier does not run and the seed queue rows stay. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `queue` | `queue_code` | QUEUE sheet | New version only | Unique; the code is the stable key across versions. |
| `queue` | `queue_name`, `team_code`, `role_code` | QUEUE sheet | New version only | Team and role must exist in the versions in force. |
| `queue` | `assignment_method` | QUEUE sheet | New version only | LOV-ASSIGN: ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL. |
| `queue` | `capacity_cap` | QUEUE sheet | New version only | 1..`queue.cap.max` (500 assumed; DL23). |
| `queue` | `overflow_queue_id` | QUEUE sheet | New version only | Must exist and form no loop. |
| `queue` | `table_version` | Applier | System-written | Version number of the applied QUEUE version. |
| `queue_member` | `queue_id`, `user_id`, `capacity`, `skill_codes` | QUEUE_MEMBER sheet | New version only | Member must hold the queue role; capacity is data. |
| `queue_member` | `table_version`, `valid_from`, `valid_to` | Applier | System-written | Active rows only; replaced whole on apply. |
| `recovery_case` | `queue_id`, `owner_user_id`, `status` | Existing case | Read-only | Used for open-case counts; status other than CLOSED is open. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every row passes | VALIDATED | Version and rows stored; not applied. |
| None | Load | Any row fails | Not written | Load refused in full; failed rows named. |
| VALIDATED | Approve | Approver not author, holds A | APPROVED | Applied on the valid from date. |
| APPROVED | Valid from reached | Date reached | Applied | Queue and member rows upserted; `table_version` set. |
| APPROVED | Rollback | Earlier approved version exists | ROLLED_BACK | Earlier version re-applied in one transaction. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Queue names a team code not in TEAM | Load refused; row named | MSG-P1-002 |
| X2 | Cap outside 1..500 | Load refused | MSG-GEN-002 |
| X3 | Approver is the author | Approval refused; version stays VALIDATED | MSG-P7-002 |
| X4 | Rollback with no earlier version | Refused; current version stays | MSG-P3-015 |
| X5 | Same file for the same valid from | Existing load returned; nothing written | None |
| X6 | Valid from in the future | Version waits; current version stays | None |
| X7 | Member does not hold the queue role | Load refused; member row named | MSG-P1-002 |
| X8 | Overflow queues form a loop | Load refused | MSG-P1-002 |
| X9 | Required column empty | Load refused | MSG-GEN-001 |
| X10 | Role without Reference data C loads a file | 403; nothing written | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /admin/reference-loads` (table QUEUE or QUEUE_MEMBER); `POST /admin/reference-loads/{loadId}/approve`; `POST /admin/reference-loads/{loadId}/rollback`. |
| Contract delta | None. The P4 endpoints already accept a table code and valid from, return `ReferenceLoad`, and the rollback accepts a reason. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; A to approve; U to roll back. 401 MSG-P4-001; 403 MSG-P4-002; 404; 409 MSG-P7-002/MSG-P3-015/MSG-GEN-004; 422 MSG-GEN-001/MSG-GEN-002/MSG-P1-002; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-42 is Epic 8. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-005, FR-RWB-012; SPEC-RWB-E1-019-001..013 | New checks, applier, capacity service, membership query and rollback handler. | Positive, negative, boundary and error-path tests: 12 queues/48 members, team, cap 0/1/500, member role, loop, author, rollback, duplicate, future version, capacity boundary. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `QueueTableChecks` | Service | `ReferenceTableCheck` for QUEUE and QUEUE_MEMBER: team, role, method, cap, overflow loop, member role. |
| `QueueVersionApplier` | Job | Daily at 00:05 and on approval or rollback, applies the versions in force to `queue` and `queue_member`. |
| `CapacityService` | Published interface | Open cases against capacity for the applied version. |
| `QueueMembershipQuery` | Published interface | Teams, regions and queues of a user, for scope (RWB-E1-037). |
| `ReferenceRollbackHandler` | Service | Marks the version ROLLED_BACK through the registry and triggers the applier. |
| `CaseAndWorkflowRepository` | Repository | `queue`, `queue_member`, open-case counts. |

### Package and boundaries

`recovery.casewf.queues`, published types in `recovery.casewf.queues.api`. TEAM, ROLE, QUEUE and
QUEUE_MEMBER are read through `ReferenceDataService` (RWB-E1-043); LOV-ASSIGN through the P4 list
interface; `recovery_case` is read only for open-case counts in the module's own repository.

### Data and migration

`V019_1__queue_member.sql` creates `queue_member` (`id`, `queue_id`, `user_id`, `capacity`,
`skill_codes`, `table_version`, `valid_from`, `valid_to`, standard columns; index on `queue_id` where
`is_active`; index on `user_id` where `is_active`) and adds `queue.table_version`. The queue table
already exists as an ACE work queue; the story writes its recovery columns.

### Checks

1. Team code exists in the TEAM version in force.
2. Role code exists in the ROLE version in force.
3. Assignment method in LOV-ASSIGN.
4. Cap in 1..`queue.cap.max`.
5. Overflow queue exists and the overflow chain forms no loop.
6. Every member holds the queue's role (ROLE table plus P4 role directory).
7. Required columns present.

Any failed row refuses the whole load and names every failed row; the registry writes nothing.

### Apply and capacity

- The applier upserts each queue by `queue_code` and keeps the existing `queue_id`, so
  `recovery_case.queue_id` stays valid.
- It replaces the active `queue_member` rows for each queue and sets `table_version`.
- `CapacityService.check(queueId, userId, onDate)` counts open cases (status other than CLOSED) and
  compares them with the lower of member capacity and queue cap. It returns `BELOW_CAP` or `AT_CAP`
  and the overflow queue ID.
- `QueueMembershipQuery.membershipOf(userId, onDate)` returns team codes, region codes and queue IDs
  for scope.

### Rollback and effective dating

- Approval sets the version APPROVED; the applier runs on the valid from date and on approval or
  rollback.
- Rollback marks the later version ROLLED_BACK, makes the previous version in force, and re-applies it
  in one transaction; the queue ID is unchanged.
- A future version is approved but not applied until its valid from date.

### Transaction and events

The apply is one transaction: all queues and members change or none. No event is published; the
allocation engine reads `CapacityService` at run time.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data CRUD; loads and rolls back | All |
| RW-TEAMMGR | Reference data A as the Shared operations owner (assumed; DL01) | Team |
| RW-COE | Reference data CRUD; may load | All |
| RW-RISK | No part in queue loads; may not hold RW-REFADM | All |
| SY-CASEWF | Applies the version and answers capacity/membership | All |

A role without Reference data C receives 403 MSG-P4-002.

### Observability and operations

- Load response: status, row count, each failed row and check.
- Applier run: version, queue count, member count, duration, result.
- Metrics: loads, refusals by check, applies, rollbacks, capacity queries, AT_CAP count.
- Alert: applier failed; a queue in force has no members.

### Performance

- 12 queues and 48 members in the SIT set; the apply is a small batch.
- Capacity counts use `ix_case_owner_status` on `recovery_case`.
- Membership is cached per user and date for the scope query.

### Feature flag and rollback

- `rwb.p3.queuetables`: off means the applier does not run and the seed queue rows stay.
- Rollback: turn the flag off; redeploy the previous tag. A queue version rollback is a data action.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-019-01 | AC1, BR1, BR3 | System | 12 queues, 48 members, version 1 | 12 and 48 rows in force; author/approver recorded |
| TC-E1-019-02 | AC2, BR5 | System | QUEUE versions 2 and 3 | Version 2 in force; queue IDs unchanged; rollback recorded |
| TC-E1-019-03 | AC3, BR6 | System | U-11 capacity 40, 40 open cases | AT_CAP; overflow TDR-BKK-OVF |
| TC-E1-019-04 | AC4, BR2 | System | Queue team XYZ on row 7 | Refused; row 7 and check named |
| TC-E1-019-05 | AC5, BR8 | System | Cap 0 | Refused; 1 and 500 named |
| TC-E1-019-06 | AC6, BR4 | System | U-90 loads and approves | Refused; version VALIDATED |
| TC-E1-019-07 | AC7, BR5 | System | Only version 1 | Refused; version 1 stays |
| TC-E1-019-08 | AC8 | System | Same file for 2026-12-15 twice | Version 5 returned; no new version |
| TC-E1-019-09 | AC9, BR3 | System | Version 3 from 2026-12-15 | Version 2 on 14th; version 3 on 15th |
| TC-E1-019-10 | AC10, BR9 | System | U-12 without RW-LITOFF on row 22 | Refused; row 22 named |
| TC-E1-019-11 | AC11, BR2 | System | DS-BKK-CO and DS-BKK-OVF loop | Refused; loop check |
| TC-E1-019-12 | AC12, BR2 | System | Row 3 without assignment method | Refused; MSG-GEN-001 |
| TC-E1-019-13 | X10 | Security | RW-CASEOWN loads a file | 403; MSG-P4-002 |

## Guardrails and out of scope

- No business value in code: team codes, queue codes, methods, caps and members are data.
- No personal data in logs, tests or prompts; members are named by user ID only.
- Roles and lists are read through P4 interfaces; versions through `ReferenceDataService`.
- A version applies whole or not at all; the queue record ID never changes.
- Out of scope: the role list and permission matrix (RWB-E1-022, RWB-E1-037); the reference version
  store and load endpoint (RWB-E1-043); allocation and assignment (RWB-E1-020); queue screens
  (Epic 8, SCR-42); reallocation when an owner leaves (Epic 2, R-UNI-18).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-004 | Who holds Reference data A for queues? | Approval cannot proceed without an approver. | Assume RW-TEAMMGR as the Shared operations owner (DL01); the grant is loaded through RWB-E1-037. | RESOLVED | SPEC-004 |
| CLAR-002 | §3; SPEC-002 | Are the TEAM codes TDR-BKK, DIL-BKK, LIT-BKK, NPA-BKK, DS-BKK and WO-BKK final? | They are test fixtures. | Assumed codes; the values are data and load through TEAM. | RESOLVED | SPEC-002 |
| CLAR-003 | BR8, AC5; SPEC-002 | Is 500 the maximum cap? | Boundary. | `queue.cap.max` = 500 (assumed; DL23); minimum 1. | RESOLVED | SPEC-002 |
| CLAR-004 | §13; SPEC-001 | Does this story create the queue table? | Migration scope. | No; `queue` is an existing ACE work queue. The story adds `queue.table_version` and creates `queue_member`. | RESOLVED | SPEC-001 |
| CLAR-005 | BR9; SPEC-002 | Is the member-role check against ROLE or the P4 role directory? | Two sources could disagree. | Both: ROLE defines the role; the P4 directory confirms the person holds it. | RESOLVED | SPEC-002 |
| CLAR-006 | X8; SPEC-002 | How deep is the overflow loop check? | A cycle can be longer than two queues. | Walk the overflow chain to its end; any revisit is a loop. | RESOLVED | SPEC-002 |
| CLAR-007 | AC2; SPEC-007 | Does rollback re-apply immediately? | Timing. | Yes; the applier runs in the same transaction as the rollback. | RESOLVED | SPEC-007 |
| CLAR-008 | BR6; SPEC-006 | What counts as an open case? | Capacity boundary. | A case in the queue owned by the person with status other than CLOSED, as in RWB-E1-020. | RESOLVED | SPEC-006 |
| CLAR-009 | §12; SPEC-012 | Does the story need a new endpoint? | Contract delta. | No; it uses the RWB-E1-043 load, approve and rollback endpoints. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 9 items are answered from the story, the data model or the
reference data pattern. The approver grant is an accepted assumption with an owner.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend reference-data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New queue, membership and capacity reference data; no screen and no contract change; the reference-load endpoints are reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: queue data, checks and applier with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 12 acceptance criteria, 10 exception paths and 4 version states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
