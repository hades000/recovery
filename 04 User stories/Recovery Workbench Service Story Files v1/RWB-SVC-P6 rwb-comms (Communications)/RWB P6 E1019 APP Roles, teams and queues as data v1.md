# RWB-P6-E1019-APP Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P6-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1019-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-CWC-006, REQ-ACA-002) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-019 for rwb-comms in the 19-service realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the role that approves a notice, the queue that owns a notice when it is unserved, and the role that sees the notice panel to be read from the role, team and queue data in force at the moment of use**, so that **a change of team, of queue or of role reaches notices without a code release**.

This story is the rwb-comms part of legacy RWB-E1-019. rwb-comms holds **no role table, no queue table and no membership table**: it reads the roles, the teams, the queues and their members through the published contract of rwb-case and applies what it reads at run time to three uses only:

- the approver role and the approver queue of a notice approval;
- the owner queue of a notice that goes unserved or into the exception path;
- the role that sees the notice panel.

Everything else in the legacy key (the template, the row checks, the apply step, the capacity answer, the rollback and the version store) is the primary slice `RWB-P3-E1019-APP`, its contract `RWB-P3-E1019-CON` and its database story. This story adds one read of the routing in force on base `/api/recovery/comms/v1` (DP-13), the resolver behind it, the authorisation of that read through the guard library (DP-08), the refusal-closed behaviour when the answer is stale, absent or late, and the proof that the service keeps no copy of a role or a queue (DP-01).

**Where the other criteria of the legacy key are owned.** The twelve load, apply, capacity and rollback criteria of RWB-E1-019 (legacy AC1 to AC12) are owned by the primary slice `RWB-P3-E1019-APP` and are not copied here. The legacy access criterion (legacy TC-E1-019-13, a role without the right refused with MSG-P4-002) is carried here as the consumer-side guard test, because that is the one legacy case whose subject still lives in every service that authorises. The legacy ACs are not restated in section 7; the criteria there are new and test only what this service does with the data.

### 2. Business rationale

Team structure and who works which list are held in spreadsheets today, and a change of team needs a change request to IT. The legacy story held every queue, its team, its role, its method, its cap, its overflow queue and its members as versioned tables, loaded from one template through the reference data service, with an approver and a one-call rollback, so that the organization changes without a release. It meets REQ-CWC-006 and REQ-ACA-002 and is the input to allocation, to scope by team and to control CTL-08.

The realignment does not change that rationale; it changes who keeps the data and who reads it. The queues, team codes, role codes, members and capacity are rwb-case data and stay in schema `rwb_case`; the Recovery roles and their permissions are rwb-access data; and every other service, rwb-comms included, becomes a **reader** of the published documents. That is what makes the promise true at the level of the whole organization rather than at the level of one table: a queue change is one rwb-case reference load, a role change is one rwb-access change, and neither of them is a release of rwb-comms.

rwb-comms still needs three answers to do its own work. A notice approval needs an approver role and a queue, because the notice approval is decision D7.1 and it needs the approval right of its capability area; a notice that comes back unserved must go to the queue that owns it, with reason `NOTICE_UNSERVED`; and the notice panel is shown only to a role that holds the read right of the area. Today those three answers are constants in a monolith. In the target they are values read from the contract at the moment of use, so a team that is reorganized on a Monday is served correctly on the Tuesday without anybody building anything.

This story therefore serves REQ-CWC-006 and REQ-ACA-002, and it carries control CTL-08 on its side of the boundary: a load with any failed row is refused in full by rwb-case, and rwb-comms never fills the hole with a default. Where a source does not fix a value, this story refuses closed rather than inventing a role, a queue or a team.

### 3. Preconditions

- `RWB-P3-E1019-CON` is published: the OpenAPI 3.1 documents for `GET /api/recovery/case/v1/queues` and the two reference-load operations, the AsyncAPI schemas of the `rwb.case.events.v1` events that carry queue and owner codes, and the contract fake. The LOV read of the rwb-case reference-data contract is needed for the names behind the codes, and its operation and element names are Not specified in the source documents (GAP-1174; ASM-2121). The build runs against the fake from Day 1 (DP-11), and this is the only contract in the story's Contract dependencies.
- The queue set in force is a version of `queue` and `queue_member` in `rwb_case`: TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK" (assumed codes; owner Shared operations), and queues such as "LIT-BKK-OFF", "DIL-BKK-CO" and "TDR-BKK-CO" carry a team code, a role code and a `table_version` (legacy RWB-E1-019 sections 1 and 3).
- The role codes this story names are the ones TSD P6 v2 T6.1 holds: RW-LITOFF, RW-LEGAL, RW-CASEOWN, RW-CONDUCT, RW-PLATADM and RW-BIANAL, each with its Documents and Litigation rights. The list itself is reference data reached through the P3 list operation and the rwb-access authorise answer, never a constant in code (DP-07).
- The rwb-access authorise contract and its guard library are available (DP-08). They are **not** in this story's dependency lists: Contract dependencies holds `RWB-P3-E1019-CON` only and Depends on (build) is None, so the guard is built against the published access document and its fake, and the missing rows are carried as a gap (GAP-1175; ASM-2122).
- The platform contracts that the DP table attaches to DP-06, DP-07, DP-14 and DP-15 (`RWB-PLT-E1042-CON` and `RWB-P3-E1042-CON`, `RWB-PLT-E1043-CON` and `RWB-P3-E1043-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1044-CON`) are also absent from the plan's lists. The service builds against the platform release train and the P3 published documents, and the omission is carried as one combined gap (GAP-1174; ASM-2121).
- The notice operations that call the resolver exist in rwb-comms: notice generation and dispatch (`RWB-P6-E1052-APP`, `RWB-P6-E1055-APP`) own the notice row and the delivery result, and this story is wired behind them. It provides no notice lifecycle of its own.
- No source decides whether a reader keeps a local reference cache. This story decides it the other way: the answer of a read lives for the life of that call only, and no cache table is created, because a cached role or queue row in `rwb_comms` is exactly the local copy DP-01 and AC7 forbid (GAP-1177; ASM-2124).
- The service reaches the database through the rwb-comms login in schema `rwb_comms` (DP-02, DP-01), and holds no grant on `rwb_case` or `rwb_access`.
- No name of a person is read, stored or logged: a queue member is an object ID in `rwb_case`, and this story reads no member row at all, because a routing answer needs a role code and a queue code and not a person.

### 4. Flow

1. A notice is read, approved or put on its exception path on the rwb-comms operations of `RWB-P6-E1052-APP` and `RWB-P6-E1055-APP`, reached through the gateway-bff composite route of the notice screens (DP-19).
2. gateway-bff declares the capability area and the right of the screen, the scope and the session, and calls rwb-comms. A role without the Documents read right is refused there with MSG-P4-002; this story repeats the check at its own operation so that a direct call is refused the same way.
3. NoticeRoutingController accepts `GET /api/recovery/comms/v1/admin/notice-routing?noticeId=...` and the resolver authorises the caller through the guard library: role, Documents R or Litigation A as the use needs, and scope, read once from the rwb-access authorise contract (DP-08, one hop, 2 s, breaker).
4. NoticeFactsReader reads the notice row in `rwb_comms` for its id, its type, its case and its state (own schema, DP-01); an unknown notice answers 404 and nothing else is read.
5. QueueReferenceReader reads the queue set in force once per call from `GET /api/recovery/case/v1/queues` (DP-11): each queue code with its team code, its role code and the `table_version` of the set. The list of values for the role and team codes comes from the LOV read of the rwb-case reference-data contract (DP-07), read as data rows with their version, when the answer has to be shown as a name; the operation and its element names are Not specified in the source documents (GAP-1174; ASM-2121).
6. CaseQueueReader reads the case of the notice once from `GET /api/recovery/case/v1/cases/{caseId}` for the queue the case sits in. That queue is the owner queue of the notice.
7. NoticeRoutingResolver composes the answer: the notice id and type, the case, the queue in force, the team code of that queue, the role code the queue names as the approver role, and the `table_version` the contract returned. The approver role is confirmed to hold the approval right of the decision D7.1 through one more authorise call; a role that does not hold it is not replaced by the next role in the list, the read is refused with MSG-P4-002.
8. The controller answers 200 with the routing. Nothing is written: the answer is a read, and the service keeps no row of it.
9. A notice whose delivery result is `UNDELIVERABLE` goes to its exception path with reason `NOTICE_UNSERVED`: rwb-comms names the owner queue from the same resolver answer and asks rwb-case for the transfer. The transfer request, the assignment row and the case move are rwb-case's (Architecture v5 slide 14; FSD P6 AC-ALT-P6-001-02), and rwb-comms writes no queue, assignment or case row.
10. A stale answer (a `table_version` older than the version the contract now returns), an absent queue, a queue whose role holds no approval right, a missing case queue or an answer that does not arrive inside 2 s refuses closed with 409, 404, 403 or 503; no default role, no default queue and no remembered version is used.
11. Every read is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). The role codes, the team codes, the queue codes, the rights and the valid-from dates are data (DP-06, DP-07), never values in code.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's role lacks the Documents read right | Refused before any routing is composed | MSG-P4-002 | AC4 |
| X2 | The caller lacks the approval right of decision D7.1 | Refused; no approver role and no approver queue is returned | MSG-P4-002 | AC4 |
| X3 | The queue set in force holds no queue for the queue code of the case | Refused closed; the answer is not patched from another queue | MSG-GEN-004 | AC5 |
| X4 | The role the queue names holds no approval right | Refused closed; no next role is guessed from the list | MSG-P4-002 | AC2, AC4 |
| X5 | The queue read answers a `table_version` older than the version in force | One more read; still stale means refused closed, and no routing is served from the stale answer | MSG-GEN-004 | AC5 |
| X6 | The rwb-case queue read does not answer inside the 2 s budget | Refused closed; no approver role, no owner queue and no default | MSG-GEN-004 | AC6 |
| X7 | The rwb-case case read answers no queue for the case | Refused closed with no owner queue; the notice stays where it is and the exception path does not move a case | MSG-GEN-004 | AC3, AC6 |
| X8 | The rwb-access contract does not answer inside the 2 s budget | Refused closed; no role answer is used past its time to live | MSG-P4-002 | AC4, AC6 |
| X9 | The notice id is unknown, or the case is outside the caller's scope | 404, or the scope refusal of the guard; nothing is resolved | MSG-P4-002 | AC4 |
| X10 | A caller sends a version, a role code or a queue code of its own | Ignored; the answer carries only what the contract returned for the version in force | MSG-GEN-004 | AC5, AC8 |
| X11 | The legacy load endpoints are called on this service | There is no reference-load operation in rwb-comms; the load path is rwb-case's, and the caller is answered 404 | None | AC7 |

X11 is the legacy access case of the split: the legacy test called an endpoint that now belongs to another service, so the only correct answer here is that rwb-comms serves none (GAP-1178; ASM-2125).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P3-E1019-CON` and its fakes, the `rwb_comms` schema of the notice stories and the guard library; the queue set, the case and the authorise answer are stubs on Day 1 |
| Negotiable | The role codes, queue codes, team codes and rights are data; the answer shape of the routing read is settled with the screen team |
| Valuable | A notice goes to the role and the queue that hold the work today, and a team or role change lands without a release of rwb-comms |
| Estimable | One read operation, one resolver, three reader components, one guard client, no table |
| Small | Fits one sprint as a secondary slice of a legacy key split across rwb-case, rwb-access and rwb-comms |
| Testable | Each criterion runs against the P3 queue fake, the P3 case fake and the rwb-access fake, including the stale and late answers |

### 7. Acceptance criteria

```gherkin
Feature: Roles, teams and queues as data, read by rwb-comms

  Background:
    Given TEAM holds "TDR-BKK", "DIL-BKK", "LIT-BKK", "NPA-BKK", "DS-BKK" and "WO-BKK"
    Given queue "LIT-BKK-OFF" belongs to team "LIT-BKK" with role RW-LITOFF
    Given the rwb-case contract mock returns queue "LIT-BKK-OFF" with team "LIT-BKK", role RW-LITOFF and table_version 1
    Given the rwb-access contract mock returns RW-LITOFF with Litigation CRUA

  Scenario: AC1 A queue and role change reaches rwb-comms without a release (new, D-RCV-60)
    Given the routing for notice "N-0101" is read and answers role RW-LITOFF and queue "LIT-BKK-OFF" from table_version 1
    When the rwb-case contract mock returns queue "LIT-BKK-OFF" with role RW-LEGAL and table_version 2, the version approved by the queue owner
    And the routing for notice "N-0101" is read again
    Then the second answer names role RW-LEGAL and queue "LIT-BKK-OFF" with table_version 2
    Then no release, no restart and no configuration change was made in rwb-comms
    Then the first answer is unchanged and no row of it was kept

  Scenario: AC2 The approver role and queue of a notice approval (new, D-RCV-60)
    Given notice "N-0101" is of type "DEMAND" for case "RC-2026-000321" in queue "LIT-BKK-OFF"
    Given the rwb-case contract mock returns case "RC-2026-000321" in queue "LIT-BKK-OFF"
    When the approval routing of notice "N-0101" is resolved
    Then the answer names approver role RW-LITOFF, approver queue "LIT-BKK-OFF", team "LIT-BKK" and table_version 1
    Then the approval right of decision D7.1 is asked of rwb-access for RW-LITOFF and answers A
    Then no role code and no queue code in the answer comes from a table in rwb_comms

  Scenario: AC3 The owner queue of a notice that goes unserved (new, D-RCV-60)
    Given notice "N-0101" is "Sent" on 2026-12-15 and its delivery result is "UNDELIVERABLE"
    Given the rwb-case contract mock returns case "RC-2026-000321" in queue "LIT-BKK-OFF"
    When notice "N-0101" is put on the exception path with reason "NOTICE_UNSERVED"
    Then the resolver answers owner queue "LIT-BKK-OFF" and team "LIT-BKK" from the rwb-case read
    Then the request to rwb-case names queue "LIT-BKK-OFF" and reason "NOTICE_UNSERVED"
    Then rwb-comms writes no queue row, no assignment row and no case row

  Scenario: AC4 A role without the right is refused with MSG-P4-002 (new, D-RCV-60)
    Given RW-CASEOWN holds Documents CRU and Litigation R, and holds no Litigation A
    Given the rwb-access contract mock returns RW-CASEOWN with Litigation R only
    When RW-CASEOWN asks for the approval routing of notice "N-0101"
    Then the response is status 403 with MSG-P4-002
    Then no approver role and no approver queue is returned
    Then no notice approval is requested and no notice row is read

  Scenario: AC5 A stale queue answer is refused closed (new, D-RCV-60)
    Given the rwb-case contract mock returns queue "LIT-BKK-OFF" with table_version 1 while the version in force is 2
    When the approval routing of notice "N-0101" is resolved with that answer
    Then the resolver reads the queue set once more
    Then the stale answer still carries table_version 1 and the response is status 409 with MSG-GEN-004
    Then no approver role, no approver queue and no owner queue is returned from the stale answer

  Scenario: AC6 A delayed queue answer is refused closed (new, D-RCV-60)
    Given the rwb-case contract mock delays the queue answer beyond 2 s
    When the approval routing of notice "N-0101" is resolved
    Then the response is status 503 and no approver role and no owner queue is returned
    Then no default role and no default queue is used
    Then one degraded-read entry records the timeout with the queue code and the read at time

  Scenario: AC7 No local role or queue row exists (new, D-RCV-60)
    Given the schema "rwb_comms" is deployed from its own Flyway sequence
    When the schema is inspected for the reference data of roles, teams, queues and members
    Then no table, view, materialised view or synonym of a role, a team, a queue or a member exists in "rwb_comms"
    Then the only role and queue values held by the service are the codes received in the answer of one call
    Then the migration of this story creates no such object and no grant on "rwb_case" or "rwb_access"

  Scenario: AC8 The version in force is the one the contract returns (new, D-RCV-60)
    Given the rwb-case contract mock returns queue "LIT-BKK-OFF" with table_version 2 on 2026-12-14 and with table_version 3 from 2026-12-15
    When the approval routing of notice "N-0101" is resolved on 2026-12-14
    Then the answer carries table_version 2
    When the approval routing of notice "N-0101" is resolved on 2026-12-15
    Then the answer carries table_version 3
    Then a version in the request, a role code in the request or a version remembered from an earlier read is ignored
```

All eight criteria are new in the realignment and test only what rwb-comms does with the data it reads. The legacy criteria of RWB-E1-019 are not restated: the twelve load, apply, capacity and rollback criteria are owned by the primary slice `RWB-P3-E1019-APP`, and the legacy access criterion is carried here as TC-E1-019-13. Every cross-service line above is the mock of an owner's published answer with the values the sources fix; no business value was added.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every queue belongs to one team and one role, and the queue is the only place a role code and a team code meet | queue.team_code (DF-WRK-004), queue.role_code (DF-WRK-005); LOV-TEAM, LOV-ROLE |
| BR2 | A version takes effect on its valid from date after approval, and rwb-comms reads the version in force at the moment of use, never a version remembered from an earlier call | Reference data change process, steps 5 and 6; REQ-CWC-006; legacy BR3 |
| BR3 | A load with any failed row is refused in full by its owner, and no reader fills the hole with a default | Reference data change process, step 3; CTL-08; legacy BR2 |
| BR4 | The author of a load cannot approve it; rwb-comms relies on that answer and does not re-implement it | Separation of duty table; CTL-08; legacy BR4 |
| BR5 | The approver of a notice holds the approval right of decision D7.1, which is Litigation A in TSD P6 v2 T6.1; a role without it is refused with MSG-P4-002 and never replaced | TSD P6 v2 T6.1 and T6.2; DP-08 |
| BR6 | rwb-comms holds no role, team, queue or member row, reads none from another schema and joins nothing across services | DP-01; Architecture v5 slide 41 |
| BR7 | A stale, absent or late answer is refused closed; the service never guesses a role, a queue or a team | DP-11; ADR-020; legacy exception paths X1 to X9 |
| BR8 | The owner queue of an unserved notice is the queue the rwb-case read names, and the transfer that follows is rwb-case's operation, not this service's | FSD P6 AC-ALT-P6-001-02; Architecture v5 slide 14 |
| BR9 | The notice panel is shown to a role that holds the read right of the area in TSD P6 v2 T6.1, and to no other role | TSD P6 v2 T6.1, T6.2; legacy section 15 |
| BR10 | One REST base, one hop and a 2 s timeout on every read; the codes, rights and dates are data and never values in code | DP-13, DP-11, DP-06, DP-07; legacy section 17 |

### 9. State transitions

None. This story changes no case status, no notice status and no reference-version status: the case state machine is rwb-case's, the notice lifecycle is the notice stories' and the version status is rwb-case's. The routing answer is a read that carries the `table_version` it was composed from, so a screen can show which version answered without the service storing anything.

The one state the operator can see is the answer itself: `RESOLVED` (a role and a queue were named from the version in force), `REFUSED` (a right is missing, MSG-P4-002), `STALE` (409, MSG-GEN-004) and `UNAVAILABLE` (503, with a degraded-read entry). These are response states, not rows.

### 10. Authority

The rights are the TSD P6 v2 T6.1 rights of the capability areas this story touches, Documents and Litigation. They are declared by the operation and asked of the rwb-access authorise contract through the guard library, one hop and 2 s, cached for the life of the call (DP-08, DP-11).

| Who | Documents (T6.1) | Litigation (T6.1) | What this story allows |
|---|---|---|---|
| RW-LITOFF, litigation officer | CRU | CRUA | Sees the notice panel, resolves the routing and approves a notice in its queue |
| RW-LEGAL, legal counsel | CRUA | RA | Approves where the queue names it; reads the routing |
| RW-CASEOWN, case owner | CRU | R | Sees the notice panel; refused the approval routing with MSG-P4-002 |
| RW-CONDUCT, conduct and QA officer | R | R | Reads the routing; no approval |
| RW-TEAMMGR, team manager | R | R | Reads the routing of its team; no approval |
| RW-PLATADM, platform administrator | R | - | Reads the routing; no approval |
| RW-BIANAL, reporting and BI analyst | - | R | Refused the notice panel and the routing with MSG-P4-002 |
| SY-CASEWF, case workflow module | R | R | Service identity: reads the owner queue for the exception path, no person involved |

Every "who" above is a role code, and the role codes, their rights and their separation-of-duty conflicts are held as data in rwb-access (P4). The authorise contract that answers them is `RWB-P4-E1037-CON` with the guard library `RWB-PLT-E1037-CON`, and neither is in this story's dependency lists, so the build runs against the published access document and its fake (GAP-1175; ASM-2122). No role in this story grants itself a right, and no path in this story reads `rwb_access` by SQL.

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-WRK-001 to DF-WRK-008 | queue | the queue code, name, team code, role code, method, cap and overflow queue | P3 (rwb_case) | Read through the P3 queue operation |
| DF-WRK-038 | queue | table_version | P3 (rwb_case) | Read through the P3 queue operation and carried in the answer |
| DF-WRK-005 | queue | role_code | P3 (rwb_case) | Read through the P3 queue operation; the approver role |
| DF-WRK-045 to DF-WRK-052 | queue_member | all fields | P3 (rwb_case) | Not read: this story needs no member, no capacity and no skill |
| DF-REF-035 | role | role_code | P4 (rwb_access) | Read through the rwb-access authorise answer, never by SQL |
| DF-REF-028, DF-REF-029 | lov_value | lov_code, value_code | P3 (rwb_case) | Read through the P3 list operation for the role and team names |
| DF-LEG-015, DF-LEG-016, DF-LEG-018 | notice | id, case_id, notice_type | P6 (rwb_comms) | Read in the service's own schema |
| DF-CAS-001, DF-CAS-010 | recovery_case | id, queue_id | P3 (rwb_case) | Read through the P3 case read |

No row of `queue`, `queue_member`, `queue_measure`, `role`, `permission` or `assignment` is written by this story, and no statement in it names a table in another schema. The values it serves are the values it received: the answer of one call, with the `table_version` of that call (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary; the legacy physical names QUEUE, QUEUE_MEMBER and `queue.table_version` are kept by their owner, rwb-case.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/admin/notice-routing` | None in the P6 API specification, which lists API-P6-001 to API-P6-011 only (GAP-1179; ASM-2126) | Query `noticeId` (uuid) | 200 `NoticeRouting`: notice id, notice type, case id, queue code, team code, approver role code, owner queue code, `table_version`, read at | Documents R, scope applied; Litigation A for the approval use | GET, no key |

Errors: 401 no session or no role (MSG-P4-001); 403 the role lacks the right, or the queue's role holds no approval right (MSG-P4-002); 404 the notice is unknown or the case is outside the scope; 409 the queue answer is stale or holds no queue for the case, or a version of the caller's own was sent (MSG-GEN-004); 503 a consumed read did not answer inside the budget (MSG-GEN-004), or the P3 answer was refused at load with MSG-P1-002, MSG-GEN-001, MSG-GEN-002, MSG-P3-015 or MSG-P7-002 relayed unchanged.

The operation is this story's design: the P6 API specification of the module has no operation that exposes the approver role and the approver queue of a notice, and the screen that needs it reads a composite route. It is therefore published with its shape fixed here and is not claimed as an API identifier until the module's API file is revised (GAP-1179; ASM-2126).

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| `GET /api/recovery/case/v1/queues` | P3 rwb-case | The queue set in force: queue code, team code, role code, `table_version`; one hop, 2 s, breaker; faked |
| The LOV read of the rwb-case reference-data contract (RWB-P3-E1043-CON) | P3 rwb-case | LOV-ROLE and LOV-TEAM as data rows, for the names behind the codes (DP-07); the operation is Not specified in the source documents (GAP-1174; ASM-2121); faked |
| `POST /api/recovery/access/v1/authorise` | P4 rwb-access | Role, right and scope of the caller and of the resolved role, through the guard library (DP-08); faked; not in this story's Contract dependencies (GAP-1175) |
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The queue the case sits in, which is the owner queue of the notice; faked; not in this story's Contract dependencies, so the fake is derived from the published P3 document |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). Queue membership is **not** read: `queue_member`, its capacity and its skills are not needed for a routing answer, and no operation of `RWB-P3-E1019-CON` publishes them anyway, since the P3 membership query is an in-process interface there and not a REST operation (GAP-1176; ASM-2123). The boundary between the two sources is fixed: the queue, its team code, its role code and the version are P3's; the role, its rights and the scope are P4's (GAP-1176).

#### 12.3 Events published

None. This story publishes no event: a routing answer is a read and changes no state, so nothing is written to the outbox and nothing is added to `rwb.comms.events.v1`, whose events remain `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` under the naming of DP-14 (Architecture v5 slide 17; RWB-PLT-E1047-CON).

#### 12.4 Events consumed

None. A change of a role, a team or a queue reaches rwb-comms on the next read of the contract, and a change of an access policy reaches the guard library, which is the platform's (DP-08). This story registers no consumer, no inbox group and no retry topic, because DP-09 is not in its pattern set and the read is the whole mechanism.

#### 12.5 Workflows and activities

None. The routing is a synchronous read with a 2 s budget; no workflow, no activity and no child workflow is started on task queue `rwb-comms` by this story.

#### 12.6 Schedules

None. There is no sweep, no cache warm-up and no nightly refresh: a schedule would be a stored copy of the data under another name, which BR6 and AC7 forbid. No Temporal Schedule is registered.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | Read for the notice type, the case and the state; written by the notice stories, not here |
| No table of a role, a team, a queue or a member | Not owned, never created | AC7: no local copy and no reference-cache table |

No object is added to the service's Flyway sequence by this story. A cache table was considered and rejected: any row of a role, a queue or a team in `rwb_comms` is the local copy DP-01 forbids, and it would serve a value that is no longer in force. The decision is this story's own, because no source decides a reader's cache (GAP-1177; ASM-2124). The per-service Flyway sequence is nevertheless the pattern the story obeys (DP-15): if a later story adds a cache, it is created in `rwb_comms` on that sequence and never in another schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case queue WireMock | The queue set with "LIT-BKK-OFF" for "LIT-BKK" and RW-LITOFF at `table_version` 1, then the same queue with RW-LEGAL at `table_version` 2; an answer that holds no queue for the case; a stale answer; a delayed answer beyond 2 s; a refused load carrying MSG-P1-002, MSG-GEN-001, MSG-GEN-002, MSG-P3-015 or MSG-P7-002 | AC1, AC3, AC5, AC6, AC8 and the relayed refusals |
| rwb-case case WireMock | `GET /cases/{caseId}` for "RC-2026-000321" in queue "LIT-BKK-OFF"; a case with no queue; a case outside the scope; a delayed answer | AC2, AC3, AC6 |
| rwb-case reference-data WireMock | LOV-ROLE with RW-LITOFF, RW-LEGAL, RW-CASEOWN, RW-CONDUCT, RW-PLATADM and RW-BIANAL, and LOV-TEAM with the six team codes | AC1, AC2 |
| rwb-access authorise WireMock | RW-LITOFF with Litigation CRUA; RW-CASEOWN with Litigation R only; RW-BIANAL with Documents none; a role answer delayed beyond 2 s | AC2, AC4, AC6 |
| guard library stub | A healthy answer and a stopped answer for the 503 path | AC4, AC6 |

The exact field-level shape of the P3 queue answer and of the P3 case queue field is Not specified in the source documents (GAP-1176; ASM-2123); the stubs are derived from the published P3 story and its operation list, and each stub is replaced by the real owner as the wave 1 stories land.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `GET /admin/notice-routing` provided; the queue set, the list, the authorise answer and the case read consumed; one hop, 2 s, breaker |
| Kafka | None | No produce and no consume; `rwb.comms.events.v1` keeps the three notice events of the service under the DP-14 naming |
| Temporal | None | No workflow, activity or Schedule in this story |
| File | None | Nothing is read from or written to a file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `routing`, Java package `th.co.scb.ace.workbench.recovery.comms.routing`. Service base `/api/recovery/comms/v1`, schema `rwb_comms`, topic `rwb.comms.events.v1`, task queue `rwb-comms` (neither used by this story).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies in the table are the ones the DP table attaches to each pattern; they are not in this story's `Depends on (build)` or `Contract dependencies` lists, which the plan fixed at `None` and `RWB-P3-E1019-CON` (GAP-1174; ASM-2121). The build therefore goes against the platform release train and the P3 published documents, and DP-08's authorise contract is additionally carried by its own gap (GAP-1175). DP-14 applies to the naming of `rwb.comms.events.v1` and of its events only, since this story publishes none; DP-15 applies as a constraint on where any later object is created, and this story creates none.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeRoutingController | Controller | `GET /admin/notice-routing`, the query and path validation, and the problem mapping for 401, 403, 404, 409 and 503 |
| NoticeRoutingResolver | Service | Composes the answer: the queue in force, its team and role codes, the approver role, the owner queue and the table version |
| QueueReferenceReader | Client | The P3 queue read and the P3 list read, cached for the life of one call only |
| CaseQueueReader | Client | The P3 case read that names the queue the case sits in, with the absent-queue path refused closed |
| NoticeFactsReader | Repository | The notice row in `rwb_comms` for the type, the case and the state |
| AccessGuardClient | Client | The rwb-access authorise contract through the guard library, one hop, 2 s, breaker (DP-08, DP-11) |
| DegradedReadRecorder | Service | One entry per degraded read, with the queue code, the read at time and the service that did not answer; no personal data |

**Database and migrations**

- Reads `notice` in `rwb_comms`; creates no table, view, index or grant.
- No migration file is added by this story, and no statement names `rwb_case`, `rwb_access` or any other schema (DP-01, DP-15). The service login is the rwb-comms login and it holds no privilege on another schema (DP-02).

**Configuration and reference data**

- The role and team names behind the codes: LOV-ROLE and LOV-TEAM through the LOV read of the P3 reference-data contract (DP-07), whose operation is Not specified in the source documents (GAP-1174; ASM-2121).
- The approval right of decision D7.1: Litigation A, asked of the authorise contract and never written as a rule in code (DP-08).
- The read budget: one hop, 2 s, one retry with jitter on a GET, a breaker per target (DP-11, ADR-020).
- The feature switch `rwb.comms.notice-routing`, read as service configuration: off answers 503 for the routing read and leaves every notice operation on its own path; it never allows a default role or a default queue.

**Build steps**

1. NoticeRoutingController and NoticeRoutingResolver over the shape of section 12.1, with the guard first; test AC4.
2. QueueReferenceReader against the P3 queue fake, with the `table_version` carried through; test AC1 and AC8.
3. CaseQueueReader and NoticeFactsReader, with the absent-queue and unknown-notice paths; test AC2, AC3 and X7.
4. The stale and delayed paths: one re-read, the 409 of MSG-GEN-004, the 503 and the degraded-read entry; test AC5 and AC6.
5. The authorise call for the resolved role, with the refusal of a role that holds no approval right; test X4 and AC4.
6. The no-copy proof: a schema inspection test that fails when a role, queue or member object appears in `rwb_comms`; test AC7.
7. The gateway-bff route behind the notice panel and the routing panel of the notice screens, against the fakes; then the contract-fake run of every consumed answer in isolation, so the story builds before rwb-access and the P3 queue set are live in SIT.

**Feature switch.** `rwb.comms.notice-routing`, read as service configuration; off refuses the routing read closed and allows nothing.

**Done when.** The tests in section 16 pass, the schema inspection shows no role, queue or member object in `rwb_comms`, and a SIT week shows the routing following the P3 queue set from version 1 to version 2 without a release or a restart while every stale, absent and late answer is refused closed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A queue check failed on a row at rwb-case, and the P3 answer that carries it reaches this story | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | A required value is missing, or the notice id is empty | Enter {field}. |
| MSG-GEN-002 | A cap outside 1 to 500 is answered by the P3 load path and relayed here | {field} must be between {min} and {max}. |
| MSG-P7-002 | The approver of a notice is its author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | A rollback with no earlier version is answered by the P3 load path and relayed here | There is no earlier version of {table} to return to. |
| MSG-P4-001 | No session, or no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The role lacks the right, or the queue's role holds no approval right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | The queue answer is stale, an absent queue, or a late read on the routing path | Someone else changed this record. Reload it to see their change. |

The texts are copied unchanged from the legacy story and the shared message set. The five load-path messages (MSG-P1-002, MSG-GEN-001, MSG-GEN-002, MSG-P7-002, MSG-P3-015) belong to rwb-case now and are relayed unchanged when its answer carries them; rwb-comms never rewords a refusal of the owner, and it never turns one into a routing answer.

### 15. Screens and states

The notice panel and the notice administration screens, reached through gateway-bff composite routes (DP-19). This story builds no screen: it serves the routing read behind the panel and the routing strip of the administration screens, and it lets the screen show the queue, the team, the approver role and the table version that answered.

States the screen shows: resolved (queue, team, approver role and `table_version`), refused with MSG-P4-002, stale with MSG-GEN-004, unavailable with 503. No screen shows a member, a person or a capacity, because this story reads none of them. The administration of the queue set itself is SCR-42 Queues and service levels in Epic 8 and reaches rwb-case, not this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-019-13 | AC4 | Component | RW-CASEOWN calls the approval routing with Litigation R and is refused with MSG-P4-002 |
| TC-E1-019-01 | AC1, AC2 | End to end | Queue set with 12 queues and 48 members; "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF |
| TC-E1-019-02 | AC6 | NFR | QUEUE versions 2 and 3, with the version in force rolled back while the routing is read |
| TC-E1-019-03 | AC3 | End to end | Member U-11 with capacity 40 and 40 open cases; the owner queue read for the unserved notice |
| TC-E1-019-04 | AC5 | End to end | Queue with team code XYZ |
| TC-E1-019-05 | AC5 | End to end | Cap 0 |
| TC-E1-019-06 | AC2 | End to end | Load and approval by U-90; the approver role and queue resolved for the author |
| TC-E1-019-07 | AC5 | End to end | Only one version |
| TC-E1-019-08 | AC7 | End to end | Same file twice for 2026-12-15; no second answer and no stored copy |
| TC-E1-019-09 | AC8 | End to end | Version 3 with valid from 2026-12-15 |
| TC-E1-019-10 | AC1 | End to end | Member U-12 without RW-LITOFF |
| TC-E1-019-11 | AC3 | End to end | Overflow loop between DS-BKK-CO and DS-BKK-OVF |
| TC-E1-019-12 | AC7 | End to end | Row 3 with no assignment method |

The IDs, their order and the Data of the thirteen legacy cases are kept. The Level follows the mapping used across the set: legacy System is End to end, legacy Access is Component, and TC-E1-019-02 is NFR because it forces the rollback of a version in force while the routing is being read, which is the forced-failure row of this key. The Covers column points at this story's new criteria, because the legacy cases were written against the load and apply path that the primary slice `RWB-P3-E1019-APP` now owns: here the same data proves the consumer side, that the answer comes from the version in force and from nowhere else, and that a refused, rolled-back or absent version never becomes a role or a queue. The legacy access case is adapted to the operation this service serves, since the legacy endpoint it called is rwb-case's and rwb-comms serves no reference load at all (GAP-1178; ASM-2125). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the role codes, team codes, queue codes, rights and valid-from dates come from the P3 contract, the P3 reference-data contract and the rwb-access answer, and never from a constant (DP-06, DP-07, DP-08).
- No personal data in events, workflow inputs, logs, tests or prompts: a member is an object ID in rwb-case, this story reads no member row, and a degraded-read entry carries a queue code and a time only.
- ACE data only through the owner's contract or the owner's `v_ace_*` views; this story reads no ACE table and no ACE view.
- No cross-schema read and no cross-service write: the queue set, the team codes, the role codes and the version are P3's, the roles and their rights are P4's, and rwb-comms reaches both through their contracts and holds no copy (DP-01).
- No local copy and no cache table: the answer of a read lives for the life of that call, and the schema inspection test of AC7 fails the build if a role, queue or member object appears in `rwb_comms` (GAP-1177).
- One REST base, one hop and a 2 s timeout on every read, with a breaker and one retry with jitter on a GET; a slow answer refuses the routing closed (DP-11, DP-13, ADR-020).
- A stale, absent or late answer is refused closed with MSG-GEN-004 or 503; the service never guesses a role, a queue or a team, and never serves a value from a version that is no longer in force.
- The guard is a library, not a local re-implementation: the rights are asked, never computed, and a refusal is MSG-P4-002 in every service (DP-08; GAP-1175).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data that change without a code release | Business Requirements Epic 1 v4, sections 3.3 and 5.3 | FEAT-CWC-06 | All recovery processes | R-UNI-38 | TC-E1-019-01, TC-E1-019-02, TC-E1-019-03, TC-E1-019-08, TC-E1-019-09, TC-E1-019-10 |
| REQ-ACA-002 | Roles held as data; a role change takes effect without a code release | Business Requirements Epic 1 v4, sections 3.4 and 5.4 | FEAT-ACA-03 | All recovery processes | None | TC-E1-019-01, TC-E1-019-06, TC-E1-019-10 |
| CTL-08 | A load with any failed row is refused in full, and the author of a load cannot approve it | Legacy RWB-E1-019 sections 2 and 8; the control code is not present in the Business Rules and Routing Logic v4 extract (GAP-1180; ASM-2127) | FEAT-CWC-06, FEAT-ACA-03 | All recovery processes | CTL-08 | TC-E1-019-04, TC-E1-019-05, TC-E1-019-06, TC-E1-019-12 |
| RWB-E1-019 | The legacy key this story is split from, with the twelve load, apply, capacity and rollback criteria owned by RWB-P3-E1019-APP and the access case kept here | Legacy section 7 | FEAT-CWC-06, FEAT-ACA-03 | All recovery processes | BR1 to BR10 of section 8 | All thirteen cases of section 16 |
| DP set | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 | Template and Rules section R5.5 | - | - | - | TC-E1-019-01, TC-E1-019-06, TC-E1-019-13 |
| ADR-013 | 19 services inside ACE, each with its own schema and login | Architecture v5 slides 20 and 41 | - | - | - | TC-E1-019-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | Architecture v5 slide 41 | - | - | - | TC-E1-019-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Template and Rules section R5.5, DP-11 | - | - | - | TC-E1-019-02, TC-E1-019-13 |
| ADR-021 | Per-service Flyway and migration ownership | Template and Rules section R5.5, DP-15 | - | - | - | TC-E1-019-08 |

The control code CTL-08 is carried from the legacy story and the FSD because no register in the sources read holds it; the citation keeps the requirement visible instead of dropping it (GAP-1180; ASM-2127).

### 19. Out of scope

- The queue, team, role-code and membership tables, their load, their checks, their apply step, their capacity answer and their rollback: rwb-case, `RWB-P3-E1019-APP`, `RWB-P3-E1019-CON` and `RWB-P3-E1019-DB`. The legacy load endpoint has no rwb-comms target (GAP-1178).
- The Recovery roles as data, the permission matrix, scope, masking and the delegation-of-authority table: rwb-access (P4), the E1-022, E1-037 and E1-038 legacy content and `RWB-P4-E1037-CON`.
- The allocation engine, assignment and transfer of a case between queues and owners, including the `NOTICE_UNSERVED` transfer itself: rwb-case, `RWB-P3-E1020-APP` and `RWB-P3-E1021-APP`.
- The notice operations and their lifecycle, including the notice approval call: `RWB-P6-E1052-APP`, `RWB-P6-E1055-APP` and the approval endpoint of rwb-decision.
- The template administration screens and their approval: `RWB-P6-E1052-APP` and `RWB-P6-E1046-APP`.
- The composite routes of the notice screens and of the case screens: `RWB-PLT-N001-CON`.
- The administration screens for queues and service levels (Epic 8, SCR-42).
- Self-service on LINE and HOME.SCB, and partner access to notices (Epic 4).
- Reallocation when an owner leaves (Epic 2, R-UNI-18).
- Any event of a queue or a role change: no such event exists in Arch v5 slides 42 and 43, and this story consumes none.
