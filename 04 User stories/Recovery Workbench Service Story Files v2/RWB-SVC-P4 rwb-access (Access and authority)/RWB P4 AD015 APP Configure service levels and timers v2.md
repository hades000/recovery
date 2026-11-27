# RWB-P4-AD015-APP Configure service levels and timers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-I |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-P4-AD015-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1028-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-015 for `rwb-access`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-AD015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 15 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator, and the access service that accepts the service-level load**, I want **the time allowed in each case state, its warning point and its escalation point accepted as a versioned load only when every row of the file is valid, approved by a second person under four eyes and recorded in the decision record before the answer, with the effect on every timer already running named in that answer**, so that **clocks and escalations follow the agreed service levels from the day the version is approved, a timer already running keeps the due date the case was worked to unless the approved row says to recompute it, and nobody can load and approve the same change alone**.

This story is the administration-ingest slice of RWB-AD-015 in `rwb-access`:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access` (P4 context pack; R4).
- Two deliverables and nothing else: the three operations of the service-level load gate — load, approve and read — which validate the whole file, hand the accepted file to `rwb-case` through its service-level contract, write the decision record before the answer and return the load with the effect on every timer already running.
- The clock is never this story's. The stage clock is a durable Temporal timer inside `rwb-case`'s `CaseWorkflow`, raised from the version in force; the escalation is a signal into that workflow, not a job (Architecture v5 slides 42 and 44; Temporal and Drools Design slide 13). This story loads the values the clock reads and reports what the clock did with the timers already running.
- `timer`, `recovery_case`, `queue` and `task` stay `rwb-case`'s. This story reaches them only through the contract of `RWB-P3-E1028-CON`, holds no timer row and writes no case table (DP-01).
- The legacy endpoints of RWB-AD-015 are the general reference-load pair `/admin/reference-loads` and `/admin/reference-loads/{loadId}/approve` (TSD P4 v3 API-P4-005 and API-P4-006), whose declared rights are Reference data C and A. The legacy story's own permission table instead gives Rules and parameters C and A. The paths this story serves for `rwb-access` and the rights it applies are Not specified in the source documents (GAP-2275; ASM-3757; GAP-2276; ASM-3763).
- The column names, order, delimiter and header of the service-level file are Not specified in the source documents (GAP-2275; ASM-3758); the columns this story reads are the state code, the allowed working days, the warning point, the escalation point, the escalation role, the recompute instruction and `valid_from`.
- The working-day calendar, the state code list and the escalation roles are data: the calendar and the state codes are read through the reference-data contract of DP-07, and an escalation role must be a `role` row of `rwb_access`. Their codes are Not specified in the source documents (GAP-2275; ASM-3760; ASM-3761).

### 2. Business rationale

DL22 asked how long a case may stay in each state before it escalates, and the answer was to hold the values as parameters that take effect from the day they are loaded. RWB-AD-015 is that answer in the monolith: the service level, its warning and its escalation point were rows of the recovery schema, loaded from an administration screen, and a short-interval job walked the timers to raise the warning and the breach. The measure survives the move: rule and limit changes are made without a code release, 100 percent (FSD P4 A2.17.1).

In the target the values are still data loaded by administration, but the clock has moved into `rwb-case`'s workflow as a durable Temporal timer and the escalation has become a signal. That move changes what administration must do: it no longer writes a table a job reads, it hands a validated version to the service that owns the clock and reports what happened to the timers already running.

Three consequences are the whole of this story. The file is validated as a whole before anything is handed over, because a half-loaded service level would leave some states on new values and some on old ones and no screen could tell which. The load is approved by a second person, because the same administration area already governs rule versions that way (Temporal and Drools Design slide 15; FSD P4 A2.4.4.3 AC-EXC-P4-004-03). And the answer names, per running timer, whether the due date was kept or recomputed, because only the service that holds the clock can answer that.

This story meets REQ-CWC-011 on the administration side, REQ-DRI-010 because the values are parameters with versions, REQ-DRI-005 and REQ-DRI-011 at its own edge, and REQ-ACA-013 because the administration surface follows the caller's rights. The breach, the escalation signal, the pause of a stage clock and the prescription date stay with `rwb-case` (RWB-P3-E1028-APP/CON).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD015-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the three operations, the `ServiceLevelLoad`, `ServiceLevelRow` and `RunningTimerEffect` schemas, the state set, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same unit of work as the answer |
| RWB-PLT-E1042-CON | The parameters client library (DP-06): the four-eyes switch and the row and file limits of a load |
| RWB-PLT-E1043-CON | The reference-data client library (DP-07): the state code list and the working-day calendar with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-42 reaches the three operations through it, one hop each |
| RWB-P3-E1042-CON | The parameters contract of `rwb-case` (DP-06): the value of the four-eyes switch and of the row and file limits. The parameter rows carrying them are Not specified in the source documents (GAP-2275; ASM-3760). A C dependency, so it never blocks the build |
| RWB-P3-E1043-CON | The reference-data contract of `rwb-case` (DP-07): the state code list and the working-day calendar with the version in force. The list codes are Not specified in the source documents (GAP-2275; ASM-3761) |
| RWB-P3-E1028-CON | The service-level and timer contract of `rwb-case`: the load of an accepted file, the approval that puts a version in force, the read of a load and the effect on each running timer. Its operations and paths are Not specified in the source documents (GAP-2275; ASM-3757), and the shape of the effect list is Not specified either (GAP-2275; ASM-3759) |

Business preconditions carried from RWB-AD-015:

- The service levels are rows of a versioned table: state code, allowed working days, warning point, escalation point, escalation role, the recompute instruction and a valid-from date. No working day, warning point, escalation point or role is written in code (REQ-CWC-011; DL22).
- The legacy test values are copied, not chosen: 10 working days for state LIT_PACK with a warning at 8. They are this story's fixture and not a business rule of the release.
- The loader holds the load right as RW-COE, and the approver holds the approval right as RW-RISK; the loader is not the approver (legacy permission checks; GAP-2276; ASM-3763).
- The state codes are reference values of `rwb-case` and the escalation roles are `role` rows of `rwb-access`; a row that names neither is refused.
- The clock that reads the values is a durable Temporal timer in `rwb-case`'s `CaseWorkflow`; `rwb-access` runs no workflow, holds no timer and owns no Schedule (Architecture v5 slides 42 and 44).
- The administration screen is SCR-42 Queues and service levels, reached through the gateway-bff composite route. Which service serves which panel of SCR-42 is Not specified in the source documents (GAP-2275; ASM-3762).

### 4. Flow

1. The loader, holding the load right, posts the file to `POST /api/recovery/access/v1/admin/service-level-loads` through the gateway-bff composite route, with the multipart part `file`, the query `validFrom` and an `Idempotency-Key` header.
2. `ServiceLevelLoadController` calls the service's own authorise operation (`POST /api/recovery/access/v1/authorise`) with the caller's role. A caller without the load right is refused 403 with MSG-P4-002 and no file is read (BR8).
3. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`; a key already answered replays that first answer and stores nothing (BR9, AC7).
4. `ParameterReader` reads the four-eyes switch and the row and file limits through the parameters contract of DP-06 with the version in force on the load date. No value is a constant (BR1).
5. `FileParser` reads the header row and one row per service level; a file that cannot be opened, or whose header lacks a required column, is refused 422 with MSG-GEN-001 naming the column (BR2, AC3).
6. `RowGate` checks every row before anything is sent: the state code must be a value of the reference list read through DP-07; the allowed working days, the warning point and the escalation point must be whole numbers of working days on the calendar in force; the warning point must be strictly before the allowed days; the escalation point must be at or before the allowed days; the escalation role must be a `role` row; the recompute instruction must be a Yes or a No; and `valid_from` must be a date (BR3).
7. A row that fails any check refuses the whole file with 422 and MSG-GEN-001 naming the row and the field, with every refused row listed; no call is made to `rwb-case`, no load id is issued and nothing is in force (BR2, AC3).
8. `ParameterReader` checks the row count and the file size against the limits of step 4, so a file over the limit is refused 422 with MSG-GEN-001 naming the limit and its parameter row (BR1, AC3).
9. `ServiceLevelClient` hands the accepted file, unchanged, to the service-level contract of `rwb-case` as one hop with a 2 s timeout. `rwb-case` stores the version and answers the load id, the row count, the version label, `validFrom`, the state `LOADED` and the author reference (BR4; GAP-2275; ASM-3757).
10. `DecisionRecordWriter` writes the load entry through the library of DP-03, then this story answers 201 with `loadId`, `rowCount`, `versionLabel`, `validFrom`, `state` and the `Location` of the read. A record that cannot be written stops the load: 503 with MSG-P7-003 and nothing is in force (BR5, AC5).
11. The approver, holding the approval right, posts `POST /api/recovery/access/v1/admin/service-level-loads/{loadId}/approve` with the decision and an `Idempotency-Key`; a caller without the approval right is refused 403 with MSG-P4-002 (BR8).
12. `FourEyesGate` compares the approver's reference with the author reference `rwb-case` answered for the load. Equal references are refused 409 with MSG-P7-002 and the load stays `LOADED` (BR6, AC4).
13. `DecisionRecordWriter` writes the approval entry first, and only then does `ServiceLevelClient` ask `rwb-case` to put the version in force from its valid-from date. A record that cannot be written stops the approval: 503 with MSG-P7-003, no promotion call and no running timer moved (BR5, AC5).
14. `rwb-case` promotes the version and answers the state and the effect list: for every timer running in a state the file covers, its timer id, its start, its due date and whether it keeps that due date or is recomputed by the instruction of the accepted row (BR7, AC2, AC6).
15. `GET /api/recovery/access/v1/admin/service-level-loads/{loadId}` calls the read of the same contract with the read right and answers the same fields, so the screen is reopened without a second approval (BR7, AC6).
16. Where `rwb-case` cannot be reached or answers beyond the 2 s budget, the call answers 503 and nothing is reported as loaded or approved; a retry with the same `Idempotency-Key` cannot create a second version (BR9, X7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The file part, `validFrom` or the `Idempotency-Key` is empty | 422 (400 for the header); no file is read and no call is made | MSG-GEN-001 | AC3 |
| X2 | The file cannot be opened, or its header lacks a required column | 422 naming the column or the part that could not be read | MSG-GEN-001 | AC3 |
| X3 | A row gives a working-day calendar reference in place of a whole count, or a value that is not a whole number | 422 naming the row and the field; nothing is forwarded | MSG-GEN-001 | AC3 |
| X4 | A row sets the warning point at or after the allowed days, or the escalation point after the allowed days | 422 naming the row and the field; nothing is forwarded | MSG-GEN-001 | AC3 |
| X5 | A row names a state code that is not a reference value, or an escalation role that is not a `role` row | 422 naming the row and the field; nothing is forwarded | MSG-GEN-001 | AC3 |
| X6 | The file carries more rows or is larger than the limit in force | 422 naming the limit and its parameter row | MSG-GEN-001 | AC3 |
| X7 | `rwb-case` does not answer inside 2 s, or the connection fails | 503; nothing is reported as loaded or approved, and a retry with the same key creates no second version | MSG-P7-003 | AC7 |
| X8 | The caller holds no load right, no approval right or no read right | 403; no file is read and nothing about the load is answerable | MSG-P4-002 | AC4 |
| X9 | The approver is the author of the load | 409; the load stays `LOADED` and is not in force | MSG-P7-002 | AC4 |
| X10 | The decision-record entry of a load or of an approval cannot be written | The action is stopped: 503, the load stays `LOADED`, no promotion call and no running timer changes | MSG-P7-003 | AC5 |

No exception path of this story changes a case, a task, a queue or a timer: the clock, the escalation signal and the pause of a stage clock are `rwb-case`'s and are reached only through its contract (DP-01).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD015-CON, the decision-record library, the parameters and reference-data libraries and the platform composite route; `rwb-case` is consumed through its contract and its fake, and no case or timer table is read or written |
| Negotiable | The column names and order of the file, the wording of each refusal and the field list of the SCR-42 panel are settled with the reference-data community and the case service owner; the three operations, the four eyes, the record-before-answer rule and the effect list are fixed |
| Valuable | One ingest that refuses a file with one bad row before anything is handed over, one four-eyes approval, and one answer naming what happened to every running timer |
| Estimable | One controller, one parser, one row gate, one four-eyes gate, one client for three case-service operations, one decision-record writer, one parameter reader and one reference-list reader, with their tests |
| Small | Fits two weeks with its tests; it creates no table of its own beyond the platform library's, starts no workflow and publishes no event of its own |
| Testable | Each owned criterion has a test case in section 16, and the `rwb-case` side is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Configure service levels and timers

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given the service level file is the multipart part file whose columns are state code, allowed working days, warning point, escalation point, escalation role, recompute instruction and valid_from, with the exact names and order Not specified in the source documents (GAP-2275; ASM-3758)
    Given the state code list and the working-day calendar are reference data of rwb-case in force on the run date
    Given until the timer projection fields and the service level file layout are published (GAP-0439), the harness holds the state code, allowed working days, warning point and valid_from as fixture data and reads each running timer as expires_at, warn_at, status and rule version
    Given test user "U-7125" holds RW-COE with the load right
    Given test user "U-7170" holds RW-RISK with the approval right
    Given test user "U-7190" holds RW-AUDIT with the read right only

  Scenario: AC1 Service level loaded (legacy RWB-AD-015 AC1)
    Given the rwb-case contract mock returns a service level of 10 working days for state LIT_PACK with a warning at 8, stored as version "SL-2027.01"
    Given a service level of 10 working days for state LIT_PACK with a warning at 8
    When it is approved
    Then new timers in that state use the values

  Scenario: AC2 Running timers (legacy RWB-AD-015 AC2)
    Given the rwb-case contract mock returns timer "T-9001" of a case in state LIT_PACK, started 2026-12-01 09:00 with due date 2026-12-15 09:00 and the outcome "kept"
    Given a timer already running
    When a new version takes effect
    Then the running timer keeps its due date unless the rule says to recompute

  Scenario: AC3 A file with one bad row is refused as a whole with the row and the field named (new, D-RCV-60)
    Given "U-7125" posts a service level file of 12 rows for validFrom 2027-01-01 in which row 7 gives the allowed working days as a working-day calendar reference instead of a whole number, row 9 sets the warning point at 11 against 10 allowed days, row 10 sets the escalation point at 12 against 10 allowed days, row 11 names the escalation role "RW-NOT-A-ROLE" and row 12 names the state code "NOT_A_STATE"
    When POST /api/recovery/access/v1/admin/service-level-loads is called
    Then the response is 422 with message MSG-GEN-001
    Then the answer lists every refused row with its field, row 7 first, and names row 7 and the working-day field
    Then the rwb-case contract fake records no call and no load id is issued
    Then the same file with those five rows corrected loads, so the refusal changed nothing

  Scenario: AC4 The loader cannot approve the load they made (new, D-RCV-60)
    Given "U-7125" loads the accepted file of 12 rows and the rwb-case contract mock returns load "SL-000042" in state "LOADED" with author reference "U-7125"
    When "U-7125" posts an approval for load "SL-000042"
    Then the response is 409 with message MSG-P7-002 and the load stays "LOADED"
    Then the rwb-case contract fake records no approval call
    When "U-7170" holding RW-RISK with the approval right approves the same load
    Then the response is 200 with state "APPROVED"
    Then "U-7190", who holds the read right only, is refused the approval with 403 and MSG-P4-002

  Scenario: AC5 A load that cannot be recorded is not approved (new, D-RCV-60)
    Given "U-7170" holding RW-RISK approves load "SL-000042" in state "LOADED"
    Given the decision-record fake is set to fail every write in this run
    When the approval is posted
    Then the response is 503 with message MSG-P7-003
    Then the load stays "LOADED" and is not in force
    Then the rwb-case contract fake records no promotion call, so no running timer changed
    Then when the fake is repaired the same approval answers 200 with state "APPROVED"

  Scenario: AC6 The answer and the read name the load and the effect on each running timer (new, D-RCV-60)
    Given the rwb-case contract mock returns load "SL-000042" with 12 rows, version "SL-2027.01", validFrom 2027-01-01 and state "APPROVED", with two running timers in states the file covers: "T-9001" started 2026-12-01 09:00 with due date 2026-12-15 09:00 kept, and "T-9002" started 2026-12-02 09:00 recomputed to due date 2026-12-20 09:00
    When "U-7170" approves load "SL-000042" and "U-7190" then reads it with GET /api/recovery/access/v1/admin/service-level-loads/SL-000042
    Then both answers carry loadId "SL-000042", rowCount 12, versionLabel "SL-2027.01", validFrom 2027-01-01 and state "APPROVED"
    Then both answers carry the effect list with "T-9001" kept at 2026-12-15 09:00 and "T-9002" recomputed to 2026-12-20 09:00
    Then neither answer carries a party value, a customer identifier or a personal field

  Scenario: AC7 One Idempotency-Key answers one load (new, D-RCV-60)
    Given "U-7125" posts the accepted 12-row file with Idempotency-Key "k-015-1"
    When the same file is posted again with Idempotency-Key "k-015-1"
    Then the first response is 201 with loadId "SL-000042", rowCount 12, versionLabel "SL-2027.01", validFrom 2027-01-01 and state "LOADED"
    Then the second response repeats that answer and the rwb-case contract fake records one call
    Then no second version is stored

  Scenario: AC8 The limits and the four-eyes switch are read from parameter rows, not written in code (new, D-RCV-60)
    Given the four-eyes switch and the row and file limits are parameter rows read through DP-06
    When the service level file is checked and a load is recorded
    Then no working day, warning point, escalation point, role or limit is taken from code and the load entry holds only the action, load id, state codes, row count, version label, validFrom and caller reference

  Scenario: AC9 A call without a token or for a load id the case contract does not hold is refused with 401 or 404 (new, D-RCV-60)
    Given a caller presents no token
    When POST /api/recovery/access/v1/admin/service-level-loads is called
    Then the response is 401 and nothing is loaded
    Given a load id that the rwb-case contract fake does not hold
    When GET /api/recovery/access/v1/admin/service-level-loads/{loadId} is called with that load id
    Then the response is 404 with message Not specified in the source documents (NEWAC-RWB-P4-AD015-APP-AC9)
```

AC1 and AC2 are the legacy criteria copied with their origin tag and proved against the contract mock: AC1 through the version the case service stores, AC2 through the due date and the outcome it answers per running timer. AC3 to AC9 are the new criteria of the split and test only this service's behaviour: the whole-file gate, the separation of duty, the record-before-answer rule, the answer shape, one key per load, the limits held as parameter rows and the refused calls.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The service levels are data: the state code and the calendar are reference values read through DP-07, and the four-eyes switch and the row and file limits are parameter rows read through DP-06. No working day, warning point, escalation point, role or limit is written in code | REQ-CWC-011; DL22; DP-06; DP-07 |
| BR2 | The file is validated as a whole before anything is handed over: one bad row refuses the whole file with 422 and MSG-GEN-001 naming the row and the field, nothing is stored and no load id is issued | RWB-AD-015 AC1; GAP-2275; ASM-3758 |
| BR3 | A row is refused when a value is not a whole number of working days, when a calendar reference stands in place of a count, when the warning point is not strictly before the allowed days, when the escalation point is after the allowed days, when the state code is not a reference value, when the escalation role is not a `role` row, or when a required field is empty | FSD P4 A2.17.3.1 VR-P4-017-1; GAP-2275; ASM-3758; ASM-3761 |
| BR4 | The accepted file is handed to the service-level contract of `rwb-case` in one hop with a 2 s timeout; this service stores no service level, no version and no timer, and answers what that contract answers | DP-11; DP-01; GAP-2275; ASM-3757 |
| BR5 | The decision-record entry is written before the acknowledgement, and the approval's entry before the version is put in force; a write that fails stops the action with 503 and MSG-P7-003, so nothing is approved and no running timer moves | DP-03; REQ-DRI-005; legacy RWB-AD-015 TC-AD-015-04 |
| BR6 | The loader cannot approve: the approver's reference must differ from the author reference of the load, and an approval by the author is refused with 409 and MSG-P7-002 while the load stays `LOADED` | FSD P4 A2.4.4.3 AC-EXC-P4-004-03; Temporal and Drools Design slide 15; ASM-3764 |
| BR7 | Whether a timer already running keeps its due date or is recomputed is decided by the recompute instruction of the accepted row and answered per timer by `rwb-case`; this story computes no date, moves no timer and starts none | RWB-AD-015 AC2; GAP-2275; ASM-3759 |
| BR8 | Only a caller holding the load right may load, the approval right may approve and the read right may read; a refused caller learns nothing about the file or the load | TSD P4 v3 API-P4-005 (Reference data C) and API-P4-006 (Reference data A), which replace the legacy Rules and parameters C and A of RWB-AD-015 permission checks; ASM-3763 |
| BR9 | One `Idempotency-Key` answers one load or one approval: a repeated post replays the first answer and `rwb-case` is called once | TSD P4 v3 API-P4-005 and API-P4-006; DP-09 |
| BR10 | No personal data enters the file check, the answer, the effect list or the record: state codes, counts, dates, a version label, a load id, timer identifiers and caller references only | Template and Rules §R7.2 s17; NFR-039; NFR-040 |
| BR11 | The record of a load names the action, the load id, the state codes of the file, the row count, the version label, `validFrom` and the caller reference; the record of an approval adds the approver reference and the outcome. Neither carries a timer value or a case fact | DP-03; REQ-DRI-011 |

Why the rules hold in `rwb-access`:

- BR2 and BR3 are one pass over the parsed file before the client is called; the gate collects every refused row with its field and the controller maps the collection to one 422, the first refused row first, so nothing is sent and nothing can be stored.
- BR4 is the absence of a service-level table in `rwb_access`: no timer, no version and no state row is created here, and a test asserts that no statement of this story names `timer`, `recovery_case`, `queue` or `task`.
- BR5 is a deliberate order, so a failure leaves the version unapproved rather than promoted and unrecorded.
- BR6 compares two references, never a personal value; BR8 is the authorise call before the body is read, so a caller without the right cannot even spend the parse.

### 9. State transitions

This service holds no version state of its own: the states are those of the load in `rwb-case`, answered unchanged.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A file is posted and passes the header and row gates | `rwb-case` stores the version | `LOADED`, with a load id and a version label |
| (none) | A file is posted and one row fails a check | The gate refuses before the call | No load, no state; the caller is answered 422 |
| `LOADED` | Approval by the approval right, approver not the author | The record of the approval commits | `APPROVED`, in force from its valid-from date |
| `LOADED` | Approval by the author of the load | The references are equal | Unchanged; 409 with MSG-P7-002 |
| `LOADED` | The decision record of the approval cannot be written | The write fails | Unchanged; 503 with MSG-P7-003 and no promotion call |
| `APPROVED` | The version reaches its valid-from date | None | In force for new timers in the states it names |
| In force | A later version is approved with a later valid-from date | None | `SUPERSEDED`, readable for its own dates |

| Command | Condition | Outcome |
|---|---|---|
| Load a file | The load right, a valid file, an unused or repeated `Idempotency-Key` | 201 with the load in `LOADED`, or the stored answer replayed |
| Load a file | A bad row, a missing column or a limit exceeded | 422 with MSG-GEN-001; nothing forwarded and no load id |
| Approve a load | The approval right, approver not the author, the record written | 200 with `APPROVED` and the effect list |
| Approve a load | The approver is the author | 409 with MSG-P7-002; the load stays `LOADED` |
| Read a load | The read right | 200 with the fields and the effect list |

Everything after `APPROVED` belongs to `rwb-case`, which holds the version and starts the clock; no transition here moves a case, changes a queue, pauses a timer or closes an escalation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM Reference data administrator | Prepares and loads a service-level file and reads a load, where the load right is held; it approves nothing |
| RW-COE Center of excellence analyst | Holds the load right (RWB-AD-015 permission checks): loads a service-level file and reads it; an approval by the analyst who loaded it is refused by the four-eyes rule |
| RW-RISK Risk and model risk officer | Holds the approval right (RWB-AD-015 permission checks): approves a loaded version, which puts it in force from its valid-from date. It loads nothing |
| RW-AUDIT Internal audit | Holds the read right: reads a load, its state, its effect on the running timers and the decision-record entries of both steps |
| RW-PLATADM, RW-SECADM | Read a load; they load and approve nothing here |
| The case roles | Hold the read right and may read a load; a working day, a warning point or an escalation point is changed by nobody but the two roles above |
| The `rwb-case` service identity | Answers the three consumed operations; it calls nothing of this story |
| `rwb-access` itself | Reads `role`, `permission` and its own `v_ace_iam_group` ACE view, and writes the idempotency and decision-record rows of a step |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 for an absent right and MSG-P4-001 for an absent session; the four-eyes refusal is 409 with MSG-P7-002. Which right letters govern the gate is a recorded conflict between the legacy permission table and TSD P4 v3 (GAP-2276; ASM-3763). The database login is the per-service login of the service baseline (DP-02) and belongs to RWB-P4-AD015-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| (ACE view) | `v_ace_iam_group` (ACE `iam_group`, RWB-ACE-001) | entra_group of the calling staff reference | Read through the service's own ACE view (DP-05) |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a load and of an approval | Write (DP-09) |
| (decision record) | outbox and record objects of the local library in `rwb_access` | the load entry and the approval entry of DP-03 | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | the state code list and the working-day calendar, read through DP-07 | Read through the contract; the table is P3's |
| DF-REF-001 to DF-REF-015 | `rule_row` of `rwb_case` | the recompute instruction of a state move (`timer_spec`, DF-REF-011) as the contract reports it | Read through the contract; the table is P3's |
| DF-WRK-027 to DF-WRK-036 | `timer` of `rwb_case` | the timer id, its start, its due date and its status, carried in the effect list | Read through the contract only |

No row of `timer`, `recovery_case`, `queue` or `task` is read or written by a statement of this story: those tables are `rwb-case`'s, the clock is a Temporal timer inside its workflow, and the only facts of them that enter this service are the identifiers and dates the contract returns (DP-01). No row of `parameter_catalog`, `parameter_value`, `reference_row` or `reference_version` is written: parameters and reference data are P3's under DP-06 and DP-07. The service-level file is not stored here; it travels in the request to `rwb-case`, which keeps it with the version it stores. Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD P4 v3, and no personal data enters the file check, the answer, the effect list or the record.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/service-level-loads` | P4 `rwb-access` | multipart `file` (the service-level rows) and query `validFrom` | `ServiceLevelLoad`: `loadId`, `rowCount`, `versionLabel`, `validFrom`, `state`, with `Location` of the read | 400, 401 (MSG-P4-001); 403 (MSG-P4-002); 409; 422 (MSG-GEN-001); 503 (MSG-P7-003) | The load right | `Idempotency-Key` header; the stored answer is replayed |
| POST | `/api/recovery/access/v1/admin/service-level-loads/{loadId}/approve` | P4 `rwb-access` | form field `decision` | `ServiceLevelLoad` with `state` `APPROVED` and the `effects[]` list | 401; 403 (MSG-P4-002); 404; 409 the approver is the author (MSG-P7-002); 503 (MSG-P7-003) | The approval right | `Idempotency-Key` header |
| GET | `/api/recovery/access/v1/admin/service-level-loads/{loadId}` | P4 `rwb-access` | None | The same fields and the `effects[]` list | 401; 403 (MSG-P4-002); 404 unknown load; 503 (MSG-P7-003) | The read right | Not applicable |

All three sit under the base `/api/recovery/access/v1` of DP-13. They are this service's administration gate for a service-level version; the version, its state and the timers are `rwb-case`'s. The API Specification v5 and TSD P4 v3 declare no `rwb-access` path for this gate — the inventory there is the general reference-load pair API-P4-005 and API-P4-006 — so the three paths above are new work off that inventory (GAP-2275; ASM-3757).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/service-levels` | P3 `rwb-case` | The accepted file and `validFrom`; answers the load id, row count, version label, `validFrom`, the state `LOADED` and the author reference |
| POST | `/api/recovery/case/v1/admin/service-levels/{loadId}/approve` | P3 `rwb-case` | Puts the version in force from its valid-from date and answers the state and the effect on each running timer |
| GET | `/api/recovery/case/v1/admin/service-levels/{loadId}` | P3 `rwb-case` | The load, its state and the effect list, for the read of this service |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (this service) | The load, approval or read check behind all three operations, under the guard library of DP-08 |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The four-eyes switch and the row and file limits of a load, with the version in force (DP-06) |

The three `rwb-case` paths and the parameters path are Not specified in the source documents (GAP-2275; ASM-3757; ASM-3760): they are proposed names on the published bases of RWB-P3-E1028-CON and RWB-P3-E1042-CON and are fixed at the contract review. The parameters read is a C dependency and never blocks the build; the service-level operations are stubbed by the fake of 12.8.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the load id | the hash-chained entry of a load or of an approval: action, load id, state codes, row count, version label, `validFrom`, caller reference and outcome |

Nothing is published on `rwb.access.events.v1`. That topic carries `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1`, and a service-level load changes neither an access policy nor a delegation limit. The breach event and the retired `TimerDue` are `rwb-case`'s and are not published here. No payload carries a personal value and none carries a timer value.

#### 12.4 Events consumed

None. The approval is a command of the screen, and the effect on the running timers is answered by the approval's own call and by the read. The clock's signals stay inside `rwb-case`'s workflow.

#### 12.5 Workflows and activities

None. The clock this story loads values for is a durable Temporal timer inside `rwb-case`'s `CaseWorkflow`; this story registers no workflow and no activity on the `rwb-access` queue, starts none and signals none (Architecture v5 slides 42 and 44; Temporal and Drools Design slide 13). The escalation is that signal and not a job: the five-minute timer check and the `TimerDue` event are retired, and no Schedule replaces them here.

#### 12.6 Schedules

None. This service owns one Schedule, the access review list (JOB-18), and its story is RWB-P4-AD008-APP. A service-level load is request-driven and nothing about the clock is scheduled in `rwb-access`.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's role, and the escalation role each row names |
| `permission` | P4 (`rwb_access`) | Read only: the load, approval or read letter of the caller's role |
| `idempotency_key` | PLT library, created in `rwb_access` | The stored request and answer of a load and of an approval (DP-09) |
| `outbox_event`, `processed_event` | PLT library, through the decision-record library of DP-03 | The record row of a load or an approval and its `DecisionRecorded` message; no inbox row, because no event is consumed |

`timer`, `recovery_case`, `queue`, `task`, `lov_value`, `rule_row` and the `parameter_*` and `reference_*` tables are P3's, reached through the `rwb-case` contracts only, never by a schema read and never by a write, and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case service-level WireMock | RWB-P3-E1028-CON | `POST /admin/service-levels` answering load "SL-000042", 12 rows, version "SL-2027.01", `validFrom` 2027-01-01, state `LOADED`, author reference "U-7125"; the approved state; a 503 and a timeout for X7 |
| rwb-case approval and read WireMock | RWB-P3-E1028-CON | `POST /admin/service-levels/{loadId}/approve` answering `APPROVED` with "T-9001" kept at 2026-12-15 09:00 and "T-9002" recomputed to 2026-12-20 09:00, and a 409 when the version is no longer `LOADED`; `GET /admin/service-levels/{loadId}` answering the same, and a 404 for an unknown load |
| reference-data fake | RWB-P3-E1043-CON | The state code list with LIT_PACK and the other states of the fixture, the working-day calendar in force on 15 December 2026, and an unknown state code for X5 |
| parameters fake | RWB-P3-E1042-CON | The four-eyes switch on, the row limit 500 and the file limit 2 MB, with the version in force on 15 December 2026 |
| decision-record fake | RWB-PLT-E1027-CON | The record append and the publish on `rwb.decision-record.v1`, including the forced failure of AC5 |
| authorise and guard fake | RWB-P4-AD015-CON, RWB-P4-E1037-CON | A granted answer for the load and approval rights, and a refused answer with MSG-P4-002 for a role without the letter |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The SCR-42 route that calls the three operations, one hop each, and merges the service-level panel with the queue panel |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3 new; consumed 5 | Base `/api/recovery/access/v1`; three `rwb-case` service-level operations, the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 0 own; 1 record type; consumed 0 | `DecisionRecorded` through the DP-03 library on `rwb.decision-record.v1`; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | The clock is `rwb-case`'s durable timer in `CaseWorkflow`; this story registers nothing |
| File | One in, none out | The multipart service-level file is parsed and validated here and forwarded unchanged to `rwb-case` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/servicelevel`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the direct write to the recovery service-level table from the administration screen (DP-01 and DP-13: the store is `rwb-case`'s, reached through its contract under this service's own base), the `casewf.config` read of the working-day values (DP-06: parameter rows with the version in force), the hard-coded state and role lists of the screen (DP-07: reference values through the contract, and `role` rows in this schema), the in-process approval call (DP-11: one hop, 2 s), the decision-log write inside the service (DP-03: the local library and the shared topic) and the ace-web screen (DP-19: the SCR-42 composite route).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ServiceLevelLoadController | Controller | The three operations: multipart and form validation, the authorise call before the body is read, RFC 9457 error mapping, `Location` on a created load |
| FileParser | Service | Opens the service-level file and returns the header and one row per service level |
| RowGate | Service | The whole-file validation of BR3; collects every refusal with its row and field |
| FourEyesGate | Service | Compares the approver reference with the author reference of the load and refuses the same person |
| ServiceLevelClient | Client | The three `rwb-case` operations, one hop and 2 s, forwarding the `Idempotency-Key`, mapping a 404 and a timeout |
| PermissionReader | Service | The `role` and `permission` rows of the caller in `rwb_access`, behind the authorise operation |
| StaffGroupReader | Service | The caller's staff reference and Entra group through `v_ace_iam_group`, with no personal field read |
| ReferenceListReader | Service | The state code list and the working-day calendar through DP-07, with the version in force |
| ParameterReader | Service | The four-eyes switch and the row and file limits through DP-06 |
| DecisionRecordWriter | Service | The load and approval entries through DP-03, written before the acknowledgement and, for the approval, before the promotion call |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations.** This story creates no table of its own: the `idempotency_key` table and the outbox and inbox objects are the platform library's, created in `rwb_access` by the service's own DB story in the per-service Flyway sequence of DP-15. No service-level table, timer table or version table is created here. No write statement touches `role` or `permission`.

**Configuration and reference data.** The four-eyes switch and the row and file limits are parameter rows of `rwb-case` read through DP-06 (RWB-P3-E1042-CON), and the row names are Not specified in the source documents (GAP-2275; ASM-3760). The state code list and the working-day calendar are read with the version in force through DP-07 (GAP-2275; ASM-3761). The escalation roles are `role` rows of `rwb_access`, so a new escalation point is a row and no build.

**Build steps**

1. `FileParser` and the header check over a synthetic 12-row file, with tests for a missing column and for a file that is not the expected shape.
2. `RowGate` with the refusals of BR3; the AC3 test, including the row and field names and the proof that the client is not called.
3. `ReferenceListReader` and `PermissionReader` over the two contracts, with a test that a new state code and a new escalation role are data with no build.
4. `ServiceLevelClient` against the `rwb-case` fake: the `LOADED` answer of AC1 and AC7, the approval with the effect list of AC2 and AC6, and the 503 of X7.
5. `FourEyesGate` and the order of the approval: the AC4 refusal and the AC5 forced failure proving that no promotion call is made when the record fails.
6. `DecisionRecordWriter` and `IdempotencyStore`: the payload of BR11, the replay of AC7 and the proof that the fake records one call for two posts.
7. The authorise path before the body read, the read-only refusal, and the composite-route run of the SCR-42 states through the gateway-bff fake.

**Feature switch.** None of this slice's own: a load that is silently switched off would leave every clock on the values of the last approved version while the screen said nothing, which is the failure the whole-file gate and the four eyes exist to prevent. The service-level feature flag of the service baseline governs the administration surface.

**Done when.** The tests in section 16 pass; a valid file loads to `LOADED` with its version label and `validFrom`; a file with one bad row is refused as a whole with 422 naming the row and the field and the case service is not called; the loader cannot approve and the approval role can; an approval whose record cannot be written is refused with 503 and puts nothing in force; and the answer names, per running timer, the due date and whether it was kept or recomputed.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required part, field or column is empty, a value is not a whole number of working days, a calendar reference stands in place of a count, the warning or escalation order is broken, the state code or the escalation role is unknown, or a limit is exceeded | Enter {field}. | This story, on the load; the detail names every refused row and its field |
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all three operations |
| MSG-P4-002 | The caller holds no load, approval or read right | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-P7-002 | The approver is the author of the load | Wording Not specified in the source documents (GAP-2275; ASM-3764) | This story, on the four-eyes refusal |
| MSG-P7-003 | The decision record cannot be written, or the case service cannot be reached inside 2 s | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story on a record failure; `rwb-case` on a 503, passed through unchanged |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 422 of a refused file carries the refused rows and their fields in `detail`, so the screen marks each row of the upload without a second call.

### 15. Screens and states

SCR-42 Queues and service levels is the administration screen, served through the gateway-bff composite route of DP-19, which calls the queue operations of `rwb-case` and the three operations of this service in parallel, one hop each, and merges the answers. This story serves the service-level panel and builds no screen surface of its own; which of the two services serves which panel is Not specified in the source documents (GAP-2275; ASM-3762).

| Screen | State | What the screen shows |
|---|---|---|
| SCR-42 Queues and service levels | Empty | Not specified in the source documents (CG-ALL-4803) |
| SCR-42 Queues and service levels | Refused | The 422 with every refused row and its field, so the analyst corrects the file; nothing was loaded and nothing is in force |
| SCR-42 Queues and service levels | Loaded, waiting for approval | The load id, row count, version label and `validFrom`, and the statement that approval belongs to the approval role |
| SCR-42 Queues and service levels | Approved | The state `APPROVED`, the valid-from date and the effect list, each running timer with its start, its due date and whether it was kept or recomputed |
| SCR-42 Queues and service levels | Read | The same fields and effect list on a later visit by a role holding the read right |
| SCR-42 Queues and service levels | Loading, error, no access | Not specified in the source documents (CG-ALL-4803) |
| SCR-39 Rules and parameters | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-4802) |

The legacy story also listed SCR-39 Rules and parameters with the states Versions, load and approval. The rule-version half of that screen is RWB-P4-AD011-APP's, and the approval letter is the same in both; this story serves no rule-version field. The timers a load affects are shown on the case record view by the case service's own stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-015-01 | AC1, BR4 | Contract | The `rwb-case` fake: a service level of 10 working days for state LIT_PACK with a warning at 8, stored as version "SL-2027.01", and the timers it starts reading those values |
| TC-AD-015-02 | AC2, BR7 | Contract | The `rwb-case` fake: timer "T-9001" started 2026-12-01 09:00 with due date 2026-12-15 09:00, kept with outcome `kept`; a second timer recomputed |
| TC-AD-015-03 | AC4, BR6, BR8 | Component | "U-7125" loads and tries to approve the same load: 409 with MSG-P7-002 and the load stays `LOADED`; the approval role approves; a caller with the read right only is refused 403 with MSG-P4-002 |
| TC-AD-015-04 | AC5, BR5 | Component | The decision-record fake forced to fail: the approval answers 503 with MSG-P7-003, the load stays `LOADED`, no promotion call is recorded and no timer moves |
| TC-AD-015-05 | AC3, BR2, BR3 | Component | A 12-row file with a calendar reference at row 7, the warning point at 11 at row 9, the escalation point at 12 at row 10, an unknown role at row 11 and an unknown state code at row 12; 422 naming each row and field; the case fake records no call |
| TC-AD-015-06 | AC6, BR7, BR10 | Contract | The approved load "SL-000042" with 12 rows, version "SL-2027.01", `validFrom` 2027-01-01 and the two-timer effect list, answered the same by the approval and by the read |
| TC-AD-015-07 | AC7, BR9 | Component | The same file twice with `Idempotency-Key` "k-015-1"; one case-service call, one version, the first answer replayed |
| TC-AD-015-08 | BR4 | Component | Every table named in §11 and §12.7 checked: a scan of each statement of this story finds no reference to `timer`, `recovery_case`, `queue`, `task`, `lov_value`, `rule_row` or a `parameter_*` or `reference_*` table, and no foreign key crosses a schema |
| TC-AD-015-09 | AC8, BR1, BR11 | Component | The four-eyes switch and the row and file limits read from parameter rows, not from code; the load entry checked for the action, load id, state codes, row count, version label, `validFrom` and caller reference, with no timer value or case fact |
| TC-AD-015-10 | AC9 | Contract | A call without a token answers 401 with nothing loaded; a load id the case contract fake does not hold answers 404 |

TC-AD-015-01 to TC-AD-015-04 are the legacy test cases under their existing ids; TC-AD-015-05 to TC-AD-015-07 are added for this story. The legacy level System maps to Contract and Access to Component, and the record-failure test (legacy Principle 5) is Component. The integration copies of these test cases end in `-ITG` and belong to RWB-ITG-AD015-ITG, the integration story the plan splits from this legacy key; no `-ITG` copy is written here.

### 17. Guardrails

- No business value in code: the working days, the warning point, the escalation point, the escalation roles, the state codes, the four-eyes switch and the row and file limits are data with versions (BR1). A test proves that a new state code or a new escalation role needs no build.
- No personal data anywhere: the file carries state codes, counts and dates, the answer carries identifiers and dates, and the record carries references. No name, no e-mail address and no party value appears in a fixture, a log or a prompt.
- No read of another service's tables (DP-01): `timer`, `recovery_case`, `queue`, `task`, `lov_value`, `rule_row` and the `parameter_*` and `reference_*` tables are `rwb-case`'s, and no foreign key crosses a schema.
- ACE data only through the owner's contract or its own `v_ace_*` views: the caller's group is read through `v_ace_iam_group` (DP-05), which carries no personal field.
- One writer for the clock: this story starts no timer, pauses none, closes no escalation and registers no workflow. A version that is not approved changes nothing.
- No record, no change: a load is acknowledged only after its record commits, and an approval puts a version in force only after its record commits (BR5).
- Refuse the file, not the row: the gate is whole-file on purpose, because a partially applied service level would leave states on different versions (BR2).
- One key, one load: the `Idempotency-Key` of a load and of an approval is stored with the answer, so a retry after a timeout cannot create a second version (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels per queue and status, warning thresholds and escalation targets are held as data, and a breach raises an event without moving the case | Program: case and workflow | ADM-01 | All recovery processes | BR1, BR3, BR7 | TC-AD-015-01, TC-AD-015-02, TC-AD-015-05, TC-AD-015-09 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Program: decision and rules | ADM-01 | All recovery processes | BR5 | TC-AD-015-04 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Program: decision and rules | ADM-01 | All recovery processes | BR1, BR3 | TC-AD-015-05 |
| REQ-DRI-011 | A reference data service holds every versioned table with its valid-from and valid-to dates, author and approver | Program: decision and rules | ADM-01 | All recovery processes | BR6, BR7, BR11 | TC-AD-015-02, TC-AD-015-06, TC-AD-015-09 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the administrator | Program: access and authority | ADM-01 | All recovery processes | BR6, BR8 | TC-AD-015-03 |

| Legacy reference | Where it is kept |
|---|---|
| AC1: a service level of 10 working days for state LIT_PACK with a warning at 8 is approved and new timers use the values | Sections 1, 3, 4, 7, 8, 9, 12.2, 16 |
| AC2: a running timer keeps its due date unless the rule says to recompute | Sections 1, 4, 7, 8, 9, 12.1, 16 |
| The `timer` fields DF-WRK-027 to DF-WRK-036 and the rule-row `timer_spec` | Sections 8, 11, 12.1 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-002, MSG-P7-003 | Section 14, exception paths |
| Screens SCR-42 and SCR-39 and their states | Sections 15, 19 |
| Permission checks of Rules and parameters C for RW-COE and A for RW-RISK | Sections 10, 12.1, 16; GAP-2276 |
| Decision DL22 (open; assumptions ASM-1162, ASM-1304, ASM-2217, ASM-2569) and the rules of the state move | Sections 2, 3, 19 |
| Legacy key RWB-AD-015, story RWB-P4-AD015-APP, contract RWB-P4-AD015-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-001 to DF-REF-015, DF-REF-027 to DF-REF-044, DF-WRK-027 to DF-WRK-036 | Section 11 |

### 19. Out of scope

- The clock itself: the durable Temporal timer inside `rwb-case`'s `CaseWorkflow`, the working-day arithmetic, the warning point, the breach, the escalation signal, the pause of a stage clock under a deviation and the prescription date. They are `rwb-case`'s (RWB-P3-E1028-APP/CON).
- The `timer` and `recovery_case` tables and their migrations, the timer panel of the case record view (RWB-P4-E2015-APP) and the case-side access answers (RWB-P4-E1028-APP).
- The queue panel of SCR-42 and the queue rows behind it: queue, assignment, task and allocation are `rwb-case`'s, and the queue configuration journey is RWB-P4-AD014-APP.
- Drafting the service-level policy, its working-day calendar and its legal periods: they are reference data of `rwb-case` and are read here, never written.
- The rule packages behind the state moves: versioning, approval and rollback of a rule package are `rwb-decision`'s, and the rule-version load journey is RWB-P4-AD011-APP.
- The approval of a reference-data load in general (RWB-P4-AD010-APP) and the delegation-of-authority table (RWB-P4-AD016-APP): this story approves a service-level load only.
- The integration harness of the journey and the end-to-end evidence across the two services: the plan splits RWB-ITG-AD015-ITG from this legacy key, and the `-ITG` copies of the test cases are written there.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: no OPS story is split from this legacy key in the plan.
