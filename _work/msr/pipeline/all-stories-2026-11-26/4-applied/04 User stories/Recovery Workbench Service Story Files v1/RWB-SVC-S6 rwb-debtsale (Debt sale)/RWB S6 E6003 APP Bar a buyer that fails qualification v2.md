# RWB-S6-E6003-APP Bar a buyer that fails qualification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6003-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-003 split out for rwb-debtsale. The four legacy acceptance criteria are kept word for word with their origin tag. The bar becomes the remediation branch of `DebtSaleWorkflow` on task queue `rwb-debtsale`: a durable timer holds the window of R-DS-40, `assessRemediation` re-opens the qualification check when the buyer supplies the missing KYC or licence evidence, `barBuyer` removes the buyer from the panel and releases the lot on a licence breach or on an expired window under R-DS-41, and the result is written to the local decision record with the rule version before any row changes (DP-03). The case move `BACK_TO_CASE_LIST` or `BUYER_PENDING_KYC` is answered to rwb-case, the panel change is requested from rwb-partner (S9), and the bar element is served read only on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). TSD S6 T-A publishes no bar operation of its own and the two legacy endpoint rows are the award path of RWB-S6-E6005-APP and the data room read of RWB-S6-E5026-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Head of Asset Liquidity**, I want **the Workbench to remove a buyer from the panel on a license breach and release the lot to the next bidder**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-003, the FEAT-DBS-07 step of the S6 Debt sale module. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the remediation and bar branch of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slides 3 and 13; Temporal and Drools Design slide 13);
- the durable window of R-DS-40, its 10-working-day target and its two outcomes: `assessRemediation` re-opens the qualification check under R-DS-40 and `barBuyer` bars the buyer under R-DS-41;
- the release of the lot in `rwb_debtsale`: the barred buyer's reference and class are cleared from `debt_sale_lot` and the lot status moves with the release (DF-SAL-025, DF-SAL-026, DF-SAL-030);
- the local decision record of the bar or the re-open, written through RWB-PLT-E1027-CON before any change (DP-03), which is what legacy AC1 and AC4 test;
- the request to rwb-partner (S9) to remove the buyer from the panel, and the read of the licence expiry, the KYC status and the panel status that decides it (DP-11);
- the answer to rwb-case for the moves `BACK_TO_CASE_LIST` and `BUYER_PENDING_KYC`, with the rule ID and the version that produced each move;
- the bar element served read only on `/api/recovery/debtsale/v1` (DP-13) for SCR-26 Award and PRT-05 Data room, through the gateway-bff composite route (DP-19).

It does not own: the published shape of the bar element, the buyer and release elements, the four consumed rows, the case-move answer, the error set and the fakes, which are RWB-S6-E6003-CON; the qualification of a buyer and its R-DS-14, R-DS-15 and R-DS-16 evaluation, which are RWB-S6-E6002-APP's, whose `qualifyBuyer` step receives the re-opened check and whose `BUYER_REJECTED` answer starts this window; the award operation API-S6-003 `POST /debt-sale-lots/{lotId}/award` and its `DecisionLogEntry` answer, which are RWB-S6-E6005-APP's, and the re-offer to the next qualified bidder under R-DS-28, which is that story's; the data room read API-S6-004 `GET /partner/data-room/{lotId}` and its `DataRoom` answer, which are RWB-S6-E5026-APP's; the bid operation API-S6-005, which is the take-bids story's; the buyer panel, its `panel_status` values, the partner users and the KYC and licence evidence, which are rwb-partner's (S9); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the central decision ledger and the rule rows, which are rwb-decision's (P7); the capability area, the rights and the scope, which are rwb-access's (P4); the notices of the sale, which are rwb-comms's (P6); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-003 gave the Workbench one step that removed a buyer from the panel on a licence breach and released the lot. The FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.7.1). The program keeps the requirement as REQ-S6-005, "A buyer who fails the check is given a remediation window and is removed from the panel if it is not met" (FSD S6 requirements served), and REQ-S6-004 for the check itself.

What D-RCV-60 changes is where each fact of the bar lives:

- **the panel is rwb-partner's (S9).** Architecture v5 slide 4 gives S9 "Partner management" and slide 13 gives rwb-partner the partner calls. The `panel_status`, the licence expiry and the KYC status of R-DS-40 and R-DS-41 are therefore facts of that service: this story reads them on its contract and **requests** the suspension there, and never writes a partner row. No operation name is published for the request, so the row carries the placeholder (GAP-2986; ASM-4921).
- **the case stays with rwb-case (P3).** `recovery_case` and the route states `BUYER_REJECTED`, `BUYER_PENDING_KYC` and `BACK_TO_CASE_LIST` are P3's; this story evaluates the rule and **answers** the move (GAP-2986; ASM-4920).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the lot release, which is what legacy AC1 asked for and what legacy AC4 tests.
- **the release splits from the re-offer.** R-DS-41 removes the buyer and releases the lot; R-DS-28 re-offers the lot to the next qualified bidder at the award. This story performs the removal, clears the barred buyer's hold and answers `BACK_TO_CASE_LIST`, and the selection of the next bidder is the award story's, so no bid ranking is invented here (GAP-2986; ASM-4924).
- **the window is a workflow timer**, not a scheduler job: R-DS-40 carries a 10-working-day target, the value is read from the rule package at its version, and Temporal holds the timer durably (DP-10 shape, no Schedule; ASM-4923).
- **the step claims no operation.** TSD S6 appendix T-A publishes five operations and none of them is a bar or panel operation; the two endpoint rows of the legacy story are the award path (API-S6-003) and the data room read (API-S6-004), which are the sibling stories' (GAP-2986; ASM-4922).
- **the wave is EP06's and the service is wave 3.** Template and Rules §R5.6 keeps the W-MAP wave, so this story is wave 4 while rwb-debtsale is created in wave 3; the conflict is recorded for the service and the business epic (GAP-2986; ASM-4926).

The metric is unchanged and no business value moves: the licence and KYC conditions, the `panel_status` values, the 10-working-day window, the `LOV-BUYER-CLASS` values and the lot status values are rule-row and reference-data values, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E6003-CON is published: the bar element and its answer shape, the buyer and release elements, the four consumed rows, the case-move answer, the error set and the fakes are baselined.
- RWB-S6-E6002-APP has answered `BUYER_REJECTED` with its rule ID and version, so the window has a start and the case is in the state R-DS-40 and R-DS-41 read. The two stories meet at the decision record and the case state only; neither reads the other's tables.
- The rwb-partner contract of the panel read and the panel suspension request is published with its fake. Its operation names are Not specified in the source documents (GAP-2986; ASM-4921), and the row is not in this story's contract-dependency list, which is None.
- The rwb-case case-state read and the case-move answer are available for the fake; the move is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2986; ASM-4920).
- The Debt sale rule package is in force at its version with R-DS-14, R-DS-16, R-DS-40 and R-DS-41; the package is authored, approved and versioned in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award and PRT-05 Data room reach this service through the gateway-bff composite route, one hop each (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_partner`, `rwb_case`, `rwb_decision` or `rwb_access` is refused by the database.
- No approval is needed to build against a Draft contract baseline; the baseline is tagged by RWB-S6-E6003-CON when its tests pass (ASM-4927).

### 4. Flow

1. rwb-case answers `BUYER_REJECTED` from the qualification step and this story's branch of `DebtSaleWorkflow` opens with the case, the lot, the buyer organisation and the rule ID with its version.
2. The branch starts the durable window of R-DS-40 from the decided-at time of the rejection record, at the package's 10-working-day target, and waits.
3. **Evidence arrives inside the window.** The buyer supplies the missing KYC or licence evidence, which is collected by rwb-partner and signalled here. `assessRemediation` evaluates R-DS-40, writes the decision record with the rule ID and version, answers rwb-case with `BUYER_PENDING_KYC`, and hands the case back to `qualifyBuyer` of RWB-S6-E6002-APP. R-DS-14 runs again there; this story writes no lot row on this path.
4. **The window expires, or a licence breach is reported.** The timer fires, or rwb-partner reports the breach. The branch reads the buyer organisation on the rwb-partner contract: the licence expiry, the KYC status and the `panel_status`.
5. `BuyerBarEvaluator` loads the Debt sale package version in force and evaluates R-DS-41: no evidence supplied inside the window, or the failure is a licence breach. Where neither condition holds, no rule fires, nothing changes and the branch waits for the window's end.
6. `BarDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case, the lot, the buyer, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `BarPanelClient` asks rwb-partner to remove the buyer from the panel, with the reason and the rule reference. rwb-partner applies the suspension to its own row and answers; this service writes no partner row and stores no personal data of the buyer (GAP-2986; ASM-4921).
8. `LotReleaseWriter` releases the lot in `rwb_debtsale` in the same transaction as the record: `buyer_partner_id` (DF-SAL-025) and `buyer_class` (DF-SAL-026) are cleared, `status` (DF-SAL-030, against `LOV-LOT-STATUS`) takes the release value, the idempotency row is written and the optimistic lock of `version` is applied. The source states no lot status value for a release after a bar, so the value carries the placeholder (GAP-2986; ASM-4924).
9. The step answers rwb-case with the move `BACK_TO_CASE_LIST`, the rule ID, the version and the decided-at time. rwb-case writes the case of record; this service writes none.
10. The answer to the partner channel withdraws the barred buyer's data room access on the same transaction boundary, and the lot is available to the re-offer of R-DS-28, which the award story runs.
11. A repeated timer fire, a repeated breach report or a repeated answer with the same lot, buyer and `Idempotency-Key` writes nothing, answers no second move and counts the repeat.
12. The bar element is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award and PRT-05 Data room through the gateway-bff composite route: the lot, the bar state, the rule ID with its version and the decided-at time, with no buyer personal data (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no release, no record, no panel request and no case-move answer | MSG-P7-003 | AC1, AC4, TC-E6-003-04, TC-E6-003-06 |
| X2 | The caller holds no Debt sale right on the lot, or the partner identity holds no Partner portal right on its own lot | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E6-003-05 |
| X3 | The case is not in `BUYER_REJECTED` | 409 and nothing is written; a bar is not re-evaluated on a case that has already moved | None | AC2 |
| X4 | The ACE data product of the case is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1, AC2 |
| X5 | The rwb-partner, rwb-case or rwb-access contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's schedule; nothing is written and no move is answered; the caller sees 503 with the platform envelope | None | AC1, AC2 |
| X6 | The buyer supplies the evidence inside the window | R-DS-40 fires instead of R-DS-41: the reason is recorded, the move is `BUYER_PENDING_KYC` and the case returns to the qualification step | None | AC2 |
| X7 | The window has not ended and no breach is reported | No rule fires: nothing changes, no record is written and the case keeps its state | None | AC1 |
| X8 | The rwb-partner panel request is refused, or the buyer is already suspended | The transaction rolls back; no release, no record and no move; the refusal is counted and alerted | None | AC1, AC2 |
| X9 | A component, a statement or a test reaches another service's schema, or a person field appears in an event, a log or a workflow input | The grant refuses the statement, the boundary test fails the build and nothing is released | None (pipeline log) | Section 17, BR5, BR9 |

X1 to X4 are the exception paths of RWB-E6-003 carried onto the split, X5 to X8 are the paths the target call types, the window and the partner channel add, and X9 is the DP-01 boundary. MSG-S6-001 is carried in section 14 and no path of this story raises it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6003-CON, the rwb-partner, rwb-case and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3, P4, P7 or S9 |
| Negotiable | The activity names, the decision code and the bar element's internal shape are this story's choice; the rules, the messages, the screens, the window target and the two tables are fixed |
| Valuable | A buyer that fails the check is removed from the panel and the lot is released, or the case is re-opened inside its window, and the case moves in the service that owns it |
| Estimable | One workflow branch, one durable timer, two activities, one evaluator, one record write, one lot update, one panel request, one case-move answer, three clients and one read-only element |
| Small | Finished inside two weeks with its tests on the fakes, with the time-skipping of the Temporal test server |
| Testable | Each criterion runs on synthetic lots and buyer organisations through the contract fakes, plus the timer, the refused panel request and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Bar a buyer that fails qualification

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the Debt sale rule package is in force at its version and carries R-DS-14, R-DS-16, R-DS-40 and R-DS-41
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Bar a buyer that fails qualification (legacy RWB-E6-003 AC1)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" with the licence expired and the panel status suspended
    Given the rwb-case contract mock returns the case state "BUYER_REJECTED" for "RC-2026-000842"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then removes a buyer from the panel on a license breach and releases the lot to the next bidder
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-41 (legacy RWB-E6-003 AC2)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" with no evidence supplied inside the window
    Given the rwb-case contract mock returns the case state "BUYER_REJECTED" for "RC-2026-000842"
    Given a case in state BUYER_REJECTED
    When buyer barred
    Then remove the buyer from the panel and release the lot to the next bidder
    Then the case moves to BACK_TO_CASE_LIST

  Scenario: AC3 Rule R-DS-14 (legacy RWB-E6-003 AC3)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" with the non-disclosure agreement signed
    Given the rwb-case contract mock returns the case state "DATA_ROOM_OPEN" for "RC-2026-000842"
    Given a case in state DATA_ROOM_OPEN
    When buyer requested access
    Then run the KYC, licensing and eligibility check on the bidder
    Then the case moves to BUYER_PENDING_KYC

  Scenario: AC4 Not recorded (legacy RWB-E6-003 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-003 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `buyer barred`, `buyer requested access`, `its trigger arrives` and the `license` spelling all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry their `Given the <service> contract mock returns <x>` lines, and those added lines are the only additions to the legacy text. Three notes are recorded rather than smoothed over. First, AC3's R-DS-14 is the same rule row that RWB-S6-E6002-APP owns and evaluates at the access request: the legacy story repeats it and both slices keep it, so the row is owned twice by design and the behaviour is built once, in the qualification step, while this story holds the row and the state it produces (GAP-2986; ASM-4920). Second, the bar of AC1 and AC2 is an answer and a request, never a write: the case move `BACK_TO_CASE_LIST` is answered to rwb-case and the panel removal is requested from rwb-partner, while the lot release is written here (BR3, BR4). Third, the legacy endpoint rows of the story are the award path and the data room read; TSD S6 T-A publishes no bar operation, the award path is API-S6-003 and RWB-S6-E6005-APP's and the data room read is API-S6-004 and RWB-S6-E5026-APP's, so this step runs behind them and claims no operation of its own (GAP-2986; ASM-4922). The buyer is a partner organisation and never a person: the fixtures carry no name, no identity number, no date of birth and no contact value, and the licence and KYC evidence is referenced, not copied.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-14 | Debt sale | D8.4 | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | nda_signed_at present | Run the KYC, licensing and eligibility check on the bidder | BUYER_PENDING_KYC | Workbench | Rules component, buyer portal | 3 working days |
| R-DS-16 | Debt sale | D8.4 | BUYER_PENDING_KYC | KYC_FAILED | kyc_status = failed or license expired or panel_status = suspended | Refuse access and record the reason | BUYER_REJECTED | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-40 | Debt sale | D8.4 | BUYER_REJECTED | BUYER_REMEDIATED | the buyer supplies the missing KYC or license evidence inside the window | Re-open the qualification check | BUYER_PENDING_KYC | Debt sale officer | Buyer portal, Workbench | 10 working days |
| R-DS-41 | Debt sale | D8.4 | BUYER_REJECTED | BUYER_BARRED | no evidence supplied inside the window, or the failure is a license breach | Remove the buyer from the panel and release the lot to the next bidder | BACK_TO_CASE_LIST | Head of Asset Liquidity | Buyer portal, Workbench | None |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character; their owner column is a role of the business and not a service. R-DS-16 is tabled because its answer is the `BUYER_REJECTED` state from which the window opens, and R-DS-14 because the legacy story carries it; the evaluation of both is the qualification step of RWB-S6-E6002-APP, and this story reads their outcome from the decision record and the case state. The case moves are written by rwb-case on this story's answer, the panel removal is applied by rwb-partner on this story's request, the lot row is written here, and the decision record is written here through DP-03 and centralised by rwb-decision (P7).

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot release is this service's: the buyer reference, the buyer class and the lot status are columns of `debt_sale_lot` in `rwb_debtsale`, and no other service writes them | Architecture v5 slide 4 (S6 Debt sale owns lots, data room, buyer terms, award, transfer); TSD S6 T3.1; GAP-2986 |
| BR2 | The decision is recorded before the lot row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy RWB-E6-003 AC1 and AC4 |
| BR3 | The panel and its `panel_status` stay with rwb-partner (S9): this story reads the licence, KYC and panel facts on the owner's contract and requests the suspension; it writes no partner row | Architecture v5 slides 4 and 13; GAP-2986 |
| BR4 | The case move is answered, not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Architecture v5 slides 3 and 13; GAP-2986 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the 10-working-day window, the licence and KYC conditions, the `panel_status` values, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-PUTBACK` | TSD S6 T3.2; FSD S6 BR-S6-007; legacy Guardrails |
| BR7 | This story declares no REST operation of its own: the branch runs behind API-S6-003 and API-S6-004 and the bar element is embedded in their answers | TSD S6 T-A.1; GAP-2986 |
| BR8 | The window is a durable workflow timer read from the package; the story registers no Schedule and no Quartz job | DP-10 shape; R-DS-40 timer; TSD S6 T2 ("Jobs") |
| BR9 | No person name, identity number, date of birth, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log or a workflow input; the buyer is an organisation | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR10 | The same timer fire, breach report or answer with the same `Idempotency-Key` writes once, answers the move once and counts the repeat | TSD S6 T-A.2; Architecture v5 slide 11 |

### 9. State transitions

The case route state is rwb-case's and this story answers it rather than writing it (BR4). What this story owns is the remediation state of the lot and the state of the step.

| From (remediation of the lot) | Event | Condition | To |
|---|---|---|---|
| Rejected | Evidence arrives inside the window | R-DS-40: the missing KYC or licence evidence is supplied | Re-opened, with the case-move answer `BUYER_PENDING_KYC` |
| Rejected | The window ends with no evidence | R-DS-41: no evidence supplied inside the window | Barred, with the case-move answer `BACK_TO_CASE_LIST` |
| Rejected | A licence breach is reported | R-DS-41: the failure is a license breach | Barred, with the case-move answer `BACK_TO_CASE_LIST`, without waiting for the window |
| Rejected | Any other event | Neither R-DS-40 nor R-DS-41 fires | Unchanged, no record and no answer |
| Barred | Any repeated report or timer fire | BR10 | Unchanged, the repeat is counted |
| Barred | The lot is re-offered to the next qualified bidder | R-DS-28, the award story RWB-S6-E6005-APP | Not this story: re-offered there |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The `BUYER_REJECTED` answer arrives | The package in force is loaded | Window open |
| Window open | Evidence, the timer or a breach report arrives | A rule fires and the record is written | Applying |
| Applying | The panel request and the lot release commit and the move is answered | The transaction commits | Waiting, or closed when the buyer is barred |
| Applying | The record write, the panel request or the transaction fails | X1, X8 | Window open, nothing changed |
| Window open | The rwb-partner or rwb-case answer is stale or absent | X4, X5 | Held, until a fresh answer |

The route states `DATA_ROOM_OPEN`, `BUYER_PENDING_KYC`, `BUYER_REJECTED` and `BACK_TO_CASE_LIST` are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria, and they live on the case of record. The lot status values are those of `LOV-LOT-STATUS`; the value taken at the release is Not specified in the source documents (GAP-2986; ASM-4924).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA in TSD S6 T6.1 and the owner role of R-DS-41: reads the bar, holds the approval authority of the sale, and sees the released lot on SCR-26 Award |
| RW-DEBTSALE, debt sale officer | Debt sale CRUA: reads the bar element, works the remediation window and reads the released lot; the officer does not bar (R-DS-41's owner is the Head of Asset Liquidity) |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the bar element and the released lot |
| PT-BUYER, debt buyer and AMC | Partner portal RU, own lots only and scoped: sees its own pending and barred states and supplies the missing evidence through rwb-partner; sees no other buyer's state |
| PT-RAMC | Partner portal R: reads its own lots and their state |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the branch, evaluates the rules, writes the record and the lot release, requests the panel change, answers the case move and serves the bar element; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard is a service-template capability, so the check is stated here and not built here (GAP-2986; ASM-4920).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the release is recorded against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the bar element |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Not written here |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Not written here: the award story owns it |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Write, cleared on the release of R-DS-41 |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Write, cleared on the release, against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Not written here |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, against `LOV-LOT-STATUS`; the release value is Not specified in the source documents (GAP-2986; ASM-4924) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the account set of the lot the release returns to the case list |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case move, decided at | Write through the local library, before the lot row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state arrives on the rwb-case contract and the move is answered to it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rows arrive in the package in force |
| DF-REF-034 to DF-REF-038 | role (P4) | id, role_code, role_name, role_class, default_scope | Not read as a table: the capability area and the right are answered by rwb-access |
| The buyer organisation | partner and partner_user (S9) | partner reference, licence expiry, kyc_status, panel_status, buyer class | Not read as a table: the facts arrive on the rwb-partner contract, and the suspension is requested there (GAP-2986; ASM-4921) |

Field IDs are those of the TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v9. The four rows of the legacy Data table, `recovery_case`, `decision_log_entry`, `rule_row` and `role`, are the rows of other owners in the target and are consumed on their contracts. **No new table, no new column and no migration**: this story writes three existing lot columns, reads the rest, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03).

The `panel_status` vocabulary is published by no source: the condition of R-DS-16 names the value `suspended` and R-DS-15 the value `active`, and the full list is Not specified in the source documents (GAP-2986; ASM-4921). **No personal data**: the rows this story writes carry identifiers, codes, dates and a rule version; the buyer is a partner organisation, so no name, identity number, date of birth, address or contact value enters the schema, the record, a log or a workflow input, and the fixtures are synthetic.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids`, and none of them is a bar, remediation or panel operation. The two endpoint rows of the legacy story are the award path (API-S6-003) and the data room read (API-S6-004), which belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP; API-S6-005 belongs to the take-bids story of this service. This story provides no operation, claims no sibling's operation and runs behind them, and the absence is recorded as GAP-2986 with ASM-4922.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the buyer's licence, KYC and panel facts (operation name Not specified in the source documents (GAP-2986; ASM-4921)) | `/api/recovery/partner/v1` | S9 rwb-partner | The licence expiry, `kyc_status`, `panel_status` and `LOV-BUYER-CLASS` value of the buyer; read only, faked |
| The panel suspension request (operation name Not specified in the source documents (GAP-2986; ASM-4921)) | `/api/recovery/partner/v1` | S9 rwb-partner | The removal of the buyer from the panel with the reason and the rule reference; the partner applies it to its own row; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the lot link; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2986; ASM-4920)) | rwb-case (P3) | P3 rwb-case | The move `BACK_TO_CASE_LIST` or `BUYER_PENDING_KYC` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-2986; ASM-4920)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Debt sale" and "Partner portal", the right of the caller and the scope of its own lot; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-14, R-DS-16, R-DS-40 and R-DS-41; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2986 with ASM-4920.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23) and `AccountsTransferred`, and neither is produced here: `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. This story writes no outbox row, opens no producer and declares no event of its own; the bar and the re-open reach rwb-case on the move answer and the partner on the read of the bar state (ASM-4925).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched`, which is the remittance step's and belongs to RWB-S6-E6011-APP, and no event of the module carries a breach report, a piece of evidence or a window expiry. This story therefore holds no consumer group, no subscription and no inbox row of its own (ASM-4925).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the case, the buyer reference and the package in force; signals: evidence, a breach report and the case state; the remediation branch holds the durable window of R-DS-40 |
| `assessRemediation` | Activity, the R-DS-40 outcome | `rwb-debtsale` | The case, the lot and the evidence in; the rule ID with its version, the record and the `BUYER_PENDING_KYC` answer out, with no lot change |
| `barBuyer` | Activity, the R-DS-41 outcome | `rwb-debtsale` | The case, the lot and the buyer in; the rule ID with its version, the record, the panel request, the lot release and the `BACK_TO_CASE_LIST` answer out, in one transaction |

No child workflow for the case and no workflow for the money exists in this service. The two activity names are target design choices fixed by no source document; the trigger is read as the window timer and the breach report for a lot, because the FSD says the step runs unattended ("None; runs unattended" is the primary role of FSD S6 A2.7.3.3) while declaring no background event (FSD S6 A2.7.4.4). The qualification step that receives the re-opened check is `qualifyBuyer` of RWB-S6-E6002-APP, and the re-offer of the lot is the award story's.

#### 12.6 Schedules

None. The window is a durable workflow timer inside `DebtSaleWorkflow`, not a Temporal Schedule and not a legacy Quartz job: this story registers no Schedule, no `JOB-nn` row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here (ASM-4923).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class and its status; the release of §11 |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot; read only here |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated timer fire, report or answer |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this step writes no row to it (ASM-4925) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `partner`, `partner_user` and the licence or KYC evidence (S9), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_lot.buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel and buyer fake | The organisation `PTR-2026-000031` with an expired licence and the panel status suspended; the same organisation with a licence in date and the panel status active; the same organisation with no evidence inside the window and the same organisation with evidence inside it; a refused suspension; no answer beyond 2 s | AC1, AC2, X5, X6, X8 |
| rwb-case case-state fake | The states `BUYER_REJECTED`, `DATA_ROOM_OPEN` and `BUYER_PENDING_KYC` of case `RC-2026-000842`; a case that is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `BACK_TO_CASE_LIST` and `BUYER_PENDING_KYC` accepted; a move refused because the case has already moved | AC2, AC3, X3 |
| rwb-access authorise fake | The capability area "Debt sale" with right C, R, U or A and the capability area "Partner portal" with right R or U for `PT-BUYER`, scoped to its own lot; a role and a partner identity without the right | AC1, X2 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-14, R-DS-16, R-DS-40 and R-DS-41 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| Temporal test server with time skipping | The 10-working-day window advanced without waiting, and a window that has not ended | AC1, AC2, X7 |
| gateway-bff composite route fake | The merged SCR-26 Award and PRT-05 Data room answer for lot `LOT-2026-000042` and case `RC-2026-000842`, with the bar element read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner panel read and suspension request, the rwb-case move answer and the rwb-access authorise call are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2986; ASM-4920).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-partner panel read and suspension request, the rwb-case state read and move answer, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the remittance story's |
| Temporal | 1 workflow and 2 activities | `DebtSaleWorkflow` with `assessRemediation` and `barBuyer` on `rwb-debtsale`, and one durable timer; no Schedule |
| File | None | No file is read, built or delivered here; the buyer evidence is collected by rwb-partner and the sale documents are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `buyerbar`, Java package `th.co.scb.ace.workbench.recovery.debtsale.buyerbar`; front end `src/modules/recovery/debtsale/BuyerBar.tsx`, the fragment SCR-26 Award and PRT-05 Data room embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the panel request and the lot release commit together or not at all. DP-13 moves the base of the bar element and nothing else. DP-19 is how SCR-26 Award and the data room reach this service, one hop through the gateway, and it is also the boundary of the partner channel.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story while the plan's C row is None, so the story builds against their documents and fakes on Day 1 (GAP-2986; ASM-4920). DP-08 is not in the pattern set although the step calls rwb-access, and DP-09 is not in it although the library object `outbox_event` exists in the schema, so neither is added to the metadata rows and both are named in the text (ASM-4925).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` remediation branch | Workflow | Waits for the rejection, the evidence, the breach report and the window, loads the package and reports the outcome to the parent |
| `assessRemediation` | Activity | Evaluates R-DS-40, writes the record, answers `BUYER_PENDING_KYC` and hands the case back to `qualifyBuyer` |
| `barBuyer` | Activity | Evaluates R-DS-41, writes the record, requests the panel change, releases the lot and answers `BACK_TO_CASE_LIST` |
| `RemediationWindowTimer` | Timer | The durable window at the package's 10-working-day target, started from the rejection's decided-at time |
| `BuyerBarEvaluator` | Service | The rule evaluation against the package in force, with the licence and panel values of the closed lists |
| `BarDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LotReleaseWriter` | Repository | Clears the buyer reference and class, sets the lot status, writes the idempotency row and applies the optimistic lock in one `rwb_debtsale` transaction |
| `PartnerPanelClient` | Client | The panel read and the suspension request of rwb-partner (S9), one hop, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `BarElementController` | Controller | The read of the bar element on the service base, the capability area and right, and the problem mapping of 400, 401, 403, 404, 422 and 503; it declares no operation that TSD S6 T-A does not publish |
| `BuyerBar` | React component | Shows the remediation, barred and released states on SCR-26 Award and PRT-05 Data room, read only |

**Database and migrations.** No Flyway file of this story. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service and the library objects come with the library's migration (DP-03); the release value of the lot status is a reference value and no column is added (GAP-2986; ASM-4924).

**Configuration and reference data.**

- `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package at its version, with the 10-working-day target of R-DS-40 and the licence, KYC and panel conditions, authored and approved in rwb-decision (P7).
- The capability areas "Debt sale" and "Partner portal" and their rights are access rows of rwb-access, read through the guard.
- The `panel_status` list and the two values the rules name are the partner's reference data; the full list carries the placeholder (GAP-2986; ASM-4921).

**Build steps**

1. The remediation branch of `DebtSaleWorkflow` with its input record and its window, registered on `rwb-debtsale` as the stage child of `CaseWorkflow` (AC1, AC2).
2. `PartnerPanelClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker, the refused request and the no-answer path (AC1, AC2, X5, X8).
3. `AccessGuardClient` and the two capability areas, with the refusal path (AC1, X2).
4. `BuyerBarEvaluator` over the package, with R-DS-40 and R-DS-41, the licence and panel conditions and the no-fire path (AC1, AC2, X6, X7).
5. `BarDecisionRecordWriter` against the library stub, with the failed-write path (AC1, AC4, X1).
6. `LotReleaseWriter` with one transaction, the three columns, the idempotency row and the optimistic lock (AC2).
7. The case-move answer and the parent signal, with the two moves (AC2, AC3).
8. `BarElementController` with the rights and the problem mapping, declaring no unpublished operation (AC1).
9. `BuyerBar` and the two screen fragments through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_debtsale`, no read of `partner`, `recovery_case`, `role` or `rule_row`, and no person field in a log, an event or a workflow input (X9, BR5, BR9).

**Feature flag.** `rwb.debtsale.buyer-bar-v1`, read as a flag of the platform library; off means the window opens and holds, nothing is written and no move is answered, and the qualification and award stories are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic rejection in SIT, each of the two rules produces its record, its lot change or hand-back and its move, the window advances under time skipping, a repeated fire writes once, a forced record failure or a refused panel request changes nothing, and SCR-26 Award and PRT-05 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the case, the lot or the buyer answer is absent or invalid (X3, X7) | Enter {field}. |
| MSG-P4-002 | A role or a partner identity without the right of the capability area reads the bar or acts on the lot (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot is released (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the case is stale after a late or failed batch (X4, VR-S6-007-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five message IDs are those of the legacy message set and of FSD S6 A2.7.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

SCR-26 Award in its open, closed, awarded and transferred states is served through the gateway-bff composite route (DP-19), and PRT-05 Data room, "lot data tapes and documents for admitted buyers, with bids" (FSD S6 Screens), is served to the partner on the same service base, scoped to its own lot. The route calls rwb-debtsale for the lot and the bar element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this story fixes the bar element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces on the element are the remediation, barred and released states of §9, with the rule version, and the one it shows besides is refused with MSG-P4-002, not recorded with MSG-P7-003, and stale data with MSG-P1-001. The award, settlement and transfer states of SCR-26 belong to the award, settlement and transfer stories of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-003-01 | AC1 | Component | The buyer organisation `PTR-2026-000031` with an expired licence on lot `LOT-2026-000042`; the record, the panel request, the release and the case move asserted on the fakes |
| TC-E6-003-02 | AC2 | Component | Case `RC-2026-000842` at `BUYER_REJECTED` with the window expired and no evidence; R-DS-41 evaluated and `BACK_TO_CASE_LIST` answered |
| TC-E6-003-03 | AC3 | Integration | Case `RC-2026-000842` at `DATA_ROOM_OPEN` with the NDA signed; R-DS-14 evaluated through the qualification step and `BUYER_PENDING_KYC` answered end to end on the fakes |
| TC-E6-003-04 | AC4 | Component | The decision-record stub stopped; nothing written, no release and MSG-P7-003 shown |
| TC-E6-003-05 | Access | Component | A role and a partner identity without the Debt sale or the Partner portal right; 403 with MSG-P4-002 and no read |
| TC-E6-003-06 | Principle 5 | Component | A forced decision log write failure at the moment of the release; no lot change, no panel request, no answer and no second attempt |

The six legacy cases are the legacy cases of RWB-E6-003 in their legacy order, with the Level column added: the component cases run on the fakes and TC-E6-003-03 maps to `Integration` because it crosses the rwb-partner and rwb-case boundaries through the qualification step. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and no `-ITG` copy is written here.

### 17. Guardrails

- No business value in code: the 10-working-day window, the licence and panel conditions, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, dates and a rule version only, and every fixture is synthetic. The buyer is a partner organisation, and the licence and KYC evidence is a reference of its owners.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test.
- The case stays with rwb-case, the panel with rwb-partner, the access with rwb-access and the ledger with rwb-decision: no `recovery_case` row, no `partner` row, no role row and no `decision_log_entry` row is written here (BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: the award path is RWB-S6-E6005-APP's and the data room read is RWB-S6-E5026-APP's, and a story that declares them as its own fails the review (GAP-2986; ASM-4922).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base, no second event on the topic, and no Schedule for the window (ASM-4923).
- The decision is recorded before the change and the move is answered, not written; a build that writes a case row or records after the release fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met (FSD S6 requirements served); the split plan carries no requirement id for this slice (GAP-2986; ASM-4920) | The window of R-DS-40, `assessRemediation`, `barBuyer`, the panel request and the lot release | TC-E6-003-01, TC-E6-003-02, TC-E6-003-04 |
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid; this story holds R-DS-14 and its `BUYER_PENDING_KYC` state while the check itself is the qualification story's | The R-DS-14 row, the re-opened check and the `BUYER_PENDING_KYC` answer | TC-E6-003-03 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot release | TC-E6-003-02 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-003-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E6-003-01, TC-E6-003-03 |
| ADR-022 | Local decision record plus central ledger | The record written before the lot release | TC-E6-003-04, TC-E6-003-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-003, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-003-01 to TC-E6-003-06 |
| Feature and screens | FEAT-DBS-07 Bar a buyer that fails qualification, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-14, R-DS-16, R-DS-40 and R-DS-41, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the bar element, the buyer and release elements, the closed lists, the consumed rows, the case-move answer, the error set and the fakes: RWB-S6-E6003-CON.
- The qualification of a buyer, R-DS-14, R-DS-15, R-DS-16 and R-DS-18 and the `qualifyBuyer` step that receives the re-opened check: RWB-S6-E6002-APP.
- The award operation API-S6-003, its `DecisionLogEntry` answer and the re-offer to the next qualified bidder under R-DS-28: RWB-S6-E6005-APP (GAP-2986; ASM-4924).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP.
- The bid submission operation API-S6-005 and the bidding window: the take-bids story of this service.
- The buyer panel, its `panel_status` values, the partner users and the licence and KYC evidence: rwb-partner (S9) (GAP-2986; ASM-4921).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4).
- The central decision ledger, the rule rows, their approval and their versioning: rwb-decision (P7).
- The sale agreement and the customer notices: rwb-document (P5) and rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-26 and PRT-05: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
