# RWB-S5-E4027-APP Enforce the five-day payment term

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4027-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-027 for rwb-asset. The four legacy criteria are kept word for word with their origin tag and the six legacy test cases keep their IDs. The payment term becomes the payment branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it starts the five-day term at the award (R-DIS-47), confirms the sale on the payment fact and starts the title transfer (R-DIS-48), raises the expiry signal that releases the asset (R-DIS-49 and R-DIS-50 stay the rounds story's), evaluates R-DIS-11 and R-DIS-37 exactly as AC2 and AC3 name them, records each outcome before the row changes (DP-03), answers `AWAITING_PAYMENT` and `TITLE_TRANSFER_PENDING` to rwb-case, and consumes the rwb-payment fact and event (DP-05). The base becomes `/api/recovery/asset/v1` (DP-13) and SCR-22 and SCR-24 read through the gateway-bff route (DP-19). Gaps: no element holds the award, the due date, the received-at time, the buyer or the term (GAP-2925; ASM-4822); the term rules sit across this story and RWB-S5-E4024-APP (GAP-2926; ASM-4823); AC2 and AC3 name rules of other features (GAP-2927; ASM-4824); no requirement row names the term (GAP-2928; ASM-4825); the consumed rows and the payment event carry no published name (GAP-2929; ASM-4826); DP-04 is outside the pattern set (GAP-2930; ASM-4827). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4027-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to track the winning bidder's payment against the term and release the asset if it is missed**, so that **assets sell sooner at approved prices** (legacy RWB-E4-027, word for word).

This is the application slice of legacy RWB-E4-027. It owns:

- the four legacy criteria with their origin tag, and the rules, messages and screens they depend on;
- the payment-term branch of `AssetDisposalWorkflow` on `rwb-asset`, a child of the case workflow (Architecture v5 slide 13);
- the start of the five-calendar-day term at the award (R-DIS-47) and the durable timer that measures it;
- the confirmation of the sale on the payment fact and the start of the title transfer (R-DIS-48), with the term status the asset record shows;
- the expiry signal that releases the asset to the rounds story: the award cancellation, the vendor score and the reopened round (R-DIS-49, R-DIS-50) are RWB-S5-E4024-APP's steps (GAP-2926; ASM-4823);
- R-DIS-11 and R-DIS-37 exactly as AC2 and AC3 state them, on the DISPOSAL package in force (GAP-2927; ASM-4824);
- the decision record of each outcome before the row changes (DP-03) and the case answers `AWAITING_PAYMENT` and `TITLE_TRANSFER_PENDING`;
- the consumption of the rwb-payment payment fact and payment event, in place of the legacy `v_ace_payment` read (DP-05) (GAP-2929; ASM-4826);
- the reads of SCR-22 Asset record and SCR-21 Asset list on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shapes of the reads, the consumed rows and the fakes, which are RWB-S5-E4027-CON; the acceptance of the bid and the agreed sale, which are FEAT-AST-16's story and RWB-S5-E4024; the award cancellation, the vendor score and the reopened round (R-DIS-49, R-DIS-50); the transfer of the vehicle registration and the Land Office transfer, which are FEAT-AST-19 and FEAT-AST-20's stories (R-DIS-51 to R-DIS-53); the proceeds and the shortfall, FEAT-AST-21; the case and its states, rwb-case (P3); the payment, its matching and its posting, rwb-payment (P8); the vendor scorecard, rwb-partner (S9); the rule package, rwb-decision (P7); the composite route, RWB-PLT-N001-CON; the deployment, which is the operations story of this key.

### 2. Business rationale

Legacy RWB-E4-027 watched the winning bidder's payment after a sale was agreed: the buyer paid inside the term, or the asset was put back on the market. The NPA sales cycle it serves is measured in years and the FSD keeps the behaviour as FEAT-AST-18 in module S5, run unattended on the auction portals, ALS and the general ledger, after the sale is agreed and before the title transfer (FSD S5 A2.18; REQ-S5-001 to REQ-S5-010 name no term) (GAP-2928; ASM-4825).

What D-RCV-60 changes:

- **the clock is Temporal's.** The five calendar days are a durable timer inside `AssetDisposalWorkflow`, not a Quartz job and not a database scan; the timer survives a restart and the workflow continues as new at each stage end (ADR-016).
- **the payment is rwb-payment's (P8).** The legacy `v_ace_payment` and `v_ace_npa_sale` reads leave the service (DP-05): the term records the due date when the award is made, and the payment arrives as the owner's fact and event with a freshness stamp. Only rwb-source-data reads the `recovery.v_ace_*` views (Architecture v5 slide 8).
- **the case stays with rwb-case (P3).** The rules decide and this story **answers** the move; it writes no case row.
- **the decision is recorded first**, one per outcome, in the transaction that changes the sale record — what AC1 asked and AC4 tested.
- **the release is one signal.** The expiry is detected here and executed by RWB-S5-E4024-APP, so no rule row is evaluated twice (GAP-2926; ASM-4823).
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's and the sale event is the sale stories' (TSD S5 T5.3); §12.3 states the absence and a build that publishes fails it.

### 3. Preconditions

- RWB-S5-E4027-CON tagged: the asset reads, the four consumed rows, the decision-record and rule-package elements, the error set and the fakes.
- `asset_sale`, `listing` and `asset` exist in `rwb_asset` with the TSD S5 T3.1 and T3.0 columns; no column holds the award, the due date, the received-at time, the buyer or the term, and none is added (GAP-2925; ASM-4822).
- The DISPOSAL package is in force with R-DIS-11, R-DIS-37, R-DIS-47 and R-DIS-48 from rwb-decision (P7), loaded through the service template; DP-04 is outside the pattern set (GAP-2930; ASM-4827).
- The term length, the reminder point and the `LOV-HOLDING` and `LOV-LISTING` lists are reference data with their version (TSD S5 T3.2).
- The rwb-case state read and the case-move answers sit behind fakes; their names are not published (GAP-2929; ASM-4826).
- The rwb-payment payment fact activity and the rwb-payment event row are published with a fake, a freshness stamp and a correlation key; their names are not published (GAP-2929).
- The award and the payment-term expiry arrive as signals of `AssetDisposalWorkflow`; the award is raised by the sale step of RWB-S5-E4024 (GAP-2926).
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the two screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass.

### 4. Flow

1. The sale of asset `AST-2026-000527` is agreed and the award is made; the sale step signals `AssetDisposalWorkflow` with case, asset, listing, sale record and buyer code.
2. The workflow confirms the case state on the rwb-case contract: `SALE_AGREED`.
3. `PaymentTermEvaluator` loads the package in force and evaluates R-DIS-47: from `SALE_AGREED`, on `AWARD_MADE`, the five-day payment term starts and the case moves to `AWAITING_PAYMENT`.
4. The due date is computed from the award date and the term length in reference data, five calendar days; where no column holds it the value is Not specified in the source documents and is held against the sale record (GAP-2925; ASM-4822).
5. `AssetDecisionRecordWriter` writes one record **before any change**, with the rule and the package version; a failed write stops the step (DP-03; AC1, AC4).
6. `SaleTermWriter` writes the award, the due date and the holding status on the sale record and the asset in one transaction with the record and the idempotency row; the asset is shown as under offer while the term runs.
7. `CaseMoveAnswer` answers `AWAITING_PAYMENT` with the sale reference, the due date, the rule and its version; rwb-case writes the case.
8. A durable timer runs to the due date. When the payment fact arrives through R-DIS-48 — `payment_received_at` at or before `payment_due_date` — the sale is confirmed, the title transfer is started, one record is written and the answer carries `TITLE_TRANSFER_PENDING` (X6).
9. Where the timer fires and the payment fact is absent or shows no payment, the expiry is detected and the case answer carries `PAYMENT_TERM_EXPIRED`; the award cancellation, the vendor score and the reopened round are RWB-S5-E4024-APP's steps (GAP-2926; ASM-4823).
10. AC2's rule R-DIS-11 is evaluated on the same package: from `WORK_ORDER_OPEN`, on `WORK_ACCEPTED` with `sale_officer_accepted = Y`, the invoice is released for payment and the asset returns to hold, and the case moves to `ASSET_HELD`.
11. AC3's rule R-DIS-37 is evaluated on the bid event: from `ROUND_OPEN`, on `BID_PLACED`, the bid is recorded against the round and the asset and the case moves to `BID_RECEIVED`; the rounds story owns the behaviour and this story keeps the state gate the criterion names.
12. A repeated signal, fact or `Idempotency-Key` writes once and is counted; the workflow returns to its durable timer and continues as new at each stage end and at least every 28 days.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered, the term not started | MSG-P7-003 | AC4, TC-E4-027-04, -06 |
| X2 | The role lacks the Asset and disposal right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-027-05 |
| X3 | The case is in another state, or the payment fact arrives after the timer fired | The rule does not fire; nothing written, the state reported | None | AC2, AC3 |
| X4 | A required field of the award signal is absent or invalid | The term does not start; the signal is counted and shown | MSG-GEN-001 | AC1 |
| X5 | The same signal, fact or key arrives twice | One term, one record, one answer | None | AC1 |
| X6 | The payment fact is stale at the due date | The confirmation is held until the fact is fresh; the data date is shown | MSG-P1-001 | AC1 |
| X7 | The payment event and the payment fact disagree | The fact wins, the event is held for replay and the difference is flagged | None | AC1 |
| X8 | A contract misses 2 s or its breaker is open | Retry on the workflow schedule; 503 in the platform envelope | None | AC1, AC3 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR6 |

X1 to X3 are the legacy paths on the split, X4 to X8 what the term clock, the payment fact and the boundaries add, and X9 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and its fakes; no live P1, P3, P8, S9 or P7 |
| Negotiable | Activity name, decision code and outcome shape are ours; rules, messages, screens, rows and reads are fixed |
| Valuable | A sale is paid or released inside five calendar days without a manual chase or a database scan |
| Estimable | One branch, two evaluators, one record per outcome, two row changes, two answers, three clients, one screen fragment |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, wrong-state, stale-payment, disagreement and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Enforce the five-day payment term

  Background:
    Given case "RC-2026-000527" holds asset "AST-2026-000527" in listing "LS-2026-000527" with sale "SL-2026-000527"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-11, R-DIS-37, R-DIS-47 and R-DIS-48
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Enforce the five-day payment term (legacy RWB-E4-027 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000527" in state SALE_AGREED with the sale "SL-2026-000527" agreed
    Given the rwb-payment contract mock returns no payment yet for "RC-2026-000527" and its due date five calendar days after the award
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tracks the winning bidder's payment against the term and releases the asset if it is missed
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-11 (legacy RWB-E4-027 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000528" in state WORK_ORDER_OPEN
    Given a case in state WORK_ORDER_OPEN
    When work accepted
    Then release the invoice for payment and return the asset to hold
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-37 (legacy RWB-E4-027 AC3)
    Given the rwb-case contract mock returns the case "RC-2026-000529" in state ROUND_OPEN
    Given a case in state ROUND_OPEN
    When bid placed
    Then record the bid against the round and the asset
    Then the case moves to BID_RECEIVED

  Scenario: AC4 Not recorded (legacy RWB-E4-027 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `the action is taken`, `its trigger arrives` and `the decision log cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-case writes the four moves, rwb-payment answers the fact, and this story starts the term, confirms the payment, detects the expiry, writes the sale record, records and answers. AC1's release is executed by RWB-S5-E4024-APP on this story's expiry signal (GAP-2926). AC2 and AC3 are kept because the legacy story and FSD S5 A2.18 carry R-DIS-11 and R-DIS-37, though both are rules of other features (GAP-2927; ASM-4824).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-11 | Asset disposal | D8.1 to D8.3 | WORK_ORDER_OPEN | WORK_ACCEPTED | sale_officer_accepted = Y | Release the invoice for payment and return the asset to hold | ASSET_HELD | Sale officer | Partner Portal, ALS core and GL | 3 working days |
| R-DIS-37 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | BID_PLACED | Any | Record the bid against the round and the asset | BID_RECEIVED | Workbench | auction portal | None |
| R-DIS-47 | Asset disposal | D8.1 to D8.3 | SALE_AGREED | AWARD_MADE | Any | Start the five-day payment term | AWAITING_PAYMENT | Buyer | auction portal, ALS core and GL | 5 calendar days |
| R-DIS-48 | Asset disposal | D8.1 to D8.3 | AWAITING_PAYMENT | PAYMENT_RECEIVED | payment_received_at at or before payment_due_date | Confirm the sale and start the title transfer | TITLE_TRANSFER_PENDING | Sale officer | ALS core and GL | None |

The four rows are copied character for character from the Business Rules and Routing Logic v4; their owner column is a business role, so the case stays in these states and moves in rwb-case on this story's answer, while the sale record and the holding status are written here. R-DIS-49 and R-DIS-50 (the cancellation and the reopened round) are RWB-S5-E4024-APP's and are not evaluated here (GAP-2926; ASM-4823). R-DIS-11 and R-DIS-37 are declared once for the service (GAP-2927; ASM-4824).

| ID | Rule | Source |
|---|---|---|
| BR1 | The term is this service's: the award, its due date and the received-at time are held against `asset_sale` in `rwb_asset`, and the term length is versioned reference data | Ownership Map; TSD S5 T3.1; GAP-2925 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version; a failed write changes nothing | DP-03; AC1, AC4 |
| BR3 | The term length, the reminder point, the holding statuses and the listing statuses are rule rows or reference data with a version, never a constant | TSD S5 T3.2; legacy Guardrails |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2929 |
| BR5 | The payment fact and the payment event are rwb-payment's; no `v_ace_payment` read and no `v_ace_npa_sale` read here | DP-05; Architecture v5 slide 8 |
| BR6 | The expiry is one signal: the cancellation, the vendor score and the reopened round are RWB-S5-E4024-APP's and no rule row is evaluated twice | Business Rules and Routing Logic v4 R-DIS-49, R-DIS-50; GAP-2926 |
| BR7 | No event is published; EV-22 `AssetTakenOn` is the take-on story's and the sale event is the sale stories' | TSD S5 T5.3 |
| BR8 | A repeated signal, fact or key writes once, answers once and is counted | TSD S5 T-A.2 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR10 | No personal data in the schema, a record, a log or a workflow input; a buyer is a code, never a person | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (case state) | Event | Condition | To |
|---|---|---|---|
| SALE_AGREED | `AWARD_MADE` under R-DIS-47 | Any award of the agreed sale | AWAITING_PAYMENT, answer `AWAITING_PAYMENT` |
| AWAITING_PAYMENT | `PAYMENT_RECEIVED` under R-DIS-48 | `payment_received_at` at or before `payment_due_date` | TITLE_TRANSFER_PENDING, answer `TITLE_TRANSFER_PENDING` |
| AWAITING_PAYMENT | `PAYMENT_TERM_EXPIRED` under R-DIS-49 | Payment absent and the due date passed | AWARD_CANCELED, raised as the expiry signal (RWB-S5-E4024-APP writes the move) |
| WORK_ORDER_OPEN | `WORK_ACCEPTED` under R-DIS-11 | `sale_officer_accepted = Y` | ASSET_HELD, answer `ASSET_HELD` |
| ROUND_OPEN | `BID_PLACED` under R-DIS-37 | Any reported bid | BID_RECEIVED, answer `BID_RECEIVED` |
| Any | An unexpected state, a late fact or a repeated signal | X3, X5 | Unchanged |

| `asset_sale` and `asset` view | Event | Condition | To |
|---|---|---|---|
| Sale agreed | The term starts | R-DIS-47 fires | Award, due date and received-at recorded; asset under offer |
| Award, term running | The payment arrives | R-DIS-48 fires | Sale confirmed, title transfer pending |
| Award, term running | The timer fires with no payment | The expiry signal is raised | Unchanged here; the rounds story cancels and reopens (BR6) |
| Any | A duplicate signal, fact or key | X5 | Unchanged |

The holding and listing statuses are the `LOV-HOLDING` and `LOV-LISTING` rows of TSD S5 T3.2; the case states are the DISPOSAL machine's (TSD S5 T4). The award and its cancellation have no dedicated element, which is GAP-2925.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD | Asset and disposal C: confirms the payment, records the award and the term |
| RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, PT-AUCTION, PT-RAMC, SY-DATALOAD | Asset and disposal U: the sale record, the term and the holding status |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL and the further roles of the read row | Asset and disposal R, in scope |
| RW-SALEOFF, RW-NPAMGR, RW-HEADNPA, RW-HEADASL, RW-PRODHEAD | Reading the term on SCR-22 and SCR-21 in their scope |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the branch; no grant on another schema and no `v_ace_*` grant |

The rights are the rows of the legacy permission table and TSD S5 T6.1, nothing wider. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee and 6 more | Write: the award, the due date, the received-at time and the confirmation |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Read; the reopen is the rounds story's write |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, asset_ref, asset_type, book_value, holding_status and 10 more | Write: holding_status on the confirmation; read otherwise |
| Standard columns | asset_sale, asset, listing (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| Not specified in the source documents (GAP-2925; ASM-4822) | none | the award, payment_due_date, payment_received_at, the buyer of the award, the term length | Held against the sale record and reference data; no column |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read: rwb-case contract |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Not read: rwb-payment fact and event (BR5) |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and 5 more | Not read: the sale is this service's, the ACE fact is rwb-source-data's |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03). **No personal data**: identifiers, codes, amounts, dates, a buyer code and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4027-CON; it adds no write, because the term starts and is confirmed inside the workflow.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the sale status and the term of each asset (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with title, listing, sale, award, due date and the days remaining (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |

The legacy Endpoints table also names `POST /assets/{assetId}/valuations` (API-S5-003) and `POST /listings/{listingId}/rounds` (API-S5-005); neither is this story's — the valuation write is rwb-valuation's under ASM-0043 (DP-11) and the round write and the reopen are RWB-S5-E4024's. Errors: 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001, 503 when a library or a contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state the rules check before they fire; faked |
| Case-move answer (name Not specified in the source documents (GAP-2929; ASM-4826)) | rwb-case (P3) | P3 rwb-case | `AWAITING_PAYMENT`, `TITLE_TRANSFER_PENDING`, `ASSET_HELD` and `BID_RECEIVED` with the rule and its version; faked |
| Payment fact activity (name Not specified in the source documents (GAP-2929; ASM-4826)) | queue `rwb-payment` | P8 rwb-payment | The due date, `payment_received_at` and the freshness stamp, in place of the legacy `v_ace_payment` read (DP-05); faked |
| Sale and award read (name Not specified in the source documents (GAP-2925; ASM-4822)) | rwb-asset (S5) | S5 | The sale record and the award the term belongs to, where no column names them |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The two placed rows are the cross-service rows the plan does not carry, so this story builds on their documents and fakes and its C and I rows are None; the wave 3 harness holds the real journey.

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale event the sale stories'; starting a term, confirming a payment and detecting an expiry write no outbox row and add nothing to `rwb.asset.events.v1`. A build that publishes here fails the absence test.

#### 12.4 Events consumed

| Topic | Event | Owner | Use |
|---|---|---|---|
| `rwb.payment.events.v1` | Payment event (name Not specified in the source documents (GAP-2929; ASM-4826)), one per matched payment | P8 rwb-payment | Correlates a confirmed payment to the award and wakes the workflow; the row comes from Architecture v5 slide 13, which marks S5 as listening to P8. Consumed through the inbox library (DP-09) with the event as a signal, never as the record of truth |

One consumer group on the owner's topic, deduplicated by event id; where the event and the fact disagree the fact wins (X7). No other subscription is added.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new across the holding | `rwb-asset` in `rwb-recovery` | Input: case, route, asset, listing, sale, package in force; signals: award made, payment received, payment-term expiry, package in force |
| `startPaymentTerm` | Activity, the term start and its record | `rwb-asset` | Sale, award and package in; rule IDs with versions, due date, holding status and case move out, one transaction |
| `confirmSalePayment` | Activity, the confirmation | `rwb-asset` | Payment fact in; rule IDs with versions, confirmation, title-transfer start and case move out, one transaction |

No child workflow and no second queue. The two activity names are design choices of this story; the payment fact runs on the owner's queue.

#### 12.6 Schedules

None. The five calendar days run as a durable timer inside the workflow, not as a Temporal Schedule and not as a Quartz job. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The sale and the award; this story writes the award, the due date and the confirmation |
| asset | S5 (`rwb_asset`) | The holding status while the term runs |
| listing | S5 (`rwb_asset`) | Read only here; the reopen is the rounds story's write |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated signal or fact |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `approval` (P7), `payment`, `payment_match`, `posting` (P8), `valuation` (S1), `document` (P5), `deviation` (S8), the partner tables (S9), every `v_ace_*` view (P1). No award table exists (GAP-2925). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | `SALE_AGREED`, `AWAITING_PAYMENT`, `TITLE_TRANSFER_PENDING`, `WORK_ORDER_OPEN` and `ROUND_OPEN` for the fixture cases; a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | The four moves accepted; a move refused for an unexpected state | AC1 to AC3 |
| rwb-payment fact fake | No payment by the due date; a payment received one day early; a payment on the due date; a stale fact; no answer inside 2 s | AC1, X6 |
| rwb-payment event fake | The payment event of `SL-2026-000527`; a duplicate event; an event that disagrees with the fact | AC1, X5, X7 |
| rwb-decision package fake | The DISPOSAL package at its version with the four rules | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-22 and SCR-21 answer for `RC-2026-000527` | AC1 |
| Award signal fake | An award with every field; one without the sale date; one repeated on the same key | AC1, X4, X5 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2929; ASM-4826).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 1 consumed | `rwb.payment.events.v1`, one consumer group, read as a signal (DP-09) |
| Temporal | 1 workflow, 2 activities owned, 1 consumed | `AssetDisposalWorkflow`, `startPaymentTerm` and `confirmSalePayment` on `rwb-asset`; the payment fact on `rwb-payment`; no Schedule |
| File | None | No file element; the portal publication is FEAT-AST-12's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.paymentterm`; front end `src/modules/recovery/asset/PaymentTerm.tsx`, the fragment SCR-22 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition here: the legacy `v_ace_payment` read leaves the service for the P8 boundary and the `v_ace_npa_sale` read for rwb-source-data, and no `v_ace_*` grant is kept. DP-03 is the transaction rule of both steps, DP-13 moves the base, DP-19 is how the screens reach the service. DP-09 is used without a platform row of its own, because the inbox library comes with the service template. The package in force is loaded through the template without the DP-04 platform row (GAP-2930; ASM-4827).

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` payment branch | Workflow | Waits on the durable timer and the signals, loads the package in force, reports to the parent |
| `startPaymentTerm`, `confirmSalePayment` | Activities | The two steps: read, evaluate, write, answer |
| `PaymentTermEvaluator` | Service | R-DIS-47 and R-DIS-48 on the award, the due date and the payment fact |
| `WorkOrderGateEvaluator`, `BidGateEvaluator` | Service | R-DIS-11 and R-DIS-37 as the state gates AC2 and AC3 name |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `SaleTermWriter` | Repository | `asset_sale` and `asset` in one transaction with the idempotency row and the lock |
| `CaseMoveAnswer`, `CaseStateClient`, `PaymentFactActivity`, `PaymentEventInbox` | Clients | The four answers, the fact and the one subscription, one hop, 2 s |
| `AssetController` | Controller | The two reads, the rights and the 400/401/403/404/422/503 map |
| `PaymentTerm` | React component | The award, the due date, the days remaining and the result on SCR-22, read only |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no award table and no column added (GAP-2925).

**Configuration.** The term length, the reminder point and the lists at their version (TSD S5 T3.2); the DISPOSAL package and version from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the branch and its input record; (2) `PaymentTermEvaluator` with the award and the confirmation paths (AC1); (3) `SaleTermWriter` with the due date and the lock (AC1, X4); (4) the payment fact client against its fake (AC1, X6); (5) the expiry detection and the signal to the rounds story (AC1); (6) the record writer against the stub (AC4, X1); (7) `WorkOrderGateEvaluator` and `BidGateEvaluator` (AC2, AC3); (8) `CaseMoveAnswer` (AC1 to AC3); (9) the inbox and the payment event row (X5, X7); (10) `AssetController` with the rights and the error map (X2); (11) the screen fragment through the route fake; (12) the boundary test (X9, BR5, BR7).

**Feature flag.** `rwb.asset.payment-term-v1`; off means the award keeps the case at `SALE_AGREED`, nothing is written and the timer is not armed.

**Done when.** §16 passes, an award starts the five-day term in SIT, a payment inside the term answers `TITLE_TRANSFER_PENDING`, an unpaid term raises exactly one expiry signal and the rounds story cancels and reopens, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | A floor or an accepted price under the approver's limit on the confirmation (X3) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | An appraisal more than a year old when the term starts (X3) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or signal is absent or invalid (X4) | Enter {field}. |
| MSG-P4-002 | A role without the right reads or acts (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the sale changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The payment fact is stale at the due date, under VR-S5-018-1 (X6) | {product} is from {date}. Today's ACE batch has not arrived. |

The five legacy IDs are copied unchanged, no message is reworded and none is added; MSG-P1-001 is the message of VR-S5-018-1 in FSD S5 A2.18.3.1 and the only row this story brings with it.

### 15. Screens and states

SCR-22 Asset record (take-on; held; listed; sold) and SCR-21 Asset list (loading; list) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, the sale and the term, rwb-case for the state and rwb-payment for the payment. SCR-24 Auction rounds shows the award and its result and is read here, not written. This story fixes the rwb-asset answers only; the route and field list are RWB-PLT-N001-CON.

The states it produces are the term state of SCR-22 — the award, the due date, the days remaining, the confirmation and the expiry signal — and the refusal, not-recorded, wrong-state, stale-payment and disagreement states with MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-P1-001 and MSG-S5-001. The take-on and listed states are the earlier stories' of this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-027-01 | AC1 | Component | Case `RC-2026-000527` with sale `SL-2026-000527`; the award, the term, the fact, the record and the case answer on the fakes |
| TC-E4-027-02 | AC2 | Component | Case `RC-2026-000528` at `WORK_ORDER_OPEN`; R-DIS-11 fires, the invoice is released, the asset returns to hold and `ASSET_HELD` is answered |
| TC-E4-027-03 | AC3 | Component | Case `RC-2026-000529` at `ROUND_OPEN`; R-DIS-37 fires, the bid is recorded and `BID_RECEIVED` is answered |
| TC-E4-027-04 | AC4 | Component | Record stub stopped; nothing written, no term started, MSG-P7-003 shown |
| TC-E4-027-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002, no read and no write |
| TC-E4-027-06 | Principle 5 | Component | A forced record failure at the term start; no row, no answer, no event |

The six cases are the legacy cases in their order with the Level column added: each runs `Component` on its fakes, and TC-E4-027-01 also exercises the timer, so its `-ITG` copy in the wave 3 harness carries the real payment and case calls. The full text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the term length, the reminder point, the statuses and the thresholds stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log; a buyer is a code and every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no data-lake export of a sale.
- The record precedes the change and the repeated signal is deduped (DP-03, BR8); the expiry is one signal, never a second evaluation of R-DIS-49.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id names this slice | FEAT-AST-18 of FSD S5 A2.18 and the epic BRD row for FEAT-AST-18: the term is tracked and the asset released if it is missed (GAP-2928; ASM-4825) | The payment branch, the two steps, the answers | TC-E4-027-01 to -04 |
| ADR-013 | 19 services inside ACE | rwb-asset owns the sale, the award and the term | TC-E4-027-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-027-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable timer and the signals; no Quartz row | TC-E4-027-01 |
| ADR-020 | Contract-first REST, one hop, 2 s | The consumed rows and the boundaries | TC-E4-027-01 |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-027-04, -06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-027, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Legacy endpoints | `POST /assets/{assetId}/valuations` is rwb-valuation's (ASM-0043); `POST /listings/{listingId}/rounds` is RWB-S5-E4024's |
| Test cases | TC-E4-027-01 to TC-E4-027-06 |
| Feature and screens | FEAT-AST-18, SCR-22 Asset record and SCR-21 Asset list, read through the composite route |
| Rules | R-DIS-47 and R-DIS-48 owned here; R-DIS-11 and R-DIS-37 kept as the AC2 and AC3 gates; R-DIS-49 and R-DIS-50 the rounds story's |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The shapes of the reads, the consumed rows, the event row, the two library elements, the error set and the fakes: RWB-S5-E4027-CON.
- The acceptance of the bid and the agreed sale, the award cancellation, the vendor score and the reopened round (R-DIS-40 to R-DIS-42, R-DIS-49, R-DIS-50): RWB-S5-E4024-APP.
- The transfer of the vehicle registration and the Land Office transfer (R-DIS-51 to R-DIS-53): FEAT-AST-19 and FEAT-AST-20's stories.
- The proceeds, the shortfall and the residual route (R-DIS-54 to R-DIS-58): FEAT-AST-21's story.
- The work-order acceptance of the held property as a behaviour (R-DIS-11): the held-property story of FEAT-AST-07; kept here only as the AC2 state gate (GAP-2927).
- The payment, its matching, its posting and its event payload: rwb-payment (P8).
- The vendor panel and the scorecard: rwb-partner (S9).
- The case, its states and the parent workflow: rwb-case (P3).
- The rule rows, the package version and its approval: rwb-decision (P7) (GAP-2930).
- The composite route and the field list: RWB-PLT-N001-CON and the edge stories.
- The real payment, case and portal calls and their evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this key.
