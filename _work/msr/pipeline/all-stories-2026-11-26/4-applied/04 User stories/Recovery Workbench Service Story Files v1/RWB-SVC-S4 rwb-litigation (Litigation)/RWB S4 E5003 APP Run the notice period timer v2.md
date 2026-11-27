# RWB-S4-E5003-APP Run the notice period timer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S4-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5003-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-003 for rwb-litigation (S4). The statutory notice period is run as a durable timer of the litigation stage on base `/api/recovery/litigation/v1` (DP-13); the proof of delivery, the notice record and the case route state are consumed on the contracts of their owners (DP-05); one decision record is written through the local decision-record library before the case moves (DP-03); the two screens are read through the gateway-bff composite route (DP-19). The notice, the case, the proof document and the timer ledger stay with rwb-comms, rwb-case and rwb-document and are consumed and faked. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the statutory notice period started from the delivery date of the notice, tracked to its expiry inside the litigation workflow, and the notice marked unserved when no proof arrives inside the proof window — with one decision record written before the case moves —**, so that **a case reaches the pack step on the day the period expires instead of waiting on a spreadsheet, and the case of record, the notice, the proof and the ledger stay with the services that own them**.

This story owns the notice period and the evaluation of its three rules, and nothing else:

- the durable timer of the litigation stage that starts at `delivered_at` and expires at the end of the period, and the two ways it ends — expiry, or the proof window closing with no proof (FSD S4 v3 A2.3; Business Rules and Routing Logic v4 R-LIT-07, R-LIT-08, R-LIT-15);
- the three legal-action operations of TSD S4 T-A on base `/api/recovery/litigation/v1`: API-S4-001 approve the notice, API-S4-002 open the legal action of the notice and API-S4-003 read it, keeping their legacy operation IDs (DP-13);
- the `legal_action` row of the notice in schema `rwb_litigation`, with its columns DF-LEG-001 to DF-LEG-014 and `action_type = NOTICE`, one value of LOV-LEGAL-TYPE (TSD S4 T3.1 and T3.2);
- the evaluation of R-LIT-07, R-LIT-08 and R-LIT-15 from the state table of TSD S4 T4, and the one decision record each evaluation writes through the local decision-record library, with the rule ID and the version in force, before anything moves (DP-03);
- the announcement of the case route fact — `WITH_CUSTOMER_NOTICE_PERIOD`, `NOTICE_UNSERVED` or `PACK_ASSEMBLY` — on the case contract of rwb-case, and the answer it returns.

It does not own the case, the notice record, the proof document or the ledger. `recovery_case`, its route state and the case timer ledger `timer` (DF-WRK-027 to DF-WRK-036) are rwb-case's: slide 10 of Architecture v5 gives the case service "case, stage, tasks, timers from schema rwb_case", and this service owns no `timer` table. The notice and its WIN delivery result are rwb-comms's (P6, "Notices rwb-comms" on Architecture v5 slide 10), even though the Ownership Map gives S4 the approve operation on a notice. The proof of delivery is a document of rwb-document (P5) — "attach the proof" in R-LIT-07 names WIN and DMS. The central `decision_log_entry` and `rule_row` are rwb-decision's (P7). No component of this story writes a `recovery_case`, `timer`, `notice`, `document`, `decision_log_entry` or `rule_row` row, and none reads a `v_ace_*` view (DP-01, DP-05).

### 2. Business rationale

Litigation takes 21 days to file, packs are incomplete and law-firm progress is not tracked (FSD S4 v3 A1.3). The notice period is the first clock of that journey and the only one that starts on a fact the bank does not produce: the WIN proof of delivery. The legacy story ran the clock as a `timer` row of the one `recovery` schema, moved the case status beside it and wrote the decision log entry in the same transaction, with the notice, the proof and the case all in reach.

The target cuts that in four. The clock is a durable timer of the litigation workflow, so a period that starts today and expires after many releases and restarts still fires on time (Temporal design slide 7, "a timer set today can fire in 2028"). The case state that the three rules move is the case of record's. The notice and its served result are the communications service's. The proof is the document hub's. What stays here is the rule answer, the period, the legal action of the notice and the decision record.

Three facts make the story more than a renamed job. First, the period length is not a number: R-LIT-07 gives "notice period by product and type" as its timing column, so the length is a versioned reference row read at run time and the expiry is computed from `delivered_at`, never from the dispatch date (BR2). Second, the period has three exits, not one: expiry with no cure and no dispute opens pack assembly on R-LIT-15, a payment in full closes the case on R-LIT-12, a dispute pauses the litigation timers on R-LIT-14, and the two last ones are the case's and the deviation service's to apply. Third, the decision record is written before the case moves, and a failed write changes nothing and shows MSG-P7-003: that is legacy AC4, and it is DP-03 applied exactly where the legacy `DecisionLogWriter` sat (TSD S4 T2, "writes the decision log entry before any change").

The legacy in-process reads are retired rather than restated. The old monolith base is served by no path of this service (DP-13). The two screens are read through the gateway-bff composite route (DP-19). The customer fields the legacy data block carries (`v_ace_customer`, DF-ACE-055 to DF-ACE-074) are read by no path of this story: a notice period is computed from a delivery date, a product group and a notice type, and the borrower's identity never enters this service (BR7).

It serves FEAT-LIT-03 "Run the notice period timer", it holds the FSD S4 measure "litigation turnaround, 6 days" by removing the manual wait between delivery and the pack step, and it keeps the legacy prerequisite FEAT-CWC-11 by consuming the case workflow of rwb-case rather than re-implementing a case state machine. The four legacy criteria AC1 to AC4 belong to this story and are copied word for word in section 7. The legacy master and the Epics 3 to 8 specification carry no requirement identifier for this feature, so the story traces to the feature until the PRD adds them (GAP-2749; ASM-4569).

### 3. Preconditions

- `RWB-S4-E5003-CON` is published: the three operations on `/api/recovery/litigation/v1`, the notice sub-shape of `LegalAction`, the timer element, the error envelope, the `Idempotency-Key` rule and the fakes. It is the first build dependency of the story and it is available on Day 1.
- The `legal_action` table exists in schema `rwb_litigation` with the columns DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the seven standard columns of T3.0. This story creates no table and no column; the notice period has no column anywhere, because S4 owns no timer table and the ledger `timer` is rwb-case's (GAP-2749; ASM-4571).
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`) and the record is hash-linked on `rwb.decision-record.v1`. It is in the build list and the story builds against its fake until the platform contract publishes.
- `LitigationWorkflow` is registered on task queue `rwb-litigation` in namespace `rwb-recovery`, and the worker runs as the service identity of this service, with no queue of another service and no name cached in code.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-18 Notice approval and SCR-19 Litigation workspace; it is in the build list (DP-19), so both surfaces are readable from Day 1.
- The notice read and the served-result announcement of rwb-comms, the proof attach of rwb-document, the case read and route fact of rwb-case, and the approval route of rwb-decision are consumed and answered by their fakes. None of the four is in this story's dependency rows and no source names their operations: each carries `Not specified in the source documents (GAP-2749; ASM-4577)`.
- LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2 are read at their version in force through the reference data of rwb-case. DP-07 is not in this story's pattern set and the read carries no dependency row (GAP-2749; ASM-4569).
- The reference row of the notice period length and the proof window of R-LIT-08 are rows of the business with a version: the length is `Not specified in the source documents (GAP-2749; ASM-4569)` and the window is the 7 days of the rule's timing column (ASM-4570).
- The caller holds a Workbench role with a Litigation right on the operation it calls (TSD S4 T6.1). DP-08 is not in this story's pattern set: the right of the screen path is enforced at the edge, and the right on the write paths is this story's design.
- The service runs as its own login on `rwb_litigation` (DP-01, DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. The notice of the case is approved on `POST /notices/{noticeId}/approve` (API-S4-001) with Litigation right A and an `Idempotency-Key`; the answer is the notice with its approval state. The notice record is rwb-comms's and is read back on its contract.
2. The legal action of the notice is opened on `POST /cases/{caseId}/legal-actions` (API-S4-002) with `actionType = NOTICE`, the case reference, the court where the notice is filed and the firm where the panel already instructed one; the row is written with status `OPEN`.
3. WIN returns the dispatch result and, later, the proof of delivery. The result reaches the workflow as the `noticeDeliveryResult` signal of the litigation stage: `served_result`, `delivered_at`, the notice reference and the proof reference. No topic and no consumer is added (12.4).
4. `NoticeDeliveryValidator` checks the signal against the notice read of rwb-comms — the notice exists, it belongs to the case of the action and its state is `NOTICE_DISPATCHED` — and against LOV values in force. A failed check ends the step with nothing written.
5. `NoticePeriodRuleEvaluation` evaluates R-LIT-07 with the rule package in force: from `NOTICE_DISPATCHED`, on `PROOF_OF_DELIVERY_RECEIVED`, condition `served_result = delivered`, action "attach the proof and start the notice period from delivered_at", to `WITH_CUSTOMER_NOTICE_PERIOD`. The condition values are compared against reference rows, never against literals in code.
6. `NoticePeriodDecisionWriter` writes one decision record through the local decision-record library **before** anything moves: rule ID `R-LIT-07`, the version in force, the inputs reference, the answer, the decision code read from LOV-DECISION and the two hashes. A failed write ends the step with nothing changed and MSG-P7-003 (AC4).
7. `ProofAttachClient` asks rwb-document to attach the proof to the notice — WIN and DMS in R-LIT-07's systems column — and keeps the returned proof reference on the legal action's inputs reference. The document, its custody and its retention are the hub's.
8. `NoticePeriodTimer` reads the period length for the product group and the notice type as a versioned reference row, computes `period_expires_at` from `delivered_at` and starts one durable timer of the stage. The timer holds `started_at`, `expires_at` and the rule ID in the workflow state; it is not a Schedule, not a row here and not a timer table of this service (12.6).
9. `CaseRouteClient` announces the route fact `WITH_CUSTOMER_NOTICE_PERIOD` with rule `R-LIT-07` and its version, the case reference and the legal action reference, and accepts the answer. rwb-case writes the case and its state; this service writes no case row (BR3).
10. Inside the period, a payment in full, an accepted treatment or a dispute ends the clock early. Those are R-LIT-12, R-LIT-13 and R-LIT-14, and each is a case move of rwb-case and a pause or a closing of the deviation service's; this story stops its timer on the signal the case contract returns and writes the decision record of the stop (12.4, section 9).
11. When the proof window of 7 days closes with no proof, `NoticePeriodRuleEvaluation` evaluates R-LIT-08 from `NOTICE_DISPATCHED` on `PROOF_WINDOW_EXPIRED`: "mark the notice unserved; the notice period does not start", to `NOTICE_UNSERVED`. The notice period is not started at all, and no timer of a period exists.
12. The decision record of R-LIT-08 is written through the library before the notice and the case are touched; `NoticeUnservedClient` then announces the unserved result to rwb-comms for the notice row and the route fact `NOTICE_UNSERVED` with rule `R-LIT-08` to rwb-case.
13. At `period_expires_at` the timer fires and R-LIT-15 is evaluated from `WITH_CUSTOMER_NOTICE_PERIOD` on `NOTICE_PERIOD_EXPIRED`: "no cure and no dispute at period_expires_at", action "open pack assembly", to `PACK_ASSEMBLY`, owner "Workbench", 3 working days. Its decision record is written first and the route fact `PACK_ASSEMBLY` is announced to rwb-case, which opens the pack stage.
14. `PrescriptionWarningCheck` raises MSG-S4-002 with the prescription date when the date carried by the case read falls inside the warning window. It is a warning, blocks nothing, and the prescription clock itself is never paused and never owned here.
15. SCR-18 and SCR-19 read the notice, the legal action, the period state and its dates through the composite route, read only, next to the case state of rwb-case and the notice of rwb-comms.
16. The same signal twice, or the same `Idempotency-Key` twice, writes one legal action and one decision record and starts no second timer; the repeat is counted under R-UNI-40.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The signal carries no notice reference, no `served_result`, or a value outside the reference set; or `delivered_at` is absent on a delivered result | The step ends with nothing written and no timer; the failure is logged against the signal key | MSG-GEN-001 | AC1, AC2 |
| X2 | The notice read answers 404, or the notice belongs to another case than the action | 404 at the API, nothing written and no timer started | None | AC1 |
| X3 | The notice state is not `NOTICE_DISPATCHED`, or the legal action is not `OPEN` | 409 and nothing changes; a period is never started twice and never restarted on an already-unserved notice | None | AC1, AC3 |
| X4 | The proof window closes with no proof, or the result is refused, returned or undeliverable | R-LIT-08 marks the notice unserved and the period does not start; the refused, returned and undeliverable results of R-LIT-09 are the notice story's and are announced to it here | None | AC3 |
| X5 | A payment in full, an accepted treatment or a dispute arrives inside the period | The case move is rwb-case's; this story stops its timer, records the stop, and releases the case fact unchanged | None | AC1 |
| X6 | The prescription date of the case falls inside the warning window | MSG-S4-002 is shown with the date; nothing is blocked and no timer changes; the legal deadline never pauses (R-DEV-01) | MSG-S4-002 | AC1 |
| X7 | A role without the Litigation right calls an operation | Refused before any read or write; no decision record and no timer | MSG-P4-002 | TC-E5-003-05 |
| X8 | The local decision-record write fails | Nothing changes: no proof is attached, no timer starts, no route fact leaves the service | MSG-P7-003 | AC4 |
| X9 | The proof attach of rwb-document does not answer inside 2 s, or its breaker is open | The step keeps the decision record it wrote, starts no timer and answers 503 with the platform envelope; the hand-off is re-run with the same signal key | None | AC1 |
| X10 | The case contract refuses the route fact | The decision record stands, the refusal is recorded for the case owner and the caller reads the refusal unchanged; this service does not move the case itself | None | AC2, AC3 |
| X11 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5003-CON`, the decision-record library and the composite route; the four consumed contracts and the reference data are faked and their absence from the dependency rows is recorded (GAP-2749) |
| Negotiable | The period length, the proof window instant, the warning window and the list values are versioned reference data; the story fixes the behaviour, the shapes and the rule answers, not the values |
| Valuable | Removes the manual wait between delivery and the pack step and makes the period survive releases; it is the clock behind the 21-day to 6-day turnaround |
| Estimable | Three operations, one validator, three rule evaluations, one library write, one timer, two clients to comms and one each to document and case, one read-only screen fragment |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each of the four criteria of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5003-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Run the notice period timer, in rwb-litigation

  Background:
    Given the notice "NT-2026-000301" of case "RC-2026-000301" and its legal action "LA-2026-000301" with action type "NOTICE"
    Given the rule package of R-LIT-07, R-LIT-08 and R-LIT-15 is in force at its version, and LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Run the notice period timer (legacy RWB-E5-003 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-comms contract mock returns the notice "NT-2026-000301" dispatched with served result "delivered" and delivered date "2026-03-16"
    Given the rwb-case contract mock returns the case "RC-2026-000301" in state "NOTICE_DISPATCHED" and accepts the route fact
    When its trigger arrives
    Then starts and tracks the statutory notice period and raises it when it expires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-07 (legacy RWB-E5-003 AC2)
    Given a case in state NOTICE_DISPATCHED
    Given the rwb-comms contract mock returns the notice "NT-2026-000301" with served result "delivered" and delivered date "2026-03-16"
    Given the rwb-document contract mock returns the proof "DOC-2026-000901" attached to the notice
    When proof of delivery received
    Then attach the proof and start the notice period from delivered_at
    Then the case moves to WITH_CUSTOMER_NOTICE_PERIOD

  Scenario: AC3 Rule R-LIT-08 (legacy RWB-E5-003 AC3)
    Given a case in state NOTICE_DISPATCHED
    Given the rwb-comms contract mock returns no proof of delivery for the notice "NT-2026-000301" inside the proof window of 7 days
    When proof window expired
    Then mark the notice unserved; the notice period does not start
    Then the case moves to NOTICE_UNSERVED

  Scenario: AC4 Not recorded (legacy RWB-E5-003 AC4)
    Given the decision log cannot be written
    Given the decision-record library stub returns a stopped chain
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

These four criteria are the legacy criteria of RWB-E5-003, copied word for word: not one legacy line is reworded, shortened or renumbered, and every value of the source (`NOTICE_DISPATCHED`, `WITH_CUSTOMER_NOTICE_PERIOD`, `NOTICE_UNSERVED`, `delivered_at`, MSG-P7-003) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside each scenario, the `Given` lines that answer a cross-service fact from its contract fake. The case states of AC2 and AC3 are states of the case of record, moved by rwb-case on the announcement of this service (BR3); the status of the legal action itself stays `OPEN` (section 9). The contract half of these surfaces is tested in `RWB-S4-E5003-CON`, and the end-to-end journey across the four services is not claimed here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| R-LIT-07 | Litigation · D7 · from `NOTICE_DISPATCHED` · event `PROOF_OF_DELIVERY_RECEIVED` · condition `served_result = delivered` · action "attach the proof and start the notice period from delivered_at" · to `WITH_CUSTOMER_NOTICE_PERIOD` · owner "Customer" · channel "WIN and DMS, Workbench" · timing "notice period by product and type" | Business Rules and Routing Logic v4 (R-LIT-07); TSD S4 T4; FSD S4 A2.3.3.1 |
| R-LIT-08 | Litigation · D7 · from `NOTICE_DISPATCHED` · event `PROOF_WINDOW_EXPIRED` · condition "no proof returned inside the proof window" · action "mark the notice unserved; the notice period does not start" · to `NOTICE_UNSERVED` · owner "Litigation officer" · channel "WIN and DMS" · timing 7 days | Business Rules and Routing Logic v4 (R-LIT-08); TSD S4 T4 |
| R-LIT-15 | Litigation · D7 · from `WITH_CUSTOMER_NOTICE_PERIOD` · event `NOTICE_PERIOD_EXPIRED` · condition "no cure and no dispute at period_expires_at" · action "open pack assembly" · to `PACK_ASSEMBLY` · owner "Workbench" · channel "Workbench, Document Hub" · timing 3 working days | Business Rules and Routing Logic v4 (R-LIT-15); FSD S4 A2.3.3.1 |
| R-LIT-09 | From `NOTICE_DISPATCHED` on `DELIVERY_FAILED` for a refused, returned or undeliverable result, the notice goes to `NOTICE_UNSERVED` and an alternate service method is queued; it is evaluated with R-LIT-08 and is the notice story's partner path | Business Rules and Routing Logic v4 (R-LIT-09) |
| R-LIT-12, R-LIT-13, R-LIT-14 | The three early exits of `WITH_CUSTOMER_NOTICE_PERIOD`: a payment in full closes the case, an accepted treatment returns it to treatment, a dispute raises X1 and pauses the litigation timers. The case move is rwb-case's and the pause is rwb-deviation's; this story stops its timer | Business Rules and Routing Logic v4 (R-LIT-12, R-LIT-13, R-LIT-14) |
| BR1 | The notice period is this service's clock and the notice record is not: the period is a durable timer of the litigation stage, the notice and its served result are rwb-comms's (P6), and the ledger row `timer` is rwb-case's (DF-WRK-027 to DF-WRK-036) | Architecture v5 slide 10 ("case, stage, tasks, timers from schema rwb_case"); Ownership Map (S4 owns `hearing` and `legal_action`) |
| BR2 | The period is computed and never written in code: its length is a versioned reference row read by product group and notice type, and its expiry is `delivered_at` plus that length, never the dispatch date | R-LIT-07 timing column; Template and Rules section R7.2 (s17) |
| BR3 | The case move is answered, not written: the three targets of the rules are route states of rwb-case and this service announces the route fact with the rule and its version and accepts the answer | TSD S4 T4; `ownership.json` (`recovery_case` owner P3); Architecture v5 slide 41 |
| BR4 | No ACE read: this story reads no `v_ace_*` view, no ACE table and no other `rwb_*` schema, and its login holds no such grant; the WIN delivery facts arrive through rwb-comms, not from `v_ace_pod` here | DP-01, DP-05 as a prohibition; Architecture v5 slide 29 |
| BR5 | The decision is written before the effect: one record through the local library with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 |
| BR6 | Closed vocabulary: `action_type` and `status` take only the values of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS in force, read with their version; no list member, date and period length appears in Java | TSD S4 T3.2; FSD S4 A2.3.3.1 (BR-S4-003) |
| BR7 | No personal data: the row, the decision record, the timer state, the logs and every call carry identifiers, list values, dates and one amount at most; the borrower and the guarantor never enter this service | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes |
| BR8 | The same signal or the same `Idempotency-Key` twice writes once and counts the repeat; a second timer is never started for the same notice | R-UNI-40; TSD S4 T-A.1 (API-S4-001 and API-S4-002 `Idempotency-Key`) |
| R-UNI-39 | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC4 |
| R-UNI-31 | When `prescription_days_remaining` reaches the warning threshold the case is forced to a litigation review ahead of every other open action; the warning this story shows is the MSG-S4-002 of that threshold | Business Rules and Routing Logic v4 (R-UNI-31); FSD S4 A2.3.3.1 (VR-S4-003-1) |

The period length that R-LIT-07's timing column names has no value in any source read for this key, and neither has the warning threshold of R-UNI-31: both are versioned reference rule rows, and their content carries the placeholder `Not specified in the source documents (GAP-2749; ASM-4569)`.

### 9. State transitions

Three objects move here and they are never used one for the other: the status of this service's legal action, the case state of rwb-case, and the timer of the stage.

**`legal_action.status`** — the values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The notice is approved and its action opened on API-S4-001 and API-S4-002 | `actionType = NOTICE`, the request validates and the decision record is written | `OPEN` |
| `OPEN` | The proof of delivery arrives and R-LIT-07 fires | `served_result = delivered` and the notice is `NOTICE_DISPATCHED` | `OPEN`, with the proof attached and the period timer started |
| `OPEN` | The proof window closes and R-LIT-08 fires | No proof inside the 7-day window | `OPEN`, with the unserved result announced and no period timer |
| `OPEN` | The period expires and R-LIT-15 fires | No cure and no dispute at `period_expires_at` | `OPEN`; the pack is the case's stage, not a status of this row |
| `OPEN` or `FILED` | The case is closed or the action withdrawn on R-LIT-12 or R-LIT-39 | The closing step of the case of record | `CLOSED` or `WITHDRAWN` |

No value of LOV-LEGAL-STATUS names a period, a served or an unserved notice, so the period lives on the timer and the served result on the notice: the value of the word "tracked" of AC1 has no list member, and it is `Not specified in the source documents (GAP-2749; ASM-4571)`.

**The notice period timer** — one durable timer of the stage, held in the workflow state and not in a row:

| From | Trigger | Condition | To |
|---|---|---|---|
| (none) | R-LIT-07 fires | The proof is attached and the decision record written | Running, with `started_at = delivered_at` and `expires_at` computed from the reference length |
| Running | `period_expires_at` reached | No cure and no dispute | Fired, and R-LIT-15 announced as `PACK_ASSEMBLY` |
| Running | Payment in full, accepted treatment or dispute | R-LIT-12, R-LIT-13 or R-LIT-14 answered by the case contract | Stopped, with the stop recorded; the case move is rwb-case's |
| Running | The case moves out of the litigation route | Any other route fact accepted by rwb-case | Cancelled, with the reason recorded |
| (none) | R-LIT-08 fires | The proof window closed with no proof | Never started; the period does not exist for that notice |

**The case states the rules name are rwb-case's**, and this story announces them (BR3):

| From (rwb-case) | Rule and event | To (rwb-case) | Owner of the move |
|---|---|---|---|
| `NOTICE_DISPATCHED` | R-LIT-07 on `PROOF_OF_DELIVERY_RECEIVED` | `WITH_CUSTOMER_NOTICE_PERIOD` | rwb-case, on the announcement of this service |
| `NOTICE_DISPATCHED` | R-LIT-08 on `PROOF_WINDOW_EXPIRED` | `NOTICE_UNSERVED` | rwb-case, on the announcement of this service |
| `WITH_CUSTOMER_NOTICE_PERIOD` | R-LIT-15 on `NOTICE_PERIOD_EXPIRED` | `PACK_ASSEMBLY` | rwb-case, on the timer of this service |
| `WITH_CUSTOMER_NOTICE_PERIOD` | R-LIT-12, R-LIT-13 or R-LIT-14 | `CASE_CLOSED`, `TO_TREATMENT` or `DEVIATION_HOLD` | rwb-case with the payment, treatment and deviation stories |

No case row and no timer row is read as a table or written here; the case read and the announcement of 12.2 are the only paths by which a case state moves (GAP-2749; ASM-4572).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA (TSD S4 T6.1): opens and reads the legal action of the notice, approves the notice (right A) and records the unserved result |
| RW-ENFORCE, enforcement owner | Litigation CRU: opens and reads the notice action in scope; it holds no approve right on a notice |
| RW-LEGAL, legal counsel | Litigation RA: reads the notice action and approves the notice for dispatch |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) and RW-HEADLIT, Head of Litigation | Litigation RA: read and approve, as the legacy permission block of RWB-E5-003 gives them |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read the notice action and its period state only |
| PT-LAWFIRM, law firm user | Partner gateway, Litigation RU on its own instructed cases; it never calls this service directly and never approves a notice |
| rwb-litigation service identity | Validates, evaluates the three rules, writes the decision records and the legal action, runs the timer and calls the comms, document, case and decision contracts; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-case (P3) service identity | Owns the case, its state and the `timer` ledger of DF-WRK-027 to DF-WRK-036; answers the route fact |
| rwb-comms (P6) service identity | Owns the notice, its state and its served result; answers the notice read and the unserved announcement |
| rwb-document (P5) service identity | Owns the proof of delivery; answers the attach |
| rwb-decision (P7) service identity | Owns the approval item, the delegation and the central ledger; answers the approval route |

The rights are the rows of TSD S4 T6.1 and the legacy permission block of RWB-E5-003, and nothing wider: Litigation C for RW-LITOFF and RW-ENFORCE, Litigation A for RW-LITOFF, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT. DP-08 is not in this story's pattern set, so the right of the screen path is enforced at the edge and the guard on the write paths is this story's design; a refusal keeps MSG-P4-002 and changes nothing. The timer of the period is not a person's action and holds no right of its own.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on create; read as the reference of every call |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on create; read and sent on the case, notice and document calls |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Write when the panel already instructed a firm; read |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write, `NOTICE` of LOV-LEGAL-TYPE |
| DF-LEG-008 | legal_action (S4, `rwb_litigation`) | court_name | Read; written by the filing story of this service |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, against LOV-LEGAL-STATUS (`OPEN`) |
| Standard columns | legal_action (S4, `rwb_litigation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity (TSD S4 T3.0) |
| DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-008, DF-DEC-012, DF-DEC-016, DF-DEC-017, DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the legal action or the case moves |
| DF-LEG-015, DF-LEG-018, DF-LEG-021 | notice (P6, `rwb_comms`) | notice type, sent date, served result and the proof reference | Read on the notice contract; the unserved result is announced to its owner, never written here |
| DF-WRK-027, DF-WRK-029, DF-WRK-031, DF-WRK-033 | timer ledger (P3, `rwb_case`) | timer id, case id, timer type, started_at, expires_at | Not written; the case timer row is rwb-case's and this story's timer is the workflow's |
| DF-CAS-001, DF-CAS-002, DF-CAS-004, DF-CAS-008, DF-CAS-011 | recovery_case (P3, `rwb_case`) | id, case no, product group, status, stage code | Read on the case contract for the period length and the warning date; never written here |
| DF-DEC-001 to DF-DEC-018; DF-REF-001 to DF-REF-015 | decision_log_entry and rule_row (P7, `rwb_decision`) | the central ledger and the rule rows | Not written; reached through the decision record and the rule package in force |

Field IDs are those of TSD S4 v2 T3.1, the notice and case identifiers of the legacy data block of RWB-E5-003, and the standard columns of TSD S4 T3.0. **No new table, no new column and no migration:** `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5003-CON`, applied by the service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration (DP-03).

**Not written, not read as a table, and named here so that a reviewer can check the absence:** `recovery_case` and `timer` (P3 rwb-case), `notice` (P6 rwb-comms), `document` (P5 rwb-document), `decision_log_entry` and `rule_row` (P7 rwb-decision), `hearing` and DF-LEG-024 to DF-LEG-029 (S4, untouched by a notice period), and every `v_ace_*` view (P1). `v_ace_customer` DF-ACE-055 to DF-ACE-074 of the legacy data block is read by no path of this story: no step needs the borrower's identity (BR7). The identifiers of the case, the notice, the proof and the approval are values, not foreign keys across schemas (DP-01, BR4).

**No personal data.** The row this story writes carries identifiers, list values and dates. The borrower, the guarantor, the address and the identity number never enter `rwb_litigation` and never enter a log, a timer state or a workflow input.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-001 | POST | `/notices/{noticeId}/approve` | Approve the generated notice for dispatch, which starts the delivery path the period runs from (TSD S4 T-A.2) | Litigation A, scope applied | `Idempotency-Key` required; the answer is stored and a repeat returns it |
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open the legal action of the notice: `action_type = NOTICE` and the decision record of the step (TSD S4 T-A.2) | Litigation C, scope applied | `Idempotency-Key` required |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | Read the legal action with its notice facts, its period state and its decision records (TSD S4 T-A.2) | Litigation R, scope applied | Not applicable |

The three operations, their rights and their error sets are those of TSD S4 T-A.1 and T-A.2; they keep their legacy IDs and differ only in the base, which DP-13 renames. The legacy endpoint block of RWB-E5-003 names the approval and the create; the read is the TSD's E5 operation and is the one the two screens use. Errors: 401 no session; 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference; 409 a notice that is not `NOTICE_DISPATCHED`, an action that is not `OPEN`, or a period already started; 422 a missing or invalid field (MSG-GEN-001); 503 the decision-record library or a consumed contract unavailable. The request and answer shapes are declared by `RWB-S4-E5003-CON`, which this story consumes as its first build dependency.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The notice read and the unserved announcement of rwb-comms, operations `Not specified in the source documents (GAP-2749; ASM-4573)` | P6 rwb-comms | Reads the notice, its notice type, its sent date, its served result and its proof reference, and announces a not-served result back; the notice row is never written here |
| The proof attach of rwb-document, operation `Not specified in the source documents (GAP-2749; ASM-4574)` | P5 rwb-document | Attaches the WIN proof of delivery to the notice and returns its reference; the document and its custody stay with the hub |
| The case read and the route fact of rwb-case, operations `Not specified in the source documents (GAP-2749; ASM-4572)` | P3 rwb-case | Reads the case state, the product group and the prescription date, and announces `WITH_CUSTOMER_NOTICE_PERIOD`, `NOTICE_UNSERVED` or `PACK_ASSEMBLY` with the rule and its version; accepts the answer |
| The approval route of rwb-decision, operation `Not specified in the source documents (GAP-2749; ASM-4576)` | P7 rwb-decision | Routes the approval of the notice where the amount or the product puts it above the officer's own authority and reads the answer; the delegation table is never read here |
| The reference-data read of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS, `RWB-P3-E1043-CON` | P3 rwb-case | The two list codes at their version in force (DP-07, declared although the pattern is not in this story's set) |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020). No operation of another service is declared as provided here (BR1).

#### 12.3 Events published

None. `rwb.litigation.events.v1` is this service's topic with its retry and `.dlt` topics, and the Ownership Map gives S4 zero events, so this story adds no outbox row and no producer; DP-09 is not in its pattern set. The decision records it writes are elements of the local decision-record library, which publishes `DecisionRecorded` (event 08) on the shared `rwb.decision-record.v1`; that element is the library's and this service declares no payload of its own. The case fact leaves on the case contract, not on a topic (12.2).

#### 12.4 Events consumed

None. The delivery result is not a subscription: it reaches the litigation stage as the `noticeDeliveryResult` signal of `LitigationWorkflow`, sent by the notice story of this service on the answer of the rwb-comms contract, so this story holds no consumer, no inbox and no subscription. Architecture v5 slide 19 shows `NoticeDelivered` among the inputs of rwb-litigation while the Ownership Map gives S4 no event and DP-09 is not applied here: whether that event exists and who consumes it is left open by the sources read and is carried as GAP-2749 with ASM-4575.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LitigationWorkflow | Workflow, one run per case stage, the S4 child of CaseWorkflow | `rwb-litigation` | Started by CaseWorkflow on rwb-case; holds the stage, its durable timers and its signals (Temporal design slide 13) |
| noticeDeliveryResult | Signal | `rwb-litigation` | The WIN delivery result: notice reference, `served_result`, `delivered_at` and the proof reference |
| openNoticeAction | Activity | `rwb-litigation` | The approval of the notice and the create of its legal action, steps 1 to 3 |
| evaluateNoticePeriodRule | Activity | `rwb-litigation` | R-LIT-07, R-LIT-08 or R-LIT-15 with the rule package in force |
| recordDecision | Activity through the library | `rwb-litigation` | The local decision record and its outbox row, written before the change (DP-03) |
| attachProof | Activity | `rwb-litigation` | The proof attach of rwb-document and the reference it returns |
| startNoticePeriod | Activity | `rwb-litigation` | The reference length, `period_expires_at` and the durable timer of the stage |
| announceCaseRoute | Activity | `rwb-litigation` | The route fact to rwb-case and its answer |
| announceNoticeUnserved | Activity | `rwb-litigation` | The unserved result to rwb-comms and its answer |
| expireNoticePeriod | Activity, after the timer fires | `rwb-litigation` | R-LIT-15 at `period_expires_at` and the `PACK_ASSEMBLY` announcement |
| prescriptionWarning | Activity | `rwb-litigation` | The MSG-S4-002 warning with the case's prescription date; it blocks nothing |

The workflow name is fixed by the Temporal and Drools design (`LitigationWorkflow` on `rwb-litigation`, in the stage list of the service). The activities are this story's registration; no source names them, so their names are this design's and carry no source value. The Quartz reference of FSD S4 A2.3.2 is not carried as a job: the period is a durable timer of the workflow and no Quartz job and no Schedule is created (12.6, GAP-2749 with ASM-4571).

#### 12.6 Schedules

None. The notice period is a durable timer inside one workflow run, started on `delivered_at` and fired at `period_expires_at`; it is not a Temporal Schedule, because a period belongs to one case and one notice and not to a calendar. No Schedule of Architecture v5 slide 44 is owned, moved or registered here. DP-10 is not in this story's pattern set, so no `RWB-PLT-E1071-CON` row is added; the Quartz marker of FSD S4 A2.3.2 is retired to the workflow timer and the absence of the platform row is part of GAP-2749.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (rwb_litigation) | The notice action: `action_type = NOTICE`, status DF-LEG-014, the case and firm references |
| decision_record | PLT library, created in `rwb_litigation` | The hash-linked record of each rule answer, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the approval and of the create, with the stored answer |

Not owned and never written: `recovery_case` and `timer` (P3), `notice` (P6), `document` (P5), `decision_log_entry` and `rule_row` (P7), `hearing` (S4, another story). No `v_ace_*` view and no ACE table is read (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice WireMock | Notice `NT-2026-000301` of `RC-2026-000301` in state `NOTICE_DISPATCHED`, a delivered result with `delivered_at` `2026-03-16`, a refused result, an absent result, a 404 and a delayed answer | AC1, AC2, AC3, X2, X4 |
| rwb-document WireMock | Proof `DOC-2026-000901` attached to the notice with its reference, and a 503 | AC2, X9 |
| rwb-case WireMock | Case `RC-2026-000301` at `NOTICE_DISPATCHED` with its product group and prescription date, the three route facts accepted, a refusal from another state and a delayed answer | AC1, AC2, AC3, X5, X10 |
| rwb-decision approval WireMock | The approval item of the notice granted and refused with a reason (placeholder operation name) | AC1, X7 |
| decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC1, AC4 |
| reference-data WireMock | LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force, and the notice-period length rows by product group and notice type | AC1, AC2, AC3 |
| Workflow test environment | A clock that advances to `period_expires_at` and to the end of the 7-day proof window without waiting | AC1, AC3 |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The merged SCR-18 and SCR-19 answer for `RC-2026-000301`, with the notice read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S4-E5003-CON` or against the comms, document, case and decision documents is a build failure.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 5 consumed | API-S4-001, API-S4-002 and API-S4-003 provided; the notice read and announcement, the proof attach, the case read and route facts, the approval route and the reference data consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed; `DecisionRecorded` is the library's element (12.3, 12.4) |
| Temporal | 1 workflow, 9 activities, 1 signal, no child workflow, no Schedule | `LitigationWorkflow`, its activities, its `noticeDeliveryResult` signal and its durable period timer |
| File | None | No file is read, built or delivered here; the proof is the document hub's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `noticeperiod`, Java package `th.co.scb.ace.workbench.recovery.litigation.noticeperiod`; front end `src/modules/recovery/litigation/NoticePeriod.tsx`, the fragment SCR-18 and SCR-19 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data through rwb-source-data's contract or the service's own ACE views; applied here as a prohibition: the WIN delivery facts arrive through rwb-comms and no view is read | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the operations keep API-S4-001, API-S4-002 and API-S4-003 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC4's fail-closed behaviour. DP-05 is applied in its negative form: the legacy story's data block names `v_ace_customer` and its trigger is a WIN result read from `v_ace_pod`, and neither is read here — the notice and its delivery result are rwb-comms's. DP-13 renames the base and keeps the operation IDs. DP-19 covers the two screens only, and the screen model and the merge order stay with the edge contract. DP-10 is **not** applied although FSD S4 A2.3.2 names a Quartz scheduler: the period is a durable timer of `LitigationWorkflow`, and no `RWB-PLT-E1071-CON` row is added (GAP-2749; ASM-4571).

**Dependencies the table adds and the plan does not hold.** The pattern table adds exactly the two H rows the metadata carries. Four consumed contracts have no row at all — comms, document, case and decision — and DP-07's reference-data read is in the same position; the five are recorded once as GAP-2749 with ASM-4577. The story builds against their fakes on Day 1 and no C dependency blocks the build (Template and Rules section R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | API-S4-001, API-S4-002 and API-S4-003 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| NoticeDeliveryValidator | Service | The notice exists, it belongs to the case, its state is `NOTICE_DISPATCHED`, the `served_result` and the `actionType` are values in force |
| NoticePeriodRuleEvaluation | Service through the embedded Drools kit | R-LIT-07, R-LIT-08 and R-LIT-15 on the state, the event and the condition rows in force; the version is pinned and recorded |
| NoticePeriodDecisionWriter | Library adapter | One hash-linked record per evaluation, before any change; refuses the step when the write fails (DP-03) |
| NoticePeriodTimer | Workflow component | The reference length, `period_expires_at` and the durable timer; stops on an early exit and never starts after an unserved result |
| NoticeActionWriter | Repository | The `legal_action` row of the notice and the idempotency row, in one `rwb_litigation` transaction |
| NoticeCommsClient | Client | The notice read and the unserved announcement, one hop, 2 s, breaker |
| ProofAttachClient | Client | The proof attach of rwb-document and the reference it returns |
| CaseRouteClient | Client | The case read and the three route facts, one hop, 2 s, breaker |
| NoticeApprovalClient | Client | The approval route of rwb-decision when the notice sits above the officer's authority |
| PrescriptionWarningCheck | Service | The prescription date of the case against the warning window, and MSG-S4-002 |
| LitigationWorkflow | Workflow | The stage on `rwb-litigation`, its `noticeDeliveryResult` signal and its period timer |
| NoticePeriod | React component | The notice, its state and the period with its dates on SCR-18 and SCR-19, read only |

**Database and migrations.** No Flyway file. `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5003-CON`; the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). The notice period has no column and no table: it is the workflow's timer, and the ledger `timer` of DF-WRK-027 to DF-WRK-036 is rwb-case's (BR1, ASM-4571). The index set of `legal_action` is `Not specified in the source documents (GAP-2749; ASM-4579)`; this story needs a lookup by `case_id` and by `id`.

**Configuration and reference data.**

- The notice period length by product group and notice type, as a versioned reference row read with its version. Its content is `Not specified in the source documents (GAP-2749; ASM-4569)`.
- The proof window of R-LIT-08, 7 days, as a versioned reference row, and the instant it starts from per ASM-4570.
- The warning window of R-UNI-31 behind MSG-S4-002, as a versioned reference row; its value is `Not specified in the source documents (GAP-2749; ASM-4569)`.
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force (TSD S4 T3.2), and the decision code of each rule answer as a value of LOV-DECISION.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `NoticeActionWriter` and `NoticeController` over the `legal_action` row and the contract fake; test API-S4-001, API-S4-002 and API-S4-003 with X1 to X3.
2. Build `NoticeDeliveryValidator` against the comms fake, with the 404, the wrong case, the wrong state and the absent result; test X2 and X3.
3. Build `NoticePeriodRuleEvaluation` and `NoticePeriodDecisionWriter` against the library fake, with the stopped chain; test AC1, AC2 and AC4.
4. Build `NoticePeriodTimer` and `startNoticePeriod` with the reference length and the workflow clock; test AC1, the expiry and X5.
5. Build `ProofAttachClient` and the proof reference, with the 2 s budget and the breaker; test AC2 and X9.
6. Build `CaseRouteClient` with the three route facts, the refusal and the delayed answer; test AC2, AC3 and X10.
7. Build R-LIT-08 and the unserved announcement with the 7-day window and `announceNoticeUnserved`; test AC3 and X4.
8. Build `PrescriptionWarningCheck` and MSG-S4-002; test X6.
9. Build `NoticePeriod` and read the notice and the action through the composite route fake; test AC1.
10. Add the boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_comms`, `rwb_document` or `rwb_decision`; test BR4.

**Feature flag.** `rwb.litigation.notice-period-v1`, read as a flag of the platform library; off means the approval and the create of the notice action answer 404 and no period timer starts, while the read of an existing legal action and its period state are unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5003-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one legal action per notice, one period per delivered notice, one unserved result per expired proof window, one decision record per rule answer, no write of a case, timer, notice, document or ledger row from this service, and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-002 | The prescription date of the case falls inside the warning window (X6) | The claim on this case expires on {date}. File before then. |
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which the pack stories of this service raise, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-GEN-001 | A required value of the request or of the delivery signal is missing or outside its list (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the Litigation right of the operation (X7) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the notice or the case moves (X8, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-003 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names. `MSG-S4-002` carries the prescription date read from the case of record, and the warning window behind it is `Not specified in the source documents (GAP-2749; ASM-4569)`. `MSG-S4-001` is authored by the pack stories and is carried here because it is the message set of the key. A downstream that does not answer (X9), a reference that is not found (X2) and a state that refuses the step (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-18 Notice approval | Generated | The notice with its type, its template state and the approve action of API-S4-001 |
| SCR-18 Notice approval | Approved | The approval recorded, the approve action closed and the dispatch awaited |
| SCR-18 Notice approval | Sent | The dispatch result read from rwb-comms, and the legal action of the notice opened with `actionType NOTICE` |
| SCR-18 Notice approval | Delivered | The proof reference, `delivered_at`, the period start and its expiry date, and the rule ID and version of R-LIT-07 |
| SCR-18 Notice approval | Unserved | The unserved result of R-LIT-08, the proof window that closed and the case state announced |
| SCR-19 Litigation workspace | Pack | The legal action of the notice and, once the period expires, the `PACK_ASSEMBLY` state of the case |
| SCR-19 Litigation workspace | Instructed | The same action after the pack, read only for this story |
| SCR-19 Litigation workspace | Filed | The court references, read only; the filing story's |
| SCR-19 Litigation workspace | Hearing | The hearings, read only; the hearing story's |
| SCR-19 Litigation workspace | Judgment | The judgment date and amount, read only |
| SCR-18 Notice approval | Not recorded | MSG-P7-003, and the notice unchanged with no period started |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-18 Notice approval | Failed | A 503 when the proof attach or the case contract did not answer, and the decision record the step kept |

The five SCR-18 states and the five SCR-19 states are the ones the legacy screen block of RWB-E5-003 gives, copied unchanged: SCR-18 carries generated, approved, sent, delivered and unserved, and SCR-19 carries pack, instructed, filed, hearing and judgment. The route merges this service's answer with the notice of rwb-comms and the case of rwb-case; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-003-01 | AC1 | End to end | Notice `NT-2026-000301` of case `RC-2026-000301` delivered on `2026-03-16`; the period length of the product group and notice type at its version; the timer fired at `period_expires_at`; the case fake accepting `WITH_CUSTOMER_NOTICE_PERIOD` and `PACK_ASSEMBLY`; two decision records with the rule IDs and versions |
| TC-E5-003-02 | AC2 | End to end | Case `RC-2026-000301` at `NOTICE_DISPATCHED`; `PROOF_OF_DELIVERY_RECEIVED`; `served_result = delivered`; proof `DOC-2026-000901` attached; `delivered_at` `2026-03-16` as the period start; the case fake answering `WITH_CUSTOMER_NOTICE_PERIOD` |
| TC-E5-003-03 | AC3 | End to end | Case `RC-2026-000301` at `NOTICE_DISPATCHED` with no proof inside the 7-day window; `PROOF_WINDOW_EXPIRED`; the notice unserved, no timer started and the case fake answering `NOTICE_UNSERVED` |
| TC-E5-003-04 | AC4 | End to end | The decision-record library stubbed to stop the chain; the notice and the legal action unchanged, no timer and MSG-P7-003 on the screen |
| TC-E5-003-05 | Access | Component | A role without the Litigation right calls API-S4-001, API-S4-002 and API-S4-003; refused with MSG-P4-002 and nothing written |
| TC-E5-003-06 | Principle 5 | NFR | A forced decision-record write failure on 10 delivered notices; no period starts, no route fact leaves the service and the incident is raised under R-UNI-39 |

The six identifiers are the legacy identifiers of RWB-E5-003 in their legacy order, with their legacy covers and their legacy data. The legacy level `System` of the first four maps to `End to end` here, because the behaviour they prove crosses the notice, the proof and the case; the access case `-05` keeps the legacy `Access` cover at `Component`, and the forced-failure case `-06` keeps the legacy `Principle 5` cover at `NFR`. The contract half of every surface they touch is tested in `RWB-S4-E5003-CON` and the cross-service journey is not claimed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the period length, the proof window instant, the warning window, the list values and the decision codes are data with a version; no role, list member, state name or date appears in Java.
- No personal data in logs, tests, workflow inputs or prompts: the row carries identifiers, list values and one amount at most, and the borrower's identity never enters this service or its history.
- ACE data only through the owner's contract or the owner's `v_ace_*` views: no component of this story reads an ACE view or an ACE table, and the service identity holds no `v_ace_*` grant (BR4).
- No read of another service's tables and no cross-schema join: the case, the notice, the proof, the approval and the ledger are reached only on their contracts and their fakes (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; a hand-off is re-run with the same signal key and never by a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step with nothing changed (DP-03, R-UNI-39, MSG-P7-003).
- The clock is a durable timer of the workflow and not a Quartz job, a Schedule or a row: the period survives a release and a restart, and no second timer is started for the same notice (12.6, BR8).
- No event, no topic producer, no consumer and no inbox of this service: the delivery result is a workflow signal and the case fact leaves on the case contract (12.3, 12.4).
- The two screens are read only, and every example in the tests and in the fakes is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Screens | Test cases |
|---|---|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2749; ASM-4569) | The notice period starts on proof of delivery and is tracked to its expiry; an unserved notice starts no period; the result is recorded with its rule version | Epics 3 to 8 specification, E5 S4 row; FSD S4 v3 A2.3 | FEAT-LIT-03 | 08 Litigate and enforce | R-LIT-07, R-LIT-08, R-LIT-15, R-LIT-09, R-LIT-12, R-LIT-13, R-LIT-14, R-UNI-31, R-UNI-39, R-UNI-40, BR1 to BR8 | SCR-18, SCR-19 | TC-E5-003-01, TC-E5-003-02, TC-E5-003-03 |
| FEAT-LIT-03 | Run the notice period timer | Business Rules and Routing Logic v4 (R-LIT-07, R-LIT-08, R-LIT-15) | FEAT-LIT-03 | 08 Litigate and enforce | R-LIT-07, R-LIT-08, R-LIT-15 | SCR-18, SCR-19 | TC-E5-003-01 to TC-E5-003-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-003, disposition Split (rework) |
| Legacy criteria | AC1, AC2, AC3 and AC4, owned by this story and copied word for word in section 7 |
| Legacy test cases | TC-E5-003-01 to TC-E5-003-06, kept in legacy order |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so the story traces to FEAT-LIT-03 until the Epics 3 to 8 PRD adds the identifiers (GAP-2749) |
| Contract half | RWB-S4-E5003-CON: the three operations, the notice sub-shape, the timer element, the error envelope, the `Idempotency-Key` rule, the `legal_action` columns and the fakes |
| Sibling slices | RWB-S4-E5002-APP for the proof of delivery, RWB-S4-E5001-APP for the issue of the notices and RWB-S4-E5004-APP for the pack that the expiry opens |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The case of record, its state, its stage clock and the `timer` ledger: rwb-case (P3); this story announces a route fact and accepts the answer.
- The notice, its template, its dispatch and its served result: rwb-comms (P6), and the notice stories of this service (`RWB-S4-E5001-APP`, `RWB-S4-E5002-APP`); the approve operation is provided here as the TSD and the Ownership Map give it, the record is not written here.
- The proof of delivery and its custody in DMS: rwb-document (P5); this story asks for the attach and keeps the reference.
- The approval item, the delegation table and the central ledger: rwb-decision (P7), `RWB-P7-E2013-CON` and `RWB-P7-E2013-APP`; the operation that raises an item is not published there (GAP-2749).
- The three early exits of the period as case moves — payment in full, accepted treatment and dispute: rwb-case (P3), rwb-payment (P8) and rwb-deviation (S8).
- R-LIT-05, R-LIT-09, R-LIT-10 and R-LIT-11, the alternate service, the substituted service and the prescription escalation: the notice stories and the pack stories of this service.
- The pack assembly that R-LIT-15 opens: `RWB-S4-E5004-APP` and rwb-document.
- The contract document itself: `RWB-S4-E5003-CON`.
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, its flag, its dashboards, its alerts and its runbook: its own OPS story.
- The cross-service journey of a notice from dispatch to pack across rwb-comms, rwb-document, rwb-litigation and rwb-case with live owners: the wave 3 integration harness.
