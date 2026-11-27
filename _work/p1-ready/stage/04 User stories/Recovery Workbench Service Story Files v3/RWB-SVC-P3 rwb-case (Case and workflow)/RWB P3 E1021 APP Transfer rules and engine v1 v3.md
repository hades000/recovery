# RWB-P3-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1021-APP |
| Work type | APP (App development) |
| Size | Not specified in the source documents (DOR-RWB-P3-E1021-APP-16) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1020-APP, RWB-P3-E1073-APP |
| Depends on (build) | RWB-P3-E1021-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1020-APP, RWB-P3-E1073-APP, RWB-P3-E1028-CON |
| Contract dependencies | RWB-P7-E1027-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P3-E1021-APP-23) |
| Readiness decisions | RD-P1-003, RD-P1-040 |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1021-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-007, FR-P3-012, FR-P3-013, FR-P3-030, FR-P3-031) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: updated the section 16 reference to Recovery Workbench Test Cases v9.

- DailyCaseRun starts only on AceDataReady with `sourceSystem` ALS and `status` COMPLETED; record key `{sourceSystem}:{businessDate}` (RD-P1-003, RD-P1-040).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-021 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 22 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the TRANSFER rule package on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without email**.

Inside `rwb-case` this is the transfer capability of the case service:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The transfer runs as the `transfer` activity of `CaseWorkflow`, reached by the case router from a Kafka event or by the manual REST call `POST /cases/{caseId}/transfer`.
- The TRANSFER rule package is evaluated locally through the embedded Drools kit (DP-04); the package and its versions are authored, approved and promoted in `rwb-decision` (RWB-P3-E1073-APP) and fetched as a model, never read as a table of another service.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-0688; ASM-1235); this story uses the phrase "the rwb-case login (DP-02)" and never the shared monolith login.

The legacy behaviour is unchanged: the same endpoint, request, response, errors and authorization; the same eight triggers; the same TRANSFER package code; the same reason list; the same decision record content.

### 2. Business rationale

A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. This story moves the case by rule when one of eight triggers fires, picks the owner in the receiving queue, ends the old assignment and records the rule ID and package version, and gives the team manager a programmatic transfer with a coded reason before the Epic 2 screens. It meets REQ-CWC-010 and REQ-CWC-016.

Under D-RCV-36 (16 November 2026) the transfer rules are package TRANSFER, evaluated with first-match semantics (T5); the eight triggers arrive as one `TransferTrigger` fact. The manual transfer API does not change; it keeps its endpoint, request, response, errors and authorization. A rule change is a package version loaded and approved through RWB-E1-073, not a release.

The realignment changes the mechanism, not the business rule:

1. The in-process `RuleEvaluator` call of the monolith becomes the embedded Drools kit of DP-04. The kit caches one KieBase per package version, verifies the checksum, refuses a checksum mismatch, and is called only inside the Temporal activity so a replay reuses the recorded answer (the Temporal and Drools design, slide 14).
2. The decision log write becomes the local decision-record library of DP-03 written in the same transaction as the state change, hash-chained to the previous record and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger within 5 minutes. The legacy decision log store of another module is no longer written directly.
3. The trigger listener becomes the case router (Kafka consumer with the inbox of DP-09) that calls `signalWithStart` on `CaseWorkflow` and forwards the trigger to the running stage child. `TimerDue` is no longer a Kafka event: the durable timer inside `CaseWorkflow` raises the same trigger inside the workflow (the timer ruling in the Ownership Map; RWB-P3-E1028-CON provides the timer contract).
4. Reference data (the transfer reason list, the queue and team lists) is read through `rwb-case`'s own reference-data contract of DP-07, never from a foreign table.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E1021-CON | The published `POST /cases/{caseId}/transfer` contract (OpenAPI 3.1) and its fake, so this story builds against a fixed shape |
| RWB-PLT-E1027-CON | The decision-record library and the `rwb.decision-record.v1` topic (DP-03) |
| RWB-PLT-E1072-CON | The embedded Drools kit: KieBase registry, checksum check, `EvaluateRules` activity (DP-04) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and `rwb-case`'s reference-data contract (DP-07) |
| RWB-PLT-TE006-CON | Outbox, inbox and idempotency library (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit: `CaseWorkflow`, activity registration, retry policy, Schedules (DP-10) |
| RWB-PLT-E1047-CON | Topic naming library, so no topic name is typed in code (DP-14) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the case record view (DP-19) |
| RWB-P3-E1020-APP | The assignment engine and the queue structure: lowest-load, named owner, round robin and the cap check |
| RWB-P3-E1073-APP | Package TRANSFER version "TRF-2026.11" loaded, tested, approved by RW-RISK (not the author) and in force from 2026-11-30, with at least 50 passing scenarios |
| RWB-P3-E1028-CON | The timer contract: a timer ends inside the workflow and raises the timer-expired trigger without a Kafka event |

Business preconditions carried from RWB-E1-021:

- Package TRANSFER version "TRF-2026.11" is in force, and each row holds trigger event, condition, target queue code and row order (D-RCV-36 T5).
- The transfer reason list LOV-TRANSFER-REASON holds R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue (DL23), loaded through RWB-E1-043 and read through the reference-data contract.
- Manual transfer callers hold Queue and allocation U (RW-TEAMMGR, RW-CAPACITY). Hold and release callers hold Case record U (for example RW-LITOFF acting on a Legal instruction).
- The case router is running on queue `rwb-case` and the `transfer` activity is deployed by RWB-P3-E1021-OPS.

### 4. Flow

Automated path (one Kafka event, the four steps of the workflow model):

1. Event source: another service writes its fact to its own outbox and publishes it — CaseStateChanged for a stage change, RouteDecided for a route decided (legacy trigger ROUTE_APPROVED), DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored or PaymentMissed. A timer expiry is raised inside `CaseWorkflow` by its durable timer. Each event names the case; no payload carries personal data.
2. Case router: the Kafka consumer of `rwb-case` reads the event into the inbox of DP-09, deduplicates by event ID (R-UNI-40), and calls `signalWithStart` on `CaseWorkflow` with workflow ID equal to the case ID.
3. `CaseWorkflow` forwards the trigger to the running stage child, or handles it itself when no stage child is open; the trigger is one `TransferTrigger` fact built from the event code and the case snapshot.
4. `EvaluateRules` activity: the embedded Drools kit evaluates package TRANSFER for the fact and the business date and returns the first matching rule in row order (T5) with its rule ID and package version. No match means no transfer and no decision record.
5. `transfer` activity: skips an automated transfer when `legal_hold` is true (R-UNI-20) and writes the skip to the log with the rule ID R-UNI-20.
6. `transfer` activity: locks the case by its version, picks the owner in the target queue with the assignment engine, and checks the move is allowed from the case status.
7. `RecordAndApply`, one transaction in `rwb_case`: ends the open assignment, writes the new assignment with reason TRANSFER and the rule ID, updates queue, team and owner, writes the decision record (rule ID, package version, from and to queue and owner, trigger, hash link), and writes the outbox rows for `rwb.case.CaseTransferred.v1` (EV-04) and the decision record.
8. The outbox relay publishes `rwb.case.CaseTransferred.v1` to `rwb.case.events.v1` and `rwb.decision-record.v1` to the shared topic; `rwb-decision` collects the record into the central ledger within 5 minutes.
9. Team manager: calls `POST /cases/{caseId}/transfer` with reason code MANUAL, transfer reason R03 and a target owner or queue; steps 6 and 7 run with reason MANUAL and step 7 writes the decision record with the caller, the reason and the target, and no rule ID. `Idempotency-Key` is required and a repeat with the same key returns the first response.
10. Litigation officer: calls `POST /cases/{caseId}/legal-hold` with action place or lift; the case goes to On hold or back to the status it paused in, and `rwb.case.CaseStateChanged.v1` is published.

The decision record is written before the change takes effect and in the same transaction, so a failure leaves both unchanged (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two transfers reach the same case in the same second | First commits; second refused on the version check and logged as rejected | MSG-GEN-004 | AC3 |
| X2 | Manual transfer without a transfer reason | Refused with 422; nothing changes | MSG-P3-001 | AC6 |
| X3 | Named target owner at the caseload cap | Refused with 422; nothing changes | MSG-P3-002 | AC7 |
| X4 | Transfer of a closed case | Refused with 409 | MSG-P3-005 | AC8 |
| X5 | Decision record write fails | Refused with 503 for a manual call; the activity is retried for a rule transfer; nothing changes | MSG-P7-003 | AC9 |
| X6 | Rule trigger arrives while legal_hold is true | No automated transfer; the skip is logged | None | AC10 |
| X7 | The same event arrives twice | Second ignored by the inbox; one transfer | None | AC11 |
| X8 | No owner below the cap in the target queue | Case placed in the target queue's overflow queue with no owner; team manager told | MSG-P3-011 | AC12 |
| X9 | Hold placed on a case already on hold | Refused with 409 | MSG-P3-005 | AC13 |
| X10 | No TRANSFER rule matches the event | No transfer; no decision record | None | AC14 |
| X11 | A role without Queue and allocation U calls the transfer | Refused with 403 | MSG-P4-002 | AC15 |

A TRANSFER version not in force is refused by the embedded Drools kit before the case is touched (NoPackageInForce, MSG-P3-027). The error is non-retryable in the activity retry policy: the event stays on the inbound topic for redelivery once a version is in force, and no case moves. It is not a per-case exception path.

Two more target-service paths:

- A stale version at commit (zero rows updated) is MSG-GEN-004 and the second transfer is recorded with final call TRANSFER_REJECTED, as in the legacy behaviour.
- Who may override a transfer that a rule or the cap check has refused is Not specified in the source documents (GAP-0689; ASM-1236). This story provides no override path: a refused transfer changes nothing and the caller may retry with another target.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the assignment engine (RWB-P3-E1020-APP), the workflow kit, the Drools kit, the decision-record library, the reference-data contract and the contract of this key; no screen |
| Negotiable | Trigger rows, target queues and the reason list are data |
| Valuable | Removes email hand-offs between the six recovery teams |
| Estimable | One case router path, one activity, one package, two endpoints |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1

  Background:
    Given package TRANSFER version "TRF-2026.11" is in force
    Given queue "LIT-BKK-OFF" belongs to team "LIT-BKK" and role RW-LITOFF with method "LOWEST_LOAD" and cap 150

  Scenario: AC1 Rule-driven transfer (legacy RWB-E1-021 AC1)
    Given case RW-2026-000301 is "IN_PROGRESS" in queue "TDR-BKK-CO" with owner U-21
    Given transfer rule "TRF-007" moves a case to queue "LIT-BKK-OFF" when ROUTE_APPROVED carries route "R4"
    Given the rwb-decision contract mock returns package TRANSFER version "TRF-2026.11" and rule "TRF-007" for route "R4"
    When the route decision approves route "R4" for the case, the route-decided fact committed as rwb.case.CaseStateChanged.v1 (assumed; GAP-0346)
    Then the case is in queue "LIT-BKK-OFF" with owner U-31, the member with the lowest load
    Then the assignment of U-21 has an end time and a new assignment has reason "TRANSFER" and rule ID "TRF-007"
    Then the decision log entry carries rule ID "TRF-007" and package version "TRF-2026.11"

  Scenario: AC2 Manual transfer (legacy RWB-E1-021 AC2)
    Given a team manager of team "TDR-BKK"
    Given the rwb-case reference-data contract mock returns transfer reason "R03" from LOV-TRANSFER-REASON
    When they call the transfer endpoint for case RW-2026-000302 with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the case owner is U-22
    Then the assignment and the decision log entry carry transfer reason "R03"

  Scenario: AC3 One queue only (legacy RWB-E1-021 AC3)
    Given case RW-2026-000303 is in queue "TDR-BKK-CO" with record version 7
    Given the rwb-decision contract mock returns package TRANSFER version "TRF-2026.11" with a matching rule for queue "LIT-BKK-OFF"
    When a rule transfer to "LIT-BKK-OFF" and a manual transfer to "DIL-BKK-CO" arrive in the same second
    Then the case ends in exactly one queue
    Then the system refuses the second transfer with MSG-GEN-004
    Then a decision log entry records the second transfer with final call "TRANSFER_REJECTED"

  Scenario: AC5 Admin API (legacy RWB-E1-021 AC5)
    Given a team manager with Queue and allocation U and a litigation officer with Case record U
    Given the rwb-case reference-data contract mock returns transfer reason "R04" from LOV-TRANSFER-REASON
    When the team manager reassigns case RW-2026-000305 to U-23 with transfer reason "R04"
    When the litigation officer places a legal hold with reason "Court order" and reference "ORD-2026-0412", then lifts it
    Then the case owner is U-23
    Then the case went to "ON_HOLD" and back to "IN_PROGRESS"
    Then each of the three calls has a decision log entry with its reason

  Scenario: AC6 Manual transfer without a reason (legacy RWB-E1-021 AC6)
    When a team manager calls the transfer endpoint for case RW-2026-000306 with no transfer reason
    Then the system refuses the call with 422 and MSG-P3-001
    Then the case keeps its queue and owner

  Scenario: AC7 Target owner at the cap (legacy RWB-E1-021 AC7)
    Given U-24 holds 150 open cases in queue "TDR-BKK-CO"
    When a team manager transfers case RW-2026-000307 to U-24 with transfer reason "R01"
    Then the system refuses the call with 422 and MSG-P3-002 naming U-24

  Scenario: AC8 Closed case (legacy RWB-E1-021 AC8)
    Given case RW-2026-000308 has status "CLOSED"
    When a team manager transfers it to queue "TDR-BKK-CO"
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC9 Decision log unavailable (legacy RWB-E1-021 AC9)
    Given the decision log store is unavailable
    When a team manager transfers case RW-2026-000309 with transfer reason "R03"
    Then the system refuses the call with 503 and MSG-P7-003
    Then the case keeps its queue and owner

  Scenario: AC10 Legal hold stops automated transfers (legacy RWB-E1-021 AC10)
    Given case RW-2026-000310 has legal_hold = true
    When TimerDue arrives and matches rule "TRF-003"
    Then the case keeps its queue and owner
    Then the system records the skip on the job log with rule R-UNI-20

  Scenario: AC11 A repeated event (legacy RWB-E1-021 AC11)
    Given PaymentMissed with event ID "EVT-88120" moved case RW-2026-000311 to "TDR-BKK-CO"
    When PaymentMissed with event ID "EVT-88120" arrives again
    Then the case has one transfer for the event
    Then the system counts the repeat as an idempotency hit

  Scenario: AC12 No owner below the cap in the target queue (legacy RWB-E1-021 AC12)
    Given every member of "LIT-BKK-OFF" holds 150 open cases
    When rule "TRF-007" fires for case RW-2026-000312
    Then the case is in the overflow queue "LIT-BKK-OVF" with no owner
    Then the system tells the team manager of "LIT-BKK" with MSG-P3-011 and count 1

  Scenario: AC13 Hold on a case already on hold (legacy RWB-E1-021 AC13)
    Given case RW-2026-000313 has status "ON_HOLD" with a legal hold
    When a litigation officer places a legal hold again
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC14 No rule matches (legacy RWB-E1-021 AC14)
    Given no TRANSFER rule matches DocumentStored for case RW-2026-000314
    Given the rwb-decision contract mock returns no TRANSFER rule for DocumentStored
    When DocumentStored arrives for the case
    Then the case keeps its queue and owner
    Then the system writes no decision log entry

  Scenario: AC15 Role without transfer right (exception X11) (new, D-RCV-60)
    Given a role RW-CASEOWN with Queue and allocation R and no Queue and allocation U
    When RW-CASEOWN calls POST /cases/{caseId}/transfer for case RW-2026-000315
    Then the system refuses the call with 403 and MSG-P4-002
    Then the case keeps its queue and owner

  Scenario: AC16 Transfer keeps status and clocks (BR10) (new, D-RCV-60)
    Given case RW-2026-000316 is "IN_PROGRESS" in queue "TDR-BKK-CO" with its clocks running
    When a team manager transfers it to owner U-25 with transfer reason "R01"
    Then the case status is "IN_PROGRESS" and its clocks are unchanged

  Scenario: AC17 Manual transfer API unchanged (BR11) (new, D-RCV-60)
    Given the transfer endpoint keeps the legacy endpoint, request, response, errors and authorization
    When a team manager calls the transfer endpoint for case RW-2026-000317 with reason code "MANUAL", transfer reason "R01" and target owner U-26
    Then the response and error codes match the legacy transfer endpoint

  Scenario: AC18 Version not in force leaves the event unprocessed (BR12) (new, D-RCV-60)
    Given package TRANSFER version "TRF-2026.11" is not in force
    When TimerDue arrives for case RW-2026-000318 and matches rule "TRF-003"
    Then the event stays unprocessed on the inbound topic
    Then the case keeps its queue and owner

  Scenario: AC19 Error answers of the transfer operation (register AC17) (new, D-RCV-60)
    Given a caller without a valid token
    When the caller calls POST /cases/{caseId}/transfer for case RW-2026-000319
    Then the system refuses the call with 401
    Then the system refuses a call to POST /cases/{caseId}/transfer for an unknown case with 404, and a role without Queue and allocation U with 403

  Scenario: AC20 Activity retry and timeout (register AC18) (new, D-RCV-60)
    Given the decision record write fails during the RecordAndApply activity of a rule transfer
    When the activity runs under the activity retry policy
    Then the activity is retried and no case moves until a retry commits
    Then an activity that runs past its timeout is failed and no case moves; the timeout value is Not specified in the source documents (NEWAC-RWB-P3-E1021-APP-AC18)
```

AC4 (Eight triggers) is not owned by this story. The eight triggers stay covered by BR2 and are exercised by TC-E1-021-04, which this story keeps in section 16 because the legacy test set for the key is carried in full by the build story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case moves by the first TRANSFER rule, in row order, whose trigger and condition match. First match follows D-RCV-36 T5 | Package TRANSFER; REQ-CWC-010 |
| BR2 | The eight triggers are stage change, route decided, timer expired, deviation raised, deviation cleared, approval needed, document received and payment missed. They arrive as one TransferTrigger fact with an event code; a manual request is a separate call with a caller-supplied reason | REQ-CWC-010; events EV-05, EV-06, EV-07, EV-09, EV-12, EV-16, EV-18; D-RCV-36 T5 |
| BR3 | A manual transfer needs a transfer reason from the list | LOV-TRANSFER-REASON (assumed); REQ-WKM-003; VR-P3-010-1; DL23 (ASM-1232, ASM-1237, ASM-1259, ASM-1560; decision open) |
| BR4 | A transfer to an owner at the cap is refused | queue.capacity_cap; VR-P3-010-2 |
| BR5 | A case is in exactly one queue with one open assignment | REQ-CWC-005 |
| BR6 | No automated transfer while a legal hold is in force | R-UNI-20 |
| BR7 | Lifting a hold returns the case to the status it paused in | R-UNI-21; casemodel.txt status transitions |
| BR8 | An event with the same ID is processed once | R-UNI-40 |
| BR9 | Every rule transfer is logged with the rule ID and package version, and every manual transfer with its caller and reason, before it takes effect | Principle 5; R-UNI-39; REQ-CWC-016; D-RCV-36 T5 |
| BR10 | A transfer keeps the case status and the clocks | R-UNI-18 (same principle for reallocation) |
| BR11 | The manual transfer API is unchanged: endpoint, request, response, errors and authorization stay as they are | REQ-CWC-010 |
| BR12 | A TRANSFER version not in force leaves the trigger event unprocessed and moves no case; it is never a default transfer | R-UNI-41; D-RCV-36 T5 |

Target-service statements that make the rules hold in `rwb-case`:

- BR1 is executed by the embedded Drools kit inside the `EvaluateRules` activity; the row order is the salience in the package, and no trigger list, row order or target queue is written in code (D-RCV-36 T3, T5). The deviation-raised and deviation-cleared triggers are evaluated in RWB-S8-E1021-APP against the package in force from rwb-decision; the manual and the other trigger paths stay in this story.
- BR9 is executed by the decision-record library of DP-03 in the same transaction as the state change (one `RecordAndApply` activity), so the record and the change commit together or not at all.
- BR3 and BR4 read the reason list and the queue cap through `rwb-case`'s own contract of DP-07 and `rwb_case.queue.capacity_cap`; no business value is typed in code (BR-P3-010).
- BR8 is executed by the inbox of DP-09 (`rwb_case.processed_event`) and by `Idempotency-Key` on the POST.
- BR11 is the reason the transfer request, response, error codes and authorization are copied unchanged into RWB-P3-E1021-CON.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| NEW, ASSIGNED, IN_PROGRESS; WAITING values Not specified in the source documents (CG-ALL-3548) | LEGAL_HOLD_PLACED (R-UNI-20) | Placed through the legal-hold endpoint | On hold |
| On hold | LEGAL_HOLD_LIFTED (R-UNI-21) | Lifted through the legal-hold endpoint | `status_before_hold` (a LOV-CASE-STATUS value) |

A rule or manual transfer changes the queue, the team and the owner, not the status. `status_before_hold` holds the status the case paused in.

Workflow states of the capability itself:

| From | Event | To |
|---|---|---|
| CaseWorkflow running, no transfer pending | a trigger event or a manual call arrives | `EvaluateRules` scheduled as an activity |
| `EvaluateRules` done with a rule | rule ID and package version returned | `transfer` activity scheduled |
| `transfer` done | queue, team, owner and assignment changed | `RecordAndApply` scheduled |
| `RecordAndApply` committed | decision record and outbox rows written | waiting on the next durable timer or signal |
| `evaluate` or `transfer` raised NoPackageInForce or a refusal | error recorded with its message ID | waiting; the case is unchanged |
| Stage ends or 28 days pass | Continue-As-New | CaseWorkflow continues with a new run and the same workflow ID |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR | Transfers and reassigns cases in team scope (Queue and allocation U) |
| RW-CAPACITY | Transfers cases (Queue and allocation U) |
| RW-LITOFF and other roles with Case record U | Place and lift a legal hold on a Legal or court instruction (Case record U) |
| RW-CASEOWN | Reads the case; may not transfer (Queue and allocation R) |
| SY-RULES | Evaluates package TRANSFER through the embedded Drools kit, inside the activity |
| SY-CASEWF | Carries out rule transfers (Queue and allocation CRU) |
| SY-DECLOG | Writes the decision records and publishes them on the shared topic |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope, masking and DoA in `rwb_access`) and is consumed as the cached permission decision the service holds. The rwb-access authorise call is the check consumed here; its operation name is Not specified in the source documents (GAP-3076). This story adds no guard of its own for it: the refusal shape is 403 with MSG-P4-002, as in the legacy endpoint. Where the legacy guard is replaced by the shared guard library is RWB-P3-E1019-APP (DP-08); this story inherits it.

Who may override a transfer that has been refused is Not specified in the source documents (GAP-0689; ASM-1236).

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0688; ASM-1235); the story refers to "the rwb-case login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read |
| DF-CAS-005 | `recovery_case` | status | Write |
| DF-CAS-006 | `recovery_case` | stage_code | Read |
| DF-CAS-008 | `recovery_case` | route_code | Read |
| DF-CAS-009 | `recovery_case` | owner_user_id | Write |
| DF-CAS-010 | `recovery_case` | queue_id | Write |
| DF-CAS-011 | `recovery_case` | team_code | Write |
| DF-CAS-019 | `recovery_case` | deviation_open | Read |
| DF-CAS-020 | `recovery_case` | legal_hold | Write |
| DF-CAS-021 | `recovery_case` | rule_version (the package version label) | Write |
| DF-CAS-055 | `recovery_case` | status_before_hold | Write |
| DF-WRK-001 | `queue` | id | Read |
| DF-WRK-002 | `queue` | queue_code | Read |
| DF-WRK-004 | `queue` | team_code | Read |
| DF-WRK-007 | `queue` | capacity_cap | Read |
| DF-WRK-008 | `queue` | overflow_queue_id | Read |
| DF-WRK-009 to DF-WRK-016 | `assignment` | all fields | Write |
| DF-WRK-040 | `assignment` | transfer_reason_code | Write |
| (queue member load) | `queue_member` | the member load used by lowest-load owner selection | Read |
| (rule row, through the kit) | package TRANSFER, held by `rwb-decision` | rule_id, package version label, event_code, condition, row_order, target_queue_code, outputs | Read only through the evaluated model |
| (decision record) | decision-record library table in `rwb_case` | chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash, entry_hash | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_case` | event rows for CaseTransferred, CaseStateChanged and the decision record | Write |
| (reference data) | `lov_value`, `reference_row`, `reference_version` | LOV-TRANSFER-REASON rows R01 to R06 | Read through the reference-data contract |

The rule row is read only as the evaluated model returned by the kit; this story writes no rule row and no rule package table (`rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are owned by rwb-decision). `recovery_case.rule_version` and the decision record's `ruleVersion` hold the package version label (D-RCV-36 T5).

No table of another service is read (DP-01). Personal data never enters the event payload, the workflow input, the decision record or the log.

### 12. Contract

The six consumed rows below have no operation name published in any source (GAP-3076). Their clients and fakes are built from the documented use until each name is published (GAP-3076):

- rwb-case transfer request that performs the move
- rwb-case queue and capacity read
- reference-data read of LOV-TRANSFER-REASON
- rwb-decision package read
- rwb-access authorise call
- rwb-source-data case-facts read

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 | The manual transfer, unchanged request, response, errors and authorization; `Idempotency-Key` required |
| POST | `/api/recovery/case/v1/cases/{caseId}/legal-hold` | P3 | Place or lift a hold; `Idempotency-Key` required |

Both are contract-defined in RWB-P3-E1021-CON.

#### 12.2 REST operations consumed

None. This story adds no REST operation consumption. The TRANSFER package is fetched as a model by the embedded Drools kit (H RWB-PLT-E1072-CON) from the rule-package registry of rwb-decision, and the authorisation decision is the cached permission decision from rwb-access that the service template's guard already holds.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, fromOwner, toOwner, reasonCode |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, decisionLogEntryId, fromState, ruleId, toState |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained decision record |

CloudEvents 1.0 envelope; no personal data in any payload.

#### 12.4 Events consumed

| Event | Topic | Owner | Note |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | Stage change; a route decided arrives as RouteDecided |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 | Trigger |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 | Trigger |
| `rwb.decision.ApprovalRequested.v1` (EV-09) | `rwb.decision.events.v1` | P7 | Trigger |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | P8 | Trigger |
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | Trigger |
| `rwb.valuation.RouteDecided.v1` | `rwb.valuation.events.v1` | S1 | Trigger for the route-decided row |

`TimerDue` (EV-18) is kept as a legacy reference only: in the target the timer expiry is raised inside `CaseWorkflow` by its durable timer, so no Kafka subscription exists for it.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `CaseWorkflow` | Parent workflow, one per case | `rwb-case` | Forwards the trigger to the running stage child or handles it; Continue-As-New at each stage end and at least every 28 days |
| `DailyCaseRun` | Workflow, started by Schedule and by AceDataReady (`sourceSystem` ALS, `status` COMPLETED) | `rwb-case` | Carries the morning allocation step (JOB-03 as a legacy reference) |
| `transfer` | Activity | `rwb-case` | Hold check, version lock, owner choice, assignment swap, decision record and outbox in one transaction |
| `EvaluateRules` | Activity, from the kit | `rwb-case` | The only place Drools is called |

#### 12.6 Schedules

None for this story. The transfer is event-started or signal-started; the only Schedule nearby is `DailyCaseRun`, which this story does not change. JOB-03 and JOB-05 are legacy references.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 | Queue, team, owner, status, legal hold, status before hold, rule version |
| `assignment` | P3 | End the open row, insert the new row with reason and transfer reason code |
| `queue` | P3 | Target queue, team, cap, overflow queue |
| `queue_member` | P3 | Member load for lowest-load and cap checks |
| `case_account` | P3 | Read for the case snapshot only |
| `task` | P3 | No write; read for the transfer-related task view |
| `timer` | P3 | Read; a hold pauses and resumes the clock through the timer contract |
| `lov_value` | P3 | LOV-TRANSFER-REASON read through the contract |
| `reference_row`, `reference_version` | P3 | Reference versions read through the contract |
| decision-record, inbox and outbox tables | PLT library, created in `rwb_case` | Written in the same transaction |

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case transfer and legal-hold fake | RWB-P3-E1021-CON | The build of the controller and the activity against the published shape |
| decision-record fake | RWB-PLT-E1027-CON | The local record write and the topic publish |
| decision contract fake | RWB-P7-E1027-CON | The central ledger's collection of the record |
| Drools kit stub with package TRANSFER "TRF-2026.11" | RWB-PLT-E1072-CON | `EvaluateRules` answers in unit and component tests |
| reference-data fake | RWB-P3-E1043-CON | LOV-TRANSFER-REASON and the queue and team lists |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 0 | The transfer and legal-hold endpoints |
| Kafka | Published 2 events and 1 decision record; consumed 7 events | `rwb.case.events.v1`, `rwb.decision-record.v1`, the inbound topics of S8, P7, P8, P5 and S1 |
| Temporal | 2 workflows, 2 activities | `CaseWorkflow` with `EvaluateRules` and `transfer`; `DailyCaseRun` unchanged |
| File | None | No file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `case/transfer`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseRouter | Kafka consumer with inbox | Reads the trigger events, deduplicates by event ID, calls `signalWithStart` on `CaseWorkflow` |
| TransferTrigger | Fact record | event code, case number, stage, route, deviation state, legal hold |
| TransferActivity | Temporal activity | Hold check, `EvaluateRules` call through the kit, version lock, owner choice, assignment swap, record and outbox in one transaction |
| TransferService | Service | The shared logic behind the activity and the manual call |
| TransferController | Controller | `POST /cases/{caseId}/transfer` and `POST /cases/{caseId}/legal-hold`, with the access check and `Idempotency-Key` |
| LegalHoldService | Service | Place and lift with `status_before_hold`, publish CaseStateChanged |
| CaseRepository | Repository | `recovery_case`, `assignment`, `queue`, `queue_member`, `timer`; no foreign table |
| RuleModelClient | Kit client | Fetches the TRANSFER model of the version in force, verifies the checksum, hands it to the KieBase registry |

**Database**

- Writes `recovery_case` (queue_id, team_code, owner_user_id, status, legal_hold, status_before_hold, rule_version, version), `assignment` (end the open row, insert the new row with transfer_reason_code), the inbox `processed_event` and the outbox.
- Update with `WHERE id = ? AND version = ?`; zero rows updated means the version changed (MSG-GEN-004).
- Constraint: partial unique index `ux_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL`.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V<next number>__transfer.sql`, taking the next free number of `rwb-case`'s own V0001 to Vnnnn sequence (not specified in the source documents (CG-ALL-3561)), adds `recovery_case.status_before_hold`, `assignment.transfer_reason_code`, the partial unique index and `processed_event` (event_id uuid primary key, consumer varchar(60), processed_at).

**Configuration and reference data**

- Package TRANSFER version "TRF-2026.11", loaded by RW-COE and approved by RW-RISK through RWB-E1-073 (RWB-P3-E1073-APP); the running version is a row in `rwb-decision`, not in this schema.
- LOV-TRANSFER-REASON (R01 to R06; DL23) through the reference-data contract of DP-07.
- Queues and members from RWB-E1-019 data, read from `rwb_case`.
- Feature flag `rwb.p3.transfer`. Off: no rule transfers, the manual endpoints return 404 and the activity is not registered.

**Build steps**

1. `TransferTrigger` and the `EvaluateRules` call through the kit, with unit tests for each trigger (BR2), no match (AC14) and a version not in force (BR12).
2. `transfer` activity with version lock, hold check and assignment swap; tests AC1, AC3, AC10, AC12.
3. Case router with the inbox and `signalWithStart`; test AC11.
4. Manual path with reason and cap validation; tests AC2, AC6, AC7, AC8.
5. `LegalHoldService` place and lift; tests AC5, AC13.
6. Decision record as the last step of the same transaction, including the rejected transfer, and the outbox rows; test AC9.
7. Controller endpoints with the access check and `Idempotency-Key`; access test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The single legacy interface the DP-11 row replaces is the in-process `RuleEvaluator` call; the transfer activity is the mockable boundary and the package is fetched as a model. DP-04's contract dependency is carried by the platform kit's own contract (H RWB-PLT-E1072-CON) in this story's dependency list; the build-time C dependency recorded on the story is the decision contract RWB-P7-E1027-CON.

**Done when.** The tests in section 16 pass, each of the eight triggers moves a case in SIT, every rule transfer decision record names the TRANSFER rule ID and package version, every manual transfer record names the caller and reason, and `rwb.case.CaseTransferred.v1` is on the topic once per transfer with no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | Manual transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-027 | No TRANSFER version is in force for a rule trigger | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The manual path answers 401, 403, 404, 409, 422 and 503; the rule path never answers a caller, it records the error on the activity and lets the retry policy act.

### 15. Screens and states

No screen in this story. The case record view (SCR-02 Case list and SCR-03 Case record) shows the new queue, owner and the hold banner through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON) and the read operations of RWB-P3-E1023-APP. The transfer screen SCR-05 comes in Epic 2 (RWB-E2-012).

States this story makes visible: the case status and queue and owner after a transfer; the hold banner while `legal_hold` is true; the overflow marker when the case sits in the overflow queue with no owner.

SCR-02 Case list: empty and loading as in Screen Specifications v1; error and no access: Not specified in the source documents (CG-ALL-3562).

SCR-03 Case record: loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-3563).

SCR-05 Transfer screen (RWB-E2-012): empty, loading, error and no access: Not specified in the source documents (CG-ALL-3564).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-15 | AC15 | Component | RW-CASEOWN calls POST /cases/{caseId}/transfer and is refused with MSG-P4-002 |
| TC-E1-021-01 | AC1, BR1 | End to end | Case in TDR-BKK-CO, route R4 approved; package TRANSFER "TRF-2026.11" |
| TC-E1-021-02 | AC2, BR3 | End to end | Manual transfer with R03 |
| TC-E1-021-03 | AC3, BR5 | End to end | Two transfers on record version 7 |
| TC-E1-021-04 | BR2 (AC4 run by Not specified in the source documents (CG-ALL-3557)) | End to end | Eight TRANSFER rules |
| TC-E1-021-05 | AC5, BR7 | End to end | Reassign, place hold, lift hold |
| TC-E1-021-06 | AC6, BR3 | End to end | No transfer reason |
| TC-E1-021-07 | AC7, BR4 | End to end | Owner U-24 at 150 |
| TC-E1-021-08 | AC8 | End to end | Closed case |
| TC-E1-021-09 | AC9, BR9 | End to end | Decision log store down for a manual call |
| TC-E1-021-10 | AC10, BR6 | End to end | legal_hold = true and TimerDue |
| TC-E1-021-11 | AC11, BR8 | End to end | Event EVT-88120 twice |
| TC-E1-021-12 | AC12 | End to end | Every member of LIT-BKK-OFF at 150 |
| TC-E1-021-13 | AC13 | End to end | Hold on a case on hold |
| TC-E1-021-14 | AC14, BR1 | End to end | DocumentStored with no rule |
| TC-E1-021-16 | Principle 5 | NFR | Decision log write forced to fail for a rule transfer; event retried, case unchanged |
| TC-E1-021-17 | Section 12 | Contract | Provider and consumer checks for the operations, events and activities of section 12 against RWB-P3-E1021-CON |
| TC-E1-021-18 | Section 12.7 (ASM-3438) | Component | Boundary on the queue cap: owner with 149 and with 150 open cases in the target queue |
| TC-E1-021-19 | AC16, BR10 | End to end | Case IN_PROGRESS with clocks running; manual transfer to U-25 with reason R01 |
| TC-E1-021-20 | AC17, BR11 | Contract | Manual transfer with reason code MANUAL, R01 and target owner U-26 against the legacy endpoint contract |
| TC-E1-021-21 | AC18, BR12 | End to end | TRANSFER version not in force; TimerDue matching TRF-003 |
| TC-E1-021-22 | AC19 | Component | Caller without a valid token; team manager calls transfer for unknown case RW-2026-000320; role without Queue and allocation U |
| TC-E1-021-23 | AC20 | NFR | Decision record write fails during RecordAndApply of a rule transfer; activity retried; timeout Not specified in the source documents (NEWAC-RWB-P3-E1021-APP-AC18) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR.

### 17. Guardrails

- No business value in code: triggers, target queues and the reason list are data in the TRANSFER package and the list; BR-P3-010.
- No personal data in logs, tests, workflow history, event payloads or prompts; the workflow payload codec of the kit encrypts every payload. The fields this story carries are the case ID, queue, team, owner user ID, reason code, rule ID and package version; any of them that the data model classes as personal data is masked under the rwb-access masking rules and kept out of prompts (DOR-RWB-P3-E1021-APP-11).
- No read of another service's tables (DP-01): the trigger events arrive through Kafka, the rule package arrives as a model, the reason list arrives through the reference-data contract.
- One evaluator: TRANSFER is evaluated only through the embedded Drools kit and only inside an activity; no trigger list, row order or target queue is written in code (D-RCV-36 T3, T5).
- The manual transfer API keeps its request, response, errors and authorization (BR11).
- A transfer never resets the stage clock or the prescription date (BR10).
- The transfer is idempotent twice over: `Idempotency-Key` on the POST and the inbox on the event.
- The feature flag `rwb.p3.transfer` removes the capability without a rollback of the schema.
- JOB-03 and JOB-05 are legacy references; the transfer is event-started and the timer is durable inside the workflow, so no case wait moves to a new scheduler in this story.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers and manual request with a reason | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-E1-021-01 to TC-E1-021-14, TC-E1-021-17, TC-E1-021-18 |
| REQ-CWC-016 | Every transfer logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-E1-021-01, TC-E1-021-03, TC-E1-021-09, TC-E1-021-16 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | Epic 2, work management | FEAT-CWC-10 | All recovery processes | VR-P3-010-1; DL23 (ASM-1232, ASM-1237, ASM-1259, ASM-1560) | TC-E1-021-02, TC-E1-021-06 |
| REQ-CWC-005 | A case is in one queue with one open assignment | Epic 1, 3.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20 | TC-E1-021-03 |

| Legacy reference | Where it is kept |
|---|---|
| Package code TRANSFER, version "TRF-2026.11" | Metadata, sections 3, 4, 8, 13, 16 |
| Event CaseTransferred (EV-04) | Sections 4, 12.3, 17 |
| MSG-P3-001, MSG-P3-002, MSG-P3-005, MSG-P3-011, MSG-P3-027, MSG-GEN-004, MSG-P7-003, MSG-P4-002 | Section 14, exception paths |
| Trigger rows TRF-001 to TRF-009, queues TDR-BKK-CO, LIT-BKK-OFF, DIL-BKK-CO, NPA-BKK-CO, DEV-HANDLER, TDR-BKK-APR, LIT-BKK-OVF | Background, AC1 to AC14, section 16 |
| Rule IDs R-UNI-20, R-UNI-21, R-UNI-39, R-UNI-40, R-UNI-41 | Sections 8, 9, 18 |
| Legacy key RWB-E1-021, story RWB-P3-E1021-APP, contract RWB-P3-E1021-CON, deployment RWB-P3-E1021-OPS | Metadata, sections 3, 12 |

### 19. Out of scope

- The transfer screen and queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap (Epic 2, R-UNI-18, R-UNI-19); RWB-P3-E1020-APP owns the assignment engine.
- Escalation of a breached timer without moving the case (RWB-E1-028; RWB-P3-E1028-APP).
- The route decision itself (Epic 4).
- The trigger arriving from the case router rather than as a Temporal signal on a stage child is the target design; the stage children themselves are Epic 3 and later.
- Loading, validating, approving and rolling back the TRANSFER package (RWB-E1-073; RWB-P3-E1073-APP).
- The contract document, its fakes and its versioning (RWB-P3-E1021-CON).
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook (RWB-P3-E1021-OPS).
- The secondary slices of the same legacy key in rwb-access, rwb-decision, rwb-document, rwb-deviation and the wave-1 integration harness.
