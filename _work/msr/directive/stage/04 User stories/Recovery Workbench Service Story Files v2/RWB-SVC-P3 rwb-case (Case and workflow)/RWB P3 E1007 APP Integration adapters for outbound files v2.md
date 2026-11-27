# RWB-P3-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-case, as the secondary slice of the legacy key. The legacy story held one adapter pattern, one SFTP transport, one retry ladder, one exception queue and four scheduled jobs of one module in one process under one `recovery_svc` identity, and it moved the case route state and raised the owner task through the in-process interfaces `CaseEvents.raise` and `TaskApi.raiseTask`. This slice takes only the case side of that key: the two consumed delivery outcomes, the route-state move of each case on the file, the one owner task at the retry limit, one decision-record entry per outcome, and the item status read one hop from rwb-integration. No SFTP class, no item table, no retry ladder, no outbound file, no Schedule, no workflow, no table of its own and no ACE view. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 36 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E1007-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P3-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E1007-CON; rwb-source-data contract; rwb-document contract. The operations, elements and payloads of the rwb-source-data and rwb-document contracts are Not specified in the source documents (GAP-1162, GAP-1164) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P3-E1007-APP-22) |
| Contract version | /v1 path segment (section 4 step 3); the contract version is Not specified in the source documents (DOR-RWB-P3-E1007-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-DRI-006, REQ-DRI-007, REQ-DRI-008) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **every case on a failed outbound file moved to route state RETRY_QUEUE after the first failed attempt and to EXCEPTION_QUEUE with one open task for my role when the retry limit is reached, and the case put back to the route state it held when the same file is delivered later**, so that **a failed outbound file is seen on the case on the day it fails, the owner is named on a task, and every move is on the append-only record**.

Inside `rwb-case` this is the case-side slice of the legacy key RWB-E1-007:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- Two deliverables, and nothing else: the listener that consumes `rwb.integration.FileFailed.v1` and `rwb.integration.FileDelivered.v1` with inbox dedupe and moves `recovery_case.route_state` and raises the owner task in one transaction; and the one-hop read of the outbound item through the rwb-integration admin operation, so the retry state and the exception state are decided on the item's own status and not on a value copied into a payload.
- The case status (`recovery_case.status`) does not change and no case event is published: a case in the retry or the exception route state keeps its status, as the allocation slice of this service already fixes for the overflow and the exception queue. The decision record carries the move.
- The build, the file, the transport, the PGP key, the retry ladder on `retry_intervals_min`, the exception queue, the resend and the `MSG-P2-001` message are **not** this story's: they are RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF and RWB-P2-E1007-OPS. The notice that requests the WIN file is RWB-P6-E1007-APP's, the buyer tape is RWB-S6-E1007-APP's, the stored bytes are rwb-document's, and the end-to-end proof of the key is RWB-ITG-E1007-ITG's.
- `interface_config`, `outbound_item` and `outbox_delivery` are P2's tables and are reached only through `GET /api/recovery/integration/v1/admin/outbound-items`, never from `rwb_integration`; `rwb_case` holds no grant outside its own schema (DP-01, DP-02).

**What rwb-case produces and hands over for an outbound item.** After DP-17 this service produces no outbound file of its own. The two legacy outbound extracts that carried its facts fed the data lake and are dropped: JOB-15 Reporting extract (INT-19, the case, queue, task and timer records of the day) and JOB-13 Decision log copy (INT-20). Neither had a consumer that was not the lake, and reporting is now read from `rwb.case.events.v1` into rwb-reporting (DP-17; GAP-0739; ASM-1341). What this service therefore produces for an outbound item is the case consequence of its delivery — the route state of each case, the owner task and the decision record — and it hands that consequence to the case owner through the case contract, not to a file.

Two source silences are load-bearing and are carried as one combined gap row and seven assumptions rather than as invented values. The element names of the two delivery events beyond the contract, the values of the task code and the task due date, and the carrier of the route state to resume are named nowhere for the target: every such value reads "Not specified in the source documents (GAP-0739; ASM-1336)" or its own numbered assumption. The legacy `CaseEvents.raise` and `TaskApi.raiseTask` interfaces and the legacy `/api/recovery/v1` case-action path have no operation in the target case contract, so the move is an internal service of the listener and no path is added (GAP-0739; ASM-1339).

### 2. Business rationale

The Workbench loads no source data and sends its files through one path (D-RCV-35 U1; legacy REQ-DRI-006). In the target that path is rwb-integration's: the builder, the MFT/SFTP transport, the retry intervals of the interface row, the exception queue and the two outcomes `FileDelivered` and `FileFailed` on `rwb.integration.events.v1` (DP-16, DP-17). What the legacy story also did — and what no other service can do — was to make a failure land on the case: the cases of the file left the active route, an owner task appeared for the platform administrator, and the record showed the move. That part belongs to rwb-case, because `recovery_case.route_state` and `task` are its rows and the decision record is the local entry the service writes through DP-03.

Read together, those rulings fix the seam. The **movement** of a file is rwb-integration's; the **effect** of a delivery outcome is rwb-case's. This story is that effect and is deliberately small: read the outcome, read the item's own status one hop, move each case once, raise one task for the case set at the retry limit, put the case back when the file is delivered later, and write the entry first. It meets REQ-DRI-007 (every outbound file is logged, retried on a defined schedule and raised to a named owner) and REQ-DRI-008 (no file is loaded, read or copied in the Workbench) for the case side, and it adds no second copy of the outbound pattern.

The behaviour the business relies on is unchanged from the legacy state table: `RETRY_QUEUE` after a first failed attempt, `EXCEPTION_QUEUE` and a task for the owner role when the retry limit is reached, a return to the state the case held when the file is delivered, and no case status change. The legacy measure is unchanged too — "outbound items in the exception queue over one day: zero" (FSD P2 A2.1) — and this slice is the half of that measure the case owner can act on, because the case is where the work resumes.

What changes is the owner of each step and the removal of the in-process interface: the route state is data on the case row, the task is a row of `task`, the reference values are rows in force, and the record names the interface, the business date and the attempt count. A reader cannot be told a different delivery state by a service that copied the item, because the item is never copied.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E1007-CON is published | The AsyncAPI document of `rwb.integration.events.v1` with `FileDelivered` and `FileFailed`, their payload elements, the admin outbound-item operations on `/api/recovery/integration/v1`, the one error envelope and the contract fakes (DP-16). This story consumes and publishes none of them |
| RWB-PLT-TE006-CON is published | The outbox and inbox library with `processed_event`, the CloudEvents 1.0 envelope, the retry topics and the `.dlt` topic (DP-09) |
| RWB-PLT-E1027-CON is published | The local decision-record library and the shared topic `rwb.decision-record.v1`, append-only and hash-chained (DP-03) |
| RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published | The reference-data contract that serves the route-state codes and the task reference rows at the version in force (DP-07). The values themselves are Not specified in the source documents (GAP-0739; ASM-1338) and no code is written for them |
| RWB-PLT-E1071-CON is published | The workflow kit and the task queue `rwb-case` in namespace `rwb-recovery` on which the listener runs (DP-10). This story registers no workflow and no `Schedule` |
| RWB-PLT-N001-CON is published | The gateway-bff composite route that serves the exception queue and the case screens (DP-19). This story builds no screen |
| RWB-P3-E1018-APP delivered the `rwb_case` baseline | `recovery_case`, `case_account`, `case_party`, `task`, `assignment` and `timer`, their dictionary rows and the case contract. This story adds no table, no column and no path |
| RWB-P3-E1021-APP delivered the route-state and transfer behaviour | The route-state codes in force and the resume-path convention already exist; this story moves the state for a file outcome and changes neither the rule set nor the transfer engine |
| RWB-P3-E1042-CON and RWB-P3-E1043-CON serve the rows this story reads | The task code, the task due date rule and the route-state codes, each at the version in force (DP-06 rows are the baseline's, not this story's) |
| The platform contracts the DP rows name are held elsewhere | RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON are pulled by the `rwb_case` baseline stories and the platform epics, so this slice adds no build dependency and starts on Day 1 (GAP-0739; ASM-1340) |
| The connection is the rwb-case login (DP-02) | It holds grants on `rwb_case` only. The login name is Not specified in the source documents (GAP-0739; ASM-1338) |
| The case workflow of RWB-P3-E2043-APP is live or stubbed for the tests | This story registers no workflow, signals none and does not extend it (GAP-0739; ASM-1339) |
| Every fixture is synthetic | No production case, file, address, identity number or row is used in a test |

### 4. Flow

1. rwb-integration builds and sends the file, retries on the intervals of its interface row and publishes `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1` after a failed attempt and again when the last allowed attempt has failed; it publishes `rwb.integration.FileDelivered.v1` when the file is sent (BR1, DP-16).
2. The rwb-case worker consumes the event: the CloudEvents envelope is validated, the inbox is checked in `processed_event` by consumer and CloudEvents id, and a duplicate is counted and dropped (BR2, BR9, AC4).
3. `ItemStatusReader` reads the item of the event's interface and business date with `GET /api/recovery/integration/v1/admin/outbound-items?interfaceId=&businessDate=` — one hop, 2 s budget, one GET retry with jitter, a breaker per downstream, and no row read of `rwb_integration` (BR3, DP-11, AC6).
4. `RouteStateResolver` maps the item status to the target route state from the reference rows in force: status RETRY answers `RETRY_QUEUE`, status EXCEPTION answers `EXCEPTION_QUEUE`, and a delivered outcome answers the state to resume (BR4, DP-07, AC1, AC3).
5. For each case of the file, `CaseRouteStateWriter` writes `recovery_case.route_state`, and the same transaction writes one decision-record entry with the from state, the to state, the interface, the business date and the attempt count (BR5, BR10, AC1).
6. At the retry limit, `OwnerTaskRaiser` adds one open `task` for the case set with the owner role of the item, the task code and the due date of the task reference rows in force; the case status is not changed (BR6, AC2).
7. On `FileDelivered` for a case that sits in `RETRY_QUEUE`, the writer restores the from state held on the latest decision-record entry of that case and interface; a case with no open retry entry is left as it is (BR7, AC3).
8. The decision record is written first in the transaction: if it cannot be written, no route state and no task change, the listener fails with `MSG-P7-003`, the inbox row is not committed and the message is redelivered (BR8, AC5).
9. The record goes to the local store and, through the library, to `rwb.decision-record.v1`, where rwb-decision collects it into the central ledger (DP-03).
10. No case event is published and no `rwb.case.CaseStateChanged.v1` is raised: the status is unchanged, and the route state is read from the case row by every reader of the case (BR11, DP-09).
11. Nothing of this service resends the file, schedules a retry or writes an item: the resend is the rwb-integration admin operation of the platform administrator and the retry ladder is rwb-integration's (BR12).
12. The task appears on the platform administrator's own task list through `GET /me/tasks` and on the case timeline through `GET /cases/{caseId}/timeline`; the exception queue screen reads the item from rwb-integration (BR13, DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same delivery outcome arrives twice with the same CloudEvents id | The second is dropped, the hit count in `processed_event` becomes 2, and no second entry and no second task exist (R-UNI-40) | None | AC4 |
| X2 | Two worker instances pick the same event | Only one holds the inbox row; the other skips it and changes nothing | None | AC4 |
| X3 | The rwb-integration admin read answers 503 or times out | No route state moves, no task is raised, the inbox row is not committed and the event is redelivered; the breaker opens per downstream | MSG-GEN-006 | AC6 |
| X4 | The item is already ACKNOWLEDGED, or returns no row for the interface and business date | The outcome is applied on the event alone for a delivered file, or parked as an unmatched outcome with an alert on the `.dlt` path; no state is invented | None | AC3, AC6 |
| X5 | The decision-record store is unavailable | No route state and no task change anywhere; the event is not marked processed and fails with `MSG-P7-003` | MSG-P7-003 | AC5 |
| X6 | The task reference row or the route-state code is not in force at the version read | The listener fails as a configuration error, drops no event and raises no task with an invented code | MSG-GEN-006 | AC8 |
| X7 | A class of the package names `rwb_integration`, `public`, a `recovery.v_ace_*` view, a data lake path or an SFTP session | The build fails with boundary rule BND-6 and the class is named | Build log | AC7 |
| X8 | `FileDelivered` arrives for a case that holds no open retry entry | One entry is written for the delivered outcome and the route state is left as it is | None | AC3 |
| X9 | A holder of another role reads the task list of RW-PLATADM | Refused at the edge and by the object check of the service; nothing changes | MSG-P4-002 | AC9, TC-E1-007-10, TC-E1-007-14 |
| X10 | The case of the event no longer exists or is closed | The case is skipped, one entry records the skip with the case ID, and no state and no task is written for it | None | AC1, AC2 |

X9 and X10 are the two paths this slice must not turn into a silent no-op: a reader that sees an empty task list must not read it as "no failure", and a closed case must not be reopened by a file outcome.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P2-E1007-CON and its fakes, the decision-record stub and the reference-data fake; it waits for no other service's build and for no in-lane story |
| Negotiable | The interface, the owner and alert roles, the attempt counts, the task code and due date, and the route-state codes are rows and parameters; the story fixes only the behaviour and the record |
| Valuable | A failed outbound file lands on the case, on an owner's task and on the append-only record on the day it fails, and a later delivery puts the case back |
| Estimable | One listener, one one-hop read, two writers, one task raiser, one inbox guard and one boundary rule; no table, no migration, no workflow, no `Schedule` and no file |
| Small | Fits one sprint with its tests, as the secondary slice of a legacy key |
| Testable | Every criterion in section 7 is one automated test against the contract fakes; the boundary criterion is a build rule |

### 7. Acceptance criteria

```gherkin
Feature: The case side of an outbound file outcome

  Background:
    Given the base is /api/recovery/case/v1, the schema is rwb_case, the topic is rwb.case.events.v1 and the task queue is rwb-case
    Given the rwb-integration adapter contract of RWB-P2-E1007-CON is published and is answered by its fake
    Given the FileFailed outcome names interface "INT-14" and business date "2026-11-10" for cases RC-2026-000441 and RC-2026-000442
    Given the route-state codes and the task reference rows are in force at the version of 2026-11-10 and no code value is written in code
    Given every case, task and item fixture is synthetic and no production case, file or address is used

  Scenario: AC1 A first failed attempt parks each case in the retry route state (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "RETRY" with attempt count 1 and owner role "RW-PLATADM"
    And rwb.integration.FileFailed.v1 arrives on rwb.integration.events.v1 for "INT-14" and "2026-11-10" with the case set of the file
    When the case file-outcome listener handles the event
    Then each case of the file moves to route state "RETRY_QUEUE" and keeps its case status unchanged
    Then one decision-record entry per case is written with the from route state, "RETRY_QUEUE", the interface "INT-14", the business date "2026-11-10", the attempt count 1 and the item reference
    Then no task row is written and no event is published on rwb.case.events.v1
    Then the from route state on the entry is the state the case held before the move
    Then a closed case of the event is skipped and only its skip entry is written

  Scenario: AC2 The retry limit raises the exception route state and one owner task (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "EXCEPTION" with attempt count 3 and owner role "RW-PLATADM"
    And rwb.integration.FileFailed.v1 arrives for the last allowed attempt of the same file and case set
    When the listener handles the event
    Then each case of the file moves to route state "EXCEPTION_QUEUE" and keeps its case status unchanged
    Then one open task is raised for the case set with owner role "RW-PLATADM", the task code and the due date of the task reference rows in force
    Then the route-state writes, the task rows and the decision-record entries are committed in one transaction
    Then the task is readable on GET /me/tasks for a holder of "RW-PLATADM" and the move is readable on GET /cases/{caseId}/timeline
    Then no retry is scheduled by this service and no item row is written

  Scenario: AC3 A delivered file restores the route state the case held (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "ACKNOWLEDGED" with attempt count 3
    And case "RC-2026-000441" sits in route state "RETRY_QUEUE" after a first failed attempt and its entry holds the from route state
    When rwb.integration.FileDelivered.v1 arrives for "INT-14" and "2026-11-10" and the listener handles it
    Then the case returns to the from route state held on its latest entry for that interface and business date
    Then one decision-record entry is written with the action "delivered", the item reference and the attempt count
    Then a case of the file that holds no open retry entry keeps its state and gets one delivered entry only
    Then no task row is changed by this story

  Scenario: AC4 A repeated outcome writes nothing new (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "EXCEPTION" with attempt count 3
    And the FileFailed outcome for "INT-14" and "2026-11-10" has been handled and its entry and task exist
    When the same event is redelivered with the same CloudEvents id
    Then the hit count of the inbox row in processed_event becomes 2 and no second entry and no second task exist
    When the same FileDelivered event is redelivered after the state is restored
    Then the hit count rises and the route state stays as restored
    Then a second worker handling the same event finds the inbox row taken and changes nothing

  Scenario: AC5 The record comes first and a failed write changes nothing (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "EXCEPTION" with attempt count 3
    And the decision-record store is unavailable
    When the listener handles FileFailed at the retry limit
    Then no route state and no task row changes and no inbox row is committed for that event
    Then the listener fails with MSG-P7-003 and the message is redelivered from the topic
    When the store answers again
    Then the event is applied once, with one entry per case and one task for the case set

  Scenario: AC6 The item status is read one hop and a failed read changes nothing (new, D-RCV-60)
    Given the rwb-integration contract mock returns 503 for the interface and business date
    When the listener handles FileFailed
    Then no route state moves, no task is raised and the inbox row is not committed
    Then the read is GET /api/recovery/integration/v1/admin/outbound-items?interfaceId=INT-14&businessDate=2026-11-10 with a 2 s budget, one hop, one GET retry with jitter and a breaker per downstream
    Then no statement of the package names interface_config, outbound_item, outbox_delivery or any other relation of rwb_integration
    Then the event is redelivered after the breaker closes and is applied once

  Scenario: AC7 No cross-schema read, no ACE view, no lake and no file access (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "RETRY" with attempt count 1
    And a class of the package names "rwb_integration.outbound_item"
    When the pipeline runs the boundary rule of the rwb-case build
    Then the build fails with boundary rule BND-6, the class and the object
    When a class names "public.customer" or "recovery.v_ace_account" instead
    Then the build fails with boundary rule BND-6, the class and the object
    When a class names a data lake path, opens an SFTP session or opens a file
    Then the build fails and the class is named
    Then the rwb-case login holds no grant on rwb_integration, on public or on any rwb_* schema but its own
    Then no outbound extract is built, no file is handed over and no lake row exists in this package

  Scenario: AC8 The route states, the task code and the due date are data (new, D-RCV-60)
    Given the rwb-integration contract mock returns item "OB-0001" in status "EXCEPTION" with attempt count 3
    And the task reference row of the outbound-file failure task is in force with its due date rule
    When a new version of that row and of the route-state codes is loaded and a later event is handled
    Then the task carries the task code and the due date of the version in force at the time of the event
    Then the entry records the reference version applied
    Then no route-state code, task code, due date, owner role or attempt count is written in code
    Then a missing or out-of-force row fails the listener with no task and no state change

  Scenario: AC9 A holder of another role cannot read the task list of another role (new, D-RCV-60)
    Given a holder of RW-CASEOWN holds no right to the task list of RW-PLATADM
    When the holder reads GET /me/tasks for the task list of RW-PLATADM
    Then the read is refused with MSG-P4-002 at the edge and by the object check of the service
    Then no row is read and no state or task changes

  Scenario: AC10 The package holds only its own record and the rules of section 8 hold (new, D-RCV-60)
    Given the rwb-integration contract mock returns an item in status "RETRY" with an attempt count
    When the case file-outcome listener handles FileFailed for an interface and a business date
    Then the item is read by one hop with the 2 s budget and no relation of rwb_integration is named in a statement
    Then the decision-record entry is written before any route state moves and carries identifiers, codes and counts only
    Then the case status and the case events stay unchanged and the package holds no retry, resend, timer, item write, outbound file or lake path
    Then a closed case of the event is skipped with one entry and is never reopened

  Scenario: AC11 A route state change the model does not allow is refused (new, D-RCV-60)
    Given a case holds a route state and the reference rows in force allow only the transitions of section 9
    When a route state change outside the allowed transitions is requested
    Then the change is refused and the route state is left as it is
    Then the case status and the case events stay unchanged and no task is written
    Then the refusal message is Not specified in the source documents (NEWAC-RWB-P3-E1007-APP-AC11)
```

The eleven criteria are new work under D-RCV-60 and test only the deliverable in the title: the case side of a delivery outcome. The state to resume is read from the from-route-state element of the latest decision-record entry of the case and interface, because no source names a carrier for it (GAP-0739; ASM-1337). The legacy criteria of RWB-E1-007 are owned elsewhere — AC1, AC2, AC3, AC5, AC6 and AC7 by RWB-P2-E1007-APP, AC4 by RWB-ITG-E1007-ITG, and the end-to-end journey of the key by RWB-ITG-E1007-ITG — and no legacy criterion text is copied into this story (GAP-0739; ASM-1342). The route-state move is internal to the case file-outcome listener and adds no operation to the case contract (GAP-2230; ASM-B2-P3-013-4).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The file is built, sent, retried and parked by rwb-integration inside the window opened by the bank scheduler, on the intervals and attempts of its interface row; this service reacts to the outcome and never executes a delivery | Architecture v5 slides 13 and 16; DP-16; legacy BR4, BR5 | AC2, AC7; TC-E1-007-02 |
| BR2 | The outcome is consumed from `rwb.integration.events.v1` with the CloudEvents envelope and deduped in `processed_event` by consumer and CloudEvents id; a duplicate is counted and dropped | DP-09; R-UNI-40; legacy BR7 | AC4; TC-E1-007-07 |
| BR3 | The item status, the attempt count, the owner role and the last error are read from the rwb-integration admin operation only, one hop with a 2 s budget; no relation of `rwb_integration` is named in a statement | DP-11; DP-16; legacy BR2 | AC6; TC-E1-007-12 |
| BR4 | The target route state is chosen by the item status from the reference rows in force — RETRY answers RETRY_QUEUE, EXCEPTION answers EXCEPTION_QUEUE — and no state code is written in code | DP-07; R-UNI-33; R-UNI-36; legacy section 9 | AC1, AC8; TC-E1-007-03, TC-E1-007-13 |
| BR5 | Each case of the file moves once per outcome, and the move is written with its decision-record entry in one transaction | DP-03; R-UNI-33; R-UNI-34; legacy section 9 | AC1, AC2; TC-E1-007-03 |
| BR6 | When the retry limit is reached one open task is raised for the case set with the owner role of the item, the task code and the due date of the task reference rows in force | R-UNI-34; legacy BR6; REQ-DRI-007 | AC2; TC-E1-007-03 |
| BR7 | A delivered file puts a case back to the route state held on the latest entry of that case and interface; a case with no open retry entry is left as it is | R-UNI-35; legacy section 9 (RETRY_SUCCEEDED to RESUME_STATE) | AC3; TC-E1-007-09 |
| BR8 | The record comes first: a decision record that cannot be written fails the whole outcome, so no state and no task is changed that cannot be recorded | R-UNI-39; DP-03 | AC5; TC-E1-007-11 |
| BR9 | A rule that acts twice on one outcome is a defect, and the inbox is the only guard | R-UNI-40; DP-09 | AC4; TC-E1-007-07, TC-E1-007-08 |
| BR10 | The entry names the interface, the business date, the item reference, the attempt count, the from and to route states, the reference version and the recorded time, and carries no name, address, identity number or file content | CTL-11; Guardrails; legacy BR10 | AC1; TC-E1-007-03 |
| BR11 | The case status is not changed and no case event is published by this story; the route state is data on the case row | TSD P3 v3 T3.1 (DF-CAS-005, DF-CAS-007); R-UNI-33, R-UNI-34; legacy section 9; RWB-P3-E1020-APP | AC1, AC3; TC-E1-007-03 |
| BR12 | This service resends no file, holds no timer and writes no item: the resend is the rwb-integration admin operation and the retry ladder is rwb-integration's | Legacy BR1, BR9; DP-16; RWB-P2-E1007-CON | AC2, AC7; TC-E1-007-02 |
| BR13 | The owner task and the route state are read through the case contract (`GET /me/tasks`, `GET /cases/{caseId}`, `GET /cases/{caseId}/timeline`), and the exception-queue screen reads the item from rwb-integration through the gateway-bff composite route | DP-19; legacy section 15 | AC9; TC-E1-007-10, TC-E1-007-14 |
| BR14 | There is no data lake, no outbound file and no inbound file: no lake path, no lake copy, no extract, no file load and no inbound interface row is built or read by this package | DP-17; legacy BR9; D-RCV-35 U1 | AC7; TC-E1-007-01 |
| BR15 | A case that is closed, or that the event names and `rwb_case` does not hold, is skipped with one entry and is never reopened or invented | Legacy X-rows; Guardrails | AC1; X10; TC-E1-007-03 |

How the rules hold in `rwb_case`: BR1 is the absence of a delivery path in the package. BR2 is `InboxGuard` over `processed_event`, whose unique key is (consumer, idempotency key), so two workers cannot both proceed. BR3 is `ItemStatusReader`, one hop with the breaker, and the boundary rule refuses a statement that names `rwb_integration`. BR4 and BR7 are `RouteStateResolver`, which reads the codes from the reference rows at the version in force and never holds a literal. BR5, BR6 and BR8 are one transaction with the record written first. BR9 is the inbox. BR10 is `FileOutcomeRecordWriter`, which carries identifiers, codes and counts only. BR11 is the absence of a status write and of a case event. BR12 is the absence of a retry or a resend path. BR13 is the baseline case contract, which this story reads and does not extend. BR14 is the absence of a file or lake element anywhere in the package. BR15 is the skip path of the listener.

### 9. State transitions

The route state of the case, held on `recovery_case.route_state`. The From and To values below are route-state codes from the reference rows of `rwb_case` (section 12.7); they are not values of LOV-CASE-STATUS:

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE, consumed as `FileFailed` with item status RETRY | First failed attempt of an outbound file for the case | RETRY_QUEUE |
| RETRY_QUEUE | RETRY_SUCCEEDED, consumed as `FileDelivered` | A later attempt is sent and the file is delivered | RESUME_STATE, the from state held on the latest entry |
| RETRY_QUEUE | RETRY_LIMIT_REACHED, consumed as `FileFailed` with item status EXCEPTION | The attempt count equals the max attempts of the interface row | EXCEPTION_QUEUE, with one open task for the owner role |
| ANY_ACTIVE | DUPLICATE_OUTCOME | The CloudEvents id is already in `processed_event` | Unchanged, hit count raised |
| CLOSED | any delivery outcome | The case is closed; one skip entry is written and no task is raised | Unchanged |

The case status (`recovery_case.status`) does not change in any row of this table, and this story writes no case event. `outbound_item.status` (PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED; LOV-OUTBOUND-STATUS, TSD P2 v3 T3.2) and `outbox_delivery.status` (PENDING, RETRYING, DELIVERED, EXCEPTION) are rwb-integration's and are observed through its admin read only. This story holds no run-record row: the run record of an outbound file is the owner's item plus its delivery rows.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Consumes the two outcomes, reads the item one hop, moves the route state, raises the owner task and writes the decision-record entries |
| rwb-integration service identity | Builds, sends, retries and parks the file, publishes `FileDelivered` and `FileFailed` and owns the item, the interface row and the exception queue |
| rwb-decision service identity | Collects the decision records from `rwb.decision-record.v1` into the central ledger |
| RW-PLATADM, platform administrator | Receives the owner task, reads the case, and resends an exception item through the rwb-integration admin operation (Platform administration, U) |
| RW-DATASTEW, data steward | Reads the route state and the task on the case (Platform administration, R) |
| RW-CASEOWN, case owner and RW-TEAMMGR, team manager | Read the case and its timeline; neither raises nor clears the task of this story |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read the route state, the task and the decision-record entries (Platform administration, R) |
| No approval level from the delegation of authority applies | The story takes no approval decision; it moves a route state and raises a task |

No role grants itself a row, and no route-state code, task code, due date, owner role or attempt count is fixed in code. The login name, the task code and the due date rule are Not specified in the source documents (GAP-0739; ASM-1338).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` (P3, `rwb_case`) | id | Read; the cases of the file |
| DF-CAS-002 | `recovery_case` (P3, `rwb_case`) | case_no | Read; the case reference of the entry |
| DF-CAS-005 | `recovery_case` (P3, `rwb_case`) | status | Read; a closed case is skipped, never written |
| DF-CAS-007 | `recovery_case` (P3, `rwb_case`) | route_state | Read and write; RETRY_QUEUE, EXCEPTION_QUEUE and the restored state |
| DF-WRK-017 | `task` (P3, `rwb_case`) | id | Write; one open task for the case set |
| DF-WRK-018 | `task` (P3, `rwb_case`) | case_id | Write; one open task for the case set |
| DF-WRK-019 | `task` (P3, `rwb_case`) | task_code | Write; the code of the task reference row in force (GAP-0739; ASM-1338) |
| DF-WRK-020 | `task` (P3, `rwb_case`) | element_type | Write; the element type of the task reference row |
| DF-WRK-022 | `task` (P3, `rwb_case`) | status | Write; open |
| DF-WRK-023 | `task` (P3, `rwb_case`) | owner_role | Write; the owner role answered by the item |
| DF-WRK-024 | `task` (P3, `rwb_case`) | due_at | Write; the due date rule of the task reference row in force (GAP-0739; ASM-1338) |
| DF-OPS-168 to DF-OPS-177 | `outbound_item` (P2, `rwb_integration`) | id, interface_id, attempt_count, status, last_error, owner_role | Read through `GET /api/recovery/integration/v1/admin/outbound-items` only; no row read |
| DF-OPS-137 to DF-OPS-148 | `interface_config` (P2, `rwb_integration`) | interface_id, direction, max_attempts, retry_intervals_min, owner_role, alert_role | Read through the owner's contract answer only; never named in a statement |
| DF-OPS-178 to DF-OPS-183 (library numbering, created in `rwb_case`) | `processed_event` (PLT library) | consumer, idempotency key, CloudEvents id, hit count, last seen at | Write; the inbox of the two outcomes |
| DF-REF-035 | `role` (P3, `rwb_case`) | role_code | Read; the owner role of the task is a role code of the service |
| Decision entry (local) | decision record (P3, written through the P7 library) | action, interface_id, business_date, item reference, attempt count, from and to route state, reference version, recorded at | Write; one entry per case per outcome |
| `reference_row`, `reference_version` (P3, `rwb_case`) | the route-state codes, the task code and the task due date rule | `row_key`, `row_data`, `version_label`, `valid_from`, `valid_to` | Read at the version in force; no value is written in code (GAP-0739; ASM-1338) |

`recovery_case` and `task` are this service's rows and are written in one transaction per outcome; `processed_event` is created in `rwb_case` by the platform library, and the decision entries are written into the service's own schema. No foreign key leaves `rwb_case`, no row of another service is copied into it, and no ACE field is read: the case side of a file outcome needs no source data at all (DP-01, DP-05). Field IDs are those of the Logical Data Model and Data Dictionary and of the legacy story section 11. The legacy names `recovery_svc` (section 13, DP-02) and `interface_run` do not name a field of this story.

### 12. Contract

#### 12.1 REST operations provided

None new. The base is `/api/recovery/case/v1` and the operations that read the result are the baseline's: `GET /cases/{caseId}`, `GET /cases/{caseId}/timeline` and `GET /me/tasks`. This slice adds no path, no query parameter and no response field: the legacy `/api/recovery/v1` case-action path and the in-process `CaseEvents.raise` and `TaskApi.raiseTask` have no target operation, so the move is an internal service of the listener (GAP-0739; ASM-1339).

#### 12.2 REST operations consumed

One operation, one hop, 2 s client budget, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020).

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/outbound-items?interfaceId=&businessDate=` | P2 rwb-integration | Reads the item of the outcome: its status, attempt count, last error and owner role, so the retry state and the exception state are decided on the item and not on a value copied into the payload (AC1, AC2, AC6) |

No second call is made at run time: the route-state codes and the task rows come from this service's own reference tables through the client library of DP-07, and the authorisation of a human reader is answered at the edge and by the object check of the service. The interface row itself is never read here: its attempts, intervals and roles are answered by the item read.

#### 12.3 Events published

None of its own. A route-state move keeps the case status and therefore publishes no `rwb.case.CaseStateChanged.v1`; the topic `rwb.case.events.v1` with the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` belongs to the case, allocation, transfer, state and timer stories under DP-14, and this slice adds none of them. The decision record is written through the DP-03 library, which publishes `rwb.decision-record.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1` under its own schema (RWB-PLT-E1027-CON). A file-outcome event of this service would duplicate `FileFailed` and `FileDelivered` and is not declared.

#### 12.4 Events consumed

| Event type | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | First sight: one item read, then per case the route state RETRY_QUEUE or EXCEPTION_QUEUE and one entry; at the retry limit one open owner task (AC1, AC2) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | First sight: the route state restored from the latest entry of the case and interface, and one entry with the action delivered (AC3) |

Both arrive with the CloudEvents 1.0 envelope in binary mode, are keyed by case ID or by file, and are deduped by consumer and CloudEvents id in `processed_event`; a message without the envelope, or of any other type, is refused by the schema check and routed to `.dlt` with an alert (DP-09). The payload of both is taken from the AsyncAPI document of RWB-P2-E1007-CON: the file, interface and business date and the case set for both, and the attempt count and last error for the failed outcome. The element names used by this story's reader beyond that contract are Not specified in the source documents (GAP-0739; ASM-1336) and no element is named a second time here.

#### 12.5 Workflows and activities

None registered. The listener runs on the `rwb-case` worker of the workflow kit and writes in one database transaction per outcome; it starts no workflow, signals none, registers no activity and adds no timer. The `CaseWorkflow` of RWB-P3-E2043-APP is not extended by this story: it reads the case row, and the route state is a column of that row (GAP-0739; ASM-1339).

#### 12.6 Schedules

None. The daily build window and the one-minute sender are rwb-integration's `deliverFile` path; JOB-13 and JOB-15 are removed with the data lake (DP-17), and INT-19 and INT-20 are removed with no target in this service; and the retry intervals are data of the interface row. This story registers no `Schedule`, no cron and no Quartz row (DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `recovery_case` | `rwb_case` | rwb-case (P3) | `route_state` read and written; `status` read so a closed case is skipped; no other column touched |
| `task` | `rwb_case` | rwb-case (P3) | One open task per case set at the retry limit |
| `reference_row`, `reference_version` | `rwb_case` | rwb-case (P3) | The route-state codes and the task code and due date rule, read through this service's contract and never joined in SQL |
| `processed_event` | PLT library, created in `rwb_case` | Platform library | The inbox of the two outcomes (DP-09) |
| decision entry (local decision record) | P3 rows in `rwb_case`, written through the P7 library | rwb-case (P3) rows, library P7 | One entry per case per outcome (DP-03) |

No table is created, altered or added, and no migration of its own is written. `interface_config`, `outbound_item` and `outbox_delivery` are P2's and appear in no statement of this package; `document` is P5's and is not reached at all; no `v_ace_*` view is named (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Kafka stubs | `rwb.integration.events.v1` | One `FileFailed` at a first attempt, one at the retry limit, one `FileDelivered`, a duplicate of each with the same CloudEvents id, one event for an unknown interface, one event naming a closed case, one malformed envelope |
| rwb-integration admin WireMock | `GET /api/recovery/integration/v1/admin/outbound-items` | One item in RETRY with attempt count 1, one in EXCEPTION with attempt count 3, one ACKNOWLEDGED, one empty answer and one 503 |
| decision-record library stub | DP-03 | A healthy chain and a stopped chain for the `MSG-P7-003` path |
| reference-data fake | DP-07 | The route-state codes and the task reference rows at the version in force, plus one row out of force |
| rwb-source-data contract fake | DP-05 | None in this slice: no ACE fact is read; the boundary fixtures are classes, not data |
| `processed_event` fixture in `rwb_case` | DP-09 | A fresh inbox and a taken inbox for the duplicate path, and one taken inbox for the second worker |
| rwb-case seed set | This story's own test data | Cases `RC-2026-000441` and `RC-2026-000442` in `RETRY_QUEUE`, the same cases in `EXCEPTION_QUEUE`, one closed case, one case that holds no open retry entry |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided, 1 consumed | `GET /api/recovery/integration/v1/admin/outbound-items` on rwb-integration; one hop, 2 s timeout, one GET retry with jitter, breaker per downstream |
| Kafka | 0 published by this story, 2 consumed | `FileFailed` and `FileDelivered` on `rwb.integration.events.v1` with the inbox dedupe; the decision-record library publishes on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities, 0 signals | The listener is a plain consumer on the `rwb-case` worker; no `Schedule` and no timer |
| File | 0 | No file is opened, read, built, stored or handed over; the case side of a file outcome holds no bytes (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case.fileoutcome`, module `fileoutcome`, in the service root `th.co.scb.ace.workbench.recovery.case`; the boundary rule is added to the test source tree of the service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; never read another service's tables; the case and the task are this service's rows | none |
| DP-02 | `recovery_svc` login | One login per service: the rwb-case login holds `rwb_case` only | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; one entry per case per outcome, written first | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts only through rwb-source-data's contract; this slice reads no view at all, and the boundary rule refuses one | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case and the client library: the route-state codes and the task code and due date rule | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON; built against the fake until published |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents 1.0, the owner's topic, retry topics and `.dlt`; the inbox is the only guard against a second application | H RWB-PLT-TE006-CON; built against the fake until published |
| DP-10 | Quartz, JOB-nn | No job and no Schedule: the build window and the sender are rwb-integration's Temporal path, the due date of the task is data, and the listener runs on the `rwb-case` worker of the kit | H RWB-PLT-E1071-CON; built against the fake until published |
| DP-11 | In-process call, published interface | REST contract with mock, one hop, 2 s timeout; the legacy published interfaces `CaseEvents` and `TaskApi` become internal services of the listener | none (C from the legacy dependency) |
| DP-16 | `recovery.integration.adapter` | The rwb-integration contract: the two outcomes and the admin item read | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); no lake target, no lake file, no lake row and no outbound extract; reporting is from events into rwb-reporting | none; gap if the story needed lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route for the exception queue and the case screens | H RWB-PLT-N001-CON; built against the fake until published |

**This is a secondary slice: the metadata H row is None and this story adds no build dependency of its own.** The platform contracts behind DP-03, DP-07, DP-09, DP-10 and DP-19 arrive with the `rwb_case` baseline and the platform epics, so they are not repeated in the metadata rows (GAP-0739; ASM-1340). DP-10 resolves to a prohibition (no `Schedule`, no job, no timer in this package), DP-05 to a prohibition enforced by the boundary rule, DP-01 to "the case and the task are this service's and no other schema is named", DP-17 to "no lake element and no outbound extract anywhere in the package", and DP-11 to the one-hop budget of the item read plus the conversion of the legacy in-process interfaces into internal services of the listener (GAP-0739; ASM-1339). The one contract dependency, `RWB-P2-E1007-CON` of DP-16, never blocks a build (§R5.4): the Kafka stubs and the admin-read fake of 12.8 stand in for rwb-integration on Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `FileOutcomeListener` | Listener | Consumes the two outcomes, validates the envelope, checks the inbox and drives the case-side steps in the order of section 4 |
| `InboxGuard` | Component | Inserts into `processed_event`; on conflict increments the hit count and drops the message |
| `ItemStatusReader` | Client | `GET /api/recovery/integration/v1/admin/outbound-items`, one hop, 2 s, breaker per downstream |
| `RouteStateResolver` | Service | Maps the item status to the target route state, and the `FileDelivered` outcome to the state to resume, from the reference rows in force |
| `CaseRouteStateWriter` | Repository | Writes `recovery_case.route_state` per case in the transaction of the outcome; skips a closed case |
| `OwnerTaskRaiser` | Service | Adds one open `task` for the case set with the task code, element type, owner role and due date of the reference rows in force |
| `FileOutcomeRecordWriter` | Service | Writes the decision-record entry first in the transaction through the DP-03 library |
| `FileOutcomeBoundaryRule` | ArchUnit rule in the test source | BND-6 over the module map: no `rwb_integration`, no `public`, no `v_ace_*` view, no lake path, no file and no SFTP class |

**Database and migrations.** None. This story creates no table, adds no column and writes no migration: `recovery_case`, `task`, `reference_row` and `reference_version` are the `rwb_case` baseline, and `processed_event` is created in `rwb_case` by the platform library migration. The service connects with its own login (DP-02), holding grants on `rwb_case` only. The only schema this service writes is `rwb_case`; `rwb_integration` is named here only as the schema of rwb-integration, which this service never reads and holds no grant on.

**Configuration and reference data**

- The route-state codes for the retry and the exception route state, and the resume-path convention: reference rows of rwb-case at the version in force; no code value is written in code.
- The task reference row of the outbound-file failure task: its task code, element type, owner-role rule and due date rule, read at the version in force. The values are Not specified in the source documents (GAP-0739; ASM-1338).
- The interface, its attempts, its intervals and its owner and alert roles stay in the interface row of rwb-integration and are never copied into this service; the item read answers them for the case at hand.
- The feature switch is `rwb.case.file-outcome`, read as a flag of the platform flag library (§R3 default rulings): off means the listener drops the outcomes with an alert and no state moves.

**Build steps**

1. `InboxGuard` over `processed_event` with the duplicate and the concurrent-worker cases; tests for AC4.
2. `ItemStatusReader` with the 503, the empty and the timeout paths and the breaker; tests for AC6.
3. `RouteStateResolver` over the reference rows, with a fixture set for RETRY, EXCEPTION and delivered; tests for AC1, AC3 and AC8.
4. `CaseRouteStateWriter` with one transaction per outcome, the closed-case skip and the case status left untouched; tests for AC1, AC2 and X10.
5. `OwnerTaskRaiser` with the task code, the owner role and the due date of the rows in force; tests for AC2 and AC8.
6. `FileOutcomeRecordWriter` written first in the transaction, with the stopped-chain path; tests for AC5.
7. `FileOutcomeListener` wiring the six steps in the order of section 4; the contract-fake run of the whole path.
8. `FileOutcomeBoundaryRule` and the module map, with fixture classes on `rwb_integration.outbound_item`, `public.customer`, `recovery.v_ace_account`, a lake path and an SFTP session; tests for AC7.

**Feature switch.** `rwb.case.file-outcome`, read as a flag of the platform flag library.

**Open decisions.** Open decision DL06 has the assumptions ASM-0189, ASM-2559, ASM-2608 and ASM-2776. The directive accepts the recommended resolution of DL06 and confirms each of these assumptions.

**Screen states (SCR-09, exception queue).** Empty: a task list or exception-queue read with no row is never shown as no failure (X9, X10). Loading, error and no access: Not specified in the source documents (DOR-RWB-P3-E1007-APP-10; CG-ALL-3390). A role that does not hold the task list or the case is refused with MSG-P4-002 (X9).

**Done when.** The tests of section 16 pass, each case of a failed file moves once, one task exists per case set at the retry limit, a delivered file restores the state held on the entry, a redelivery writes nothing, the build is green and red on the five boundary fixtures, and a session as the rwb-case login holds no privilege on `rwb_integration`, on `public` or on any `rwb_*` schema but its own.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written, so no route state and no task is changed | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, in `FileOutcomeRecordWriter` |
| MSG-GEN-006 | The rwb-integration admin read is unavailable, or a reference row is not in force, and the outcome is retried | {system} is not available. Your request is queued and will be retried. | This story, on the item read and the reference read |
| MSG-P4-001 | The caller holds no Workbench role when reading the task list or the case | You have no Recovery Workbench role. Ask your team manager to request one. | rwb-access, surfaced here |
| MSG-P4-002 | A role without the right reads a task list or a case it does not hold | You cannot {action} here. Your role does not include it. | rwb-access, surfaced here |
| MSG-P2-001 | Produced by rwb-integration when its item moves to the exception queue; read here as the reference of the task description, never produced | The {interface} file {file} was not sent after {count} attempts. It is in the exception queue. | rwb-integration, read here |
| MSG-GEN-004 | A reader acts on a case whose version changed | Someone else changed this record. Reload it to see their change. | This story, on the case read |
| Build log | A class names `rwb_integration`, `public`, a `v_ace_*` view, a lake path or a file | Boundary rule BND-6 broken: {class} names {object}. A case class names no other schema, no ACE view, no lake and no file. | This story, in the pipeline |

For MSG-P4-002 in this story, {action} names the action the role tried, for example "read the task list of another role", and never a row of a case. No new `MSG-` identifier is introduced by this story, and no identifier is renumbered by the realignment. The task description text and the alert text are Not specified in the source documents (GAP-0739; ASM-1338) and are owned by RWB-P2-E1007-OPS through the alert role of the interface row. The refusal order is fixed: session, then right, then the case, and only then is a row read or a state moved.

### 15. Screens and states

No screen is built by this story. The exception queue is SCR-09, served by the gateway-bff composite route (DP-19): it reads the failed items from rwb-integration through that service's admin operation and shows them with the interface, the attempt count, the last error and the case count, and this story supplies the other half — the route state of each case and the open owner task. The case record view and the timeline show the route state and the task without a screen of this story. The route path, the screen-model field list and the visual layout are Not specified in the source documents (GAP-0739; ASM-1338) and belong to RWB-PLT-N001-CON and the designer.

| Screen | State | What the reader sees through the owner's contract |
|---|---|---|
| SCR-09 Exception queue | Retry | The item in RETRY on the rwb-integration read, and the case in route state RETRY_QUEUE with one entry and no task |
| SCR-09 Exception queue | Exception | The item in EXCEPTION with `MSG-P2-001`, the case in route state EXCEPTION_QUEUE and one open task for RW-PLATADM |
| SCR-09 Exception queue | Restored | The case back in the state it held, one entry with the action delivered, and the task unchanged |
| SCR-09 Exception queue | Repeated | The same view as the first outcome, with the inbox hit count raised and no second entry and no second task |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-3390) |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-3390) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-3390) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-3390) |
| Case record view and timeline | Delivery state | The route state of the case and the owner task, with the interface, the business date and the attempt count of each entry |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-10 | X9, BR13 | End to end | A holder of RW-CASEOWN reading the task list and the case of another role; refused with MSG-P4-002 and nothing changed |
| TC-E1-007-01 | AC7, BR14 (the one adapter pattern is RWB-P2-E1007-APP's) | Component | Negative boundary fixture classes on `rwb_integration.outbound_item`, `public.customer`, `recovery.v_ace_account`, a lake path and an SFTP session; no data is set up in an ACE view, and any ACE fact comes from the rwb-source-data contract fake (section 12.8), none in this slice |
| TC-E1-007-02 | AC2, AC7, BR1, BR12 (the ACE-view read is RWB-P1-E1069-APP's and the file build is RWB-P2-E1007-APP's) | Component | The same boundary fixture set, with one passing class on the service's own rows |
| TC-E1-007-03 | AC1, AC2, BR4, BR5, BR6, BR10, BR11, BR15 | Integration | WIN file for 85 synthetic cases; items in RETRY with attempt count 1 and in EXCEPTION with attempt count 3; route states, one entry per case and one task for the case set asserted |
| TC-E1-007-04 | None here (the held request is RWB-P2-E1007-APP's and RWB-ITG-E1007-ITG's); this story reacts only to a published outcome | Integration | No event is published while the request is held, so the listener has nothing to apply and no state moves |
| TC-E1-007-07 | AC4, BR2, BR9 | Component | Each outcome sent twice with the same CloudEvents id; hit count 2, no second entry and no second task |
| TC-E1-007-08 | AC4 (the second-worker path) | Component | Two worker instances on one event; one inbox row taken and one change |
| TC-E1-007-09 | AC3, BR7 | Integration | Item in EXCEPTION after 3 attempts, then a resend through the rwb-integration admin operation and a `FileDelivered`; the state restored from the entry |
| TC-E1-007-05 | None (retired with the inbound file load; the behaviour is ACE ingestion and EV-27 AceDataLate) | NFR | Asserts that no inbound FileLoadAdapter, inbound folder listing, DQ-057 or DQ-059 check, JOB-09 missing-file run row, interface_run or interface_signoff exists in this service; closed when the ACE ingestion story publishes its own checks |
| TC-E1-007-06 | None (retired with the inbound file load; the behaviour is ACE ingestion) | NFR | Asserts that no inbound file load, inbound folder listing or DQ-057 and DQ-059 check exists in this service; the behaviour is ACE ingestion; closed when the ACE ingestion story publishes its own checks |
| TC-E1-007-11 | AC5, BR8 | Component | Decision-record library stub with a stopped chain for MSG-P7-003; FileFailed at the retry limit for INT-14; business date Not specified in the source documents (CG-ALL-3385) |
| TC-E1-007-12 | AC6, BR3 | Integration | rwb-integration admin WireMock failing the read for INT-14; business date Not specified in the source documents (CG-ALL-3385); the event is redelivered after the read recovers |
| TC-E1-007-13 | AC8, BR4 | Component | Reference-data fake with the route-state codes and the task row in force, then a new version and one row out of force |
| TC-E1-007-14 | AC9, X9, BR13 | Component | A holder of RW-CASEOWN reads the task list of RW-PLATADM; refused at the edge and at the object check with MSG-P4-002 and no row read |
| TC-E1-007-15 | AC10, BR1, BR3, BR8, BR10, BR11, BR12, BR14, BR15 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1007-APP-AC10) |
| TC-E1-007-16 | AC11 | Component | A route state change outside the transitions allowed by the reference rows in force; refusal asserted and no state or task change; refusal message Not specified in the source documents (NEWAC-RWB-P3-E1007-APP-AC11) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to Integration or End to end and Access to End to end. Every legacy test case of this key is listed above with the slice of the behaviour this story answers: TC-E1-007-03 answers the retry and the exception route state with the owner task, which is exactly the case-side half of the key; TC-E1-007-07 and TC-E1-007-08 answer the duplicate and the concurrent worker on the consumed outcome; TC-E1-007-09 answers the restore after a resend; TC-E1-007-10 answers the right check on the case read; TC-E1-007-01 and TC-E1-007-02 answer the adapter pattern and the ACE-view read, whose mechanics are RWB-P2-E1007-APP's, and are answered here only as the boundary prohibition of AC7; and TC-E1-007-05 and TC-E1-007-06 stay as retired legacy IDs. The `-ITG` copies of these cases are not here — they belong to RWB-ITG-E1007-ITG, which proves the file path across the real services.

### 17. Guardrails

- No business value in code: the route-state codes, the task code, the due date rule, the owner and alert roles, the attempts, the intervals and the feature switch are rows and parameters read at run time.
- No personal data in events, logs, workflow inputs, decisions, tests or prompts: the entry carries identifiers, codes, counts and dates, and no file content is ever logged.
- ACE data only through the owner's contract or `v_ace_*` views — and this package reads neither: a class that names a view or `public` fails the build.
- No cross-schema read and no cross-schema key: `rwb_case` holds no foreign key into another schema and no copy of an item, an interface row or a delivery row; the item is read through the rwb-integration admin operation only (DP-01).
- No file access and no outbound extract: the package opens no file, no SFTP session and no lake path, and hands no bytes to anyone (DP-16, DP-17).
- The record comes first: a state move that cannot be recorded is not made, and an outcome that cannot be recorded fails the listener rather than being dropped (R-UNI-39).
- One hop, no chaining: the item read never calls a downstream of a downstream, and the breaker and bulkhead are per downstream.
- The case status is not moved by a file outcome, and no case event is published for it; a story that changes `recovery_case.status` here has left this slice.
- No new table, no column, no migration, no workflow and no `Schedule`: a story that adds one of them has left this slice.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No direct call to a system of record; source data is read from ACE through the views and leaves through ACE's paths and the Workbench outbound adapters | Program 5.2; Epic 1 3.2 | FEAT-DRI-10, FEAT-DRI-11 | All recovery processes | ADR-010; BR-P2-001-ACE; BR3, BR12 | TC-E1-007-01, TC-E1-007-02, TC-E1-007-04 |
| REQ-DRI-007 | Every outbound file is logged, retried on a defined schedule and raised to a named owner in an exception queue | Program 5.2; Epic 1 3.2 | FEAT-RDF-21, FEAT-RDF-23, FEAT-RDF-24, FEAT-DRI-13 | All recovery processes | R-UNI-33, R-UNI-34, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40; BR1, BR5, BR6, BR8, BR9 | TC-E1-007-01, TC-E1-007-03, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09, TC-E1-007-10 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; the Workbench runs no file load and no lake copy | Program 5.2; Epic 1 3.2 | FEAT-RDF-24, FEAT-DRI-10 | All recovery processes | D-RCV-35 U1; DL06; BR14 | TC-E1-007-04, TC-E1-007-05, TC-E1-007-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, claim-check for files | Decision log, D-RCV-60; ADR-020 | DP-11, DP-16 | All recovery processes | ADR-020; BR2, BR3 | TC-E1-007-03, TC-E1-007-09 |

The supporting features of this slice are FEAT-RDF-24 (raise an interface failure to the exception queue) and FEAT-DRI-13 (detect and ignore a duplicate event), which the FSD P2 module pairs with the outbound stories; this slice answers them on the case side only and changes neither the adapter nor the event design. The `-ITG` copies of the test cases and the end-to-end journey of the key are carried by RWB-ITG-E1007-ITG.

### 19. Out of scope

- The outbound-file capability itself — the builder, the MFT/SFTP transport with PGP, the retry ladder on `retry_intervals_min`, the exception queue, the resend, the `MSG-P2-001` message and the two events: RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-P2-E1007-INF and RWB-P2-E1007-OPS.
- The real cross-service journey of the outbound path with all services live: RWB-ITG-E1007-ITG.
- The WIN notice file and its request: RWB-P6-E1007-APP and the P6 notice stories. The debt buyer data tape and the data room: RWB-S6-E1007-APP and the S6 debt-sale stories.
- The stored bytes, the document hub and the claim-check read: RWB-P5-E1007-APP and the P5 document stories.
- The exception-queue and case screens, their composite route and their states: RWB-PLT-N001-CON and the screen stories. This story supplies the case state they render.
- The alert rules, their thresholds and their identifiers: RWB-P2-E1007-OPS, over the alert role of the interface row.
- The case status machine, the route sets and the rule packages that decide a route: RWB-P3-E1021-APP, RWB-P3-E2042-APP and RWB-P7-E1073-CON. This story moves a route state for a file outcome and writes no rule.
- The `CaseWorkflow` itself and its durable timers: RWB-P3-E2043-APP and RWB-P3-E1028-APP. This story registers no workflow, no activity and no timer.
- The data lake and every lake statement of the legacy key, including the JOB-15 reporting extract (INT-19) and the JOB-13 decision-log copy (INT-20): removed by DP-17, with reporting from events into rwb-reporting (GAP-0739; ASM-1341).
- Inbound source ingestion, its schedules and its checks: RWB-ACE-001. There is no inbound file in this story and none is built.
