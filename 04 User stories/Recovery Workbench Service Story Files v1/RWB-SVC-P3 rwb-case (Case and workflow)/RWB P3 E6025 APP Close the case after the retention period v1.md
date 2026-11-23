# RWB-P3-E6025-APP Close the case after the retention period

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E6025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P3-AV |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-S7-E6025-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-025 for rwb-case, case side of the retention closure. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the case of record to start the retention timer when the placement term has run, to close the case when that timer expires and the write-off service answers that the closure conditions hold, stopping every timer and cancelling every open task, and to keep the closed case readable with its closing date and its closure reason**, so that **a charged-off case ends on the date the rules name, with no clock still running and no open action left on a closed case**.

This is the case side of legacy RWB-E6-025 (FEAT-WOF-13). rwb-case owns the case, its stage, its timers, its tasks and its closing facts (Architecture v5 slide 14, P3 OUT row: schema `rwb_case` holds case, CMMN state, queues, tasks, allocation and timers; slide 41, P3 ownership row). rwb-writeoff owns the placement, the scan, the committee, the posting, the cash recovered, the loss and the closing entry (slide 20, S7 OUT row). The two answers of the write-off route set that land on the case — the retention-start answer of R-WO-36 and the closure answer of R-WO-47, with the hold of R-WO-48 — cross one service boundary through the contract of RWB-S7-E6025-CON, and this story applies them exactly once.

Inside `rwb-case` the slice is served on the service's own base `/api/recovery/case/v1` (DP-13), from schema `rwb_case`, in Java package `th.co.scb.ace.workbench.recovery.case`, on topic `rwb.case.events.v1` and task queue `rwb-case` in namespace `rwb-recovery`.

The slice holds no legacy acceptance criterion. The four criteria of RWB-E6-025 describe the feature across S7 and P3 and are proved end to end by RWB-ITG-E6025-ITG and on the write-off side by RWB-S7-E6025-APP; the eight criteria of section 7 are new and test only the case-side deliverable (ASM-1361).

### 2. Business rationale

R-WO-36 closes the placement and starts the retention timer when the placement term has run and nothing was recovered; R-WO-47 closes the case, stops every timer and writes the closing entry when no placement, no sale and no exception is open and every document carries a retention class; R-WO-48 holds the closure and raises a document task when a class is missing. All three are rows of the write-off route set, and all three land on facts that belong to the case: its stage, its clocks, its tasks and its closing date. The requirement is REQ-S7-008 and the business rule is BR-057 of the Epics 3 to 8 requirements: a case closes after its retention period with no action open, and reopening a closed case needs a written rule, a reason and an approver. RULE-022 carries the same statement, and NFR-031 states that case records carry a retention and archive rule by record class and that a case closes after its retention period, with the period itself still open under DL26.

In the monolith the timer, the state move, the closing entry and the case update were four statements inside one process and one Quartz job. In the target the rule answer is rwb-writeoff's and the case, the clocks, the tasks and the closing facts are rwb-case's, so the answer crosses a service boundary and must be applied exactly once, in one transaction, on a durable clock.

The case side is where a failure becomes visible. If the closure answer is dropped, the case sits in RETENTION_RUNNING for ever and its service-level timers keep escalating on a case nobody will work again. If the answer is applied twice, the case carries two closing dates. If the expiry is a table scan and a five-minute check, a restart loses the expiry and the case closes late or not at all. If the timers and the tasks are not stopped with the closure, a closed case reappears in a queue with an open action on it. Each of those is a wrong record on a charged-off balance, and none of them raises an error of its own.

The boundary must hold as well. rwb-case keeps the stage, the retention clock, the closing date and the closure reason, and keeps nothing of the write-off record: no placement, no sale, no exception, no document, no cash recovered, no loss, no closing entry. The retention period and the retention timer type are rows read at run time and never constants, because NFR-031 leaves the period open and a period in code would be a release. The expiry is a durable timer of CaseWorkflow, so it fires in a later year, after many releases, without a Quartz row. The case is served on `/api/recovery/case/v1` (DP-13), SCR-27 composes the case and the write-off through the gateway-bff composite route (DP-19), and every decision is written locally and published on `rwb.decision-record.v1` (DP-03).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-S7-E6025-CON is published | The two answers of the write-off route set that touch this story: the retention-start answer of R-WO-36 (write-off reference, recovered amount, placement end date, decision, rule ID, rule version) and the closure answer of R-WO-47 with the hold of R-WO-48 (decision Close or Hold, hold rule, rule ID, rule version, package version and business date), with their transport, error envelope and contract fake. The paths and the element names are Not specified in the source documents (GAP-0741; ASM-1356) because that contract story fixes them; this story builds against the contract and its fake and never against a write-off table |
| The `rwb_case` baseline exists | `recovery_case`, `timer`, `task`, `queue`, the local decision-record table and the outbox, inbox and idempotency objects, from the Epic 1 case story of this service (RWB-P3-E1018-APP) |
| CaseWorkflow runs one per case | Task queue `rwb-case`, workflow ID `case-{caseId}`, Continue-As-New at each stage end and at least every 28 days, and the workflow kit holds durable timers, so this story adds a timer and a step and no workflow and no Schedule (TSD P3 v3 T2.4) |
| The retention period is a parameter row | Read through the parameters contract of this service with the version in force. The period length is Not specified in the source documents (GAP-0741; ASM-1357): NFR-031 and the BRD question Q-012 leave it open under DL26 |
| The retention timer type is a reference row | LOV-TIMER holds SERVICE_LEVEL, NOTICE_PERIOD, CURE_PERIOD, PRESCRIPTION, HEARING_DEADLINE, OFFER_VALIDITY, HOLDING_AGE, CLAIM_DEADLINE and INSTALLMENT_DUE, and none of them is a retention timer; the new row is Not specified in the source documents (GAP-0741; ASM-1358) |
| The Case record right and the scope are answered by rwb-access | The authorise contract of rwb-access (P4) gives the right and the scope, cached by the platform guard library; RW-CREDITAD holds Case record R in the RBAC matrix of TSD P3 v3 T6.1 |
| The platform contracts the two DP rows name are published | RWB-PLT-E1027-CON (DP-03) and RWB-PLT-N001-CON (DP-19). They are pulled by the rwb-case baseline stories and by the platform, so this slice adds no build dependency and starts on Day 1 (ASM-1355) |
| No build dependency | Day 1, against the RWB-S7-E6025-CON fake; the C dependency never blocks the lane |

### 4. Flow

1. rwb-writeoff applies R-WO-36 when the placement term has run and nothing was recovered, and sends the retention-start answer through the operation of RWB-S7-E6025-CON: one hop, 2 s timeout, breaker per downstream.
2. The case router of rwb-case consumes the answer, dedupes it in its inbox on the write-off reference and the message key, and starts the retention-start step for the case. A duplicate never acts twice (R-UNI-40).
3. The step reads the case row: its stage code, which must be PLACED_WITH_AGENCY, its open tasks and its timers. It reads `rwb_case` rows only.
4. The step validates the answer: write-off reference, rule ID, rule version and business date present, and MSG-GEN-001 names the field when one is missing; a case not in PLACED_WITH_AGENCY is refused with MSG-P3-005 and nothing changes.
5. The step reads the retention period in force for the product group from the parameter row and computes the expiry from the business date of the answer.
6. RecordAndApply, in one `rwb_case` transaction: `stage_code` RETENTION_RUNNING by R-WO-36, `stage_clock_start`, `rule_version` (DF-CAS-021), the timer row with the retention type, `started_at`, `expires_at`, `status` RUNNING (DF-WRK-027 to DF-WRK-036), the local decision record naming R-WO-36 and the rule version, and the outbox rows of `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1`. A failed write rolls the whole transaction back (R-UNI-39).
7. The step signals CaseWorkflow with the expiry. CaseWorkflow holds it as a durable timer of the workflow kit; when it fires the workflow starts the closure step on task queue `rwb-case`. No Quartz row, no timer-check job and no Schedule is involved.
8. The closure step asks the write-off service for the decision of R-WO-47 through the same contract, carrying the case reference, the write-off reference and the business date, and receives Close with the rule version, or Hold with R-WO-48.
9. On Close the step checks the case's own open actions — no task in status OPEN and no timer other than the retention timer in status RUNNING — and then closes: `stage_code` CASE_CLOSED, `closed_date` (DF-CAS-022) the business date of the answer, `closure_reason` (DF-CAS-023) WRITTEN_OFF of LOV-CLOSURE, every timer of the case to status STOPPED, every open task to status CANCELED, and the next-action fields cleared.
10. On Hold the step records the hold under R-WO-48 and leaves the stage, the clocks and the tasks untouched; the document task that follows is raised by rwb-document and not here.
11. The closure writes one decision record naming R-WO-47 and the rule version, and the outbox rows of `rwb.case.CaseStateChanged.v1`, `rwb.case.TimerBreached.v1` and `rwb.decision-record.DecisionRecorded.v1`, in the same transaction as the closure.
12. Officers read the closed case: `GET /api/recovery/case/v1/cases/{caseId}` returns the stage, the closing date, the closure reason and the stopped timers, `GET /api/recovery/case/v1/cases/{caseId}/next-action` returns no next action, and both are guarded by the Case record right and the scope, cached per request.
13. SCR-27: the gateway-bff composite route calls rwb-case for the case, its clocks and its closing facts, rwb-writeoff for the write-off state and rwb-document for the documents of the case, one hop each, and merges them into the screen model (DP-19); the browser calls one route and no owner service.
14. Nothing of the placement, the sale, the exception, the documents, the cash recovered, the loss or the closing entry is written or served by rwb-case; those stay with their owners, and the closure answer carries only the decision, the rules and the business date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same retention-start or closure answer arrives twice | The inbox ignores the second answer and records the idempotency hit; no row, no clock, no closure and no event is written twice | None | AC4 |
| X2 | An answer names a case that is not in the stage its rule starts from | The answer is refused, the stage and the clocks do not change, and the refusal is recorded with the rule the answer carried | MSG-P3-005 | AC5 |
| X3 | The local decision record cannot be written | The transaction rolls back: the stage, the clock, the closing date and the closure reason do not change, and the answer is retried | MSG-P7-003 | AC6 |
| X4 | The closure answer is Hold under R-WO-48 because a document carries no retention class | The case stays in RETENTION_RUNNING, every clock keeps running and no closing fact is written | None | AC3 |
| X5 | The case still holds a task in status OPEN when the closure answer is Close | The case is not closed, the retention clock keeps running and the open task stays on the case | None | AC4 |
| X6 | An answer carries no write-off reference, no rule ID or no business date | The answer is refused, nothing changes and the missing field is named | MSG-GEN-001 | AC1 |
| X7 | The write-off answer does not arrive within 2 s or the service is unavailable | Nothing moves; the retention clock keeps its expiry and the closure step retries the ask | None | AC2 |
| X8 | The write-off service reports that the scan is on hold for the missing tax criteria and sends no answer | The case stays where it is and the reason carried by the answer is passed through unchanged | MSG-S7-001 | AC1 |
| X9 | A role without the Case record right reads a closed case | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC7 |
| X10 | A closed case outside the caller's scope is read | Refused as not found; nothing is returned and nothing is written | MSG-P4-003 | AC7 |

X1 is the duplicate rule R-UNI-40 and X3 is the no-unlogged-action rule R-UNI-39; both are applied through the inbox and the decision-record library and are platform behaviour, not this story's code. X5 is the case-side reading of "no action is open": the guards that look at the placement, the sale, the exception and the document class are the write-off service's and arrive as the decision of the answer (ASM-1359).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the rwb-writeoff contract fake of RWB-S7-E6025-CON, the authorise fake and the workflow kit; no work order sits inside another team's lane |
| Negotiable | The retention period, the retention timer type, the closure reason, the rule version and the contract element names are parameter rows, reference rows or contract fields; the story fixes the behaviour and no value |
| Valuable | A charged-off case closes on the date the rules name, with no clock still running and no open action on it |
| Estimable | One consumer, one durable timer, one closure step, one ask to the write-off service, one transaction, two read operations and one panel |
| Small | Fits two weeks with its tests: no new table, no new column, no new workflow and no Schedule |
| Testable | Each of the eight criteria of section 7 is one automated test, and every cross-service answer is stubbed in the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Close the case after the retention period on the case

  Background:
    Given case "RW-2026-000625" is open for write-off "WO-2026-000625" with recovered amount 0
    Given rule rows R-WO-36, R-WO-47 and R-WO-48 are in force with rule version "WO-2026.11"
    Given the retention period parameter row in force for product group "MORTGAGE" holds the fixture value "P1"
    Given the retention timer type is a row of LOV-TIMER in force

  Scenario: AC1 The retention-start answer moves the case to RETENTION_RUNNING (new, D-RCV-60)
    Given case "RW-2026-000625" is in stage "PLACED_WITH_AGENCY" with no open task
    Given the rwb-writeoff contract mock returns the retention-start answer of R-WO-36 for write-off "WO-2026-000625" with placement end date 2026-12-31, recovered amount 0 and rule version "WO-2026.11"
    When the retention-start step applies the answer for case "RW-2026-000625"
    Then the case stage code is "RETENTION_RUNNING" by R-WO-36 and stage_clock_start is 2026-12-31
    Then one timer row of the retention timer type is written with status "RUNNING", started_at 2026-12-31 and expires_at equal to 2026-12-31 plus the period "P1"
    Then CaseWorkflow holds that expiry as a durable timer and no Quartz row, no timer-check job and no Schedule is created
    Then one decision record names R-WO-36 and the rule version "WO-2026.11"
    Then the decision record, the stage change and the outbox rows of rwb.case.CaseStateChanged.v1 and rwb.decision-record.DecisionRecorded.v1 commit in one rwb_case transaction

  Scenario: AC2 The retention expiry closes the case and stops every clock (new, D-RCV-60)
    Given case "RW-2026-000625" is in stage "RETENTION_RUNNING" with a retention timer in status "RUNNING" and one service-level timer in status "RUNNING"
    Given the rwb-writeoff contract mock returns the closure answer Close of R-WO-47 for write-off "WO-2026-000625" with rule version "WO-2026.11" and business date 2027-06-30
    When the retention durable timer fires and the closure step applies the answer
    Then the case stage code is "CASE_CLOSED" by R-WO-47, closed_date is 2027-06-30 and closure_reason is "WRITTEN_OFF" of LOV-CLOSURE
    Then every timer of the case is status "STOPPED", the retention timer and the service-level timer included
    Then every open task of the case is status "CANCELED" and the next-action read of the case returns no next action
    Then one decision record names R-WO-47 and the rule version "WO-2026.11"
    Then rwb.case.CaseStateChanged.v1, rwb.case.TimerBreached.v1 and rwb.decision-record.DecisionRecorded.v1 are in the outbox in the same rwb_case transaction as the closure

  Scenario: AC3 A missing document retention class holds the closure (new, D-RCV-60)
    Given case "RW-2026-000625" is in stage "RETENTION_RUNNING" with a retention timer in status "RUNNING"
    Given the rwb-document contract mock returns document "DOC-2026-000625-01" of case "RW-2026-000625" with no retention class in force
    Given the rwb-writeoff contract mock returns the hold answer of R-WO-48 for write-off "WO-2026-000625" naming R-WO-48 and rule version "WO-2026.11"
    When the retention durable timer fires and the closure step applies the answer
    Then the case stage code stays "RETENTION_RUNNING" and closed_date and closure_reason stay empty
    Then the retention timer and every other timer of the case keep status "RUNNING"
    Then no task is canceled and one decision record names R-WO-48 with the rule version "WO-2026.11"
    Then no case is closed by this step and rwb-case raises no document task, because that task is rwb-document's

  Scenario: AC4 A repeated answer and an open action change nothing (new, D-RCV-60)
    Given the closure answer Close of R-WO-47 for write-off "WO-2026-000625" has been applied and case "RW-2026-000625" is in "CASE_CLOSED"
    When the same answer arrives again with the same write-off reference and the same business date
    Then the inbox dedupes it and no second closure, no second timer stop and no second decision record is written
    Then no second CaseStateChanged event is published and closed_date stays 2027-06-30
    Given another case "RW-2026-000626" is in "RETENTION_RUNNING" with one task in status "OPEN"
    When the closure answer Close of R-WO-47 arrives for it
    Then the case is not closed, the task stays "OPEN" and the retention timer keeps "RUNNING"

  Scenario: AC5 An answer for the wrong stage is refused (new, D-RCV-60)
    Given case "RW-2026-000625" is in stage "RETENTION_RUNNING"
    Given the rwb-writeoff contract mock returns the retention-start answer of R-WO-36 for write-off "WO-2026-000625"
    When the retention-start step applies the answer for the case
    Then the response is refused with MSG-P3-005 naming "RETENTION_RUNNING" and the stage the rule starts from
    Then the stage, stage_clock_start and every timer stay unchanged and no decision record is written

  Scenario: AC6 A closure that cannot be recorded does not close the case (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the closure answer Close of R-WO-47 arrives for case "RW-2026-000625" in "RETENTION_RUNNING"
    Then the stage code, closed_date, closure_reason, the timer statuses and the task statuses do not change
    Then no CaseStateChanged event is published and the user sees MSG-P7-003
    Then the retried answer writes one decision record and one closure

  Scenario: AC7 The closed case is read only with the right and inside the scope (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /api/recovery/case/v1/cases/{caseId} for a closed case
    Then the call is refused with status 403 and MSG-P4-002
    Given a case owner whose scope is "Own" and a closed case owned by another person
    When the case owner calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    Then the read writes nothing and raises no event

  Scenario: AC8 SCR-27 shows the closed case and serves none of the write-off facts (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-27 for case "RW-2026-000625" in "CASE_CLOSED"
    Given the rwb-writeoff contract mock returns the write-off state of "WO-2026-000625" with the cash recovered and the loss the write-off service reports
    Given the rwb-document contract mock returns the two documents of case "RW-2026-000625" with their retention classes in force
    When the Credit Administration officer opens SCR-27
    Then the screen shows the state "Closed", closed date 2027-06-30 and closure reason "Written off"
    Then the screen shows every timer as stopped and offers no action, no reopening and no clock change
    And the browser calls one composite route and no owner service directly
    Then the cash recovered, the loss, the closing entry, the placement, the sale and the documents are read from rwb-writeoff and rwb-document on the same route and are not served by rwb-case
```

The eight criteria are this slice's own, because the plan allocates no legacy criterion to it: AC1 to AC4 of RWB-E6-025 are proved by RWB-S7-E6025-APP and end to end by RWB-ITG-E6025-ITG (ASM-1361). Where a criterion needs another service, the `Given` names its contract mock: rwb-writeoff for the two answers of R-WO-36 and R-WO-47 and the hold of R-WO-48, rwb-document for the documents and their retention class, rwb-access for the right and the scope. "P1" is a fixture value of the retention period parameter row and not a business value: the period is Not specified in the source documents (GAP-0741; ASM-1357), and the write-off reference, the case ID, the rule version label "WO-2026.11" and the dates are synthetic fixtures of the same kind as the legacy "SYN" values. The cash recovered and the loss carry no value here, because they are the write-off service's and this story never stores or echoes them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | When the placement term has run and nothing was recovered, the placement is closed, the retention timer starts and the case moves from PLACED_WITH_AGENCY to RETENTION_RUNNING | R-WO-36 |
| BR2 | When the retention timer expires, no placement, no sale and no exception is open and every document carries a retention class, the case closes to CASE_CLOSED, every timer stops, every open task is canceled and the closing facts are written | R-WO-47 |
| BR3 | A document without a retention class holds the closure: the case stays in RETENTION_RUNNING and the hold is recorded under R-WO-48 | R-WO-48; REQ-DCM-010 |
| BR4 | The retention period and the retention timer type are a parameter row and a reference row of this service, read at run time; neither is a constant, because NFR-031 leaves the period open under DL26 | NFR-031; BRD Q-012; ASM-1357 |
| BR5 | The expiry is a durable timer of CaseWorkflow, not a Quartz job, a Schedule or a five-minute check, so the date survives a restart and fires after any number of releases | TSD P3 v3 T2.3 and T2.4; ADR-011 |
| BR6 | The case stage, the clocks, the tasks, the closing date and the closure reason are rwb-case's and are never written by the caller that answers the closure | Architecture v5 slide 14 and slide 41; ASM-1359 |
| BR7 | The placement, the sale, the exception, the documents, the cash recovered, the loss and the closing entry are other services'; rwb-case holds the decision, the rule ID and the rule version and nothing of the write-off record | Architecture v5 slide 20 (S7 OUT) and slide 41 |
| BR8 | The decision record, the state change and the outbox rows are one transaction: a closure that cannot be recorded does not happen | R-UNI-39 |
| BR9 | The same answer arriving twice writes no row and raises no event a second time | R-UNI-40 |
| BR10 | The closing step names the rule ID and the rule version on every decision record; both arrive in the answer and are never written in code | R-WO-36; R-WO-47; DF-REF-001 to DF-REF-015 |
| BR11 | A closed case has no next action and no open task, so it never appears in a list of active cases with no next action | FSD P3 v4 AC-EXC-P3-050-03 |
| BR12 | The read of a case is guarded by the Case record right and the scope, and a read writes nothing | TSD P3 v3 T6.1 and T6.2; MSG-P4-002; MSG-P4-003 |

How the rules hold in `rwb-case`: BR1 and BR2 are two steps of the case router, each writing one stage change, one clock state and one decision record; the rule ID and the version come in the answer, so no Drools package is loaded and no KieBase is built on this path. BR3 is the Hold branch of the closure step: the answer decides, and this service only records it. BR4 is one parameter read and one reference read, so a period change is a data change with no release. BR5 is the workflow kit's timer, and the TimerScheduler port of TSD P3 v3 T2.3 is where the replacement of the retired five-minute check by durable timers happens, behind the same interface, with no caller change. BR6 and BR7 are the repository and an architecture test that fails a statement naming another schema. BR8 and BR9 are the one transaction and the inbox. BR10 is the decision-record writer. BR11 is the cleared next-action fields and the canceled tasks. BR12 is one authorise call per request, cached.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLACED_WITH_AGENCY | PLACEMENT_TERM_EXPIRED | The placement term has run, the recovered amount is 0 and the answer names R-WO-36 | RETENTION_RUNNING |
| RETENTION_RUNNING | RETENTION_TIMER_EXPIRED | The retention durable timer fired, the answer names R-WO-47 Close and the case holds no task in status OPEN | CASE_CLOSED |
| RETENTION_RUNNING | RETENTION_CLASS_MISSING | A document on the case has no retention class and the answer names R-WO-48 Hold | RETENTION_RUNNING, unchanged |
| RETENTION_RUNNING | A retention-start answer of R-WO-36 | The case is not in PLACED_WITH_AGENCY | Unchanged, MSG-P3-005 |
| RETENTION_RUNNING | The decision record cannot be written | The transaction rolls back | RETENTION_RUNNING, unchanged |

These four state names are the from-state and to-state values of R-WO-36, R-WO-47 and R-WO-48 in the write-off route set, written to `stage_code` of `recovery_case` (DF-CAS-006) together with `status` CLOSED of LOV-CASE-STATUS at the closure. They are not values of LOV-STAGE, which lists the route stages RESTRUCTURE to DEVIATIONS; the mapping from a route-set state name to a case stage code is Not specified in the source documents (GAP-0741; ASM-1358), and this story writes the rule's own names unchanged so a decision record and a case row can be read side by side. The closing facts are `closed_date` (DF-CAS-022) and `closure_reason` (DF-CAS-023); the reason written by a retention closure is WRITTEN_OFF of LOV-CLOSURE. A legal hold that is open on the case is not lifted here, because a hold overrides expiry and is rwb-access's and rwb-document's row under NFR-072. A payment after the closure is R-WO-49 and belongs to rwb-writeoff.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity | Applies the two answers, moves the stage, writes the retention clock, stops the clocks, cancels the tasks, writes the closing facts and the decision record |
| CaseWorkflow | Holds the retention durable timer and starts the closure step when it fires; moves no stage by itself |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-CREDITAD, Credit Administration officer | Reads the closed case and its closing facts (Case record R); takes no closure action on the case |
| RW-PRODHEAD, RW-WOCOMM, RW-FINANCE | Hold the write-off rights of the capability area; they read the case and act in the write-off service, not here |
| RW-WRITEOFF, write-off team | Runs the placement, the scan and the closure answer in rwb-writeoff (Write-off and posting C) |
| RW-COE | Owns the retention period parameter row, the retention timer type and the LOV-CLOSURE rows as reference data |
| RW-REFADM | Holds no Case record right; refused on the case read with MSG-P4-002 |
| No approval applies | The story takes no decision; the approval of a write-off is the committee's in rwb-writeoff |

The Write-off and posting rights A and C named in the legacy permission table (RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM, RW-FINANCE; RW-WRITEOFF, RW-CREDITAD) are checked in rwb-writeoff and are outside this story. No person is named anywhere in this story; the actor is a role and the record carries a user reference only.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002, DF-CAS-003 | recovery_case | id, case_no, product_group | Read |
| DF-CAS-005 | recovery_case | status | Read, and CLOSED written with the closure |
| DF-CAS-006 | recovery_case | stage_code | Read, and RETENTION_RUNNING and CASE_CLOSED written with the two moves |
| DF-CAS-018 | recovery_case | stage_clock_start | Write: the start of the retention clock |
| DF-CAS-021 | recovery_case | rule_version | Write: the rule version in force named by the answer |
| DF-CAS-022 | recovery_case | closed_date | Write: the business date of the closure answer |
| DF-CAS-023 | recovery_case | closure_reason | Write: WRITTEN_OFF of LOV-CLOSURE |
| DF-CAS-019, DF-CAS-020 | recovery_case | deviation_open, legal_hold | Read only, to show the state of the case; neither changes here |
| DF-CAS-049 to DF-CAS-053 | recovery_case | next_action_text, next_action_owner_role, next_action_due_date, next_action_rule_id, next_action_waiting | Write: cleared on the closure |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, task_id, timer_type, started_at, expires_at, warn_at, paused, status, escalation_level | Write: one retention timer at the start, and status STOPPED on every timer of the case at the closure |
| DF-WRK-017 to DF-WRK-026 | task | id, case_id, task_code, element_type, discretion, status, owner_role, due_at, completed_at, outcome_code | Read the open tasks, and write status CANCELED on each of them at the closure |
| DF-WRK-001 to DF-WRK-008 | queue | id, queue_code, queue_name, team_code, role_code, assignment_method, capacity_cap, overflow_queue_id | Read only: the queue the case was last on; the closure writes no placement |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write locally; the central entry in `decision_log_entry` is rwb-decision's (P7) |
| Not specified in the source documents (GAP-0741; ASM-1357) | parameter_catalog, parameter_value | the retention period row per product group, with the version in force | Read, in process through the parameters contract of this service |
| Not specified in the source documents (GAP-0741; ASM-1358) | reference_row, reference_version | the retention timer type in LOV-TIMER, WRITTEN_OFF in LOV-CLOSURE and STOPPED in LOV-TIMER-STATUS | Read, in process through the reference-data contract of this service |
| DF-PRT-001 to DF-PRT-007 | partner (owner S9) | id, partner_code, partner_name, partner_type, panel_status, contract_end | Not read and not written: the placement is rwb-partner's and its end date arrives in the answer |
| DF-REF-001 to DF-REF-015 | rule_row (owner P7) | rule_id, rule_version, from_state, event_code, to_state | Not read here: the rule ID and the rule version arrive in the answer |

Field IDs are those of the Technical Specifications by Module and the Logical Data Model. Every row written is a `rwb_case` row: the parameters and the reference rows are read through the contracts of this same service and never joined in SQL, and `rwb_case` holds no foreign key into another schema. `write_off`, `debt_sale`, `deviation`, `document`, `partner`, `rule_row` and `decision_log_entry` are other services' and are reached only through their owners' contracts. The legacy data block of RWB-E6-025 names `recovery_case`, `timer`, `partner`, `decision_log_entry` and `rule_row`; the first two are this service's and the last three are not read or written here.

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no operation. The closed case is read through the operations of this base that already exist — `GET /api/recovery/case/v1/cases/{caseId}` for the case with its stage, its closing date and its closure reason, `GET /api/recovery/case/v1/cases/{caseId}/timers` for the stopped clocks and `GET /api/recovery/case/v1/cases/{caseId}/next-action` for the empty next action — all three owned by rwb-case (P3) in the ownership map. The two closing fields are added to the Case resource those operations answer; their spelling `closedDate` and `closureReason` follows the column names and the rest of the element spelling is Not specified in the source documents (GAP-0741; ASM-1362). All three declare the Case record right R with the scope applied, and all three are read only.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| Not specified in the source documents (GAP-0741; ASM-1356) | Not specified in the source documents (GAP-0741; ASM-1356) | rwb-writeoff (S7) | The retention-start answer of R-WO-36 on the placement term, and the closure decision of R-WO-47 or the hold of R-WO-48 on the retention expiry: decision, rule ID, rule version, package version and business date; built against the RWB-S7-E6025-CON fake | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right and the scope before a case read, cached per request by the guard library | One hop, 2 s |

Two calls and no chain. The closure step asks the write-off service once per expiry and makes no second call for the same expiry; the write-off service makes no call back into rwb-case on this path. The path and the element names of the write-off operation are fixed by RWB-S7-E6025-CON and are not invented here.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, fromStageCode, toStageCode, eventCode (PLACEMENT_TERM_EXPIRED or RETENTION_TIMER_EXPIRED), ruleId, ruleVersion, writeOffRef, businessDate |
| `rwb.case.TimerBreached.v1` (EV-19) | `rwb.case.events.v1` | P3 | caseId | caseId, timerType, expiresAt, ruleId, ruleVersion |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID R-WO-36, R-WO-47 or R-WO-48, rule version, business date |

All three are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; no personal data and no amount is in any payload. rwb-case publishes no separate case-closed event: the closure is carried by CaseStateChanged with its event code, because the six published events of this module are CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached, and TimerDue is retired inside the workflow.

#### 12.4 Events consumed

None. The closure decision arrives as a call of the S7 contract and is not a Kafka subscription of this story, and the case router that consumes the state signals of a case is the Epic 1 and Epic 2 work of this service. A payment after the closure (R-WO-49) is consumed by rwb-writeoff and rwb-payment. This story adds no consumer group and no inbox use beyond the dedupe of the two answers.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID `case-{caseId}`) | `rwb-case` | Holds the retention expiry as a durable timer of the workflow kit and starts the closure step when it fires |
| RetentionStartStep | Step of the case router | `rwb-case` | Validates the R-WO-36 answer, reads the period, computes the expiry, records and applies the move, and signals CaseWorkflow |
| CaseClosureStep | Step of the case router | `rwb-case` | Asks the write-off service for the R-WO-47 decision, checks the case's own open actions, records and applies the closure |
| RecordAndApply | Transactional step (decision-record library) | `rwb-case` | Writes the stage, the closing facts, the clock and task statuses, the decision record and the outbox rows in one transaction |

No other activity and no child workflow is added: the write-off steps before the start and after the closure belong to rwb-writeoff, and the stage children of CaseWorkflow belong to the route services.

#### 12.6 Schedules

None added. The retention expiry is a durable timer of CaseWorkflow and not a Temporal Schedule, because an expiry is one date for one case and not a cadence; the retired five-minute timer check (JOB-05) is replaced by the workflow kit's timers behind the same timers port, and no caller changes (TSD P3 v3 T2.3). No Schedule, no Quartz row and no timer-check job is created, and no scheduler job of rwb-case reads the timer table for this story. The document-side retention job (JOB-17, monthly, owner rwb-document) and the legal-hold override are P5's and are not this story's. Whether the retention period should also be reviewed on a bank-wide cadence is Not specified in the source documents (GAP-0741; ASM-1360).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `recovery_case` | rwb_case | P3 | The story writes `stage_code`, `status`, `stage_clock_start`, `rule_version`, `closed_date`, `closure_reason` and the cleared next-action fields |
| `timer` | rwb_case | P3 | One retention timer at the start, and status STOPPED on every timer of the case at the closure |
| `task` | rwb_case | P3 | Read to find an open action, and status CANCELED written on every open task at the closure |
| `queue`, `assignment` | rwb_case | P3 | Read only: the closure writes no placement and no transfer |
| `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` | rwb_case | P3 | The retention period, the retention timer type, the closure reason and the timer status, read through this service's contracts and never joined in SQL |
| decision record (local library) | created in rwb_case | Platform library | The local record of the two moves, hash-linked, written in the same transaction |
| `outbox_event`, `processed_event`, `idempotency_key` | created in rwb_case | Platform library | Outbox, inbox and idempotency objects |

`write_off`, `debt_sale`, `deviation`, `document` and `partner` are other services' tables: this story holds no foreign key into any of their schemas, no cross-schema join and no copy of a row. `decision_log_entry` and `rule_row` are rwb-decision's and are reached only through its contracts. `outbox_event` and `outbox_delivery` are the platform library's.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-writeoff WireMock | The S7 contract of RWB-S7-E6025-CON | The retention-start answer of R-WO-36 with write-off "WO-2026-000625", placement end date 2026-12-31 and recovered amount 0; the Close answer of R-WO-47 with business date 2027-06-30; the Hold answer of R-WO-48; an answer for a case in the wrong stage; an answer with no rule ID; a delayed answer beyond 2 s; an unreadable answer |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing it for RW-REFADM, and excluding a case from an Own scope |
| rwb-document WireMock | The P5 contract, used by the composite route only | Two documents of case "RW-2026-000625" with their retention classes in force, and one document with no class in force |
| gateway-bff composite route stub | The DP-19 route of SCR-27 | The merged screen model of AC8: the stage, the closing date and reason, the stopped clocks, the write-off state and the documents |
| Parameter and reference fixtures | This story's own test data | The retention period row for product group "MORTGAGE" with the fixture value "P1" and a second value "P2"; the retention timer type in LOV-TIMER; WRITTEN_OFF in LOV-CLOSURE; STOPPED in LOV-TIMER-STATUS. The period and the timer type value are Not specified in the source documents (GAP-0741; ASM-1357; ASM-1358) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, two consumed | The S7 answer and the P4 authorise; one hop, 2 s, breaker per downstream |
| Kafka | Three published, none consumed | `rwb.case.events.v1` (CaseStateChanged, TimerBreached) and `rwb.decision-record.v1` (DecisionRecorded), all through the outbox |
| Temporal | One workflow | CaseWorkflow, extended with the retention durable timer; three steps and no child workflow |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `caseclosure`, front end `src/modules/recovery/case/CaseClosurePanel.tsx`.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Only DP-03, DP-13 and DP-19 are in this slice's pattern set. DP-01, DP-02, DP-05, DP-06, DP-07, DP-09, DP-10, DP-11, DP-14, DP-15 and DP-17 are not, so this story applies none of them and adds none: the read of its own schema, the single login, the parameter and reference rows, the outbox and inbox, the durable timer and the one-hop call are obligations of the rwb-case baseline stories, the platform contracts and the workflow kit, and are described here as behaviour and not as patterns applied (ASM-1355).

The two H dependencies the DP table adds are held by the platform contract stories and are not repeated in the metadata rows, which carry only the contract dependency of this slice, RWB-S7-E6025-CON. The story is Day 1 and builds against the published contract and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RetentionAnswerController | Controller | The rwb-case side of the S7 contract: accepts the two answers, applies the access check of the caller identity and hands them to the steps |
| RetentionAnswerValidator | Service | Checks the write-off reference, the rule ID, the rule version and the business date; refuses with MSG-GEN-001 or MSG-P3-005 |
| RetentionStartStep | Step of the case router | Reads the case, reads the period, computes the expiry, moves the stage and signals CaseWorkflow |
| CaseClosureStep | Step of the case router | Asks the write-off service on the expiry, checks the case's own open actions and drives the record and the apply |
| CaseStageRepository | Repository | Writes `stage_code`, `status`, `stage_clock_start`, `rule_version`, `closed_date`, `closure_reason` and the next-action fields in `rwb_case` only |
| RetentionTimerWriter | Service | Writes the retention timer row and signals CaseWorkflow with the expiry; writes status STOPPED on every timer of the case at the closure |
| OpenActionGuard | Service | Finds an open task of the case and holds the closure while one is open |
| TaskCanceller | Service | Writes status CANCELED on every open task of the case at the closure |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the rule ID and the rule version, hash-linked, in the same transaction (DP-03) |
| InboxDedupe | Library adapter | Dedupes both answers on the write-off reference and the message key |
| CaseClosurePanel | React component | Shows the closed state, the closing date, the closure reason and the stopped clocks on SCR-27, read only |

**Database and migrations**

- One migration, `V6025_1__case_closure.sql`, adds no column and no table: `closed_date` (DF-CAS-022), `closure_reason` (DF-CAS-023) and the timer and task statuses already exist in `rwb_case`, and the closure writes them.
- One index for the read: a partial index on `recovery_case (closed_date)` where `closure_reason` is not null, so the closed-case read and the retention report are read without a scan.
- The retention timer type is a row of LOV-TIMER and not a database check constraint; no constraint holds a list value.
- The migration runs in this service's own Flyway sequence and touches no other schema.

**Configuration and reference data**

- The retention period row per product group, read through the parameters contract with the version in force; the length is Not specified in the source documents (GAP-0741; ASM-1357).
- The retention timer type in LOV-TIMER, WRITTEN_OFF in LOV-CLOSURE and STOPPED in LOV-TIMER-STATUS; LOV-TIMER holds nine values today and none of them is a retention timer (ASM-1358).
- The rule version in force is the one named in the write-off answer; rwb-case holds no package and evaluates no rule on this path, so no KieBase and no lock file is involved.

**Build steps**

1. `RetentionAnswerController` and `RetentionAnswerValidator` against the S7 contract fake, with the wrong-stage refusal; tests for AC1 and AC5.
2. `InboxDedupe` on the write-off reference and the message key; test for AC4.
3. `CaseStageRepository` and `RetentionTimerWriter` with the period row and the CaseWorkflow signal, and the assertion that no Schedule and no timer-check job is created; test for AC1.
4. `CaseClosureStep` with the ask to the write-off service, `OpenActionGuard` and `TaskCanceller`, in one transaction with the decision record; tests for AC2 and AC4.
5. The Hold branch of R-WO-48, with the untouched clocks and the untouched tasks; test for AC3.
6. The failed decision-record write and the rollback; tests for AC6 and the NFR case.
7. The read path with the authorise guard and the scope, the empty next action of a closed case and the composite-route contract test of SCR-27; tests for AC7 and AC8.
8. A contract-fake run of every S7 answer in isolation, so the story builds before rwb-writeoff lands.

**Feature switch.** `rwb.p3.case-closure`, a service configuration value read as a parameter row. Off: both answers are stored as pending inbox entries, the retention clock is not written, no stage moves and no closure is applied; on: the two steps apply the answers.

**Done when.** The tests of section 16 pass, the RWB-S7-E6025-CON contract tests stay green, every case in RETENTION_RUNNING carries exactly one retention timer, no closed case carries a timer in status RUNNING or a task in status OPEN, and no case in the SIT run has closed without the Close answer of R-WO-47.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-S7-001 | The write-off service reports that the scan is on hold for the missing tax criteria and sends no answer | The scan is on hold until Finance publishes the tax criteria. | rwb-writeoff, passed through unchanged |
| MSG-GEN-001 | An answer carries no write-off reference, no rule ID or no business date | Enter {field}. | This story, in `RetentionAnswerValidator` |
| MSG-P3-005 | An answer arrives for a case in the wrong stage | This case cannot move to {state} from {current}. | This story, in `RetentionAnswerValidator` |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision-record library, surfaced here |
| MSG-P4-002 | A role without the Case record right reads a closed case | You cannot {action} here. Your role does not include it. | rwb-access through the authorise contract, surfaced here |
| MSG-P4-003 | The closed case is outside the caller's scope | This case is not in your scope. | This story, on the read path |

MSG-GEN-001, MSG-P3-005, MSG-P7-003 and MSG-P4-002 are copied unchanged from the legacy story and no identifier is renumbered by the realignment; MSG-P4-003 is the scope refusal used by the other reads of this service, so both answer a case outside scope the same way. For MSG-GEN-001 the placeholder {field} is the name of the field the answer left empty, such as the write-off reference or the business date. For MSG-P3-005, {state} is the stage the rule starts from and {current} is the stage of the case. The refusal order is fixed: session, then right, then scope, then the answer's own fields, then the stage the rule starts from, and only then is a row read or a state moved.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-27 Write-off proposal | Approved and closed | The stage "Closed", the closing date and the closure reason of the case, and every clock shown as stopped |
| SCR-27 Write-off proposal | Retention running | The stage "Retention running", the retention clock with its expiry, and no action offered on the case |
| SCR-27 Write-off proposal | Closure held | The stage "Retention running" with the hold recorded, and the clocks still running |
| SCR-27 Write-off proposal | Read refused | MSG-P4-002 for a role without the Case record right, MSG-P4-003 for a case outside the scope |

SCR-27 is composed by the gateway-bff composite route, which calls rwb-case for the case and its clocks, rwb-writeoff for the write-off state and rwb-document for the documents, in parallel and one hop each, and merges the answers into the screen model (DP-19); the browser calls one route and no owner service. This story serves the case-side facts read only and offers no action, no reopening and no clock change. The screen field order, the masking and the merge order are Not specified in the source documents (GAP-0741; ASM-1362) and belong to the edge contract story and to the designer. The write-off screen, its buttons and the place a reopening of a closed case would take remain with RWB-S7-E6025-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-025-01 | AC1, AC2, AC8 | Component | S7 stub answers R-WO-36 for write-off "WO-2026-000625" with placement end date 2026-12-31 and answers Close of R-WO-47 with business date 2027-06-30; the case is read on the composite route |
| TC-E6-025-02 | AC1, AC4 | Component | Case in PLACED_WITH_AGENCY with recovered amount 0, the period row of MORTGAGE at "P1", and the same answer delivered twice |
| TC-E6-025-03 | AC2, AC3, AC5 | Component | Retention clock fired; the Close answer, the Hold answer of R-WO-48 with a document that has no class, and a retention-start answer for a case in RETENTION_RUNNING |
| TC-E6-025-04 | AC6 | Component | Decision-record store stopped on the closure path; nothing changes and MSG-P7-003 is shown |
| TC-E6-025-05 | AC7 | Component | RW-REFADM without the Case record right reads a closed case; refused with MSG-P4-002; another owner's case in an Own scope refused with MSG-P4-003 |
| TC-E6-025-06 | AC6 | NFR | Decision-record write forced to fail on the closure; the stage, the closing date, the clock statuses and the task statuses are unchanged and the retry closes once |

The six legacy test cases are kept in their legacy order and mapped to the levels of this template: the legacy System cases become Component, the legacy Access case becomes Component and the legacy resilience case becomes NFR, because the cross-service behaviour of this key is proved by RWB-ITG-E6025-ITG, which also holds the `-ITG` copy of each case. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the retention period, the retention timer type, the closure reason, the rule ID and the rule version are rows, reference data or contract fields, and the code holds behaviour only.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs, write-off references and rule IDs, never account numbers, names or identity numbers, and the workflow payloads pass the payload codec.
- No read of another service's tables and no ACE view: the decision comes from the S7 contract, the rights from rwb-access, the documents from rwb-document on the composite route, and `rwb_case` holds no foreign key into another schema.
- The cash recovered, the loss, the closing entry, the placement, the sale and the documents are not stored, echoed or validated by rwb-case.
- A read of a closed case writes nothing and raises no event.
- The decision record is written in one transaction with the stage change and the clock and task statuses; a failed write rolls the whole closure back (R-UNI-39).
- A closed case carries no timer in status RUNNING and no task in status OPEN, so it never reaches a work queue again.
- The retention expiry is a durable timer and not a Schedule; no Quartz row and no timer-check job is added.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only.
- One hop only: the service calls the write-off contract and the authorise contract and never calls a service that calls another.

### 18. Traceability

The Epics 3 to 8 story RWB-E6-025 carries no requirement ID, and the plan allocates none to this slice, so this story claims none (ASM-1361). The requirement behind the feature is REQ-S7-008 of the Program requirements — a case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver — with BR-057 and RULE-022 of the Epics 3 to 8 requirements and NFR-031 for the retention rule by record class; all four are claimed by the write-off slice RWB-S7-E6025-APP and proved end to end by RWB-ITG-E6025-ITG. The trace here goes through the legacy feature, the three rules the story applies and the test cases it holds.

| Reference | Requirement (short) | Source section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | Start the retention period when the placement term has run | Epics 3 to 8 v3, RWB-E6-025, AC2 | FEAT-WOF-13 | 9 Write-off (D9) | R-WO-36 | TC-E6-025-01, TC-E6-025-02 |
| REQ-S7-008, BR-057, RULE-022, NFR-031 (claimed by RWB-S7-E6025-APP) | Close the case when the retention period has run and no action is open | Epics 3 to 8 v3, RWB-E6-025, AC1 and AC3; Program requirements REQ-S7-008 and NFR-031 | FEAT-WOF-13 | 9 Write-off (D9) | R-WO-47; R-WO-48 | TC-E6-025-01, TC-E6-025-03 |
| D-RCV-60 DP-03 | The decision is recorded locally in the same transaction and published on `rwb.decision-record.v1` | Template and Rules §R5.5; TSD P3 v3 T5.3 | FEAT-WOF-13 | 9 Write-off (D9) | R-WO-36; R-WO-47; R-UNI-39 | TC-E6-025-02, TC-E6-025-04, TC-E6-025-06 |
| D-RCV-60 DP-13 | The case is served on `/api/recovery/case/v1` | Template and Rules §R5.5; Architecture v5 slide 14 | FEAT-WOF-13 | 9 Write-off (D9) | R-WO-47 | TC-E6-025-01, TC-E6-025-05 |
| D-RCV-60 DP-19 | SCR-27 is a gateway-bff composite route over rwb-case, rwb-writeoff and rwb-document, read only | Template and Rules §R5.5; Architecture v5 slide 10 | FEAT-WOF-13 | 9 Write-off (D9) | R-WO-47 | TC-E6-025-01, TC-E6-025-05 |

| Legacy reference | Where it is kept |
|---|---|
| The story statement and the closing purpose of AC1 | Metadata, sections 1, 2, 7 |
| The states PLACED_WITH_AGENCY, RETENTION_RUNNING and CASE_CLOSED with R-WO-36 and R-WO-47 | Sections 7 AC1 to AC3, 8 BR1 to BR3, 9 |
| The stopping of every timer and the closing entry with cash recovered and loss | Sections 4 step 9, 7 AC2, 8 BR2 and BR7, 11 |
| The unrecorded-action criterion AC4 with MSG-P7-003 | Sections 5 X3, 7 AC6, 14 |
| The two legacy write-off operations and the write-off rights | Section 10 and section 19: both are rwb-writeoff's |
| The legacy data block with `recovery_case`, `timer`, `partner`, `decision_log_entry` and `rule_row` | Section 11 |
| The legacy test set TC-E6-025-01 to TC-E6-025-06 | Section 16 |
| Legacy key RWB-E6-025, story RWB-P3-E6025-APP, contract RWB-S7-E6025-CON | Metadata, sections 1, 3, 12 |

### 19. Out of scope

- The placement, its term, the recovery made under it and the answer that closes it: rwb-partner (S9) and rwb-writeoff (S7).
- The scan, the eligibility and tax criteria, the committee, the posting, the exception loop and the write-off route set: RWB-S7-E6025-CON and RWB-S7-E6025-APP.
- The cash recovered, the loss and the closing entry: rwb-writeoff's, read on the composite route and never stored here.
- The documents, their retention class, the retention job JOB-17 and the document task that a missing class raises: rwb-document (P5) and R-WO-48.
- The sale of a charged-off population, the buyer, the remittance and the data transfer: rwb-debtsale (S6).
- The deviation records and the exception that holds a closure open: rwb-deviation (S8).
- A legal hold over expiry and the disposal decision at the end of a retention period: rwb-access and rwb-document under NFR-072 and NFR-074.
- Reopening a closed case, which needs a written rule, a reason and an approver (REQ-S7-008).
- A payment that arrives after the closure (R-WO-49) and the move it makes on the closed case.
- The four legacy acceptance criteria of RWB-E6-025, which stay with RWB-S7-E6025-APP and RWB-ITG-E6025-ITG.
- The editable states of SCR-27 and the write-off screen, and the place a reopening would take: RWB-S7-E6025-APP.
- The full case record view and the timer and deviation sections: the case record view and timer stories of this service.
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
