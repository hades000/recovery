# RWB-ITG-AD014-ITG Configure queues

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-AD014-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1019-APP, RWB-P4-AD014-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-014 Configure queues as the wave 4 integration proof that one approved queue version is in force for allocation across rwb-case, rwb-access and rwb-decision from its valid-from date, and that a queue file naming an overflow queue that does not exist refuses the whole load; the application build of the queue load, the queue read and the approval route is RWB-P3-E1019-APP and RWB-P4-AD014-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that one approved queue version is in force for allocation across rwb-case, rwb-access and rwb-decision from its valid-from date, and that an overflow queue that does not exist refuses the whole load**, so that **queue configuration is proved to be one contract-wide fact and not a copy that three services can disagree about**.

This story builds the harness and the evidence, and nothing else. rwb-case (P3) owns `queue`, `assignment`, `reference_row` and `reference_version`, and the reference-load and approve operations `POST /api/recovery/case/v1/admin/reference-loads` and `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, with the read `GET /api/recovery/case/v1/queues`. rwb-access (P4) owns the role list `GET /api/recovery/access/v1/admin/roles`, and the Rules and parameters right the approval is checked against. rwb-decision (P7) owns the rule-version approval `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` and the central decision ledger `GET /api/recovery/decision/v1/decision-log`. The screen SCR-42 Queues and service levels is the gateway-bff composite route over those calls (DP-19).

The harness builds nothing in any service. It drives the owners' published operations, observes the effect through their published reads and the shared topic `rwb.decision-record.v1`, and writes one run report. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

Queues carry the team that works a case, the role that may work it, the method by which an officer is chosen, the caseload cap that officer may hold and the overflow queue a case is sent to when the queue is full. Today that structure is a file loaded by the reference-data service and applied to the queue tables the allocation step reads, and a change of team or cap is a data load, not a release: RWB-AD-014 states it in one sentence — queues with their team, role, assignment method, caseload cap and overflow queue are loaded as data, so that allocation follows the team set-up without a code change.

The failure this story is written against is a queue that is in force in one place and not in another. If allocation reads a queue row from one store, the inspector reads the same row from a second and the approval record sits in a third, three separate component tests can all pass while the three disagree: allocation offers a case to a team that is not in force, or holds an officer to a cap the administrator has already changed, or the version on the screen is approved and never applied. Queue configuration therefore has to be proved as one contract-wide fact, on one date, in one run.

The target splits the monolith's one schema along the ownership the architecture gives each service. `queue`, `assignment`, `reference_row` and `reference_version` stay in `rwb_case` (DP-01, DP-07), and the load, the approval recording and the queue read are rwb-case operations on the base `/api/recovery/case/v1` (DP-13). Roles and the permission matrix are `rwb_access` data, and the Rules and parameters right that an approval needs is answered by the rwb-access role list over one hop, cached, with a 2 s budget (DP-05, DP-06, DP-11). The approval itself is the rule-version approval of rwb-decision, which writes the decision record through the local decision-record library and publishes it on `rwb.decision-record.v1` (DP-03), the ledger in rwb-decision collects it and answers it on `GET /api/recovery/decision/v1/decision-log` (ADR-022). Every hop is one REST call with a 2 s budget and never a chain (ADR-020). Where a screen would compose these calls, the path is the gateway-bff composite route (DP-19).

Under DP-06 and DP-07 nothing a business person may change is written in code: the queue code, the team code, the role code, the assignment method, the cap and the overflow code are rows in the file and rows in the version, read back through the rwb-case contract. The values this run uses — queue "LIT-BKK-OFF", team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", caseload cap 40, overflow queue "LIT-BKK-OVF", valid from 2027-06-30, the roles RW-REFADM, RW-RISK, RW-TEAMMGR and RW-OFF, and the messages MSG-P4-002, MSG-P7-003 and MSG-GEN-001 — are copied character for character from the legacy story or from the tables that story points at. The methods FEWEST_CASES and ROUND_ROBIN and the other values of the assignment-method list come from the legacy data, never from code.

RWB-P4-AD014-APP owns the queue-side application behaviour and RWB-P3-E1019-APP owns the reference-load, the queue read and the allocation step this run drives; the legacy AC1 and AC2 belong to those builds and are listed as out of scope here. This story owns no legacy acceptance criterion: the four legacy test cases are carried as `-ITG` copies, and the six criteria of section 7 are the new cross-service proof. Nothing on the target side fixes the exact publication surface of the queue reference load, the exact approval route of a queue load between the rwb-case approve and the rwb-decision rule-version approve, the file layout and cap values, the valid-from parameter or the message ID of an overflow refusal; those are recorded once as GAP-0438 and ASM-0630, and the run reads them from the published contracts and fails the preflight if a field is absent.

Release 30 June 2027 stays tentative and is copied unchanged.

### 3. Preconditions

- RWB-P3-E1019-APP is the integration story that publishes the reference-load, the load approval, the queue read and the allocation step in SIT on `/api/recovery/case/v1`; until it lands, the stubs of section 12.8 stand in from Day 1 and the run is reported as a stub pass.
- RWB-P4-AD014-APP is the application build of the queue load and the queue screen; until it lands, its published contract and stub stand in from Day 1.
- The published contracts of P3 rwb-case, P4 rwb-access and P7 rwb-decision are versioned in the contract registry, and the suite consumes only those contracts; the gateway-bff composite route RWB-PLT-N001-CON is the path a screen would use for SCR-42.
- SIT is in place with the three services, the shared topic `rwb.decision-record.v1` with its retry and `.dlt` topics, the schema registry, the gateway-bff entry and the rwb-access guard answer inside 2 s.
- The synthetic queue, role, team and user set of the harness RWB-ITG-W1J01-ITG is available, with queue "LIT-BKK-OFF" for team "LIT-BKK" and role "RW-LITOFF", method "FEWEST_CASES", caseload cap 40 and overflow queue "LIT-BKK-OVF", and with officers on that queue at the cap and below it; the W1J01 harness may be reused rather than rebuilt.
- The synthetic callers hold RW-REFADM with Reference data C (the loader), RW-RISK with Rules and parameters A (the approver), RW-TEAMMGR with Rules and parameters R (the reader) and RW-OFF without Rules and parameters A (the refused caller of AC3).
- The loader and the approver are different synthetic identities, and no production identity, case, queue or version is used anywhere in the run.
- The clock of the harness can be placed on 2027-06-29 and on 2027-06-30, so that the version in force before the load and the version in force from its valid-from date are both read on the services' own dates.
- The H dependencies the applied patterns add — RWB-PLT-E1027-CON for DP-03, RWB-PLT-E1042-CON for DP-06, RWB-PLT-E1043-CON for DP-07 and RWB-PLT-N001-CON for DP-19 — are platform stories delivered by the platform wave; they sit on the service slices and are not repeated in the metadata H row of this story (Template and Rules section R5.4 and R5.7).
- The file layout of the queue load, the cap values it may carry, the valid-from parameter, the approval route of a queue load between the rwb-case approve and the rwb-decision rule-version approve, the overflow-refusal message ID, and the exact publication and read surface of the rwb-case reference-load and queue reads and of the rwb-decision approval are Not specified in the source documents (GAP-0438; ASM-0630); the run reads what the contracts publish and fails the preflight on an absent field.
- No build dependency, so the story is ready on Day 1 (Template and Rules section R5.7); the release date 30 June 2027 is tentative and is copied unchanged.

### 4. Flow

1. Harness: seeds the synthetic set of RWB-ITG-W1J01-ITG — the queue rows of version 1, the officers of queue "LIT-BKK-OFF", the cases and the four synthetic callers — takes a snapshot of the queue rows, the assignment rows and the case-to-queue values, and places its clock on 2027-06-29. It opens no service schema and no production row.
2. Harness, AC1: submits the queue file with valid from 2027-06-30 through `POST /api/recovery/case/v1/admin/reference-loads` as RW-REFADM with one `Idempotency-Key`, and reads back the load ID, the version ID, the row count and the status VALIDATED.
3. Harness, AC1: reads `GET /api/recovery/case/v1/queues` on 2027-06-29 and asserts that queue version 1 is still the version in force, with the queue rows of the snapshot.
4. Harness, AC4: approves the loaded version through `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` as RW-RISK, and asserts that the answer carries the rule id and the rule version of the approved queue version, that exactly one `rwb.decision-record.DecisionRecorded.v1` is published on `rwb.decision-record.v1`, and that `GET /api/recovery/decision/v1/decision-log` holds one entry for the approval with that rule id and rule version, confirmed by the central ledger.
5. Harness, AC1: records the approval against the load through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, and asserts that the version is read as APPROVED with its author, its approver and its approval time.
6. Harness, AC1: moves its clock to 2027-06-30, reads `GET /api/recovery/case/v1/queues` again, and asserts queue "LIT-BKK-OFF" in force from 2027-06-30 with team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", caseload cap 40, overflow queue "LIT-BKK-OVF" and the table version of the approved load, and that no queue row changed on 2027-06-29.
7. Harness, AC1: reads `GET /api/recovery/access/v1/admin/roles` and asserts that "RW-LITOFF" is a role in force in rwb-access, so the role the queue row points at is answered by its owner and not copied into rwb-case.
8. Harness, AC1: offers the synthetic case at queue "LIT-BKK-OFF" through `POST /api/recovery/case/v1/queues/{queueId}/placements` and asserts that the answer follows the method of the approved version — the officer with the fewest open cases on the queue is chosen and an officer at caseload cap 40 is skipped — and reads the placed case through `GET /api/recovery/case/v1/cases/{caseId}` in queue "LIT-BKK-OFF" with that officer.
9. Harness, AC2: submits a second queue file whose row 4 names overflow queue code "LIT-BKK-OVX", which is not a queue of the file and not a queue in force, and asserts that the whole load is refused with row 4 and code "LIT-BKK-OVX" named, that `GET /api/recovery/case/v1/queues` still answers the version in force, and that no queue row, no assignment row and no case-to-queue value changed against the snapshot.
10. Harness, AC3: has RW-OFF call `POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` on a version loaded as VALIDATED, and asserts status 403 with MSG-P4-002, that the version is not in force, that the rwb-case approve is not called, and that `GET /api/recovery/case/v1/queues` still answers the earlier version.
11. Harness, AC5: forces the decision-record write to fail in the run fixture, has RW-RISK call the rule-version approval again, and asserts MSG-P7-003, that the version stays VALIDATED and is not in force, that `GET /api/recovery/decision/v1/decision-log` gains no entry and no `rwb.decision-record.DecisionRecorded.v1` is published, and that `GET /api/recovery/case/v1/queues` still answers the version in force before the run.
12. Harness, AC6: closes the call set — one hop per call on the owner's base with a 2 s budget, the gateway-bff composite route named for SCR-42, no service schema read and no ACE view read — writes one run report per criterion, removes the synthetic versions and callers, and restores the clock.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A queue row names an overflow queue code that is not in the file and not in force | The whole load is refused and the answer names the row and the overflow code; no queue row, no assignment row and no case-to-queue value changes | None (the message ID of an overflow refusal is Not specified in the source documents (GAP-0438; ASM-0630)) | AC2 |
| X2 | A required field of a queue row is empty, for example the role code or the assignment method | The whole load is refused and the answer names the missing field; nothing is written | MSG-GEN-001 | AC2 |
| X3 | The caller approving the version holds Rules and parameters R and not A | The approval is refused with status 403, the version stays VALIDATED and is not in force, and the queue read still answers the earlier version | MSG-P4-002 | AC3 |
| X4 | The decision record cannot be written at the approval | The approval is not taken, the version stays VALIDATED and is not in force, and no ledger entry and no event exist for it | MSG-P7-003 | AC5 |
| X5 | The queue read is asked on the day before the valid-from date | The earlier version answers, no row changes and no error is produced | None | AC1 |
| X6 | The rwb-access role read does not answer inside 2 s | The load and the approval are refused with 503 and nothing is written; no cached role answer is used past its time-to-live | None | AC3 |
| X7 | The approval is submitted twice for the same version | One decision record and one ledger entry stand for the version, and the second call publishes no second `rwb.decision-record.DecisionRecorded.v1` | None | AC4 |
| X8 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | Every test case, at the preflight |
| X9 | A consumed operation exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy, the report records it, and no assertion is made on data that was not read | None | AC6 |
| X10 | A suite step tries to read a service schema or an ACE view | The step does not exist: the suite is built with no client for a service schema and no view | None | AC6 |

X1 to X7 are the load and approval failure paths of the legacy story read across the services; X8 to X10 are the suite's own failure modes, so that a timeout never becomes a pass and a schema read is impossible rather than discouraged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A module of its own that reuses the harness RWB-ITG-W1J01-ITG; it needs the two integration stories and the published contracts of P3, P4 and P7, not their source code, and it owns no schema and no table |
| Negotiable | The fixture sizes, the poll interval, the clock control and the report layout are configuration; the queue and team codes, the role codes, the method, the cap, the overflow code, the valid-from date and the message IDs are fixed by the legacy story and the tables it points at |
| Valuable | Proves across services what no single service story can prove: the approved version is the one allocation uses on its valid-from date, the role it names is answered by rwb-access, the approval is one record in the central ledger, and a wrong overflow code refuses the whole load without a row changing |
| Estimable | One suite module, one queue-file driver, one queue probe, one role probe, one approval probe, one decision probe, one event observer and one report |
| Small | Fits one sprint with the report; no service code, no schema change and no screen |
| Testable | Every criterion is asserted on an observable: a REST answer, a status, a message ID, a queue row, an assignment, a decision-log entry, an event count or a call set |

### 7. Acceptance criteria

```gherkin
Feature: Configure queues, proven across the rwb-case, rwb-access and rwb-decision contracts

  Background:
    Given the synthetic set holds queue "LIT-BKK-OFF" for team "LIT-BKK" and role "RW-LITOFF", assignment method "FEWEST_CASES", caseload cap 40 and overflow queue "LIT-BKK-OVF"
    Given the loader holds RW-REFADM with Reference data C and the approver holds RW-RISK with Rules and parameters A
    Given rwb-case, rwb-access and rwb-decision are reachable in SIT behind gateway-bff with their published contracts and the stubs of section 12.8
    Given the harness writes no service table, publishes no business event and changes no state
    Given the clock of the harness is on 2027-06-29

  Scenario: AC1 The approved queue version is in force for allocation from its valid-from date (new, D-RCV-60)
    Given the queue file holds queue "LIT-BKK-OFF" with team "LIT-BKK", role "RW-LITOFF", assignment method "FEWEST_CASES", caseload cap 40 and overflow queue "LIT-BKK-OVF", with valid from 2027-06-30
    Given queue version 1 is in force before it
    When the file is loaded through POST /api/recovery/case/v1/admin/reference-loads and approved through POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve, and the approval is recorded through POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve
    Then GET /api/recovery/case/v1/queues on 2027-06-29 answers queue version 1
    Then GET /api/recovery/case/v1/queues on 2027-06-30 answers queue "LIT-BKK-OFF" from the approved version, with team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", caseload cap 40 and overflow queue "LIT-BKK-OVF"
    Then GET /api/recovery/access/v1/admin/roles answers "RW-LITOFF" as a role in force in rwb-access
    Then the case offered at the queue through POST /api/recovery/case/v1/queues/{queueId}/placements is placed against the officer with the fewest open cases and an officer at caseload cap 40 is skipped
    Then GET /api/recovery/case/v1/cases/{caseId} reads the case in queue "LIT-BKK-OFF" with that officer, so the method and the cap the allocation used are those of the approved version and not a value in code

  Scenario: AC2 An overflow queue that does not exist refuses the whole load (new, D-RCV-60)
    Given the queue file has a row 4 that names overflow queue "LIT-BKK-OVX"
    Given no queue of code "LIT-BKK-OVX" exists in the file or in the version in force
    When the file is submitted through POST /api/recovery/case/v1/admin/reference-loads
    Then the whole load is refused and the answer names row 4 and the overflow code "LIT-BKK-OVX"
    Then GET /api/recovery/case/v1/queues answers the version in force before the call, with no queue row added or changed
    Then no assignment row changes and no case changes its queue, read through GET /api/recovery/case/v1/cases/{caseId}
    Then the message ID of the refusal is Not specified in the source documents (GAP-0438; ASM-0630) and the report records the answer it read

  Scenario: AC3 A role without Rules and parameters A cannot approve the version (new, D-RCV-60)
    Given a queue version is loaded and VALIDATED and the version in force before it is version 1
    Given the synthetic caller holds RW-OFF, which holds Rules and parameters R and not A
    When the caller calls POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the answer is status 403 with MSG-P4-002
    Then the version is not in force and no decision record is written for it
    Then POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve is not called
    Then GET /api/recovery/case/v1/queues still answers the earlier version

  Scenario: AC4 The approval writes exactly one decision record with its rule id and rule version (new, D-RCV-60)
    Given a queue version is loaded and VALIDATED and the approver holds Rules and parameters A
    When the approver calls POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve once
    Then the answer carries the rule id and the rule version of the approved queue version
    Then exactly one "rwb.decision-record.DecisionRecorded.v1" is published on "rwb.decision-record.v1" for that approval
    Then GET /api/recovery/decision/v1/decision-log holds exactly one entry for the approval with that rule id and rule version, and the central ledger in rwb-decision confirms it
    Then GET /api/recovery/case/v1/queues reads the version as APPROVED and, from 2027-06-30, as the version in force

  Scenario: AC5 A forced decision-record failure stops the approval (new, D-RCV-60)
    Given the decision record for the queue version cannot be written, forced in the run fixture
    Given the version in force before the run is version 1
    When the approver calls POST /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve
    Then the answer carries MSG-P7-003
    Then the version stays VALIDATED and is not in force
    Then GET /api/recovery/decision/v1/decision-log gains no entry for the approval and no "rwb.decision-record.DecisionRecorded.v1" is published for it
    Then POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve is not called and GET /api/recovery/case/v1/queues still answers version 1

  Scenario: AC6 Every call is one hop on the owner's base and nothing is read from a table (new, D-RCV-60)
    Given the call set of the run is recorded with its base, its contract version and the service that answered
    When the run of AC1 to AC5 has finished
    Then every call is one hop on /api/recovery/case/v1, /api/recovery/access/v1 or /api/recovery/decision/v1 with a 2 s budget, and no call is chained through a second service
    Then the route a screen would take for SCR-42 Queues and service levels is the gateway-bff composite route RWB-PLT-N001-CON
    Then the call set shows no read of a service schema and no read of an ACE view, and the report names the owner of every value it asserts
```

**Target reading.** Against the monolith, the queue file is a rwb-case reference load on `/api/recovery/case/v1` (DP-07, DP-13), the role it names and the right the approval needs are answered by rwb-access over its role list and its guard (DP-05, DP-06), the approval is the rwb-decision rule-version approval that writes one decision record and publishes it on `rwb.decision-record.v1` (DP-03, ADR-022), and every screen path enters through the gateway-bff composite route (DP-19). No service reads another service's table (DP-01): the queue version and the allocation are asserted through the rwb-case reads, the role through the rwb-access role list, the approval and its record through the rwb-decision reads and the shared topic. The queue fields and the messages are the legacy values; the file layout, the cap values, the valid-from parameter, the approval route and the overflow-refusal message ID are Not specified in the source documents (GAP-0438; ASM-0630).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A queue carries its team, its role, its assignment method, its caseload cap and its overflow queue, and is loaded as data, so allocation follows the team set-up without a code change | RWB-AD-014 story line, `queue` fields DF-WRK-001 to DF-WRK-008 |
| BR2 | The loaded version takes effect on its valid-from date after approval, and the version in force answers until that date | RWB-AD-014 AC1 "from the valid from date"; DP-07 |
| BR3 | A queue row that names an overflow queue which does not exist refuses the whole load | RWB-AD-014 AC2 |
| BR4 | A load is taken whole or not at all: one refused row writes no queue row, no assignment row and no case-to-queue value | RWB-AD-014 AC2; DP-07 reference-load pattern |
| BR5 | The approval is recorded once, with the rule id and the rule version of the approved version, and the central ledger in rwb-decision confirms that record | DP-03; Arch v5 slide 20 (DecisionRecorded to `rwb.decision-record.v1`, ledger in rwb-decision); slide 42 row 08; ADR-022 |
| BR6 | When the decision record cannot be written the approval is not taken and the answer is MSG-P7-003 | RWB-AD-014 messages; ADR-022; Temporal design slide 13 (RecordAndApply, one transaction) |
| BR7 | The queue, the assignment and the version store are rwb-case data, the roles and the permission matrix are rwb-access data, the approval record is rwb-decision's, and no service reads another's table or an ACE view | DP-01, DP-05; Arch v5 slide 41; ownership map rows `queue`, `assignment`, `role`, `reference_row`, `reference_version`, `decision_log_entry`, `parameter_catalog` |
| BR8 | Every hop is one REST call on the owner's base `/api/recovery/<short>/v1` with a 2 s budget, never an in-process call and never a second hop; a screen path is the gateway-bff composite route | DP-11, DP-13, DP-19; ADR-020; Arch v5 slide 11 |
| BR9 | A caller without Rules and parameters A cannot approve the version, and the version stays out of force | RWB-AD-014 permission checks (Rules and parameters A: RW-RISK); MSG-P4-002 |
| BR10 | The queue fields, the methods and the cap are read as data through the rwb-case contract, and the decision record is published once through the owner's outbox with inbox dedupe in the consumer, so a replay never produces a second record | DP-06, DP-07; ADR-015; Arch v5 slide 42 notes; Temporal design slide 16 (rule id and version on every answer) |

The harness asserts these rules and changes none of them. The queue version and the allocation are rwb-case's, the role answer and the right are rwb-access's, the approval and the record are rwb-decision's; the run only drives the published operations of those three and reads the effect.

### 9. State transitions

| From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|
| None | Queue file loaded | every row passes the load checks, including that every overflow code exists | VALIDATED | P3 rwb-case, `POST /api/recovery/case/v1/admin/reference-loads` |
| None | Queue file loaded | a row fails a check (overflow code not in the file and not in force, required field empty) | REFUSED, nothing written | P3 rwb-case |
| VALIDATED | Approval decision recorded | the caller holds Rules and parameters A and one decision record is written and published | APPROVED, with the rule id, the rule version, the approver and the approval time | P7 rwb-decision writes the decision and its record; P3 rwb-case records the approval through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` |
| VALIDATED | Approval decision refused | the caller does not hold Rules and parameters A | VALIDATED, not in force, 403 MSG-P4-002 | P4 rwb-access answers the right; P7 refuses |
| VALIDATED | Approval decision refused | the decision record cannot be written | VALIDATED, not in force, MSG-P7-003, no entry and no event | P7 rwb-decision |
| APPROVED | Valid-from date reached | the version is approved and the valid-from date is today | IN_FORCE, and the version in force before it is superseded | P3 rwb-case |

The version states are those of the reference-data contract of rwb-case (VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, REFUSED); the refusal is a state of the load and not of a version in force. The approval record is P7's and the version is P3's, so the run reads the same transition from two owners and asserts that they agree on the date. The harness changes no state: every change in the table is made by the owner through the operation named beside it, and the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM | Loads the queue file (Reference data C) and is the loader of the run |
| RW-RISK | Approves the queue version (Rules and parameters A), which is the approval the run drives |
| RW-TEAMMGR | Reads the queue rows and the decision log (Rules and parameters R); takes no part in the load or the approval |
| RW-OFF | The refused caller of AC3: holds Rules and parameters R and not A, and is refused at the approval |
| QA lead | Owns the harness configuration, the synthetic set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P3 performs the load, records the approval and answers the queue read and the allocation; P4 answers the role list and the right; P7 takes the approval, writes the decision record and answers the ledger; they make every change the harness asserts |
| No role | Reads a service schema or an ACE view directly, or takes production data into the run |
| No delegation of authority level applies | Queue structure is configuration and not a credit decision, so no DoA level is consulted |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-WRK-001 to DF-WRK-008 | queue (rwb_case) | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | Loaded through the rwb-case reference-load operation; read through the rwb-case queue read |
| DF-WRK-009 to DF-WRK-016 | assignment (rwb_case) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Written by the allocation of rwb-case; read through the rwb-case case read |
| DF-REF-034 to DF-REF-038 | role (rwb_access) | id, role_code, role_name, role_class, default_scope | Read through the rwb-access role list; never copied into a queue row |
| Not specified in the source documents (GAP-0438; ASM-0630) | reference_version (rwb_case) | the version of the queue file, its table, its valid from, its author, its approver and its state | Read through the rwb-case queue read and the load answer |
| Not specified in the source documents (GAP-0438; ASM-0630) | reference_row (rwb_case) | the approved row of the queue file | Read through the rwb-case queue read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (rwb_decision) | the record of the approval, with its rule id and rule version | Read through the rwb-decision decision log; written by rwb-decision |
| DF-DOC-001 to DF-DOC-011 | document (rwb_document) | the fields the legacy story's data table lists for the document entity | P5's data and not touched by this story |

Field IDs are those of the legacy story and are copied unchanged. The legacy story wrote these tables in one schema; in the target `queue`, `assignment`, `reference_row` and `reference_version` are in `rwb_case` (P3, DP-01, DP-07), `role` is in `rwb_access` (P4, DP-01), and `decision_log_entry` is in `rwb_decision` (P7, DP-03). The `document` entity appears in the legacy data table for a different purpose and is P5's; nothing in this run reads, writes or counts a document. The suite owns no field and no table: every queue, assignment, role, user and version in the run is synthetic, and the queue fields the run asserts — "LIT-BKK-OFF", "LIT-BKK", "RW-LITOFF", "FEWEST_CASES", caseload cap 40, "LIT-BKK-OVF" — are the legacy values held in the fixture as data.

### 12. Contract

#### 12.1 REST operations provided

None. The suite is a test runner and provides no REST operation. It publishes no operation, builds no route and owns no endpoint in any service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | AC1, AC2: submit the queue file with its valid-from date as a version, with one `Idempotency-Key`, and read the load ID, the version ID and the status | 2 s |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | AC1, AC4: record the approval against the load so the version is APPROVED in rwb-case | 2 s |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | AC1, AC2, AC3, AC5: the queue rows in force with team code, role code, method, cap, overflow queue, valid from and table version | 2 s |
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | P3 rwb-case | AC1: offer the synthetic case at the queue and read the allocation the approved version produces | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1, AC2: the queue and the officer of the case, and the proof that no case moved on a refused load | 2 s |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | AC1: the role the queue row points at, as a role in force | 2 s |
| POST | `/api/recovery/decision/v1/admin/rule-versions/{versionId}/approve` | P7 rwb-decision | AC1, AC3, AC4, AC5: the approval of the queue version, the right that guards it and the one decision record it writes | 2 s |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | AC4, AC5: the one entry of the approval with its rule id and rule version, and the ledger confirmation | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget. No operation is invented: each path is the owner's published operation in the ownership map, and where a screen would compose them the path would be the gateway-bff composite route for SCR-42 (DP-19). The division of the approval between the rwb-case load approve and the rwb-decision rule-version approve is not fixed by any source read: the run takes the approval decision and its record in rwb-decision and records the approval against the load in rwb-case, and the split is Not specified in the source documents (GAP-0438; ASM-0630).

#### 12.3 Events published

None. The suite publishes no business event. The one publication the run counts is the owner's: rwb-decision publishes `rwb.decision-record.DecisionRecorded.v1` through its own outbox when the approval is recorded (DP-03).

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision, through the local decision-record library (DP-03; Arch v5 slide 42 row 08, "all 19" producers, ledger in rwb-decision) | Counts exactly one publication for the approval, proves none on the forced failure, and pairs each count with the ledger entry read through the decision log (AC4, AC5) |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case (Arch v5 slide 42 row 02) | Counts one publication when the synthetic case is placed under the approved version, so the allocation effect is read on the owner's own announcement and on the case read (AC1) |

The suite subscribes to the two topics under one consumer group of its own, counts publications and replays each event once; a replay leaves the queue version, the assignment and the ledger unchanged, because the consumer inbox holds one processed row. No other event is asserted: the rwb-case queue read is synchronously the owner's, and no service announces a queue version.

#### 12.5 Workflows and activities

None added. The run observes CaseWorkflow (rwb-case, allocate step): the parent workflow of a case on task queue `rwb-case` in the namespace `rwb-recovery`, which runs the allocation step that reads the queue row in force and places the case (Arch v5 slide 14, "Act: allocate, transfer, rebalance"; slide 23; Temporal design slide 13). The step is the owner's and the harness only reads its outcome through the case read and the queue read. No workflow, activity, Schedule or task queue is created, changed or owned by this story, and the harness starts no workflow of its own.

#### 12.6 Schedules

None. No Schedule takes part in a reference load or in an approval: the load and the approval are synchronous calls and the version applies on its valid-from date from the version store. The harness moves only its own clock, to place the run on 2027-06-29 and 2027-06-30, and it neither waits on nor reads JOB-03 or JOB-20.

#### 12.7 Tables owned

None. The suite owns no schema and no table and never reads another service's schema (DP-01). The tables it exercises are listed in section 11 with their owners: `queue`, `assignment`, `reference_row` and `reference_version` in `rwb_case` (P3), `role` in `rwb_access` (P4) and `decision_log_entry` in `rwb_decision` (P7).

#### 12.8 Contract fakes

| Stub | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-case | `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve`, `GET /queues`, `POST /queues/{queueId}/placements`, `GET /cases/{caseId}` | Accepts the queue file once per `Idempotency-Key` and answers the load ID and the version VALIDATED; refuses the file whose row 4 names "LIT-BKK-OVX" and names row 4 and the code; answers the queue rows of version 1 before 2027-06-30 and of the approved version from 2027-06-30 with team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", cap 40 and overflow queue "LIT-BKK-OVF"; the placement answers the officer with the fewest open cases and skips an officer at cap 40; the case read answers queue "LIT-BKK-OFF" with that officer |
| Stub for rwb-access | `GET /admin/roles` | Answers "RW-LITOFF", "RW-REFADM", "RW-RISK", "RW-TEAMMGR" and "RW-OFF" as roles in force, with the Rules and parameters rights of section 10, and answers no A right for RW-OFF |
| Stub for rwb-decision | `POST /admin/rule-versions/{versionId}/approve`, `GET /decision-log` | Accepts one approval from RW-RISK and answers the rule id and the rule version with one decision record; refuses RW-OFF with 403 MSG-P4-002; forces MSG-P7-003 and writes no entry when the fixture asks for the failure; answers one decision-log entry per accepted approval with its rule id, its rule version and the ledger confirmation |
| Stub for the gateway-bff route | The composite route RWB-PLT-N001-CON for SCR-42 | Answers the composed queue, role and decision answers of one screen load, so the run proves the path a screen would take without building the screen |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The overflow-refusal message ID is not in any stub's contract either; the run asserts the row and the code and records the answer it read, and the missing ID is Not specified in the source documents (GAP-0438; ASM-0630).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.decision-record.DecisionRecorded.v1` and `rwb.case.CaseAllocated.v1`, counted and replayed once |
| Temporal | None added; CaseWorkflow (rwb-case, allocate step) observed through the case read and the queue read |
| File | One synthetic queue file, submitted as the payload of the rwb-case reference load; no claim-check store, no batch and no manifest |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies these patterns add — RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON — and the C dependencies they carry — RWB-P3-E1042-CON and RWB-P3-E1043-CON — sit on the service slices that own the code, not on this harness: they are platform and contract stories delivered elsewhere, and they are not repeated in the metadata H and C rows of this story, which stay None. DP-05 adds nothing: the run reads no ACE data and no view, and any ACE data behind the three services is read through the rwb-source-data contract by those services. The two integration dependencies RWB-P3-E1019-APP and RWB-P4-AD014-APP replace their stubs as they land, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| QueueLoadDriver | Job | Builds the synthetic queue file, submits it with valid from 2027-06-30 and one `Idempotency-Key`, records the load ID and the version, and submits the refused file of AC2 |
| QueueReadProbe | Job | Reads the queue rows in force on both dates, keeps the queue ID, the table version and the valid from of each row, and compares reads across the two dates |
| RoleProbe | Job | Reads the role list in force from rwb-access and asserts the role code each queue row points at |
| ApprovalProbe | Job | Drives the rule-version approval and the rwb-case approval recording, and asserts the right that guards them |
| DecisionProbe | Job | Reads the decision log, asserts one entry per approval with its rule id and rule version, and forces the write failure of AC5 |
| EventObserver | Job | Subscribes to `rwb.decision-record.v1` and `rwb.case.events.v1`, counts publications and replays each event once |
| StubSet | Fake | The four stubs of section 12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Job | Writes one run report per criterion with the queue rows, the roles, the approval, the record, the event counts, the call set and the verdicts |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-P3-E1019-APP and RWB-P4-AD014-APP land, on the synthetic set of RWB-ITG-W1J01-ITG: queue "LIT-BKK-OFF", team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", caseload cap 40, overflow queue "LIT-BKK-OVF", the missing overflow code "LIT-BKK-OVX", valid from 2027-06-30, the clock dates 2027-06-29 and 2027-06-30, and the four synthetic callers. The harness seeds nothing by hand and never writes a schema row. The file layout, the cap values, the valid-from parameter, the approval route and the pass or fail gate are Not specified in the source documents (GAP-0438; ASM-0630).

**Build steps**

1. Generate the four stubs and the synthetic set from the published contracts, pin each contract version in the run report, and fail the run on a mismatch (X8).
2. Build the QueueLoadDriver and the queue file fixture, submit the file with valid from 2027-06-30, and assert the load ID, the version and the status VALIDATED.
3. Add AC1 on the two dates: the queue read on 2027-06-29 answers version 1 and the same read on 2027-06-30 answers the approved version with team, role, method, cap and overflow queue.
4. Add the ApprovalProbe and the DecisionProbe for AC4: one approval, one decision record with its rule id and rule version, one `rwb.decision-record.DecisionRecorded.v1`, one ledger entry confirmed.
5. Add the RoleProbe and the allocation step of AC1: "RW-LITOFF" in force in rwb-access, the placement follows FEWEST_CASES, an officer at cap 40 is skipped, and the case read confirms the queue and the officer.
6. Add AC2: the file whose row 4 names "LIT-BKK-OVX" is refused with row and code named, and no queue row, assignment row or case-to-queue value changes against the snapshot.
7. Add AC3: RW-OFF is refused at the approval with 403 MSG-P4-002, the version stays VALIDATED, the rwb-case approval is not called and the earlier version still answers.
8. Add AC5: the forced decision-record failure answers MSG-P7-003, leaves the version out of force, adds no entry and publishes no event.
9. Add the EventObserver replay and the AC6 call-set assertions, swap each stub for the real owner as its integration story lands, and run the whole suite twice to prove that a repeated run adds no version and no row.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The four test cases of section 16 pass against the stubs and again against RWB-P3-E1019-APP and RWB-P4-AD014-APP as they land, the six criteria of section 7 are signed off with an observable each, the approved version is proved to be the one allocation uses on its valid-from date, the role it names is answered by rwb-access, the approval is proved to be one record confirmed in the central ledger, the refused load is proved to write nothing, no service table and no ACE view was read, the synthetic set is removed and the evidence report names every criterion with its evidence.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Error | Enter {field}. |

The three texts are copied unchanged from RWB-AD-014 and this story adds no message ID. MSG-P4-002 is asserted with {action} naming the approval when RW-OFF calls the rule-version approval (AC3). MSG-P7-003 is asserted when the decision record cannot be written and the version stays out of force (AC5). MSG-GEN-001 is asserted with the missing field named when a queue row is submitted with a required field empty (X2). The refusal of a queue that names an overflow queue which does not exist carries no message ID in the legacy story, and none is invented here: the run asserts the refused load, the row and the overflow code, and records the answer it read — the message ID is Not specified in the source documents (GAP-0438; ASM-0630).

### 15. Screens and states

SCR-42 Queues and service levels (states Versions; load) is not built, rendered or tested here. It is the wave 4 administration screen, it reaches rwb-case, rwb-access and rwb-decision through the gateway-bff composite route (DP-19), and the stub of that route in section 12.8 only proves the composed path a screen would take. What the wave entry check looks at instead is the run report.

| State | Read through | What the run asserts |
|---|---|---|
| VALIDATED | rwb-case load answer and queue read | The file is accepted whole, with its valid-from date, its author and its row count, and no queue row is in force from it yet |
| APPROVED | rwb-case queue read, rwb-decision decision log | The approval is recorded with the rule id, the rule version, the approver and the approval time, and one ledger entry confirms it |
| IN_FORCE | rwb-case queue read on 2027-06-30 | The approved version answers with team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", cap 40 and overflow queue "LIT-BKK-OVF", and the allocation uses that method and that cap |
| REFUSED | rwb-case load answer and queue read | A queue naming "LIT-BKK-OVX" refuses the whole load, the row and the code are named, and the version in force is unchanged |
| A refused approval | P4 role list and the P7 answer | 403 with MSG-P4-002, the version out of force, the rwb-case approval not called |
| A failed decision record | P7 answer, decision log and the topic | MSG-P7-003, the version out of force, no entry and no event |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-014-01-ITG | AC1 | End to end | Queue file with queue "LIT-BKK-OFF", team "LIT-BKK", role "RW-LITOFF", method "FEWEST_CASES", cap 40, overflow queue "LIT-BKK-OVF", valid from 2027-06-30; queue version 1 in force; the clock on 2027-06-29 and 2027-06-30; the synthetic case placed on the queue |
| TC-AD-014-02-ITG | AC2 | Integration | Queue file whose row 4 names overflow queue "LIT-BKK-OVX", which is not in the file and not in force; the snapshot of the queue rows, the assignment rows and the case-to-queue values |
| TC-AD-014-03-ITG | AC3 | Component | A caller holding RW-OFF with Rules and parameters R and not A, calling the rule-version approval on a version loaded as VALIDATED |
| TC-AD-014-04-ITG | AC4, AC5 | Integration | One approval by RW-RISK on a VALIDATED version, the decision-log read with its rule id and rule version and the ledger confirmation, then the forced decision-record failure on the same approval |

The legacy test cases TC-AD-014-01, TC-AD-014-02, TC-AD-014-03 and TC-AD-014-04 are carried here as the `-ITG` copies above, and the legacy Covers values are kept: AC1 to TC-AD-014-01-ITG, AC2 to TC-AD-014-02-ITG, Access to TC-AD-014-03-ITG and Principle 5 to TC-AD-014-04-ITG. The legacy AC1 and AC2 stay the build criteria of RWB-P4-AD014-APP; the copies here assert the same behaviour across the service boundary, on the real contracts, with the cross-service reads the component copy cannot make. AC6 has no test case of its own: it is asserted on every case above at the preflight, through the call set, the budget and the absence of any schema or view read.

### 17. Guardrails

- No business value in code: the queue code, the team code, the role codes, the method, the cap, the overflow codes, the valid-from date and the report layout are data held in the fixture or read through a contract, never constants in the suite.
- No personal data in events, logs, fixtures or the report: every caller, case and queue is synthetic, the run carries codes, dates, counts and statuses, and no person, account or customer value enters the run record.
- ACE data only through the owner's contract: nothing ACE is read here, and any ACE data behind the three services is read by them through the rwb-source-data contract (DP-01, DP-05); the suite ships with no client for a service schema and no client for a view.
- One hop and a 2 s budget on every call, with a breaker per downstream, so the harness fails where a screen would (DP-11, DP-13, ADR-020).
- No invented operation and no invented message: only the eight operations of section 12.2 and the three messages of section 14, and the overflow refusal is asserted by row and code because its message ID is not in any source read.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner, and the stub set is swapped as the two integration stories land.
- SIT only: the harness refuses to start against any other environment, and it removes the synthetic versions and restores the clock at the end.
- No schema read, no direct row write and no state set by hand: every value the run asserts was produced by an owner's operation, and a state the harness had set itself would prove nothing.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-014 Configure queues | `04 User stories/Recovery Workbench Administration Stories v3.md`, lines 1138 to 1218 | Sections 1, 2, 3, 11, 14 and 19 of this file |
| Legacy AC1 "Queue loaded" and AC2 "Overflow must exist" | The same, lines 1157 to 1166 | Section 7, AC1 and AC2 in the cross-service form; the legacy criteria themselves stay with RWB-P4-AD014-APP (section 19) |
| Legacy test cases TC-AD-014-01 to TC-AD-014-04 and their Covers values | The same, lines 1207 to 1214 | Section 16, carried as `-ITG` copies with the legacy Covers kept |
| Legacy data table: queue, assignment, document, role | The same, lines 1168 to 1175 | Section 11; the document entity is P5's and is not touched |
| Legacy endpoints, permission checks, screen SCR-42 and messages | The same, lines 1177 to 1205 | Sections 12.2, 10, 15 and 14 |
| Arch v5 slides 14, 20, 41 and 42 | `Recovery Workbench Architecture v5 Text Extract v1.md`: P3, P4 and P7 contracts at lines 1033 to 1043; every service writing its own decision record at line 1478; the 19-service catalogue at lines 2878 to 2903; event catalogue rows 02 and 08 at lines 2914 and 2920 | Sections 2, 8, 12.2, 12.4 and 13 |
| Arch v5 slide 44, the job map, and slide 11, the call types | The same, lines 2970 to 3002 and 782 to 850 | Sections 12.5, 12.6 and 8 |
| Temporal and Drools design: the four steps, RecordAndApply in one transaction, the allocation rule and version label | `Recovery Workbench Temporal and Drools Design Text Extract v1.md`, slides 11, 13, 15 and 16 (lines 440 to 519, 611 to 675, 800 to 888) | Sections 2, 8 and 12.5 |
| DP-03, DP-05, DP-06, DP-07, DP-13, DP-19 | Template and Rules v1 section R5.5 | Section 13, pattern application |
| Ownership map rows `queue`, `assignment`, `role`, `parameter_catalog`, `reference_row`, `reference_version`, `decision_log_entry` | `_work/msr/plan/ownership.json` | Sections 1, 3 and 11 |
| Ownership map API rows `GET /queues`, `GET /admin/roles`, `POST /admin/rule-versions/{versionId}/approve`, `GET /decision-log`, `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve`, `POST /queues/{queueId}/placements`, `GET /cases/{caseId}` | The same | Section 12.2 |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records, with the three as added by Template and Rules v1 section R8.4 | Sections 8, 12.4 and 17: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| Gap GAP-0438 and assumption ASM-0630 | This run, D-RCV-60 | Sections 2, 3, 5, 7, 11, 12.2, 12.8, 13 and 14: the file layout and cap values, the valid-from parameter, the approval route of a queue load, the overflow-refusal message ID, and the publication and read surface of the P3 reference-load and queue reads and the P7 approval |
| Release date 30 June 2027 | Legacy story header, "E8, release 30 June 2027" | Metadata table; tentative and copied unchanged (Template and Rules section R1 U7, and sections R5.7 and R8.4) |

### 19. Out of scope

- RWB-P3-E1019-APP: the build of the reference load, the load approval, the queue read and the allocation step in rwb-case, which publishes the operations this run drives.
- RWB-P4-AD014-CON and RWB-P4-AD014-APP: the build of the queue configuration itself, including the legacy AC1 and AC2, which belong to those stories and not to this one.
- The platform H dependencies named in section 13, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON, and the contract dependencies RWB-P3-E1042-CON and RWB-P3-E1043-CON.
- SCR-42 Queues and service levels and every gateway-bff composite route: the screen is not built, rendered or tested, and only the composed path is stubbed.
- The allocation engine itself, its queue-ordering rules and the rebalancing of a queue: the run observes the allocation the approved version produces and changes nothing.
- The overflow behaviour once every officer of a queue is at the cap: the run asserts the overflow queue on the queue row and the refusal of a file that names one which does not exist, and asserts no routing to the overflow queue.
- The role list, the permission matrix and the Rules and parameters rights themselves, which are rwb-access data and the RWB-AD-* and RWB-E1-* content of that service.
- The rule-version family as a whole, its authoring, its 50-scenario gate, its effective dating and its rollback, which are the RWB-ITG-E1073-ITG and RWB-E1-073 content; only the approval of a queue version is driven here.
- Sibling legacy keys in the same wave, RWB-AD-015, RWB-AD-018, RWB-AD-019 and RWB-AD-022, and the non-functional epic RWB-ITG-NFR.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service.
