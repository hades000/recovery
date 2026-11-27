# RWB-S5-E4024-APP Run auction rounds and report bids

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-P |
| Ready to start | Day 1 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S5-E4024-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-S5-E4024-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S5-E4024-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs); traces to FEAT-AST-15 of FSD S5 A2.15 and the epic BRD row for that feature until the PRD allocates requirement ids (GAP-2909; ASM-4807) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-024 for rwb-asset. The three legacy criteria are kept word for word with their origin tag and the five legacy test cases keep their IDs. The round becomes the auction branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it opens each round at the price step the schedule sets, records the reported round on `listing` and the sale record it opens in `rwb_asset`, evaluates R-DIS-36, R-DIS-37, R-DIS-40, R-DIS-49 and R-DIS-50 on the DISPOSAL package in force, records each outcome before the row changes (DP-03), answers the case in rwb-case and publishes nothing. The legacy `v_ace_payment` and `v_ace_score` reads leave the service: the payment fact arrives on the rwb-payment boundary and the vendor score on the rwb-partner boundary (DP-05). The base becomes `/api/recovery/asset/v1` (DP-13) and SCR-24 and SCR-21 read through the gateway-bff route (DP-19). Gaps: no element holds a round's bids (GAP-2906; ASM-4804); consumed operation names not published (GAP-2907; ASM-4805); R-DIS-49 sits across the payment-term story (GAP-2908; ASM-4806); no requirement id (GAP-2909; ASM-4807); DP-04 outside the pattern set (GAP-2910; ASM-4808); the award and its cancellation have no element (GAP-2911; ASM-4809). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 10 cross-document, 8 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **auction vendor**, I want **the Workbench to let the vendor run each round and report the bids back into the case**, so that **assets sell sooner at approved prices** (legacy RWB-E4-024, word for word).

This is the application slice of legacy RWB-E4-024. It owns:

- the three legacy criteria with their origin tag, and the rules, messages and screens they depend on;
- the round branch of `AssetDisposalWorkflow` on `rwb-asset`, a child of the case workflow (Architecture v5 slide 13);
- the opening of a round at the price step the schedule sets (R-DIS-36) and the record of the reported round and its bids (R-DIS-37) on `POST /listings/{listingId}/rounds`;
- the outcome of a reported bid at or above the floor (R-DIS-40) and the cancellation of the award with the vendor score and the reopened round when the payment term expires (R-DIS-49, R-DIS-50);
- the write of the round number and the listing status on `listing`, and of the sale record a round opens, in `rwb_asset`;
- the decision record of each outcome before the change (DP-03) and the case answers `ROUND_OPEN`, `BID_RECEIVED`, `SALE_AGREED` and `AWARD_CANCELED`;
- the reads of SCR-24 and SCR-21 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shape of the round write and the reads and the consumed rows, which are RWB-S5-E4024-CON; the start price, the floor and its approval, which are FEAT-AST-11's story; the listing publication, FEAT-AST-12; the step down on a round with no bid and the re-list, which are FEAT-AST-13 and FEAT-AST-17's stories; the second signature of a bid below the floor, FEAT-AST-16's story; the five-day payment term itself and the title transfer, FEAT-AST-18 to FEAT-AST-20's stories; the vendor allocation, FEAT-AST-14's story; the case and its states, rwb-case (P3); the payment and its posting, rwb-payment (P8); the vendor panel and scorecard, rwb-partner (S9); the rule package, rwb-decision (P7); the deployment, the operations story of this key.

### 2. Business rationale

Legacy RWB-E4-024 kept a listing moving through its auction rounds: the vendor ran each round on the portal, the bids came back into the case, and a bid at or above the floor became a sale. The FSD keeps it as FEAT-AST-15 in module S5, run by the auction vendor on the partner portal and the auction portals, after FEAT-AST-14 allocates the asset to a vendor and before FEAT-AST-16 tests a bid below the floor.

What D-RCV-60 changes:

- **the round is this service's.** `listing` in `rwb_asset` carries the round number, and the standard columns carry the status (Ownership Map; Architecture v5 slide 41). No source names an element for the bids of a round, so the bids are a gap and not an invented table (GAP-2906; ASM-4804).
- **the picture stays with its owners.** The case state is rwb-case's, the payment is rwb-payment's and the vendor score is rwb-partner's; the legacy `v_ace_*` reads leave the service (DP-05).
- **the decision is recorded first**, one per outcome, in the row's transaction — what AC1 asked and AC3 tested.
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3); §12.3 states the absence and a build that adds an event fails it.

### 3. Preconditions

- RWB-S5-E4024-CON tagged: the round write, the two reads, the consumed rows, the decision-record element, the rule-package element, the error set and the fakes.
- `listing` exists in `rwb_asset` with TSD S5 T3.1 columns including `round_no`; `asset_sale` exists with its sale elements; no column holds a bid and none is added (GAP-2906; ASM-4804).
- The DISPOSAL package is in force with R-DIS-36, R-DIS-37, R-DIS-40, R-DIS-49 and R-DIS-50 from rwb-decision (P7), loaded through the service template; DP-04 is outside the pattern set (GAP-2910; ASM-4808).
- The price step of the round is the schedule `listing` already holds; the ladder and its step are reference data with their version (TSD S5 T3.2).
- The `LOV-LISTING` and `LOV-SALE-CHANNEL` lists are reference data with their version.
- The rwb-case state read, the case-move answer, the rwb-payment payment fact and the rwb-partner vendor score are behind fakes; none of their names is published (GAP-2907; ASM-4805).
- The round due fact and the payment-term expiry arrive as signals of `AssetDisposalWorkflow`; no subscription is added.
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the two screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass.

### 4. Flow

1. The listing is live and its schedule step falls due; `AssetDisposalWorkflow` wakes on the durable timer, confirms the case state on the rwb-case contract and opens round `n`.
2. The step writes the round number and the status on `listing`, records the opening (DP-03) and answers `ROUND_OPEN` to rwb-case.
3. The auction vendor runs the round on the portal; the portal reports it as `POST /listings/{listingId}/rounds` with the round number, the date, the result and the price of the round, and an `Idempotency-Key`.
4. `AssetController` checks the Asset and disposal right U, the listing and its status, and the round number; a listing that is not live and a round out of order are refused (X4).
5. `RoundEvaluator` loads the package in force and evaluates R-DIS-37: from `ROUND_OPEN`, on `BID_PLACED`, the bid is recorded against the round and the asset and the case moves to `BID_RECEIVED`.
6. `AssetDecisionRecordWriter` writes one record **before any change**; a failed write stops the request (DP-03; AC1, AC3).
7. `RoundWriter` writes the round number and the status on `listing` in one transaction with the record and the idempotency row; the round price and the result are held where an element carries them and are Not specified in the source documents elsewhere (GAP-2906; ASM-4804).
8. The answer carries the round and the sale record the round opens (`AssetSale`), and `CaseMoveAnswer` answers `BID_RECEIVED` with the round, the price and the rule version; rwb-case writes the case (GAP-2911; ASM-4809).
9. On a bid at or above the floor R-DIS-40 fires: the bid is accepted, the sale is agreed, one record is written and the answer carries `SALE_AGREED`. A bid below the floor is not accepted here: the case moves to `SECOND_SIGNATURE_PENDING` on the second-signature story's step (X3).
10. The payment term runs on the awarded sale; when it expires with no payment, R-DIS-49 fires from `AWAITING_PAYMENT`: the award is cancelled, the vendor is scored and the round is reopened, one record is written and the answer carries `AWARD_CANCELED` (AC2).
11. R-DIS-50 then reopens the round at the same price step: the round number and the status are written again, a record is written and the answer carries `ROUND_OPEN`; no price steps down here.
12. A repeated request or key writes once and is counted; the workflow returns to its durable timer and continues as new at each stage end and at least every 28 days.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered, the sale record not opened | MSG-P7-003 | AC3, TC-E4-024-03, TC-E4-024-05 |
| X2 | The role lacks the Asset and disposal right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-024-04 |
| X3 | The case is in another state, or the bid is below the floor | The rule does not fire; nothing accepted, the state reported | MSG-S5-001 where under the limit | AC2 |
| X4 | The listing is not live, or the round number is out of order | 409 with the stage the listing is in; nothing written | MSG-GEN-001 | AC1 |
| X5 | The same report or key arrives twice | One round, one record, one answer | None | AC1 |
| X6 | The payment fact is missing or stale at the due date | The cancellation is held until the fact confirms no payment; the data date is shown | None | AC2 |
| X7 | The vendor score boundary does not answer | The award is still cancelled and the score is queued on the workflow | None | AC2 |
| X8 | A contract misses 2 s or its breaker is open | Retry on the workflow schedule; 503 in the platform envelope | None | AC1, AC2 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | AC4, TC-E4-024-08, §17, BR9 |

X1 to X3 are the legacy paths on the split, X4 to X8 what the round write, the boundaries and the payment fact add, and X9 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P3, P8 or S9 |
| Negotiable | Activity name, decision code and outcome shape are ours; rules, messages, screens, rows and reads are fixed |
| Valuable | The vendor reports a round and the case sees its result the same hour; the award reopens when the term is missed |
| Estimable | One branch, two evaluators, one record per outcome, two row changes, four answers, two clients, one screen fragment |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, wrong-state, repeat, stale-payment and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Run auction rounds and report bids

  Background:
    Given case "RC-2026-000541" holds asset "AST-2026-000541" in live listing "LS-2026-000541"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-36, R-DIS-37, R-DIS-40, R-DIS-49 and R-DIS-50
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Run auction rounds and report bids (legacy RWB-E4-024 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000541" in state ROUND_OPEN with round 1 open on the listing
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the vendor run each round and report the bids back into the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-49 (legacy RWB-E4-024 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000542" in state AWAITING_PAYMENT with an award on the sale
    Given the rwb-payment contract mock returns no payment received by the payment due date for "RC-2026-000542"
    Given a case in state AWAITING_PAYMENT
    When payment term expired
    Then cancel the award, score the vendor and reopen the round
    Then the case moves to AWARD_CANCELED

  Scenario: AC3 Not recorded (legacy RWB-E4-024 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 Boundary refuses ACE and foreign reads (exception X9, DP-01 and DP-05) (new, D-RCV-60)
    Given a statement in the rwb_asset service reads a v_ace_* view, recovery_case or a foreign schema
    When the statement runs against the grant
    Then the grant refuses it
    Then the boundary test fails the build

  Scenario: AC5 Business rules BR1 to BR10 hold (§8) (new, D-RCV-60)
    Given the rwb_asset service is deployed with its grant and its contract fakes
    When the round is run, reported, recorded and answered
    Then each rule BR1 to BR10 in §8 holds and is checked by its test in §16

  Scenario: AC6 Error answers of the provided operations are 401, 403 or 404 (new, D-RCV-60)
    Given the provided operations of rwb_asset are published with their error envelope
    When a request is refused for a missing valid login, for a role without the Asset and disposal right, or for an unknown asset or listing
    Then the answer is 401, 403 or 404 in the platform error envelope
    Then nothing is read or written beyond the refusal

  Scenario: AC7 Replay of a write with the same idempotency key writes once (new, D-RCV-60)
    Given a round report with an idempotency key already recorded for the round
    When the same report arrives again with that key
    Then no second round, record or answer is written

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the rwb-case contract mock returns a case in state ROUND_OPEN
    When a status change is requested that the rules do not allow from that state
    Then the change is refused and the state is reported
    Then nothing is written

  Scenario: AC9 An activity that is retried or times out writes once (new, D-RCV-60)
    Given the rwb-case contract mock returns a case in state ROUND_OPEN
    When an activity of the round is retried or runs past its timeout
    Then the retry carries the same idempotency key as the first attempt
    Then no second round, record or answer is written

  Scenario: AC10 A consumed call that fails or does not answer writes nothing (new, D-RCV-60)
    Given the rwb-case contract mock returns no answer for a case
    When a consumed call fails or does not answer
    Then nothing is written and the case stays in its state
    Then the round is not reported as recorded
```

The three criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `the action is taken`, `payment term expired` and `the decision log cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-case writes the four moves, rwb-payment and rwb-partner answer the payment and the score, and this story opens the round, records the report, evaluates the rules, writes the row, records and answers. AC2's "reopen the round" is R-DIS-50's step; the award and the term it expires are FEAT-AST-18's story (GAP-2908; ASM-4806). R-DIS-49 and R-DIS-50 are kept with this story because AC2 tests them; R-DIS-47 and R-DIS-48 stay with FEAT-AST-18's payment-term story, so the two stories are not built twice.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-36 | Asset disposal | D8.1 to D8.3 | LISTING_LIVE | ROUND_OPENED | schedule step due | Open the round at the scheduled price step | ROUND_OPEN | Auction and remarketing vendor | auction portal, Workbench scheduler | per schedule |
| R-DIS-37 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | BID_PLACED | Any | Record the bid against the round and the asset | BID_RECEIVED | Workbench | auction portal | None |
| R-DIS-40 | Asset disposal | D8.1 to D8.3 | BID_RECEIVED | BID_AT_OR_ABOVE_FLOOR | bid_amount at or above floor_price | Accept the bid and agree the sale | SALE_AGREED | Sale officer | Case Workspace, auction portal | 1 working day |
| R-DIS-49 | Asset disposal | D8.1 to D8.3 | AWAITING_PAYMENT | PAYMENT_TERM_EXPIRED | payment absent and payment_due_date passed | Cancel the award, score the vendor and reopen the round | AWARD_CANCELED | Sale officer | auction portal, Partner Portal | None |
| R-DIS-50 | Asset disposal | D8.1 to D8.3 | AWARD_CANCELED | ROUND_REOPENED | Any | Reopen the round at the same price step | ROUND_OPEN | Auction and remarketing vendor | auction portal | None |

The five rows are copied character for character from the Business Rules and Routing Logic v4; their owner column is a business role, so the case stays in these states and moves in rwb-case on this story's answer, while the `listing` row and the sale record are written here. R-DIS-38 and R-DIS-39 (the round with no bid) are FEAT-AST-13 and FEAT-AST-17's; R-DIS-41 and R-DIS-42 (a bid below the floor) are FEAT-AST-16's; R-DIS-47 and R-DIS-48 (the term and its payment) are FEAT-AST-18's (GAP-2908; ASM-4806). The DISPOSAL package in force is loaded through the service template; DP-04 (the H and C rows) is outside this slice's pattern set, so no platform rules-kit row is added here and the reading is recorded for the next realignment of the pattern set (GAP-2910; ASM-4808).

| ID | Rule | Source |
|---|---|---|
| BR1 | The round is this service's: `round_no` and the status are `listing` elements in `rwb_asset`, and the sale a round opens is `asset_sale` there | Ownership Map; Architecture v5 slide 41; TSD S5 T3.1 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version; a failed write changes nothing | DP-03; AC1, AC3 |
| BR3 | The price step, the floor and the re-list limit are rule rows or reference data with a version, never a constant | TSD S5 T3.2; legacy Guardrails |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2907 |
| BR5 | No element holds the bids of a round: the report carries the round, the date, the result and the price, and a bid list is Not specified in the source documents | GAP-2906; ASM-4804 |
| BR6 | The payment fact is rwb-payment's and the vendor score is rwb-partner's; no `v_ace_payment` read and no `v_ace_score` read here | DP-05; Architecture v5 slide 8 |
| BR7 | No event is published; EV-22 `AssetTakenOn` is the take-on story's | TSD S5 T5.3 |
| BR8 | A repeated report or key writes once, answers once and is counted | TSD S5 T-A.2 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR10 | No personal data in the schema, a record, a log or a workflow input; a bidder is a code, never a person | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (case state) | Event | Condition | To |
|---|---|---|---|
| LISTING_LIVE | `ROUND_OPENED` under R-DIS-36 | The schedule step is due | ROUND_OPEN, answer `ROUND_OPEN` |
| ROUND_OPEN | `BID_PLACED` under R-DIS-37 | Any reported bid | BID_RECEIVED, answer `BID_RECEIVED` |
| BID_RECEIVED | `BID_AT_OR_ABOVE_FLOOR` under R-DIS-40 | Bid amount at or above the floor | SALE_AGREED, answer `SALE_AGREED` |
| AWAITING_PAYMENT | `PAYMENT_TERM_EXPIRED` under R-DIS-49 | Payment absent and the due date passed | AWARD_CANCELED, answer `AWARD_CANCELED` |
| AWARD_CANCELED | `ROUND_REOPENED` under R-DIS-50 | Any | ROUND_OPEN, answer `ROUND_OPEN` |
| Any | An unexpected state, a bid below the floor or a repeated report | X3, X5 | Unchanged |

| `listing` status | Event | Condition | To |
|---|---|---|---|
| Live | The round opens | R-DIS-36 fires | Live, `round_no` = n |
| Live | A round is reported | R-DIS-37 fires | Live, `round_no` = n, result recorded |
| Live | A bid at or above the floor is accepted | R-DIS-40 fires | Under offer, sale record opened |
| Under offer | The term expires | R-DIS-49 and R-DIS-50 fire | Live, same `round_no` |
| Any | A duplicate request or key | X5 | Unchanged |

The statuses are the `LOV-LISTING` rows of TSD S5 T3.2; the case states are the DISPOSAL machine's (TSD S5 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| PT-AUCTION, auction and remarketing vendor | Asset and disposal U: reports a round and its bids on the portal |
| RW-SALEOFF, RW-ENFORCE, RW-NPAMGR, SY-DATALOAD | Asset and disposal U: the round write, the award cancellation and the reopen |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL and the further roles of the read row | Asset and disposal R, in scope |
| PT-RAMC | Asset and disposal R and U on its own listings |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the branch; no grant on another schema and no `v_ace_*` grant |

The rights are the rows of the legacy permission table and TSD S5 T6.1, nothing wider. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability. The rwb-access authorise check of each operation is Not specified in the source documents (DOR-RWB-S5-E4024-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at, status | Write: round_no, status |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_key, listing_id, contract_date, sale_date, sale_price, transfer_fee and 6 more | Write: the sale record a round opens, its dates and price completed by the accept and award stories; the award element is Not specified in the source documents (GAP-2911; ASM-4809); read on R-DIS-49 |
| Standard columns | listing, asset_sale (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| Not specified in the source documents (GAP-2906; ASM-4804) | none | the bids of a round, their count and the best amount | No element; the round records its round number, date, result and price, and the bid list is a gap of this service until the DB story or the LDM names it |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount and 8 more | Not read: rwb-payment boundary (BR6) |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, score_value and 6 more | Not read: rwb-partner boundary (BR6) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, book_value and 9 more | Not read: rwb-source-data contract (BR6) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03); `decision_record` is not an entity of Logical Data Model v9 or Data Classification v5. **No personal data**: identifiers, codes, amounts, dates, a vendor code and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). Contract version 5.0.0 (rwb-asset.yaml, Recovery Workbench API Specification v5). This story supplies the behaviour behind the shapes of RWB-S5-E4024-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the round of each listing (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with title, listing, round number and round price (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |
| POST | `/listings/{listingId}/rounds` | AuctionRoundRequest in — roundNo, heldOn, result, price — and the sale record the round opens out, `AssetSale`, 200 (API-S5-005) | Asset and disposal, U, scope applied | Idempotency-Key |

The round write is the only write of this slice; the listings write `POST /assets/{assetId}/listings` (API-S5-004) is the pricing story's and is not changed here. Errors: 400 with Not specified in the source documents (CG-ALL-10023), 401 with Not specified in the source documents (CG-ALL-10023), 403 with MSG-P4-002, 404 with Not specified in the source documents (CG-ALL-10023), 409 for a listing that is not live or a round out of order with Not specified in the source documents (CG-ALL-10023), 422 with MSG-GEN-001 or MSG-S5-001, 503 when a library or a contract does not answer with Not specified in the source documents (CG-ALL-10023).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and the round the case sees; faked |
| Case-move answer (name Not specified in the source documents (GAP-2907; ASM-4805)) | rwb-case (P3) | P3 rwb-case | `ROUND_OPEN`, `BID_RECEIVED`, `SALE_AGREED` and `AWARD_CANCELED` with the rule and its version; faked |
| Payment fact activity (name Not specified in the source documents (GAP-2907; ASM-4805)) | queue `rwb-payment` | P8 rwb-payment | The payment due date and whether the payment arrived; the legacy `v_ace_payment` read becomes this row (DP-05); faked |
| Vendor score activity (name Not specified in the source documents (GAP-2907; ASM-4805)) | queue `rwb-partner` | S9 rwb-partner | The score of the vendor whose award was cancelled; the legacy `v_ace_score` read becomes this row (DP-05); faked |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). They are the cross-service rows the plan does not carry, so this story builds on their documents and fakes and its C and I rows are None; the wave 3 harness holds the real journey.

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale event the sale stories'; a round, a bid and a cancelled award write no outbox row and add nothing to `rwb.asset.events.v1`. A build that publishes here fails the absence test.

#### 12.4 Events consumed

None. The round due fact, the payment-term expiry and the vendor score arrive as signals and activities of `AssetDisposalWorkflow`; the rwb-payment subscription of the connection matrix belongs to FEAT-AST-18's story, so this slice adds no consumer group and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new across the holding | `rwb-asset` | Input: case, route, asset, listing, package in force; signals: round due, round reported, payment-term expiry, package in force |
| `reportAuctionRound` | Activity, the round write | `rwb-asset` | Listing, round and report in; rule IDs with versions, round number, status, sale record reference and case move out, one transaction |

No child workflow and no second queue. The activity name is a design choice of this story; the two boundary activities run on the owner's queue. The consumed operation names of rwb-case, rwb-payment and rwb-partner are Not specified in the source documents (GAP-2907; ASM-4805); the build runs against the documents and their fakes, and the names come from the owners' published contracts at the tag of RWB-S5-E4024-CON. R-DIS-49 and R-DIS-50 are evaluated once, in this story; R-DIS-47 and R-DIS-48 belong to the payment-term story (FEAT-AST-18) and are not evaluated here. R-DIS-11 and R-DIS-37 are declared once for rwb-asset as the state gates they name; R-DIS-37 is also built by FEAT-AST-15, and that duplication is recorded for the story-split review.

Workflow ID form, start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-10025; DOR-RWB-S5-E4024-APP-8).

#### 12.6 Schedules

None. R-DIS-36 runs "per schedule" as a durable timer inside the workflow; the step owns no Temporal Schedule and no Quartz job. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing; this story writes `round_no` and the status |
| asset_sale | S5 (`rwb_asset`) | The sale a round opens; written here, read on the cancellation |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated report |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8), every `v_ace_*` view (P1). No bid table exists (GAP-2906; ASM-4804). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | `ROUND_OPEN`, `BID_RECEIVED`, `SALE_AGREED` and `AWAITING_PAYMENT` for the fixture cases; a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | The four moves accepted; a move refused for an unexpected state | AC1 to AC3 |
| rwb-payment payment fact fake | No payment by the due date; a payment received a day early; a stale fact | AC2, X6 |
| rwb-partner vendor score fake | The score of vendor `VN-2026-0012`; no answer inside 2 s | AC2, X7 |
| rwb-decision package fake | The DISPOSAL package at its version with the five rules | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| Composite route fake | The merged SCR-24 and SCR-21 answer for `RC-2026-000541` | AC1 |
| Round report fake | A report at or above the floor, one below it, one out of order and one repeated | AC1, X4, X5 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2907; ASM-4805).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The asset reads and the round write on `/api/recovery/asset/v1`; the case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The round and payment facts are workflow signals |
| Temporal | 1 workflow, 1 activity owned, 2 consumed | `AssetDisposalWorkflow` and `reportAuctionRound` on `rwb-asset`; the payment and vendor-score activities on `rwb-payment` and `rwb-partner`; no Schedule |
| File | None | No file element; the publication of the listing is FEAT-AST-12's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.rounds`; front end `src/modules/recovery/asset/AuctionRounds.tsx`, the fragment SCR-24 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition here: the legacy `v_ace_payment` and `v_ace_score` reads leave the service for the P8 and S9 boundaries, and no `v_ace_*` grant is kept. DP-03 is the transaction rule of the round write, DP-13 moves the base, DP-19 is how the screens reach the service. The two boundary rows are built on documents and fakes on Day 1 (GAP-2907). The package in force is loaded through the service template without the DP-04 platform row (GAP-2910).

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` round branch | Workflow | Waits on the timer and the signals, loads the package in force, reports to the parent |
| `reportAuctionRound` | Activity | The one step: read, evaluate, write, answer |
| `RoundEvaluator` | Service | R-DIS-36, R-DIS-37 and R-DIS-40 on the round, the bid and the floor |
| `AwardCancellationEvaluator` | Service | R-DIS-49 and R-DIS-50 on the due date and the payment |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `RoundWriter` | Repository | `listing` and `asset_sale` in one transaction with the idempotency row and the lock |
| `CaseMoveAnswer`, `CaseStateClient`, `PaymentFactActivity`, `VendorScoreActivity` | Clients | The four answers and boundary calls, one hop, 2 s |
| `AuctionRoundController` | Controller | The round write and the reads, rights, key and the 400/401/403/404/409/422/503 map |
| `AuctionRounds` | React component | The rounds, the bids reported and the result on SCR-24, read only |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no bid table and no column added (GAP-2906).

**Configuration.** The price schedule, the floor and the re-list limit at their version (TSD S5 T3.2); the DISPOSAL package and version from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the round branch and its input record; (2) `RoundEvaluator` with the opening, the report and the below-floor paths (AC1, X3); (3) the round write with the round-number and status checks (AC1, X4); (4) the two boundary clients against their fakes for the payment and the score (AC2, X6, X7); (5) `AwardCancellationEvaluator` with R-DIS-49 and R-DIS-50 (AC2); (6) the record writer against the stub (AC3, X1); (7) `RoundWriter` with the idempotency row (AC1, X5); (8) `CaseMoveAnswer` (AC1, AC2); (9) `AuctionRoundController` with the rights and the error map (AC1, X2); (10) the screen fragment through the route fake; (11) the boundary test (X9, BR6, BR7).

**Feature flag.** `rwb.asset.auction-rounds-v1`; off means the report is held, nothing is written and no move is answered.

**Done when.** §16 passes, a reported round moves the case and records its outcome in SIT, a bid at or above the floor answers `SALE_AGREED`, an expired term answers `AWARD_CANCELED` and then `ROUND_OPEN`, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | A bid or a floor under the approver's limit on the round write (X3) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | An appraisal more than a year old when the round is opened (X6) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or signal is absent or invalid (X4) | Enter {field}. |
| MSG-P4-002 | A role without the right reports or reads (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the round changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five IDs are the legacy set, copied unchanged; no message is reworded and none is added.

### 15. Screens and states

SCR-24 Auction rounds (scheduled, open, result, settled; empty, loading, error and no access: Not specified in the source documents (CG-ALL-10031)) and SCR-21 Asset list (loading, list; empty, error and no access: Not specified in the source documents (CG-ALL-10030)) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, the listing, the round and its price, rwb-case for the state, rwb-payment for the term and rwb-partner for the vendor. This story fixes the rwb-asset answers only; the route and field list are RWB-PLT-N001-CON.

The states it produces are the round state of SCR-24 — round number, date, result, price, the sale it opened and the reopened round — and the refusal, not-recorded, wrong-state and stale-payment states with MSG-P4-002, MSG-P7-003, MSG-GEN-001 and MSG-S5-001. Scheduled and settled are the schedule and the sale stories'.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-024-01 | AC1 | Component | Case `RC-2026-000541` with a live listing and round 1; the report, the record, the round number and the case answer on the fakes |
| TC-E4-024-02 | AC2 | Integration | Case `RC-2026-000542` at `AWAITING_PAYMENT` with an expired term; cancellation, score, reopen and `AWARD_CANCELED` then `ROUND_OPEN` across the fakes |
| TC-E4-024-03 | AC3 | Component | Record stub stopped; nothing written, no sale record opened, MSG-P7-003 shown |
| TC-E4-024-04 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-024-05 | Principle 5 | Component | A forced record failure at the round write; no row, no answer, no event |
| TC-E4-024-06 | §12 operations, events and activities | Integration | Each consumed operation, published event and activity in §12 checked against its owner's published contract on the fakes |
| TC-E4-024-07 | §12.7 tables (ASM-3438) | Component | Each table in §12.7 written and read only inside `rwb_asset`; a read or write on any table not owned fails the boundary test (DP-01) |
| TC-E4-024-08 | AC4 | Integration | A statement reading a `v_ace_*` view, `recovery_case` or a foreign schema from `rwb_asset`; the grant refuses it and the boundary test fails the build |
| TC-E4-024-09 | AC5 | Integration | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC5) |
| TC-E4-024-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC6) |
| TC-E4-024-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC7) |
| TC-E4-024-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC10) |
| TC-E4-024-13 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC8) |
| TC-E4-024-14 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S5-E4024-APP-AC9) |

The five cases are the legacy cases in their order with the Level column added: TC-E4-024-02 runs `Integration` because it crosses three boundaries, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness, which carries the real payment and partner calls.

### 17. Guardrails

- No business value in code: the price schedule, the floor, the re-list limit and the statuses stay reference data or rule rows with a version. Reference-data contract DP-06 and DP-07; the parameter keys are Not specified in the source documents (DOR-RWB-S5-E4024-APP-20).
- No personal data in the schema, a workflow input or a log; a bidder is a vendor or buyer code and every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no data-lake export of a round.
- The record precedes the change and the repeated report is deduped (DP-03, BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| No requirement id for this slice | FEAT-AST-15 of FSD S5 A2.15 and the epic BRD row for FEAT-AST-15: the vendor runs each round and the bids come back into the case (GAP-2909; ASM-4807) | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | The round branch, the write, the answers | TC-E4-024-01 to -03 |
| ADR-013 | 19 services inside ACE | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | rwb-asset owns the round and the sale it opens | TC-E4-024-01 |
| ADR-014 | Schema and login per service | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | `rwb_asset` and its login | TC-E4-024-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | The durable timer and the signals; no Quartz row | TC-E4-024-01 |
| ADR-020 | Contract-first REST, one hop, 2 s | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | The consumed rows and the boundaries | TC-E4-024-01, -02, -06 |
| ADR-022 | Local decision record plus central ledger | FEAT-AST-15 | Not specified in the source documents (DOR-RWB-S5-E4024-APP-2) | The record before the change | TC-E4-024-03, -05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-024, Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word |
| Test cases | TC-E4-024-01 to TC-E4-024-05 |
| Feature and screens | FEAT-AST-15, SCR-24 and SCR-21 |
| Rules | R-DIS-36, R-DIS-37, R-DIS-40, R-DIS-49 and R-DIS-50, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The shape of the round write and the reads, the consumed rows, the record and rule-package elements, the error set and the fakes: RWB-S5-E4024-CON.
- The start price, the floor and the head of NPA's approval: FEAT-AST-11's story.
- The publication to HOME.SCB, the EASY app and the auction portal: FEAT-AST-12.
- The step down on a round with no bid and the re-list: FEAT-AST-13 and FEAT-AST-17's stories (R-DIS-38, R-DIS-39).
- The second signature of a bid below the floor: FEAT-AST-16's story (R-DIS-41, R-DIS-42).
- The five-day payment term, its reminder and the title transfer: FEAT-AST-18 to FEAT-AST-20's stories (R-DIS-47, R-DIS-48).
- The vendor allocation and the scorecard: FEAT-AST-14's story and rwb-partner (S9).
- The payment, its matching and its posting: rwb-payment (P8).
- The case, its states, the stage clock and the parent workflow: rwb-case (P3).
- The rule rows and the package version: rwb-decision (P7) (GAP-2910).
- The composite route and the field list: RWB-PLT-N001-CON and the edge stories.
- The real payment and partner calls and their evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this key.
