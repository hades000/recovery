# RWB-E1-019 Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-019 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-06 Hold roles, teams and queues as data; FEAT-ACA-03 Hold roles as data |
| Requirement IDs | REQ-CWC-006, REQ-ACA-002 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.4; Business Requirements Program, sections 5.3 and 5.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-038, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **reference data administrator (RW-REFADM)**, I want **queues, queue membership and capacity, each tied to a team code and a role code, held as versioned reference data loaded from the Excel template**, so that **the organization changes without a code release**.

## 2. Business rationale

Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. This story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation (RWB-E1-020), to scope by team (RWB-E1-037) and to control CTL-08.

## 3. Preconditions

- RWB-E1-043 is done: ReferenceVersionRegistry and ReferenceDataService hold versions of reference tables, and POST /admin/reference-loads calls them; QUEUE is a LOV-REF-TABLE code and QUEUE_MEMBER is added to it (see additions).
- RWB-E1-038 is done: the reference approval pattern is in use for the delegation table.
- The ROLE and TEAM tables have a version in force (RWB-E1-043); TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK" (assumed codes; owner Shared operations), each with its region code.
- The loader holds RW-REFADM (Reference data C). The approver is the table owner for queues, Shared operations, acting through RW-TEAMMGR with Reference data A (assumed grant; DL01).
- Queue member user IDs are Entra ID object IDs of people who hold the queue's role.

## 4. Flow

1. RW-REFADM: fills the Queues template (sheets QUEUE and QUEUE_MEMBER) and calls POST /admin/reference-loads once per sheet with valid from 2026-11-30.
2. QueueTableChecks: runs the queue checks on top of the RWB-E1-043 row checks: team code in TEAM, role code in ROLE, method in LOV-ASSIGN, cap range, overflow queue exists and forms no loop, member holds the queue role.
3. ReferenceVersionRegistry (RWB-E1-043): on any failed row refuses the load whole and names every failed row; on a clean file stores the version with status VALIDATED.
4. RW-TEAMMGR: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.
5. QueueVersionApplier: on the valid from date, applies the QUEUE and QUEUE_MEMBER versions in force to the queue and queue_member tables: upsert by queue code keeping the queue ID, replace active member rows, set table_version.
6. CapacityService: answers capacity questions for the allocation engine from the applied version.
7. QueueMembershipQuery: answers the teams and regions of a user for scope by team (RWB-E1-037).
8. RW-REFADM: if the version is wrong, calls POST /admin/reference-loads/{loadId}/rollback; the previous version is in force again and QueueVersionApplier re-applies it in one transaction.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A queue names a team code not in TEAM | Load refused in full; the row is named | MSG-P1-002 | AC4 |
| X2 | A cap outside 1 to 500 | Load refused in full | MSG-GEN-002 | AC5 |
| X3 | The approver is the author | Approval refused; version stays VALIDATED | MSG-P7-002 | AC6 |
| X4 | Rollback with no earlier version | Refused; current version unchanged | MSG-P3-015 | AC7 |
| X5 | The same file is loaded again for the same valid from | The existing load is returned; nothing new is written (RWB-E1-043 idempotency) | None | AC8 |
| X6 | Valid from is in the future | The version waits; the current version stays in force until that date | None | AC9 |
| X7 | A member does not hold the queue's role | Load refused in full; the member row is named | MSG-P1-002 | AC10 |
| X8 | Overflow queues form a loop | Load refused in full | MSG-P1-002 | AC11 |
| X9 | A required column is empty | Load refused in full | MSG-GEN-001 | AC12 |
| X10 | A role without Reference data C loads a file | Refused with 403 | MSG-P4-002 | Access test TC-E1-019-13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the reference data service of RWB-E1-043; adds the queue checks, the apply step and two read interfaces |
| Negotiable | Team codes, queues, caps and members are data; the template layout can change with the checks |
| Valuable | A team change takes one load and one approval instead of a release |
| Estimable | One check set, one applier, two read services, one migration |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Roles, teams and queues as data

  Background:
    Given TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK"
    Given the loader holds RW-REFADM and the approver holds RW-TEAMMGR

  Scenario: AC1 Tables loaded
    Given the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows
    When the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved
    Then 12 queue rows are in force with table version 1
    Then each queue holds its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF
    Then 48 member rows are in force
    Then the reference version holds the author, the approver and the approval time

  Scenario: AC2 Rollback
    Given QUEUE version 3 is in force with an error in queue "DIL-BKK-CO"
    Given QUEUE version 2 was in force before it
    When rollback is called once for version 3
    Then QUEUE version 2 is in force for every queue row
    Then each queue keeps its record ID, so cases in the queue keep their queue
    Then the system records the rollback with the caller, the time and the reason

  Scenario: AC3 Capacity
    Given member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases
    When a 41st case is offered for U-11
    Then the capacity service answers "AT_CAP" for U-11
    Then names the overflow queue "TDR-BKK-OVF" for the case

  Scenario: AC4 Unknown team code
    Given the QUEUE sheet has queue "XYZ-CO" on row 7 with team code "XYZ"
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming row 7 and check "team code not in TEAM"
    Then no queue or member row changes

  Scenario: AC5 Cap outside its range
    Given queue "NPA-BKK-CO" has capacity cap 0
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-002 for capacity cap with minimum 1 and maximum 500

  Scenario: AC6 Author cannot approve
    Given QUEUE version 4 was loaded by user U-90
    When U-90 approves it
    Then the system refuses the approval with MSG-P7-002
    Then version 4 stays VALIDATED and is not in force

  Scenario: AC7 Rollback with no earlier version
    Given QUEUE version 1 is the only version
    When rollback is called for version 1
    Then the system refuses the call with MSG-P3-015
    Then version 1 stays in force

  Scenario: AC8 The same file loaded twice
    Given the QUEUE sheet for valid from 2026-12-15 was loaded as version 5
    When the same file is loaded again for valid from 2026-12-15
    Then the response returns version 5
    Then the system writes no new version

  Scenario: AC9 A version with a future valid from
    Given QUEUE version 2 is in force and version 3 is approved with valid from 2026-12-15
    When the capacity service is asked on 2026-12-14
    Then it answers from version 2
    Then on 2026-12-15 it answers from version 3

  Scenario: AC10 Member without the queue role
    Given member U-12 on row 22 of the QUEUE_MEMBER sheet is listed on queue "LIT-BKK-OFF" and does not hold RW-LITOFF
    When the sheet is loaded
    Then the system refuses the load with MSG-P1-002 naming row 22 and check "member does not hold the queue role"

  Scenario: AC11 Overflow loop
    Given queue "DS-BKK-CO" overflows to "DS-BKK-OVF" and "DS-BKK-OVF" overflows to "DS-BKK-CO"
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-P1-002 and check "overflow queues form a loop"

  Scenario: AC12 Required column empty
    Given queue row 3 has no assignment method
    When the QUEUE sheet is loaded
    Then the system refuses the load with MSG-GEN-001 for assignment method on row 3
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every queue belongs to one team and one role | queue.team_code (DF-WRK-004), queue.role_code (DF-WRK-005); LOV-TEAM, LOV-ROLE |
| BR2 | A load with any failed row is refused in full | Reference data change process, step 3; CTL-08 |
| BR3 | A version takes effect on its valid from date after approval; open cases keep the queue they are in | Reference data change process, steps 5 and 6; R-UNI-38 |
| BR4 | The author of a load cannot approve it | Separation of duty table; CTL-08 |
| BR5 | Rollback returns the previous version in one call | Reference data change process, step 7; REQ-CWC-006 |
| BR6 | A person's capacity is the lower of their member capacity and the queue cap | queue.capacity_cap (DF-WRK-007); DL23 |
| BR7 | Assignment method is one of ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL | LOV-ASSIGN |
| BR8 | Cap range 1 to 500 | Parameter `queue.cap.max` = 500 (assumed; DL23), RWB-E1-042 |
| BR9 | A member must hold the queue's role | ROLE table; P4 role directory |

## 9. State transitions

None. This story does not change a case status. It changes the status of a reference version (RWB-E1-043): VALIDATED, APPROVED, ROLLED_BACK, and the table_version applied to the queue rows.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every row passes | VALIDATED |
| VALIDATED | Approve | Approver is not the author | APPROVED; applied on its valid from date |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK; the earlier version is applied |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM | Loads the sheets and calls rollback (Reference data CRUD) |
| RW-TEAMMGR | Approves a queues version as the Shared operations owner (Reference data A, assumed grant; DL01) |
| RW-COE | Reads versions (Reference data CRUD); may load |
| RW-RISK | No part in queue loads; may not hold RW-REFADM (separation of duty) |
| SY-CASEWF | Applies the version on its valid from date and answers capacity and membership questions |
| No delegation of authority level applies | Queue structure is not a credit decision |

## 11. Data

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

reference_version and reference_row are new entities of RWB-E1-043, read here through ReferenceDataService. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint, RWB-E1-043)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx sheet), table = "QUEUE" or "QUEUE_MEMBER", validFrom (date) |
| Response | 201 ReferenceLoad: id, table, validFrom, status, rows |
| Errors | 401 (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 422 a row fails (MSG-GEN-001, MSG-GEN-002; queue checks as MSG-P1-002 with the rows in Problem.detail); 503 |
| Authorization | Reference data, right C |
| Idempotency | Table code, valid from and content hash (RWB-E1-043) |

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint)

| Item | Value |
|---|---|
| Response | 200 ReferenceLoad with status APPROVED |
| Errors | 401; 403 no Reference data A; 404; 409 approver is the author (MSG-P7-002) or the version changed (MSG-GEN-004); 503 |
| Authorization | Reference data, right A |

**POST /admin/reference-loads/{loadId}/rollback** (new endpoint, see additions)

| Item | Value |
|---|---|
| Request | Path loadId (uuid); body { reason: string, required } |
| Response | 200 ReferenceLoad with status ROLLED_BACK |
| Errors | 401; 403 no Reference data U; 404; 409 no earlier version (MSG-P3-015); 422 reason empty (MSG-GEN-001); 503 |
| Authorization | Reference data, right U |
| Idempotency | Idempotency-Key header; a repeat returns the first result |

**Published interfaces**

```java
// P3, package recovery.casewf.queues.api (published)
public interface CapacityService {
    CapacityAnswer check(UUID queueId, UUID userId, LocalDate onDate);
    List<QueueMemberView> membersInForce(UUID queueId, LocalDate onDate);
}
public record CapacityAnswer(Status status, int openCases, int capacity, UUID overflowQueueId) {
    public enum Status { BELOW_CAP, AT_CAP }
}
public interface QueueMembershipQuery {
    Membership membershipOf(UUID userId, LocalDate onDate);   // teamCodes, regionCodes, queueIds
}
// P3 checks plugged into the RWB-E1-043 registry for table codes QUEUE and QUEUE_MEMBER
public interface ReferenceTableCheck {
    String tableCode();
    List<RowCheckFailure> check(List<Map<String, Object>> rows, LocalDate validFrom);
}
```

## 13. Solution plan

**Package.** `recovery/casewf/queues`, Java package `recovery.casewf.queues`; published types in `recovery.casewf.queues.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| QueueTableChecks | Service | ReferenceTableCheck for QUEUE and QUEUE_MEMBER: team, role, method, cap range, overflow loop, member role |
| QueueVersionApplier | Job | Daily at 00:05, and on approval or rollback, applies the QUEUE and QUEUE_MEMBER versions in force to queue and queue_member |
| CapacityService | Published interface | Open cases against capacity for the applied version |
| QueueMembershipQuery | Published interface | Teams, regions and queues of a user, for scope (RWB-E1-037) |
| ReferenceRollbackHandler | Service | Rollback for reference loads: marks the version ROLLED_BACK through the registry and triggers the applier |
| CaseAndWorkflowRepository | Repository | queue, queue_member, open case counts |

**Database**

- Writes queue (all columns plus table_version) and queue_member.
- Reads recovery_case (owner_user_id, queue_id, status) for open case counts (index ix_case_owner_status).
- Migration in this story: `V019_1__queue_member.sql` creates queue_member (id, queue_id, user_id, capacity, skill_codes, table_version, valid_from, valid_to, standard columns; index on (queue_id) where is_active; index on (user_id) where is_active) and adds queue.table_version.

**Configuration and reference data**

- TEAM, ROLE, QUEUE and QUEUE_MEMBER through ReferenceDataService (RWB-E1-043); LOV-ASSIGN through the P4 list interface.
- Parameter `queue.cap.max` = 500 (assumed; DL23) from RWB-E1-042.
- The Queues template, owned by Shared operations.

**Build steps**

1. QueueTableChecks with one check per rule; unit tests for AC4, AC5, AC10, AC11, AC12.
2. Add the checks to the RWB-E1-043 registry for QUEUE and QUEUE_MEMBER; test AC8 through the registry's idempotency.
3. Approval through the registry; test AC6.
4. QueueVersionApplier: upsert queues by queue code keeping the ID, replace member rows; tests AC1, AC9.
5. ReferenceRollbackHandler and the rollback endpoint; tests AC2, AC7.
6. CapacityService with the lower of member capacity and queue cap; test AC3.
7. QueueMembershipQuery for RWB-E1-037.
8. Access test on the load endpoint.

**Feature flag.** `rwb.p3.queuetables`. Off: the applier does not run and the queue rows from the seed migration stay.

**Done when.** The tests in section 16 pass and the SIT queue set for six teams loads, approves and rolls back.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A queue check fails on a row (team code, member role, overflow loop) | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Required column empty, or no rollback reason | Enter {field}. |
| MSG-GEN-002 | Cap outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The administrator loads by file through the reference load endpoint; SCR-42 Queues and service levels (states Versions; load) comes in Epic 8. The result of each load is returned as the ReferenceLoad response.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-019-01 | AC1, BR1, BR3 | System | Template with 12 queues and 48 members |
| TC-E1-019-02 | AC2, BR5 | System | QUEUE versions 2 and 3 |
| TC-E1-019-03 | AC3, BR6 | System | Member U-11 with capacity 40 and 40 open cases |
| TC-E1-019-04 | AC4, BR2 | System | Queue with team code XYZ |
| TC-E1-019-05 | AC5, BR8 | System | Cap 0 |
| TC-E1-019-06 | AC6, BR4 | System | Load and approval by U-90 |
| TC-E1-019-07 | AC7, BR5 | System | Only one version |
| TC-E1-019-08 | AC8 | System | Same file twice for 2026-12-15 |
| TC-E1-019-09 | AC9, BR3 | System | Version 3 with valid from 2026-12-15 |
| TC-E1-019-10 | AC10, BR9 | System | Member U-12 without RW-LITOFF |
| TC-E1-019-11 | AC11, BR2 | System | Overflow loop between DS-BKK-CO and DS-BKK-OVF |
| TC-E1-019-12 | AC12, BR2 | System | Row 3 with no assignment method |
| TC-E1-019-13 | Access | Access | RW-CASEOWN calls POST /admin/reference-loads and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: team codes, queue codes, methods, caps and members are data.
- No personal data in logs, tests or prompts; members are named by user ID only.
- No read of another module's tables: roles and lists through P4 interfaces; versions through ReferenceDataService.
- A version applies whole or not at all; the queue record ID never changes, so recovery_case.queue_id stays valid.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-06 | All recovery processes | R-UNI-38 | TC-E1-019-01 to TC-E1-019-12 |
| REQ-ACA-002 | Roles held as data; a change without a release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03 | All recovery processes | None | TC-E1-019-01, TC-E1-019-10 |

## 19. Out of scope

- The role list and the permission matrix themselves (RWB-E1-022, RWB-E1-037).
- The reference version store and the load endpoint (RWB-E1-043).
- Allocation and assignment by these tables (RWB-E1-020).
- Administration screens for queues (Epic 8, SCR-42).
- Reallocation when an owner leaves (Epic 2, R-UNI-18).
