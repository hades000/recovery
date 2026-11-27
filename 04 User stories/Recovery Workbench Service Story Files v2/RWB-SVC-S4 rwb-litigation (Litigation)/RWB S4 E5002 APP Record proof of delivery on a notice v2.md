# RWB-S4-E5002-APP Record proof of delivery on a notice

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S4-C |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5002-APP-16) |
| Depends on (build) | RWB-S4-E5002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version | /v1 path base only; Not specified in the source documents (DOR-RWB-S4-E5002-APP-23) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-002 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the notice and its served result are rwb-comms (P6), the case route state and its timers are rwb-case (P3), and the WIN proof of delivery is read on rwb-source-data's contract because this service holds no `v_ace_*` grant (DP-05); the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before anything changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-18 and SCR-19 read through the gateway-bff composite route (DP-19); the trigger, the record of delivery and the notice-period value have no source specification and are declared as the working read of the assumptions (GAP-2744 to -5; ASM-4564 to -5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 29 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **the Workbench to write the delivery confirmation onto the case, which the notice period timer starts from**, so that **cases reach court faster with complete packs**.

This is the application slice of legacy RWB-E5-002 and it owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the notice-served step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09 on the served result of the notice and on the proof window, with the LITIGATION package version in force;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before anything changes (DP-03);
- the notice-period durable timer, started at `delivered_at` under R-LIT-07 and never started under R-LIT-08 and R-LIT-09;
- the answers to rwb-case for the case move `WITH_CUSTOMER_NOTICE_PERIOD` or `NOTICE_UNSERVED`, for the case-stage timer and for the officer task the unserved rules name;
- the two surfaces SCR-18 Notice approval in its delivered and unserved states and SCR-19 Litigation workspace in its pack state, as this service's answers through the gateway-bff composite route (DP-19).

It does not own: the shape of the consumed facts, the served-result vocabulary, the proof window, the errors and the fakes, which are RWB-S4-E5002-CON; the notice row, its barcode, its `sent_date` and the write of the served result, which are rwb-comms (P6) and its own slice of this legacy key; the case of record, its route state, the parent `CaseWorkflow` and the case-stage timer and task rows, which are rwb-case (P3); the WIN consignment fact and the ACE ingestion that lands it, which are rwb-source-data (P1) and rwb-integration (P2); the proof document, its custody and its retention, which are rwb-document (P5); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-002 closed the gap between dispatch and the statutory clock: a notice went out through WIN, its proof of delivery came back, and the notice period started from the delivery date rather than from an officer's memory. It kept two rule outcomes — R-LIT-07 attached the proof and started the notice period from `delivered_at`, and R-LIT-08 marked the notice unserved inside the 7-day proof window — plus R-LIT-09 for a refused, returned or undeliverable notice. The functional specification keeps the objective and its metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today (FSD S4 A2.2.1).

What D-RCV-60 changes is who owns each fact of the step. In the monolith the notice row, the timer row, the case state and the decision log row sat in one `recovery` schema and one process. In the target:

- **the notice and its served result are rwb-comms (P6).** `notice` (DF-LEG-015 to DF-LEG-023) is P6's row, and Architecture v5 slide 10 gives the "Notices" tab to rwb-comms at one hop. This story reads the notice and its served result on the owner's contract and never writes them;
- **the case route state and the case timers are rwb-case (P3).** `recovery_case`, the route states `NOTICE_DISPATCHED`, `WITH_CUSTOMER_NOTICE_PERIOD` and `NOTICE_UNSERVED`, the case-stage timer and the officer task are P3's; this story answers the move and starts nothing on a case row;
- **the notice-period clock is this service's.** R-LIT-07 belongs to the litigation route set (D7) and runs for months at a time; the notice period is therefore a durable timer of `LitigationWorkflow`, the workflow that "keeps the dates" for litigation (context pack: Temporal and Drools Design slide 7), and not a row of the case service;
- **the decision is recorded first**, in the same transaction as the answer and the timer, which is what legacy AC1 asked for and what legacy AC4 tested;
- **no ACE view is read here.** FEAT-LIT-02 says the step "reads the WIN proof of delivery from `v_ace_pod`, which ACE ingests"; the pack gives rwb-litigation no `v_ace_*` grant and gives the ACE view contract to rwb-source-data, so DP-05 applies as a prohibition and the proof arrives on P1's contract (GAP-2744; ASM-4564).

The step is not carried by an event. The pack gives this service zero events of its own, DP-09 is not in its pattern set, and the `PROOF_OF_DELIVERY_RECEIVED` of the state machine is the name of a workflow signal and not a Kafka subscription (GAP-2745; ASM-4565). The proof window of 7 days is a value in force (Business Rules and Routing Logic v4, R-LIT-08 timer column); the notice period "by product and type" is a routing value whose content no source read for this key gives, so it is read as a versioned reference row (GAP-2746; ASM-4566).

### 3. Preconditions

- RWB-S4-E5002-CON is published: the consumed facts, the served-result vocabulary, the proof window, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The ACE-data read of `v_ace_pod` is available on rwb-source-data's contract with its fake: the WIN proof of delivery of a notice. No P1 operation is named in any source read for this key, so the operation name is Not specified in the source documents (GAP-2744; ASM-4564).
- The rwb-comms notice contract is available with its fake: the notice reference, its case, `sent_date`, the barcode and the served result of the consignment. The operation name is Not specified in the source documents (GAP-2744; ASM-4564).
- The rwb-case contract that reads the case state and answers the move, the case-stage timer and the officer task is available with its fake; the operation name is Not specified in the source documents (GAP-2745; ASM-4565).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-18 and SCR-19 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The LITIGATION rule package is in force at its version with R-LIT-07, R-LIT-08 and R-LIT-09 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce` (GAP-2748; ASM-4568).
- The notice period of each product and notice type is a reference row at its version in force; its content is Not specified in the source documents (GAP-2746; ASM-4566).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_pod`, `rwb_comms.notice` or `rwb_case` is refused by the database and fails the boundary test (DP-05; GAP-2744).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5002-CON when its tests pass.

### 4. Flow

1. rwb-source-data answers the WIN proof of delivery of a notice on its contract, and this service reads no ACE view: the notice or consignment reference, the served result, the delivered-at time and the recipient result, one hop with a 2 s budget and a breaker.
2. The notice-served step of `LitigationWorkflow` on queue `rwb-litigation` receives the fact and reads the notice of the case on the rwb-comms contract: the notice reference, `notice_type`, `sent_date`, the barcode, its case and its status, all of the notice row DF-LEG-015 to DF-LEG-023 (GAP-2744; ASM-4564).
3. The step reads the case route state on the rwb-case contract: the case must be in `NOTICE_DISPATCHED` for R-LIT-07, R-LIT-08 or R-LIT-09 to be evaluated (GAP-2745; ASM-4565).
4. `NoticeDeliveryEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the rule whose condition the fact satisfies: `served_result = delivered` (R-LIT-07), no proof inside the proof window of 7 days (R-LIT-08), or `served_result` in refused, returned or undeliverable (R-LIT-09). The LITIGATION package read is a non-blocking consumed contract of rwb-decision with its fake; the embedded runtime is a service-template capability and no rule row is authored in this story (GAP-2748).
5. The evaluation answers the rule ID, the package version, the action of the rule and the case move the rule names. The meaning of the two unexercised LOV-DELIVERY values and the reference-data contract that serves LOV-DELIVERY are Not specified in the source documents (GAP-1192).
6. `NoticeDeliveryDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the case reference, the notice reference, the rule ID with its version, the inputs reference, the served result, the delivered-at time and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. Under R-LIT-07 the step attaches the proof reference, starts the notice-period durable timer of `LitigationWorkflow` at `delivered_at` with the period of the product and notice type read from reference data, and sets the workflow state to `WITH_CUSTOMER_NOTICE_PERIOD`. Under R-LIT-08 and R-LIT-09 it marks the notice unserved in its own state, starts no timer and sets the state to `NOTICE_UNSERVED`.
8. `CaseAnswer` answers rwb-case in one call: the case move `WITH_CUSTOMER_NOTICE_PERIOD` or `NOTICE_UNSERVED`, the case-stage timer with its start and expiry under R-LIT-07, the officer task under R-LIT-08 and R-LIT-09 because the rule owner is the litigation officer, and the rule ID with its version. rwb-case writes `recovery_case`, its route state and its own timer and task rows; this service writes none of them (GAP-2745; ASM-4565). PROOF_OF_DELIVERY_RECEIVED, PROOF_WINDOW_EXPIRED and DELIVERY_FAILED are workflow signals, not Kafka subscriptions: neither this service nor rwb-case publishes or consumes an event for them.
9. The served result itself is written on the notice by rwb-comms (P6), whose slice of this legacy key owns that row; this story keeps the outcome in its decision record and in the timer, and sends no notice write to P6 (GAP-2744; ASM-4564). This service decides that a notice is due, approves it and owns the notice period; rwb-comms returns the served result, and the notice period starts from the delivered_at it returns (GAP-1740).
10. A repeated fact with the same notice reference and the same delivered-at time writes nothing, starts no second timer and sends no second answer, and the repeat is counted.
11. SCR-18 Notice approval shows the delivered and unserved states and SCR-19 Litigation workspace shows the pack state, both read only through the gateway-bff composite route (DP-19). No access: the refusal MSG-P4-002 of TC-E5-002-05. Empty, loading and error states of SCR-18 and SCR-19 are Not specified in the source documents (DOR-RWB-S4-E5002-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no timer starts, no case move is answered and the notice keeps its state | MSG-P7-003 | AC4, TC-E5-002-04, TC-E5-002-06 |
| X2 | A role without the Litigation right reads the step outcome on a screen | The read is refused at the edge before any service call; nothing changes | MSG-P4-002 | AC5, TC-E5-002-05 |
| X3 | The case is not in `NOTICE_DISPATCHED` for this notice | 409 on the answer; no rule is evaluated, nothing changes and no decision record is written | None | AC2, AC3 |
| X4 | The notice is unknown to rwb-comms or outside the caller's scope | 404 on the read; the step stops and nothing is written | None | AC1, AC2 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered | None | AC1, AC3 |
| X6 | The served result satisfies no rule condition (it is neither delivered nor a failed result, and the proof window has not expired) | No rule fires: nothing changes, no record is written and the case keeps its state | None | AC2, AC3 |
| X7 | The same notice fact arrives twice with the same delivered-at time | One record, one timer and one answer; the repeat is counted | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | The notice period of the product and notice type has no reference row at its version | The proof is attached and the record written; the timer is held, the case is not moved and the step waits on the reference row | None | AC2 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `notice` row, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, TC-E5-002-09, Section 17, BR5 |

X1 to X4 are the exception paths of RWB-E5-002 carried onto the split, X5 to X9 are the paths the target call types add, and X10 is the DP-05 and DP-01 boundary. The 7-day proof window of X6 is a value in force and not a constant of the code.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5002-CON and the fakes of rwb-source-data, rwb-comms, rwb-case and rwb-decision, on its own schema, and needs no live service |
| Negotiable | The activity name, the state names of the step and the shape of the case answer are this story's choice; the rules, the messages, the screens, the served-result vocabulary and the proof window are fixed |
| Valuable | The statutory clock starts on the day the notice was actually served, in one recorded step, and the notice and the case are updated by the services that own them |
| Estimable | One workflow step, one evaluator, one record write, one timer, one answer client and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic notices and consignment results through the contract fakes, plus the component cases of the refused right and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Record proof of delivery on a notice

  Background:
    Given case "RC-2026-000602" carries the demand notice "NTC-2026-000602" dispatched on 2026-12-01 by WIN
    Given the LITIGATION rule package is in force at its version and carries R-LIT-07, R-LIT-08 and R-LIT-09
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record proof of delivery on a notice (legacy RWB-E5-002 AC1)
    Given the rwb-source-data contract mock returns the proof of delivery of notice "NTC-2026-000602" with served_result "delivered" and delivered_at 2026-12-07
    Given the rwb-comms contract mock returns the notice "NTC-2026-000602" of case "RC-2026-000602" sent on 2026-12-01
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the delivery confirmation onto the case, which the notice period timer starts from
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-07 (legacy RWB-E5-002 AC2)
    Given the rwb-case contract mock returns the case state "NOTICE_DISPATCHED" for "RC-2026-000602"
    Given the rwb-source-data contract mock returns the proof of delivery of notice "NTC-2026-000602" with served_result "delivered" and delivered_at 2026-12-07
    Given a case in state NOTICE_DISPATCHED
    When proof of delivery received
    Then attach the proof and start the notice period from delivered_at
    Then the case moves to WITH_CUSTOMER_NOTICE_PERIOD

  Scenario: AC3 Rule R-LIT-08 (legacy RWB-E5-002 AC3)
    Given the rwb-case contract mock returns the case state "NOTICE_DISPATCHED" for "RC-2026-000602"
    Given the rwb-source-data contract mock returns no proof of delivery for notice "NTC-2026-000602" inside the proof window of 7 days
    Given a case in state NOTICE_DISPATCHED
    When proof window expired
    Then mark the notice unserved; the notice period does not start
    Then the case moves to NOTICE_UNSERVED

  Scenario: AC4 Not recorded (legacy RWB-E5-002 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Access refused (X2) (new, D-RCV-60)
    Given a role without the Litigation right
    When the role reads the step outcome on SCR-18 or SCR-19
    Then the read is refused at the edge before any service call and the user sees MSG-P4-002
    Then nothing changes

  Scenario: AC6 Boundary of the owned schema (X10) (new, D-RCV-60)
    Given a component, a statement or a test that reads a `v_ace_*` view or writes a `notice` row
    When the boundary test runs
    Then the grant refuses the statement and the build fails
    Then nothing is released

  Scenario: AC7 Repeated notice fact (X7, BR6) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the proof of delivery of notice "NTC-2026-000602" with served_result "delivered" and delivered_at 2026-12-07
    Given the same notice fact has already been recorded once for case "RC-2026-000602"
    When the same notice fact arrives again with the same delivered_at
    Then one record, one timer and one answer exist
    Then the repeat is counted

  Scenario: AC8 No personal data (BR8) (new, D-RCV-60)
    Given the decision record and the workflow input of the step
    When they are inspected
    Then they carry case and notice references, codes, dates and a rule version only
    Then no person name, address, contact value or identity number is present

  Scenario: AC9 Rule R-LIT-09 (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the proof of delivery of notice "NTC-2026-000602" with served_result "refused"
    Given the rwb-case contract mock returns the case state "NOTICE_DISPATCHED" for "RC-2026-000602"
    When delivery failed
    Then record the result and queue an alternate service method
    Then the case moves to NOTICE_UNSERVED

  Scenario: AC10 Disallowed transition refused (X3) (new, D-RCV-60)
    Given the rwb-case contract mock returns the case state "WITH_CUSTOMER_NOTICE_PERIOD" for "RC-2026-000602"
    Given the rwb-source-data contract mock returns the proof of delivery of notice "NTC-2026-000602" with served_result "delivered" and delivered_at 2026-12-07
    When proof of delivery received
    Then the answer is refused with 409 and nothing changes
    Then no decision record is written

  Scenario: AC11 Retried or timed-out call (X5) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer the proof of delivery of notice "NTC-2026-000602" inside 2 s
    Given the rwb-case contract mock returns the case state "NOTICE_DISPATCHED" for "RC-2026-000602"
    When the step calls the proof of delivery
    Then the step waits and retries on the workflow's own schedule
    Then nothing is written and no case move is answered

  Scenario: AC12 Failed consumed call (X5) (new, D-RCV-60)
    Given the rwb-comms contract mock fails the call for notice "NTC-2026-000602" of case "RC-2026-000602"
    When the step reads the notice
    Then the step waits and retries on the workflow's own schedule
    Then nothing is written and no case move is answered
```

AC1 to AC4 are the legacy criteria of RWB-E5-002 with their origin tag added: the repetition of `Then`, the legacy wording of `the action is taken` and `its trigger arrives` all stand, and `the decision log` reads `the decision record` (DP-03). AC5 to AC12 are owned by this story, carry no legacy tag and cover X2, X10, X7, BR8, R-LIT-09, X3 and X5. The cross-service parts are mocked, so AC1 to AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions. What the legacy lines describe happens in three places in the target: rwb-source-data answers the WIN proof, rwb-comms holds the notice and its served result, and this story evaluates the rule, writes the record, starts the timer and answers the case move that rwb-case writes.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-07 | Litigation | D7 | NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | served_result = delivered | Attach the proof and start the notice period from delivered_at | WITH_CUSTOMER_NOTICE_PERIOD | Customer | WIN and DMS, Workbench | Notice period by product and type |
| R-LIT-08 | Litigation | D7 | NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | no proof returned inside the proof window | Mark the notice unserved; the notice period does not start | NOTICE_UNSERVED | Litigation officer | WIN and DMS | 7 days |
| R-LIT-09 | Litigation | D7 | NOTICE_DISPATCHED | DELIVERY_FAILED | served_result in (refused, returned, undeliverable) | Record the result and queue an alternate service method | NOTICE_UNSERVED | Litigation officer | WIN and DMS | 2 working days |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business: the `Customer` owner of R-LIT-07 is the party the notice is served on and the `Litigation officer` owner of R-LIT-08 and R-LIT-09 is the role that receives the task when the notice is unserved. The systems column maps to the target as follows: WIN is rwb-comms and the ACE ingestion of rwb-source-data, DMS is rwb-document (P5), and Workbench is this service and the screens.

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice-served step of the litigation journey is this service's: the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09, the notice-period timer and the decision record are `rwb_litigation` objects and workflow state, and no other service evaluates them | Architecture v5 slide 41 (rwb-litigation owns litigation, hearings, judgments, enforcement, LED auction ladder); context pack ownership rows (workflow `LitigationWorkflow`, queue `rwb-litigation`); FSD S4 A2.2.3.1 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-002 AC1 and AC4 |
| BR3 | The notice row, its barcode, its `sent_date` and its served result stay with rwb-comms (P6); this story reads them on the owner's contract and writes none of them; the proof of delivery stays with the notice in rwb-comms, reaches this service on rwb-source-data's contract and is matched to the notice by barcode (GAP-1597) | Context pack (ownership rows of S4 name `hearing` and `legal_action` only); Architecture v5 slide 10 ("Notices — rwb-comms"); GAP-2744 |
| BR4 | The case move, the case route states `NOTICE_DISPATCHED`, `WITH_CUSTOMER_NOTICE_PERIOD` and `NOTICE_UNSERVED`, the case-stage timer and the officer task stay with rwb-case (P3); this story answers them and writes no case row | Context pack (workflow ownership and the case of record); TSD S4 T5.2 ("P3 for the case"); GAP-2745 |
| BR5 | No ACE view and no ACE table is read or written here, and no cross-schema join is made: the proof arrives on rwb-source-data's contract and the notice on rwb-comms' | DP-05; context pack (ACE data only through the owner's contract or `v_ace_*` views; this service holds no `v_ace_*` grant) |
| BR6 | The same notice fact twice writes once, starts one timer, answers once and counts the repeat | TSD S4 T-A.2 (idempotency rule of the write paths); Architecture v5 slide 11 |
| BR7 | The served-result vocabulary is closed — delivered, refused, returned, undeliverable — and the proof window is 7 days; neither is a constant of the code | Business Rules and Routing Logic v4 (R-LIT-07, R-LIT-08, R-LIT-09); context pack slide 7 notes ("the proof window is 7 days"); BR-S4-002 (FSD S4 A2.2.3.1) |
| BR8 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case and notice references, codes, dates and a rule version | Template and Rules v1 §R7.2 (s17); FSD S4 A2.2 field catalogue |

| Rule ID | Covered by |
|---|---|
| BR1 | AC1, TC-E5-002-01 |
| BR2 | AC4, TC-E5-002-04, TC-E5-002-06 |
| BR3 | AC6, TC-E5-002-09 |
| BR4 | AC2, AC3, TC-E5-002-02, TC-E5-002-03 |
| BR5 | AC6, TC-E5-002-09 |
| BR6 | AC7, TC-E5-002-10 |
| BR7 | AC2, AC3, TC-E5-002-02, TC-E5-002-03 |
| BR8 | AC8, TC-E5-002-11 |

**Where each rule lives in the target.** R-LIT-07 attaches the proof, starts the notice-period timer at `delivered_at` and asks for `WITH_CUSTOMER_NOTICE_PERIOD`. R-LIT-08 and R-LIT-09 record the served result, start no timer and ask for `NOTICE_UNSERVED`, and R-LIT-09 additionally queues the alternate service method on the case as the task request of section 4, step 8. VR-S4-002-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no ACE batch status read, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here (GAP-2744; ASM-4564).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4).

| From (case route state) | Event | Condition | To (answered, written by rwb-case) |
|---|---|---|---|
| NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED under R-LIT-07 | served_result = delivered | `WITH_CUSTOMER_NOTICE_PERIOD`, with the notice-period timer started at `delivered_at` |
| NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED under R-LIT-08 | no proof returned inside the proof window | `NOTICE_UNSERVED`, with the officer task and no timer |
| NOTICE_DISPATCHED | DELIVERY_FAILED under R-LIT-09 | served_result in (refused, returned, undeliverable) | `NOTICE_UNSERVED`, with the officer task and the alternate service request |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The proof of delivery of the notice answers on the P1 contract | The notice and the case state are read | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The timer is set under R-LIT-07, or the unserved state is set | The case answer is accepted | Waiting for the next fact |
| Applying | The record write, the timer or the answer fails | X1, X5, X9 | Waiting, nothing changed |

No column of this service changes in this story: the step has no business row, and its durable state is the workflow state and the timer. The notice status of rwb-comms and the case route state of rwb-case are read or answered, never written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record, sets the timer and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix and the also-user of the FSD feature: reads the outcome on SCR-18 and SCR-19, and receives the task the unserved rules name |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the notice outcome of the case in scope |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Litigation RA: read the notice outcome and the decision record |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU as TSD S4 T6.1 gives it: no part of this step is taken by a firm user |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it; the service identities run the step and are subject to the same checks |

The FSD declares the feature "runs unattended" with the litigation officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the R-LIT-07 path, and the litigation officer is the role of the task that R-LIT-08 and R-LIT-09 raise. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation on the contract, and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | Read only, on the P6 contract: the notice reference, its case, `notice_type`, `sent_date` and the barcode; the served result is part of the same answer; never written, joined or stored here |
| DF-WRK-027 to DF-WRK-036 | timer (P3, `rwb_case`) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read and not written as a table: the notice-period clock is a durable timer of `LitigationWorkflow`, and the case-stage timer is answered to rwb-case |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Read as the case route state on the answer, and never written |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | id, rule_id, rule_version, route_set and 11 more | Read as the LITIGATION package in force, never written |
| DF-LEG-001 to DF-LEG-014 | legal_action (S4, `rwb_litigation`) | the 14 action fields | Not written by this story: the action of the case is the sibling stories' |
| No published field ID for the WIN proof | the WIN proof of delivery (rwb-source-data, ACE ingestion) | the WIN consignment fact | Read only on the rwb-source-data contract and never written; the element is Not specified in the source documents (GAP-2744; ASM-4564) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1 and the legacy data table of RWB-E5-002. **No new table, no new column and no migration**: this story writes no business row, `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` is a platform library object created in `rwb_litigation` by the library's own migration (DP-03). `notice` (P6), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5) and every `v_ace_*` view (P1) are not created, not written and not read as tables.

**No personal data.** The rows and the record carry identifiers, dates, list values and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input; the fixture of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. This step is an unattended workflow step and publishes no operation of its own. The five operations of rwb-litigation (API-S4-001 to API-S4-005, TSD S4 T-A.1) belong to the notice approval, the legal action and the hearing stories of this service: API-S4-001 `POST /notices/{noticeId}/approve` is the dispatch approval that precedes this step, and API-S4-002 to API-S4-005 are the legal-action operations of the sibling stories. Declaring a delivery operation here would add a sixth operation to the ownership rows of this service, which name five (GAP-2744; ASM-4564). This service writes no business row; its durable effects are the decision record, the workflow state and the notice-period timer, and the proof and notice reads are the placeholder operations of rwb-source-data and rwb-comms (GAP-2744).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The ACE-data read of `v_ace_pod` (operation name Not specified in the source documents (GAP-2744; ASM-4564)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The WIN proof of delivery of the notice: the notice or consignment reference, the served result, the delivered-at time and the recipient result; faked |
| The notice read (operation name Not specified in the source documents (GAP-2744; ASM-4564)) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice of the case with its `notice_type`, `sent_date`, barcode, case and served result; faked |
| The case read (operation name Not specified in the source documents (GAP-2745; ASM-4565)) | `/api/recovery/case/v1` | P3 rwb-case | The case route state `NOTICE_DISPATCHED` that gates the three rules; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2745; ASM-4565)) | rwb-case (P3) | P3 rwb-case | The case move `WITH_CUSTOMER_NOTICE_PERIOD` or `NOTICE_UNSERVED`, the case-stage timer and the officer task, with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2748; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-07, R-LIT-08 and R-LIT-09; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All five rows are contract dependencies of class C in fact that this story's metadata row does not carry, because the plan's C row is None; the two platform rows of the pattern set (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are its only H rows beside its own contract (GAP-2744, GAP-2745, GAP-2748; ASM-4564, ASM-4565, ASM-4568).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. DP-09 is not in this story's pattern set, so it writes no outbox row and widens no topic; the only record it relays is the local decision record on the shared `rwb.decision-record.v1` of DP-03, which is the library's topic and not an event of this service (GAP-2745; ASM-4565).

#### 12.4 Events consumed

None. The `PROOF_OF_DELIVERY_RECEIVED` of the state machine and EV-15 of the Temporal design are the names of the fact that starts R-LIT-07, not a Kafka subscription: this service has no consumer group, no subscription and no inbox of its own. The proof therefore arrives on the P1 contract of 12.2, synchronously, and the case state on the rwb-case read (GAP-2745; ASM-4565).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4 and the notice; signals: the proof of delivery, the case state answered by rwb-case, the rule package in force; the notice-period durable timer |
| `recordNoticeDelivery` | Activity, the one notice-served step of this story | `rwb-litigation` | The notice and the proof in; the rule ID with its package version, the served result, the timer fact and the case move out, with the decision record written in the same transaction |

The activity name and the workflow state names are target design choices of this story and are fixed by no source document; the trigger of the step is read as the arrival of a proof-of-delivery fact for a notice whose case is in `NOTICE_DISPATCHED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2745; ASM-4565). The workflow run of the dispatch belongs to the notice story, and no run record of Architecture v5 is owned or registered here. LitigationWorkflow ID form: Not specified in the source documents (CG-ALL-9020). Catalog start rule: 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'; duplicate-start policy: Not specified in the source documents (CG-ALL-9020).

#### 12.6 Schedules

None. The notice-period clock is a durable timer of `LitigationWorkflow` started at `delivered_at` under R-LIT-07, and the proof window of 7 days is a durable timer of the same workflow started at dispatch under R-LIT-08. No Temporal Schedule, no Quartz row and no shared job table is declared, and no batch window is read or set by this story (GAP-2746; ASM-4566).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row; this story writes none of its columns |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by this story |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated fact |

Not owned and never read as a table: `notice` (P6), `recovery_case`, `timer` and `task` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data pod fake | The proof of delivery of notice `NTC-2026-000602` with `served_result` delivered and `delivered_at` 2026-12-07; a refused, a returned and an undeliverable result; no proof inside the proof window; no answer beyond 2 s | AC1, AC2, AC3, X5, X6 |
| rwb-comms notice fake | The demand notice `NTC-2026-000602` of case `RC-2026-000602` sent on 2026-12-01 with its barcode and its served result; an unknown notice | AC1, AC2, AC3, X4 |
| rwb-case fake | The case state `NOTICE_DISPATCHED` and a case in another state; the moves `WITH_CUSTOMER_NOTICE_PERIOD` and `NOTICE_UNSERVED` accepted, and a move refused | AC1, AC2, AC3, X3 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-07, R-LIT-08 and R-LIT-09, and a package at a second version | AC1, AC2, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 answer for case `RC-2026-000602`, with the notice facts of this service read once | AC1, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the five consumed rows and the rwb-source-data answer element are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2744, GAP-2745, GAP-2748; ASM-4564, ASM-4565, ASM-4568).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The pod read, the notice read, the case read, the case-stage answer and the rule package read; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity, 2 durable timers | `LitigationWorkflow`, `recordNoticeDelivery`, the notice-period timer and the proof window; no Schedule |
| File | None | The WIN file is ingested by ACE and read on the P1 contract; no file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `notice`, Java package `th.co.scb.ace.workbench.recovery.litigation.notice`; front end `src/modules/recovery/litigation/NoticeDelivery.tsx`, the fragment SCR-18 and SCR-19 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the proof arrives on rwb-source-data's contract (GAP-2744; ASM-4564). DP-03 is the transaction rule of the step: the record, the timer and the case answer commit together or not at all. DP-13 is the base of this service's five operations, none of which this story provides. DP-19 is how SCR-18 and SCR-19 reach this service, one hop through the gateway.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries. The five consumed contracts are class C in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-2744, GAP-2745, GAP-2748).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` notice branch | Workflow | The stage of the journey that waits for the proof, holds the notice-period timer and the proof window, and reports the outcome to the parent |
| `recordNoticeDelivery` | Activity | The one step: read the notice and the case state, read the proof, evaluate R-LIT-07, R-LIT-08 or R-LIT-09, write the record, set the timer and answer the case |
| `NoticeDeliveryEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the served-result vocabulary and the proof window |
| `NoticeDeliveryDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before anything changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `NoticeTimer` | Workflow timer | Starts the notice-period timer at `delivered_at` under R-LIT-07 and never starts it under R-LIT-08 and R-LIT-09 |
| `PodFactClient` | Client | The `v_ace_pod` read on the P1 contract, one hop, 2 s, breaker, no retry of its own |
| `NoticeFactClient` | Client | The notice and served-result read on the P6 contract, one hop, 2 s, breaker |
| `CaseAnswer` | Client and signal reporter | The case read and the case-stage answer to rwb-case; it reports, it never changes a case row |
| `NoticeDelivery` | React component | Shows the delivered and unserved states on SCR-18 and the pack state on SCR-19, read only, with the refusal and failure states |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). This story writes no business row, so no column is added for `served_result`, `delivered_at` or the notice period: those are facts of the consumed answer, of the record and of the timer, and storing them would copy two other services' facts into this schema (GAP-2744, GAP-2746).

**Configuration and reference data.**

- The served-result vocabulary and the proof window of 7 days, read as reference data with a version and never as constants (BR7).
- The notice period per product and notice type, read as a versioned reference row; its content is Not specified in the source documents (GAP-2746; ASM-4566).
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- The parameters the step reads are the proof window of 7 days (BR7) and the notice period per product and notice type; their parameter keys are Not specified in the source documents (DOR-RWB-S4-E5002-APP-20). The reference-data contract is the rwb-decision read of the LITIGATION package (DP-06, DP-07); the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The notice branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the proof as its trigger (GAP-2745; ASM-4565).
2. `PodFactClient` and `NoticeFactClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X4, X5).
3. `NoticeDeliveryEvaluator` over the LITIGATION package, with the three rules, the vocabulary, the proof window and the no-fire path (AC1, AC2, AC3, X6).
4. `NoticeDeliveryDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `NoticeTimer` and the reference read of the notice period, with the missing-reference path (AC2, X9).
6. `CaseAnswer` with the move, the case-stage timer and the officer task (AC2, AC3, X3).
7. `NoticeDelivery` and the two screens through the composite route fake (AC1, AC3).
8. The boundary test: no statement outside the service's own schema, no `v_ace_*` read, no write to any other owner's schema (X10, BR3, BR5).

**Feature flag.** `rwb.litigation.notice-delivery-v1`, read as a flag of the platform library; off means the step holds the proof and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic proof in SIT, each of the three rules produces its record, its timer state and its move, a repeated fact writes once, a forced record failure changes nothing, no `notice` row and no `recovery_case` row is written from this service, and SCR-18 and SCR-19 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the fact or of the answer is absent or invalid (X6 of the contract) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads the step outcome (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-002-1 (FSD S4 A2.2.3.1). This service holds no ACE batch status read, so the check is the owner's and the message is carried here (GAP-2744; ASM-4564) | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-002 section 14 and of the FSD S4 A2.2 message list. MSG-P1-001 is aligned to the wording of FSD P1 v3 VR-P1-001-1 ({product} is from {date}. Today's ACE batch has not arrived.), which replaces 'load' with 'ACE batch'; no other message is reworded and no new message is added. The Thai wording, the field-level text of MSG-GEN-001 and the approver are left to the message work of DL10 (GAP-1748). `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5), a notice that is not found (X4) and a case in the wrong state (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it evaluates, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-18 Notice approval | Generated | The notice generated for the case, read only, owned by the notice story |
| SCR-18 Notice approval | Approved | The dispatch approval of API-S4-001, read only |
| SCR-18 Notice approval | Sent | `sent_date` of the notice on the P6 answer, read only |
| SCR-18 Notice approval | Delivered | The served result, the `delivered_at` time, the proof reference and the notice-period timer started under R-LIT-07 |
| SCR-18 Notice approval | Unserved | The served result or the expired proof window, and the reason the notice period did not start, under R-LIT-08 or R-LIT-09 |
| SCR-19 Litigation workspace | Pack | The step outcome next to the legal action of the case, read only |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9027) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9027) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9027) |
| SCR-19 Litigation workspace | No access | A role without the Litigation right: MSG-P4-002 and nothing changes (X2) |
| SCR-18 Notice approval | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-18 Notice approval | Stale data | The message MSG-P1-001 shown where the owner reports the stale data product of the source |
| SCR-18 Notice approval | Timer held | The notice period reference row of the product and notice type is missing, and the timer waits (X9) |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-9026) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-9026) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-9026) |
| SCR-18 Notice approval | No access | Same as Refused: MSG-P4-002 and nothing changes (X2) |

The route merges the answer of this service with rwb-comms for the notice and rwb-case for the case and its route state; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The two state lists are the legacy lists of RWB-E5-002 ("generated; approved; sent; delivered; unserved" and "pack; instructed; filed; hearing; judgment") with the refusal, failure and timer-held states this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-002-01 | AC1 | End to end | Record proof of delivery on a notice |
| TC-E5-002-02 | AC2 | End to end | Rule R-LIT-07 |
| TC-E5-002-03 | AC3 | End to end | Rule R-LIT-08 |
| TC-E5-002-04 | AC4 | Component | Not recorded |
| TC-E5-002-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-002-06 | Principle 5 | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-002-07 | Section 12 operations, events and activities | Contract | Contract test of the operations, events and activities of section 12 against the published contract |
| TC-E5-002-08 | Section 12.7 tables | Boundary | Boundary test: no statement reads or writes a table outside section 12.7 |
| TC-E5-002-09 | AC6 | Boundary | A component, a statement or a test reaches a `v_ace_*` view or a `notice` row; the grant refuses it and the build fails |
| TC-E5-002-10 | AC7 | Component | A repeated notice fact writes once, starts one timer, answers once and counts the repeat |
| TC-E5-002-11 | AC8 | Component | The decision record and the workflow input carry no person name, address, contact value or identity number |
| TC-E5-002-12 | AC9 | Component | Rule R-LIT-09: the failed delivery is recorded, the alternate service method is queued and the case moves to NOTICE_UNSERVED |
| TC-E5-002-13 | AC10 | Component | A case not in NOTICE_DISPATCHED receives a proof: the answer is refused with 409, nothing changes and no decision record is written (X3) |
| TC-E5-002-14 | AC5 | Component | A role without the Litigation right reads the step outcome: refused with MSG-P4-002 and nothing changes (X2) |
| TC-E5-002-15 | AC11 | Component | A consumed call that does not answer inside 2 s is retried on the workflow's own schedule; nothing is written and no case move is answered (X5) |
| TC-E5-002-16 | AC12 | Component | A consumed call that fails is retried on the workflow's own schedule; nothing is written and no case move is answered (X5) |

The six legacy test case IDs are kept in order and their Covers are kept; the Data of TC-E5-002-06 reads `decision record` where the legacy wording read `decision log`, and TC-E5-002-07 to -16 are added by this story. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3, the "System" level of the legacy story) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The fakes and the stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000602`, notice `NTC-2026-000602`, dispatch on 2026-12-01, delivery on 2026-12-07 and the 7-day proof window — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the served-result vocabulary, the 7-day proof window, the notice period per product and notice type and the message texts are values and reference rows with a version; no list value, state name, day count or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the step carries references, dates, codes and a rule version only, and the test data is synthetic.
- The notice stays with rwb-comms: no `notice` row, no served result and no barcode is written here (BR3; DP-01).
- The case stays with rwb-case: no `recovery_case` row, no route state, no case-stage timer row and no task row is written here, and the move is answered with the rule and its version (BR4).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant (DP-05).
- No read of another service's tables and no cross-schema join: `notice`, `recovery_case`, `timer`, `rule_row`, `decision_log_entry` and `document` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second answer.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing, consumes nothing and registers no job, and the catalogue of the service is not widened (12.3, 12.4, 12.6).
- The two screens are read only; SCR-18 posts nothing and its approval action is API-S4-001 of the notice story.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed, which this story does by starting the notice period on the proof of delivery and marking the notice unserved when the proof does not come (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID (GAP-2747; ASM-4567) | FEAT-LIT-02 | 08 Litigate and enforce | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E5-002-01, TC-E5-002-02, TC-E5-002-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-002 | The four legacy criteria word for word, the three rules, the two screens, the messages and the six test cases; the `notice`, `timer` and `recovery_case` writes of the legacy data table are retired to their owners |
| RWB-S4-E5002-CON | H: the consumed facts, the served-result vocabulary, the proof window, the errors and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-18 and SCR-19 |
| rwb-source-data (P1), rwb-comms (P6), rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the proof, the notice, the case read and answer, and the rule package, all faked (GAP-2744, GAP-2745, GAP-2748) |
| RWB-S4-E5002-APP and RWB-S4-E5002-CON siblings of this key | The application and contract halves of the same legacy key |
| FEAT-LIT-02, SCR-18, SCR-19 | The feature and the two screens of the legacy story |
| DP-03, DP-05, DP-13, DP-19 | The decision record, the ACE prohibition, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, Temporal with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-source-data, rwb-comms and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the consumed facts, the served-result vocabulary, the proof window, the errors and the fakes: RWB-S4-E5002-CON.
- The notice row, its barcode, its `sent_date`, the served result and the notice document: rwb-comms (P6) and rwb-document (P5), and the rwb-comms slice of this legacy key. **The notice is written by rwb-comms, and this story evaluates the rule, records the decision, starts the timer and answers the case move** (GAP-2744; ASM-4564).
- The case of record, its route state `WITH_CUSTOMER_NOTICE_PERIOD` or `NOTICE_UNSERVED`, the parent `CaseWorkflow`, the case-stage timer and the officer task: rwb-case (P3) and its slice of this legacy key (GAP-2745; ASM-4565).
- The WIN consignment, its file and its ACE ingestion, and the read of `v_ace_pod`: rwb-integration (P2) and rwb-source-data (P1).
- The generation, the template and the dispatch of the notice: FEAT-LIT-01 of this module, and API-S4-001 `POST /notices/{noticeId}/approve` of the notice story.
- The running and the expiry of the notice period after it starts, and the wake-up that opens pack assembly under R-LIT-15: FEAT-LIT-03 of this module, the sibling story of this key family.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-07, R-LIT-08 and R-LIT-09: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-2748; ASM-4568).
- The notice period value per product and notice type: the reference-data owner of rwb-case and the business owner of S4; the story reads the row and carries the placeholder (GAP-2746; ASM-4566).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-18 and SCR-19: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
