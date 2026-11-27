# RWB-S6-E5026-APP Open the buyer data room

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-D |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S6-E5026-APP-16) |
| Contract version | Not specified in the source documents (DOR-RWB-S6-E5026-APP-23); the path base is /api/recovery/debtsale/v1 (DP-13) |
| Depends on (build) | RWB-S6-E5026-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-document (masked tape, class C; read as a reference on the rwb-document contract, while building, masking, rejection and rebuild stay with RWB-S6-E5025-APP, the PII service and the rwb-access masking policy; tape object and field list unpublished, GAP-1960, GAP-1976), rwb-partner (buyer panel, class C), rwb-case (case state and move, class C); built against their published contracts and fakes on Day 1; operation names Not specified in the source documents (DOR-RWB-S6-E5026-APP-9; GAP-1958; GAP-2977; GAP-2978 baseline placeholders confirmed before tag) |
| Integration dependencies | Partner gateway buyer channel, an edge dependency with no plan row (GAP-2977); the partner gateway fronts rwb-partner and is the route of API-S6-004 declared as one Partner portal operation of rwb-debtsale, operation name Not specified in the source documents (GAP-1959) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (REQ-S6-003 and FEAT-DBS-04 adopted for traceability) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the data-room slice of RWB-E5-026 split out for rwb-debtsale. The two legacy criteria are kept word for word with their origin tag; the target keeps them as one step of `DebtSaleWorkflow` on queue `rwb-debtsale` that opens the room on the masked tape of the tape step (R-DS-13), reads the admitted buyer panel on the rwb-partner contract, answers the case move to rwb-case and serves API-S6-004 on base `/api/recovery/debtsale/v1` (DP-13) behind the partner channel and the gateway-bff composite route (DP-19), with the outcome recorded through the local decision-record library (DP-03). The plan's C row for this key is None although the step consumes three other services, the partner channel and the lot status of the opening have no source, and the tape belongs to RWB-S6-E5025-APP (GAP-2977; ASM-4899 to -7). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E5026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 24 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **the Workbench to publish the lot and the masked tape to the data room for qualified buyers**, so that **debt sales run on approved lots and masked data, instead of on spreadsheets, and the 45-day debt sale turnaround is measured on the decision log and the Workbench records**.

This is the data-room slice of legacy RWB-E5-026. It owns:

- the two legacy criteria, copied verbatim with their origin tag, and the rules, messages and screen they rest on;
- one step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, the stage child of `CaseWorkflow` owned by rwb-case (context pack, Temporal and Drools slides 12 and 13; Architecture v5 slide 19);
- the evaluation of R-DS-13 on the tape the tape step prepared, and the reading of the tape branch R-DS-10, R-DS-11 and R-DS-12 that RWB-S6-E5025-APP runs;
- the read of the lot and its accounts from `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale` (DF-SAL-020 to DF-SAL-037), and the read of the tape and its masking-check result on the rwb-document contract;
- the read of the admitted buyer panel of the lot on the rwb-partner contract, which is who "qualified buyers" are under R-DS-13;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before anything is served (DP-03);
- the answer to rwb-case for the case move `DATA_ROOM_OPEN`, with the rule ID and the version that produced it;
- the read API-S6-004 `GET /partner/data-room/{lotId}` on base `/api/recovery/debtsale/v1`, on the partner channel through the partner gateway and on the staff channel through the gateway-bff composite route (DP-13, DP-19), serving PRT-05 Data room.

It does not own: the published shape of the read, the `DataRoom`, lot and account elements, the case-move answer, the error set and the fakes, which are RWB-S6-E5026-CON; the building of the masked tape and the masking check, which are RWB-S6-E5025-APP with rwb-document (P5) and the PII service; the buyer panel, the KYC and licensing check and the non-disclosure agreement, which are rwb-partner's (S9) and RWB-S6-E6002-APP's; the case of record, its route states, the parent `CaseWorkflow` and the case timers, which are rwb-case (P3); the bidding, the award, the transfer and their events, which are RWB-S6-E6004-APP, RWB-S6-E6005-APP and RWB-S6-E6007-APP; the rule rows and their versioning, which are governed in rwb-decision (P7); and the deployment of the build, which is the operations story of this legacy key.

### 2. Business rationale

The legacy step published the lot and the masked tape to the data room and wrote the decision log entry. The FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a target of 45 days (FSD S6 A2.4.1), and the feature runs unattended with the debt sale officer as also-user (FSD S6 A2.4.3.3). The requirement is REQ-S6-003, "The data room holds a masked data tape, and no unmasked personal data leaves the bank" (FSD S6 Requirements served).

What D-RCV-60 changes is who owns the lot, the tape, the buyers and the case. In the monolith one process read the lot, the tape and the buyer list in one schema. In the target:

- **the lot and its accounts are this service's.** Architecture v5 gives rwb-debtsale "lots, data room, buyer terms, bids, award, transfer", and the context pack gives `debt_sale_lot` and `debt_sale_account` to S6. This step reads both and writes neither; the data room has no table of its own and is read as the answer over them and the P5 tape, and the lot status after the opening is not named by any source (GAP-1962, BR10).
- **the tape is rwb-document's document.** R-DS-10 builds it under the PII masking rules and R-DS-11 rejects it when an unmasked identifier is found; both are the tape step's. This step consumes the prepared tape on the P5 contract and never rebuilds, re-masks or copies it (ASM-4901).
- **the "qualified buyers" are rwb-partner's panel.** R-DS-13 opens the room "to buyers who have signed the non-disclosure agreement"; the panel, the partner users and the partner channel are S9's, and the partner gateway in the DMZ fronts rwb-partner. This story reads the panel, it does not own it (ASM-4900).
- **the case of record stays with rwb-case.** `recovery_case` and the DEBTSALE route states are P3's; this story evaluates the rule, records the decision and answers the case move (ASM-4902).
- **the decision is recorded first**, through the local decision-record library in the same transaction as the state answer, which is what legacy AC1 asks and legacy AC2 tests.
- **nothing is published on the topic by this step.** The service owns `rwb.debtsale.events.v1` with `LotAwarded` and `AccountsTransferred`, and both belong to the award and transfer stories; this step has no event of its own, so 12.3 and 12.4 are None (ASM-4904).

No business value moves: the masking rules, the closed lists `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK`, the non-disclosure condition and the "per cycle" clock are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E5026-CON is published: the `GET /partner/data-room/{lotId}` operation on `/api/recovery/debtsale/v1`, the `DataRoom`, lot and account elements, the four closed lists, the consumed rows, the error set and the fakes are baselined and handed to this story.
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0. This story adds no table, no column and no migration.
- The masked tape of the lot exists and has passed its masking check under R-DS-10 and R-DS-11, and its reference and masking-check result are readable on the rwb-document contract. The operation name of that read is Not specified in the source documents (GAP-2977; ASM-4901), and the row is not in this story's contract-dependency list, which is None.
- The admitted buyer panel of the lot, with the non-disclosure agreement flag of R-DS-13, is readable on the rwb-partner contract. Its operation name is Not specified in the source documents (GAP-2977; ASM-4900), and the row is not in this story's contract-dependency list either.
- The case state and the case-move answer of rwb-case are available for the fake. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent applies, and any REST case-move operation carries the placeholder (GAP-2977; ASM-4902).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: PRT-05 reaches this service through the gateway-bff composite route on the staff channel and through the partner gateway on the buyer channel, one hop each (DP-19; ASM-4905).
- The DEBTSALE rule package is in force at its version with R-DS-10 to R-DS-13; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_document`, `rwb_partner` or `rwb_access` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E5026-CON when its tests pass.

### 4. Flow

1. The tape step of RWB-S6-E5025-APP completes R-DS-10 on an approved lot and records the masking-check result of R-DS-11 or R-DS-12, so the case reaches `TAPE_PREPARED`. Nothing of that step is run twice here.
2. The data-room step of `DebtSaleWorkflow` receives the trigger for a case in `TAPE_PREPARED` and reads the lot and its accounts from `debt_sale_lot` and `debt_sale_account`: `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id`, `buyer_class`, `signing_date`, `approval_authority`, `payment_terms` and `status`, with the account rows of DF-SAL-031 to DF-SAL-037.
3. The step reads the tape of the lot on the rwb-document contract: the document reference, the lot it belongs to, the masking-check result and the freshness of the document, one hop with a 2 s budget and a breaker. No unmasked account identifier and no borrower value is taken from that answer (ASM-4901).
4. The step reads the admitted buyer panel of the lot on the rwb-partner contract: the buyers with an active panel row and `nda_signed_at` present, which is the "buyers who have signed the non-disclosure agreement" of R-DS-13, one hop with a 2 s budget (ASM-4900).
5. The step reads the case state on the rwb-case read, to confirm that the case is in `TAPE_PREPARED` and to take the case reference the decision record carries.
6. `DataRoomEvaluator` loads the DEBTSALE package version in force from rwb-decision and evaluates R-DS-13 on the tape fact: `MASKING_CHECK_PASSED` and no unmasked identifier. Where the tape carries an unmasked identifier, R-DS-11 of the tape step is the branch that applies and this step changes nothing. Where no rule fires, the step changes nothing and reports the reason to the parent.
7. `DataRoomDecisionRecordWriter` writes one decision record through the local decision-record library, **before anything is served**: the case reference, the lot reference, the rule ID R-DS-13 with its version, the inputs reference (tape reference and panel reference), the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
8. `CaseMoveAnswer` answers rwb-case with the move `DATA_ROOM_OPEN`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (ASM-4902).
9. The lot is published to the data room: the lot rows are readable on API-S6-004 for the admitted buyers of that lot, and the tape is the document rwb-document holds. This step writes no new row of either table, and the value of `status` a data-room opening would carry is Not specified in the source documents (GAP-2977; ASM-4903).
10. A repeated trigger for the same case and the same tape reference writes no second decision record, serves no second opening and counts the repeat.
11. PRT-05 reads the lot, its accounts and its tape reference from this service through the partner channel and through the composite route, where the partner gateway asserts the buyer identity and its lot scope, next to the panel state of rwb-partner and the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no record, no case-move answer and no opening is served | MSG-P7-003 | AC2, TC-E5-026-02, TC-E5-026-04 |
| X2 | The caller does not hold the Partner portal right of the read | 403 before any read of the lot or the tape; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E5-026-03 |
| X3 | The case is not in `TAPE_PREPARED` | 409 and nothing is written; the room is not opened on a case that has already moved | None | AC1 |
| X4 | The tape is absent, its masking check has failed, or it is stale | The step holds, writes nothing and shows the data date; the opening resumes on the next fresh answer | MSG-P1-001 | AC1 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered; the caller sees 503 with the error envelope | None | AC1 |
| X6 | The buyer is not admitted to the lot: no active panel row or no signed non-disclosure agreement | The partner channel answers 403 with the error envelope; the buyer sees no lot, no account and no tape reference | MSG-P4-002 | AC1, TC-E5-026-03 |
| X7 | The lot is unknown, or the buyer is outside the scope of the lot | 404 with the error envelope; nothing is read and nothing changes | None | AC1 |
| X8 | The same trigger or the same tape reference arrives twice | One record, one answer and one opening; the repeat is counted and no second record is written | None | AC1 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC3, Section 17, BR3, BR5 |

X1 and X2 are the exception paths of RWB-E5-026 carried onto the split; X3 and X8 are the state and repeat paths the split makes explicit; X4 is the tape branch R-DS-11 and R-DS-12 that the tape step owns; X5 to X7 are the call-type and partner-channel paths; X9 is the DP-01 boundary. The masking rules of X4 and the non-disclosure condition of X6 are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E5026-CON, the rwb-document, rwb-partner and rwb-case fakes and the decision-record stub, on its own schema; needs no live P3, P5, S9 or P7 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the read and the lot and account columns are fixed |
| Valuable | An approved lot reaches the buyers of its panel with its masked tape and a recorded decision on the cycle it is due, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one record write, one case-move answer, three clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and synthetic panels through the contract fakes, plus the component cases of the refused role, the refused buyer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Open the buyer data room

  Background:
    Given case "RC-2026-001207" carries the approved lot "DS-2026-0007"
    Given the DEBTSALE rule package is in force at its version and carries R-DS-10, R-DS-11, R-DS-12 and R-DS-13
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Open the buyer data room (legacy RWB-E5-026 AC1)
    Given the rwb-document contract mock returns the masked data tape of lot "DS-2026-0007" as prepared by the tape step of RWB-S6-E5025-APP, with its masking check passed
    Given the rwb-partner contract mock returns the buyer panel of lot "DS-2026-0007" with the non-disclosure agreement signed
    Given the rwb-case contract mock returns the case state "TAPE_PREPARED" for "RC-2026-001207"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then publishes the lot and the masked tape to the data room for qualified buyers
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E5-026 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Boundary test of the buyer data room (exception X9) (new, D-RCV-60)
    Given a component, a statement or a test of this story reaches a `v_ace_*` view or another service's schema
    When the boundary test runs in the build
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC4 Business rules of section 8 (BR1 to BR10) (new, D-RCV-60)
    Given the rules of section 8 are in the build
    When the boundary and guardrail tests run
    Then each rule BR1 to BR10 holds and is covered by a test of section 16

  Scenario: AC5 Error answers of the provided operations (new, D-RCV-60)
    Given a caller of API-S6-004 with no valid session, a role without the Partner portal right, or an unknown lot
    When the caller sends the request
    Then the caller gets 401 for no valid session, 403 for a role without the Partner portal right or a buyer not admitted to the lot, and 404 for an unknown lot, each with the error envelope

  Scenario: AC6 Activity retry and timeout of openDataRoom (new, D-RCV-60)
    Given a consumed contract does not answer inside 2 s
    When the openDataRoom activity times out
    Then the activity is retried under a retry policy Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC6), nothing is written, no case move is answered and the caller sees the error envelope

  Scenario: AC7 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed contract returns an error or does not answer
    When the call fails
    Then nothing is written, no case move is answered and the caller sees the error envelope

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change is requested that the model does not allow from the current state
    When the change is requested
    Then the change is refused, nothing is written and no case move is answered
```

The two criteria are the legacy criteria of RWB-E5-026 word for word, with their origin tag added, the legacy term for the record changed to decision record, and nothing else changed: the repeated `Then`, the legacy wording of `the action is taken`, `the decision record cannot be written` and `its trigger arrives` all stand. The cross-service facts of AC1 are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those are the only additions to the legacy text; AC2 needs none, because the decision-record library is local. What the legacy lines describe happens in three places in the target: the masked tape is built and held by the tape step of RWB-S6-E5025-APP in rwb-document (P5); the "qualified buyers" are the admitted panel of rwb-partner (S9) behind the partner gateway; and this story evaluates R-DS-13, writes the record, answers the case move and serves the read, while rwb-case writes `DATA_ROOM_OPEN` on the case. The tape is referenced, never copied, and no unmasked personal data is served to a buyer (REQ-S6-003).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-13 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier | Open the data room to buyers who have signed the non-disclosure agreement | DATA_ROOM_OPEN | Debt sale officer | buyer portal, Document Hub | per cycle |
| R-DS-10 | Debt sale | D8.4 | LOT_APPROVED | TAPE_BUILD_RUN | Any | Build the masked data tape under the PII masking rules | TAPE_PREPARED | Workbench | PII service, Recovery Data Store, Document Hub | 3 working days |
| R-DS-11 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | Reject the tape and rebuild it | TAPE_REJECTED | Workbench | PII service, Document Hub | None |
| R-DS-12 | Debt sale | D8.4 | TAPE_REJECTED | TAPE_REBUILT | masking check passes | Return the tape for data room release | TAPE_PREPARED | Workbench | PII service | None |



The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a business role and not a service: R-DS-13 is evaluated here, the case move it names is written by rwb-case on this story's answer, the tape of R-DS-10 and R-DS-12 is built by the tape step of RWB-S6-E5025-APP, and the masking check of R-DS-11 is the PII service's on that tape. The three tape rows are tabled because they are the branch the same step reads and because R-DS-13 cannot be evaluated without their outcome (ASM-4901).

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and its accounts are this service's: `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id`, `buyer_class`, `signing_date`, `approval_authority`, `payment_terms` and `status` are columns of `debt_sale_lot` in `rwb_debtsale`, and no other service writes them | Architecture v5 (rwb-debtsale owns lots, data room, buyer terms, bids, award, transfer); TSD S6 T3.1; context pack ownership rows |
| BR2 | The decision is recorded before the room is served, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy RWB-E5-026 AC1 and AC2 |
| BR3 | The masked tape is rwb-document's document and the masking rules are the PII service's: this story reads the tape reference and its masking-check result on the owner's contract and never rebuilds, re-masks, copies or stores the tape | R-DS-10, R-DS-11; FSD S6 A2.3 and A2.4; ASM-4901 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | TSD S6 T4; context pack ownership rows; ASM-4902 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR6 | R-DS-13 opens the room to buyers who have signed the non-disclosure agreement: the admitted panel is read from rwb-partner and is never decided here | R-DS-13; Architecture v5 (rwb-partner owns the panel and the partner users); ASM-4900 |
| BR7 | No unmasked personal data leaves the bank: the partner answer carries the lot and its masked account rows, and no borrower code, account number or identity value | REQ-S6-003; FSD S6 A2.3.1; legacy Guardrails |
| BR8 | Every value a business person may change is reference data or a rule row read with its version: `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-PUTBACK`, the masking rules and the "per cycle" clock; the parameters are read as reference data, and the reference-data contract (DP-06, DP-07) is Not specified in the source documents (DOR-RWB-S6-E5026-APP-20) | TSD S6 T3.2; FSD S6 BR-S6-004; legacy Guardrails |
| BR9 | The opening publishes no event: `LotAwarded` and `AccountsTransferred` are the award and transfer stories', and this step writes no outbox row | TSD S6 T5.3; context pack event row EV-23; ASM-4904 |
| BR10 | The lot status a data-room opening would carry is not named by any source, and `LOV-LOT-STATUS` carries no data-room value, so this step writes no lot status | TSD S6 T3.2; ASM-4903 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent applies it to the case of record (BR4). What this story owns is the opening of the step and the decision it records.

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier, and the buyers hold a signed non-disclosure agreement | `DATA_ROOM_OPEN`, with this story's answer, its record and the served read |
| TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | `TAPE_REJECTED` by the tape step's answer, nothing here |
| TAPE_REJECTED | TAPE_REBUILT | masking check passes | `TAPE_PREPARED` by the tape step's answer, then this step |
| DATA_ROOM_OPEN and every later state | Any tape or opening trigger for the same lot | X3 | Unchanged, nothing written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The trigger arrives for a case in `TAPE_PREPARED` | The package in force is loaded | Evaluating |
| Evaluating | R-DS-13 fires | The tape fact and the panel are fresh | Recording |
| Recording | The record is written and the case-move answer is sent | The transaction commits | Waiting for the next trigger |
| Recording | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The tape is absent, stale or rejected | X4 | Held, until a fresh tape answer |

The route states are those of the DEBTSALE machine of TSD S6 T4 and they live on the case of record. The lot status values are those of `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED); none of them names a data-room opening, so this step writes no lot status (ASM-4903).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role of the feature, holding C, R, U and A on the lot and reading the opening outcome |
| RW-SALEOFF, sale officer | Debt sale R: reads the lot, its accounts and the opening outcome |
| RW-NPAMGR, NPA and asset manager | Debt sale R: reads the lot and its data-room state |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads, and approves where a lot needs it, which is the approval story's |
| RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-WRITEOFF | Debt sale R: read only, in scope |
| PT-BUYER, debt buyer and AMC | Debt sale RU: the buyer of the panel, who reads the lot, its masked accounts and its tape on PRT-05 through the partner gateway and bids in the bidding story |
| PT-RAMC, RAMC user | Debt sale R: reads the lot and its data-room state |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-partner service identity | Presents the buyer channel and the panel facts of the lot; it holds the partner users and the agreement, not the lot |
| rwb-debtsale service identity | Runs the step, evaluates R-DS-13, writes the record, answers the case move and serves the read; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission row of RWB-E5-026 gives the Partner portal right R to RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more, while T6.1 gives the buyer PT-BUYER RU on Debt sale; both statements are recorded and the wider holders list is left as the legacy text gives it (GAP-2977; ASM-4900). The FSD says the feature runs unattended with the debt sale officer as also-user, and both hold: the step runs under the service identity with no officer task on the happy path. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here. The rwb-access authorise check is named here: the read of API-S6-004 calls the rwb-access authorise contract for the Partner portal right before any read; its operation name is Not specified in the source documents (DOR-RWB-S6-E5026-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot reference the record and the answer carry |
| DF-SAL-021 to DF-SAL-024 | debt_sale_lot (S6) | lot_no, cut_off_date, segment, reserve_price | Read; `segment` against `LOV-SEGMENT`; `reserve_price` is withheld from a buyer until the award story publishes the terms |
| DF-SAL-025 to DF-SAL-028 | debt_sale_lot (S6) | buyer_partner_id, buyer_class, signing_date, approval_authority | Read; `buyer_class` against `LOV-BUYER-CLASS` |
| DF-SAL-029, DF-SAL-030 | debt_sale_lot (S6) | payment_terms, status | Read; `status` against `LOV-LOT-STATUS` and not written here (ASM-4903) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read; `borrower_code` is never served to a buyer (BR7) and `put_back_status` is against `LOV-PUTBACK` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, decided at, case and lot references | Write through the local library, before anything is served |
| Standard columns | debt_sale_lot and debt_sale_account | `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_active` | Not written here: this story inserts no row of either table |
| The masked data tape | document (P5, `rwb_document`) | the tape reference, the lot it belongs to and the masking-check result | Not read as a table: read on the rwb-document contract (ASM-4901) |
| The buyer panel | partner and partner_user (S9, `rwb_partner`) | panel status, partner user, `nda_signed_at`, buyer class | Not read as a table: read on the rwb-partner contract (ASM-4900) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case answer (ASM-4902) |
| rule_row | rwb_decision (P7) | the R-DS-10 to R-DS-13 rows and their version | Not read as a table: the package version is loaded from rwb-decision |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, this story writes neither, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03, DP-09). The data room has no table of its own: Architecture v5 names "data room" as part of what the service owns, while TSD S6 T3.1 defines only the lot and the account, so the room is a served view of those two tables and of the P5 tape.

**No personal data.** The rows and answers this story handles carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_debtsale`, the decision record, a log, an answer, a workflow input or a screen, and every fixture is synthetic. `borrower_code` stays in this service's table and is never served to the partner channel: the tape the buyer sees is masked under PDPA before it reaches the room (REQ-S6-003; BR7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). This story supplies the behaviour behind the one read whose shape RWB-S6-E5026-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partner/data-room/{lotId}` | `DataRoom` of status 200 out, with the lot, its masked accounts and its tape reference, for an admitted buyer (API-S6-004) | Partner portal, right R, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot and 503 when the library or a consumed contract does not answer. API-S6-001, API-S6-002, API-S6-003 and API-S6-005 belong to the lot, approval, award and bidding stories and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The tape read of rwb-document (operation name Not specified in the source documents (GAP-2977; ASM-4901)) | `/api/recovery/document/v1` | P5 rwb-document | The masked tape of the lot: its reference, the lot it belongs to, the masking-check result and its freshness; read only, faked |
| The buyer-panel read of rwb-partner (operation name Not specified in the source documents (GAP-2977; ASM-4900)) | `/api/recovery/partner/v1` | S9 rwb-partner | The admitted buyers of the lot: panel status, partner user and the agreement flag of R-DS-13; read only, faked |
| The case read of rwb-case | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2977; ASM-4902)) | on the rwb-case boundary | P3 rwb-case | The move `DATA_ROOM_OPEN` with the rule ID and its version; the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None (GAP-2977; ASM-4899).

#### 12.3 Events published

None. The data-room step of R-DS-13 publishes no event. The service's events are `LotAwarded` on `rwb.debtsale.events.v1`, with rwb-case and rwb-payment as consumers, and `AccountsTransferred` on the same topic, and both belong to RWB-S6-E6005-APP and RWB-S6-E6007-APP. This story writes no outbox row, declares no producer and holds no topic of its own, and a build that adds one fails the absence test (ASM-4904).

#### 12.4 Events consumed

None. The service's consumed event is `ProceedsMatched` from `rwb.payment.events.v1`, which is the settlement step's. The opening is triggered by the tape step's completed state and by the case signal the parent forwards, so this story holds no consumer group, no subscription and no inbox row of its own (ASM-4904).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case, the child of `CaseWorkflow`, the saga whose pivot is the transfer, using the Saga runner of the workflow kit | `rwb-debtsale` | Input: the case, the lot, the route and the package in force; signals: the case state, the package in force and the tape state; workflow ID: Not specified in the source documents (CG-ALL-10410); start: the catalog trigger is the monthly sale cycle opening or a residual arriving from disposal (R-DS-01); duplicate-start policy: Not specified in the source documents (CG-ALL-10410) |
| `openDataRoom` | Activity, the one data-room step | `rwb-debtsale` | The case and the lot in; the rule ID with its version, the opening and the case move out, with the record written before the answer and no outbox row |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source. The trigger is read as the arrival of the trigger for a case in `TAPE_PREPARED`, because the legacy story runs the step unattended while the FSD declares no background event for the feature (FSD S6 A2.4.4.4). The debt sale saga names the transfer as its pivot, and this step sits before it and needs no compensating activity of its own. No KYC or qualification operation is provided here: the qualification is the embedded admitted-panel check of BR6, and the award path of the legacy endpoint rows belongs to RWB-S6-E6005-APP.

#### 12.6 Schedules

None. The step runs from the tape step's completed state and from the case signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. The "per cycle" timer of R-DS-13 and the monthly cycle are durable timers of `DebtSaleWorkflow` and values of the rule package, not a Schedule of this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The approved lot; this story reads the row and writes none of its columns (ASM-4903) |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot; this story reads the rows and writes none of their columns |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of the R-DS-13 outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The outbox of the service; this story writes no row of it (BR9) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `document` (P5), `partner`, `partner_user` and the panel (S9), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), the bid and award rows (S6, the sibling stories') and every `v_ace_*` view (P1). No foreign key leaves the schema, and `buyer_partner_id` and `account_id` are identifiers, not cross-schema keys (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document tape fake | The masked tape of lot `DS-2026-0007` with its masking check passed and its date; the same tape with the check failed; a stale tape; no answer beyond 2 s | AC1, X4, X5 |
| rwb-partner panel fake | The panel of lot `DS-2026-0007` with two admitted buyers whose agreement is signed; a panel with no admitted buyer; a panel with the agreement missing; no answer beyond 2 s | AC1, X5, X6 |
| rwb-case state and move fake | The states `TAPE_PREPARED`, `TAPE_REJECTED` and `DATA_ROOM_OPEN` of case `RC-2026-001207`; an accepted move and a refused move | AC1, X3 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-10 to R-DS-13 | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC2, X1 |
| Partner channel and gateway-bff route fake | The merged PRT-05 answer for lot `DS-2026-0007` for an admitted buyer, and the 403 of a buyer who is not admitted | AC1, X6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the tape read, the panel read and the case-move answer carry the placeholder until their owners confirm them (GAP-2977; ASM-4899 to -4).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The `GET /partner/data-room/{lotId}` read on `/api/recovery/debtsale/v1`; the tape read, the panel read, the case read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | This step publishes and consumes nothing; `LotAwarded` and `AccountsTransferred` are the award and transfer stories' |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its `openDataRoom` step on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; the tape is a P5 document referenced by claim-check, and the buyer file of INT-25 is delivered on the partner channel (ASM-4901) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `dataroom`; front end fragment `src/modules/recovery/debtsale/DataRoom.tsx`, the PRT-05 fragment that rwb-partner's buyer panel embeds on the partner channel and that the staff route reads, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record is written in the caller's transaction before anything is served, and a failed write changes nothing. DP-13 moves the base of the read and nothing else. DP-19 is how PRT-05 reaches this service, one hop: the buyer channel through the partner gateway to rwb-partner's buyer panel, the staff channel through the composite route, and the screen field list and route specification belong to RWB-PLT-N001-CON (ASM-4905).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and not in the metadata, and the partner-channel route has no plan row of its own, so both are recorded in the registers and neither is added to the metadata (ASM-4899, -7). The outbox library of DP-09 is not a dependency of this step, because it publishes no event (ASM-4904).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` data-room branch | Workflow | Waits for a case in `TAPE_PREPARED`, loads the package in force and reports the outcome to the parent |
| `openDataRoom` | Activity | The one step: read the lot, the tape, the panel and the case, evaluate R-DS-13, write the record and answer the move |
| `DataRoomEvaluator` | Service | The rule evaluation against the package version in force, with the tape fact and the panel fact |
| `DataRoomDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and version before anything is served, hash-linked, and refuses the step when the write fails (DP-03) |
| `LotReader` | Repository | Reads `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`, with the scope filter of the caller |
| `DocumentTapeClient`, `PartnerPanelClient`, `CaseStateClient` | Clients | The tape, panel and case rows, one hop, 2 s, breaker each |
| `DataRoomController` | Controller | The one read, the capability area and right, the buyer scope, the masking rule of the answer and the problem mapping |
| `DataRoom` | React component | Shows the lot, its masked accounts and its tape on PRT-05, with the refused and not-admitted states |

**Database and migrations.** No Flyway file. The two lot tables arrive with the DB story of this service, and the record, key and outbox are library objects created in `rwb_debtsale` by the library's migration.

**Configuration and reference data.** `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2); the DEBTSALE package and its version, loaded on `RulePackageInForce`, with the masking rules, the non-disclosure condition and the "per cycle" clock as values; the capability area "Partner portal" and right R as access rows of rwb-access. No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The data-room branch of `DebtSaleWorkflow`, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the `TAPE_PREPARED` trigger.
2. The three clients against their fakes, with the 2 s budget, the breaker, the stale-tape path and the no-answer path (AC1, X4, X5).
3. `LotReader` and the scope filter over the two tables, with the masking rule of the answer (AC1, BR7).
4. `DataRoomEvaluator` over the package, with R-DS-13, the tape fact, the panel fact and the no-fire path (AC1).
5. `DataRoomDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `CaseMoveAnswer` and the parent signal, with the move, the repeat path and the state guard (AC1, X3, X8).
7. `DataRoomController` with the right, the buyer scope, the masking rule and the problem mapping (AC1, X2, X6, X7).
8. `DataRoom` and PRT-05 on the partner channel and through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to another service's schema (X9, BR3, BR5).

**Feature flag.** `rwb.debtsale.data-room-v1`, read as a flag of the platform library; off means the step holds the trigger, writes nothing and serves no opening.

**Done when.** The tests of section 16 pass, the step runs from a synthetic tape and panel in SIT, R-DS-13 produces its record, its answer and its served read, a repeated trigger writes once, a forced record failure changes nothing, a buyer without an active panel row or a signed agreement is refused with 403, no `recovery_case` row and no `v_ace_*` read exists in the build, and PRT-05 answers on the partner channel and through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation and belongs to the eligibility step of RWB-S6-E5023-APP, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | The `lotId` path parameter is absent or malformed, or a required input of the step is absent (X7) | Enter {field}. |
| MSG-P4-002 | A role without the Partner portal right reads the room, or a buyer is not admitted to the lot (X2, X6) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the room is served (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The tape or its masking-check result is stale after a late or failed step (X4, VR-S6-004-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are those of the legacy message set and of FSD S6 A2.4.3.1; the text of the four legacy messages is copied unchanged, and the text of MSG-P1-001 is the wording of Error and Message Standard v4; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it. MSG-P1-001 carries the Error and Message Standard v4 wording although the check behind it is the tape step's and the owner of the batch status is rwb-source-data (ASM-4901).

### 15. Screens and states

Screens of this story: PRT-05 Data room, the only screen this story serves; no other screen is named here.

PRT-05 Data room in its admitted, bidding and closed states is served through the partner channel to rwb-partner's buyer panel and, for staff, through the gateway-bff composite route (DP-19; ASM-4905). The route calls rwb-debtsale for the lot, its masked accounts and its tape reference, rwb-partner for the panel and the buyer, rwb-document for the tape and rwb-case for the case and its route state. This story fixes the rwb-debtsale answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the admitted state of PRT-05 for a lot: the lot, its date, its segment and its masked account rows, with the tape reference the buyer may open. The bidding state belongs to RWB-S6-E6004-APP and the closed state to the award and put-back stories of this service, and both read the same route. The refusal and failure states are: refused with MSG-P4-002 for a role without the right and for a buyer who is not admitted, not recorded with MSG-P7-003, and stale tape with MSG-P1-001.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-026-01 | AC1 | Component | Case `RC-2026-001207` at `TAPE_PREPARED` with the tape of lot `DS-2026-0007` passed and its panel admitted; the record, the `DATA_ROOM_OPEN` answer and the served read asserted on the fakes |
| TC-E5-026-02 | AC2 | Component | The decision-record stub stopped; nothing written, no answer, no opening and MSG-P7-003 shown |
| TC-E5-026-03 | Access | Component | A role without the Partner portal right, and a buyer with no active panel row or no signed agreement; 403 with MSG-P4-002 and no read of the tape |
| TC-E5-026-04 | Principle 5 | Component | A forced record write failure at the moment of the answer; no record, no case move and no opening |
| TC-E5-026-05 | §12 | Component | The operations, events and activities of §12 checked against the rwb-debtsale contract, including the openDataRoom activity and the DebtSaleWorkflow start; no operation outside §12 served |
| TC-E5-026-06 | §12.7 (ASM-3438) | Component | Each table of §12.7 read and written only as its owner states; no write to debt_sale_lot or debt_sale_account and no read of recovery_case |
| TC-E5-026-07 | AC3 | Build | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC3) |
| TC-E5-026-08 | AC4 | Component | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC4) |
| TC-E5-026-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC5) |
| TC-E5-026-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC6) |
| TC-E5-026-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC7) |
| TC-E5-026-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S6-E5026-APP-AC8) |

The four legacy cases are those of RWB-E5-026 in their legacy order, with the Level column added: the legacy `System` level maps to `Component` where the step is tested on its fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy belongs to this story, because the cross-service journey of the legacy key is the wave 3 harness's.

### 17. Guardrails

- No business value in code: the masking rules, the non-disclosure condition, the "per cycle" and monthly clocks, the four lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in an answer, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, `borrower_code` never leaves the service, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-01).
- The case stays with rwb-case, the tape with rwb-document and the panel with rwb-partner: no case row, document row or partner row is written here (BR3, BR4, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event of this step and no data-lake extract.
- The decision is recorded before anything is served; a build that serves the room before the record commits fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank (FSD S6 Requirements served). The TSD requirement table maps it to FEAT-DBS-01 while the FSD gives the room to FEAT-DBS-04 (GAP-2977) | The data-room step, the tape read and the masked answer | TC-E5-026-01, TC-E5-026-04 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| FEAT-DBS-04 | Open the buyer data room, prerequisite FEAT-DBS-03 (FSD S6 A2.4; Epics 3 to 8 Specification v3) | The whole story | TC-E5-026-01 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| R-DS-13 | TAPE_PREPARED and MASKING_CHECK_PASSED to DATA_ROOM_OPEN for buyers who signed the agreement (Business Rules and Routing Logic v4) | The evaluator and the case-move answer | TC-E5-026-01 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot and the room | TC-E5-026-01 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E5-026-04 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| ADR-019 | Edge: gateway-bff and partner gateway | The buyer channel and the staff route of PRT-05 | TC-E5-026-03 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E5-026-01 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before the answer | TC-E5-026-02, TC-E5-026-04 | FEAT-DBS-04 | Not specified in the source documents (DOR-RWB-S6-E5026-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-026, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Source text | Legacy RWB-E5-026; FSD S6 Debt sale v3 A2.4; TSD S6 Debt sale v2 T2 to T6 and T-A; Epics 3 to 8 Specification v3 row FEAT-DBS-04; Business Rules and Routing Logic v4 rows R-DS-10 to R-DS-13 |
| Test cases | TC-E5-026-01 to TC-E5-026-04 |
| Feature and screens | FEAT-DBS-04, PRT-05 Data room |
| Rules | R-DS-13, with the tape branch R-DS-10 to R-DS-12 of RWB-S6-E5025-APP, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the read, the `DataRoom`, lot and account elements, the four closed lists, the consumed rows, the error set and the fakes: RWB-S6-E5026-CON.
- The building of the masked tape, the masking check and the PII masking rules: RWB-S6-E5025-APP, the PII service and rwb-document (P5) (ASM-4901).
- The buyer panel, the partner users, the non-disclosure agreement, the KYC and licensing qualification and the remediation window: rwb-partner (S9) and RWB-S6-E6002-APP (ASM-4900).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (ASM-4902).
- The lot building, the estimate of the price and the reserve: RWB-S6-E5024-APP and RWB-S6-E6001-APP, API-S6-001 and API-S6-002.
- The bidding, the award and the transfer, and the events `LotAwarded` and `AccountsTransferred`: RWB-S6-E6004-APP, RWB-S6-E6005-APP and RWB-S6-E6007-APP, API-S6-005 and API-S6-003.
- The rule rows of R-DS-10 to R-DS-13 and their versioning, and the reference data of the four lists: rwb-decision (P7) and rwb-case (P3) per the default rulings.
- The access guard library and the capability rows of the Partner portal right: rwb-access (P4) and the service template.
- The partner gateway in the DMZ, its FAPI 2.0 profile and the penetration test before launch, and the composite route and PRT-05 field list: the edge stories and RWB-PLT-N001-CON (ASM-4905; NFR-056).
- The lot status a data-room opening would carry: not named by any source (ASM-4903).
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
