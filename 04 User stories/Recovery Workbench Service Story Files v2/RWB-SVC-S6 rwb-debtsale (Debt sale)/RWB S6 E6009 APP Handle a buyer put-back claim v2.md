# RWB-S6-E6009-APP Handle a buyer put-back claim

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-M |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S6-E6009-APP-16) |
| Depends on (build) | RWB-S6-E6009-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1 (path version of `/api/recovery/debtsale/v1`); the document version number is Not specified in the source documents (DOR-RWB-S6-E6009-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-009 split out for rwb-debtsale. The four legacy acceptance criteria are kept word for word with their origin tag; the put-back review becomes one activity of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which evaluates R-DS-35 on the claim, R-DS-36 or R-DS-38 on the sale terms, R-DS-37 on the return of the account and R-DS-34 on the claim window, writes the claim state against the sold account in `rwb_debtsale`, records the decision through the local decision-record library before the row changes (DP-03), answers rwb-case for the moves to `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED`, and serves the claim element to SCR-26 Award and PRT-05 Data room on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). TSD S6 appendix T-A publishes no put-back operation of its own, and the two legacy endpoint rows, the award path and the data room read, belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP; the transfer of R-DS-29 and the posting that creates `GL_POSTED` belong to RWB-S6-E6007-APP and RWB-S6-E6008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **to review a claim that an account should not have been sold, and settle or reject it**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-009, the FEAT-DBS-13 step of the S6 Debt sale module, and it is one step of the saga that the Temporal and Drools Design gives S6 ("Monthly sale cycle; Award within reserve and cap"; the saga runner is used by S2, S5, S6 and S7). It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they name;
- the put-back review of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case, under the DEBTSALE route set of 41 rules over 29 states;
- R-DS-35 on the claim, R-DS-38 on a claim outside the sale terms, R-DS-36 on a claim inside them, R-DS-37 on the return of the account and R-DS-34 on the claim window that closes the lot; R-DS-29 is tabled with them because the legacy criteria name it and its transfer precedes the claim window;
- the claim state of the sold account on `debt_sale_account.put_back_status` (DF-SAL-037 against `LOV-PUTBACK`), the account's `selling_price` (DF-SAL-036) and the lot status of `debt_sale_lot.status` (DF-SAL-030 against `LOV-LOT-STATUS`), in schema `rwb_debtsale`;
- the realized recovery by lot and by buyer that R-DS-34 and R-DS-39 record when the lot closes;
- the local decision record of every claim outcome, written through RWB-PLT-E1027-CON before any row changes (DP-03), which is what legacy AC1 and AC4 test;
- the answer to rwb-case for the moves `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED`, with the rule ID and the version that produced each move;
- the claim element served read only on `/api/recovery/debtsale/v1` (DP-13) to SCR-26 Award and PRT-05 Data room through the gateway-bff composite route (DP-19).

It does not own: the published shape of the claim and lot elements, the consumed rows, the case-move answer, the error set and the fakes, which are RWB-S6-E6009-CON; the transfer of the account data to the buyer under R-DS-29, which is RWB-S6-E6007-APP's; the derecognition and general ledger posting of R-DS-30 and R-DS-31 that create the `GL_POSTED` state, and the reversal on an upheld claim, which are RWB-S6-E6008-APP's; the settlement adjustment of an upheld claim, which is rwb-payment's (P8) and the settlement story's; the award operation API-S6-003 and its `DecisionLogEntry` answer, RWB-S6-E6005-APP's; the data room read API-S6-004 and its `DataRoom` answer, RWB-S6-E5026-APP's; the bid submission of API-S6-005; the buyer panel, the partner users and the buyer's identity, which are rwb-partner's (S9); the case of record, its route states and the parent `CaseWorkflow`, rwb-case's (P3); the central decision ledger and the rule rows, rwb-decision's (P7); the capability area and the right, rwb-access's (P4); the sale documents and the notices, rwb-document's (P5) and rwb-comms's (P6); the read model that R-DS-34's "Power BI" names under the monolith, rwb-reporting's (P9); and the deployment of this build, the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-009 gave the Workbench one step that reviewed a claim that an account should not have been sold and settled or rejected it, and the FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.13.1). The program keeps the requirement as REQ-S6-009, "A put-back claim from a buyer is reviewed against the sale terms and either accepted or refused with a reason" (FSD S6 Requirements served). The FSD glossary defines the object: "Put-back — a buyer returning an account under the sale terms".

What D-RCV-60 changes is where each fact of the claim lives and who acts on it.

- **The claim is a fact of the sold account, and the account set is this service's.** `debt_sale_account.put_back_status` with `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`) is the only claim column in TSD S6 T3.1 and it is S6's. The review therefore writes here, and the case moves are answered to rwb-case, which owns `recovery_case` and every route state (GAP-3008; ASM-4975).
- **The claim arrives through the partner channel, and no operation publishes it.** TSD S6 appendix T-A publishes five operations and none is a claim or a claim decision; the two endpoint rows of the legacy story are the award path API-S6-003 and the data room read API-S6-004, which are two sibling stories' (GAP-3008; ASM-4970).
- **Two of the four criteria execute rules that sit in sibling stories.** AC2 is R-DS-29, the transfer step of RWB-S6-E6007-APP, and AC3 starts from `GL_POSTED`, which R-DS-30 and R-DS-31 create in RWB-S6-E6008-APP; the criteria stay here word for word because the plan assigns them here, and the sibling activity is faked (GAP-3008; ASM-4973).
- **The claim window has no value and no column.** R-DS-34 fires on `CLAIM_WINDOW_CLOSED` with the timer "per claim window", and neither the workbook, the FSD nor the TSD gives its length. It is read as a parameter with its version and is never a constant of the build (GAP-3008; ASM-4971).
- **Realized recovery has no column and no event.** R-DS-34 and R-DS-39 record recovery by lot and by buyer; neither table carries such a column, the service's only event is EV-23 `LotAwarded`, and DP-17 removes the data lake and Power BI behind it. The figure is held on the lot and account rows and served on the lot read, and the reporting path is recorded (GAP-3008; ASM-4972).
- **The decision is recorded first**, through the local library of DP-03 in the same transaction as the claim change, which is what legacy AC1 asked for and what legacy AC4 tested.
- **The wave is EP06's and the service is wave 3.** §R5.6 keeps the W-MAP wave of a story when it is later than the service's Arch v5 wave, so this story is wave 4 while rwb-debtsale is created in wave 3; the conflict is recorded once for the service and the business epic (GAP-3008; ASM-4974).

No business value moves: the `LOV-PUTBACK` and `LOV-LOT-STATUS` values, the claim-window parameter, the 10-working-day review target of R-DS-35 and the sale terms are reference data, parameters and rule rows, read with their version.

### 3. Preconditions

- RWB-S6-E6009-CON is published: the claim, lot and account elements, the closed lists, the six consumed rows, the case-move answer, the error set and the fakes are baselined and handed to this story.
- The rwb-partner contract of the buyer, the sale terms and the claim is published with its fake, so a claim can be read on Day 1. Its operation names are Not specified in the source documents (GAP-3008; ASM-4969), and the row is not in this story's contract-dependency list, which is None.
- The rwb-case state read and the case-move answer are available for the fake: the states `SETTLED`, `DATA_TRANSFERRED`, `GL_POSTED`, `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED` are read and answered, never written here. No source publishes a REST operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3008; ASM-4975).
- The Debt sale rule package is in force at its version with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- The claim-window parameter and its version are in force. The default ruling gives parameters to rwb-case (P3) and DP-06 is not in this story's pattern set, so the value is read through the parameters contract with a placeholder for its operation name and is stated here rather than built as a guard (GAP-3008; ASM-4971).
- The access contract of rwb-access (P4) answers the capability area "Debt sale" with its right and the scope of the caller, so a role without it is refused before any read.
- The RuleAndParameterClient reads the package in force from rwb-decision and the claim-window parameter from rwb-case, each with its version; the two rows are separate clients and separate fakes.
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the claim change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award and PRT-05 Data room reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration of its own.
- The service runs as its own login on schema `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_partner`, `rwb_payment` or `rwb_decision` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6009-CON when its tests pass.

### 4. Flow

1. A lot is awarded, settled and its account data transferred; the claim window of R-DS-34 opens at `GL_POSTED`. This story reads those states and owns none of them: the transfer is RWB-S6-E6007-APP's, the posting that creates `GL_POSTED` is RWB-S6-E6008-APP's, and the settled lot and signed sale terms arrive on the lot and account rows (GAP-3008; ASM-4973).
2. A buyer raises a claim against one sold account inside the sale terms. The claim reaches the Workbench through the partner channel and the partner portal; the claim read on the rwb-partner contract gives the claim reference, the sold account reference, the sale terms in force and the buyer organisation, and no operation of TSD S6 T-A carries it (GAP-3008; ASM-4970).
3. The claim branch of `DebtSaleWorkflow` on queue `rwb-debtsale` signals the review with the lot and the account, and reads the case state on the rwb-case contract to confirm that the case is in `GL_POSTED`.
4. `PutbackClaimEvaluator` loads the Debt sale package version in force from rwb-decision and applies R-DS-35: the claim is inside the sale terms and the case is in `GL_POSTED`. Where the claim falls outside the terms on its face, R-DS-38 applies rather than R-DS-35.
5. `PutbackDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the case reference, the lot reference, the account reference, the claim reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
6. `PutbackClaimWriter` records the claim in one `rwb_debtsale` transaction: `put_back_status = CLAIMED` on the `debt_sale_account` row (DF-SAL-037), the account and lot references, the claim reference in the decision record, the idempotency row, and the optimistic lock on `version`. The buyer and the terms are referenced, never copied.
7. The step answers rwb-case with the move `PUTBACK_RAISED`, the rule ID, the version and the decided-at time. rwb-case writes the case row and its route state; this service writes neither.
8. On the decision inside the sale terms, R-DS-36 is applied: `put_back_status = ACCEPTED` (DF-SAL-037), the account is returned to the bank, and the step answers the move `PUTBACK_UPHELD`. R-DS-37's reversal of the derecognition and the settlement adjustment are the GL story's and rwb-payment's, and are recorded here as answered facts (GAP-3008; ASM-4973).
9. On a decision outside the sale terms, R-DS-38 is applied: `put_back_status = REJECTED` with the reason in the decision record, and the step answers the move `PUTBACK_REFUSED`.
10. When the claim window closes with no put-back claim inside it, R-DS-34 is applied: the lot moves to `status = CLOSED` (DF-SAL-030), the realized recovery is recorded by lot and by buyer from `selling_price` (DF-SAL-036) and the account set, and the step answers the move `LOT_CLOSED`. R-DS-39 applies the same close to a lot whose one claim was refused. The figure has no column of its own and no event, and both are recorded (GAP-3008; ASM-4972).
11. A repeated claim, a repeated decision or a repeated claim-window close with the same claim reference or `Idempotency-Key` writes nothing, answers no second move and counts the repeat; a claim on a lot that is not in `GL_POSTED` is refused with 409 and writes nothing.
12. The claim element is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award and for PRT-05 Data room through the gateway-bff composite route: the lot reference, the account reference, the claim reference, the claim state against `LOV-PUTBACK`, the rule ID with its version and the decided-at time, with no personal data (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no claim state, no lot close and no case-move answer leaves the service | MSG-P7-003 | AC1, AC4, TC-E6-009-04, TC-E6-009-06 |
| X2 | The role does not hold the Debt sale right of the capability area | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E6-009-05 |
| X3 | The case is not in the state the rule expects (`GL_POSTED` for R-DS-35 and R-DS-34, or one claim per account) | 409 and nothing is written; a second claim on the same account does not overwrite the first | None | AC1, AC3 |
| X4 | The ACE product that carries the account balance is stale after a late or failed batch | The step holds, writes nothing and shows the data date; the review resumes on the next fresh answer | MSG-P1-001 | AC1, AC3 |
| X5 | The rwb-partner, rwb-case or rwb-access contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC3, AC8, AC9 |
| X6 | The claim lies plainly outside the sale terms | R-DS-38 refuses it with the reason recorded and the move `PUTBACK_REFUSED`; nothing is returned to the bank here | None | AC1 |
| X7 | The claim window parameter or its version is absent, or the window cannot be resolved | No rule fires: the lot is not closed, nothing changes and the reason is reported to the parent | None | AC3 |
| X8 | A claim, a decision or a claim-window close arrives twice for the same lot, account and reference | One row, one answer and one decision record; the repeat is counted | None | AC1, AC3 |
| X9 | A component, a statement or a test reaches `rwb_case`, `rwb_partner`, `rwb_payment`, `rwb_decision` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E6-009-09, Section 17, BR8 |

X1 to X3 and X6 are the exception paths of RWB-E6-009 carried onto the split, X4, X5, X7 and X8 are the paths the target call types, the parameter and the idempotency rule add, and X9 is the DP-01 boundary. The claim-window length and the list values are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6009-CON, the rwb-partner, rwb-case and rwb-access fakes, the rwb-decision package fake and the decision-record stub, on its own schema, and needs no live P3, P4, P7, P8 or S9 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the claim element and the two tables are fixed |
| Valuable | A buyer's claim is settled or rejected with a recorded reason, and the lot closes with its realized recovery recorded, in the service that owns the sold account |
| Estimable | One workflow step, one evaluator, one record write, two claim writes, one lot close, one case-move answer, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots, claims and accounts through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Handle a buyer put-back claim

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL" and the sold account "ACC-2026-000451"
    Given the Debt sale rule package is in force at its version and carries R-DS-29, R-DS-34, R-DS-35, R-DS-36, R-DS-37, R-DS-38 and R-DS-39
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Handle a buyer put-back claim (legacy RWB-E6-009 AC1)
    Given the rwb-partner contract mock returns the put-back claim "PB-2026-000017" on the sold account "ACC-2026-000451" with the sale terms of the lot
    Given the rwb-case contract mock returns the case state "GL_POSTED" for "RC-2026-000842"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then reviews a claim that an account should not have been sold, and settles or rejects it
    Then the system writes one decision record with the rule ID R-DS-35 and its rule package version, and answers the case move PUTBACK_RAISED

  Scenario: AC2 Rule R-DS-29 (legacy RWB-E6-009 AC2)
    Given the rwb-case contract mock returns the case state "SETTLED" for "RC-2026-000842"
    Given a case in state SETTLED
    When data transfer run
    Then transfer the account data to the buyer
    Then the case moves to DATA_TRANSFERRED

  Scenario: AC3 Rule R-DS-34 (legacy RWB-E6-009 AC3)
    Given the rwb-case contract mock returns the case state "GL_POSTED" for "RC-2026-000842"
    Given a case in state GL_POSTED
    When claim window closed
    Then close the lot and record realized recovery by lot and by buyer
    Then the case moves to LOT_CLOSED

  Scenario: AC4 Not recorded (legacy RWB-E6-009 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 A statement that reaches another service's schema is refused (new, D-RCV-60)
    Given a component statement reaches the schema of `rwb_case`
    When the build runs the boundary test
    Then the grant refuses the statement and the build fails

  Scenario: AC6 Rule R-DS-37 returns the upheld account to the case list (new, D-RCV-60)
    Given the rwb-case contract mock returns the case state "PUTBACK_UPHELD" for a fixture case
    Given a case in state PUTBACK_UPHELD
    When account returned
    Then reverse the derecognition and return the account to the case list

  Scenario: AC7 Rule R-DS-39 closes the lot of a refused claim (new, D-RCV-60)
    Given the rwb-case contract mock returns the case state "PUTBACK_REFUSED" for a fixture case
    Given a case in state PUTBACK_REFUSED
    When claim closed
    Then close the lot with realized recovery recorded
    Then the case moves to LOT_CLOSED

  Scenario: AC8 A timed-out activity retries on the workflow's schedule (new, D-RCV-60)
    Given the rwb-partner contract mock does not answer inside 2 s for a fixture claim
    When the activity `reviewPutbackClaim` times out
    Then the activity retries on the workflow's own schedule and nothing is written

  Scenario: AC9 A failed consumed call writes nothing and answers no move (new, D-RCV-60)
    Given the rwb-case contract mock fails for a fixture case with its breaker open
    When the step is called
    Then nothing is written, no move is answered and the caller sees 503 with the platform error envelope
```

The four criteria are the legacy criteria of RWB-E6-009 word for word, except that `decision log` is written `decision record`: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision record cannot be written`, `data transfer run`, `claim window closed` and `the user acts on the screen` all stand, and nothing is reworded or dropped. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one `Given the <service> contract mock returns <x>` line, and those added `Given` lines and the Then line of AC1 that names its values are the only additions to the legacy text. The legacy words `decision log` in these lines are written `decision record`, the name of the record of sections 11 and 12.7 in the target; every other legacy word stands unchanged. AC5 to AC9 are the criteria this story adds and have no legacy origin: AC5 covers exception X9 of section 5, AC6 covers rule R-DS-37, AC7 covers rule R-DS-39, AC8 the retry and timeout of X5 and AC9 the failed call of X5.

What the legacy lines describe happens in four places in the target. The claim and the sale terms are rwb-partner's (S9), read on its contract and never as a table. The claim state is this service's, on `debt_sale_account.put_back_status` against `LOV-PUTBACK`, and the lot status on `debt_sale_lot.status` against `LOV-LOT-STATUS`. The case moves `DATA_TRANSFERRED`, `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED` are **answered** to rwb-case, which writes the `recovery_case` row and its route state. Two points are recorded rather than smoothed over: AC2's transfer is the transfer step of RWB-S6-E6007-APP and AC3's `GL_POSTED` is created by RWB-S6-E6008-APP, so both are faked here while the criteria stay owned by this story; and the realized recovery of AC3 has no column and no event, so it is held on the account's `selling_price` and the closed lot and recorded as such (GAP-3008; ASM-4972; ASM-4973). The buyer is an organisation and the fixture data is synthetic: no name, identity number, date of birth or contact value appears in a fixture, and the account is carried by its masked reference.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-29 | Debt sale | D8.4 | SETTLED | DATA_TRANSFER_RUN | Any | Transfer the account data to the buyer | DATA_TRANSFERRED | Workbench | buyer portal | 5 working days |
| R-DS-34 | Debt sale | D8.4 | GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | Close the lot and record realized recovery by lot and by buyer | LOT_CLOSED | Debt sale officer | Recovery Data Store, Power BI | per claim window |
| R-DS-35 | Debt sale | D8.4 | GL_POSTED | PUTBACK_CLAIMED | buyer raises a claim inside the sale terms | Record the claim and review it against the terms | PUTBACK_RAISED | Debt sale officer | buyer portal, Decision Log | 10 working days |
| R-DS-36 | Debt sale | D8.4 | PUTBACK_RAISED | PUTBACK_ACCEPTED | the claim is valid under the sale terms | Return the account to the bank and adjust the settlement | PUTBACK_UPHELD | Debt sale officer | ALS core and GL, buyer portal | None |
| R-DS-37 | Debt sale | D8.4 | PUTBACK_UPHELD | ACCOUNT_RETURNED | Any | Reverse the derecognition and return the account to the case list | BACK_TO_CASE_LIST | Case owner | ALS core and GL, Workbench | None |
| R-DS-38 | Debt sale | D8.4 | PUTBACK_RAISED | PUTBACK_REFUSED_BY_BANK | the claim falls outside the sale terms | Refuse the claim with a recorded reason | PUTBACK_REFUSED | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-39 | Debt sale | D8.4 | PUTBACK_REFUSED | CLAIM_CLOSED | Any | Close the lot with realized recovery recorded | LOT_CLOSED | Debt sale officer | Recovery Data Store | None |

The seven rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Each rule row carries its BR ID in the table that follows: R-DS-29 is BR11, R-DS-34 is BR12, R-DS-35 is BR13, R-DS-36 is BR14, R-DS-37 is BR15, R-DS-38 is BR16 and R-DS-39 is BR17. Their owner column is a role of the business and not a service: the claim state and the lot close are written here, the case route states are written by rwb-case on this story's answer, the claim and the sale terms are rwb-partner's, the transfer of R-DS-29 is RWB-S6-E6007-APP's, and the derecognition reversal of R-DS-37 and the settlement adjustment of R-DS-36 are RWB-S6-E6008-APP's and rwb-payment's. R-DS-29 is tabled because AC2 names it and no claim can be raised before the account data is transferred; the transfer itself is not this story's step.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The claim fact is this service's: `put_back_status`, `selling_price` and the lot `status` are columns of `debt_sale_account` and `debt_sale_lot` in `rwb_debtsale`, and no other service writes them | Architecture v5 slide 41 (rwb-debtsale owns lots, data room, buyer terms, bids, award, transfer); TSD S6 T3.1; GAP-3008 | AC1, AC3, TC-E6-009-01, TC-E6-009-03 |
| BR2 | The decision is recorded before the claim row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E6-009 AC1 and AC4 | AC1, AC4, TC-E6-009-04, TC-E6-009-06 |
| BR3 | The claim, the sale terms and the buyer stay with rwb-partner (S9): this story reads no `partner`, `partner_user` or sale-terms table and takes the facts on the owner's contract only | Architecture v5 slide 41; Ownership Map (`partner` and `partner_user` owner S9); GAP-3008 | AC1, TC-E6-009-01, TC-E6-009-07 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; ASM-4975 | AC1, AC3, TC-E6-009-01, TC-E6-009-03 |
| BR5 | One account carries one claim state: a second claim on the same account is refused with 409 and does not overwrite the first; the state follows `LOV-PUTBACK` only | TSD S6 T3.2 (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`); R-DS-35 to R-DS-38 | AC1, AC3 (through X3) |
| BR6 | The claim window and the review target are parameters read with their version, and no list value or window length is a constant of the code; the window length and the operation that reads it are Not specified in the source documents (GAP-3008) | FSD S6 BR-S6-013; R-DS-34 ("per claim window") and R-DS-35 (10 working days); GAP-3008 | AC3, TC-E6-009-03 |
| BR7 | The realized recovery of a closed lot is the sum of the `selling_price` of its account set, held on the lot and account rows; no separate column and no event exists for it; a reporting contract for it is Not specified in the source documents (GAP-3008) | R-DS-34 and R-DS-39; TSD S6 T3.1; ASM-4972 | AC3, AC7, TC-E6-009-03 |
| BR8 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 (relationships inside the module only) | AC5, TC-E6-009-08, TC-E6-009-09 |
| BR9 | This story declares no REST operation of its own: the review is reached through the lot read and the data room read of its siblings, and the claim is read on the rwb-partner contract | TSD S6 T-A.1; GAP-3008; ASM-4970 | TC-E6-009-07, AC1 |
| BR10 | No person name, identity number, date of birth, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) | AC1, TC-E6-009-01 |
| BR11 | R-DS-29 (SETTLED to DATA_TRANSFERRED on DATA_TRANSFER_RUN): the account data is transferred to the buyer; the transfer is RWB-S6-E6007-APP's step | Business Rules and Routing Logic v4, row R-DS-29 | AC2, TC-E6-009-02 |
| BR12 | R-DS-34 (GL_POSTED to LOT_CLOSED on CLAIM_WINDOW_CLOSED): the lot is closed and its realized recovery recorded | Business Rules and Routing Logic v4, row R-DS-34 | AC3, TC-E6-009-03 |
| BR13 | R-DS-35 (GL_POSTED to PUTBACK_RAISED on PUTBACK_CLAIMED): the claim is recorded and reviewed against the sale terms | Business Rules and Routing Logic v4, row R-DS-35 | AC1, TC-E6-009-01 |
| BR14 | R-DS-36 (PUTBACK_RAISED to PUTBACK_UPHELD on PUTBACK_ACCEPTED): the account is returned to the bank and the settlement adjusted | Business Rules and Routing Logic v4, row R-DS-36 | AC1, TC-E6-009-01 |
| BR15 | R-DS-37 (PUTBACK_UPHELD to BACK_TO_CASE_LIST on ACCOUNT_RETURNED): the derecognition is reversed and the account returned to the case list | Business Rules and Routing Logic v4, row R-DS-37 | AC6, TC-E6-009-10 |
| BR16 | R-DS-38 (PUTBACK_RAISED to PUTBACK_REFUSED on PUTBACK_REFUSED_BY_BANK): the claim is refused with a recorded reason | Business Rules and Routing Logic v4, row R-DS-38 | AC1, X6, TC-E6-009-01 |
| BR17 | R-DS-39 (PUTBACK_REFUSED to LOT_CLOSED on CLAIM_CLOSED): the lot is closed with realized recovery recorded | Business Rules and Routing Logic v4, row R-DS-39 | AC7, TC-E6-009-11 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story owns is the claim state of the sold account and the state of the lot.

| From (claim state of the sold account) | Event | Condition | To |
|---|---|---|---|
| NONE | A claim arrives under R-DS-35 | The case is in `GL_POSTED` and the claim is inside the sale terms | CLAIMED, with the case-move answer `PUTBACK_RAISED` |
| NONE | A claim arrives that falls outside the sale terms | R-DS-38 on its face | REJECTED with the reason recorded, with the case-move answer `PUTBACK_REFUSED` |
| CLAIMED | The decision under R-DS-36 | The claim is valid under the sale terms | ACCEPTED, with the case-move answer `PUTBACK_UPHELD` |
| CLAIMED | The decision under R-DS-38 | The claim falls outside the sale terms | REJECTED with the reason recorded, with the case-move answer `PUTBACK_REFUSED` |
| NONE | The claim window closes under R-DS-34 | No put-back claim inside the window | Unchanged on the account; the lot closes and the answer is `LOT_CLOSED` |
| ACCEPTED, REJECTED | The claim window closes under R-DS-39 or R-DS-34 | The lot is in `GL_POSTED` | Unchanged on the account; the lot closes and the answer is `LOT_CLOSED` |
| Any | A repeated claim, decision or close for the same reference | X8 | Unchanged, the repeat is counted |

| Lot status | Event | Condition | To |
|---|---|---|---|
| TRANSFERRED | The transfer completes under R-DS-29, the transfer story's step | Any | Unchanged here; the case moves to `DATA_TRANSFERRED` and then to `GL_POSTED` |
| GL_POSTED | A claim inside the window under R-DS-35 | One claim per account | Still open for the window; the claim state is CLAIMED |
| GL_POSTED | The claim window closes under R-DS-34, or the claim is refused under R-DS-39 | No claim inside the window, or the one claim refused | CLOSED, with the realized recovery recorded |

The route states `SETTLED`, `DATA_TRANSFERRED`, `GL_POSTED`, `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED`, `BACK_TO_CASE_LIST` and `LOT_CLOSED` are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria, and they live on the case of record except `LOT_CLOSED`, which is answered with the lot close. The claim states are those of `LOV-PUTBACK` and the lot states those of `LOV-LOT-STATUS` in TSD S6 T3.2. This story adds no value to either closed list; the route states above are case-of-record moves of the DEBTSALE machine, not members of `LOV-LOT-STATUS` or `LOV-PUTBACK`.

SCR-26 states for the claim element: the empty state is Not specified in the source documents (DOR-RWB-S6-E6009-APP-10); the loading state is Not specified in the source documents (DOR-RWB-S6-E6009-APP-10); the error state shows MSG-P7-003 when the decision record is stopped (TC-E6-009-04); the no-access state shows MSG-P4-002 with no read (TC-E6-009-05).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role of the feature, holding C, R, U and A; records the claim, decides it and closes the lot |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the claim and approves through the approval path where a claim needs it; the DoA approval itself is `ApprovalWorkflow` of rwb-decision (P7) |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: the approval authority of the sale and of an upheld claim; the authority itself is a parameter of the package |
| PT-BUYER, debt buyer and AMC | Partner portal RU, own lots only and scoped: raises a claim and reads its own outcome; sees no other buyer's claim |
| PT-RAMC | Partner portal R: reads its own lots and the claim state of its own accounts |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the step, evaluates the rules, writes the decision record, the claim state and the lot close, answers the case move and serves the claim element; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission table gives the Partner portal right R to the internal case roles with a long role list; in the target that read is the partner's own, scoped to its lots, and the internal roles read the same claim element on SCR-26 Award under their Debt sale right. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface, and the guard of the access service is a service-template capability (GAP-3008; ASM-4969).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the claim and the close are recorded against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the screen answer |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read, the window is counted from the cut-off and the transfer |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024, DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price, payment_terms | Read only: the sale terms are the buyer's contract fact and the settlement adjustment is rwb-payment's |
| DF-SAL-025, DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id, buyer_class | Read, the buyer the claim is raised by, against `LOV-BUYER-CLASS` |
| DF-SAL-027, DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date, approval_authority | Read, the signed sale the claim is judged against |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, against `LOV-LOT-STATUS`, to CLOSED on R-DS-34 and R-DS-39 |
| DF-SAL-031, DF-SAL-032, DF-SAL-033, DF-SAL-034 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code | Read, the sold account the claim is raised on |
| DF-SAL-035 | debt_sale_account (S6, `rwb_debtsale`) | outstanding | Read, the balance the realized recovery is measured against (source Core bank (ALS) via COLLINS) |
| DF-SAL-036 | debt_sale_account (S6, `rwb_debtsale`) | selling_price | Read, the realized recovery by lot and by buyer of R-DS-34 |
| DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | put_back_status | Write, against `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`) |
| Standard columns | debt_sale_lot, debt_sale_account (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case move, decided at | Write through the local library, before the claim row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case contract and the move is answered to it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rule rows arrive in the package in force from rwb-decision |
| DF-REF-034 to DF-REF-038 | role (P4) | id, role_code, role_name, role_class, default_scope | Not read as a table: the capability area and the right are answered by rwb-access |
| The claim and the sale terms | partner and instructor (S9) | claim reference, sold account reference, sale terms in force, buyer organisation | Not read as a table: the facts arrive on the rwb-partner contract, and no personal data of any person is read (GAP-3008; ASM-4969) |

Field IDs are those of TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v9. The four rows of the legacy Data table, `recovery_case`, `assignment`, `decision_log_entry` and `rule_row`, are the rows of other owners in the target: `recovery_case` and `assignment` are P3's, `decision_log_entry` and `rule_row` are P7's, and this story reads none of them as a table. **No new table, no new column and no migration**: this story writes two existing columns and reads the rest, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration.

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. The buyer is a partner organisation: no name, no identity number, no date of birth, no address and no contact value enters `rwb_debtsale`, the decision record, a log, an event or a workflow input, the account is carried by its masked reference, and the fixture data of the tests is synthetic. Any field of the table above that Data Classification v5 classes as personal data is read only as a code or reference and is never written, logged or passed to an event or workflow input.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids`, and none of them is a claim or a claim-decision operation. The two endpoint rows of the legacy story are API-S6-003 and API-S6-004, which belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP. This story therefore provides no operation of its own, claims no sibling's operation, and is reached through the lot read and the data room read; the claim itself arrives on the rwb-partner contract. The absence is recorded as GAP-3008 with ASM-4970.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The buyer claim read (operation name Not specified in the source documents (GAP-3008; ASM-4969)) | `/api/recovery/partner/v1` | S9 rwb-partner | The claim reference, the sold account reference, the sale terms in force and the buyer organisation; read only, faked. The read family of the Ownership Map is `GET /partners` |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the lot and account link, read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3008; ASM-4969)) | rwb-case (P3) | P3 rwb-case | The move `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED`, `BACK_TO_CASE_LIST` or `LOT_CLOSED` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3008; ASM-4969)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Debt sale" with right C, R, U or A and "Partner portal" with right R, and the scope of the caller; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39; read only, faked |
| The claim-window parameter and its version (operation name Not specified in the source documents (GAP-3008; ASM-4971)) | `/api/recovery/case/v1` | P3 rwb-case | The claim-window parameter of R-DS-34 and R-DS-39 at its version, on the parameters contract the default ruling gives rwb-case; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3008 with ASM-4969.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (EV-23, consumers rwb-case and rwb-payment) and `AccountsTransferred`, and this story produces neither: `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. The claim outcome and the lot close are answered to rwb-case on the move, and the realized recovery is held on the lot and account rows because the service's event set carries no recovery event (GAP-3008; ASM-4972). This story writes no outbox row, opens no producer and declares no event of its own, and a build that publishes one fails the absence test.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched`, which belongs to the settlement step of this service, and no event of the module carries a buyer claim or a claim-window close; the window is a durable timer of the workflow, not an event. This story therefore holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement and the claim window | `rwb-debtsale` | Input: the lot, the case, the claim and the rule package in force; signals: the claim, the claim decision and the case state answered by rwb-case; the claim-window timer is a durable timer of this workflow |
| `reviewPutbackClaim` | Activity, the one claim step of this story | `rwb-debtsale` | The lot, the case, the account and the claim in; the rule ID with its package version, the claim state, the lot close, the realized recovery and the case move out, with the decision record and the claim update in one transaction |
| `closeLotOnClaimWindow` | Activity, the claim-window close of R-DS-34 and R-DS-39 | `rwb-debtsale` | The lot, the account set and the window parameter in; the lot close, the realized recovery by lot and by buyer and the case move out |

No child workflow for the case and no workflow for the money exists in this service. The activity names are a target design choice of this story and are fixed by no source document. The saga steps of the workflow — reserve accounts, approve sale, buyer pays, transfer accounts, post proceeds, close cases and tell customers — belong to the award, settlement, transfer and posting stories of this service; this story owns the claim step and the claim-window close alone.

Workflow ID form for `DebtSaleWorkflow`: Not specified in the source documents (CG-ALL-10733). Start rule: the catalog trigger is 'The monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)'; the start mode and the duplicate-start policy are Not specified in the source documents (CG-ALL-10733).

#### 12.6 Schedules

None. The step runs from the claim and from a durable timer of the workflow, and owns no Temporal Schedule and no legacy Quartz job; the monthly debt sale cycle and the overnight jobs of Architecture v5 slide 44 are not owned, moved or registered here. The claim window of R-DS-34 is a timer of this workflow and not a Schedule, because it is per lot and starts at the posting.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer, its terms and its status; this story writes `status` and reads the rest |
| debt_sale_account | S6 (`rwb_debtsale`) | The sold account, its `outstanding`, its `selling_price` and its `put_back_status`; this story writes `put_back_status` and reads the rest |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated claim or close and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this step writes no row to it (ASM-4972) |

Not owned and never read as a table: `recovery_case` and `assignment` (P3), `partner`, `partner_user` and the sale-terms rows (S9), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` and the settlement rows (P8), the rwb-reporting read model (P9) and every `v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_lot.buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner claim fake | The claim `PB-2026-000017` on the sold account `ACC-2026-000451` inside the sale terms, the same claim outside them, a claim on a lot that is not in `GL_POSTED`, no claim, and no answer beyond 2 s | AC1, X3, X5, X6 |
| rwb-case state fake | The states `SETTLED`, `DATA_TRANSFERRED`, `GL_POSTED`, `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED` of case `RC-2026-000842`, and a case that is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED`, `BACK_TO_CASE_LIST` and `LOT_CLOSED` accepted, and a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-access authorise fake | The capability area "Debt sale" with right C, R, U or A and "Partner portal" with right R for `PT-BUYER`, scoped to its own lot; a role and a partner identity without the right | AC1, X2 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39 | AC1, AC3 |
| rwb-case claim-window parameter fake | The claim-window parameter at its version in force, and a parameter set without the window | AC3, X7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC1, AC4, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award and PRT-05 answers for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the claim element once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner claim read, the rwb-case move answer, the rwb-access authorise call and the rwb-decision parameter read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3008; ASM-4969).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-partner claim read, the rwb-case state read and move answer, the rwb-access authorise call, the rwb-decision package read and the rwb-case claim-window parameter read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` (EV-23) and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the settlement step's; no claim event exists |
| Temporal | 1 workflow and 2 activities | `DebtSaleWorkflow`, `reviewPutbackClaim` and `closeLotOnClaimWindow` on `rwb-debtsale`; the claim window is a durable timer, not a Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the partner portal and no file of this step leaves the bank |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `putbackclaim`, Java package `th.co.scb.ace.workbench.recovery.debtsale.putbackclaim`; front end `src/modules/recovery/debtsale/PutbackClaim.tsx`, the fragment SCR-26 Award and PRT-05 Data room embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the claim update commit together or not at all. DP-13 moves the base of the claim element and nothing else. DP-19 is how SCR-26 Award and PRT-05 reach this service, one hop through the gateway; the buyer's claim itself arrives over the partner channel, which has no plan row (GAP-3008; ASM-4970). DP-06 is not in the pattern set although the claim window is a parameter, DP-08 is not in it although the right is checked on every surface, and neither is added to the metadata rows; both are named here and in the registers (GAP-3008; ASM-4969; ASM-4971).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` claim branch | Workflow | The branch that waits for the claim, the decision and the window, loads the package in force and reports the outcome to the parent |
| `reviewPutbackClaim` | Activity | The one step: read the claim and the case, evaluate R-DS-35, R-DS-36 or R-DS-38, write the record and the claim state, answer the case move |
| `closeLotOnClaimWindow` | Activity | The close under R-DS-34 and R-DS-39: check the window against the parameter, close the lot, record the realized recovery and answer the move |
| `PutbackClaimEvaluator` | Service | The rule evaluation against the Debt sale package version in force, with the `LOV-PUTBACK` and `LOV-LOT-STATUS` values of the closed lists |
| `PutbackDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `PutbackClaimWriter` | Repository | Writes `put_back_status` on the `debt_sale_account` row and `status` on the `debt_sale_lot` row in one `rwb_debtsale` transaction, with the idempotency row and the optimistic lock |
| `PartnerClaimClient` | Client | The claim and sale-terms read of rwb-partner (S9), one hop, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `RuleAndParameterClient` | Client | The package in force and the claim-window parameter with their versions, from rwb-decision (P7) and rwb-case (P3) |
| `PutbackClaimController` | Controller | Serves the claim element on the service base with the capability area and right, and maps 400, 401, 403, 404, 409, 422 and 503; it declares no operation that TSD S6 T-A does not publish (GAP-3008; ASM-4970) |
| `PutbackClaim` | React component | Shows the claim state, the reason of a refusal and the closed lot on SCR-26 Award and PRT-05, read only |

**Database and migrations.** No Flyway file of this story. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, the decision record and the idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03), and no realized-recovery column is added here; the absence of that column is recorded (GAP-3008; ASM-4972).

**Configuration and reference data.**

- `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-BUYER-CLASS` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39 and the claim-window parameter, both with their versions, authored and approved in rwb-decision (P7); the 10-working-day target of R-DS-35 is a value of the package.
- The capability area "Debt sale" and its rights are access rows of rwb-access, read through the guard.
- No parameter of the claim step itself is named in the sources beyond the window; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The claim branch of `DebtSaleWorkflow` and its input record on `rwb-debtsale`, with the claim, the decision and the claim-window timer as its triggers.
2. `PartnerClaimClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, AC3, X4, X5).
3. `AccessGuardClient` and the two capability areas, with the refusal path (AC1, X2).
4. `RuleAndParameterClient` and `PutbackClaimEvaluator` over the package, with R-DS-35, R-DS-36, R-DS-38 and the no-fire path of an absent window (AC1, AC3, X7).
5. `PutbackDecisionRecordWriter` against the library stub, with the failed-write path (AC1, AC4, X1).
6. `PutbackClaimWriter` with the one transaction, the two columns, the idempotency row and the optimistic lock (AC1, X8).
7. `closeLotOnClaimWindow` with the window check, the lot close and the realized recovery by lot and by buyer (AC3).
8. `CaseMoveAnswer` and the parent signal, with the five moves (AC1, AC2, AC3).
9. `PutbackClaimController` with the rights and the problem mapping, declaring no unpublished operation, and `PutbackClaim` on the two screen fragments through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_debtsale`, no read of `recovery_case`, `assignment`, `partner`, `role`, `rule_row` or a `v_ace_*` view, and no write to another service's schema (X9, BR8, BR10).

**Feature flag.** `rwb.debtsale.putback-claim-v1`, read as a flag of the platform library; off means the step holds the claim, writes nothing and answers no move, and the award, transfer and posting stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic claim in SIT, each of the five rules produces its record, its claim state and its move, the lot closes with its realized recovery, a repeated claim or close writes once, a forced record failure changes nothing, no `recovery_case`, `assignment`, `partner` or `v_ace_*` read exists in the build, and SCR-26 Award and PRT-05 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account selected for a lot, which is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the claim or of the decision is absent or invalid (X3, X6) | Enter {field}. |
| MSG-P4-002 | A role or a partner identity without the right of the capability area raises, decides or closes a claim (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the claim row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE product that carries the account balance is stale after a late or failed batch (X4) | {product} is from {date}. Today's load has not arrived. |

The five message IDs are those of the legacy message set and of FSD S6 A2.13.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is worded as in Error and Message Standard v4 (Warning row). MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-26 Award in its open, closed, awarded and transferred states is served through the gateway-bff composite route (DP-19), and PRT-05 Data room, "Lot data tapes and documents for admitted buyers, with bids" (FSD S6 Screens), is served to the partner on the same service base through the partner gateway in the DMZ. The route calls rwb-debtsale for the lot, the account set and the claim element, rwb-case for the case and its route state and rwb-partner for the claim and the sale terms; this story fixes the claim element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces on the claim element are `CLAIMED`, `ACCEPTED` and `REJECTED` against `LOV-PUTBACK`, the closed lot against `LOV-LOT-STATUS`, the refusal reason and the rule version, and it shows the failure states it reads: refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001 and a case in the wrong state with 409. The award, settlement and transfer states of SCR-26 belong to the award, settlement and transfer stories and are read from the same route. The empty and loading states of SCR-26 are Not specified in the source documents (CG-ALL-10740); the error and no access states are those given in section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-009-01 | AC1 | Component | The claim `PB-2026-000017` on account `ACC-2026-000451` for lot `LOT-2026-000042`; the record, the claim state and the case move asserted on the fakes |
| TC-E6-009-02 | AC2 | Component | Case `RC-2026-000842` at `SETTLED`; the transfer answer of the sibling step and the `DATA_TRANSFERRED` move shape on the fakes |
| TC-E6-009-03 | AC3 | Integration | Case `RC-2026-000842` at `GL_POSTED` with the window closed and no claim; the lot closed with its realized recovery, and `LOT_CLOSED` answered end to end on the fakes |
| TC-E6-009-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-009-05 | Access | Component | A role and a partner identity without the Debt sale or the Partner portal right; 403 with MSG-P4-002 and no read |
| TC-E6-009-06 | Principle 5 | Component | A forced decision record write failure at the moment of the claim update; no claim change, no answer and no second attempt | 
| TC-E6-009-07 | §12 operations, events and activities | Contract | The section 12 contract checked against the published contract of each operation and event on the fakes; the rwb-partner, rwb-case and rwb-access answers as the contracts publish them |
| TC-E6-009-08 | §12.7 tables | Boundary | The tables of section 12.7 checked against the owned and not-owned lists: no write outside debt_sale_lot and debt_sale_account and no read of a not-owned table (ASM-3438) |
| TC-E6-009-09 | AC5 | Component | A component statement that reaches `rwb_case`, `rwb_partner`, `rwb_payment`, `rwb_decision` or another service's schema; the grant refuses it and the boundary test fails the build; nothing is released |
| TC-E6-009-10 | AC6 | Component | A fixture case at `PUTBACK_UPHELD`; the account returned to the case list and BACK_TO_CASE_LIST answered on the fakes |
| TC-E6-009-11 | AC7 | Component | A fixture case at `PUTBACK_REFUSED`; the lot closed with its realized recovery and LOT_CLOSED answered on the fakes |
| TC-E6-009-12 | AC8 | Component | The rwb-partner stub that does not answer inside 2 s for a fixture claim; the activity retried on the workflow's schedule, nothing written and no move answered on the fakes |
| TC-E6-009-13 | AC9 | Component | The rwb-case stub failing for a fixture case with its breaker open; nothing written, no move answered and 503 with the platform error envelope on the fakes |

The six legacy cases are the legacy cases of RWB-E6-009 in their legacy order, with the Level column added: the component cases map to `Component` because the step is tested on its fakes, and TC-E6-009-03 maps to `Integration` because it crosses the rwb-case boundary and the window. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and no `-ITG` copy is written here.

### 17. Guardrails

- No business value in code: the `LOV-PUTBACK`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-BUYER-CLASS` values, the claim-window length, the 10-working-day review target and the rule rows stay data, reference data, parameters or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, every fixture synthetic, and the account carried by its masked reference. The buyer is a partner organisation, so no name, identity number, date of birth or contact value is written.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test.
- The case stays with rwb-case, the claim and the sale terms with rwb-partner, the settlement adjustment with rwb-payment, the posting with the GL story and the central ledger with rwb-decision: no `recovery_case`, `assignment`, `partner`, `proceeds` or `decision_log_entry` row is written here (BR2, BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: the award path is RWB-S6-E6005-APP's and the data room read is RWB-S6-E5026-APP's, and a story that declares them as its own fails the review (GAP-3008).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data lake extract and no second event on the topic (DP-17).
- The decision is recorded before the change and the move is answered, not written; a build that writes a case row or records after the update fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S6-009 | A put-back claim from a buyer is reviewed against the sale terms and either accepted or refused with a reason (FSD S6 Requirements served; Business Requirements Program v5); the split plan carries no requirement id for this slice (GAP-3008; ASM-4969) | The claim step, R-DS-35, R-DS-36 and R-DS-38, the decision record and the claim state | TC-E6-009-01, TC-E6-009-04, TC-E6-009-06, TC-E6-009-10 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying; this story reads the transferred and posted state and closes the lot after it | The `DATA_TRANSFERRED` and `GL_POSTED` reads of AC2 and AC3, and the lot close | TC-E6-009-02, TC-E6-009-03, TC-E6-009-11 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the sold account and its claim state | TC-E6-009-01 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-009-06, TC-E6-009-08 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E6-009-01, TC-E6-009-03, TC-E6-009-07 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |
| ADR-022 | Local decision record plus central ledger | The decision record written before the claim changes | TC-E6-009-04, TC-E6-009-06 | FEAT-DBS-13 | Not specified in the source documents (DOR-RWB-S6-E6009-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-009, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-009-01 to TC-E6-009-06 |
| Feature and screens | FEAT-DBS-13 Handle a buyer put-back claim, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-29, R-DS-34 and R-DS-35 to R-DS-39, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022, and ADR-018 for the removed data lake behind R-DS-34 |

### 19. Out of scope

- The published shape of the claim, lot and account elements, the closed lists, the consumed rows, the error set and the fakes: RWB-S6-E6009-CON.
- The transfer of the account data to the buyer under R-DS-29 and its `DATA_TRANSFERRED` move: RWB-S6-E6007-APP (GAP-3008).
- The derecognition, the general ledger posting and the reversal under R-DS-30 and R-DS-31, which create `GL_POSTED` and reverse it on an upheld claim: RWB-S6-E6008-APP (GAP-3008).
- The settlement adjustment of R-DS-36 and the money side of the lot: rwb-payment (P8) and the settlement story of this service.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP.
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP; the bid submission API-S6-005: the take-bids story of this service.
- The claim, the sale terms, the partner users and the buyer's identity: rwb-partner (S9) (GAP-3008).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (ASM-4975).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3008).
- The central decision ledger, the rule rows, their approval, the claim-window parameter and its versioning: rwb-decision (P7) (ASM-4971).
- The read model and the reporting of realized recovery under the monolith's Power BI, which the target reaches from events or from the owner's contract: rwb-reporting (P9), with no event or contract allocated (GAP-3008; ASM-4972).
- The sale documents and the notices of a returned account: rwb-document (P5) and rwb-comms (P6); the partner gateway in the DMZ and the composite route: the edge stories and RWB-PLT-N001-CON.
- The debt buyers outside the bank, INT-25, which are reached through the partner portal and no adapter of this service.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
