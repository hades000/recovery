# RWB-S5-E3022-APP Serve the statutory notice and prove delivery

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-E |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement. Not specified in the source documents (DOR-RWB-S5-E3022-APP-16) |
| Depends on (build) | RWB-S5-E3022-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version | v1; delivery state comes from rwb-comms GET /api/recovery/comms/v1/notices/{noticeId} (API-P6-002) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-007, RD-P1-041, RD-P1-064 |

**Version 3 changes.**

- D-RCV-60 P1 developer readiness (RD-P1 register). Routed the asset delivery check through the rwb-comms notice read and removed the asset caller of the P1 proof endpoint. Backfilled 3 mapped v9 test case IDs. RD-P1-064.
- Version 3 aligns the notice delivery dependency and the proof scenarios to the owner contracts.
- RD-P1-007: the read writes nothing, and only `rwb-comms` appends delivery entries; this step appends none (finding 3). `data_as_of` is not the freshness stamp (finding 4).
- AC9 and AC10 added for the stale and closed-flag answers (finding 5).
- Resolved the asset caller question through the rwb-comms notice read (RD-P1-064 rule 6).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-022 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag. The notice step becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset`: it requests the statutory sale notice on the rwb-comms contract (API-P6-001), reads the notice delivery state from rwb-comms, which owns access to the P1 read over `v_ace_pod`, evaluates R-DIS-04 and R-DIS-05 with the DISPOSAL package version in force, records the decision through the local decision-record library before any change (DP-03) and answers rwb-case with the hold, the failed notice task and the re-serve move. The notice row is rwb-comms' (`rwb_comms`), the proof is rwb-source-data's, the task and the case state are rwb-case's, and this service holds none of the three (`GAP-2852`, `GAP-2854`; `ASM-4720`, `ASM-4721`, `ASM-4724`). The base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to serve the notice the repossession requires, prove its delivery and hold the take-on until the notice is served**, so that **a vehicle is not sold on a notice the bank cannot prove it served, and the bank meets the hire-purchase notice duty without a manual chase of the WIN call-back**.

This is the application slice of legacy RWB-E3-022. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and roles they depend on;
- one step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slides 19 and 41; Temporal and Drools Design slide 13);
- the request of the statutory sale notice on rwb-comms (`POST /cases/{caseId}/notices`, API-P6-001) and the read of its state (`GET /notices/{noticeId}`, API-P6-002), one hop each;
- the notice delivery state on GET /api/recovery/comms/v1/notices/{noticeId}; the asset step makes no ledger append (RD-P1-064);
- the evaluation of R-DIS-04 and R-DIS-05 with the DISPOSAL package version in force, and the hold, the re-serve and the two case moves they name;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before anything changes (DP-03);
- the request of the failed notice task, its two-working-day due date and the human task of the re-serve, all on the workflow kit and on the rwb-case answer.

It does not own: the published shape of the notice request and read, the notice element, the proof row, the stage answer, the failed notice task element, the error set and the fakes, which are RWB-S5-E3022-CON; the notice row, its template, its dispatch and its WIN call-back, which are rwb-comms (P6); the ACE proof-of-delivery view and the WIN file, which are rwb-source-data (P1) and rwb-integration (P2); the case of record, its route states `ASSET_PENDING_TAKE_ON` and `FAILED_NOTICE_QUEUE`, the `task` row and the parent `CaseWorkflow`, which are rwb-case (P3); the asset record itself, which the take-on stories of this service write; the rule rows and the DISPOSAL package, which rwb-decision (P7) authors and approves; and the deployment of this build, which is the operations story of this legacy key and the wave 2 harness.

### 2. Business rationale

Legacy RWB-E3-022 gave the Workbench one step that sent the notice the repossession requires and recorded the proof. The FSD keeps the objective and the metric unchanged: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and moves from 1,486 days to a target of 1,095 days (FSD S5 A2.4.1). The regulatory anchor is REG-20: give the hirer notice before terminating the contract and repossessing, and notify the hirer and the guarantor before the vehicle is sold (Regulatory Requirements Map v3). The rule the bank already applies is REQ-OCC-006 with NFR-044: a customer who withdraws consent stops receiving on that channel, and statutory notices continue.

What D-RCV-60 changes is who owns the notice, the proof and the case.

- **The notice is rwb-comms' (P6).** `notice` is P6's table in `rwb_comms`, with DF-LEG-015 to DF-LEG-023, `LOV-NOTICE`, `LOV-DELIVERY` and `LOV-SENT-TYPE`; the context pack gives S5 two tables, `asset_sale` and `listing`, and no notice row (`GAP-2852`; `ASM-4720`). This story requests the notice and reads its state on the P6 contract, and copies no notice field into `rwb_asset`.
- **rwb-comms provides the notice and its delivery state.** rwb-source-data owns the WIN proof view and serves the proof endpoint only to rwb-comms. The asset step reads the notice contract (RD-P1-064; GAP-2854; ASM-4724).
- **The case, its route state and the failed notice task are rwb-case's (P3).** R-DIS-04 names the move to `FAILED_NOTICE_QUEUE` and opens a task; the `task` row and the route state are P3's, so this story answers the move and requests the task with its rule and its version (`GAP-2852`; `ASM-4721`).
- **The decision is recorded first**, through the local decision-record library of DP-03 in one transaction with any local write, which is what legacy AC1 asks for and legacy AC4 tests.
- **No event is published.** The service's catalogue event is EV-22 `AssetTakenOn` on `rwb.asset.events.v1`, published by the take-on stories; a notice hold is a case move and a decision record, not an asset event, so this story publishes nothing and consumes nothing (`GAP-2853`; `ASM-4723`).
- **The WIN dispatch file is not this service's call.** The registered-mail file to WIN is built and sent by rwb-comms' dispatch loop through the rwb-integration adapter (DP-16), and the FSD's "Integration points: WIN" line is satisfied there, not by a file call from rwb-asset (`GAP-2854`).

No business value moves: the notice type, the delivery-status vocabulary, the two-working-day target of R-DIS-04 and the hold reasons are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S5-E3022-CON is published: the notice request and read rows, the notice element, the proof row, the failed notice task element, the stage answer, the error set and the fakes are baselined and handed to this story.
- The rwb-comms contract of DP06-comparable notice generation is published with its fake: `POST /cases/{caseId}/notices` (API-P6-001) and `GET /notices/{noticeId}` (API-P6-002) on `/api/recovery/comms/v1`, with the notice type, the sent date, the barcode and the delivery status. The row is not in this story's contract-dependency list, which is None.
- rwb-comms publishes GET /api/recovery/comms/v1/notices/{noticeId} with a fake. The notice read returns the dispatch and proof-of-delivery fields. Only rwb-comms calls the P1 proof endpoint and appends delivery entries (RD-P1-064 rule 6).
- The case state read and the case-move answer of rwb-case are available for the fake, with the route states `ASSET_PENDING_TAKE_ON` and `FAILED_NOTICE_QUEUE`. No source names a published operation that creates a task or moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent applies, and the failed notice task is requested on it with its due date (`GAP-2854`; `ASM-4721`).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision record is written in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service and rwb-comms through the gateway-bff composite route, one hop each (DP-19).
- The DISPOSAL rule package is in force at its version with R-DIS-04 and R-DIS-05; the package is authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`. The two-working-day target, the notice types and the delivery-status vocabulary are values of that package and of reference data.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema, no `v_ace_pod` grant and no `v_ace_contact` grant, so a statement on either view or on `rwb_case` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline; the baseline is tagged by RWB-S5-E3022-CON when its tests pass.

### 4. Flow

1. The repossession route of a vehicle reaches the take-on of rwb-asset, and the repossession requires the statutory sale notice to be served before the asset is sold (FSD S5 A2.4.1 and A2.4.2; REG-20).
2. The notice step of `AssetDisposalWorkflow` on queue `rwb-asset` receives the trigger for a case in `ASSET_PENDING_TAKE_ON` and reads the case state and the case reference on the rwb-case contract, read only, one hop with a 2 s budget.
3. `NoticeRequestClient` requests the statutory sale notice on rwb-comms: `POST /cases/{caseId}/notices` with the case reference, the notice type of `LOV-NOTICE` that the DISPOSAL package names for the route, the addressee role and the `Idempotency-Key`. P6 generates the notice with its template, references the document of P5, hands the letter to the WIN dispatch loop through the rwb-integration adapter and answers `noticeId`, the sent date, the barcode and the dispatch state.
4. ProofOfDeliveryClient reads GET /api/recovery/comms/v1/notices/{noticeId} for the notice being evaluated, one hop with a 2 s timeout. It evaluates the notice’s delivery state and proof fields. A notice without proven delivery cannot pass the take-on proof check. The read writes nothing (RD-P1-064 rule 6).
5. `NoticeServingEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-04 (`delivery_status` does not prove delivery) and R-DIS-05 (`new_address_confirmed = Y` on a case in `FAILED_NOTICE_QUEUE`) on the fact. Where neither rule fires, nothing changes and the step reports the notice state to the parent.
6. `NoticeDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the `noticeId`, the barcode, the delivery status, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. **Delivery proved.** The step answers the parent that the notice is proved, with the `noticeId`, the barcode and the `callback_date`; no route state changes, and the take-on continues on its own rules in RWB-S5-E3019-APP, RWB-S5-E3020-APP or RWB-S5-E3021-APP.
8. **Delivery not proved (R-DIS-04).** The step holds the take-on and writes nothing, answers rwb-case with the move `FAILED_NOTICE_QUEUE` and requests the failed notice task with its rule, its version and its due date two working days ahead, read as a reference value. rwb-case writes the `recovery_case` row, the route state and the `task` row.
9. The parent starts the failed notice human task of the workflow kit on `rwb-asset`; the sale officer confirms a new address and re-issues. The address is recorded in the rwb-comms contact repository and is never copied here; the step carries the confirmed contact key and the confirmation flag (`GAP-2852`; `ASM-4724`).
10. **Re-serve (R-DIS-05).** On `NOTICE_REISSUED` with `new_address_confirmed = Y` the step requests a second statutory notice on rwb-comms with the confirmed contact key, reads the fresh proof of delivery and answers rwb-case with the move `ASSET_PENDING_TAKE_ON`; the take-on resumes and the asset record is opened by the take-on story on its own rules.
11. A repeated proof row, a repeated `noticeId` or the same `Idempotency-Key` writes nothing, answers no second move and counts the repeat; the step is safe to retry after a workflow replay.
12. SCR-21 Asset list and SCR-22 Asset record read the asset and its holding status from this service and the notice and its delivery status from rwb-comms through the gateway-bff composite route; this step fixes no screen state of its own (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing and no case move and no task request leaves the service | MSG-P7-003 | AC4, TC-E3-022-04, TC-E3-022-06 |
| X2 | The role does not hold the Asset and disposal right of the failed notice task | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E3-022-05 |
| X3 | The case is not in `ASSET_PENDING_TAKE_ON` or `FAILED_NOTICE_QUEUE` as the rule expects | 409 and nothing is written; a rule is never applied to a case that has already moved | None | AC2, AC3 |
| X4 | The notice read has no delivery fact for this notice | The step holds until there is a delivery answer. It requests no failed-notice task and writes no proof result | None | AC9, AC10 |
| X5 | rwb-comms, rwb-source-data or rwb-case does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the screen sees 503 with the platform envelope | None | AC1, AC3, AC6, TC-E3-022-14 |
| X6 | rwb-comms refuses the notice request (a template withdrawn, a contact stop, a closed service) | No proof is awaited and no move is answered; the step reports the refusal and the reason to the parent | None | AC1, X1, AC7, TC-E3-022-15 |
| X7 | The proof row or the notice is already recorded for the case and the barcode | One decision record, one move and one task request; the repeat is counted | None | AC1, AC3 |
| X8 | A build, a statement or a test reaches `v_ace_pod`, `v_ace_contact`, the `notice` table or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E3-022-09, Section 17, BR3, BR5 |

X1 to X3 are the exception paths of RWB-E3-022 carried onto the split, X4 to X7 are the paths the target call types add, and X8 is the DP-05 and DP-01 boundary. The two-working-day target and the notice types are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3022-CON and the rwb-comms, rwb-case and decision-record fakes, on its own schema; needs no live P1, P3, P6 or P7 |
| Negotiable | The activity name, the element names of the stage answer and the decision code per rule are this story's choice; the rules, the messages, the notice operations, the proof read and the state names are fixed |
| Valuable | No asset is sold on an unproved notice, the failed notice is a task a person can act on, and the re-serve returns the case to the take-on without a manual chase of WIN |
| Estimable | One workflow step, one evaluator, one record write, two client groups, one task request, two case moves and no screen of its own |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic notices and proof rows through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Serve the statutory notice and prove delivery

  Background:
    Given case "RC-2026-000622" is on the repossession route with asset "AST-2026-000622"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-04 and R-DIS-05
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Serve the statutory notice and prove delivery (legacy RWB-E3-022 AC1)
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000622"
    Given the rwb-comms contract mock returns the statutory sale notice "N-000622" for "RC-2026-000622" with barcode "RR123456789TH" and sent date 2026-11-20
    Given the rwb-comms contract mock answers GET /notices/{noticeId} for this notice with delivery status "DELIVERED" and proof dated 2026-11-23
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the notice the repossession requires and records the proof
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-04 (legacy RWB-E3-022 AC2)
    Given the rwb-comms contract mock answers GET /notices/{noticeId} for this notice with delivery status "UNDELIVERABLE" and delivery_proved "N"
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000622"
    Given a case in state ASSET_PENDING_TAKE_ON
    When statutory notice failed
    Then hold the take-on, raise a failed notice task and re-serve on a confirmed address
    Then the case moves to FAILED_NOTICE_QUEUE

  Scenario: AC3 Rule R-DIS-05 (legacy RWB-E3-022 AC3)
    Given the rwb-case contract mock returns the case state "FAILED_NOTICE_QUEUE" for "RC-2026-000622"
    Given the rwb-comms contract mock returns the re-issued statutory sale notice "N-000623" for the confirmed address of "RC-2026-000622"
    Given a case in state FAILED_NOTICE_QUEUE
    When notice reissued
    Then re-serve the statutory notice and resume the take-on
    Then the case moves to ASSET_PENDING_TAKE_ON

  Scenario: AC4 Not recorded (legacy RWB-E3-022 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 No ACE read and no foreign statement (X8, DP-05; added for X8, not legacy) (new, D-RCV-60)
    Given a build contains a statement that reads `v_ace_pod`, `v_ace_contact`, the `notice` table or a table of another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC6 Activity retried or timed out (X5, ADR-020; added for X5, not legacy) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer within 2 s for "RC-2026-000622"
    When the serveStatutoryNotice activity runs
    Then nothing is written, no move is answered and the activity is retried on the workflow's own schedule

  Scenario: AC7 Consumed call fails (X6; added for X6, not legacy) (new, D-RCV-60)
    Given the rwb-comms contract mock refuses the notice request for "RC-2026-000622" with a template withdrawn
    When the notice request is sent
    Then no proof is awaited, no move is answered and the refusal and its reason are reported to the parent

  Scenario: AC8 Disallowed status change refused (added for NEWAC-RWB-S5-E3022-APP-AC9, not legacy) (new, D-RCV-60)
    Given the rwb-case contract mock returns a case state that does not allow the requested status change for "RC-2026-000622"
    When a status change the model does not allow is requested
    Then the change is refused, nothing is written and no move is answered

  Scenario: AC9 A notice waiting for proof does not advance take-on (RD-P1-064)
    Given case "RC-2026-000622" is at "ASSET_PENDING_TAKE_ON" with notice "N-000622" and barcode "RR123456789TH"
    Given the rwb-comms contract mock answers the notice read without a delivery fact
    When the notice step evaluates the proof
    Then no move is answered, no failed notice task is requested and no decision record of a proof result is written
    Then the step stays in "Held, until a fresh answer"
    Then the step makes no direct P1 proof read and no ledger write

  Scenario: AC10 A delivery fact must belong to the notice being evaluated (RD-P1-064)
    Given the rwb-comms notice mock has a delivered fact only for a different notice
    When the notice step evaluates the proof
    Then no move is answered, no failed notice task is requested and nothing is held or proved on the answer
    Then the step makes no direct P1 proof read and no ledger write
```

The four criteria are the legacy criteria of RWB-E3-022 word for word, with their origin tag added and nothing else changed except the decision-log wording, now `decision record` (CG-ALL-9709): the repetition of `Then`, the legacy wording of `the action is taken`, `the decision record cannot be written` (CG-ALL-9709), `its trigger arrives`, `statutory notice failed` and `notice reissued` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target: rwb-comms generates, dispatches and holds the notice; rwb-comms provides the notice delivery state; this story evaluates R-DIS-04 or R-DIS-05, writes the decision record and answers the hold, the task and the move; and rwb-case writes the case state and the `task` row. Three notes are recorded rather than smoothed over. The legacy story's screens are SCR-21 and SCR-22, which carry no notice state, so the notice and its proof are read from rwb-comms through the same composite route and this step adds no screen state (`GAP-2852`). The legacy Data table names `v_ace_contact` and the `notice` table, and neither is this service's to read or write in the target (`GAP-2852`; `ASM-4720`, `ASM-4724`). The trigger is not named by any source, so the step starts from the take-on fact of the case and from the re-issue signal the parent forwards (`GAP-2854`; `ASM-4722`).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-04 (BR10) | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | STATUTORY_NOTICE_FAILED | delivery_proved = N | Hold the take-on, raise a failed notice task and re-serve on a confirmed address | FAILED_NOTICE_QUEUE | Sale officer | WIN and DMS, Document Hub | 2 working days |
| R-DIS-05 (BR11) | Asset disposal | D8.1 to D8.3 | FAILED_NOTICE_QUEUE | NOTICE_REISSUED | new_address_confirmed = Y | Re-serve the statutory notice and resume the take-on | ASSET_PENDING_TAKE_ON | Workbench | WIN and DMS, Document Hub | None |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves to `FAILED_NOTICE_QUEUE` and back to `ASSET_PENDING_TAKE_ON` are written by rwb-case on this story's answer, the notice is generated, dispatched and re-issued by rwb-comms, the notice delivery read is rwb-comms’, and the failed notice task is created by rwb-case. The timer column of R-DIS-04 is the due date this story puts on the task request; the rule's own wait is a durable timer of `AssetDisposalWorkflow` (`GAP-2852`; `ASM-4721`).

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice is rwb-comms' and is referenced, never copied: this story carries `noticeId` and the barcode, declares no `notice` column and writes no notice row | TSD S5 T5.2 (P6 for notices); TSD P6 T3.1 and T3.2; `GAP-2852`; `ASM-4720` |
| BR2 | The decision is recorded before any change, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2; legacy RWB-E3-022 AC1 and AC4 |
| BR3 | Notice delivery comes from rwb-comms (RD-P1-064). This story reads no `v_ace_pod`, no `v_ace_contact` and no ACE table, and uses the rwb-comms notice read | DP-05; Architecture v5 slides 29, 37 and 45; `GAP-2854` |
| BR4 | The case move is answered and not written: `recovery_case`, the route states and the `task` row are rwb-case's, and this story sends the move, the task request and the two-working-day due date with the rule and its version | Ownership Map (recovery_case and task owner P3); Architecture v5 slide 41; `GAP-2852` |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id`, the contact key and the notice reference are identifiers of other services' facts | DP-01; TSD S5 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: `LOV-NOTICE`, `LOV-DELIVERY`, `LOV-SENT-TYPE`, the hold reasons and the two-working-day target | TSD P6 T3.2; FSD S5 BR-S5-004; legacy Guardrails |
| BR7 | The notice is requested once per serving and once more per re-issue, with an `Idempotency-Key`; a repeated proof row or key writes once, moves once and requests one task | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR8 | No person name, address, contact value or identity number enters `rwb_asset`, a decision record, a log or a workflow input: the proof row and the notice reference carry identifiers, codes and dates only | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |
| BR9 | No event is published or consumed by this step: EV-22 `AssetTakenOn` belongs to the take-on stories, and a build that adds a topic, a consumer or a Schedule fails the absence test | Architecture v5 slide 19; `GAP-2853`; `ASM-4723` |

Coverage of the rules, by criterion or test case: BR1 AC1 and TC-E3-022-08; BR2 AC1, AC4, TC-E3-022-04 and TC-E3-022-06; BR3 AC5 and TC-E3-022-08; BR4 AC2 and AC3; BR5 AC5 and TC-E3-022-08; BR6 TC-E3-022-10; BR7 AC1, AC3 and TC-E3-022-11; BR8 TC-E3-022-12; BR9 TC-E3-022-13; R-DIS-04 (BR10) AC2; R-DIS-05 (BR11) AC3.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the notice-serving state of its step and the decision it records.

| From (case route state, answered by this story) | Event | Condition | To |
|---|---|---|---|
| ASSET_PENDING_TAKE_ON | The proof of delivery proves service | delivery_proved = Y | Unchanged, the notice is proved and the take-on continues |
| ASSET_PENDING_TAKE_ON | The proof of delivery does not prove service | delivery_proved = N (R-DIS-04) | `FAILED_NOTICE_QUEUE`, with the failed notice task requested |
| FAILED_NOTICE_QUEUE | A confirmed address is recorded and the notice re-issued | new_address_confirmed = Y (R-DIS-05) | `ASSET_PENDING_TAKE_ON`, the take-on resumed |
| Any other state | Any notice fact of the case | X3 | Unchanged, 409 and nothing written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The take-on fact arrives for a case in `ASSET_PENDING_TAKE_ON` | The package in force is loaded | Requesting the notice |
| Requesting the notice | rwb-comms answers the notice | A `noticeId` and a barcode are returned | Awaiting the proof |
| Awaiting the proof | The proof row of the business date is read | The gate is complete and the row matches the notice | Evaluating |
| Evaluating | A rule fires | The decision record is written | Applying |
| Applying | The move, the task request and the record commit | The transaction commits | Waiting for the next fact |
| Applying | The record write or a consumed call fails | X1, X5, X6 | Waiting, nothing changed |
| Awaiting the proof | The data product is stale or the gate is closed | X4 | Held, until a fresh answer |

The route states `ASSET_PENDING_TAKE_ON` and `FAILED_NOTICE_QUEUE` are those of the DISPOSAL machine of TSD S5 T4 and of the legacy criteria, and they live on the case of record. The step states are the workflow's own and no row records them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the primary role of the legacy story, acting on the failed notice task to confirm an address and re-issue |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the notice state of a case and confirms the re-serve |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the notice state before the take-on of a repossessed vehicle |
| RW-HEADNPA, RW-HEADASL, RW-PRODHEAD | Asset and disposal R or RA: read the notice state and the hold where a route needs approval |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal RU or R as the TSD S5 T6.1 matrix gives it: the partner sees its own assets, never the notice decision |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step under the same checks |
| rwb-asset service identity | Runs the step, requests the notice, reads the proof, evaluates the rules, writes the decision record and answers the move and the task; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and nothing wider. The FSD declares the feature as "None; runs unattended" for the primary actor with the sale officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the sale officer is the primary actor on the failed notice task and on the re-serve. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6, `rwb_comms`) | id | Not written: read as the `noticeId` reference of the decision record and the answer |
| DF-LEG-016 | notice (P6) | case_id | Not written: the case reference is sent on the request and the answer |
| DF-LEG-017 | notice (P6) | document_id | Not written and not read: the document reference is P6's and P5's |
| DF-LEG-018 | notice (P6) | notice_type | Not written: the type of `LOV-NOTICE` is named on the request |
| DF-LEG-019 | notice (P6) | sent_date | Read on the notice answer, carried on the decision record |
| DF-LEG-020 | notice (P6) | barcode | Read on the notice answer, carried on the decision record and used to match the proof row |
| DF-LEG-021 | notice (P6) | callback_date | Read from the proof row, carried on the decision record |
| DF-LEG-022 | notice (P6) | delivery_status | Read from the proof row against `LOV-DELIVERY`, the fact R-DIS-04 tests |
| DF-LEG-023 | notice (P6) | sent_type | Read from the proof row against `LOV-SENT-TYPE` |
| DF-ACE-251 to DF-ACE-260 | `v_ace_pod` (P1) | pod_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system, data_as_of | Not read: this service holds no `v_ace_pod` grant; the facts arrive on the P1 read (BR3) |
| `v_ace_contact` (P1) | contact_key, contact_type, person_key, contact_value, usage_code | Not read: the address is the rwb-comms contact repository's, and the step carries only the confirmed contact key |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code | Not read as a table: the state arrives on the rwb-case answer |
| DF-WRK-017 to DF-WRK-026 | task (P3) | task_code, status, due date | Not written: the failed notice task is requested on the case answer |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything changes |

Field IDs are those of the Logical Data Model and Data Dictionary v9, and the notice and ACE rows are the rows the legacy story lists in its Data table, with their owners changed to P6 and P1 by the target. **No new table, no new column and no migration**: this story writes no business table at all, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_asset` by the library's own migration (`GAP-2852`; `ASM-4720`). The notice reference (`noticeId`, barcode, delivery status and callback date) is carried on the decision record and on the stage answer; whether any notice reference is persisted in `rwb_asset` is decided in step D1 (`GAP-2852`).

**No personal data.** The rows this story handles carry identifiers, codes and dates. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic. The confirmed address stays in the rwb-comms contact repository and is referenced by its contact key only.

### 12. Contract

#### 12.1 REST operations provided

None. This legacy key owns no REST operation: the Ownership Map gives rwb-asset six operations, `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`, and none of them is a notice operation. The two operations the legacy story lists are named in 12.2 and 12.8 as other keys' or other services': `GET monolith-base/assets/{assetId}` is API-S5-002, declared by RWB-S5-E3019-CON on `/api/recovery/asset/v1` (DP-13), and `POST monolith-base/assets/{assetId}/valuations` is API-S5-003, which belongs to rwb-valuation under the Ownership Map ruling ASM-0043 (`GAP-2853`; `ASM-4722`).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `POST /cases/{caseId}/notices` (API-P6-001) | `/api/recovery/comms/v1` | P6 rwb-comms | Requests the statutory sale notice of the case with its type of `LOV-NOTICE`, the addressee role and the `Idempotency-Key`; answers `noticeId`, the sent date, the barcode and the dispatch state; faked |
| `GET /notices/{noticeId}` (API-P6-002) | `/api/recovery/comms/v1` | P6 rwb-comms | Reads the notice, its dispatch fields and its proof-of-delivery fields; faked |

| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference the notice request carries; read only, faked |
| The case-move answer with the failed notice task request (operation name Not specified in the source documents (`GAP-2854`; `ASM-4721`)) | rwb-case (P3) | P3 rwb-case | The move `FAILED_NOTICE_QUEUE` or `ASSET_PENDING_TAKE_ON` with the rule ID and its version, and the failed notice task with its due date; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None; the absence is recorded as `GAP-2853` and `GAP-2854` with `ASM-4722`.

#### 12.3 Events published

None. The service's catalogue event is EV-22 `AssetTakenOn` on `rwb.asset.events.v1` (Architecture v5 slide 19 OUT and slide 43 row 22), published by the take-on stories of this service; a notice hold, a re-serve and a status read change no asset, so this story publishes nothing. A build that adds an event, a topic or a second producer fails the absence test (`GAP-2853`; `ASM-4723`).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is a notice fact, a proof of delivery or a case state; the step starts from the take-on fact of the case and from the re-issue signal the parent forwards. This story therefore holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | Input: the case, the route and the rule package in force; signals: the case state answered by rwb-case, the rule package in force, the re-issue answer of the failed notice task and the dispatch answer of rwb-comms |
| `serveStatutoryNotice` | Activity, the one notice step of this story | `rwb-asset` | The case and the notice fact in; the `noticeId`, the barcode, the delivery status, the rule ID with its package version, the case move and the task request out, with the decision record written in one transaction |
| `FailedNoticeTask` | Human task of the workflow kit with an SLA | `rwb-asset` | The task request of the case move answer: the case, the notice reference, the reason and the two-working-day due date |

No child workflow for the case and none for the notice exists in this service; the notice is a request to rwb-comms and not a workflow of its own. The activity name and the task name are target design choices and are fixed by no source document.

Workflow ID form: Not specified in the source documents (CG-ALL-9702). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9702).

#### 12.6 Schedules

None. The step runs from the take-on fact and from the re-issue signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP (Architecture v5 slide 44; context pack jobs JOB-19). No other Job of slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

None of this story's own, beyond the platform library objects.

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the notice decision (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated proof row and the answer it holds |

Not owned and never read as a table: `notice` (P6), `recovery_case` and `task` (P3), `document` (P5), `asset` and `asset_sale` and `listing` (S5, the take-on, sale and pricing stories'), `decision_log_entry` and `rule_row` (P7), and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01, DP-05).

Personal data: the personal-data class of each field this story reads from rwb-comms and rwb-source-data is the class Data Classification v5 gives it; where that document gives none, it is Not specified in the source documents (DOR-RWB-S5-E3022-APP-11).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | The statutory sale notice `N-000622` for case `RC-2026-000622` with barcode `RR123456789TH` and sent date 2026-11-20; the re-issued notice `N-000623` for a confirmed address; a request refused for a withdrawn template; no answer beyond 2 s | AC1, AC3, X5, X6 |
| rwb-comms notice delivery fake | A delivered notice, an undeliverable notice, a notice without a delivery fact, and a different notice with a delivered fact | AC1, AC2, AC9, AC10, X4 |
| rwb-case case-state fake | The states `ASSET_PENDING_TAKE_ON` and `FAILED_NOTICE_QUEUE` of case `RC-2026-000622`; a case in another state | AC1, AC2, AC3, X3 |
| rwb-case move and task fake | The move `FAILED_NOTICE_QUEUE` accepted with the task created and dated; the move `ASSET_PENDING_TAKE_ON` accepted; a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-04 and R-DIS-05 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000622`, with the asset read once from this service and the notice read from rwb-comms | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the case-move answer and of the task request is stubbed from the published documents and carries the placeholder until its owner confirms it (`GAP-2854`; `ASM-4721`).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-comms notice request and read, the rwb-case state read and the case-move answer with the task request; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record goes on the library's `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 activity and 1 human task | `AssetDisposalWorkflow`, `serveStatutoryNotice` and `FailedNoticeTask` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here; the WIN registered-mail file is rwb-comms' through the rwb-integration adapter (DP-16) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `notice`, Java package `th.co.scb.ace.workbench.recovery.asset.notice`; no front-end module, because this step adds no screen state and the notice is shown by rwb-comms through the composite route.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_pod` and no `v_ace_contact` grant, reads no ACE view and no ACE table, and the notice delivery state comes from rwb-comms (`GAP-2854`; `ASM-4724`). DP-03 is the transaction rule of the step: the record and the answer commit together or not at all. DP-13 moves the base of the reads the legacy story names and nothing else. DP-19 is how SCR-21 and SCR-22 reach this service and rwb-comms, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as `GAP-2853` and `GAP-2854`. The outbox and inbox library of DP-09 is not needed, because this step publishes and consumes nothing (`ASM-4723`). The two legacy REST operations are not owned by this key: API-S5-002 (GET /api/recovery/v1/assets/{assetId}) is declared by RWB-S5-E3019-CON and API-S5-003 (POST /api/recovery/v1/assets/{assetId}/valuations) is assigned to rwb-valuation (ASM-A6-api-6), so this key owns no notice operation; the four consumed rows stay class C dependencies, and step D1 decides whether they become C dependencies of this key (`GAP-2853`).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` notice branch | Workflow | The step of the journey that waits for the take-on fact or the re-issue signal, loads the package in force and reports the outcome to the parent |
| `serveStatutoryNotice` | Activity | The one step: read the case, request the notice, read the proof, evaluate R-DIS-04 or R-DIS-05, write the record, answer the move and the task |
| `NoticeRequestClient` | Client | `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` of rwb-comms, one hop, 2 s, breaker, `Idempotency-Key` |
| ProofOfDeliveryClient | Client | GET /api/recovery/comms/v1/notices/{noticeId} for the notice’s delivery state, read only, one hop, 2 s |
| `NoticeServingEvaluator` | Service | The rule evaluation over the DISPOSAL package in force, with the delivery-status and notice-type lists |
| `NoticeDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, and refuses the step when the write fails (DP-03) |
| `CaseMoveAnswer` | Client | The case state read, the move and the failed notice task request of rwb-case, one hop, 2 s |
| `FailedNoticeTask` | Workflow kit task | The human task with its SLA, carrying the case, the notice reference, the reason and the due date |

**Database and migrations.** No Flyway file. This story writes no business table; the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). Schema ownership: `rwb_asset` is this service's; `rwb_case` is owned by rwb-case (recovery_case and task, P3) and `rwb_comms` by rwb-comms (notice, P6); the owner of `rwb_decision` is not named in the source documents, and this story writes none of the three.

**Configuration and reference data.**

- `LOV-NOTICE`, `LOV-DELIVERY` and `LOV-SENT-TYPE` at their version in force (TSD P6 T3.2), read as reference data and never as constants.
- The DISPOSAL package and its version, loaded on `RulePackageInForce`; the two-working-day target and the hold reasons are values of the package and of reference data.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- Parameters: the two-working-day target and the hold reasons, read from the DISPOSAL package and reference data under the reference-data contract of DP-06 and DP-07; the 2 s budget and the single hop are the platform rule of ADR-020. Parameter keys in parameter-catalog.csv: Not specified in the source documents (DOR-RWB-S5-E3022-APP-20).

**Build steps**

1. The notice branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`.
2. `NoticeRequestClient` against the rwb-comms fake, with the `Idempotency-Key`, the refusal path and the no-answer path (AC1, X5, X6).
3. `ProofOfDeliveryClient` against the rwb-comms fake, with delivery, undeliverable, no proof and timeout answers (AC1, X4, X5).
4. `NoticeServingEvaluator` over the DISPOSAL package, with R-DIS-04 and R-DIS-05 and the no-fire path (AC1, AC2, AC3).
5. `NoticeDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `CaseMoveAnswer` with the two moves and the failed notice task request with its due date (AC2, AC3, X3).
7. `FailedNoticeTask` with its SLA and the confirmed contact key of the rwb-comms contact repository (AC3).
8. The idempotency and repeat path (AC1, AC3, X7).
9. The boundary test: no statement outside `rwb_asset`, no `v_ace_pod` and no `v_ace_contact` read, no write to `rwb_case`, `rwb_comms` or `rwb_decision` (X8, BR3, BR5).

**Feature flag.** `rwb.asset.notice-serving-v1`, read as a flag of the platform library; off means the step holds the fact, writes nothing and answers no move, and the take-on stories keep their own path.

**Done when.** The tests of section 16 pass, the step requests a notice and reads a proof against the fakes, each of the two rules produces its record, its move and its task, a repeated proof row answers once, a forced record failure changes nothing, no `notice` and no `v_ace_*` read exists in the build, and SCR-21 and SCR-22 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of the notice request or of a request body is absent or invalid (X3, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right acts on the failed notice task (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the notice answer (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |


The six message IDs are those of the legacy message set and of FSD S5 A2.4.3.1, and their text is from the legacy and FSD wording. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them.

### 15. Screens and states

The legacy story names SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states, all served through the gateway-bff composite route (DP-19). Neither screen carries a notice state: the composite route calls this service for the asset and its holding status, rwb-case for the case and its route state, rwb-comms for the notice and its delivery status, rwb-source-data for the ACE asset fact and rwb-valuation for the valuation references, and this story fixes no screen field. The empty, error and no-access states of SCR-21 are Not specified in the source documents (CG-ALL-9710), and the empty, loading, error and no-access states of SCR-22 are Not specified in the source documents (CG-ALL-9711).

The states this story produces are on the case and in the workflow, not on a screen: the case in `FAILED_NOTICE_QUEUE` with its failed notice task, the task in its open, confirmed and closed states, and the hold on the take-on. The officer's work is the failed notice task of rwb-case's worklist, where MSG-P4-002 and MSG-GEN-001 are shown by the owner of that screen. The composite route specification and the screen field list belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-022-01 | AC1 | Component | Case `RC-2026-000622` at `ASSET_PENDING_TAKE_ON`; the notice request, the delivered proof for `RR123456789TH` from the rwb-comms notice delivery fake (§12.8), the decision record and the proved answer asserted on the fakes |
| TC-E3-022-02 | AC2 | Component | The `UNDELIVERABLE` proof for `RR123456789TH` from the rwb-comms notice delivery fake (§12.8); the hold, the `FAILED_NOTICE_QUEUE` move and the failed notice task with its due date asserted |
| TC-E3-022-03 | AC3 | Integration | Case `RC-2026-000622` at `FAILED_NOTICE_QUEUE` with a confirmed address; the re-issued notice `N-000623`, the fresh proof from the rwb-comms notice delivery fake (§12.8) and the `ASSET_PENDING_TAKE_ON` move asserted end to end on the fakes |
| TC-E3-022-04 | AC4 | Component | The decision-record stub stopped; nothing written, no move answered and MSG-P7-003 shown |
| TC-E3-022-05 | Access | Component | A role without the Asset and disposal right on the failed notice task; 403 with MSG-P4-002 and no read |
| TC-E3-022-06 | Principle 5 | Component | A forced decision record write failure at the moment of the notice answer; no record, no move and no task |
| TC-E3-022-07 | Contract (§12.5, §12.7) | Contract | The operations, events and activities of §12 driven against the rwb-comms, rwb-case contract fakes (§12.8); each request and answer matches the contract |
| TC-E3-022-08 | Boundary (§12.7, ASM-3438) | Component | The tables of §12.7 with only `decision_record` and `idempotency_key` written in `rwb_asset`; no read of the not-owned objects of §12.7 and no `v_ace_*` view |
| TC-E3-022-09 | Boundary (AC5, X8, DP-05) | Component | A build or statement that reads `v_ace_pod`, `v_ace_contact`, the `notice` table or another service's schema fails the boundary test and nothing is released |
| TC-E3-022-10 | Reference data (BR6) | Component | The step reads `LOV-NOTICE`, `LOV-DELIVERY`, `LOV-SENT-TYPE` and the rule package at their version in force and holds no constant of them |
| TC-E3-022-11 | Idempotency (BR7, X7) | Component | A repeated proof row or `Idempotency-Key` writes one decision record, moves once and requests one task |
| TC-E3-022-12 | Privacy (BR8) | Component | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input |
| TC-E3-022-13 | Absence (BR9) | Component | The build adds no event topic, consumer or Schedule for this step |
| TC-E3-022-14 | AC6 | Component | An rwb-case call with no answer inside 2 s; nothing written, no move answered and the retry on the workflow's own schedule asserted; the proposed test is Not specified in the source documents (NEWAC-RWB-S5-E3022-APP-AC7) |
| TC-E3-022-15 | AC7 | Component | An rwb-comms refusal of the notice request with a withdrawn template; no proof awaited, no move answered and the refusal and its reason reported to the parent asserted; the proposed test is Not specified in the source documents (NEWAC-RWB-S5-E3022-APP-AC8) |
| TC-E3-022-16 | AC8 | Component | A case state that does not allow the requested status change; the refused change, nothing written and no move answered asserted; the proposed test is Not specified in the source documents (NEWAC-RWB-S5-E3022-APP-AC9) |
| TC-S5-E3022-APP-01 | AC9 | Component | Notice awaiting delivery, with no case move or failed-notice task. |
| TC-S5-E3022-APP-02 | AC10 | Component | Delivery recorded for a different notice does not prove the notice under evaluation. |

The six legacy cases are the legacy cases of RWB-E3-022 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes, and TC-E3-022-03 maps to `Integration` because it crosses the rwb-comms and rwb-source-data boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness and are not owned here.

### 17. Guardrails

- No business value in code: the notice types, the delivery statuses, the hold reasons, the two-working-day target and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a decision record, in a workflow input or in a log: identifiers, codes and dates only, the address stays in the rwb-comms contact repository, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_pod` and no `v_ace_contact` grant, and a build that adds one fails the boundary test (DP-05).
- The notice stays with rwb-comms, the case and its task with rwb-case, the delivery state with rwb-comms and the record of the decision with rwb-decision: this story writes none of their rows (BR1, BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no second producer on `rwb.asset.events.v1`.
- The decision is recorded before the answer leaves the service; a build that answers a move before the record commits fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this feature, decided at step D1 (GAP-2854) | The TSD S5 T8 map carries REQ-S5-001 to REQ-S5-005 for FEAT-AST-01 and REQ-S5-006 to REQ-S5-010 for FEAT-AST-08, and none of them covers FEAT-AST-04; the regression anchor is REG-20, and REQ-OCC-006 with NFR-044 (statutory notices continue) is the constraint that holds it (`GAP-2854`; `ASM-4725`) | The notice step, the proof read, the hold, the task and the re-serve | TC-E3-022-01, TC-E3-022-02, TC-E3-022-03 |
| REQ-OCC-006 | A customer who withdraws consent for a channel stops receiving on that channel, and statutory notices continue (Business Requirements Program v5; NFR-044) | The statutory notice is requested on its own path and is not suppressed by a channel preference | TC-E3-022-01, TC-E3-022-02 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the step, with the notice, the proof and the case with their owners | TC-E3-022-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login, with no grant on another schema | TC-E3-022-06, TC-E3-022-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E3-022-03, TC-E3-022-07 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the answer | TC-E3-022-04, TC-E3-022-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-022, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-022-01 to TC-E3-022-16 |
| Feature and screens | FEAT-AST-04; SCR-21 Asset list and SCR-22 Asset record as the legacy feature names them, with no notice state added; empty and error states of SCR-21 and empty, loading and error states of SCR-22: Not specified in the source documents (DOR-RWB-S5-E3022-APP-10); the no-access states of both are Not specified in the source documents (DOR-RWB-S5-E3022-APP-10), and TC-E3-022-05 asserts 403 with MSG-P4-002 on a role without the right |
| L3 process | Not specified in the source documents (DOR-RWB-S5-E3022-APP-2) |
| Rules | R-DIS-04 and R-DIS-05, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the notice rows, the stage answer, the failed notice task element, the error set and the fakes: RWB-S5-E3022-CON.
- The notice row, its template, its generation, its dispatch, the WIN registered-mail file and the WIN call-back: rwb-comms (P6) and, for the file, rwb-integration (P2) under DP-16.
- The ACE proof-of-delivery view, the `v_ace_batch_status` gate and the contact views: rwb-source-data (P1) (`GAP-2854`).
- The case of record, its route states, the failed notice task row, the worklist and the parent `CaseWorkflow`: rwb-case (P3), whose state and answer this story consumes and fakes.
- The asset record and the take-on routes of R-DIS-01, R-DIS-02 and R-DIS-03: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP, which write the `asset` row from their own facts.
- The notice document, its custody and its retention: rwb-document (P5) and, for the templates, rwb-comms.
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-04 and R-DIS-05: rwb-decision (P7).
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

### 20. Remaining delivery steps

- Size the story at refinement (squad).



- RWB-S5-E3022-CON Done with its fakes published (rwb-asset contract owner).
- Add the AC1, AC9 and AC10 test case rows to Test Cases v9 and the RTM (test lead).
- Load the test data in DEV and SIT (test lead).
