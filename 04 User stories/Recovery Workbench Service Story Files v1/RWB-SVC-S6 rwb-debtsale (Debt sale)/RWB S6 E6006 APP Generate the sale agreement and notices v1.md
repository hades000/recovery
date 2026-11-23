# RWB-S6-E6006-APP Generate the sale agreement and notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S6-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6006-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the agreement-and-notices slice of RWB-E6-006 split out for rwb-debtsale. The three legacy acceptance criteria are kept word for word with their origin tag; the sale agreement is now produced in rwb-document (P5), the customer notices in rwb-comms (P6) and the customer addressee fact read on the rwb-source-data contract (DP-05), while this service evaluates R-DS-23 of the DS package, records the decision through the local decision-record library before the `debt_sale_lot` row changes (DP-03), writes `signing_date` and `status`, answers rwb-case for the case move to `LOT_AWARDED` and serves the award screen on the base `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). The award operation API-S6-003 and R-DS-19 stay with RWB-S6-E6005-APP; the empty C row, the step boundary, the reference storage, the customer and notice facts, the WIN path, the EP06 wave 4 against the wave 3 service and the missing S6 extract are recorded as GAP-2996 to -7 with ASM-4943 to -7. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **the Workbench to produce the agreement and the customer notices the sale requires**, so that **debt sales run on approved lots and masked data**.

This is the agreement-and-notices slice of legacy RWB-E6-006. It owns:

- the three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screen and test cases they depend on;
- the R-DS-23 branch of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, the saga child of `CaseWorkflow` owned by rwb-case (Temporal and Drools Design slide 13; Architecture v5 slide 19, "Temporal DebtSaleWorkflow (saga, pivot = transfer)");
- the evaluation of R-DS-23 on the confirmed award, with the DS package version in force and the 54 percent cap read from the package, never as a constant;
- the sale agreement and the customer notices as a request to their owners: the agreement is produced and kept by rwb-document (P5) from an approved template, the notices are issued by rwb-comms (P6), and this service holds their references and their outcome;
- the customer addressee fact of the notices, read on the rwb-source-data contract from the ACE customer data and never from a `v_ace_*` view (DP-05);
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the lot row changes (DP-03), which is what legacy AC1 and AC3 require;
- the write of `signing_date` (DF-SAL-027) and `status` (DF-SAL-030, `AWARDED`) on the `debt_sale_lot` row in schema `rwb_debtsale`, with the optimistic lock and no other column;
- the answer to rwb-case for the case move `LOT_AWARDED`, with the rule ID and the version that produced it;
- the award screen SCR-26 in its awarded state, served on `/api/recovery/debtsale/v1` through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the elements, the lists, the consumed rows, the rights, the error set and the fakes, which are RWB-S6-E6006-CON; the award operation API-S6-003, the price test R-DS-19, the `AwardRequest`, the `DecisionLogEntry` answer and the buyer columns, which are RWB-S6-E6005-APP's; the lot build, the estimate and the reserve, which are RWB-S6-E5024-APP's; the data room, the tape and the bids, which are RWB-S6-E5026-APP and the take-bids story's; the agreement's template, its generation and its custody, which are rwb-document's (P5); the notices, their templates, the conduct check, the WIN despatch and the proof of delivery, which are rwb-comms's (P6) and the P2 INT-14 file; the case of record and its route states, which are rwb-case's (P3); the rule package, the ledger and the approval chain, which are rwb-decision's (P7); the settlement term and the data transfer, which are RWB-S6-E6007-APP's; and the deployment of this build, which is the operations story of this legacy key and the wave 4 harness.

### 2. Business rationale

Legacy RWB-E6-006 asked the Workbench for one thing the debt sale officer cannot do by hand at scale: the agreement and the customer notices the sale requires, produced on approved lots and masked data. The FSD keeps the objective unchanged — "Produces the agreement and the customer notices the sale requires", unattended, integration points "Workbench, WIN", on the 45-day debt sale turnaround measured on the decision log and the Workbench records (FSD S6 A2.10.1 and A2.10.2) — and the feature list keeps it as FEAT-DBS-10, first in E6, which depends on FEAT-OCC-07, the P6 capability that generates contract and approval documents from approved templates (Feature List v4 row FEAT-OCC-07).

What D-RCV-60 changes is where each piece is produced and who owns it:

- **the agreement is a document, not a column of this service.** Documents, their templates, their custody and their retention are rwb-document's (P5) in the target, so the agreement this step requests is generated and kept there and this service holds its reference only. The legacy feature's chained prerequisite FEAT-OCC-07 is read the same way, as that document-generation capability rather than as a call from the debt sale step (GAP-3000).
- **the notices are rwb-comms's.** The legacy `notice` row of the data table, with its `notice_type`, `sent_date` and `barcode`, is the notice fact of the communications service (P6) in the target, which also holds the template, the conduct check before an outbound contact and the WIN despatch with its proof of delivery (Feature List v4 rows FEAT-OCC-01, FEAT-OCC-02 and FEAT-OCC-05). This story asks for the notices and reads their outcome; it writes no notice row.
- **the customer fact is not this service's.** The legacy data table reads the customer from `v_ace_customer`. In the target the 30 `recovery.v_ace_*` views are read by rwb-source-data alone, so the addressee of a notice arrives on that owner's contract with its as-of date, which is DP-05 and its only pattern row this story claims (GAP-2996).
- **the award decision is the sibling's and the award effect is this story's.** R-DS-19 tests the best bid against the reserve and the 54 percent cap and routes the award to `AWARD_PENDING`; R-DS-23 then awards the lot, generates the agreement and the notices and moves the case to `LOT_AWARDED` (Business Rules and Routing Logic v4). API-S6-003 and R-DS-19 are RWB-S6-E6005-APP's, and this story owns the R-DS-23 effect and nothing of the price test (GAP-2997).
- **the decision is recorded first**, in the same transaction as the lot change, which is what TSD S6 T2 states ("writes the decision log entry before any change") and what legacy AC3 tested.
- **no event leaves this step.** Architecture v5 slide 19 OUT gives the service exactly two events, `LotAwarded` and `AccountsTransferred`; the award event is RWB-S6-E6005-APP's and the transfer event is RWB-S6-E6007-APP's, and the completed award reaches rwb-case on the case-move answer and is read by its consumers on the lot read (12.3).

The delivery is stated as the plan gives it: this key is EP06 and therefore wave 4 with release 30 April 2027, while rwb-debtsale is created in wave 3, so one service delivers its EP05 keys in wave 3 and this key in wave 4, and the date is copied unchanged and marked tentative (GAP-3001).

### 3. Preconditions

- RWB-S6-E6006-CON is published: the sale-agreement and sale-notice elements, the lot answer with its award-time fields, the four closed lists, the consumed document, comms, customer, case and package rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-document generation contract is available for the fake: the approved template in force, the case and lot facts merged into it, the sealed document and its reference. No source publishes the operation name, so the row carries the placeholder (GAP-2996; ASM-4943).
- The rwb-comms notice contract is available for the fake: the notice type, the template and its version, the addressee, the issued notice with its `sent_date` and its `barcode`, and the despatch outcome. No source publishes the operation name, so the row carries the placeholder (GAP-2996; ASM-4943).
- The rwb-source-data customer read is available for the fake: the addressee fact of each sold account's primary person, masked under the policy in force, with its as-of date. The service holds no `v_ace_*` grant (DP-05; GAP-2999; ASM-4946).
- The rwb-case state read and the case-move answer are available for the fake: the case is in `AWARD_PENDING` when the confirmation arrives, and the move is answered for `LOT_AWARDED`. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-2996; ASM-4943).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the lot columns, the record and the references commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration (GAP-2998).
- The DS rule package is in force at its version with R-DS-23, the 54 percent cap and the notice-type and template lists as versioned values; the package is authored, approved and versioned in rwb-decision (P7).
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_document.document`, on `rwb_comms.notice`, on `rwb_case.recovery_case` or on a view is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6006-CON when its tests pass.

### 4. Flow

1. The award step of RWB-S6-E6005-APP has tested the best bid against the reserve and the 54 percent cap and routed the case to `AWARD_PENDING` on R-DS-19. This story receives the award confirmation for a lot in that state and writes nothing of the price test.
2. The R-DS-23 branch of `DebtSaleWorkflow` on queue `rwb-debtsale` reads the lot and its accounts from `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`, and the case state and reference on the rwb-case contract, read only, one hop with a 2 s budget and a breaker.
3. It reads the rule version in force on the rwb-decision contract and applies R-DS-23 to the fact the award step produced: the confirmed award, the buyer, the price tested and its record.
4. For the agreement it asks rwb-document (P5) to generate the sale agreement from the approved template in force, merging the lot, the buyer, the price, the signing date and the case facts. rwb-document seals the document, keeps it under its retention policy and answers with the document reference and its template version.
5. For the notices it asks rwb-comms (P6) to issue the customer notices the sale requires: one notice per sold account, with the notice type, the template and its version, the addressee read in step 6, and the language the case carries. rwb-comms runs its conduct check, dispatches through the WIN path where the channel is a letter and answers with the notice references, the `sent_date` and the `barcode` of each.
6. The addressee of each notice is read on the rwb-source-data contract, masked under the policy in force, and is passed to rwb-comms only inside the notice request. It is not written in `rwb_debtsale`, not put in the decision record, not logged and not put in a workflow input beyond the request that carries it (DP-05).
7. `DebtSaleDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the lot reference, the rule ID with its version, the inputs reference, the agreement reference, the notice references, the outcome, the case move and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
8. `DebtSaleAwardWriter` updates the `debt_sale_lot` row in one `rwb_debtsale` transaction with the decision record, the idempotency row and the optimistic lock of `version`: `signing_date` (DF-SAL-027) from the date the sale was signed that the confirmation carries, and `status` (DF-SAL-030) to `AWARDED` of `LOV-LOT-STATUS`. `reserve_price`, `approval_authority`, `payment_terms`, `buyer_partner_id` and `buyer_class` are not written by this step.
9. `CaseMoveAnswer` answers rwb-case with the move `LOT_AWARDED`, the rule ID, its version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither.
10. A repeated confirmation for the same lot and award reference writes nothing, requests no second agreement and no second notice set, sends no second case move and counts the repeat.
11. SCR-26 Award in its awarded state reads the lot, its signing date, its status and the references of the agreement and the notices through the gateway-bff composite route, read only, next to the case route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no lot column, no case-move answer and no committed reference leaves the service | MSG-P7-003 | AC3, TC-E6-006-03, TC-E6-006-05 |
| X2 | The caller is not the service identity of the step, or a role without the Debt sale right reads the award screen | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-006-04 |
| X3 | The case is not in `AWARD_PENDING` when the confirmation arrives, or the lot is not the one the award names | 409 and nothing is written; the step is not re-evaluated on a case that has already moved | None | AC2 |
| X4 | rwb-document cannot generate the agreement, or answers with no reference | The step writes nothing and answers no case move; the agreement request is retried on the workflow's schedule and the award stays in `AWARD_PENDING` | None | AC1, TC-E6-006-01 |
| X5 | rwb-comms cannot issue the notices, or the conduct check stops one | The step completes no notice set: the decision record is not written, no lot column changes and the case does not move; the stopped notice is raised to rwb-comms | None | AC1, AC2 |
| X6 | The customer fact of a sold account is absent, stale or unmasked on the rwb-source-data answer | The notice of that account is not requested and the step fails as X5; no placeholder addressee and no invented name is used | MSG-P1-001 | AC1, AC2 |
| X7 | rwb-document, rwb-comms, rwb-source-data, rwb-decision or rwb-case does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written, no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X8 | The same confirmation arrives twice for the same lot and award reference | One record, one update, one agreement, one notice set and one case-move answer; the repeat is counted | None | AC1, AC2 |
| X9 | A component, a statement or a test reaches `rwb_document`, `rwb_comms`, `rwb_case`, `rwb_decision` or `rwb_source_data`, another service's schema, or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6 |

X1 to X3 are the exception paths of RWB-E6-006 carried onto the split, X4 to X8 are the paths the target call types and the document and notice boundaries add, and X9 is the DP-01, DP-02 boundary. The 45-day turnaround target and the 54 percent cap are values in force in the package, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6006-CON, the rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P5, P6 or P7 |
| Negotiable | The activity names, the decision code, the shape of the notice request and the step outcome are this story's choice; the rules, the messages, the screen, the read and the lot columns are fixed |
| Valuable | An awarded lot gets its agreement and its customer notices exactly once, the decision is recorded before the lot changes, and the case moves to `LOT_AWARDED` with the references the officers and the buyer need |
| Estimable | One workflow branch, one evaluator, one record write, one row update, one case-move answer, three clients, two request adapters and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots, agreements and notice answers through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Generate the sale agreement and notices

  Background:
    Given lot "LOT-2027-000041" is awarded to buyer "PTR-2027-000031" for case "RC-2027-000611"
    Given the DS rule package is in force at its version and carries R-DS-23 and the 54 percent cap
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Generate the sale agreement and notices (legacy RWB-E6-006 AC1)
    Given the rwb-document contract mock returns the sale agreement of lot "LOT-2027-000041" with its reference and its template version
    Given the rwb-comms contract mock returns one issued notice per sold account of "LOT-2027-000041" with its sent_date and its barcode
    Given the rwb-source-data contract mock returns the masked addressee fact of each sold account
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the agreement and the customer notices the sale requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-23 (legacy RWB-E6-006 AC2)
    Given the rwb-case contract mock returns the case state "AWARD_PENDING" for "RC-2027-000611"
    Given the rwb-document contract mock returns the sale agreement of lot "LOT-2027-000041" with its reference
    Given the rwb-comms contract mock returns one issued notice per sold account of "LOT-2027-000041"
    Given a case in state AWARD_PENDING
    When award confirmed
    Then award the lot and generate the sale agreement and the customer notices
    Then the case moves to LOT_AWARDED

  Scenario: AC3 Not recorded (legacy RWB-E6-006 AC3)
    Given the rwb-document contract mock returns the sale agreement of lot "LOT-2027-000041" with its reference
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-006 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `its trigger arrives`, `award confirmed`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so each criterion carries one to four `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target: rwb-document produces and keeps the agreement, rwb-comms issues the notices and dispatches them through the WIN path, rwb-source-data answers the masked addressee fact, and rwb-case applies the `LOT_AWARDED` move this story answers, while this story evaluates R-DS-23, records the decision, holds the references and writes `signing_date` and `status` on the lot. Legacy AC2 names the award and the agreement in one sentence; the award operation and the price test are RWB-S6-E6005-APP's and the award effect is this story's, so the two stories own different halves of the sentence and the split is recorded (GAP-2997; ASM-4944).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-19 | Debt sale | D8.4 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | best_bid at or above reserve_price | Test the price against the reserve and the 54 percent cap, and route the award | AWARD_PENDING | Debt sale officer | Case Workspace, Committee View | 2 working days |
| R-DS-23 | Debt sale | D8.4 | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |
| R-DS-24 | Debt sale | D8.4 | LOT_AWARDED | SETTLEMENT_TERM_STARTED | Any | Start the settlement term and await payment | SETTLEMENT_PENDING | Buyer | buyer portal, ALS core and GL | per agreed settlement period |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. R-DS-23 is the one rule this story evaluates and owns the criterion of; R-DS-19 is tabled because it is the predecessor whose outcome this step consumes, and its criterion and test are RWB-S6-E6005-APP's; R-DS-24 is tabled because it is the successor this step hands the awarded lot to, and its step belongs to the settlement story of this service. Their owner column is a role of the business and not a service: the case states are written by rwb-case on this story's answer, the agreement and the notices are produced by rwb-document and rwb-comms, and the lot columns are written here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The award-time columns of the lot are this service's: `signing_date` and `status` are columns of `debt_sale_lot` in `rwb_debtsale`, and the buyer columns are the award step's | Architecture v5 slide 41 (rwb-debtsale owns lots and buyer terms); TSD S6 T3.1; Ownership Map `debt_sale_lot` owner S6 |
| BR2 | The decision is recorded before the lot row changes, with the rule ID and the package version in force, and the agreement and notice references are part of that record; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy RWB-E6-006 AC1 and AC3 |
| BR3 | The agreement is rwb-document's and the notices are rwb-comms's: this step requests them, holds their references and writes no `document` row and no `notice` row | Architecture v5 slide 41 P5 and P6; Feature List v4 rows FEAT-OCC-01, FEAT-OCC-02, FEAT-OCC-05 and FEAT-OCC-07; GAP-2996 |
| BR4 | The addressee fact is read on the rwb-source-data contract and never from a `v_ace_*` view; it enters the notice request only and is kept in no column, record, log or event of this service | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2999 |
| BR5 | The case move is answered and not written: `recovery_case` and the route states `AWARD_PENDING`, `LOT_AWARDED` and `SETTLEMENT_PENDING` are rwb-case's, and this story sends the move with the rule and its version | Ownership Map `recovery_case` owner P3; Architecture v5 slide 41; GAP-2996 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id`, `account_id` and the case reference are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR7 | The price test is not repeated here: the 54 percent cap and the reserve comparison are read from the package and from the record the award step wrote, and this step recomputes no price and writes no `reserve_price` and no buyer column | Business Rules and Routing Logic v4 R-DS-19 and R-DS-23; TSD S6 T4; GAP-2997 |
| BR8 | Every value a business person may change is reference data or a rule row read with its version: the notice types, the notice and agreement templates and their versions, `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-PUTBACK`, the 54 percent cap and the 45-day target | TSD S6 T3.2; FSD S6 A2.10.3.1 BR-S6-010; legacy Guardrails |
| BR9 | The same confirmation twice, or the same `Idempotency-Key` twice, writes once, requests one agreement and one notice set and answers the case move once | TSD S6 T-A.2; Architecture v5 slide 11 |
| BR10 | No person name, contact value or identity number is held in `rwb_debtsale`, in a workflow input, in the decision record or in a log; the notices carry their content inside the rwb-comms request and nowhere else | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes; BR4 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR5). What this story does own is the award fact of the lot and the state of the step.

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| `AWARD_PENDING` | `AWARD_CONFIRMED` under R-DS-23 | price tested against the reserve and the 54 percent cap, and recorded | `LOT_AWARDED`, with the agreement and the notices issued and `signing_date` and `status` written |
| `LOT_AWARDED` | `SETTLEMENT_TERM_STARTED` under R-DS-24 | the award step of the settlement term starts | `SETTLEMENT_PENDING`, outside this story |
| Any state the rule does not name | Any confirmation for the same lot | X3, X8 | Unchanged, the repeat or the exception is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The award confirmation arrives for a case in `AWARD_PENDING` | The package in force is loaded | Evaluating |
| Evaluating | R-DS-23 fires | The agreement and the notice set are requested | Requesting |
| Requesting | rwb-document and rwb-comms answer with their references | Both answers carry a reference | Applying |
| Applying | The record, the two lot columns and the case-move answer are written | The transaction commits | Waiting for the next award |
| Applying | The record write or the transaction fails, or an answer carries no reference | X1, X4, X5 | Waiting, nothing changed |

The lot's own status at the end of the step is `AWARDED`, one of the five values of `LOV-LOT-STATUS` — BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED (TSD S6 T3.2). No source states that the award step changes the lot status, so the write is declared here and the difference is recorded (GAP-2998; ASM-4945).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-debtsale service identity | Runs the branch unattended, evaluates R-DS-23, requests the agreement and the notices, writes the decision record, the two lot columns and the case-move answer; it holds no grant on another schema and no `v_ace_*` grant |
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: reads the awarded lot, its signing date and the references of the agreement and the notices on SCR-26, and is the also-user the FSD names |
| RW-PRODHEAD, product head | Debt sale RA: reads the awarded lot and its references |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the awarded lot and its references |
| RW-SALEOFF, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | Debt sale R: the partner sees its own lot and its own award through the partner gateway, never a customer fact and never a notice |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R: the service identities run the step and are subject to the same checks |
| rwb-document and rwb-comms | Generate the agreement and issue the notices under their own rights, templates and conduct rules; this story holds no right over their rows |

The rights above are the rows of TSD S6 T6.1. The legacy Permission checks table gives the Debt sale A right to RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL; the FSD gives this feature no primary role at all — "None; runs unattended | Primary" with the debt sale officer as an also-user (FSD S6 A2.10.3.3) — and the A right of the legacy table is exercised on the award operation, which is RWB-S6-E6005-APP's and is the only surface of this key that carries it (GAP-2997; ASM-4944). DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot reference of the record, the requests and the answer |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, merged into the agreement and shown on the screen |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read, merged into the agreement |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Read only, as the fact the award step tested against; never written here |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Read, the buyer named in the agreement; written by the award step, not here |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Read, against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Write, the date the sale was signed that the confirmation carries |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Read only, the authority the approval step wrote |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Read only, merged into the agreement |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, to `AWARDED` of `LOV-LOT-STATUS` |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read only, the sold accounts that need a notice and the accounts of the agreement |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `updated_at`, `updated_by` and the optimistic lock of `version` on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, agreement reference, notice references, outcome, decided at | Write through the local library, before the lot row changes |
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | Not read as a table: the issued notice arrives on the rwb-comms contract, with its type, sent date and barcode (GAP-2996) |
| document | document (P5, `rwb_document`) | the sale agreement, its template, its version and its reference | Not read as a table: the agreement arrives on the rwb-document contract (GAP-2996) |
| DF-ACE-055 to DF-ACE-074 | customer (P1, ACE data) | person_key, cif_no, name, date_of_birth, customer_status and 14 more | Not read as a table and not read as a view: the masked addressee arrives on the rwb-source-data contract (DP-05; GAP-2999) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case read and the move is answered (GAP-2996) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule rows are governed in rwb-decision and loaded here as the package in force |

Field IDs are those of TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v8; the `notice`, customer, case and rule rows are the rows the legacy story lists in its Data table, with their owner moved to P6, P1, P3 and P7 by the target. **No new table, no new column and no migration**: this story writes two existing columns of the lot and no column of the account row, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_debtsale` by the library's own migration (DP-03). The lot has no column for the agreement reference or for the notice references, so both live in the decision record and in the custody of their owners; the absence is recorded (GAP-2998; ASM-4945).

**No personal data.** The columns this story writes carry identifiers, codes, amounts, dates and a rule version. The addressee of a notice is read on the owner's contract, passed inside the notice request and held nowhere in this service: no name, address, contact value or identity number enters `rwb_debtsale`, the decision record, a log or a workflow input beyond that request, and every fixture is synthetic. `borrower_code` is an identifier and never a name.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module — API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids` — and none of them is an agreement or a notice operation. The legacy Endpoints table of RWB-E6-006 rows API-S6-003: it is RWB-S6-E6005-APP's operation, it carries the A right, and this step provides no operation of its own and declares none. The awarded lot, its `signing_date`, its `status` and its references are read on API-S6-002, whose shape is RWB-S6-E6001-CON's baseline and is not redefined here (GAP-2997; ASM-4944).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The generation of the sale agreement from the approved template (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/document/v1` | P5 rwb-document | The template in force, the sealed agreement and its reference; faked |
| The issue of the customer notices (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice type, the template and its version, the addressee, and the issued notice with its `sent_date` and `barcode`; the conduct check and the WIN despatch sit behind it; faked |
| The masked addressee fact of a sold account (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The addressee of the notice and its as-of date, masked under the policy in force; faked (DP-05) |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the stage the lot belongs to; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | rwb-case (P3) | P3 rwb-case | The move `LOT_AWARDED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2996; ASM-4943)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows of R-DS-23 with the 54 percent cap, the notice types and the templates; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2996 with ASM-4943.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale exactly two events, `LotAwarded` and `AccountsTransferred`; `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's, so this step writes no outbox row and holds no producer of its own. The completed award reaches rwb-case on the case-move answer and is read by its other consumers on API-S6-002, and a build that adds an event here fails the absence test (GAP-2997; ASM-4944).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale `ProceedsMatched`, which is the settlement fact of RWB-S6-E6011-APP's step; the award confirmation arrives as the stage signal of R-DS-23 and the case state on the rwb-case contract. This story therefore holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow`, pivot = transfer | `rwb-debtsale` in namespace `rwb-recovery` | Input: the case, the lot, the award reference and the rule package in force; signals: the award confirmation, the agreement answer, the notice answer and the case state |
| The R-DS-23 branch of `DebtSaleWorkflow` | Workflow branch, the step from the confirmed award to `LOT_AWARDED` | `rwb-debtsale` | Applies R-DS-23, requests the agreement and the notices, writes the record and the lot columns and reports the stage outcome to the parent |
| The document run of rwb-document | Activity started on the owner's queue through the kit's document intake, owned and run by P5 | `rwb-document` (P5) | The template, the merged facts and the sealed document; started by this story, owned by P5 |
| `recordAwardAndIssueNotices` | Activity, the one step of this story | `rwb-debtsale` | The case, the lot, the award and the two owner answers in; the rule ID with its package version, the two lot columns, the decision record and the case move out, in one transaction |

No child workflow for the case and no workflow for the money exists in this service, and neither the agreement nor the notice is produced here: they are the owners' runs (BR3). The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the award confirmation for a case in `AWARD_PENDING`, because the FSD declares no background event for the feature (FSD S6 A2.10.4.4, "No background event").

#### 12.6 Schedules

None. The step runs from the award confirmation, and owns no Temporal Schedule and no legacy Quartz job. The monthly debt sale cycle shown on the temporal design as the clock of the route set is not a Schedule of this step, and no Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot; this story writes `signing_date` and `status` and updates the optimistic lock |
| debt_sale_account | S6 (`rwb_debtsale`) | The sold accounts the notices are raised for; read only in this story |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome, with the agreement and notice references (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated confirmation and the outcome it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Created in this schema by the library and used by the stories that publish; this step writes no row of it (12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `document` (P5), `notice` (P6), `approval`, `decision_log_entry` and `rule_row` (P7), `partner` (S9), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_lot.buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document agreement fake | The sale agreement of lot `LOT-2027-000041` with its reference, its template and its template version; a run that answers no reference; a run that fails; no answer beyond 2 s | AC1, AC2, AC3, X4, X7 |
| rwb-comms notice fake | One issued notice per sold account with its type, `sent_date` and `barcode`; a notice stopped by the conduct check; a run that answers no reference; no answer beyond 2 s | AC1, AC2, X5, X7 |
| rwb-source-data addressee fake | The masked addressee fact of each sold account with its as-of date; an absent addressee; a stale fact; no answer beyond 2 s | AC1, AC2, X6 |
| rwb-case state fake | The case states `AWARD_PENDING`, `LOT_AWARDED` and `SETTLEMENT_PENDING` of case `RC-2027-000611`; a case in a state the rule does not name | AC2, X3 |
| rwb-case case-move fake | The move `LOT_AWARDED` accepted, and a move refused because the case is not in `AWARD_PENDING` | AC2, X3 |
| rwb-decision rule-package fake | The DS package at its version in force with R-DS-23, the 54 percent cap, the notice types and the templates | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2027-000041`, with the lot facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the rwb-document, rwb-comms, rwb-source-data and rwb-case operations and of the package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2996; ASM-4943).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-document agreement generation, the rwb-comms notice issue, the rwb-source-data addressee read, the rwb-case state read and move answer and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` is the award story's, `AccountsTransferred` the transfer story's and `ProceedsMatched` the settlement story's; this step holds no producer and no consumer |
| Temporal | 1 workflow, 1 branch, 1 activity, 1 run on the P5 queue | `DebtSaleWorkflow` and its R-DS-23 branch on `rwb-debtsale`, its `recordAwardAndIssueNotices` activity, and the document run started on `rwb-document`; no Schedule |
| File | 1 outbound, not built here | The WIN daily letters file (INT-14) is produced and handed over by rwb-comms and rwb-integration on the notice despatch; this service reads and writes no file (GAP-3000) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `award`, Java package `th.co.scb.ace.workbench.recovery.debtsale.award`; front end `src/modules/recovery/debtsale/DebtSaleAwardDocuments.tsx`, the fragment SCR-26 Award embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the references and the lot update commit together or not at all, and the failed write is MSG-P7-003. DP-05 is the customer fact of the notices, which this service reads on rwb-source-data's contract and never from `v_ace_customer`, the view the legacy data table names. DP-13 moves the base of the award screen and nothing else. DP-19 is how SCR-26 reaches this service, one hop through the gateway. No other pattern is claimed: the agreement and the notices are consumed contracts and not builds of this story, so DP-11 and DP-16 stay off this table and the absence of their rows from the plan's C row is recorded in the registers (GAP-2996).

**Dependencies the tables add and the plan does not hold.** The six consumed rows — the P5 agreement, the P6 notices, the P1 addressee, the P3 state read and move answer, and the P7 package — are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2996. The document run also adds a Temporal dependency on the P5 queue that no H or C row expresses.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` award branch | Workflow | The step of the saga that waits for the award confirmation, requests the agreement and the notices, applies R-DS-23 and reports the outcome to the parent |
| `recordAwardAndIssueNotices` | Activity | The one step: read the case and the lot, evaluate R-DS-23, write the record and the two lot columns, answer the case move |
| `AwardDocumentEvaluator` | Service | The rule evaluation against the DS package version in force, with the cap, the notice types and the templates as package and reference values |
| `SaleAgreementClient` | Client | The rwb-document generation and its reference; one hop, 2 s, breaker |
| `SaleNoticeClient` | Client | The rwb-comms notice issue and its references, sent dates and barcodes; one hop, 2 s, breaker |
| `CustomerAddresseeClient` | Client | The masked addressee read of rwb-source-data; one hop, 2 s, breaker (DP-05) |
| `DebtSaleDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID, the version, the agreement and notice references before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `DebtSaleAwardWriter` | Repository | Updates the two lot columns in one `rwb_debtsale` transaction, with the idempotency row and the optimistic lock |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `DebtSaleLotController` | Controller | The lot read of the awarded state, the capability area and right, the scope and the problem mapping of 400, 401, 403, 404 and 503 |
| `DebtSaleAwardDocuments` | React component | Shows the awarded lot, its signing date, its status and its agreement and notice references on SCR-26, read only |

**Database and migrations.** No Flyway file. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, and the decision record, the idempotency key and the outbox are library objects created in `rwb_debtsale` by the library's migration (DP-03). No column is added for the references: `signing_date` and `status` already exist as DF-SAL-027 and DF-SAL-030.

**Configuration and reference data.**

- `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The DS package and its version, authored, approved and versioned in rwb-decision (P7); the 54 percent cap and the 45-day turnaround target are values of the package and of reference data, not of this build.
- The notice types, the notice and agreement templates and their versions, held by rwb-comms and rwb-document and read through their contracts; no template text, no template version and no notice type is a constant of this build.
- The capability area "Debt sale" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The award branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the award confirmation as its trigger.
2. `CaseStateClient` and `CustomerAddresseeClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X6, X7).
3. `AwardDocumentEvaluator` over the DS package, with R-DS-23 and the no-fire path (AC2, X3).
4. `SaleAgreementClient` and the document run on the P5 queue, with the reference, the no-reference and the failed run paths (AC1, X4).
5. `SaleNoticeClient` and the notice issue, with the issued set, the conduct stop and the no-reference path (AC1, AC2, X5).
6. `DebtSaleDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
7. `DebtSaleAwardWriter` with the one transaction, the two columns, the idempotency row and the optimistic lock (AC2, X8).
8. `CaseMoveAnswer` and the parent signal, with the `LOT_AWARDED` move and its refusal (AC2, X3).
9. `DebtSaleLotController` with the rights, the scope and the problem mapping of 400, 401, 403, 404 and 503 (AC1).
10. `DebtSaleAwardDocuments` and SCR-26 through the composite route fake (AC1).
11. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to `rwb_document`, `rwb_comms`, `rwb_case`, `rwb_decision` or `rwb_source_data` (X9, BR3, BR4, BR6).

**Feature flag.** `rwb.debtsale.award-documents-v1`, read as a flag of the platform library; off means the branch holds the award confirmation, writes nothing, requests nothing and answers no move, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic award confirmation in SIT, R-DS-23 produces its record, its agreement, its notice set and its case-move answer, `signing_date` and `status` are written, a repeated confirmation writes once, a forced record failure changes nothing, no `document`, `notice`, `recovery_case` or `v_ace_*` read exists in the build, and SCR-26 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the exclusion path of RWB-S6-E5023-APP, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the award confirmation is absent or invalid, or the confirmation carries no date the sale was signed and no award reference (VR-S6-010-1) | Enter {field}. |
| MSG-P1-001 | The customer data product behind a notice is stale after a late or failed ACE batch, or carries no addressee for a sold account (VR-S6-010-1, X6) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the Debt sale right reads the awarded lot (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four legacy message IDs are those of the legacy message set of this key and of FSD S6 A2.10.3.1, and the text is the legacy and FSD wording, copied unchanged; MSG-P1-001 is the stale-data message of VR-S6-010-1, which the FSD carries for every feature of the module. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it. No message is reworded and no new one is added.

### 15. Screens and states

SCR-26 Award is the screen of this step: "Open; closed; awarded; transferred" of the legacy screen table, first in E6, and the awarded state is the one this story produces. It is served through the gateway-bff composite route (DP-19): the route calls rwb-debtsale for the lot, its signing date, its status and its references, rwb-case for the case and its route state and rwb-document and rwb-comms for the agreement and the notices the references point at. This story fixes the rwb-debtsale answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story shows are the awarded lot with its signing date and its references, the held state while the agreement or a notice has not answered, the refusal with MSG-P4-002, the not-recorded state with MSG-P7-003 and the stale-customer-data state with MSG-P1-001. The open, closed and transferred states of the legacy table are read as the case route state and the lot status together: `AWARD_PENDING` and `OFFERED` for open, `AWARDED` for awarded, and the transferred state belongs to RWB-S6-E6007-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-006-01 | AC1 | Component | The confirmed award of lot `LOT-2027-000041` for case `RC-2027-000611`; the agreement reference, the notice set, the decision record and the case move answered on the fakes |
| TC-E6-006-02 | AC2 | Integration | The award confirmation on a case at `AWARD_PENDING`; R-DS-23 fires, the agreement and the notices are issued, `signing_date` and `status` written and the `LOT_AWARDED` move asserted across the rwb-document, rwb-comms, rwb-source-data and rwb-case fakes |
| TC-E6-006-03 | AC3 | Component | The decision-record stub stopped; nothing written, no agreement and no notice requested, no move answered and MSG-P7-003 shown |
| TC-E6-006-04 | Access | Component | A role without the Debt sale right reads the awarded lot; 403 with MSG-P4-002 and no read |
| TC-E6-006-05 | Principle 5 | Component | A forced decision log write failure at the moment of the lot update; no column changed, no reference committed and no move answered |

The five legacy cases are the legacy cases of RWB-E6-006 in their legacy order, with the Level column added: the component cases run on the service's own fakes and TC-E6-006-02 maps to `Integration` because it crosses the rwb-document, rwb-comms, rwb-source-data and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the 54 percent cap, the 45-day target, the notice types, the templates and their versions, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input, in the decision record or in a log: identifiers, codes, amounts, dates and a rule version only, the addressee travels inside the notice request and nowhere else, and every fixture is synthetic.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant, reads no ACE table and reads the customer fact on rwb-source-data's contract (DP-01, DP-05).
- The agreement and the notices stay with their owners: no `document` row, no `notice` row, no template text and no conduct rule is written, copied or overridden here (BR3).
- The case stays with rwb-case and the package with rwb-decision: no `recovery_case` row, no ledger entry and no rule row is written here (BR2, BR5).
- The price test and the award operation stay with RWB-S6-E6005-APP: this story declares no operation, recomputes no price and writes no buyer column (BR7; GAP-2997).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second event on the topic and no notice or document table of this service's own.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve (Must, E6; FSD S6 requirements served). It is the nearest requirement row: no FSD requirement names the agreement or the notices, and TSD S6 T8 maps the FEAT-DBS rows to REQ-S6-001 to REQ-S6-009 without a row for FEAT-DBS-10 (GAP-2998; ASM-4945) | The award branch, the agreement and notice references, the two lot columns and the case move | TC-E6-006-01, TC-E6-006-02 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the awarded lot and the requester of its documents | TC-E6-006-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-006-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E6-006-02 |
| ADR-022 | Local decision record plus central ledger | The decision record with its references, written before the lot changes | TC-E6-006-03, TC-E6-006-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-006, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story |
| Test cases | TC-E6-006-01 to TC-E6-006-05 |
| Feature and screens | FEAT-DBS-10, SCR-26 Award |
| Rules | R-DS-23, with R-DS-19 as its predecessor and R-DS-24 as its successor, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |
| Source text | FSD S6 Debt sale v3 A2.10, TSD S6 Debt sale v2 T3, T4, T5 and Appendix T-A, Business Rules and Routing Logic v4, the legacy story master of Epics 3 to 8 v3 and the Feature List v4 rows FEAT-OCC-01, -02, -05 and -07 |

### 19. Out of scope

- The shape of the elements, the lists, the consumed rows, the rights, the error set and the fakes: RWB-S6-E6006-CON.
- The award operation API-S6-003, the price test R-DS-19, the `AwardRequest`, the buyer columns and the `LotAwarded` event: RWB-S6-E6005-APP (GAP-2997).
- The lot build, the estimate and the reserve: RWB-S6-E5024-APP; the eligible-account selection and the deviation exclusion: RWB-S6-E5023-APP.
- The data room, the tape, the masking and the bids: RWB-S6-E5026-APP and the take-bids story.
- The agreement's template, its generation, its custody and its retention: rwb-document (P5).
- The notices, their templates, the conduct check, the WIN despatch and the proof of delivery: rwb-comms (P6) and the P2 INT-14 file (GAP-3000).
- The customer fact and its masking policy: rwb-source-data (P1) and rwb-access (P4) (DP-05).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule package, its versioning, the approval chain and the ledger: rwb-decision (P7).
- The settlement term, the data transfer, derecognition and the general ledger posting: RWB-S6-E6007-APP and RWB-S6-E6008-APP.
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
