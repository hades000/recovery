# RWB-P3-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P3-AB |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P2-E2007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-033, FR-P3-034) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)**, I want **the case moved from its operations-waiting route state to the next route state, with one decision log entry naming the rule and the package version, when the booking confirmation for an approved restructure or settlement reaches rwb-case, and one task opened on the case when the booking is missing or the booked terms differ**, so that **every approved decision is confirmed as booked in the core bank with the case on the right route state, and no file the Workbench has to load**.

### 2. Business rationale

The officer books restructures and settlements by hand in ALS (INT-03), and nothing in the Workbench moves the case when the booking arrives. Today the case and the treatment record drift apart: the officer has confirmed the booking and the case still shows the operations-waiting route state, so the next step of the journey (the settlement payment due date) never starts. rwb-case owns the case record, the route state, the CMMN state and the tasks (DF-CAS-007, DF-WRK-017 to DF-WRK-026), so the confirmation has to land here and move the case in one transaction with its decision record.

This story is the rwb-case part of legacy RWB-E2-007. The matching service, JOB-08 and the ALS read are the rwb-integration part of the same legacy key (RWB-P2-E2007-APP and RWB-P2-E2007-CON), the treatment record and its APPROVED to BOOKED state are rwb-treatment (RWB-S2-E2007-APP), and the ACE view read is rwb-source-data (RWB-P1-E2007-APP). rwb-case reads no ACE view (DP-05) and no other service's tables (DP-01): the confirmation arrives as TreatmentBooked (EV-11) on `rwb.payment.events.v1`, the booking facts are read through the rwb-treatment contract, and the case move is decided by the route rows of package BOOKING_MATCH through the embedded Drools kit on the version in force (DP-04). The decision record is written locally by the decision-record library and relayed on `rwb.decision-record.v1` to the central ledger in rwb-decision (DP-03). It meets REQ-CHO-008, supports REC-03 (approved treatments against bookings, zero after two days) and keeps R-UNI-39 (a decision that cannot be recorded does not proceed).

### 3. Preconditions

- RWB-P2-E2007-CON is published: the case-facing part of the booking-confirmation contract — the TreatmentBooked (EV-11) envelope and fixture used to drive the case router, the booking-match result passed to the rwb-case `raiseTask` activity, the error envelope and the Idempotency-Key rule.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger behind it.
- RWB-PLT-E1072-CON is published: the embedded Drools kit, with one KieBase per package version, first-match semantics and the `NoPackageInForce` outcome (DP-04).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case and its client library (DP-06).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, with LOV-ROLE and the booking task codes held as reference rows (DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with CloudEvents, so the case router dedupes a redelivered event (DP-09).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, one durable timer per case (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-01 (DP-19); its field list and hop detail are Not specified in the source documents (GAP-0730; ASM-1289).
- The `rwb_case` baseline is applied: `recovery_case`, `task`, `timer` and the outbox, inbox and idempotency objects exist before this story runs its own migration.
- Package BOOKING_MATCH version "BKG-2026.12" is in force from its valid-from date, with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht (DL25), loaded, tested with at least 50 scenarios and approved by RW-RISK, who is not the author, through the package governance of the decision centre.
- The route rows R-RES-22 and R-SET-13 are in the versions in force on the business date; a case keeps the version it was decided under (R-UNI-38).
- The rwb-treatment contract is live for this build through its fake: `GET /api/recovery/treatment/v1/treatments/{treatmentId}` returns treatment type, state, booked at and booking difference. The exact booking fields of that response are Not specified in the source documents (GAP-0730; ASM-1286).
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0730; ASM-1285).

### 4. Flow

1. rwb-payment publishes TreatmentBooked (EV-11) on `rwb.payment.events.v1` with treatmentId, bookingRef (account_key + business date) and businessDate, keyed by caseId, after the booking is confirmed (the type is owned by rwb-payment; the case-facing fixture is published with RWB-P2-E2007-CON).
2. rwb-case: the case router consumes the event through its inbox `processed_event` in the same transaction as its own change; a duplicate ce_id acts once and is dropped.
3. rwb-case: the router reads the case and the treatment reference through the rwb-treatment contract, then calls `signalWithStart` on CaseWorkflow (workflow ID case-{caseId}) on task queue `rwb-case` and forwards the confirmation to the stage child.
4. rwb-case: the router refuses a confirmation whose decision names no package version in force and answers MSG-P3-027; nothing moves and the stuck-workflow scan raises the case (AC9).
5. BookingConfirmation activity: builds the route facts for the case — current `route_state`, the confirmation event, the treatment type, the booked business date and the package version named in the decision.
6. EvaluateRules activity: the embedded Drools kit evaluates the route rows of package BOOKING_MATCH on the version in force; first match wins, and the RESTRUCTURE row R-RES-22 decides BOOKING_CONFIRMED to BOOKED_IN_ALS_NLEADS while the SETTLEMENT row R-SET-13 decides SETTLEMENT_BOOKED to AWAITING_PAYMENT.
7. RecordAndApply activity: in one rwb_case transaction the service writes the new `route_state`, the `rule_version` label (DF-CAS-021), the `next_action_*` fields, the payment-due timer of 30 calendar days for a settlement (R-SET-13 row), CaseStateChanged (EV-05) in the outbox, and the local decision record with decision code "D6", the rule ID and the package version; a failed record write rolls the whole transaction back (R-UNI-39, AC8).
8. rwb-case: the outbox relay publishes CaseStateChanged on `rwb.case.events.v1` and DecisionRecorded on `rwb.decision-record.v1`; the central ledger in rwb-decision collects the record within 5 minutes.
9. rwb-case: when the booking-match result names a missing booking after the grace batches, the `raiseTask` activity opens one task WITH_OPS_BOOKING (restructure) or WITH_OPS_SETTLEMENT (settlement) for role RW-RESTRUCT with MSG-P2-011; the treatment and the route state stay unchanged (the match outcome and its text are the rwb-integration part, RWB-P2-E2007-APP).
10. rwb-case: when the result names different terms, `raiseTask` opens one task UNMATCHED_EXCEPTION for role RW-CREDITAD with MSG-P2-012, carrying the difference read from the treatment contract; no route state changes.
11. rwb-case: a second request for the same case, task code and treatment finds the open task through the partial unique index and returns it; no second task and no second event are produced (AC6).
12. RW-RESTRUCT opens SCR-01 My work through gateway-bff, which calls `GET /api/recovery/case/v1/me/tasks` on rwb-case and, on click, `GET /api/recovery/case/v1/cases/{caseId}`; SCR-14 Treatment record shows the case route state and the booked at, or the difference, from the treatment contract.
13. The officer books in ALS, the next ACE batch makes the booking visible, and the next confirmation moves the case in the same way; the case keeps the rule version of the move that decided it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No booking in the next batch | Task WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT to RW-RESTRUCT; route state and treatment unchanged | MSG-P2-011 | AC2 (carried by the P2 slice) |
| X2 | A booked term differs from the approved term | One task UNMATCHED_EXCEPTION to RW-CREDITAD with the difference read through the treatment contract; route state unchanged | MSG-P2-012 | AC3 (carried by the P2 slice) |
| X3 | Only some accounts of the case are booked | One task naming the accounts without a booking; route state unchanged | MSG-P2-011 | AC4 (carried by the P2 slice) |
| X4 | The ACE batch for ALS and the business date is not complete | The booking-match workflow does not start for the date, so no confirmation and no task reach rwb-case | MSG-P1-001 | AC5 (carried by the ITG slice) |
| X5 | The same confirmation arrives twice, or JOB-08 runs twice for the business date | The inbox drops the duplicate; no second route state move, no second CaseStateChanged and no second task | None | AC6 |
| X6 | A booking is still missing on the next batch | No second task; the open task stays and the REC-03 break list of rwb-source-data carries the days missing | None | AC7 (carried by the ITG slice) |
| X7 | The decision record write fails when the case is moved | The route state does not move, the timer is not started and no CaseStateChanged is published; an incident is raised and the next confirmation retries | MSG-P7-003 | AC8 |
| X8 | The confirmation names no BOOKING_MATCH version in force | NoPackageInForce; nothing moves, no difference is written and no task is opened for the date; the run ends failed and alerts RW-PLATADM | MSG-P3-027 | AC9 |
| X9 | A role without Case record R reads the case or its tasks | Refused with 403 by the rwb-access authorise check behind the endpoint | MSG-P4-002 | TC-E2-007-10 |
| X10 | The treatment contract does not answer inside the REST budget | One hop, 2 s timeout (DP-11); the confirmation stays on the queue and is retried; the case is never moved from a partial answer | None | AC8, TC-E2-007-11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts: RWB-P2-E2007-CON, the platform contract stories and the rwb_case baseline. The rwb-treatment, rwb-decision and rwb-access answers come from their contract fakes, and the confirmation arrives as a topic fixture |
| Negotiable | Route rows, tolerance and package version are data; the story fixes the case-side behaviour and names no compared term in code |
| Valuable | Every confirmed restructure or settlement moves its case to the next route state with a decision log entry, and every break reaches the right role as one task |
| Estimable | One event listener, one workflow signal path, one route evaluation, one task activity, three read endpoints |
| Small | Fits one sprint with its tests |
| Testable | Every owned criterion has a test case in section 16; every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load

  Background:
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED

  Scenario: AC1 Booking confirmed (legacy RWB-E2-007 AC1)
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht
    Given the officer booked the settlement in ALS on 2026-12-16
    Given v_ace_account shows settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht for synthetic account "A-0701" at business date 2026-12-16
    Given the rwb-treatment contract mock returns settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" with state "BOOKED" and booked at 2026-12-16
    Given the rwb-decision contract mock returns package "BOOKING_MATCH" version "BKG-2026.12" with the SETTLEMENT row "R-SET-13" and target route state "AWAITING_PAYMENT"
    When the next day's ALS batch is complete and JOB-08 runs on 2026-12-17
    Then the SETTLEMENT row of package "BOOKING_MATCH" version "BKG-2026.12" decides that the account is booked
    Then the booked terms match the approved treatment and the treatment state is "BOOKED" with booked at 2026-12-16
    Then the system publishes treatmentBooked with business date 2026-12-16
    Then the route state moves from "WITH_OPS_SETTLEMENT" to "AWAITING_PAYMENT" by R-SET-13 with a decision log entry

  Scenario: AC6 Match run twice (legacy RWB-E2-007 AC6)
    Given JOB-08 marked "TRT-SYN-0701" booked for business date 2026-12-16
    Given the rwb-treatment contract mock returns treatment "TRT-SYN-0701" with state "BOOKED" and booked at 2026-12-16
    When JOB-08 is rerun for 2026-12-16
    Then the system publishes no second TreatmentBooked event
    Then the system raises no task

  Scenario: AC8 Decision log write fails on confirmation (legacy RWB-E2-007 AC8)
    Given the decision log store is unavailable
    Given the rwb-treatment contract mock returns settlement treatment "TRT-SYN-0701" with state "BOOKED" and booked at 2026-12-16
    Given the rwb-decision contract mock returns package "BOOKING_MATCH" version "BKG-2026.12" with the SETTLEMENT row "R-SET-13"
    When the match finds "TRT-SYN-0701" booked
    Then the treatment stays "APPROVED" and no TreatmentBooked event is published
    Then the system raises an incident with message MSG-P7-003
    Then the match runs again with the next batch

  Scenario: AC9 No BOOKING_MATCH version in force (legacy RWB-E2-007 AC9)
    Given no BOOKING_MATCH version is IN_FORCE on 2026-12-17
    Given the rwb-decision contract mock returns NoPackageInForce for package "BOOKING_MATCH" on 2026-12-17
    When JOB-08 starts for business date 2026-12-16
    Then NoPackageInForce is thrown with MSG-P3-027 for package "BOOKING_MATCH"
    Then no treatment is marked booked, no difference is written and no task is raised
    Then the run ends as failed and alerts role "RW-PLATADM"
```

AC1, AC6, AC8 and AC9 are the four criteria this story owns, and they are the ones the rwb-case deliverable answers for: the confirmation moves the route state with a decision log entry (AC1), a repeated confirmation acts once (AC6), a decision that cannot be recorded does not move the case (AC8), and a decision that names no package version in force moves nothing (AC9). The remaining criteria of legacy RWB-E2-007 are not owned here: AC2 (booking missing), AC3 (terms differ) and AC4 (only some accounts booked) are carried by the rwb-integration slice RWB-P2-E2007-APP, which owns the match and the task texts and calls the `raiseTask` activity this story delivers; AC5 (ACE batch not complete) and AC7 (booking still missing on the next batch) are carried by the integration slice RWB-ITG-E2007-ITG. They appear in the flow and the exception table of this story only, marked with the slice that carries them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ACE batch; rwb-case moves the case only on a confirmation, never on an officer's action | INT-03; DL12; D-RCV-35 U1 |
| BR2 | A confirmed restructure moves the case from WITH_OPS_BOOKING to BOOKED_IN_ALS_NLEADS by row R-RES-22 | R-RES-22; package BOOKING_MATCH |
| BR3 | A confirmed settlement moves the case from WITH_OPS_SETTLEMENT to AWAITING_PAYMENT by row R-SET-13 and starts the payment-due timer of 30 calendar days | R-SET-13; package BOOKING_MATCH |
| BR4 | The route state is decided only by the route rows of package BOOKING_MATCH on the version in force; the answer names the rule ID and the package version, and no route table and no compared term sits in code | D-RCV-36 T3, T5; ADR-012; DP-04 |
| BR5 | The decision record, the route state, the timer and the outbox row commit in one transaction; a failed record write means nothing moves | Principle 5; R-UNI-39 |
| BR6 | A missing booking after the grace batches, and a booking whose terms differ, each open at most one task per case and task code; a repeat request returns the open task | REC-03; FEAT-CHO-08 |
| BR7 | A missing booking task goes to RW-RESTRUCT with MSG-P2-011; a differing terms task goes to RW-CREDITAD with MSG-P2-012; both leave the route state and the treatment unchanged | MSG-P2-011; MSG-P2-012 |
| BR8 | No BOOKING_MATCH version in force is a refusal (NoPackageInForce) with MSG-P3-027, never a default move and never a default task | R-UNI-41; D-RCV-36 T7 |
| BR9 | A duplicate confirmation acts once: the inbox records ce_id in the same transaction as the move, and the second copy changes nothing and publishes nothing | DP-09; Arch v5 slide 22 |
| BR10 | The case links to the treatment and the account by business key (treatmentId, account_key) with no foreign key across services; the booking facts are read through the rwb-treatment contract and are never copied into `rwb_case` | DP-01; D-RCV-35 U4; ADR-010 |
| BR11 | A case keeps the rule version of the move that decided it, and the version label is written to `recovery_case.rule_version` | R-UNI-38; DF-CAS-021 |
| BR12 | Task codes, owner roles and route values are data behind the reference-data contract; no route value or role is written in Java | LOV-ROLE; DP-07; BR-P3-034 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_OPS_BOOKING | BOOKING_CONFIRMED | NLEADS result APPROVED recorded and every account matched | BOOKED_IN_ALS_NLEADS |
| WITH_OPS_SETTLEMENT | SETTLEMENT_BOOKED | Agreement signed and terms booked in ALS | AWAITING_PAYMENT |

The treatment state moves from APPROVED to BOOKED on the treatment record, which rwb-treatment owns (RWB-S2-E2007-APP); this story reads it through the contract. A missing or differing booking leaves both the route state and the treatment state unchanged, and so does a decision record that cannot be written.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Consumes the confirmation, moves the route state, starts the payment-due timer, opens the tasks and writes the decision record |
| Drools evaluator (SY-RULES identity) | Evaluates the route rows R-RES-22 and R-SET-13 of package BOOKING_MATCH through the embedded kit (Rules and parameters R) |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| Case router | Turns the event into a workflow signal; owns no case data of its own |
| RW-RESTRUCT, restructuring officer | Receives the missing booking task and books in ALS (Treatment and offer, CRUA) |
| RW-CREDITAD, Credit Administration officer | Receives the differing terms task (Write-off and posting, CRUA) |
| RW-PLATADM, platform administrator | Receives the alert when no package version is in force and works the stuck case |
| RW-DATASTEW, data steward | Reads the REC-03 break list, which rwb-source-data owns |

The per-service login name is Not specified in the source documents (GAP-0730; ASM-1285); the story names it "the rwb-case login (DP-02)" until it is agreed. No role in this story may change a route state by hand: the move comes only from the confirmation.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | case header, status, route state, rule version | Read and write |
| DF-CAS-007 | recovery_case | route_state | Write |
| DF-CAS-021 | recovery_case | rule_version | Write |
| DF-CAS-049 to DF-CAS-053 | recovery_case | next action text, owner role, due date, rule ID, waiting flag | Write |
| DF-WRK-017 to DF-WRK-026 | task | id, case_id, task_code, element_type, discretion, status, owner_role, due_at, completed_at, outcome_code | Write |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, timer_type, started_at, expires_at, warn_at, paused, status, escalation_level | Write |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-ROLE and the booking task codes, with the version in force | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write |
| DF-TRT-004 | treatment (through the rwb-treatment contract) | treatment_type | Read |
| DF-TRT-012 | treatment (through the rwb-treatment contract) | booked_at | Read |
| DF-TRT-028 | treatment (through the rwb-treatment contract) | booking_difference | Read |

No copy of a treatment row and no copy of an ACE row is written into `rwb_case`: the booking facts are read through the rwb-treatment contract on each confirmation, and the ALS facts behind them stay with rwb-source-data. The treatment booking fields the contract returns are Not specified in the source documents (GAP-0730; ASM-1286). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}` | Read the case with its route state, rule version, status and next action | Case record R, scope applied | Not applicable |
| GET | `/me/tasks` | Read the caller's open tasks, including the booking and terms tasks | Case record R, scope applied | Not applicable |
| PATCH | `/tasks/{taskId}` | Complete or reassign a booking task with an outcome | Case record U, scope applied | Not applicable |

Response fields per the case CON story: case `id`, `caseNo`, `productGroup`, `status`, `routeState`, `routeCode`, `ruleVersion`, `nextActionText`, `nextActionOwnerRole`, `nextActionDueDate`, `nextActionWaiting`; task `id`, `caseId`, `taskCode`, `status`, `ownerRole`, `dueAt`, `outcomeCode`. Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 409 task already completed, 503 store down.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | Treatment type, state, booked at and booking difference for the confirmation | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | rwb-decision (P7) | Package model and checksum for the route rows R-RES-22 and R-SET-13 (DP-04) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, scope and right check before a read or a task update, cached | One hop, 2 s (DP-11) |

This story reads no rwb-source-data operation: the ALS facts reach it only inside the confirmation and the treatment answer (DP-05).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, fromRouteState, toRouteState, ruleId, ruleVersion, businessDate |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | decision code "D6", final call, rule ID, rule version, business date, record reference |

Both are written to the outbox in the same transaction as the route state change and relayed with the CloudEvents envelope; no personal data is carried (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | P8 | Case router: inbox dedupe, `signalWithStart` of CaseWorkflow and the confirmation forwarded to the stage child |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 | Drops the cached KieBase for package BOOKING_MATCH so the next evaluation fetches the version in force |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID case-{caseId}) | `rwb-case` | Tracks the case from entry to closure; receives the confirmation as a signal |
| case router | Kafka consumer | `rwb-case` | Dedupes the event and starts or signals CaseWorkflow; no case data of its own |
| BookingConfirmation | Activity | `rwb-case` | Builds the route facts and calls EvaluateRules for the route rows |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Calls the embedded Drools kit with package code, facts and the business date; returns the rule ID, version and target route state |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the route state, the timer and the outbox rows in one transaction |
| raiseTask | Activity (published contract) | `rwb-case` | Opens at most one task per case and task code; called by the booking-match workflow with the match outcome |

The route state is a field of `recovery_case`, so the route rows R-RES-22 and R-SET-13 are evaluated in rwb-case as they were in the legacy P3 module (legacy flow step 6), while the treatment state is applied in rwb-treatment; each service holds only its own approved copy of the package and every answer names the rule ID and the version. That division is read as stated and is Not specified in the source documents (GAP-0730; ASM-1288). The exact field list of the booking-match result passed to `raiseTask` is Not specified in the source documents (GAP-0730; ASM-1287).

#### 12.6 Schedules

None. JOB-08 Booking confirmation is an event-started workflow in rwb-integration, carried by the rwb-integration slice; this story starts on the confirmation event and holds no Schedule of its own. The 30-day payment-due timer of R-SET-13 is a durable Temporal timer inside CaseWorkflow, not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | Route state, rule version, status and next action of the case |
| task | P3 (rwb_case) | The booking and terms tasks with task code, owner role, due date and status |
| timer | P3 (rwb_case) | The 30-day payment-due timer row behind the durable timer |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

rwb-case reads no table of another service and holds no foreign key across services (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment WireMock | The S2 contract | `GET /treatments/{id}` for TRT-SYN-0701 BOOKED at 2026-12-16, and the approved and differing fixtures the matching slice uses |
| rwb-decision WireMock | The P7 contract | `GET /rule-models/{n}/{v}` for package BOOKING_MATCH "BKG-2026.12" with rows R-RES-22 and R-SET-13, and the `NoPackageInForce` answer |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and U, and refusing both for a role without the right |
| rwb-payment topic fixture | The EV-11 event from RWB-P2-E2007-CON | A TreatmentBooked message for TRT-SYN-0701 with business date 2026-12-16, replayed twice for the inbox test |
| rwb-source-data WireMock | The P1 contract | Not called by this story: the batch gate and the ACE view read are carried by RWB-P2-E2007-APP and RWB-ITG-E2007-ITG |

The booking-match result passed to `raiseTask` is stubbed with its published fixture; its exact field list is Not specified in the source documents (GAP-0730; ASM-1287).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | Case, task and completion provided; treatment, decision models and authorise consumed; one hop, 2 s timeout |
| Kafka | 2 published, 2 consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published; `rwb.payment.events.v1` and `rwb.decision.events.v1` consumed |
| Temporal | 1 workflow, 4 activities | CaseWorkflow; BookingConfirmation, EvaluateRules, RecordAndApply, raiseTask |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `bookingconfirmation`, Java package `th.co.scb.ace.workbench.recovery.case.bookingconfirmation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition in this story: the ALS account, batch and booked-settlement facts reach rwb-case only through the confirmation and the rwb-treatment contract, so no ACE view is read and no `v_ace_*` grant is needed. DP-11 fixes the one-hop, 2 s form of the treatment and decision reads. DP-10 turns the settlement payment-due period of the R-SET-13 row into a durable timer inside CaseWorkflow.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentBookedListener | Listener | Consumes EV-11 through the inbox, drops a duplicate ce_id and hands the confirmation to the case router |
| CaseRouter | Service | Loads the case and the treatment reference, refuses a decision with no package version in force, and calls `signalWithStart` on CaseWorkflow |
| BookingConfirmationActivity | Activity | Builds the route facts (current route state, confirmation, treatment type, business date, package version) and calls EvaluateRules |
| RouteRuleClient | Client | Fetches the BOOKING_MATCH model and checksum from rwb-decision, verifies it and hands it to the KieBase registry (DP-04) |
| CaseStateApplier | Service | Applies the decided route state, the rule version, the next action and the payment-due timer in one transaction |
| DecisionRecordWriter | Service | Writes the local decision record with the rule ID and version through the library, first in the transaction (DP-03) |
| BookingTaskService | Service | Opens at most one task per case and task code and returns the open task on a repeat request |
| TreatmentClient | Client | Calls the rwb-treatment contract for the booking fields; reads only, copies nothing |
| TaskController | Controller | `GET /me/tasks` and `PATCH /tasks/{taskId}` with the access check and scope |
| CaseController | Controller | `GET /cases/{caseId}` with route state and next action |
| AccessCheckClient | Client | Calls the rwb-access authorise contract (cached) before a read or a task update |
| ReferenceCatalog | Service | Reads LOV-ROLE and the booking task codes through the reference-data contract; no route value or role in Java |

**Database and migrations**

- Writes `recovery_case` (route state, rule version, next action), `task`, `timer` and the outbox in schema `rwb_case`.
- Constraint: partial unique index `ux_task_open_case_code ON task (case_id, task_code) WHERE status IN ('OPEN','IN_PROGRESS')`, so a repeat request for the same case and task code returns the open task and opens nothing (AC6, BR6).
- Constraint: one open payment-due timer per case and timer type, so a second confirmation does not restart the clock.
- Migration in this story: `V2007_1__booking_confirmation.sql` adds the two partial unique indexes above. The tables arrive with the `rwb_case` baseline; no column is added for treatment or ACE data.

**Configuration and reference data**

- Package BOOKING_MATCH version "BKG-2026.12" with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht, in force from its valid-from date; the route rows R-RES-22 and R-SET-13 are read from the version in force.
- The payment-due period of 30 calendar days is the timer spec of the R-SET-13 row and is read from the row, not from code.
- LOV-ROLE and the booking task codes through the reference-data contract, owner RW-COE.
- The feature switch is the legacy flag `rwb.integration.booking-confirmation`, kept as the legacy reference. In the target it is a parameter read through the parameters contract: off means the listener acknowledges the confirmation and moves no case.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0730; ASM-1285).

**Build steps**

1. TreatmentBookedListener and the case router with inbox dedupe and the refusal path for a decision with no version in force; tests for AC6 and AC9.
2. TreatmentClient over the rwb-treatment contract; test the booking fields and the difference for AC1 and AC8.
3. BookingConfirmationActivity and RouteRuleClient with the embedded kit, the checksum check and the RESTRUCTURE and SETTLEMENT rows; tests for AC1 and AC9.
4. DecisionRecordWriter and CaseStateApplier in one transaction, with the rollback when the record cannot be written; tests for AC8.
5. BookingTaskService with the partial unique index and the repeat-request rule; tests for AC6 and the task path the matching slice calls.
6. TaskController and CaseController with the access check, scope and the masking rule; test for the refused read.
7. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-treatment, rwb-payment and rwb-source-data are live.

**Feature switch.** Legacy `rwb.integration.booking-confirmation`, read as a parameter through the parameters contract; off means no route state moves and no task is opened.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P2-E2007-CON stay green, and a SIT week shows every confirmed synthetic treatment on the right route state with one decision record naming the rule and the package version, and no case moved without one.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS batch for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ACE batch late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No BOOKING_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without Case record R or U reads or updates | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "BOOKING_MATCH" and the business date only, never a case or account fact. MSG-P1-001 and the two task texts are raised by the rwb-integration slice and are copied here unchanged, because the case shows them.

### 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees booked at, or the booking difference with each term approved and booked, and the case route state beside it. SCR-01 My work (Loading; empty; list) shows the booking and terms tasks with their message and due date. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4.

Both screens are served by the gateway-bff composite route, which calls rwb-case for the case and task and the owning service for the treatment and the contact fields, one hop each, and merges the answers into the screen model (DP-19). The screen fields, the field-level masking and the composite route specification are Not specified in the source documents (GAP-0730; ASM-1289).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-10 | Access | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-01 | AC1, BR1, BR2, BR3, BR4, BR5, BR11 | End to end | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR6, BR7 | End to end | Restructure with tdr_flag false in v_ace_account |
| TC-E2-007-03 | AC3, BR6, BR7 | End to end | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR6, BR7 | End to end | Two accounts, one booked |
| TC-E2-007-05 | AC5 | End to end | ACE batch failed for 2026-12-17 |
| TC-E2-007-06 | AC6, BR9 | End to end | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | AC7, BR6 | End to end | Booking missing on two batches |
| TC-E2-007-08 | AC8, BR5 | End to end | Decision log store stopped |
| TC-E2-007-09 | AC9, BR8, BR11 | End to end | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-11 | Principle 5, BR5 | NFR | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-007-10 and TC-E2-007-11 keep their legacy data; for this slice they are run through the rwb-case task and decision-record paths, and their cross-service part is proved again by the integration slice.

### 17. Guardrails

- No business value in code: the route rows, the 30-day payment period, the task codes and the roles are data in package BOOKING_MATCH and the reference tables, read with the version in force.
- No personal data in logs, tests, workflow history or prompts. The story reads and writes treatment IDs, case IDs and account keys only: no name, address or identity number. Workflow payloads pass the payload codec, and test data uses synthetic case, treatment and account keys.
- No read of another service's tables and no ACE view: the booking facts come only through the rwb-treatment contract, and the ALS facts only inside the confirmation from rwb-integration (DP-01, DP-05). The `rwb_case` schema holds no foreign key into another schema.
- One evaluator per service: package BOOKING_MATCH is evaluated only through the embedded Drools kit on the version fetched from rwb-decision; rwb-case holds no route table, no workbook and no DRL source, and the treatment-side state is applied by rwb-treatment (DP-04, R-UNI-38).
- The decision record, the route state, the timer and the outbox row are one transaction, and the record is written first, so a decision that cannot be recorded does not move the case (R-UNI-39).
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only; a redelivered event is dropped by the inbox (DP-09).
- One open task per case and task code: the partial unique index and the activity return the open task, so a retry never duplicates a task.
- The case links to its source by business key (treatmentId, account_key) with no foreign key; nothing is invented from a partial answer.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-09, TC-E2-007-11 |
| D-RCV-35 U1 | Bookings are made in ALS and confirmed only from the next ACE batch, never from a Workbench action | Decision log, D-RCV-35 section 6.1 | FEAT-CHO-08 | 7.3 | R-RES-22, R-SET-13 | TC-E2-007-01, TC-E2-007-06 |
| D-RCV-36 T3, T5 | The route answer comes from package BOOKING_MATCH and names the rule ID and the package version | Decision log, D-RCV-36; ADR-012 | FEAT-CHO-08 | 7.3 | R-UNI-38, R-UNI-41 | TC-E2-007-01, TC-E2-007-09 |

### 19. Out of scope

- The matching run, JOB-08 and the booking comparison: rwb-integration (RWB-P2-E2007-APP), with its contract in RWB-P2-E2007-CON.
- The ACE account and batch read: rwb-source-data (RWB-P1-E2007-APP).
- The treatment record, its APPROVED to BOOKED state and the booking difference: rwb-treatment (RWB-S2-E2007-APP).
- Access rules, roles and masking as data: rwb-access (RWB-P4-E2007-APP).
- Authoring, approval and rollback of package BOOKING_MATCH (legacy RWB-E2-042, not this story).
- Posting a settlement booking to ALS from the Workbench (FEAT-PAY-06, Epic 4) and the SCR-29 Posting screen (Epic 4).
- Payment matching to the plan or settlement (JOB-07 and FEAT-OCC-10, Epic 2) and the REC-03 break list, which rwb-source-data owns (RWB-P1-E2007-APP).
- The `rwb_case` schema baseline, the topic and queue provisioning, the dashboards and the runbook of this capability.
