# RWB-P3-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E2021-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P3-AI |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2021-CON |
| Contract version | v1 (base path /api/recovery/case/v1, section 12.1); revision Not specified in the source documents (DOR-RWB-P3-E2021-APP-23) |
| Integration dependencies | RWB-ACE-001 (ACE view v_ace_pod read by rwb-source-data for proof of delivery; this story takes the proof as EV-15 from rwb-comms and does not read the view; not yet accepted by the ACE team) |
| External dependencies | None |
| Platform dependencies (DP-added, H; platform CON stories) | RWB-PLT-E1027-CON (DP-03); RWB-PLT-E1043-CON (DP-07); RWB-PLT-TE006-CON (DP-09); RWB-PLT-E1071-CON (DP-10); RWB-PLT-E1044-CON (DP-15); RWB-PLT-N001-CON (DP-19) |
| Service baselines (DP-added) | Not specified in the source documents (GAP-1277) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 26 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a litigation officer (RW-LITOFF) and an enforcement owner (RW-ENFORCE)**, I want **the legal hold placed on the case and lifted again with a reason and returned as a flag on the case read, every dispatch and every proof of delivery written as a ledger entry and shown on the case timeline from the facts `rwb-comms` publishes, and one `NOTICE_UNSERVED` task raised to the case owner when a letter is refused, undeliverable or unproven inside its window**, so that **no letter leaves a case that is on hold, the case itself shows what was posted and what came back, and an undelivered letter always has an owner and an action**.

This is the case slice of legacy RWB-E2-021 (`Split (rework)`, secondary; it owns no legacy criterion — GAP-2217; ASM-3649):

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- It builds three things only: the hold switch that `rwb-comms` reads before writing a letter (`POST /cases/{caseId}/legal-hold`, `legalHold` on `GET /cases/{caseId}`); the letter facts on the case timeline (`GET /cases/{caseId}/timeline`, fed from the interaction ledger through the `rwb-source-data` contract, DP-18); and the one `NOTICE_UNSERVED` task and queue transfer that follow an unserved letter.
- It builds no notice, no template, no merge field, no conduct-check rule, no WIN file, no proof capture and no notice-period timer. The notice, its states and the conduct check are `rwb-comms`'s (RWB-P6-E2021-APP, built against RWB-P6-E2021-CON and its fake); the notice-period clock from the delivery date is RWB-P3-E5002-APP; the deviation contact stop is `rwb-deviation`'s; the ledger record is `rwb-source-data`'s; the central decision ledger is `rwb-decision`'s.

### 2. Business rationale

A notice period counted from a print date can be challenged, and a letter that leaves a case on legal hold is a conduct breach. In the split, one service must own the two facts the rest of the loop depends on — whether a letter may leave this case at all, and what happened to it afterwards on the case record. Keeping them in `rwb-case` means `rwb-comms` needs one published read and no table, and it means the officer sees the dispatch and the proof on the same timeline as every other case event, without a cross-service join. It serves REQ-OCC-005 (a conduct result on every outbound contact), REQ-ILG-010 (dispatch results in the ledger) and the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- The case exists in `rwb_case` with its owner, queue and status; the ACE business keys (`account_key`, `person_key`) are on the case and are read as keys only, never as a foreign key.
- RWB-P6-E2021-CON is published; this story is built against that contract and its fake, never against a live `rwb-comms` (DP-11, DP-09).
- The `rwb-source-data` ledger contract is published and its fake is available; the case holds no `interaction` table (DP-18; GAP-2221; ASM-3653).
- The platform decision-record library (DP-03), the outbox and inbox library (DP-09), the workflow kit (DP-10) and the gateway-bff composite route (DP-19) are in place from wave 0 (ASM-3655).
- The requester holds a role with Case record U to place or lift a hold and Case record R to read the case and its timeline (TSD P3 T6.1). Scope is applied to every read.
- The hold reason list, the `SERVICE_LEVEL` row for the task due date and the LOV values used here are in force as reference data of `rwb-case` (DP-07; GAP-2218 and GAP-2222).

### 4. Flow

1. Litigation officer opens the case: `GET /api/recovery/case/v1/cases/{caseId}` returns the case with `legalHold`, `status`, `status_before_hold`, the owner, the queue and the next action; the gateway composes it with the other tabs over the DP-19 route.
2. Case owner or litigation officer places a legal hold: `POST /cases/{caseId}/legal-hold`. The service writes one decision record (R-UNI-20), keeps the status it held in `status_before_hold`, moves the case to `ON_HOLD`, and inserts `rwb.case.CaseStateChanged.v1` in the outbox of the same transaction.
3. `rwb-comms` reads the case through the published case contract before each letter; the `legalHold` flag is the case-side input of its conduct check. This story provides the flag only; the check, its held reason and the file are P6's.
4. `rwb-comms` publishes `rwb.comms.NoticeDispatched.v1` with the notice, the barcode and its conduct result. The rwb-case inbox applies it: one ledger entry through the `rwb-source-data` contract (channel `LETTER`, conduct check `PASSED`, barcode in the summary). The case status does not move.
5. `rwb-comms` publishes `rwb.comms.NoticeDelivered.v1` with `DELIVERED` and the call-back date. The inbox writes the delivery ledger entry dated on the call-back date; the notice period from that date is started by RWB-P3-E5002-APP, not here.
6. The same event with `REFUSED`, `UNDELIVERABLE` or `PENDING` (an unproven letter): the inbox writes the ledger entry, one decision record (decision code `D7.1`, rule R-LIT-09), places the case in its owner's queue with the reason `NOTICE_UNSERVED`, raises one `OPEN` task `NOTICE_UNSERVED` to the case owner, sets the next action and inserts `rwb.case.CaseTransferred.v1` in the outbox.
7. The officer reads the letter facts on SCR-04: `GET /cases/{caseId}/timeline` merges the case's own events with the ledger entries of the case, in time order. Lifting the hold on the case returns it to the status in `status_before_hold` (R-UNI-21) and publishes `CaseStateChanged`.

Screen states for SCR-04 and SCR-18: no access returns MSG-P4-002 (403) and a case out of scope returns MSG-P4-003; an error on a decision-record write returns MSG-P7-003. The empty states of SCR-04 and SCR-18 are Not specified in the source documents (DOR-RWB-P3-E2021-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision-record or ledger write fails for a dispatch, proof or unserved fact | Nothing is applied; the event stays unacknowledged and is retried; an incident is raised under R-UNI-39 | MSG-P7-003 | AC8 |
| X2 | The same P6 event is delivered twice (relay retry, replay) | The inbox deduplicates on event ID and business date; one ledger entry, one task, one decision record, one event | None | AC6 |
| X3 | The case is outside the caller's scope | Refused; no ledger entry is returned | MSG-P4-003 | AC9 |
| X4 | A hold is placed on a case already `ON_HOLD`, or lifted where there is none | Refused; nothing changes | MSG-P3-005 | AC2 |
| X5 | The `rwb-source-data` ledger contract is down or answers beyond 2 s | The fact is not applied and the event is retried by the inbox; no task is raised before its ledger entry exists | MSG-P7-003 | AC8 |
| X6 | The P6 read that the case record composes times out or the breaker is open | The case answer still returns `legalHold` and the case facts; the notice panel shows a retry state and no fact is fabricated | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E2021-CON and its fake; no in-lane story is waited for (Day 1) |
| Negotiable | The hold reason list, the task code, the owner role and the task due date are data, not code |
| Valuable | Two facts the loop cannot work without — may this letter leave, and what happened to it — sit on the case |
| Estimable | One operation, one flag, one timeline query, one consumer, one activity and one screen fragment |
| Small | Fits in two weeks with its tests |
| Testable | Every criterion runs against the P6, ledger and gateway fakes with synthetic notices |

### 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN, case side

  Background:
    Given case "RC-2026-000321" is "IN_PROGRESS" with owner "LIT-0101"
    And the rwb-comms contract mock and the rwb-source-data ledger mock are running

  Scenario: AC1 Legal hold stops every letter on the case (new, D-RCV-60)
    Given case "RC-2026-000321" is "IN_PROGRESS" with legal hold false
    When "LIT-0101" places a legal hold with a reason through POST /api/recovery/case/v1/cases/RC-2026-000321/legal-hold
    Then the case is "ON_HOLD" with status_before_hold "IN_PROGRESS" and legalHold true
    Then one decision record exists with rule "R-UNI-20" and the package version in force
    Then GET /api/recovery/case/v1/cases/RC-2026-000321 returns legalHold true and status "ON_HOLD"
    Then the CaseStateChanged event carries the case number, fromState "IN_PROGRESS" and toState "ON_HOLD" only

  Scenario: AC2 Lifting the hold returns the case to the status it held (new, D-RCV-60)
    Given case "RC-2026-000321" is "ON_HOLD" with status_before_hold "IN_PROGRESS" and legalHold true
    When "LIT-0101" lifts the hold through POST /api/recovery/case/v1/cases/RC-2026-000321/legal-hold
    Then the case is "IN_PROGRESS" with legalHold false
    Then one decision record exists with rule "R-UNI-21"
    When "LIT-0101" lifts the hold a second time
    Then the call is refused with MSG-P3-005 and the case is unchanged

  Scenario: AC3 A dispatch is on the case timeline with its conduct result (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0101" for case "RC-2026-000321" with barcode "RR223344556TH", sent date 2026-12-15 and conduct check "PASSED"
    When rwb-case consumes NoticeDispatched for "N-0101"
    Then one ledger entry exists for case "RC-2026-000321" with channel "LETTER", conduct check "PASSED" and a summary naming "RR223344556TH"
    Then GET /api/recovery/case/v1/cases/RC-2026-000321/timeline returns that entry with the barcode
    Then the case status stays "IN_PROGRESS"
    Then no name, address or notice text appears in the event, the ledger summary or the log line

  Scenario: AC4 A proof of delivery is on the case timeline on the call-back date (new, D-RCV-60)
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the rwb-comms contract mock returns NoticeDelivered for "N-0101" with result "DELIVERED" and call-back date 2026-12-18
    Then the timeline shows a delivery entry on 2026-12-18 with delivery status "DELIVERED"
    Then the case status stays "IN_PROGRESS"
    Then rwb-case starts no timer of its own for the notice period

  Scenario: AC5 An unserved letter raises one task and one queue transfer (new, D-RCV-60)
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the rwb-comms contract mock returns NoticeDelivered for "N-0101" with result "UNDELIVERABLE"
    Then exactly one task "NOTICE_UNSERVED" is "OPEN" on case "RC-2026-000321" with the case owner role
    Then the task due date is read from the SERVICE_LEVEL reference row in force
    Then the case is placed in its owner's queue with the reason "NOTICE_UNSERVED"
    Then one decision record exists with decision code "D7.1" and rule "R-LIT-09"
    Then the case next action names "NOTICE_UNSERVED" and the owner sees MSG-P6-008 for notice type "DEMAND" and result "UNDELIVERABLE"
    Then the CaseTransferred event carries the case number and the reason "NOTICE_UNSERVED"

  Scenario: AC6 A repeated result changes nothing (new, D-RCV-60)
    Given the unserved result of "N-0101" for business date 2026-12-21 was applied
    When the same event is delivered again with the same event ID
    Then case "RC-2026-000321" has one "NOTICE_UNSERVED" task, one ledger entry and one decision record
    Then no second CaseTransferred event is published

  Scenario: AC7 An unproven letter is unserved and a letter inside its window is not (new, D-RCV-60)
    Given notice "N-0102" for case "RC-2026-000654" is "Sent" with sent date 2026-12-15
    And notice "N-0103" for case "RC-2026-000655" is "Sent" with sent date 2026-12-16
    When the rwb-comms contract mock returns NoticeDelivered for "N-0102" with result "PENDING" on 2026-12-22
    Then case "RC-2026-000654" has the "NOTICE_UNSERVED" task and one decision record with rule "R-LIT-08"
    Then case "RC-2026-000655" has no "NOTICE_UNSERVED" task
    Then no notice-period entry appears on either timeline

  Scenario: AC8 Nothing is applied when the decision cannot be recorded (new, D-RCV-60)
    Given the rwb-source-data ledger mock is unavailable
    When NoticeDelivered for "N-0101" with result "UNDELIVERABLE" arrives
    Then case "RC-2026-000321" is unchanged: no task, no queue move and no next action
    Then the consumer record shows MSG-P7-003 and the event stays unacknowledged for retry
    Then one incident is raised under rule "R-UNI-39"

  Scenario: AC9 The timeline of a case outside the caller's scope (new, D-RCV-60)
    Given case "RC-2026-000321" is outside the scope of "LIT-0101"
    When "LIT-0101" sends GET /api/recovery/case/v1/cases/RC-2026-000321/timeline
    Then the response is status 404 with MSG-P4-003
    Then no ledger entry is returned

  Scenario: AC10 Only the delivery date starts the notice-period clock (new, D-RCV-60)
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the rwb-comms contract mock returns NoticeDelivered for "N-0101" with result "UNDELIVERABLE"
    Then no NOTICE_PERIOD timer is started on case "RC-2026-000321"
    Then the task due date for "NOTICE_UNSERVED" comes from the SERVICE_LEVEL reference row in force and no value is held in code

  Scenario: AC11 A caller without access is refused (new, D-RCV-60)
    Given the requester holds no Case record R role
    When the requester sends GET /api/recovery/case/v1/cases/RC-2026-000321/timeline
    Then the response is status 403 with MSG-P4-002
    Then an unauthenticated call returns status 401 with a message code Not specified in the source documents (NEWAC-RWB-P3-E2021-APP-AC14)

  Scenario: AC12 A replayed write changes nothing (new, D-RCV-60)
    Given case "RC-2026-000321" is "IN_PROGRESS" with legal hold false
    When "LIT-0101" sends POST /api/recovery/case/v1/cases/RC-2026-000321/legal-hold twice with the same idempotency key
    Then the case is "ON_HOLD" with one decision record for the hold
    Then the second call writes nothing; the idempotency key header is Not specified in the source documents (NEWAC-RWB-P3-E2021-APP-AC15)
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A legal hold on a case stops every outbound action on it and every letter for it | R-UNI-20; REQ-OCC-005 | AC1 |
| BR2 | Lifting the hold returns the case to the status it held when the hold was placed, and the move is recorded | R-UNI-21 | AC2 |
| BR3 | The case exposes the hold as one flag on its published read; no other service reads the case tables for it | R-PREC (Arch v5 catalogue); DP-01 | AC1 |
| BR4 | Every dispatch and every proof of delivery is one ledger entry for the case, with its channel, conduct result and delivery status | REQ-ILG-010; FEAT-ILG-07 | AC3, AC4 |
| BR5 | A refused, returned or undeliverable letter records the result and moves the case to its owner with an action, under R-LIT-09 | R-LIT-09; CTL-15 | AC5 |
| BR6 | No notice-period clock is started from a print date or from an unserved letter; the clock is the E5002 story's and starts from the delivery date | R-LIT-07; R-LIT-08 | AC4, AC10 |
| BR7 | A held or unserved result that cannot be written to the decision record does not proceed | Principle 5; R-UNI-39 | AC8 |
| BR8 | Which hold reasons, task codes and due dates apply is data held as reference data, never code | Principle 1; LOV-ROLE; GAP-2218 | AC10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Any active status | Legal hold placed | R-UNI-20; the case is not `CLOSED` | `ON_HOLD`, with the previous status kept in `status_before_hold` |
| `ON_HOLD` | Legal hold lifted | R-UNI-21 | The status in `status_before_hold` |
| `ON_HOLD` | Legal hold placed or lifted twice | The case is already in the target state | No change; refused with MSG-P3-005 |

The notice state (`Approved`, `Sent`, `Delivered`, `Unserved`, `Held`) is `rwb-comms`'s and is never held in `rwb_case`: this story writes the case status, the task, the next action and the ledger reference only. Task status moves `OPEN` to `DONE` or `CANCELED` through the existing task operation of RWB-P3-E2035.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Places and lifts a hold (Case record U); reads the case and the timeline; works the `NOTICE_UNSERVED` task |
| RW-LITOFF, litigation officer | Places and lifts a hold (Case record U); reads the dispatch and the proof on the timeline |
| RW-ENFORCE, enforcement owner | Places and lifts a hold; reads the timeline |
| RW-TEAMMGR, RW-LEGAL, RW-HEADLIT, RW-HEADNPA | Read the case, the hold and the timeline (Case record R) |
| RW-CONDUCT, Conduct and QA officer | Reads the timeline entries with their conduct result (Case record R) |
| SY-CASEWF, case workflow module | Applies the P6 facts, the task, the queue transfer and the outbox rows |

No approval level from the delegation of authority applies in this story; approval of the notice itself is RWB-P3-E2014-APP and RWB-P6-E2021-APP. The notice approval is held in the ApprovalWorkflow of rwb-decision; POST /notices/{noticeId}/approve is the decision point; the notice waits in Approved and is not written to the file (GAP-2093).

Each REST operation of this story is authorised by the rwb-access authorise check of DP-08 for the role that calls it; the check's identifier is Not specified in the source documents (DOR-RWB-P3-E2021-APP-6).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Write |
| DF-CAS-010 | recovery_case | queue_id | Write |
| DF-CAS-020 | recovery_case | legal_hold | Read, write |
| DF-CAS-055 | recovery_case | status_before_hold | Write |
| DF-CAS-049 | recovery_case | next_action_text | Write |
| DF-CAS-050 | recovery_case | next_action_owner_role | Write |
| DF-CAS-051 | recovery_case | next_action_due_date | Write |
| DF-CAS-053 | recovery_case | next_action_waiting | Write |
| DF-WRK-017 to DF-WRK-026 | task | id, case_id, task_code, status, owner_role, due_at, outcome_code | Write |
| DF-WRK-009 to DF-WRK-015 | assignment | case_id, assignee_user_id, assigned_at, reason | Write, through the case's own assignment record |
| DF-INT-005, DF-INT-011, DF-INT-012, DF-INT-028 | interaction | channel, summary, conduct_check, delivery_status | Write and read, through the `rwb-source-data` ledger contract only (DP-18) |
| DF-REF-147 to DF-REF-158 | parameter_value, reference_row | The `SERVICE_LEVEL` row and the hold reason list | Read, through the reference-data contract (DP-07) |

Personal data: none is copied into this service's letter facts. The ledger summary carries the case number, the notice type, the barcode and the result code, never a name, an address or notice text.

### 12. Contract

#### 12.1 REST operations provided

All on base `/api/recovery/case/v1`, owner `rwb-case` (P3).

| Method | Path | Purpose | Access |
|---|---|---|---|
| POST | `/cases/{caseId}/legal-hold` | Place or lift the legal hold on the case: body `hold` (boolean, required), `reason` (string, required on place) | Case record U |
| GET | `/cases/{caseId}` | The case read, extended with `legalHold`, `statusBeforeHold`, the next action and the case's queue | Case record R, scope applied |
| GET | `/cases/{caseId}/timeline` | The case timeline: the case's own events merged with the ledger entries of the case, in time order, paged | Case record R, scope applied |
| GET | `/me/tasks` | The caller's tasks, which include `NOTICE_UNSERVED` (existing operation, unchanged) | Case record R |
| PATCH | `/tasks/{taskId}` | Closes or cancels the `NOTICE_UNSERVED` task with an outcome code (existing operation, unchanged) | Case record U |

Errors: 401 no session; 403 role without Case record U (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 409 the case is already in the target state (MSG-P3-005); 422 a field fails (MSG-GEN-001); 503 the decision record cannot be written (MSG-P7-003). `POST /cases/{caseId}/legal-hold` is idempotent by the case ID and the target state.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| Not specified in the source documents (GAP-2220; ASM-3652) | The interaction write and the case-read operations of the `rwb-source-data` contract | rwb-source-data (P1) | Writing the dispatch, the proof and the unserved entry; reading the case's ledger entries for the timeline (DP-18) | One hop, 2 s, breaker |
| Not specified in the source documents (GAP-2220; ASM-3652) | The keep-safe cases read of the `rwb-comms` contract, fixed by RWB-P6-E2021-CON | rwb-comms (P6) | Nothing is called for the letter facts: they arrive as events; the notice read is used only to show the notice type on the timeline, built against the contract fake (DP-11) | One hop, 2 s, breaker |
| Not specified in the source documents (GAP-2220; ASM-3652) | The decision-record write and seal operations of the `rwb-decision` contract, owned by `rwb-decision` on base `/api/recovery/decision/v1` | rwb-decision (P7) | The central seal of the decision record written locally (DP-03) | One hop, 2 s |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, decisionLogEntryId, fromState, ruleId (R-UNI-20, R-UNI-21), toState |
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, fromOwner, reasonCode (`NOTICE_UNSERVED`), toOwner |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the ledger; every service writes its own record | caseId | decision record reference, decision code (`D7.1` where a rule decided the notice outcome), ruleId, packageVersion, business date |

All three are written to the outbox in the same transaction as the change and relayed with the CloudEvents envelope (DP-09). No payload carries a name, an address, a notice text or a barcode beyond the notice reference.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 | Inbox: one ledger entry with channel `LETTER`, the conduct result, the barcode in the summary and the sent date |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 | Inbox: the delivery entry (`DELIVERED`, with the call-back date), or the unserved entry with the task, the decision record and the queue transfer (`REFUSED`, `UNDELIVERABLE`, `PENDING`) |

Both are consumed with the inbox object and the idempotency key `noticeId` + business date, so a relay retry or a replay applies nothing twice (DP-09).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID `case-{caseId}`) | `rwb-case` | Receives the signal that carries one P6 letter fact and runs the apply step; holds no Quartz trigger (DP-10) |
| ApplyNoticeFact | Activity (the one activity this story adds) | `rwb-case` | Validates the fact, calls the ledger contract, and writes the case status or the task, the decision record and the outbox rows in one transaction |

No other workflow and no other activity is added. The letter fact is applied by an event-started workflow, not a schedule, and the workflow reads no clock and calls no rule engine.

#### 12.6 Schedules

None. The legacy behaviour sat in `JOB-10` (daily 16:00), which is `rwb-comms`'s; on the case side the fact arrives as an event and the workflow is started by it (DP-10). `rwb-case` owns no schedule for the letter loop.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (`rwb_case`) | Writes `status`, `status_before_hold`, `legal_hold`, `queue_id` and the next-action columns; no new column and no new table |
| task | P3 (`rwb_case`) | The `NOTICE_UNSERVED` task row: `task_code`, `status`, `owner_role`, `due_at`, `outcome_code` |
| assignment | P3 (`rwb_case`) | The queue placement of the case after an unserved letter, with its reason |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_case` | Outbox, inbox and idempotency objects (DP-09) |
| decision_record | PLT library, created in `rwb_case` | The local hash-linked decision record of the change (DP-03) |

`interaction` is **not** owned here: the ledger belongs to `rwb-source-data` under DP-18 and the R-PREC default ruling, so there is no `interaction` table in `rwb_case`, no view over it and no foreign key to it (GAP-2221; ASM-3653). `notice`, `template` and `merge_field` are `rwb_comms`'s and are neither read nor written. `decision_log_entry` is `rwb-decision`'s and is reached only through its contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms WireMock and event stub | RWB-P6-E2021-CON | A dispatch for "N-0101" with barcode "RR223344556TH", sent date 2026-12-15 and conduct `PASSED`; a delivery on 2026-12-18; `UNDELIVERABLE`; `PENDING` on 2026-12-22; a duplicate delivery with the same event ID; a delayed answer beyond 2 s |
| rwb-source-data WireMock | The P1 ledger contract | A successful write with a returned reference; a case ledger with two entries; an unavailable answer for AC8 |
| rwb-decision WireMock | The P7 decision-record contract | A successful seal; an unavailable answer for AC8 |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-04 and the case record view | The merged case and timeline answers of AC1, AC3 and AC4, including the retry state of X6 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed groups | The hold operation, the case read and the timeline provided; the ledger, the notice read and the decision-record seal consumed; one hop, 2 s, breaker |
| Kafka | 3 published, 2 consumed | `rwb.case.events.v1` (two types), `rwb.decision-record.v1`, and the two `rwb.comms` facts consumed with the inbox |
| Temporal | 1 workflow, 1 activity | CaseWorkflow per case; ApplyNoticeFact |
| File | None | No file is read or written by this story; the WIN file is `rwb-comms`'s |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `letterloop`, Java package `th.co.scb.ace.workbench.recovery.case.letterloop`; front-end fragment `src/modules/recovery/case/NoticeTimeline.tsx`, embedded in SCR-04 and the case record view.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform edges this table adds belong to wave-0 CON stories that are already in place and are not repeated as H rows in the metadata table, which carries only the contract dependency of this legacy key (ASM-3655). DP-07 resolves to the reference-data contract of `rwb-case` built in wave 1 (RWB-P3-E1043-CON), so no new dependency is added. DP-05 resolves to one ACE read: the account number shown with the letter facts is read from `v_ace_account` by `case_account.account_key`, inside `rwb_case`, with no copy and no foreign key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseHoldController | Controller | `POST /cases/{caseId}/legal-hold` and the `legalHold` field of the case read |
| CaseHoldService | Service | Applies R-UNI-20 and R-UNI-21, keeps `status_before_hold`, refuses a repeat with MSG-P3-005, writes the decision record |
| NoticeFactConsumer | Inbox consumer | Consumes EV-14 and EV-15, deduplicates by event ID and business date, signals CaseWorkflow; EV-15 NoticeDelivered is published by rwb-comms when a proof is matched to its notice by barcode |
| NoticeFactValidator | Service | Required fields of the fact (noticeRef, caseRef, result, date), builds the idempotency key, refuses an unreadable fact with MSG-GEN-001 |
| ApplyNoticeFact | Activity | The one transaction: ledger entry, decision record, task, next action, queue placement, outbox rows |
| LedgerClient | Client | The `rwb-source-data` contract with one hop, 2 s and a breaker; no retry of its own (the workflow owns retry) |
| NoticeTaskFactory | Service | The `NOTICE_UNSERVED` task row: owner role from `LOV-ROLE`, due date from the `SERVICE_LEVEL` row (DP-07) |
| CaseTimelineQuery | Query | Merges the case's own events with the ledger entries of the case for `GET /cases/{caseId}/timeline` (DP-18) |
| DecisionRecordWriter | Library adapter | Local hash-linked record with the rule ID and package version, in the same transaction (DP-03) |
| CaseEventPublisher | Outbox adapter | Inserts CaseStateChanged, CaseTransferred and DecisionRecorded in the outbox (DP-09) |
| NoticeTimeline | React component | The SCR-04 fragment: dispatch, delivery and unserved entries with their conduct result, read only |

**Database and migrations**

- No new table and no new column: `legal_hold`, `status_before_hold`, the next-action columns, `task` and `assignment` already exist in `rwb_case`.
- One index only: `ix_task_case_code ON task (case_id, task_code)` so the consumer finds an existing `NOTICE_UNSERVED` task without a scan (idempotency).
- Migration `Not specified in the source documents (CG-ALL-4270)` runs in the service's own migration sequence with a parameterised schema name; no other schema is touched and no foreign key into `rwb_comms` (owned by rwb-comms) or `rwb_source_data` (owned by rwb-source-data) is created.

**Configuration and reference data**

- The `SERVICE_LEVEL` reference row that gives the `NOTICE_UNSERVED` task its due date. The row code and its value are Not specified in the source documents (GAP-2218; ASM-3650).
- The hold reason list and its codes, as a reference table of `rwb-case`; the list is Not specified in the source documents (GAP-2222; ASM-3654).
- No feature flag of its own: the legacy flag `rwb.comms.win-dispatch-loop` is P6's, and a key for this slice is Not specified in the source documents (GAP-2219; ASM-3651).
- The 2 s timeout and the single hop are the platform rule of DP-11, not a configurable value of this story.
- The conduct and consent rule package is one versioned package governed in rwb-decision; this story records the conduct result on each entry (BR4). The package identifier is Not specified in the source documents (GAP-1610).

**Build steps**

1. CaseHoldController and CaseHoldService with R-UNI-20 and R-UNI-21, the repeat refusal and the decision record; tests for AC1 and AC2.
2. NoticeFactConsumer with the inbox, the dedupe key and the signal; tests for AC6.
3. NoticeFactValidator and the ledger write in `ApplyNoticeFact`; tests for AC3, AC4 and AC8.
4. NoticeTaskFactory, the next action and the queue placement with reason `NOTICE_UNSERVED`; tests for AC5 and AC7.
5. CaseTimelineQuery and the `NoticeTimeline` fragment against the gateway route fake; tests for AC3, AC4 and AC9.
6. Decision-record and outbox wiring in the one transaction, with the incident on failure; tests for AC8.

**Done when.** The tests in section 16 pass, the RWB-P6-E2021-CON contract tests stay green, every move and every unserved letter carries a decision record with its rule ID and package version, and no letter fact is stored in `rwb_case` outside the ledger reference.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-005 | A hold is placed on a case already `ON_HOLD`, or lifted where there is none | This case cannot move to {state} from {current}. |
| MSG-P6-005 | Not specified in the source documents (GAP-1096) | Not specified in the source documents (GAP-1096) |
| MSG-P3-004 | A legal hold or deviation blocks the letter (read by the P6 check from this flag) | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | Not specified in the source documents (DOR-RWB-P3-E2021-APP-9) | Not specified in the source documents (DOR-RWB-P3-E2021-APP-9) |
| MSG-GEN-001 | A required field of the fact or the request is missing | Enter {field}. |

### 15. Screens and states

| Screen | What the user sees and does |
|---|---|
| SCR-04 Case timeline | One row per event and per ledger entry of the case, in time order: the dispatch with its conduct result and barcode, the delivery with the call-back date, the unserved result with its reason. Read only; loaded on click over the DP-19 composite route. Loading: as Screen Specifications v1 states it; empty, error and no access: Not specified in the source documents (CG-ALL-4271). |
| Case record view | The hold banner with `legalHold`, the status `ON_HOLD`, the next action `NOTICE_UNSERVED` and its due date; the hold is placed and lifted from here with a reason |
| SCR-18 Notice approval (P6) | Unchanged; the notice states it shows are `rwb-comms`'s. This story adds the hold banner that tells the officer why a letter cannot go. Empty, loading, error and no access: Not specified in the source documents (CG-ALL-4272). |

### 16. Test cases

The 14 legacy case IDs are kept. The AC numbers in Covers are the legacy RWB-E2-021 criteria, whose primary story is RWB-P6-E2021-APP; the second AC number is the case-side criterion of this file that runs the same data.

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | Legacy AC1; AC3 here | Component | N-0101 Approved; acknowledgment RR223344556TH |
| TC-E2-021-02 | Legacy AC2; AC4 here | Component | INT-15 DELIVERED, call-back 18122026 |
| TC-E2-021-03 | Legacy AC3; AC5 here | Component | INT-15 UNDELIVERABLE |
| TC-E2-021-04 | Legacy AC4; the hold flag only (AC1), the contact stop stays with P6 | Contract | Open X1 with contact stop |
| TC-E2-021-05 | Legacy AC5; no case-side step | Contract | Postal consent WITHDRAWN, DEMAND notice |
| TC-E2-021-06 | Legacy AC6; AC7 here | Component | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; fact applied on 2026-12-22 |
| TC-E2-021-07 | Legacy AC7; AC1 here | Component | Legal hold true |
| TC-E2-021-08 | Legacy AC8; no case-side step | Contract | DEMAND-SSME TH v1 withdrawn 2026-12-13 |
| TC-E2-021-09 | Legacy AC9; AC8 here | Component | Open X2 with stop; ledger mock stubbed unavailable |
| TC-E2-021-10 | Legacy AC10; AC6 here | Component | The same delivery event delivered twice with one event ID |
| TC-E2-021-11 | Legacy AC11; AC9 here | Contract | N-0200 outside scope |
| TC-E2-021-12 | Legacy AC12; no case-side step | Contract | POST with no notice type |
| TC-E2-021-13 | Legacy AC11 access; AC9 here | Contract | RW-CASEOWN sends the timeline read outside scope; refused with MSG-P4-003 |
| TC-E2-021-14 | Legacy principle 5; AC8 here | NFR | Ledger and decision-record writes forced to fail on 10 unserved facts; no case changes |
| TC-E2-021-15 | New; section 12.7 table boundary (ASM-3438) | Component | Write to `interaction` from rwb_case; refused |
| TC-E2-021-16 | New; AC10 here (BR6, BR8) | Component | N-0101 Sent 2026-12-15; NoticeDelivered UNDELIVERABLE; SERVICE_LEVEL row in force |
| TC-E2-021-17 | New; AC11 here | Contract | Requester without Case record R reads the timeline; unauthenticated call |
| TC-E2-021-18 | New; AC12 here | Contract | POST legal-hold sent twice with one idempotency key |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the hold reason list, the task code, the owner role and the task due date are data rows with a version.
- No personal data in events, workflow inputs, ledger summaries or logs: the case number, the notice reference, the barcode and the result code only.
- No read of another service's tables: the ledger goes through `rwb-source-data`, the letter facts through `rwb-comms`, the decision record through its own library and seal. ACE data only through `v_ace_*` views, read only.
- The ledger write, the decision record and the outbox row commit in one transaction, so a stop or a hold raised after a fact is applied reaches the next one and no half state exists.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-06, TC-E2-021-10, TC-E2-021-11, TC-E2-021-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-UNI-20, R-UNI-21, R-LIT-09 | TC-E2-021-04, TC-E2-021-07, TC-E2-021-09, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-13 |

### 19. Out of scope

- Notice generation, template and merge fields (RWB-P6-E2021-APP, RWB-P3-E1052-APP).
- The conduct check itself, the WIN file, the acknowledgment and the proof capture: `rwb-comms`'s.
- The notice-period clock from the delivery date: RWB-P3-E5002-APP.
- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- SMS and LINE dispatch (RWB-E2-022); notice approval (RWB-P3-E2014-APP, RWB-E2-014 as reworked).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
