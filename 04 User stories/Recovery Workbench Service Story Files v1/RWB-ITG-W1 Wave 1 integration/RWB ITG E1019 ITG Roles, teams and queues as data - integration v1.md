# RWB-ITG-E1019-ITG Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1019-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P4-E1038-APP, RWB-P3-E1019-APP, RWB-P4-E1019-APP, RWB-P6-E1019-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-019 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-019 roles, teams and queues as versioned reference data across rwb-case (P3, the queue and membership version), rwb-access (P4, the roles in force, the reader's scope and the delegation-of-authority reference-approval pattern of RWB-P4-E1038-APP) and rwb-comms (P6, the notice that carries a queue code without holding a copy)**, so that **one approved load is proved to be in force for every reader, one rollback is proved to return every reader to the earlier version, and no service is proved to hold a second copy of a queue**.

### 2. Business rationale

Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. The legacy story holds every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables QUEUE and QUEUE_MEMBER, loaded from one template through the reference data service, with an approver and a one-call rollback, and applies the version in force to the queue tables the engines use. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation, to scope by team and to control CTL-08.

The split keeps the behaviour and separates the two halves of the data. Queues, queue membership, capacity and the version store are rwb-case data: `queue`, `queue_member`, `reference_row` and `reference_version` live in `rwb_case` (DP-01, DP-07), and the load, the approve and the rollback are rwb-case admin operations on the base `/api/recovery/case/v1` (DP-13). Roles, the permission matrix, scope, masking and the delegation-of-authority table are rwb-access data in `rwb_access`, and every other service asks for them over the rwb-access contract through the guard library, cached, one hop, 2 s (DP-08, DP-11). rwb-comms holds notices and templates and no queue row at all: it carries the queue code that the rwb-case contract answers at the moment the notice is built, so a queue rename reaches a letter without a change in rwb-comms (DP-01, DP-06, DP-07). The reference-approval pattern itself is one pattern for every reference table, and RWB-P4-E1038-APP keeps it for the delegation-of-authority table: an author cannot approve, the approval is dated and recorded, and a wrong version is returned by one call.

RWB-P3-E1019-APP, RWB-P4-E1019-APP and RWB-P6-E1019-APP own the component behaviour, and RWB-P4-E1038-APP owns the approval pattern for the delegation table. This integration story owns no legacy acceptance criterion: the thirteen legacy test cases are carried as `-ITG` copies, and the ten criteria of section 7 are the new cross-service proof that the same version is in force for three readers at once. What a single service cannot prove is the whole point of the story. One approved load must be visible to the queue read in rwb-case, to the role read in rwb-access and to the notice in rwb-comms in the same run, because three separate component tests can all pass while the three readers disagree. A rollback must return every reader on its next call, not only the caller's own service. A refused load must name the row, and the answer that refuses it comes from another service's role list. A queue membership row must become a reader's scope in rwb-access and must close a case that is outside the team, which is a fact about two services and one sign-in. And the code printed on a notice must be the code read from the queue contract, which is a fact about a third service and an absence of a copy.

The delta against the monolith is named in GAP-0344 and ASM-0438. In the monolith the loader, the version store, the roles and the lists were one schema; in the target the queue load is a rwb-case reference load, the role answer is a rwb-access read, the list of values is a rwb-case read, and the notice is built in rwb-comms from the queue code the rwb-case contract answers. No service contract is faked in this story: the four integration dependencies are the real services on their published contracts, and a fake would defeat the purpose of the run. Release 30 November 2026 stays tentative and is copied unchanged.

### 3. Preconditions

- RWB-P3-E1019-APP is done: the queue checks, the apply step, the capacity answer, the membership query and the reference-load, approve and rollback operations are in SIT on rwb-case, and `queue`, `queue_member`, `reference_row` and `reference_version` exist in `rwb_case`.
- RWB-P4-E1019-APP is done: the role list in force, the scope answer and the session of the signed-in reader are published on rwb-access, and the guard library answers role, permission and scope questions, cached, with a 2 s timeout.
- RWB-P6-E1019-APP is done: the notice request and its response are published on rwb-comms, the notice carries the queue and team code it was built with, and `rwb_comms` holds no queue table and no queue row.
- RWB-P4-E1038-APP is done: the delegation-of-authority table is loaded through the same reference-load pattern, approved by a role other than the author, dated, and returned by one call.
- The published contracts of P3, P4 and P6 are versioned in the registry, and the suite consumes only those contracts; the ownership map gives the reference-load, approve and rollback operations to rwb-case, the role list and the session to rwb-access, and the notice request to rwb-comms.
- The TEAM versions are in force in the rwb-case reference data: TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK" (assumed codes; owner Shared operations), each with its region code.
- The loader holds RW-REFADM (Reference data C). The approver holds RW-TEAMMGR with Reference data A (assumed grant; DL01).
- Queue member user IDs are Entra ID object IDs of people who hold the queue's role, and the run uses synthetic test identities only.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic cases, teams, queues, members and test users, and the clock of the harness can be placed on 2026-11-30, 2026-12-14 and 2026-12-15.
- SIT is in place with the wave 1 services, the topics and their retry and `.dlt` topics, the schema registry, the gateway-bff entry and the P4 guard cache.
- No production data is read, copied or connected to; every queue, member, case, user and version in the run is synthetic.
- The field names by which the P4 session and the P6 notice response expose the team scope and the queue code are Not specified in the source documents (GAP-0344; ASM-0438); the suite reads them from the published contracts and fails the preflight if a field is absent.
- The release date 30 November 2026 is tentative and is copied unchanged; this story has no build dependency, so it is ready on Day 1 (Template and Rules section R5.7).

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, the test users, the six team codes and the member rows of the harness RWB-ITG-W1J01-ITG, places the clock on 2026-11-30, and opens no service schema and no production row.
2. Harness, AC1: submits the QUEUE sheet and the QUEUE_MEMBER sheet of the Queues template with valid from 2026-11-30 through `POST /api/recovery/case/v1/admin/reference-loads` as RW-REFADM, with an `Idempotency-Key` per sheet, and reads the load ID, the table and the status of each response.
3. Harness, AC1: approves both loads through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` as RW-TEAMMGR, then reads `GET /api/recovery/case/v1/queues` and asserts 12 queue rows in force with table version 1, each with its team code and its role code, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF, and 48 member rows behind the queue.
4. Harness, AC1: reads `GET /api/recovery/case/v1/admin/lists/LOV-REF-TABLE` and asserts that QUEUE and QUEUE_MEMBER are reference tables in force, and reads `GET /api/recovery/case/v1/admin/lists/LOV-ASSIGN` and asserts that every assignment method of the 12 rows is a value of the list and not a value in code.
5. Harness, AC1: reads `GET /api/recovery/access/v1/admin/roles` and asserts that RW-LITOFF is a role in force in rwb-access, then requests the notice for a case in queue "LIT-BKK-OFF" through `POST /api/recovery/comms/v1/cases/{caseId}/notices` and asserts that the notice carries queue code "LIT-BKK-OFF" and team code "LIT-BKK" exactly as the P3 queue read answered them, and that no queue row exists in `rwb_comms`.
6. Harness, AC2: places the clock on a version 3 that is in force with an error in queue "DIL-BKK-CO", calls `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` once, and asserts that `GET /api/recovery/case/v1/queues` answers version 2 for every queue row, that each queue keeps its record ID, that the next notice for a case in "DIL-BKK-CO" carries the version 2 code, and that the role read in rwb-access is unchanged because the roles are versions of their own.
7. Harness, AC3: loads a QUEUE sheet whose row 5 names role code RW-LITOFF while rwb-access answers no role code RW-LITOFF in force, and asserts the refusal of the whole load with MSG-P1-002 naming row 5, that no queue and no member row changed, and that the refusal came from the rwb-access answer and not from a cached value.
8. Harness, AC4 and AC5: offers a 41st case for member U-11 of "TDR-BKK-CO" at capacity 40 with 40 open cases through `POST /api/recovery/case/v1/queues/{queueId}/placements`, asserts the capacity answer "AT_CAP" with the overflow queue "TDR-BKK-OVF", then signs member U-12 in, reads the team scope from `GET /api/recovery/access/v1/me/session`, asserts the case in team scope, and asserts the 404 for a case in another team's queue.
9. Harness, AC6 and AC7: approves version 3 with valid from 2026-12-15, asserts on 2026-12-14 that the queue read and the notice build both answer from version 2, asserts on 2026-12-15 that both answer from version 3, and asserts that the same file submitted again for 2026-12-15 returns version 5 with no new row in any service.
10. Harness, AC8, AC9 and AC10: loads a sheet as a user holding RW-CASEOWN and asserts the 403 with MSG-P4-002 and no version written; asserts that the same approve operation and the same four-eyes rule approve the delegation-of-authority version and refuse the author (MSG-P7-002); asserts that the queue code of the notice for a case in "WO-BKK-CO" is the code read from the P3 contract and that a new approved version changes the next notice with no change in rwb-comms; then writes the evidence report, removes the synthetic set and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A queue names a role code that is not in force in rwb-access | The load is refused in full and the row and the role code are named; no queue and no member row changes | MSG-P1-002 | AC3 |
| X2 | The approver is the author of the load | The approval is refused, the version stays VALIDATED and is not in force | MSG-P7-002 | AC9 |
| X3 | Rollback with no earlier version | The call is refused and the version in force is unchanged | MSG-P3-015 | AC2 |
| X4 | The same file is loaded again for the same valid from | The existing load is returned and no row is written in any service | None | AC7 |
| X5 | Valid from is in the future | The version waits and the version in force answers until that date, in every reader | None | AC6 |
| X6 | A role without Reference data C loads a file | The call is refused with status 403, no version is created and no queue row changes | MSG-P4-002 | AC8 |
| X7 | The rwb-access role read does not answer inside 2 s | The load is refused with 503 and nothing is written; no cached role answer is used past its time-to-live | None | AC3 |
| X8 | The notice cannot read the queue code from the rwb-case contract | No notice is built, the case is reported and no queue value is taken from a copy | None | AC10 |
| X9 | A consumed operation exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy, the evidence report records it, and no assertion is made on data that was not read | None | AC1, AC2 |
| X10 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema | None | Section 17 |

X1 to X8 are the reference-data failure paths of the legacy story read across the services; X9 and X10 are the suite's own failure modes, so that a timeout never becomes a pass and a schema read is impossible rather than discouraged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the four integration dependencies and the published contracts of P3, P4 and P6, not their source code, and it owns no schema and no table |
| Negotiable | The fixture sizes, the poll interval, the clock control and the report layout are configuration; the actions, the message IDs, the check names and the valid-from dates are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one version in force for three readers, one rollback for three readers, a refusal that names a row and comes from another service's role list, a scope that comes from a membership row, and a notice with no queue copy |
| Estimable | One suite module, one template driver, four probes, a capacity step, a rollback step and one report |
| Small | Fits one sprint with the report; no service code and no schema change |
| Testable | Every criterion is asserted on an observable: a REST response, a status, a message, a row count, a queue ID or a call set |

### 7. Acceptance criteria

```gherkin
Feature: Roles, teams and queues as data, proven across the wave 1 services

  Background:
    Given TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK"
    Given the loader holds RW-REFADM and the approver holds RW-TEAMMGR
    Given the wave 1 services rwb-case, rwb-access and rwb-comms are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic cases, members, teams and users are loaded and no production data is used
    Given the clock is on 2026-11-30

  Scenario: AC1 One approved load is in force for the queue read, the role read and the notice (new, D-RCV-60)
    Given the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows
    When the QUEUE and QUEUE_MEMBER sheets are loaded with valid from 2026-11-30 through POST /api/recovery/case/v1/admin/reference-loads and approved by the approver through POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve
    Then GET /api/recovery/case/v1/queues answers 12 queue rows in force with table version 1, each with its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF
    Then GET /api/recovery/case/v1/admin/lists/LOV-REF-TABLE holds QUEUE and QUEUE_MEMBER, and GET /api/recovery/case/v1/admin/lists/LOV-ASSIGN holds the method of every one of the 12 rows
    Then GET /api/recovery/access/v1/admin/roles answers RW-LITOFF as a role in force in rwb-access
    Then the notice requested through POST /api/recovery/comms/v1/cases/{caseId}/notices for a case in queue "LIT-BKK-OFF" carries queue code "LIT-BKK-OFF" and team code "LIT-BKK" exactly as the queue read answered them
    Then rwb_comms holds no queue table and no queue row, and the reference version holds the author, the approver and the approval time

  Scenario: AC2 One call returns the earlier version for every reader (new, D-RCV-60)
    Given QUEUE version 3 is in force with an error in queue "DIL-BKK-CO"
    Given QUEUE version 2 was in force before it
    When rollback is called once for version 3 through POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback
    Then GET /api/recovery/case/v1/queues answers QUEUE version 2 for every queue row
    Then each queue keeps its record ID, so cases in the queue keep their queue
    Then the next notice for a case in "DIL-BKK-CO" carries the queue code and the role code of version 2, read from the rwb-case contract when the notice is built
    Then GET /api/recovery/access/v1/admin/roles is unchanged, because the roles are versions of their own in rwb-access
    Then the system records the rollback with the caller, the time and the reason

  Scenario: AC3 A queue role that is not in force in rwb-access refuses the whole load (new, D-RCV-60)
    Given the QUEUE sheet has queue "LIT-BKK-OFF" on row 5 with role code RW-LITOFF
    Given rwb-access answers no role code RW-LITOFF in force on 2026-11-30
    When the sheet is loaded
    Then the system refuses the load in full with MSG-P1-002 naming row 5 and check "role code not in the rwb-access role list"
    Then no queue row and no member row changes in rwb-case
    Then the refusal is answered by the rwb-access role read of that call and not from a cached value

  Scenario: AC4 The capacity answer and the allocation agree at the cap (new, D-RCV-60)
    Given member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases
    Given queue "TDR-BKK-CO" overflows to "TDR-BKK-OVF"
    When a 41st case is offered for U-11 through POST /api/recovery/case/v1/queues/{queueId}/placements
    Then the capacity answer to the placement is "AT_CAP" for U-11 and names the overflow queue "TDR-BKK-OVF" for the case
    Then the case read through GET /api/recovery/case/v1/cases/{caseId} shows queue "TDR-BKK-OVF" and no owner value of U-11
    Then GET /api/recovery/case/v1/queues still answers the version in force for "TDR-BKK-CO" with its overflow queue "TDR-BKK-OVF"

  Scenario: AC5 Queue membership becomes the scope of a reader (new, D-RCV-60)
    Given member U-12 is on the QUEUE_MEMBER rows of queue "LIT-BKK-OFF" in the version in force, holds RW-LITOFF as the load check requires, and the queue belongs to team "LIT-BKK"
    Given a case in queue "LIT-BKK-OFF" and a case in queue "TDR-BKK-CO" both exist
    When U-12 signs in and calls GET /api/recovery/access/v1/me/session
    Then the session answers team scope "LIT-BKK" for U-12, taken from the queue membership read through the rwb-case contract
    Then GET /api/recovery/case/v1/cases/{caseId} for the case in "LIT-BKK-OFF" answers the case
    Then GET /api/recovery/case/v1/cases/{caseId} for the case in "TDR-BKK-CO" answers status 404
    Then removing U-12 from the member rows in a new approved version removes "LIT-BKK" from the scope on the next sign-in, with no deployment

  Scenario: AC6 A future valid from is answered from the version in force by both services (new, D-RCV-60)
    Given QUEUE version 2 is in force and version 3 is approved with valid from 2026-12-15
    When the queue read and the notice build are asked on 2026-12-14
    Then both answer from version 2
    Then on 2026-12-15 both answer from version 3
    Then no queue row changed before 2026-12-15 and no service was redeployed

  Scenario: AC7 The same file loaded twice returns the same version and adds no row (new, D-RCV-60)
    Given the QUEUE sheet for valid from 2026-12-15 was loaded as version 5
    When the same file is loaded again for valid from 2026-12-15
    Then the response returns version 5
    Then the system writes no new version
    Then GET /api/recovery/case/v1/queues answers the same queue IDs and the same table version as before the second call
    Then no queue read, role read or notice of any service sees a new row

  Scenario: AC8 A role without Reference data C is refused by the P4 guard (new, D-RCV-60)
    Given a user holding RW-CASEOWN, which has no Reference data C
    When the user calls POST /api/recovery/case/v1/admin/reference-loads
    Then the call returns status 403 with MSG-P4-002
    Then no version is created and no queue row changes
    Then the refusal is answered by the rwb-access guard library in one hop inside 2 s

  Scenario: AC9 The same reference-approval pattern approves the delegation table and the queue version (new, D-RCV-60)
    Given a delegation-of-authority version is loaded as table "delegation_limit" and QUEUE version 4 was loaded by user U-90
    When U-90 approves QUEUE version 4 through POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve
    Then the system refuses the approval with MSG-P7-002
    Then version 4 stays VALIDATED and is not in force
    Then the same operation and the same four-eyes rule approve the delegation-of-authority version when a different holder of Reference data A approves it
    Then both versions record the author, the approver and the approval time in the reference version store, and the delegation version is returned by one call like the queue version

  Scenario: AC10 A queue code on a notice is read and never copied (new, D-RCV-60)
    Given the version in force answers queue code "WO-BKK-CO" for team "WO-BKK"
    Given a case in queue "WO-BKK-CO"
    When the notice for that case is requested through POST /api/recovery/comms/v1/cases/{caseId}/notices
    Then the notice carries queue code "WO-BKK-CO" and team code "WO-BKK" exactly as GET /api/recovery/case/v1/queues answers them
    Then the call set of the run shows the queue value read from the rwb-case contract only, and rwb_comms holds no queue table and no queue row
    Then renaming the queue in a new approved version changes the next notice with no change in rwb-comms and no deployment
```

**Target reading.** Against the monolith, the queue and membership version is a rwb-case reference load on `/api/recovery/case/v1` (DP-07, DP-13), the role and scope answers come from rwb-access over the authorise contract through the guard library (DP-08, DP-11), the lists are read as data (DP-06), the version store is the rwb-case reference registry with its own Flyway sequence (DP-15), the topic naming of the owner applies to any event used (DP-14), and every screen path enters through the gateway-bff composite route (DP-19). No service reads another service's tables (DP-01): the suite asserts the queue version through the rwb-case contract, the role list and the scope through the rwb-access contract, and the queue code on the notice through the rwb-comms response. The field names by which the session and the notice response expose the team scope and the queue code are Not specified in the source documents (GAP-0344; ASM-0438), so the suite reads them from the published contracts and treats an absent field as contract drift.

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
| BR8 | Cap range 1 to 500 | Parameter `queue.cap.max` = 500 (assumed; DL23), the parameters contract of rwb-case |
| BR9 | A member must hold the queue's role | The rwb-access role list over the authorise contract; legacy ROLE table |
| BR10 | One version is in force at a time for the whole organization: the queue read in rwb-case, the role check in rwb-access and the notice in rwb-comms answer the same version on the same date | REQ-CWC-006; REQ-ACA-002; DP-07 |
| BR11 | The queue tables live in `rwb_case` only, the roles and the delegation table in `rwb_access` only, and no service holds a queue copy | DP-01; ownership map (queue, queue_member, role, delegation_limit) |
| BR12 | A queue row carries the role code it points at, and the role itself is read from the rwb-access contract at load time and at read time, never copied into a queue table | DP-08; DP-11 |
| BR13 | The queue membership row is the source of a reader's team scope: the scope answer is derived from the membership in force, and a case outside the team is refused as not found | REQ-ACA-009; DP-08 |
| BR14 | The delegation-of-authority table and the queue version use one approval pattern: load, check, four-eyes approval, dated effect, one-call rollback | RWB-E1-038 reference approval pattern; CTL-08; REQ-ACA-004 |
| BR15 | The lists of values and the parameters that the load and the readers use are read as data through the rwb-case contracts, not written in code | DP-06; DP-07 |
| BR16 | Every call is one hop to the owning service with a 2 s client budget, and no service is called through another service | ADR-020; DP-11; DP-13 |

### 9. State transitions

None for the case status. This story changes the status of a reference version and observes it across the services, and it changes the team scope a reader holds by changing the membership rows the scope is derived from.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every row passes the checks, including the rwb-access role answer | VALIDATED |
| VALIDATED | Approve | The approver is not the author and holds Reference data A | APPROVED; applied on its valid from date |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK; the earlier version is in force again in every reader |

The observations the run makes across the services:

| Object | States | Meaning |
|---|---|---|
| Reference version (rwb_case) | LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED | The vocabulary of the reference-data contract; this story moves the version through VALIDATED, APPROVED and ROLLED_BACK |
| Queue row (rwb_case) | In force at table version n | The queue keeps its record ID across versions, so a case keeps its queue |
| Role list (rwb_access) | In force at its own version | Unchanged by a queue load or a queue rollback; read by the loader and by every reader |
| Reader scope (rwb_access) | Team codes of the membership in force | Changes only when a new membership version is approved, on the next sign-in |
| Notice (rwb_comms) | Built from the queue code of the moment | Holds no queue state of its own; a new version changes the next notice |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the clock control and the evidence report |
| RW-REFADM | Loads the sheets and calls rollback (Reference data C and U) |
| RW-TEAMMGR | Approves a queues version as the Shared operations owner (Reference data A, assumed grant; DL01) |
| RW-CASEOWN | Holds no Reference data C and is refused at the load, which is the access proof of AC8 |
| RW-COE | Reads versions (Reference data CRUD); may load |
| RW-RISK | No part in queue loads and may not hold RW-REFADM (separation of duty); approves the delegation-of-authority version in the pattern AC9 cites |
| Service owner of rwb-case | Owns the load, the approve, the rollback, the queue read, the lists and the capacity and membership answers |
| Service owner of rwb-access | Owns the role list, the scope answer, the session and the guard that refuses the load |
| Service owner of rwb-comms | Owns the notice and the reading of the queue code from the rwb-case contract |
| No role | Reads a service schema directly or takes production data into the run |
| No delegation of authority level applies | Queue structure is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-WRK-001 to DF-WRK-008 | queue (rwb_case) | all fields | Written by rwb-case; read through the rwb-case contract |
| DF-WRK-038 | queue (rwb_case) | table_version | Written by rwb-case; read through the rwb-case contract |
| DF-WRK-045 to DF-WRK-052 | queue_member (rwb_case) | all fields | Written by rwb-case; read through the rwb-case contract and the scope answer |
| DF-REF-159 | reference_version (rwb_case) | id | Read through the rwb-case contract |
| DF-REF-161 | reference_version (rwb_case) | version_no | Read through the rwb-case contract |
| DF-REF-184 | reference_row (rwb_case) | row_data | Read through the rwb-case contract |
| DF-REF-035 | role (rwb_access) | role_code | Read through the rwb-access role list; never by SQL |
| DF-REF-028 | lov_value (rwb_case) | lov_code | Read through the list operation of rwb-case |
| DF-REF-029 | lov_value (rwb_case) | value_code | Read through the list operation of rwb-case |
| DF-REF-016 to DF-REF-026 | delegation_limit (rwb_access) | all fields | Loaded and approved through the rwb-case reference-load operations; read through the contract |
| DF-CAS-005 | recovery_case (rwb_case) | status | Read through the rwb-case contract |
| DF-CAS-009 | recovery_case (rwb_case) | owner_user_id | Read through the rwb-case contract |
| DF-CAS-010 | recovery_case (rwb_case) | queue_id | Read through the rwb-case contract |

Field IDs are those of RWB-E1-019 and are copied unchanged. The legacy story wrote these tables in one schema; in the target `queue`, `queue_member`, `reference_row`, `reference_version` and `lov_value` are in `rwb_case` (P3, DP-01, DP-07), `role`, `delegation_limit`, `permission` and `masking_rule` are in `rwb_access` (P4, DP-01, DP-08), and no queue field is stored in `rwb_comms` (P6). The suite owns no field and no table: every row is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract, and no production value is used.

The field names by which the P4 session returns the team scope and by which the P6 notice response returns the queue and team code are Not specified in the source documents (GAP-0344; ASM-0438). The values themselves are the ones the criteria name: the six team codes, the queue codes, RW-LITOFF, RW-REFADM, RW-TEAMMGR, RW-CASEOWN, valid from 2026-11-30, 12 queue rows and 48 member rows.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the task queue `rwb-integration` and the schema `rwb_integration` - are recorded as reserved and are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | AC1, AC7: submit the QUEUE sheet and the QUEUE_MEMBER sheet of the Queues template as a version, with an `Idempotency-Key` | 2 s |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | AC1, AC6, AC9: approve a loaded version, and assert the refusal when the approver is the author | 2 s |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 rwb-case | AC2: one-call rollback to the previous version, with a reason | 2 s |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | AC1, AC2, AC4, AC6, AC7, AC10: the queue rows in force with team code, role code, method, cap, overflow queue and table version | 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC1: LOV-REF-TABLE and LOV-ASSIGN as the lists in force, so no method or table code is written in code | 2 s |
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | P3 rwb-case | AC4: offer the 41st case for a member at the cap and read the capacity answer of the allocation step | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC4, AC5: the queue of a case, and the 404 outside the reader's scope | 2 s |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | AC1, AC2, AC3: the role list in force that a queue row points at | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC5: the team scope of the reader after a sign-in | 2 s |
| POST | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | AC1, AC2, AC6, AC10: build the notice and read back the queue and team code it used | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget. The reference-load, approve and rollback operations are rwb-case operations in the ownership map, while the roles, the scope and the delegation table are rwb-access data; the queue is never read from `rwb_access` and the role is never read from `rwb_case`.

#### 12.3 Events published

None. The suite publishes no business event. A queue version is a synchronous reference load and no service announces it; the readers answer from the version in force on the next call.

#### 12.4 Events consumed

None. The access announcements of rwb-access - `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, producer P4 - belong to the role and delegation changes of RWB-P4-E1019-APP and RWB-P4-E1038-APP, and this suite asserts the refreshed guard answer through the P4 contract instead of waiting on an event of another legacy key. No `rwb.case.*` event carries a queue version either, so nothing is consumed here.

#### 12.5 Workflows and activities

None. The apply step is a synchronous service step on approval and on rollback, plus a start-up re-check in rwb-case; the suite starts no workflow and observes none.

#### 12.6 Schedules

None. No Schedule takes part in a reference load or in a rollback, and the suite moves only its own harness clock to place the run on 2026-11-30, 2026-12-14 and 2026-12-15.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises are listed in section 11 with their owners: `queue`, `queue_member`, `lov_value`, `reference_row` and `reference_version` in `rwb_case`, and `role` and `delegation_limit` in `rwb_access`.

#### 12.8 Contract fakes

None for a service contract. The only stubs are external to the nineteen services:

| Stub | Purpose |
|---|---|
| Synthetic fixture set (RWB-ITG-W1J01-ITG) | Supplies the synthetic cases, teams, members, users and the Queues template; it stands in for the operating data of the bank, outside the nineteen services |
| Mock Entra sign-in | Gives the run its synthetic test identities and their group membership, as the platform demo sign-in does |

No published service contract is faked, and a run that needs a fake for P3, P4 or P6 fails the preflight.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite | Notes |
|---|---|---|---|
| REST | 0 | 10 operations | The load, the approve, the rollback, the queue read, the list read, the placement, the case read, the role list, the session and the notice; one hop, 2 s (DP-11, DP-13) |
| Kafka | 0 | 0 | Nothing asserted in this story; see 12.4 |
| Temporal | 0 | 0 | The apply step is synchronous in rwb-case |
| File | 0 | 1 | The Queues template, submitted as `multipart/form-data` on the load operation; no claim-check store |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a template driver that builds and submits the two sheets, a set of contract probes for the three services, a capacity and placement step, a rollback step, a scope step and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts of P3, P4 and P6, run order, report and exit code |
| QueueTemplateDriver | Test harness | Builds the Queues template with 12 queues and 48 member rows, submits the QUEUE and QUEUE_MEMBER sheets, and records the load ID, the version and the status |
| QueueProbe | Test harness | Reads the queue rows in force, keeps the queue ID and the table version of each row, and compares two reads of the same version |
| RoleProbe | Test harness | Reads the role list in force from rwb-access and the role code each queue row points at |
| SessionProbe | Test harness | Signs a synthetic test user in and reads the team scope from the session |
| NoticeProbe | Test harness | Requests a notice and reads back the queue and team code it carries, with no queue value stored in rwb-comms |
| CapacityStep | Test harness | Offers a case for a member at the cap through the placement operation and compares the answer with the queue read |
| RollbackStep | Test harness | Rolls a version back in one call and asserts the predecessor on the next read of every consumer, with the record IDs unchanged |
| ReportWriter | Test harness | One row per test case with the version, the queue IDs, the role codes, the statuses, the messages and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object.

**Configuration and reference data**

- The SIT endpoints of P3, P4 and P6 behind gateway-bff, the topic names, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic cases, members, teams and test users of the W1J01 set, the six team codes, the 12 queue rows, the 48 member rows and the dates 2026-11-30, 2026-12-14 and 2026-12-15.
- The role codes RW-REFADM, RW-TEAMMGR, RW-LITOFF and RW-CASEOWN, read through the rwb-access contract and never written in the suite code as a grant.
- The lists LOV-REF-TABLE and LOV-ASSIGN and the parameter `queue.cap.max` = 500 (assumed; DL23), read through the rwb-case contracts (DP-06, DP-07).
- The 2 s client budget, the poll interval and the wait window of the run.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | `queue`, `queue_member` and the version store stay in `rwb_case`; `role` and `delegation_limit` stay in `rwb_access`; `rwb_comms` holds no queue row; the suite asserts through contracts only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On RWB-P3-E1019-APP for `queue.cap.max`; the suite reads it through the P3 contract and writes no value in code |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On RWB-P3-E1019-APP for the queue and membership versions and the lists; the suite loads and reads through that contract |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON | On RWB-P3-E1019-APP, RWB-P4-E1019-APP and RWB-P6-E1019-APP for the role, scope and refusal answers; the suite asserts the 403 and the scope through the P4 contract |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The ten consumed REST operations of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2, and no monolith base anywhere in the suite |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON | On the owners of the topics the story names; the suite publishes nothing and asserts no event |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P3-E1019-APP and its DB story; the suite owns no schema and no migration |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; no screen is in scope in this story |

The nine patterns above are the metadata list DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15 and DP19, written with the hyphen here as the pattern table writes them. The H and C dependencies in the table belong to the owning APP stories: they record what the services the suite proves had to build, not what the suite waits for. This story carries no H, no C and no X of its own, and its I list is the four integration dependencies RWB-P4-E1038-APP, RWB-P3-E1019-APP, RWB-P4-E1019-APP and RWB-P6-E1019-APP. An ITG story builds against published contracts and blocks no build (Template and Rules section R5.4 and R5.7).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Queues template | 12 queues for the six teams and 48 member rows, one sheet per table | AC1, AC2, AC3, AC4, AC6, AC7, AC8, AC9, AC10 |
| Version state | Version 1 in force, version 2 as the predecessor, version 3 with valid from 2026-12-15 and version 5 for the repeated file | AC2, AC6, AC7 |
| Member state | U-11 at capacity 40 with 40 open cases, U-12 on the litigation queue rows, U-90 as an author | AC2, AC4, AC5, AC9 |
| Case set | A case in "LIT-BKK-OFF", a case in "TDR-BKK-CO" and a case in "WO-BKK-CO", all synthetic | AC4, AC5, AC10 |
| Delegation state | The delegation-of-authority version loaded as table "delegation_limit", with an approver other than its author | AC9 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG, wire it to the SIT endpoints of P3, P4 and P6 through gateway-bff, and write the preflight: the three services answer, the contracts are the published ones, and the field names of the session and the notice response are present.
2. Build QueueTemplateDriver and the Queues template fixture; submit the two sheets with valid from 2026-11-30 and assert the load ID, the status and the two lists of section 12.2.
3. Build QueueProbe and RoleProbe and implement AC1: 12 queue rows with table version 1, the team and role code of each row, RW-LITOFF in force in rwb-access, and the notice that carries the same code.
4. Build RollbackStep and implement AC2: version 3 to version 2 in one call, the record IDs unchanged, the next notice from the predecessor, and the role read unchanged.
5. Implement AC3: a queue row naming a role code that rwb-access answers as not in force, the refusal in full with MSG-P1-002, the row named, and no row written.
6. Build CapacityStep and SessionProbe and implement AC4 and AC5: the capacity answer and the placement agree at the cap, the membership row becomes the team scope, and a case outside the team answers 404.
7. Implement AC6, AC7 and AC8: the future valid from answered from the version in force by both services, the repeated file returning the same version with no new row, and the guard refusal with MSG-P4-002.
8. Implement AC9 and AC10, write the evidence report, clean up the synthetic set and the versions, restore the clock, and run the whole suite twice to prove that a repeated run adds no version and no row.

**Done when.** The thirteen test cases of section 16 pass in SIT against the published wave 1 contracts of P3, P4 and P6, the ten criteria of section 7 are signed off with an observable each, one approved load is in force for the queue read, the role read and the notice in the same run, one rollback returns all three readers, no service table was read, the synthetic set is cleaned up, and the evidence report names every criterion with its evidence.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A queue check fails on a row (team code, member role, overflow loop, role code not in force) | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Required column empty, or no rollback reason | Enter {field}. |
| MSG-GEN-002 | Cap outside 1 to 500 | {field} must be between {min} and {max}. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The six texts are copied unchanged from RWB-E1-019 and this story adds no message ID. For MSG-P1-002 the {check} value is the name of the failed check and the {source} and {date} values are the table and the valid-from date of the load. A 404 outside the reader's scope carries no message ID in this story: the scope answer is the P4 rule and the case read answers not found.

### 15. Screens and states

No screen is built or tested by this story. SCR-42 Queues and service levels (states Versions; load) comes in Epic 8, is owned by the APP stories, and reaches rwb-case through the gateway-bff composite route (DP-19); the suite reads the same facts through the operations of section 12.2. The states an operator sees on a version are VALIDATED, APPROVED and ROLLED_BACK, and a version with a future valid from shows APPROVED without changing any queue row. The scope answer and the notice are read through their contracts and not through a screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-019-13-ITG | Access | Integration | RW-CASEOWN calls POST /admin/reference-loads and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-01-ITG | AC1, BR1, BR3 | Integration | Template with 12 queues and 48 members; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-02-ITG | AC2, BR5 | Integration | QUEUE versions 2 and 3; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-03-ITG | AC3, BR6 | Integration | Member U-11 with capacity 40 and 40 open cases; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-04-ITG | AC4, BR2 | Integration | Queue with team code XYZ; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-05-ITG | AC5, BR8 | Integration | Cap 0; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-06-ITG | AC6, BR4 | Integration | Load and approval by U-90; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-07-ITG | AC7, BR5 | Integration | Only one version; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-08-ITG | AC8 | Integration | Same file twice for 2026-12-15; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-09-ITG | AC9, BR3 | Integration | Version 3 with valid from 2026-12-15; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-10-ITG | AC10, BR9 | Integration | Member U-12 without RW-LITOFF; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-11-ITG | AC11, BR2 | Integration | Overflow loop between DS-BKK-CO and DS-BKK-OVF; end-to-end: real services on the wave 1 contracts |
| TC-E1-019-12-ITG | AC12, BR2 | Integration | Row 3 with no assignment method; end-to-end: real services on the wave 1 contracts |

The thirteen legacy test cases of RWB-E1-019 are carried as `-ITG` copies in the legacy order, and the Covers column keeps the legacy criterion numbers, which at component level belong to RWB-P3-E1019-APP. The copies this story signs off against its own criteria are TC-E1-019-13-ITG (AC8 and AC5, extended with the session read), TC-E1-019-01-ITG (AC1 and AC10, extended with the notice read), TC-E1-019-02-ITG (AC2), TC-E1-019-03-ITG (AC4), TC-E1-019-04-ITG and TC-E1-019-10-ITG (AC3, extended with the rwb-access role answer), TC-E1-019-06-ITG (AC9, extended with the delegation version), TC-E1-019-08-ITG (AC7) and TC-E1-019-09-ITG (AC6). The other four copies - TC-E1-019-05-ITG, TC-E1-019-07-ITG, TC-E1-019-11-ITG and TC-E1-019-12-ITG - are regression evidence for the component copy RWB-P3-E1019-APP, which owns their criteria, and they run here on the real services so that a change in one service cannot pass unnoticed. The Level column follows Template and Rules section R7.2: the legacy System level and the legacy Access level both become Integration, because the copy crosses a service boundary.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every queue, member, case, test user and version, and no production data is read, copied or connected to.
- No personal data in events, logs, workflow history, fixtures or the report: member rows are named by user ID only, and the suite carries queue codes, team codes, role codes, version numbers and dates.
- No cross-service table read: the queue version is read through the rwb-case contract, the role list and the scope through the rwb-access contract, and the queue code on a notice through the rwb-comms response; the suite ships with no client for a service schema (DP-01).
- No business value in the test code: team codes, queue codes, methods, caps and members are data; the cap range comes from `queue.cap.max` and the methods from LOV-ASSIGN, both read through the rwb-case contracts (DP-06, DP-07).
- One hop and a 2 s budget on every REST call, with no service called through another service and no cached role answer used past its time-to-live (ADR-020, DP-08, DP-11).
- A version applies whole or not at all, and a queue record ID never changes, so a case keeps its queue across a rollback (BR3, BR5).
- The reference-approval pattern is one pattern: no load is approved by its author, every approval records the author, the approver and the time, and a wrong version is returned by one call (BR4, BR14).
- No production access and no production namespace: the run is pinned to SIT and refuses to start against any other environment, and it restores the clock and removes the synthetic versions at the end.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data, changed without a release | `POST /api/recovery/case/v1/admin/reference-loads`, the approve and rollback operations, `GET /api/recovery/case/v1/queues`, the notice read | TC-E1-019-01-ITG, TC-E1-019-02-ITG, TC-E1-019-03-ITG, TC-E1-019-06-ITG, TC-E1-019-08-ITG, TC-E1-019-09-ITG |
| REQ-ACA-002 | Roles held as data; a role change takes effect without a release | `GET /api/recovery/access/v1/admin/roles`, `GET /api/recovery/access/v1/me/session`, MSG-P1-002 on a role code not in force | TC-E1-019-01-ITG, TC-E1-019-04-ITG, TC-E1-019-10-ITG, TC-E1-019-13-ITG |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow | The session of P4 and the case read of P3, with status 404 outside the team scope | TC-E1-019-13-ITG |
| REQ-ACA-004 | The delegation-of-authority table is reference data and sets every approval limit | The reference-load and approve operations on table "delegation_limit", and the one-call rollback | TC-E1-019-06-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The ten operations of 12.2 and the preflight contract test | Every test case, at the preflight |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| DP-01 | Owner's schema, never another service's tables | One writer per schema: the queue and version tables in `rwb_case`, the roles and the delegation table in `rwb_access`, no queue row in `rwb_comms` | TC-E1-019-01-ITG, TC-E1-019-02-ITG, TC-E1-019-13-ITG |
| DP-07 | Reference-data contract of rwb-case | The queue and membership versions and the lists, read and loaded through the P3 contract | TC-E1-019-01-ITG, TC-E1-019-08-ITG, TC-E1-019-09-ITG |
| DP-08 | Authorise contract of rwb-access and the guard library | `GET /api/recovery/access/v1/admin/roles`, `GET /api/recovery/access/v1/me/session`, MSG-P4-002 | TC-E1-019-04-ITG, TC-E1-019-10-ITG, TC-E1-019-13-ITG |
| RWB-E1-019 (legacy story) | Roles, teams and queues as data: the load, the approve, the apply, the rollback, the capacity answer and the membership query | The ten operations of section 12.2 and the six messages of section 14 | The nine signed-off copies of section 16 |
| RWB-P3-E1019-APP (component copy) | The queue checks, the apply step and the capacity and membership answers in rwb-case | The queue check path, the apply step, the queue read and the placement | The four regression copies of section 16 |

### 19. Out of scope

- The four application builds this run depends on: RWB-P4-E1038-APP, RWB-P3-E1019-APP, RWB-P4-E1019-APP and RWB-P6-E1019-APP.
- The sibling CON, DB and OPS stories of the legacy key, including RWB-P3-E1019-CON and RWB-P3-E1019-DB.
- The criteria the component copy owns: the legacy AC1 to AC12 and the access test, which belong to RWB-P3-E1019-APP, RWB-P4-E1019-APP and RWB-P6-E1019-APP.
- The role list, the permission matrix, scope, masking and the delegation-of-authority table themselves, which are rwb-access data and the RWB-E1-022, RWB-E1-037 and RWB-E1-038 content.
- The reference version store and the load, approve and rollback operations themselves, which are the RWB-P3-E1043-CON content.
- The parameter tables `parameter_catalog` and `parameter_value`, which are the RWB-E1-042 stories.
- Allocation and assignment by these tables (RWB-E1-020) and transfer rules (RWB-E1-021).
- Administration screens for queues (Epic 8, SCR-42) and reallocation when an owner leaves (Epic 2).
- The build of the harness RWB-ITG-W1J01-ITG itself, which is a precondition here and not a deliverable.
- The non-functional epic RWB-ITG-NFR.
