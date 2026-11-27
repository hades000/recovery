# RWB-P3-E5002-APP Record proof of delivery on a notice

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E5002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P3-AT |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E5002-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-S4-E5002-CON (notice contract, fake and schema published as slice 2.1 before wave 3); the LITIGATION rule package contract of rwb-decision (non-blocking, consumed) |
| Contract version | Not specified in the source documents (DOR-RWB-P3-E5002-APP-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P3-E5002-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E5-002 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E5002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 26 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the delivery answer of a notice applied to the case — the case moved to the notice period and its timer started from the delivery date when the proof of delivery is in, or the notice marked unserved when the proof window has expired — with the rule and the rule version recorded on a decision record**, so that **the notice period is counted from the day the customer actually received the notice, a notice nobody could serve is visible as such, and the pack is complete when the case goes to court**.

### 2. Business rationale

A statutory notice only starts its clock when it has been served. The legacy story wrote the delivery confirmation onto the case and started the notice period from the delivery date, because a period counted from the dispatch date can expire before the customer had the notice, and a period never started leaves a case stuck in the litigation route with an incomplete pack. When nobody could serve the notice, the legacy story marked it unserved and did not start the period. The FSD S4 module measures exactly this: a litigation turnaround target of 6 days against 21 days to file today, with incomplete packs and untracked law firm progress as the problem (FSD S4 A2.2.1).

In the target the same journey is cut across three services. **rwb-comms (P6)** owns the notice, the notice template, the merge fields and the proof of delivery itself — the ownership map and the Architecture v5 slide 41 row name exactly those four things for P6, and slide 17 gives P6 the `rwb_comms` schema with notices and proof of delivery (DP-01). **rwb-litigation (S4)** owns the legal action, the pack and the evaluation of rules R-LIT-07, R-LIT-08 and R-LIT-09 on the notice fact, and answers the delivery outcome through its own contract on `/api/recovery/litigation/v1`. **rwb-case (P3)** owns the case of record: it holds the case state, starts and shows the notice-period timer, places the task of the notice period, and writes the local decision record that names the rule and the rule version in force, in the same transaction as the state change (DP-03). This story is the rwb-case slice: it applies the delivery fact it receives through the S4 contract, performs the R-LIT-07 transition on a delivery, the R-LIT-08 or R-LIT-09 transition when the notice was not served, creates or does not create the notice-period timer with its durable Temporal timer inside CaseWorkflow, and publishes the state change.

The split is what keeps the three services independent. rwb-case stores three facts of the case — the notice reference, the delivery date and the outcome — and never the notice row, the proof document or the barcode: it holds no foreign key into `rwb_comms` and reads no notice table, which is the DP-01 rule stated as an acceptance criterion. Proof of delivery itself and the notice stay with P6, the legal action stays with S4, and the legacy in-process write of the delivery confirmation is replaced by one contract answer on one side and one `rwb_case` transaction with its outbox rows on the other. The legacy legal-action and notice-approval operations of the monolith keep their owners: they are served on `/api/recovery/litigation/v1` and `/api/recovery/comms/v1` (DP-13), and no operation of this story is added (DP-19 covers only the screen read through gateway-bff).

No ACE view is read here. The legacy data table of RWB-E5-002 lists the `v_ace_customer` view (DF-ACE-055 to DF-ACE-074); in the target the customer attributes travel inside the S4 answer when a rule needs them, and rwb-case reads no `v_ace_*` view for this step (DP-05 resolves to the owner's contract, not to a direct ACE read).

The legacy story master of the Epics 3 to 8 set carries no requirement ID for RWB-E5-002: the entry has the feature, the module, the data table, the endpoints, the screens, the rights and the test cases, but no REQ identifier (GAP-0737; ASM-1326). Traceability therefore runs to feature FEAT-LIT-02, to rules R-LIT-07, R-LIT-08 and R-LIT-09 and to the test cases until the Epics 3 to 8 PRDs add the requirement IDs.

### 3. Preconditions

- RWB-S4-E5002-CON is published: the delivery-answer resource shape (the notice reference, `deliveredAt`, the proof-window outcome, the rule ID and the package version of the S4 evaluation), its operation on `/api/recovery/litigation/v1`, its error envelope and its contract fake. This story builds against that contract and its fake and never against a notice table (DP-01).
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `task`, `timer`, `queue` and the outbox, inbox and idempotency objects.
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published by the platform contract story of DP-03; the workflow kit that holds a durable timer inside a workflow is published by the platform contract story of DP-10. Those platform dependencies are held by the platform stories and are not repeated in the metadata rows.
- A litigation rule package version is IN_FORCE on the business date and carries the rows R-LIT-07, R-LIT-08 and R-LIT-09 with their `action_text`, `owner_role` and `timer_spec`, and the version has the passing scenarios and the approval its governance requires. The package code that carries the three rows is Not specified in the source documents (GAP-0737; ASM-1327); the story reads the version in force from the rwb-decision registry on every evaluation and names no code.
- The notice-period duration is in force as a SERVICE_LEVEL reference row of the rwb-case reference data, read through the reference-data contract of the service (DP-07). The reference row code and its value are Not specified in the source documents (GAP-0737; ASM-1323).
- The case is in route state `NOTICE_DISPATCHED` with a notice reference that P6 dispatched and reported through NoticeDispatched (EV-14), which is what makes the S4 answer addressable by the notice reference.
- The rwb-access guard library is published by the platform contract story of DP-08 and answers the Litigation R right and the caller's scope.
- The login is the rwb-case login (DP-02).

### 4. Flow

1. The legal stage runs as LitigationWorkflow, the child workflow on task queue `rwb-litigation` started by CaseWorkflow. When the stage has a delivery answer for the notice of the case, it signals CaseWorkflow on `rwb-case` with the case ID and the notice reference. The hand-over direction between the two services is the direction recorded in GAP-0737: the contract names the answer, and the parent receives only the reference, so the answer itself is read once, by the service that owns the case.
2. CaseWorkflow runs its single step, EvaluateAndApply, on task queue `rwb-case`. The step calls the RWB-S4-E5002-CON operation inside the workflow kit activity with one hop, a 2 s timeout and a breaker per downstream (DP-11), and the call is recorded in the workflow history, so a replay reuses the recorded answer and never re-evaluates.
3. The answer names the notice reference, `deliveredAt` or the expiry of the proof window, the outcome and the rule ID with the package version of the S4 evaluation. A field that the contract marks as required and that is missing is a refusal: the step writes nothing and reports the field through MSG-GEN-001.
4. The step builds the idempotency key from the case ID, the notice reference and the answer (the delivery date, or the proof-window expiry). A key that `processed_event` and `idempotency_key` already hold is dropped: no state move, no second timer row and no second event, which is the inbox rule of DP-09.
5. A delivery answer moves the case from `NOTICE_DISPATCHED` to `WITH_CUSTOMER_NOTICE_PERIOD` by R-LIT-07 (`PROOF_OF_DELIVERY_RECEIVED`, `served_result = delivered`): the notice period starts at `deliveredAt`, and the timer row carries `timer_type` of the notice period, `started_at` = `deliveredAt` and `expires_at` = `deliveredAt` plus the duration of the SERVICE_LEVEL reference row.
6. A proof-window expiry answer moves the case from `NOTICE_DISPATCHED` to `NOTICE_UNSERVED` by R-LIT-08 (`PROOF_WINDOW_EXPIRED`): the notice is marked unserved with its reason, no notice-period timer row is written and no timer is started. A served result of refused, returned or undeliverable takes the same end by R-LIT-09 (`DELIVERY_FAILED`), also without a timer.
7. EvaluateAndApply writes, in one `rwb_case` transaction: the case state `route_state`, the `rule_version` of the move, the notice reference, the delivery date and the outcome (`served_result`) on `recovery_case`; the timer row on the delivery path only; the task of the notice period when the fired rule row names a timer spec; the local decision record with the rule ID (R-LIT-07, R-LIT-08 or R-LIT-09) and the package version; and the outbox rows CaseStateChanged and DecisionRecorded (DP-03, DP-09). A failed write rolls the whole transaction back, so neither the state nor the timer moves.
8. The workflow signals CaseWorkflow with the expiry of the notice period and holds it as a durable timer of the workflow kit (DP-10): the workflow ID is the case ID, so exactly one timer per case is open at a time in the namespace `rwb-recovery`. When the timer passes, the workflow raises TimerBreached through its own state; this story creates and holds the timer and does not own the breach (RWB-P3-E1028-APP).
9. A repeat of the same notice reference and the same delivery date, or of the same expiry answer, is dropped in step 4. The case keeps its state, its expiry and its single decision record.
10. Litigation officer: SCR-18 Notice approval and SCR-19 Litigation workspace read the case through the gateway-bff composite route, which calls rwb-case `GET /cases/{caseId}` and `GET /cases/{caseId}/timers` and merges the two answers (DP-19). The notice row itself, its states and the proof are served by rwb-comms; the pack states are served by rwb-litigation. The rwb-case fragment shows the case state and the notice-period end, read only, and shows "unserved" with its reason. When the caller has no Litigation R right, the fragment shows MSG-P4-002; when the case is outside the caller's scope, it shows MSG-P4-003. The empty and loading states are Not specified in the source documents (DOR-RWB-P3-E5002-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The S4 answer does not arrive within 2 seconds or the service is unavailable | The step keeps the case in `NOTICE_DISPATCHED` and raises no timer and no decision record; the workflow retries the activity with the kit's retry policy and the answer is read again | MSG-GEN-006 | AC1, AC2 |
| X2 | The S4 answer cannot be read (an unreadable envelope or a missing required field) | Nothing is written; the breach is recorded for the S4 owner and the case stays in `NOTICE_DISPATCHED` | MSG-GEN-001 | AC1 |
| X3 | No litigation rule package version is IN_FORCE on the business date | `NoPackageInForce`; no state move, no timer row and no decision record; the case is placed in the exception queue for role RW-TEAMMGR | MSG-P3-027 | AC5 |
| X4 | The local decision-record write fails | The transaction rolls back: the state, the notice columns and the timer do not move, the step fails, and the answer is retried | MSG-P7-003 | AC6 |
| X5 | The same notice reference and the same answer arrive twice | The second arrival is dropped by the inbox and the idempotency key; no second state change, no second timer row and no second event | None | AC4 |
| X6 | A delivery date arrives for a case that is not in `NOTICE_DISPATCHED` | The transition is refused; the case keeps its state and the arrival is recorded as an exception with the state it found | None | AC1 |
| X7 | A role without the Litigation R right reads the case | Refused before any read; nothing is returned and nothing is written | MSG-P4-002 | AC7 |
| X8 | A case outside the caller's scope is read | The response is 404, so the caller cannot tell an out-of-scope case from a case that does not exist | MSG-P4-003 | AC7 |

A served result of refused, returned or undeliverable is not an exception: R-LIT-09 marks the notice unserved exactly as R-LIT-08 does and the served-result values come from the FSD S4 A2.2 rule table, not from code.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-S4-E5002-CON fake and the platform kits; no work order sits inside another team's lane, and the notice row and the proof are out of the lane by design |
| Negotiable | The notice-period duration, the rule rows, the package version in force and the timer type are rows and reference data; the story fixes the behaviour, not the values |
| Valuable | The notice period is counted from the day the notice was served, an unserved notice is visible with its reason, and every move carries the rule and the version that made it |
| Estimable | One step, one client, one validator, one repository, one transaction, one durable timer and one read-only screen fragment |
| Small | Fits two weeks with its tests |
| Testable | Each of the eight criteria of section 7 is one automated test; the cross-service answer is stubbed in the S4 contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Record proof of delivery on a notice

  Background:
    Given case "RW-2026-000512" is in route state "NOTICE_DISPATCHED" with notice reference "NT-2026-000512-01"
    Given the SERVICE_LEVEL reference row of the case gives the notice-period duration in days
    Given the litigation rule package is in force with rows R-LIT-07, R-LIT-08 and R-LIT-09

  Scenario: AC1 Proof of delivery recorded moves the case into the notice period (new, D-RCV-60)
    Given the rwb-litigation contract mock returns proof of delivery for notice "NT-2026-000512-01" with delivered_at 2026-12-14
    When the delivery answer reaches case "RW-2026-000512"
    Then the case moves from "NOTICE_DISPATCHED" to "WITH_CUSTOMER_NOTICE_PERIOD" by R-LIT-07
    Then the timer row holds timer_type of the notice period, started_at 2026-12-14 and expires_at 2026-12-14 plus the duration of the SERVICE_LEVEL reference row
    Then CaseWorkflow holds expires_at as a durable timer and no Quartz row is written
    Then one decision record names R-LIT-07 and the package version in force
    Then rwb.case.CaseStateChanged.v1 is published with fromState "NOTICE_DISPATCHED" and toState "WITH_CUSTOMER_NOTICE_PERIOD"

  Scenario: AC2 An expired proof window marks the notice unserved (new, D-RCV-60)
    Given the rwb-litigation contract mock returns the expiry of the proof window for notice "NT-2026-000512-01"
    When the delivery answer reaches case "RW-2026-000512"
    Then the notice is marked unserved with the reason "proof window expired"
    Then the case moves from "NOTICE_DISPATCHED" to "NOTICE_UNSERVED" by R-LIT-08
    Then no notice-period timer row is written and no durable timer is started
    Then one decision record names R-LIT-08 and the package version in force

  Scenario: AC3 The notice row and the proof stay with rwb-comms (new, D-RCV-60)
    Given the notice row and the proof of delivery are held by rwb-comms
    Given the rwb-litigation contract mock returns proof of delivery for notice "NT-2026-000512-01" with delivered_at 2026-12-14
    When the delivery answer reaches case "RW-2026-000512"
    Then rwb-case stores only notice_ref "NT-2026-000512-01", proof_delivered_at 2026-12-14 and the outcome "delivered"
    Then rwb-case writes no rwb_comms table, holds no foreign key into it and reads no notice row directly (DP-01)
    Then the barcode and the proof document are not copied into rwb_case

  Scenario: AC4 A repeated delivery answer changes nothing (new, D-RCV-60)
    Given the delivery answer with notice "NT-2026-000512-01" and delivered_at 2026-12-14 was applied
    When the same answer arrives a second time on the inbox
    Then no state move, no timer row, no decision record and no event is written a second time
    Then the case stays in "WITH_CUSTOMER_NOTICE_PERIOD" with the same expires_at

  Scenario: AC5 No rule package version in force is a refusal (new, D-RCV-60)
    Given no litigation rule package version is IN_FORCE on the business date
    When the delivery answer arrives for case "RW-2026-000512"
    Then NoPackageInForce is raised with MSG-P3-027
    Then the case stays in "NOTICE_DISPATCHED", no timer row is written and no decision record is written
    Then the case is placed in the exception queue for role "RW-TEAMMGR"

  Scenario: AC6 An unrecorded decision stops the move (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the delivery answer arrives for case "RW-2026-000512"
    Then nothing moves: the case stays in "NOTICE_DISPATCHED", no timer row is written and no event is published
    Then the user sees MSG-P7-003

  Scenario: AC7 The case read is refused without the right or outside the scope (new, D-RCV-60)
    Given user "U-5002" holds RW-REFADM, which has no Litigation R right
    Given the rwb-access contract mock returns no Litigation R right for role "RW-REFADM"
    When "U-5002" calls GET /cases/{caseId} for case "RW-2026-000512"
    Then the call is refused with status 403 and MSG-P4-002
    Given a case owner whose scope is "Own" and a case owned by another person
    When the case owner calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    Then the read writes nothing

  Scenario: AC8 The notice state and the notice-period end show on the two screens (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-18 Notice approval and SCR-19 Litigation workspace for case "RW-2026-000512"
    Given the case holds notice "NT-2026-000512-01" in "NOTICE_UNSERVED" with the reason "proof window expired"
    When the litigation officer opens SCR-18 and SCR-19
    Then SCR-18 shows the notice state "unserved" with its reason and SCR-19 shows the notice-period end from GET /cases/{caseId}/timers
    Then both screens are read only and the browser calls one composite route and no owner service directly

  Scenario: AC9 A request without a login is refused with status 401 (new, D-RCV-60)
    Given the caller presents no rwb-case login
    When a caller calls GET /cases/{caseId} for case "RW-2026-000512"
    Then the call is refused with status 401
    Then the read writes nothing

  Scenario: AC10 A refused, returned or undeliverable result marks the notice unserved and keeps the reference rules (new, D-RCV-60)
    Given the rwb-litigation contract mock returns served result "refused" for notice "NT-2026-000512-01"
    When the delivery answer reaches case "RW-2026-000512"
    Then the notice is marked unserved and the case moves from "NOTICE_DISPATCHED" to "NOTICE_UNSERVED" by R-LIT-09
    Then an alternate service method is queued
    Then no notice-period timer row is written and the case status stays "In progress"
    Then the notice-period end comes from the SERVICE_LEVEL reference row, not from a constant in code
    Then the move reads no ACE view and no notice table

  Scenario: AC11 A retried or timed-out activity writes one decision record and one state move (new, D-RCV-60)
    Given the EvaluateAndApply activity for case "RW-2026-000512" times out before it returns
    When the workflow retries the activity
    Then the retry writes no second decision record, no second state move and no second timer row
    Then the case stays in "NOTICE_DISPATCHED" until the retried activity completes
    Then no event is published a second time
```

AC1 to AC11 are new for the rwb-case slice: the four legacy criteria of RWB-E5-002 are proved end to end by RWB-ITG-E5002-ITG and by the S4 slice RWB-S4-E5002-APP, so this story owns no legacy criterion and copies none. The notice-period clock is one clock per notice: its start is keyed by the notice reference and the delivered date through the partial unique running index and the idempotency key, so a second fact for the same notice is a repeat counted under R-UNI-40; the wave 3 refinement revisits this. In the registers, the RTM and the Covers column, this story's criteria are cited as RWB-P3-E5002-APP ACn; the bare labels AC1 to AC4 belong to RWB-S4-E5002-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case in `NOTICE_DISPATCHED` whose proof of delivery is in moves to `WITH_CUSTOMER_NOTICE_PERIOD`, and the notice period starts at `delivered_at` | R-LIT-07 (`served_result = delivered`) |
| BR2 | A case in `NOTICE_DISPATCHED` whose proof window has expired is marked `NOTICE_UNSERVED`, the notice period does not start, and the case moves to `NOTICE_UNSERVED` | R-LIT-08 (`PROOF_WINDOW_EXPIRED`) |
| BR2b | A served result of refused, returned or undeliverable also marks the notice unserved and moves the case to `NOTICE_UNSERVED`, and queues an alternate service method | R-LIT-09 (`DELIVERY_FAILED`) |
| BR3 | The notice, the notice template, the merge fields and the proof of delivery belong to rwb-comms (P6); the legal action and the pack belong to rwb-litigation (S4); the case state, the timer, the task and the decision record belong to rwb-case (P3) | Architecture v5 slide 41 and slide 17; `ownership.json` (notice, merge_field, template own P6; recovery_case, timer, task own P3); DP-01 |
| BR4 | The notice-period duration is reference data (a SERVICE_LEVEL row), never a constant in code; the expiry is the delivery date plus that duration | DP-07; Template and Rules §R7.3; R-LIT-07 |
| BR5 | The decision record is written with the rule ID and the package version in the same transaction as the state change; no record, no move | Principle 5; R-UNI-39; DP-03 |
| BR6 | No rule package version in force is a refusal (`NoPackageInForce`), never a default state move | R-UNI-41; Temporal and Drools design slide 14 |
| BR7 | A repeat of the same notice reference and the same answer writes no row, starts no timer and raises no event | R-UNI-40 |
| BR8 | The clock of the notice period is a durable timer inside CaseWorkflow; the timer row in `rwb_case` is the projection the screens read, and no Quartz row and no polling job is involved | `ownership.json` timer ruling; DP-10; Architecture v5 slide 44 |
| BR9 | The case read is guarded by the Litigation R right and by the caller's scope: a role without the right is refused, and a case outside the scope answers 404 | Legacy permission block of RWB-E5-002; DP-08; MSG-P4-002, MSG-P4-003 |
| BR10 | This step reads no ACE view and no notice table: the delivery fact comes from the S4 contract, and the customer attributes travel inside that answer when a rule needs them; they are personal data, and this step writes none of them to rwb_case | DP-01, DP-05; ADR-010 |
| BR11 | The notice state is a case route state; the case status stays "In progress" while the notice period runs | DF-CAS-007; legacy RWB-E5-002 ("a case in state NOTICE_DISPATCHED") |
| BR12 | A delivery answer whose result is PENDING is refused: the notice and the case stay unchanged and no timer starts, until the notice state for PENDING is settled | GAP-1192 (recommended resolution); LOV-DELIVERY (TSD P6 T3.2) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | R-LIT-07; the answer carries `delivered_at` and `served_result` delivered | WITH_CUSTOMER_NOTICE_PERIOD |
| NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | R-LIT-08; no proof returned inside the proof window | NOTICE_UNSERVED |
| NOTICE_DISPATCHED | DELIVERY_FAILED | R-LIT-09; `served_result` in refused, returned, undeliverable | NOTICE_UNSERVED |
| any other state | PROOF_OF_DELIVERY_RECEIVED, PROOF_WINDOW_EXPIRED or DELIVERY_FAILED | the case is not in `NOTICE_DISPATCHED` | unchanged; the arrival is recorded as an exception |
| WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | R-LIT-15; owned by the notice-period timer story, not by this one | PACK_ASSEMBLY |

The transitions and their event codes are those of the S4 TSD rule table for this feature (R-LIT-07 `NOTICE_DISPATCHED`/`PROOF_OF_DELIVERY_RECEIVED`/`WITH_CUSTOMER_NOTICE_PERIOD`, R-LIT-08 `NOTICE_DISPATCHED`/`PROOF_WINDOW_EXPIRED`/`NOTICE_UNSERVED`, R-LIT-09 `NOTICE_DISPATCHED`/`DELIVERY_FAILED`/`NOTICE_UNSERVED`). These are case route states (`recovery_case.route_state`, DF-CAS-007); the case status stays "In progress". The story also writes the notice facts of the case (`notice_ref`, `proof_delivered_at`, `notice_outcome`), which are facts and not states, and the package version of the move (`rule_version`, DF-CAS-021).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs EvaluateAndApply; reads the delivery answer through the rwb-litigation contract; writes the case state, the notice facts, the timer row, the task and the decision record |
| rwb-litigation (S4) service identity | Answers the delivery outcome, the rule ID and the package version of its own evaluation; owns the legal action and the pack |
| rwb-comms (P6) service identity | Owns the notice, the proof of delivery and the barcode; serves the notice row to the screens |
| Drools evaluator (SY-RULES identity) of rwb-litigation | Evaluates R-LIT-07, R-LIT-08 and R-LIT-09 on the notice fact; rwb-case applies the answer and never re-evaluates it |
| CaseWorkflow | Holds the notice-period durable timer and raises TimerBreached through its own state; moves no state by itself |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-LITOFF, litigation officer | Holds Litigation C and Litigation R; reads the case, the notice state and the timer in scope |
| RW-ENFORCE, enforcement officer | Holds Litigation C and Litigation R; reads the same |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Hold Litigation A; read the case and the notice state in scope |
| RW-CASEOWN, RW-TEAMMGR | Hold Litigation R; read the case state and the timer in scope |
| RW-TEAMMGR, team manager | Receives the case in the exception queue on the no-package path |
| RW-COE | Owns the rows R-LIT-07, R-LIT-08 and R-LIT-09 and the SERVICE_LEVEL reference row of the notice-period duration |
| RW-RISK | Approves a rule package version; the author cannot approve |
| RW-REFADM | Holds no Litigation R right; refused on the case read with MSG-P4-002 |

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and the rest | Read, and the row is written |
| DF-CAS-007 | recovery_case | route_state (the notice state of this story) | Write |
| DF-CAS-021 | recovery_case | rule_version (the package version of the move) | Write |
| Not specified in the source documents (GAP-0737; ASM-1322) | recovery_case | notice_ref, proof_delivered_at, notice_outcome (three new columns of this story) | Write |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, task_id, timer_type (DF-WRK-030), started_at (DF-WRK-031), expires_at, status (DF-WRK-035) and the rest | Write on the delivery path; read for the screen projection |
| DF-WRK-018, DF-WRK-019, DF-WRK-024 | task | case_id, task_code, due_at | Write when the fired rule row names a timer spec; read otherwise |
| DF-LEG-015 to DF-LEG-023 | notice (rwb_comms, owner P6) | id, case_id, document_id, notice_type, sent_date, barcode and the rest | Not read and not written: only the notice reference arrives on the S4 answer |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer (view of rwb-source-data) | person_key, cif_no, first_name, last_name, date_of_birth, customer_status and the rest | Not read: this story needs no customer attribute (DP-05) |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision) | all fields | Write locally; the central entry is sealed by rwb-decision |
| DF-REF-001 to DF-REF-015 | rule_row (rwb_decision, owner P7) | id, rule_id, rule_version, route_set, from_state, event_code and the rest | Read, by rule ID and package version through the rwb-decision registry |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | The SERVICE_LEVEL row of the notice-period duration and its version in force | Read |

The delivery answer fields (`noticeRef`, `deliveredAt`, the proof-window expiry, the outcome, the rule ID and the package version) are read from the rwb-litigation contract and are not read from any table. Ownership follows GAP-1740: rwb-comms owns the notice template, merge fields, delivery and proof of delivery; this story owns the notice period and the case notice state, and reads only the served result returned for the notice. No copy of a notice row is written into `rwb_case`, no barcode and no proof document is stored there, and no foreign key crosses a schema (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. This story adds no person-facing operation: the notice state and the notice-period end are read with the existing operations of rwb-case on base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | `/cases/{caseId}` | The case read, which already carries `route_state`; this story adds no field to the answer | Litigation R, scope applied |
| GET | `/cases/{caseId}/timers` | The timer read, which shows the notice-period `started_at` and `expires_at` from the timer row | Litigation R, scope applied |

Both operations are owned by their Epic 1 stories and are named here only because the screens of this story read them; this story writes the rows behind them.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| Not specified in the source documents (GAP-0737; ASM-1324) | `/api/recovery/litigation/v1` (path fixed by RWB-S4-E5002-CON) | rwb-litigation (S4) | The delivery answer of one notice: the notice reference, `deliveredAt` or the proof-window expiry, the outcome, the rule ID and the package version (built against RWB-S4-E5002-CON and its fake) | One hop, 2 s, breaker |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Litigation R right and the scope before the case read, cached by the guard library | One hop, 2 s |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, decisionLogEntryId, fromState, toState (WITH_CUSTOMER_NOTICE_PERIOD or NOTICE_UNSERVED), ruleId (R-LIT-07, R-LIT-08 or R-LIT-09) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID (R-LIT-07, R-LIT-08 or R-LIT-09), package version, business date |

Both are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; no personal data is carried and no proof image, barcode or customer attribute is in any payload (DP-09). TimerBreached stays with RWB-P3-E1028-APP and is not published by this story.

#### 12.4 Events consumed

None. The delivery fact arrives on the rwb-litigation contract inside EvaluateAndApply and on the workflow signal that names the notice reference, so this story subscribes to no topic and holds no consumer of its own; the inbox and idempotency objects are used for the signal and for the activity answer.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = `case-{caseId}`) | `rwb-case` | Receives the signal that names the notice reference, runs the step, and holds the notice-period expiry as a durable timer (DP-10) |
| EvaluateAndApply | Activity (the one activity this story adds, called by CaseWorkflow) | `rwb-case` | Reads the S4 answer, validates it, decides among R-LIT-07, R-LIT-08 and R-LIT-09, and applies the state, the notice facts, the timer, the task, the decision record and the outbox rows in one transaction |

No other workflow and no other activity is added by this story. The S4 read runs inside EvaluateAndApply, so the answer is recorded in the workflow history and a replay reuses it.

#### 12.6 Schedules

None. The notice period is a durable timer of CaseWorkflow, not a Schedule, not a Quartz row and not a polling job (DP-10). The workflow that raises the expiry itself is RWB-P3-E1028-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story adds `notice_ref` varchar(40), `proof_delivered_at` timestamp and `notice_outcome` varchar(20), and writes `route_state` and `rule_version` |
| timer | P3 (rwb_case) | The notice-period row: `timer_type`, `started_at`, `expires_at` and `status`; the screen projection behind the timers read, while the clock is the durable timer of CaseWorkflow |
| task | P3 (rwb_case) | The task of the notice period when the fired rule row names a timer spec |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |
| decision_record | PLT library, created in rwb_case | The local hash-linked decision record of the move (DP-03) |

`notice`, `template` and `merge_field` are P6's tables in `rwb_comms` and are neither read nor written here: no foreign key, no cross-schema join and no view over them (DP-01). `rule_row` and `decision_log_entry` are rwb-decision tables and are read or written only through its contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-litigation WireMock | The S4 contract of RWB-S4-E5002-CON | proof of delivery at a fixed `delivered_at` 2026-12-14; the expiry answer of the proof window; a delayed answer beyond 2 s; a NoPackageInForce answer; an unreadable answer |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Litigation R, refusing it for RW-REFADM and excluding a case from an Own scope |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-18 and SCR-19 | The merged case and timer answers of AC8, including the "unserved" state with its reason |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | No operation added; the S4 delivery answer and the P4 authorise consumed; one hop, 2 s |
| Kafka | 2 published | `rwb.case.events.v1` and `rwb.decision-record.v1` published; none consumed |
| Temporal | 1 workflow, 1 activity | CaseWorkflow with its durable notice-period timer; EvaluateAndApply |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `noticedelivery`, Java package `th.co.scb.ace.workbench.recovery.case.noticedelivery`; front end `src/modules/recovery/case/NoticeState.tsx`, the read-only fragment that SCR-18 and SCR-19 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies this table adds are held by the platform contract stories and are not repeated in the metadata rows, which carry only the contract dependency of this legacy key: RWB-S4-E5002-CON (that bookkeeping is recorded in ASM-1325). DP-05 resolves to no ACE view and no rwb-source-data call: the customer attributes that a rule needs arrive inside the S4 answer, so rwb-case reads no `v_ace_*` view (ADR-010).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeDeliveryStep (EvaluateAndApply) | Activity of CaseWorkflow | Drives the read, the validation, the decision and the apply, and records the counts of the step |
| DeliveryAnswerClient | Client | Calls the rwb-litigation operation with one hop, the 2 s timeout and a breaker; never retries on its own, so the workflow kit owns the retry |
| DeliveryAnswerValidator | Service | Checks the required fields of the answer, rejects an answer with neither a delivery date nor an expiry with MSG-GEN-001, and builds the idempotency key from case ID, notice reference and answer |
| NoticeTransitionService | Service | Applies R-LIT-07, R-LIT-08 or R-LIT-09 to the case state, refuses a transition from any state other than `NOTICE_DISPATCHED`, and decides whether a timer row is created |
| NoticeTimerFactory | Service | Computes `started_at` and `expires_at` from `delivered_at` and the SERVICE_LEVEL reference row; writes nothing itself |
| CaseNoticeRepository | Repository | Writes `route_state`, `rule_version`, `notice_ref`, `proof_delivered_at` and `notice_outcome` in schema rwb_case only |
| NoticeTimerRepository | Repository | Writes the timer row of the notice period and the task row when the rule names a timer spec |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the rule ID and the package version, hash-linked, in the same transaction (DP-03) |
| CaseStateChangedPublisher | Outbox adapter | Inserts CaseStateChanged and DecisionRecorded in the outbox of the same transaction (DP-09) |
| NoticeState | React component | Shows the case state and the notice-period end on SCR-18 and SCR-19, read only, with the "unserved" reason |

**Database and migrations**

- Migration `V5002_1__notice_delivery.sql` adds `notice_ref` varchar(40), `proof_delivered_at` timestamp and `notice_outcome` varchar(20) to `recovery_case`; `notice_outcome` is validated against the outcome list by the service, with no database check constraint on the list value.
- No new table: the timer, the task and the outbox, inbox and idempotency objects already exist in `rwb_case`.
- One index: `ix_recovery_case_notice_ref ON recovery_case (notice_ref)`, so the signal that names the notice reference finds its case without a scan.
- The migration runs in the rwb-case Flyway sequence of the service's own schema (DP-15); no other schema is touched and no foreign key into `rwb_comms` is created.

**Configuration and reference data**

- The SERVICE_LEVEL reference row of the notice-period duration, versioned reference data of rwb-case (RW-COE). The row code and its value are Not specified in the source documents (GAP-0737; ASM-1323).
- The rows R-LIT-07, R-LIT-08 and R-LIT-09 with their action text, owner role and timer spec, in the litigation rule package of rwb-litigation. The package code is Not specified in the source documents (GAP-0737; ASM-1327); the version in force per environment is read from the rwb-decision registry on every evaluation and there is no lock file.
- No parameter of this step is named in the sources; the timeout of 2 s and the single hop are the platform rule of DP-11, not a configurable value of this story.

**Build steps**

1. DeliveryAnswerClient against the RWB-S4-E5002-CON fake, with the 2 s timeout and the breaker; tests for AC1 and AC2.
2. DeliveryAnswerValidator with the required-field checks and the idempotency key; tests for AC1, AC4 and X2.
3. NoticeTransitionService with the three rules and the state guard; tests for AC1, AC2 and AC6.
4. NoticeTimerFactory and NoticeTimerRepository with the SERVICE_LEVEL reference row; test for AC1 and AC2.
5. CaseNoticeRepository, DecisionRecordWriter and CaseStateChangedPublisher in one transaction; tests for AC1, AC4 and AC6.
6. The signal handler of CaseWorkflow and the durable timer with the expiry; test for AC1.
7. The read-only fragment and the composite-route contract test; test for AC8.

**Feature switch.** The legacy story names no feature flag for this behaviour; a switch that turns the step off (the case stays in `NOTICE_DISPATCHED` and the screen shows the state without a timer) is a parameter row read through the parameters contract if an environment needs one.

**Done when.** The tests in section 16 pass, the S4 contract tests stay green, every move carries a decision record that names its rule ID and the package version, and no case has a notice-period timer started from anything other than a delivery date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | The S4 answer carries a required field empty, for example neither a delivery date nor an expiry | Enter {field}. |
| MSG-GEN-006 | The rwb-litigation service does not answer within 2 seconds or is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P3-027 | No litigation rule package version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Litigation R right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-S4-001 | The pack is incomplete when the litigation officer files (served by RWB-S4-E5002-APP) | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim of the case is close to expiry (served by RWB-S4-E5002-APP) | The claim on this case expires on {date}. File before then. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the business date only, never a case fact. For MSG-GEN-006, {system} is "rwb-litigation". MSG-S4-001 and MSG-S4-002 are carried here from the legacy key so that the validation and message table of RWB-E5-002 stays traceable character for character; their owner is the S4 slice and this story neither raises nor changes them. Their English wording is kept character for character from the FSD; the Thai wording is not specified in the source documents (GAP-1748) and is left to the message work DL10 names.

### 15. Screens and states

SCR-18 Notice approval, states Generated; approved; sent; delivered; unserved; empty, loading, error and no access are Not specified in the source documents (CG-ALL-4480): the rwb-case fragment shows the case state and the notice-period end, and when the answer of R-LIT-08 has been applied it shows "unserved" with its reason, read only. SCR-19 Litigation workspace, states Pack; instructed; filed; hearing; judgment; empty, loading, error and no access are Not specified in the source documents (CG-ALL-4481): the same fragment shows the notice-period end from `GET /cases/{caseId}/timers` beside the pack state that rwb-litigation serves.

Both screens are served by the gateway-bff composite route, which calls rwb-case and rwb-comms and rwb-litigation in parallel, one hop each, and merges the answers into the screen model: the notice row and the proof from rwb-comms, the pack state from rwb-litigation, the case state and the timer from rwb-case (DP-19). No screen calls an owner service directly, and the screen writes nothing. The field-level mapping of the notice row, the proof and the barcode stays with P6, and the pack states stay with S4; the full read-only case view, the timer section and the deviation flag remain with RWB-P3-E1023-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-002-01 | RWB-P3-E5002-APP AC1, RWB-P3-E5002-APP AC3, RWB-P3-E5002-APP AC8, BR1, BR3, BR8 | Component | S4 stub proof of delivery for NT-2026-000512-01 with delivered_at 2026-12-14 and served_result delivered; SERVICE_LEVEL row duration; composite-route stub of SCR-18 and SCR-19 |
| TC-E5-002-02 | RWB-P3-E5002-APP AC1, RWB-P3-E5002-APP AC4, BR7 | Component | The same delivery answer delivered twice on the inbox |
| TC-E5-002-03 | RWB-P3-E5002-APP AC2, RWB-P3-E5002-APP AC5, BR2, BR6 | Component | S4 stub expiry answer of the proof window; then the NoPackageInForce answer on a business date with no package |
| TC-E5-002-04 | RWB-P3-E5002-APP AC6, BR5 | Component | Decision-record store stopped on the R-LIT-07 path |
| TC-E5-002-05 | RWB-P3-E5002-APP AC7, BR9 (Access) | Component | RW-REFADM without Litigation R calls GET /cases/{caseId}; case owner with Own scope and a case of another owner |
| TC-E5-002-06 | RWB-P3-E5002-APP AC6, BR5 | NFR | Decision-record write forced to fail on the R-LIT-07 path; the case state, the notice columns and the timer unchanged |
| TC-E5-002-07 | §12 operations, events and activities (contract) | Contract | RWB-S4-E5002-CON fake and schema; the S4 operation, the events and the EvaluateAndApply activity of §12.5 |
| TC-E5-002-08 | §12.7 tables | Boundary | Writes at the column limits of notice_ref and notice_outcome on recovery_case (limits Not specified in the source documents (DOR-RWB-P3-E5002-APP-7)); the timer, task and PLT tables of §12.7 |
| TC-E5-002-09 | BR2b | Component | S4 stub served result refused, returned or undeliverable for NT-2026-000512-01 with the case in NOTICE_DISPATCHED |
| TC-E5-002-10 | BR4 | Component | SERVICE_LEVEL reference row with a changed duration; expiry checked against the delivery date plus that duration |
| TC-E5-002-11 | BR10 | Component | S4 stub answer carrying customer attributes; no ACE view or notice table read |
| TC-E5-002-12 | BR11 | Component | Case in NOTICE_DISPATCHED after R-LIT-07; case status stays In progress |
| TC-E5-002-13 | RWB-P3-E5002-APP AC9 | Component | Request without an rwb-case login on GET /cases/{caseId} for case RW-2026-000512 |
| TC-E5-002-14 | RWB-P3-E5002-APP AC10, BR2b, BR4, BR10, BR11 | Component | S4 stub served result refused for NT-2026-000512-01 with the case in NOTICE_DISPATCHED; SERVICE_LEVEL reference row; no ACE view or notice table read |
| TC-E5-002-15 | RWB-P3-E5002-APP AC11, BR5, BR7 | NFR | EvaluateAndApply activity timeout forced on case RW-2026-000512, then retried; timeout value Not specified in the source documents (NEWAC-RWB-P3-E5002-APP-AC11) |

The legacy levels map System to Component, Access to Component and Resilience to NFR, because the cross-service behaviour of this key is proved by the integration story. The `-ITG` copy of each case is held by RWB-ITG-E5002-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the notice-period duration is a SERVICE_LEVEL reference row, the rule rows R-LIT-07, R-LIT-08 and R-LIT-09 and their timer specs are data, and the package version is read from the rwb-decision registry on every evaluation.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs, notice references and rule IDs, never a name, an account number or an identity number; the workflow payloads pass the payload codec.
- No read of another service's tables: the delivery answer comes from the rwb-litigation contract, the rights from rwb-access; `rwb_case` holds no foreign key into `rwb_comms` and no copy of a notice row, a barcode or a proof document (DP-01).
- No ACE view: the customer attributes a rule needs travel inside the S4 answer, so this step reads no `v_ace_*` view (DP-05, ADR-010).
- One evaluator: R-LIT-07, R-LIT-08 and R-LIT-09 are evaluated once, in rwb-litigation; rwb-case applies the answer and never re-evaluates a rule or reads a rule workbook.
- The decision record is written before the state moves, in one transaction with it; a failed write rolls the whole move back (R-UNI-39).
- NoPackageInForce is never caught and turned into a default state move; the case goes to the exception queue.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).
- The read of the screens writes nothing and raises no event.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None: the Epics 3 to 8 story RWB-E5-002 carries no requirement ID (GAP-0737; ASM-1326) | Record proof of delivery on a notice | Epic 5, module S4 Litigation and enforcement | FEAT-LIT-02 | Litigation stage (see module) | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E5-002-01, TC-E5-002-02, TC-E5-002-03, TC-E5-002-04, TC-E5-002-05, TC-E5-002-06 |
| D-RCV-60 DP-03 | The decision record names the rule and the package version and is written in the same transaction as the state change | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-LIT-02 | Litigation stage | R-UNI-39, R-UNI-41 | TC-E5-002-01, TC-E5-002-03, TC-E5-002-04 |
| D-RCV-60 DP-10 | The notice period is a durable timer of the workflow, not a Quartz row or a polling job | Template and Rules §R5.5; Architecture v5 slide 44 | FEAT-LIT-02 | Litigation stage | R-LIT-07 | TC-E5-002-01, TC-E5-002-02 |
| D-RCV-60 DP-01 | The notice row and the proof are P6's; rwb-case stores only the notice reference, the delivery date and the outcome | Template and Rules §R5.5; Architecture v5 slide 41 | FEAT-LIT-02 | Litigation stage | R-LIT-07, R-LIT-08 | TC-E5-002-01, TC-E5-002-03 |

The feature FEAT-LIT-02 and the rules R-LIT-07, R-LIT-08 and R-LIT-09 are the whole legacy trace of RWB-E5-002, because the story master of Epics 3 to 8 gives it no requirement ID: the requirement IDs are added when the Epics 3 to 8 PRDs are produced (C1), and until then the traceability of this key runs through GAP-0737 and ASM-1326. The FSD S4 module states REQ-S4-001 (demand and recall notices generated by rule, approved, dispatched, and their notice periods timed) for the notice family as a whole, and the A2.2 rule table carries R-LIT-07, R-LIT-08 and R-LIT-09; neither is attached to the story master, so the PRD of EP05 is where the requirement ID of this feature is attached.

### 19. Out of scope

- The notice row, the notice template, the merge fields, the proof of delivery document and the barcode: rwb-comms (P6), owner of `notice`, `template` and `merge_field`.
- The legal action, the hearing, the judgment, the enforcement and the pack of the litigation route, and the creation of a legal action on `/api/recovery/litigation/v1`: rwb-litigation (S4), RWB-S4-E5002-APP.
- The notice approval operation on `/api/recovery/comms/v1`: rwb-comms (P6).
- The evaluation of R-LIT-07, R-LIT-08 and R-LIT-09 itself, and the rule package that carries them: rwb-litigation and rwb-decision.
- The raise of TimerBreached when the notice period ends: RWB-P3-E1028-APP; the tracking and reporting of the notice period and its legal values: the notice-period timer story of this legacy family.
- The four legacy criteria of RWB-E5-002 proved end to end across the three services: RWB-ITG-E5002-ITG.
- The rights, the roles and the scope data themselves (P4 access stories).
- The full read-only case record view, the timer section and the deviation flag (RWB-P3-E1023-APP).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
