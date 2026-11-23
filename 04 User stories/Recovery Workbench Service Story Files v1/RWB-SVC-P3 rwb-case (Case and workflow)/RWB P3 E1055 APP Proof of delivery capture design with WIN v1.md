# RWB-P3-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1055-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P3-S |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1055-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-OCC-003, REQ-ILG-004, REQ-DRI-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the proof-of-delivery fact that `rwb-comms` publishes to start one durable `NOTICE_PERIOD` clock on the case, dated from the day the customer actually received the notice and as long as the product's notice period in force, with the notice reference and the two dates on the timer read and nothing of the notice itself copied into `rwb_case`**, so that **the notice period is counted from delivery rather than from a print date or a phone call, a late or replayed fact does not move the clock, and the case shows a deadline a court can accept**.

This is the rwb-case slice of legacy RWB-E1-055 (`Split (rework)`, secondary; it owns no legacy criterion - GAP-2247; ASM-3704):

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- It builds one thing of its own: the `NOTICE_PERIOD` timer of a case, started by the `rwb.comms.NoticeDelivered.v1` fact, dated from the delivered date the fact carries, held by a durable Temporal timer inside `CaseWorkflow`, projected on the `timer` row of `rwb_case` and served by the existing case reads.
- It builds no WIN file, no notice, no template, no barcode reconciliation and no proof row: the daily 16:00 file to WIN (JOB-10), the acknowledgment, the proof read from the DP07 records and the REC-05 break list are `rwb-comms`'s (RWB-P6-E1055-APP, built against RWB-P6-E1055-CON and its fake); the pod rows, the freshness answer and the interaction ledger are `rwb-source-data`'s (DP-18); the stored letter is `rwb-document`'s.

### 2. Business rationale

A notice period counted from a print date can be challenged, and proof of delivery is chased by phone today. Legacy RWB-E1-055 fixed the loop at WIN and named the case-side owner of the clock in one line: "P3 starts the NOTICE_PERIOD timer when it consumes NoticeDelivered (EV-15)". In the monolith that line was a call into the case workflow module inside one deployment; in the target the fact arrives on `rwb.comms.events.v1` and the clock is a durable Temporal timer on task queue `rwb-case` (DP-09, DP-10), so a period that ends next month still fires once and on time after several releases of both services.

The split keeps the two services independent. `rwb-comms` owns the notice, its states and the proof; `rwb-case` owns the case of record and the clock. It stores the notice reference and the two dates on the timer row and never the notice state, the barcode or the address: the notice panel is composed from the `rwb-comms` answer over the gateway-bff route (DP-11, DP-19), and no table of `rwb_comms`, `rwb_source_data` or `rwb_document` is read or joined (DP-01).

It serves REQ-OCC-003 (letters dispatched for print and post, proof of delivery returns to the case), REQ-ILG-004 (what happened in an interaction is recorded) and REQ-DRI-006 (files move only through the integration adapters, so no file is touched here), and it carries the case-side half of the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- RWB-P6-E1055-CON is published: the notice read with its dispatch and proof fields, the delivery-status list and the event envelope of `rwb.comms.NoticeDelivered.v1`, with its fake. This story is built against that contract and never against a live `rwb-comms`.
- The case exists in `rwb_case` with its product group, queue, owner and status, and the notice is linked to it by `caseId` on the fact.
- RWB-PLT-TE006-CON (outbox, inbox and idempotency, CloudEvents 1.0, retry and `.dlt` topics), RWB-PLT-E1071-CON (workflow kit, namespace `rwb-recovery`), RWB-PLT-E1044-CON (per-service Flyway), RWB-PLT-E1043-CON (reference-data client) and RWB-PLT-N001-CON (gateway-bff composite route) are in place from wave 0.
- The `NOTICE_PERIOD` type is in LOV-TIMER and the states in LOV-TIMER-STATUS (RUNNING, PAUSED, EXPIRED, STOPPED), read through the reference-data contract of `rwb-case` (DP-07).
- The `NOTICE_PERIOD_DAYS` product parameter of the product group is in force on the delivered date, with its unit, and within the catalog range 1 to 365. Test values: `MORTGAGE` 30 calendar days and `HIRE_PURCHASE` 60 calendar days, PRODUCT_PARAMETER version 2 (RWB-P3-E1045-APP); the values are the business lead's.
- The `SERVICE_LEVEL` row in force for the case's queue and status names the escalation role that receives the expiry. The role of a notice period with no matching row is Not specified in the source documents (GAP-2248; ASM-3705).
- The `timer` row and its projection columns exist in `rwb_case` (RWB-P3-E1028-APP); this story adds the notice reference and its index.
- The login is the rwb-case login (DP-02): one login, one connection pool, grants on `rwb_case` only. The case is in the caller's scope and the caller holds Case record R; `rwb-access` answers through its authorise contract, cached per request.

### 4. Flow

1. `NoticeFactConsumer` consumes `rwb.comms.NoticeDelivered.v1` from `rwb.comms.events.v1`, dedupes it in the inbox of `rwb_case` on the event ID and on the business key, and signals `CaseWorkflow` with the case ID, the notice reference and the delivered date.
2. `CaseWorkflow` reads the case row, refuses a fact whose case is closed, and asks `StartNoticePeriod` for the due date.
3. `CalculateDueDate` reads `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", deliveredDate)` in the service's own schema and adds the days in the unit of the same answer (DP-01; RWB-P3-E1045-APP). No row in force is a refusal, not a default.
4. `StartNoticePeriod` stops any running `NOTICE_PERIOD` timer of the case, computes `expires_at` from the delivered date and not from the processing date, and asks `WriteNoticeTimer`.
5. `WriteNoticeTimer` writes the `timer` row (`NOTICE_PERIOD`, `started_at` = delivered date, `expires_at`, `status` RUNNING, `paused` false, escalation level 0, `reference_ref` = notice reference) and the outbox row in one transaction, and fails as one unit.
6. The workflow waits on the durable timer until `expires_at`. A restart, a release and a Continue-As-New do not lose the wait; a worker outage is satisfied once on recovery from history.
7. At `expires_at` the workflow sets the timer EXPIRED with escalation level 1 and `escalated_to_role` from the `SERVICE_LEVEL` row in force, and writes one `rwb.case.TimerBreached.v1` to the outbox. The case status does not move and no next action is written by this story.
8. A `NOTICE_PERIOD` timer is never paused: the deviation events pause the `SERVICE_LEVEL` clock and leave this one running (R-DEV-01).
9. `CaseWorkflow` stops the running `NOTICE_PERIOD` timer when the case reaches CLOSED, and never restarts it.
10. `TimersController` already serves `GET /cases/{caseId}/timers`; this story adds the notice period rows to that answer and `noticePeriod` to `GET /cases/{caseId}`, with the authorisation and the scope of the two reads unchanged.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No `NOTICE_PERIOD_DAYS` row in force for the product group on the delivered date | No timer is written; the case is placed on the exception queue; the fact is acknowledged | MSG-P3-034 | AC4 |
| X2 | The fact is consumed late (worker outage, relay backlog) | The clock is still dated from the delivered date; the expiry is unchanged | None | AC3 |
| X3 | The same fact arrives twice, or two events carry the same notice and delivered date | One timer; the repeat is counted under R-UNI-40; no second event | None | AC2 |
| X4 | The timer row or the outbox row cannot be written | Nothing is applied; the event stays unacknowledged and is retried with backoff | MSG-GEN-006 | AC8 |
| X5 | A deviation is raised on the case | The `SERVICE_LEVEL` clock pauses; the notice period keeps running | MSG-P3-004 | AC5 |
| X6 | The fact names a case that is CLOSED or unknown | No timer; the fact is acknowledged and the row is listed for the data steward | None | AC9 |
| X7 | The `rwb-comms` notice answer is down or beyond 2 s | The case answer still returns `noticePeriod`; the notice panel shows a retry state and no fact is invented | None | AC7 |
| X8 | The caller is outside the scope, or lacks Case record R | 404 with no timer rows; 403 by rwb-case on the `rwb-access` answer | MSG-P4-003, MSG-P4-002 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E1055-CON and its fake and the wave-0 platform contracts; no in-lane story is waited for (Day 1) |
| Negotiable | The notice period days, their unit, the list values and the escalation role are data rows, never code |
| Valuable | The case carries the deadline the notice period actually has, dated from delivery and defensible in court |
| Estimable | One consumer, one command inside the workflow, one activity, one migration, one read extension |
| Small | Fits in two weeks with its tests |
| Testable | Every criterion runs against the `rwb-comms` stub, the parameter fixture and the Temporal test clock |

### 7. Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN, case side

  Background:
    Given case "RC-2026-000123" is "IN_PROGRESS" with product group "MORTGAGE", queue "LIT-BKK-OFF" and owner "LIT-0101"
    Given PRODUCT_PARAMETER version 2 is in force with NOTICE_PERIOD_DAYS 30 calendar days for "MORTGAGE"
    And the rwb-comms contract mock and the rwb-comms event stub are running

  Scenario: AC1 The delivery fact starts the notice period from the delivered date (new, D-RCV-60)
    Given notice "N-0001" for case "RC-2026-000123" was sent for registered mail on 2026-11-26 with barcode "RR123456789TH"
    When the rwb-comms contract mock returns NoticeDelivered for "N-0001" with delivery status "DELIVERED" and call-back date 2026-11-28
    Then a NOTICE_PERIOD timer is "RUNNING" on case "RC-2026-000123" with started_at 2026-11-28 and expires_at 2026-12-28
    Then GET /api/recovery/case/v1/cases/RC-2026-000123/timers returns the timer with timerType "NOTICE_PERIOD" and noticeRef "N-0001"
    Then GET /api/recovery/case/v1/cases/RC-2026-000123 returns noticePeriod startedOn 2026-11-28 and dueOn 2026-12-28
    Then the case status stays "IN_PROGRESS" and no case status event is published
    Then the event, the timer row and the log line carry no name, address or notice text

  Scenario: AC2 The same delivery fact twice starts one clock and counts the repeat (new, D-RCV-60)
    Given the delivery of "N-0001" on 2026-11-28 was applied and the NOTICE_PERIOD timer is "RUNNING"
    When the same NoticeDelivered event is delivered again with the same event ID
    Then case "RC-2026-000123" has one NOTICE_PERIOD timer with expires_at 2026-12-28 and started_at 2026-11-28
    Then the repeat is counted under rule "R-UNI-40"
    Then no second timer row and no second TimerBreached are written

  Scenario: AC3 A late delivery fact still dates the clock from the delivery date (new, D-RCV-60)
    Given the rwb-case worker was stopped from 2026-11-28 to 2026-12-05
    When the NoticeDelivered for "N-0001" with call-back date 2026-11-28 is consumed on 2026-12-05
    Then the NOTICE_PERIOD timer has started_at 2026-11-28 and expires_at 2026-12-28
    Then the timer is not dated from 2026-12-05
    Then the workflow history records the delivered date the fact carried

  Scenario: AC4 No notice period in force writes no clock (new, D-RCV-60)
    Given no NOTICE_PERIOD_DAYS row is in force for "SSME" on 2026-11-28
    When the NoticeDelivered for "N-0002" of SSME case "RC-2026-000456" arrives with call-back date 2026-11-28
    Then no NOTICE_PERIOD timer is written for the case
    Then the case is placed on the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS"
    Then the case status stays "IN_PROGRESS" and the fact is acknowledged

  Scenario: AC5 A deviation pauses the stage clock and not the notice period (new, D-RCV-60)
    Given the rwb-deviation contract mock returns DeviationRaised on 2026-12-02 and DeviationCleared on 2026-12-04
    Given case "RC-2026-000123" has a RUNNING SERVICE_LEVEL timer and a RUNNING NOTICE_PERIOD timer expiring 2026-12-28
    When DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04
    Then the NOTICE_PERIOD timer stayed "RUNNING" with expires_at 2026-12-28 and paused false
    Then the arrival of the two deviation events does not move started_at or expires_at of the notice period
    Then the case record shows MSG-P3-004 with the prescription date while the deviation was open

  Scenario: AC6 The notice period ends once and raises one breach (new, D-RCV-60)
    Given the NOTICE_PERIOD timer of case "RC-2026-000123" has expires_at 2026-12-28 and the SERVICE_LEVEL row in force gives escalation role "RW-LITOFF"
    When the durable timer fires at 2026-12-28
    Then the timer is "EXPIRED" with escalation level 1 and escalated_to_role "RW-LITOFF"
    Then exactly one rwb.case.TimerBreached.v1 is written to the outbox with timerType "NOTICE_PERIOD", expiresAt 2026-12-28 and escalateTo "RW-LITOFF"
    Then the case status stays "IN_PROGRESS"
    When the workflow is replayed from history
    Then no second TimerBreached is published and the escalation level stays 1

  Scenario: AC7 The notice period is a case fact and the notice stays with rwb-comms (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0001" with state "Delivered", barcode "RR123456789TH" and call-back date 2026-11-28
    When "LIT-0101" opens case "RC-2026-000123"
    Then GET /api/recovery/case/v1/cases/RC-2026-000123 returns noticePeriod noticeRef "N-0001" and dueOn 2026-12-28 and no notice state, barcode or address
    Then the notice panel is filled from the rwb-comms answer over the gateway-bff composite route
    When the rwb-comms answer times out beyond 2 s
    Then the case answer still returns noticePeriod and the notice panel shows a retry state
    Then rwb_case holds no notice table, no notice column and no foreign key into rwb_comms

  Scenario: AC8 Nothing is applied when the clock cannot be written (new, D-RCV-60)
    Given the timer write of case "RC-2026-000123" fails
    When the NoticeDelivered for "N-0001" arrives
    Then no NOTICE_PERIOD timer exists for the case and no outbox row is written
    Then the consumer record shows MSG-GEN-006 and the event stays unacknowledged for retry
    When the retry succeeds
    Then the timer is written once with started_at 2026-11-28 and expires_at 2026-12-28

  Scenario: AC9 The clocks of a case outside the caller's scope or right (new, D-RCV-60)
    Given case "RC-2026-000123" is outside the scope of "PH-0203"
    When "PH-0203" sends GET /api/recovery/case/v1/cases/RC-2026-000123/timers
    Then the response is status 404 with MSG-P4-003 and no timer row is returned
    When a role without Case record R sends the same read
    Then the response is status 403 with MSG-P4-002
```

**Note.** The nine criteria are new because this secondary slice owns none of the legacy ones (GAP-2247; ASM-3704); they keep the legacy values unchanged (notice "N-0001", case "RC-2026-000123", barcode "RR123456789TH", delivered 2026-11-28) and assert only the clock of the case side. Every cross-service Given is the `rwb-comms` or `rwb-deviation` contract mock of section 12.8. The wave 1 harness RWB-ITG-E1055-ITG copies the journey with the `-ITG` suffix.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A notice period starts only from the delivered date on the proof of delivery, never from the print, dispatch or file date | R-LIT-07; CTL-15; legacy BR2 |
| BR2 | The length of the period is `NOTICE_PERIOD_DAYS` of the product group in force on the delivered date, in the unit of the same answer, and within the catalog range 1 to 365 | `PRODUCT_PARAMETER` (RWB-P3-E1045-APP); FSD P3 A2.25 |
| BR3 | No parameter row in force means no clock: the case goes to the exception queue rather than to a guessed period | FSD P3 AC-EXC-P3-025-03; MSG-P3-034 |
| BR4 | The notice period is a legal clock: a deviation pauses the stage clock and never this one | R-DEV-01 |
| BR5 | A `NOTICE_PERIOD` timer is dated from the fact, so a fact consumed late yields the same expiry | ADR-016; DP-10 |
| BR6 | The same fact twice produces one effect and the repeat is counted | R-UNI-40; legacy BR6 |
| BR7 | `rwb_case` keeps the notice reference and the two dates on the timer only; the notice, its state and its barcode are read from the `rwb-comms` answer | DP-01; DP-11 |
| BR8 | Timer start, read and expiry go only through the timer boundary inside `CaseWorkflow`; no caller writes or updates the `timer` row | ADR-011; ADR-016; RWB-P3-E1028-APP BR10 |
| BR9 | At expiry one `TimerBreached` is published with the escalation role of the `SERVICE_LEVEL` row in force, and the case status does not move | R-UNI-30; legacy section 9 |
| BR10 | The timer row and its outbox row commit as one unit; a failed write leaves no half state and is retried | R-UNI-39; Principle 5 |

### 9. State transitions

None on the case: this story does not change a case status. It changes the state of the `NOTICE_PERIOD` timer (LOV-TIMER-STATUS):

| From | Event | Condition | To |
|---|---|---|---|
| None | `rwb.comms.NoticeDelivered.v1` | `NOTICE_PERIOD_DAYS` in force for the product group | RUNNING, `started_at` = delivered date |
| None | `rwb.comms.NoticeDelivered.v1` | No parameter row in force | None; case on the exception queue with MSG-P3-034 |
| RUNNING | A second delivery fact for the same notice and delivered date | Inbox repeat of the business key | RUNNING, unchanged, repeat counted |
| RUNNING | The durable timer fires at `expires_at` | None | EXPIRED, escalation level 1, one `TimerBreached` |
| RUNNING | `rwb.case.CaseStateChanged.v1` to CLOSED | None | STOPPED, never restarted |

A `NOTICE_PERIOD` timer moves to PAUSED only if a later decision makes it a stage clock; it is a legal clock today, so a deviation does not pause it (BR4). The reading that a statutory notice period is a legal deadline is assumed, because R-DEV-01 names the prescription clock and not this one (GAP-2245; ASM-3702). The warning point of the clock is written as null: no source sets a warning point for a notice period (GAP-2244; ASM-3701).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow identity | Consumes the delivery fact, starts, expires and stops the `NOTICE_PERIOD` timer, writes the `timer` row and the outbox row |
| RW-LITOFF, litigation officer | Reads the notice period on the case and receives the expiry as the escalation role |
| RW-CASEOWN, case owner | Reads the notice period on their cases (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the clocks in team scope; receives the expiry where the `SERVICE_LEVEL` row names the team manager role |
| RW-LEGAL, legal counsel | Owns the notice-period values with the business lead; reads the clock |
| RW-PLATADM, platform administrator | Reads the timer and the consumer record, its retries and the `.dlt` |
| RW-DATASTEW, data steward | Reads the exception list of MSG-P3-034 |
| No role and no service | Writes a notice row, a notice state, a barcode or an address into `rwb_case` |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, timer_type, started_at, expires_at, warn_at, paused, status, escalation_level | Write |
| DF-WRK-043, DF-WRK-044 | timer | escalated_to_role, escalated_at | Write at expiry |
| Not specified in the source documents (GAP-2246; ASM-3703) | timer | notice reference of the clock (`reference_ref`) | Write, read |
| DF-CAS-001, DF-CAS-002 | recovery_case | id, case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read, for the parameter lookup |
| DF-CAS-005 | recovery_case | status | Read, and read again to refuse a CLOSED case |
| DF-CAS-009, DF-CAS-010 | recovery_case | owner_user_id, queue_id | Read, for the escalation role |
| DF-WRK-002, DF-WRK-004 | queue | queue_code, team_code | Read, for the escalation role |
| DF-WRK-039, DF-WRK-040 | assignment | queue_id, transfer_reason_code | Write, for the exception-queue placement of AC4 |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `NOTICE_PERIOD_DAYS` and its unit in force | Read through the parameters contract of rwb-case |
| DF-REF-184 | reference_row | LOV-TIMER, LOV-TIMER-STATUS, LOV-SEND-STATUS | Read through the reference-data contract |

The legacy fields that named the ACE proof-of-delivery rows (DF-ACE-253 to DF-ACE-258), the contact address (DF-ACE-078) and the ledger entries (DF-INT-002 to DF-INT-011) are **not** read here: the pod rows belong to `rwb-source-data` (DP-05, DP-18), the notice fields to `rwb-comms` (DP-01), and this story reads no `v_ace_*` view and no `interaction` table. Personal data: none. The timer carries a notice reference, two dates and codes only.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). No new path is published: the three operations exist and this story fills the notice-period part of their answer.

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | `/cases/{caseId}/timers` | The clocks on the case (API-P3-013); this story adds the `NOTICE_PERIOD` rows with `timerType`, `startedAt` (delivered date), `expiresAt`, `status`, `escalationLevel`, `escalatedToRole` and `noticeRef`, ordered by `expiresAt` | Case record R, scope applied |
| GET | `/cases/{caseId}` | One case (API-P3-002); the answer carries `noticePeriod` as `{noticeRef, startedOn, dueOn, status}` from the running or last timer | Case record R, scope applied |
| GET | `/cases/{caseId}/next-action` | The next action of the case (API-P3-016), unchanged; this story writes no next action, so the answer proves the case status and the next action did not move at the expiry | Case record R, scope applied |

Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 unknown or out of scope (MSG-P4-003), 503 store down. The three reads are idempotent by nature and write nothing.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice state, sent date, barcode and call-back date of the panel beside the clock; never stored, never joined (DP-11) | One hop, 2 s, GET retry once with jitter, breaker |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record R and the scope check on the three reads, cached per request | One hop, 2 s |

Two calls, no chain, both built against their contract and its fake. The delivery fact itself is an event, not a call (12.4). The element names the fact carries and the fields of the notice answer are Not specified in the source documents (GAP-2243; ASM-3700).

#### 12.3 Events published

| Event | Topic | Payload | Key |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | caseId, caseNo, timerId, timerType (`NOTICE_PERIOD`), expiresAt, escalateTo, noticeRef | caseId |

One event at the expiry of the clock, written to the outbox in the same transaction as the timer change and relayed in the CloudEvents 1.0 envelope by the outbox relay of `rwb_case` (DP-09). No payload carries a name, an address, a notice text or a document. No case status event is published: the status does not move.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | Inbox: starts the `NOTICE_PERIOD` clock from the delivered date; a repeat of the business key is counted |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Stops the running clock when the case reaches CLOSED |
| `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | No effect on this clock; the rows prove that the stage clock pauses and the legal clock does not (wave 2) |

All rows carry the inbox dedupe of `rwb_case` and the retry and `.dlt` path of `rwb.case.events.v1` and `rwb.comms.events.v1` (DP-09). The dispatch fact `rwb.comms.NoticeDispatched.v1` is **not** consumed here: its ledger entry is RWB-P3-E2021-APP's, and a dispatch starts no clock.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Holds the `NOTICE_PERIOD` durable timer, stops the previous one, refuses a CLOSED case, runs the catch-up from history |
| StartNoticePeriod | Command inside the workflow | `rwb-case` | Computes `expires_at` from the delivered date and the parameter answer, and calls the write activity |
| WriteNoticeTimer | Activity | `rwb-case` | One transaction: the `timer` row and the outbox row; fails as one unit |
| CalculateDueDate | Activity, reused from RWB-P3-E1045-APP | `rwb-case` | Reads `NOTICE_PERIOD_DAYS` and its unit in force through the parameters contract of rwb-case; a missing row is a refusal |

No Schedule is registered by this story and no new workflow is created.

#### 12.6 Schedules

None. The legacy clock hung off `JOB-10` (Quartz, daily 16:00) and its read at 06:00; both are `rwb-comms`'s and run as its Temporal Schedule on `rwb-comms` (RWB-P6-E1055-APP). On the case side the clock is started by an event and waited on inside `CaseWorkflow` (DP-10), and `JOB-02`, `JOB-03` and `JOB-06` keep their owners in this service and are not touched here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The `NOTICE_PERIOD` row: type, start, expiry, paused flag, status, escalation level, escalated role and time, notice reference |
| recovery_case | P3 (rwb_case) | Product group, status, queue and owner read; no column written by this story |
| queue | P3 (rwb_case) | `queue_code` and `team_code` of the escalation role |
| assignment | P3 (rwb_case) | The exception-queue placement of a case with no notice period in force |
| parameter_catalog, parameter_value, reference_row, reference_version | P3 (rwb_case) | `NOTICE_PERIOD_DAYS` and the three lists, read through the two contracts |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the published event and the inbox dedupe |

`notice`, `pod_receipt`, `v_ace_pod` and `interaction` are **not** tables of `rwb_case` and are not read, joined or referenced by a foreign key (DP-01, DP-05, DP-18).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms WireMock and event stub | RWB-P6-E1055-CON | `NoticeDelivered` for N-0001 with `DELIVERED` and call-back date 2026-11-28; a duplicate with the same event ID; the same fact delivered late; a fact for a CLOSED case; the notice answer with state `Delivered`, barcode `RR123456789TH`; a delayed answer beyond 2 s |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing a role without it, and refusing a case outside the caller's scope |
| rwb-deviation event fixture | The S8 contract | `DeviationRaised` on 2026-12-02 and `DeviationCleared` on 2026-12-04 for RC-2026-000123 (wave 2) |
| Parameter and reference fixture | The rwb-case contracts | `NOTICE_PERIOD_DAYS` 30 calendar days for MORTGAGE, 60 for HIRE_PURCHASE, none for SSME; LOV-TIMER, LOV-TIMER-STATUS, LOV-SEND-STATUS |
| Temporal test-time control | The workflow kit | Moves the workflow clock to 2026-12-28 and to the retry, and replays the history |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided (no new path), 2 consumed | Timers, case and next action provided; the notice read and the authorise call consumed; one hop, 2 s |
| Kafka | 1 published, 4 consumed | TimerBreached published; the delivery fact, the case state change and the two deviation rows consumed |
| Temporal | 1 workflow, 1 new activity, 1 reused, no Schedule | CaseWorkflow with the notice clock; WriteNoticeTimer; CalculateDueDate |
| File | None | No file is read or written; the WIN file is `rwb-comms`'s and the edge `rwb-integration`'s |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case.noticeperiod`, module `noticeperiod`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform CON stories this table names are in place from wave 0, and the same-service contracts of DP-07 are wave 1 work of the service, so none of them is repeated as an H row: the metadata table carries what the work package fixes, which is the one contract dependency of this legacy key, RWB-P6-E1055-CON (ASM-3706). DP-05 resolves to a statement - this story reads no ACE view - and DP-18 resolves to a boundary: `rwb_case` holds no `interaction` table and this story writes no ledger entry, which is RWB-P3-E2021-APP's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeFactConsumer | Inbox consumer | Consumes the delivery fact, dedupes on the event ID and the business key, signals `CaseWorkflow` |
| NoticeFactValidator | Service | Requires the case, the notice reference, the delivered date and the delivery status; refuses an unreadable fact |
| StartNoticePeriod | Command | Stops the previous clock, computes the expiry from the delivered date, calls the write activity |
| WriteNoticeTimer | Activity | One transaction: the `timer` row with `reference_ref` and the outbox row |
| NoticeClockBoundary | Boundary | The only writer of the `NOTICE_PERIOD` row; a boundary test fails any class outside it |
| TimersQuery, CaseReadQuery | Query | Add the notice period to the two existing answers, with the authorisation and the scope |
| AccessCheckClient, NoticeReadClient | Clients | The P4 and P6 contracts with the 2 s budget, the retry and the breaker |
| NoticePeriodPanel | Data contract only | The fields the case record shows; the panel itself belongs to RWB-P3-E2015-APP |

**Database.** One Flyway step in the per-service sequence of `rwb_case` (DP-15): `timer.reference_ref` (varchar(40), nullable, the notice reference), the partial unique index `ux_timer_notice_running ON timer (case_id, reference_ref) WHERE timer_type = 'NOTICE_PERIOD' AND status IN ('RUNNING','PAUSED')`, and `ix_timer_notice_expiry ON timer (expires_at) WHERE timer_type = 'NOTICE_PERIOD' AND status = 'RUNNING'`. No new table, no column beyond these, no foreign key into another schema.

**Configuration and reference data.** `NOTICE_PERIOD_DAYS` and its unit are product parameter rows of `rwb-case`, loaded by RWB-P3-E1045-APP and read through the parameters contract in force on the delivered date; the test values are the business lead's. LOV-TIMER, LOV-TIMER-STATUS and LOV-SEND-STATUS are reference rows. The consumer timeout, the retry count and the `.dlt` topic are service configuration, never code.

**Build steps**

1. Flyway step and the boundary test: the notice reference column, the two indexes, and no writer outside `NoticeClockBoundary`.
2. `NoticeFactConsumer` and `NoticeFactValidator` with the inbox, the dedupe key and the CLOSED-case refusal; tests for AC2, AC3, AC9.
3. `StartNoticePeriod` over `CalculateDueDate` with the parameter answer and the unit; tests for AC1, AC4.
4. `WriteNoticeTimer` with the one transaction and the outbox row, and the retry of X4; test for AC8.
5. The expiry fire: EXPIRED, level 1, `escalated_to_role`, one `TimerBreached`, unchanged status; tests for AC6.
6. The two read extensions with the notice period and the degraded panel; tests for AC7, AC9.
7. The deviation proof: the clock is untouched by the two deviation events while the stage clock pauses; test for AC5.

**Feature switch.** `rwb.case.notice-period-v1`. Off: the fact is acknowledged, no clock is written and the two reads answer without `noticePeriod`; on: the behaviour above.

**Done when.** Every test in section 16 passes, the contract tests of RWB-P6-E1055-CON stay green, no notice table, notice column or cross-schema foreign key exists in `rwb_case`, and a period started in 2026 fires once and on time after a release of both services in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-034 | No notice period in force for the product group | No {parameter} is set for {scope}. The timer did not start. |
| MSG-P3-004 | A deviation is open on the case and the legal clock keeps running | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The clock cannot be written and the fact is queued | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No session on a read | Your session has ended. Sign in again. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case unknown or outside the scope | This case is not in your scope. |

MSG-P3-034 keeps the wording used by FSD P3 AC-EXC-P3-025-03; MSG-P3-004 is the case record text of the timers story; MSG-GEN-006 is the legacy retry text of the story, kept unchanged. Thai text follows DL10.

### 15. Screens and states

| Screen | What the user sees and does |
|---|---|
| SCR-03 Case record | The notice period: type "Notice period", started on the delivered date, due date, status; read only. The notice state, sent date, barcode and call-back date come from the `rwb-comms` answer on the same screen over the gateway-bff route, with the retry state of X7 |
| SCR-03, states | Loading, Read only, On hold (the clock keeps running while the case is on hold or under a deviation), Closed (the clock is STOPPED) |
| SCR-09 Exception queue | The cases with MSG-P3-034 for a product group with no notice period in force, in its Loading and List states |
| SCR-44 Interface and job monitor | The consumer record of the delivery fact, its retries and its `.dlt` entries; no `JOB-10` row belongs to this service |

The screens are served by the gateway-bff composite route (DP-19); the panels are built by RWB-P3-E2015-APP and this story fixes the answers they read.

### 16. Test cases

The twelve legacy IDs are kept in order with the Level column of section R7.2. The AC numbers before the semicolon are the legacy criteria of RWB-E1-055, whose primary story is RWB-P6-E1055-APP; the criterion after it is the case-side one of this file that runs the same data.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | Legacy AC1; no case-side step (the dispatch is P6's) | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | Legacy AC2; AC1, AC3 here | Component | Pod fact for 2026-11-30 with RR123456789TH, call-back 2026-11-28 |
| TC-E1-055-03 | Legacy AC3; no case-side step | Contract | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | Legacy AC4; no case-side step | Contract | No acknowledgment on three runs |
| TC-E1-055-05 | Legacy AC5; AC7 here (degraded panel) | Component | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | Legacy AC6; no case-side step | Component | 30 rows, 1 unknown |
| TC-E1-055-07 | Legacy AC7; AC2 here | Component | The delivery fact of 2026-11-30 delivered twice |
| TC-E1-055-08 | Legacy AC8; no case-side step | Contract | Dispatch rerun on 2026-11-25 |
| TC-E1-055-09 | Legacy AC9; no case-side step | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | Legacy AC10; AC2 here | Component | Repeat of RR123456789TH with call-back 2026-11-28 |
| TC-E1-055-11 | Legacy AC11; AC7 here | Component | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Legacy access; AC9 here | Component | RW-PHONECOL reads the timers; refused with MSG-P4-002 |
| TC-E1-055-13 | AC4, BR3, BR9 | Component | SSME with no NOTICE_PERIOD_DAYS row in force |
| TC-E1-055-14 | AC5, BR4 | Component | Deviation from 2026-12-02 to 2026-12-04 on a case with both clocks |
| TC-E1-055-15 | AC3, BR5 | Component | Worker stopped 2026-11-28 to 2026-12-05, fact consumed late |
| TC-E1-055-16 | AC8, BR10 | Component | Timer write forced to fail, then the retry |

TC-E1-055-13 to TC-E1-055-16 are new with the criteria of this file and are marked as such; the twelve legacy IDs keep their data. The legacy levels map as the rest of this story set maps them: System to End to end, Access to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the notice period days, their unit, the three lists and the escalation role are data rows with a version in force.
- No personal data in events, workflow history, logs or prompts: the case number, the notice reference, two dates, a barcode and codes only; no name, address or notice text enters `rwb_case`.
- No read of another service's table and no direct ACE view: the notice through `rwb-comms`, the ledger through `rwb-source-data`, authorisation through `rwb-access` (DP-01, DP-05, DP-11, DP-18).
- No file, no SFTP, no WIN endpoint and no integration adapter is called: files move only through `rwb-integration` (REQ-DRI-006, DP-16 boundary).
- The clock is a durable Temporal timer; no Quartz job, no `JOB-10` trigger and no Schedule is created by this story.
- The timer row is written only by `NoticeClockBoundary`; no class outside it writes or updates a `NOTICE_PERIOD` row.
- One hop and 2 s per consumed call, a breaker per downstream, and GET retried once with jitter.
- Every answer carries IDs, codes, dates and amounts only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-30, R-UNI-40 | TC-E1-055-02, TC-E1-055-07, TC-E1-055-10, TC-E1-055-13, TC-E1-055-15, TC-E1-055-16 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-02, TC-E1-055-07, TC-E1-055-12 |
| REQ-DRI-006 | Files move only through the integration adapters | Business Requirements Epic 1, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | None | TC-E1-055-01, TC-E1-055-04 |
| ADR-011, ADR-016 | The durable timer replaces the Quartz clock behind the same boundary | Architecture v5 slide 44; Temporal and Drools design | All three features | All recovery processes | R-UNI-30 | TC-E1-055-14, TC-E1-055-16 |

### 19. Out of scope

- The WIN file, the acknowledgment, the proof read, the barcode reconciliation and the dispatch states (RWB-P6-E1055-APP); the contract baseline, the infrastructure and the deployment of that key (RWB-P6-E1055-CON, -INF, -OPS).
- The pod rows, the freshness answer and the interaction ledger (RWB-P1-E1055-APP, DP-18); the letter behind the notice (RWB-P5-E1055-APP).
- The dispatch and delivery ledger entries on the case timeline and the unserved-letter task (RWB-P3-E2021-APP).
- The notice-period transition driven by the S4 delivery answer on the litigation route (RWB-P3-E5002-APP).
- The other timer types, the warning and escalation engine and the prescription clock (RWB-P3-E1028-APP); the values of the parameters (RWB-P3-E1045-APP).
- The next action and the task of the case after the period ends (RWB-P3-E2035-APP) and the notice panel itself (RWB-P3-E2015-APP).
- The cross-service journey harness and its evidence (RWB-ITG-E1055-ITG).
