# RWB-S6-E6010-APP Close a case awarded in a sold lot

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6010-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-010 split out for rwb-debtsale. The two legacy acceptance criteria are kept word for word with their origin tag; the closure becomes one step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which evaluates R-UNI-47 with the UNIVERSAL package in force when the lot is awarded, writes the decision record through the local decision-record library before anything changes (DP-03), answers rwb-case to stop every open action on the case and close it as sold, and carries the closure element read only on the service base `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). The case of record, its state, its tasks, its timers and its open route children stay with rwb-case (P3); the transfer of the account data stays with RWB-S6-E6007-APP and the derecognition and posting with RWB-S6-E6008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **the Workbench to stop every open action on a case whose account is sold in a lot, and close it**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-010, the FEAT-DBS-14 step of the S6 Debt sale module. It owns:

- the two legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screen states they depend on;
- the closure step of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slides 19 and 23; Temporal and Drools Design slide 13);
- the evaluation of R-UNI-47 of the UNIVERSAL route set, at the award confirmation of the lot, with the package version in force recorded with the outcome; R-DS-23 is tabled with it because its `AWARD_CONFIRMED` signal is the trigger of the step;
- the local decision record of the closure, written through RWB-PLT-E1027-CON before the case is closed (DP-03), which is what legacy AC1 and AC2 test;
- the answer to rwb-case, one per case of the awarded lot, that stops every open action on the case and closes it as sold with the rule ID, the version and the decided-at time;
- the closure element served read only on `/api/recovery/debtsale/v1` (DP-13) for SCR-26 Award in its closed state, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the closure element, the closure answer and its vocabulary, the consumed rows, the error set and the fakes, which are RWB-S6-E6010-CON; the award operation API-S6-003 `POST /debt-sale-lots/{lotId}/award` and its `DecisionLogEntry` answer, which are RWB-S6-E6005-APP's; the lot create and lot read operations API-S6-001 and API-S6-002, which are the lot stories'; the transfer of the awarded account data under R-DS-29, which is RWB-S6-E6007-APP's; the derecognition under R-DS-30 and the general ledger posting under R-DS-31, which are RWB-S6-E6008-APP's; the sale agreement and the customer notices under R-DS-23, which are RWB-S6-E6006-APP's and rwb-comms's and rwb-document's; the lot close under R-DS-34 and R-DS-39, which is the put-back story's; the case of record, its route states, its tasks, its timers and its open stage children, which are rwb-case's (P3); the deviation records and their pause of the stage clock, which are rwb-deviation's (S8); the central decision ledger, the rule rows and their approval, which are rwb-decision's (P7); the capability area, the right and the scope, which are rwb-access's (P4); the buyer panel, which is rwb-partner's (S9); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-010 gave the Workbench one step that stopped every open action on a case whose account is sold in a lot and closed it, and the FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.14.1). The program keeps the requirement as REQ-S6-007, "An account awarded in a lot stops every other open action on its case the same day" (Business Requirements Program v5).

What D-RCV-60 changes is who owns each fact the closure stands on. In the monolith the case, its tasks, its timers, the decision log and the lot sat in one `recovery` schema and one process. In the target:

- **the case of record stays with rwb-case (P3).** `recovery_case`, its route state, its tasks, its timers and the child workflows of the other routes are rwb-case's; this story evaluates the rule, writes its own record and **answers** the closure with the end state `CASE_CLOSED_SOLD`, and rwb-case applies it (GAP-3010; ASM-4976).
- **the trigger is the award, not a screen.** R-UNI-47 fires on `ACCOUNT_IN_SOLD_LOT`, and R-DS-23 records `AWARD_CONFIRMED` at the price test. The step therefore runs inside `DebtSaleWorkflow` and its timer is the same day of R-UNI-47, so no person is the primary role, which is what FSD S6 A2.14.3.3 says ("None; runs unattended").
- **"every open action" is applied on the workflow and case boundary.** No source enumerates the set: the FSD states only the outcome. The answer names the case and the end state, and rwb-case cancels its own tasks, timers and open deviations while the parent `CaseWorkflow` cancels the open stage children (GAP-3010; ASM-4978).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the caller's transaction, which is what legacy AC1 asked for and what legacy AC2 tested.
- **the step publishes no operation of its own.** TSD S6 appendix T-A publishes five operations for the module and none is a case closure; the closure arrives as the award signal on API-S6-003, which is RWB-S6-E6005-APP's, and the closure element is embedded in the lot read answer API-S6-002 of the lot stories. This story claims no sibling's operation (GAP-3010; ASM-4977).
- **the unattended step has no human right of its own.** The FSD makes the feature unattended, the legacy permission table gives Debt sale right A to three human roles, and TSD S6 T6.1 gives the service identities the right R only. The step therefore runs under the rwb-debtsale service identity and the right A stays with the three roles for the award and for the read of the closure element (GAP-3010; ASM-4979).
- **ALS and GL are not this step's.** The integration points of FEAT-DBS-14 read "Workbench, ALS and GL", while the ALS derecognition and the ledger posting are R-DS-30 and R-DS-31 of FEAT-DBS-12. The closure holds no adapter, no posting and no balance (GAP-3010; ASM-4980).
- **the wave is EP06's and the service is wave 3.** Template and Rules §R5.6 keeps the W-MAP wave of a story when it is later than the service's Arch v5 wave, so this story is wave 4 while rwb-debtsale is created in wave 3; the conflict is recorded once for the service and the business epic and is not raised again here.

The metric of the feature is unchanged and is the review of the closure records, so no business value moves: the `CASE_CLOSED_SOLD` end state, the `LOV-LOT-STATUS` and `LOV-PUTBACK` values and the same-day timer of R-UNI-47 are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E6010-CON is published: the closure element, the closure answer and its vocabulary, the consumed rows, the error set and the fakes are baselined and handed to this story.
- The rwb-case state read and the closure answer are available for the fake. No source publishes an operation that closes a case on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST closure operation its name is Not specified in the source documents (GAP-3010; ASM-4976, ASM-4981).
- The rwb-access authorise contract answers the capability areas "Debt sale" and "Case workflow" with their rights and the scope, so a caller without the right is refused before any read. The operation name is Not specified in the source documents (GAP-3010; ASM-4976).
- The UNIVERSAL package of 50 rules is in force at its version with R-UNI-47, and the DEBTSALE package at its version; both are authored, tested and approved in rwb-decision (P7) and loaded here on the package read. The rule rows and the reference data of the lot status are governed there. The operation name of the package read is Not specified in the source documents (GAP-3010; ASM-4976).
- The lot of the case is `AWARDED` with its buyer reference and its signing date from the award story, and `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037; this story adds no table, no column and no migration of its own.
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the record and the answer commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_decision`, `rwb_access` or `rwb_deviation` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6010-CON when its tests pass.

### 4. Flow

1. The award operation API-S6-003 of RWB-S6-E6005-APP records `AWARD_CONFIRMED` on the lot and the lot reaches `LOT_AWARDED` under R-DS-23; that signal is the trigger of this step, and no screen starts it.
2. The closure branch of `DebtSaleWorkflow` on queue `rwb-debtsale` starts one execution of the step per case of the awarded lot, and arms the same-day timer of R-UNI-47.
3. The step reads its own lot on `debt_sale_lot` in `rwb_debtsale`: the lot reference, the buyer reference, the signing date and the status `AWARDED`, and the account set of `debt_sale_account` for that lot (DF-SAL-031 to DF-SAL-037). No other schema is read.
4. It reads the case of each awarded account on the rwb-case contract: the case reference, the case number, the route state and the count of open actions, read only, one hop with a 2 s budget and a breaker (GAP-3010; ASM-4976).
5. It loads the UNIVERSAL package version in force from rwb-decision and evaluates R-UNI-47 on the fact: an account of the case is awarded in this debt sale lot while the case is active. Where the case is already closed, no rule fires, nothing changes and the repeat is counted.
6. `ClosureDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the lot reference, the account reference, the rule ID `R-UNI-47` with its package version, the inputs reference, the outcome `CASE_CLOSED_SOLD` and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
7. `SoldCaseClient` answers rwb-case with the closure of that case: the end state `CASE_CLOSED_SOLD`, the rule ID with its version and the instruction to stop every open action on the case. rwb-case writes the `recovery_case` row, its state and its timer rows; this service writes none of them.
8. rwb-case stops the open actions it owns and reports the closed case; the parent `CaseWorkflow` cancels the open stage children of the other routes on the case, and the open deviations of rwb-deviation (S8) are closed against the sold case with their outcome recorded there.
9. The transfer of the awarded account data under R-DS-29 and the derecognition and posting under R-DS-30 and R-DS-31 follow in RWB-S6-E6007-APP and RWB-S6-E6008-APP against the case that is now closed; this step waits for none of them and posts nothing (GAP-3010; ASM-4980).
10. A repeated award signal or a repeated closure answer for the same case and `Idempotency-Key` writes nothing, answers no second closure and counts the repeat.
11. The closure element is served read only on `/api/recovery/debtsale/v1` (DP-13) with the lot reference, the case reference, the end state, the rule ID with its version and the decided-at time, for SCR-26 Award in its closed state through the gateway-bff composite route (DP-19), and it carries no personal data.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no case closure answer leaves the service and the case keeps its state | MSG-P7-003 | AC1, AC2, TC-E6-010-02, TC-E6-010-04 |
| X2 | The caller does not hold the Debt sale or the Case workflow right of the capability area on the read of the closure element | 403 before any read; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-010-03 |
| X3 | The case is already closed when the award signal arrives | No rule fires: nothing changes, no record is written and the repeat is counted | None | AC1 |
| X4 | The rwb-case, rwb-access or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no closure is answered, and the read of the element answers 503 with the platform error envelope | None | AC1 |
| X5 | An account of the lot has no open case | Nothing is done for that account and the lot closure count records the absence; the case that is already closed is not re-closed | None | AC1 |
| X6 | A statement or a component reaches `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR10 |
| X7 | The request body of the element read fails validation | 400 with the platform error envelope, and the closure itself is untouched | MSG-GEN-001 | AC1 |

X1 and X2 are the exception paths of RWB-E6-010 carried onto the split; X3 to X7 are the paths the workflow trigger, the call types and the DP-01 boundary add. The `MSG-S6-001` row of the legacy message set names an open deviation on an account, which the eligibility check of FEAT-DBS-01 raises at lot building, so no path of this step raises it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6010-CON, the rwb-case, rwb-access and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3, P4 or P7 |
| Negotiable | The activity name, the decision code and the shape of the stage outcome are this story's choice; the rule row, the end state, the messages, the screen states and the two tables are fixed |
| Valuable | A case whose account is sold stops every open action and closes the same day, in one record, and the case owner sees the end state |
| Estimable | One workflow step, one evaluator, one record write, one closure answer per case, one answer to the parent, three clients and one read-only element |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and cases through the contract fakes, plus the component cases of the failed record write and the refused caller |

### 7. Acceptance criteria

```gherkin
Feature: Close a case awarded in a sold lot

  Background:
    Given case "RC-2026-000842" carries an account sold in the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the UNIVERSAL package is in force at its version and carries R-UNI-47
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Close a case awarded in a sold lot (legacy RWB-E6-010 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000842" in the state "LOT_AWARDED" with its open actions
    Given the rwb-decision contract mock returns the UNIVERSAL package at its version in force with R-UNI-47
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then stops every open action on a case whose account is sold in a lot, and closes it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-010 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E6-010 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `its trigger arrives`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target. The case and its open actions are rwb-case's: the step answers the closure with the end state `CASE_CLOSED_SOLD` and rwb-case cancels its own tasks, timers and open deviations, while the parent `CaseWorkflow` cancels the open stage children of the other routes. The decision is recorded through the local decision-record library before the answer leaves the service, which is the `decision log` of the legacy text and the central ledger of rwb-decision behind it. The step is triggered by the award confirmation of the lot, its timer is the same day of R-UNI-47, and it publishes no operation of its own. The set of "open actions" is not enumerated by any source, so the answer names the case and the end state and the owners apply it inside their own boundaries (GAP-3010; ASM-4978).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-23 | Debt sale | D8.4 | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |
| R-UNI-47 | Universal rules | All | ANY_ACTIVE | ACCOUNT_IN_SOLD_LOT | the account is awarded in a debt sale lot while on another route | Stop every open action, close the case as sold, transfer the data | CASE_CLOSED_SOLD | Debt sale officer | ALS and GL, Workbench | same day |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target "Workbench" is rwb-case and SCR-26, "Document Hub" is rwb-document (P5), "ALS and GL" are the derecognition and posting steps of R-DS-30 and R-DS-31 in RWB-S6-E6008-APP, and "buyer portal" is the partner channel of rwb-partner. R-DS-23 is tabled because its `AWARD_CONFIRMED` signal is the trigger of this step; the award itself, the agreement and the notices belong to RWB-S6-E6005-APP and RWB-S6-E6006-APP, and the data transfer named in the action of R-UNI-47 belongs to RWB-S6-E6007-APP. The from state of R-UNI-47 is `ANY_ACTIVE`, "Any non-terminal state on any route", so the row applies to a case whose only route is the debt sale as well as to one that sits on another route (ASM-4978).

| ID | Rule | Source |
|---|---|---|
| BR1 | The closure is this service's decision and rwb-case's write: this story evaluates R-UNI-47, records it and answers `CASE_CLOSED_SOLD`; `recovery_case`, its state, its tasks and its timers are never written here | Ownership Map (`recovery_case` owner P3); TSD S6 T4; GAP-3010 |
| BR2 | The decision is recorded before the closure answer leaves the service, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E6-010 AC1 and AC2 |
| BR3 | The step is triggered by the award confirmation of the lot and bounded by the same-day timer of R-UNI-47; no screen, no batch and no schedule starts it | Business Rules and Routing Logic v4 R-DS-23 and R-UNI-47; FSD S6 A2.14.2 |
| BR4 | "Every open action" is applied by the owners: rwb-case cancels its tasks, timers and open deviations and the parent cancels the open stage children; this service sends the case reference, the end state and the rule with its version only | FSD S6 A2.14.1; GAP-3010; ASM-4978 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-PUTBACK`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and the same-day timer of R-UNI-47 | TSD S6 T3.2; FSD S6 BR-S6-014; legacy Guardrails |
| BR7 | This story declares no REST operation of its own: the closure element is embedded in the lot read answer API-S6-002 and read through the composite route, and the award operation API-S6-003 is RWB-S6-E6005-APP's | TSD S6 T-A.1; GAP-3010 |
| BR8 | The same award signal or the same closure answer twice, or the same `Idempotency-Key` twice, closes once, answers once and counts the repeat | TSD S6 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, identity number, date of birth, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log or a workflow input; the case is named by its reference | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR10 | The staff screen reads the closure element through the gateway-bff composite route and no screen calls a service directly; the service holds no grant on another schema | DP-19; DP-01; Architecture v5 slides 8 and 13 |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the step answers the closure and the parent `CaseWorkflow` applies it to the case of record (BR1). What this story does own is the state of the step.

| From (case of record, answered) | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | `ACCOUNT_IN_SOLD_LOT` under R-UNI-47 | An account of the case is awarded in the lot | CASE_CLOSED_SOLD, with the rule ID and its version |
| CASE_CLOSED_SOLD | Any repeated award signal | X3 | Unchanged, the repeat is counted |
| Any state | The same-day timer of R-UNI-47 passes without a closure answer | X4 | The step is retried; the case keeps its state until the answer lands |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The award confirmation of the lot arrives | The package in force is loaded | Evaluating |
| Evaluating | R-UNI-47 fires for a case of the lot | The decision record is written | Applying |
| Applying | The closure answer is sent and rwb-case accepts it | The transaction commits | Waiting for the next case or the end of the lot |
| Applying | The record write or the answer fails | X1, X4 | Waiting, nothing changed |
| Waiting | The case is already closed | X3 | Done, nothing written |

`CASE_CLOSED_SOLD` is the end state of the UNIVERSAL route set in the Business Rules and Routing Logic v4 ("Case closed as sold", "Debt sold or asset cleared the balance") and lies on the case of record of rwb-case. The lot status stays `AWARDED` here and moves to `TRANSFERRED` under R-DS-29 in RWB-S6-E6007-APP and to `CLOSED` under R-DS-34 or R-DS-39 in the put-back story; `LOV-LOT-STATUS` carries those values.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the role of the legacy permission row, reading the closure element on SCR-26 and holding the award that triggers the closure; the closure itself runs unattended |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the closure element and approves through the approval path where a lot needs it; the DoA approval is `ApprovalWorkflow` of rwb-decision (P7) |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the closure element and holds the authority of the sale |
| RW-CREDITAD, Credit Administration officer | Debt sale R: reads the closure element of a sold lot for the remittance and posting work of RWB-S6-E6011-APP and RWB-S6-E6008-APP |
| RW-CASEOWN, case owner | Reads the closure state on the case of record, which is rwb-case's surface, and takes no action of this story |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the closure step, evaluates R-UNI-47, writes the decision record and answers the closure; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission table gives Debt sale right A to `RW-DEBTSALE`, `RW-PRODHEAD` and `RW-HEADASL`, and that row stays with the award operation and the read of the closure element, because the FSD makes the closure unattended and no service identity holds the right A in the target matrix (GAP-3010; ASM-4979). DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot of the awarded accounts |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the element |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Read, the buyer the accounts were sold to |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Read, the date the sale was signed |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Read only, `AWARDED` as the award story leaves it; the later states are the transfer and put-back stories' |
| DF-SAL-022, DF-SAL-023, DF-SAL-024, DF-SAL-026, DF-SAL-028, DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date, segment, reserve_price, buyer_class, approval_authority, payment_terms | Not read and not written by this step |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the account set of the lot whose cases are closed; no column is written |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Not written: this step changes no lot row |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case reference, decided at | Write through the local library, before the closure answer |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the open actions of the case | Not read as a table: the case state and its open actions arrive on the rwb-case contract and the closure is answered to it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rule rows arrive in the package in force from rwb-decision |
| DF-REF-034 to DF-REF-038 | role (P4) | id, role_code, role_name, role_class, default_scope | Not read as a table: the capability area and the right are answered by rwb-access |

Field IDs are those of the TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v9, and the three rows of the legacy Data table, `recovery_case`, `decision_log_entry` and `rule_row`, are the rows of other owners in the target. **No new table, no new column and no migration**: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service and are read only here, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03).

**No personal data.** The rows this story writes carry identifiers, codes, dates and a rule version. The account is named by its identifier and the case by its reference: no name, no identity number, no date of birth, no address and no contact value enters `rwb_debtsale`, the decision record, a log, an event or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (Debt sale C), API-S6-002 `GET /debt-sale-lots/{lotId}` (Debt sale R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (Debt sale A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a case-closure operation. The single endpoint row of the legacy story is the award path `POST /debt-sale-lots/{lotId}/award`, which is API-S6-003 and belongs to RWB-S6-E6005-APP, on which this step is signalled. The closure element is embedded in the lot read answer API-S6-002 of the lot stories, so this story provides no operation and claims no sibling's operation (GAP-3010; ASM-4977).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, the case number, the route state and the open actions of each case of the awarded lot; read only, faked |
| The case-closure answer (operation name Not specified in the source documents (GAP-3010; ASM-4981)) | rwb-case (P3) | P3 rwb-case | The end state `CASE_CLOSED_SOLD` with the rule ID, its version and the instruction to stop every open action; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3010; ASM-4981)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Case workflow", the right of the caller and the scope; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The UNIVERSAL package at its version with R-UNI-47 and the DEBTSALE package; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3010 with ASM-4976.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23, consumers rwb-case and rwb-payment) and `AccountsTransferred` (consumers rwb-case and rwb-reporting). `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's; the closure produces neither, so this story writes no outbox row, opens no producer and declares no event of its own, and a build that publishes one fails the absence test.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched` (event 25), which is the settlement step's and belongs to RWB-S6-E6011-APP, and the closure is signalled inside the service's own workflow by the award confirmation. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the award confirmation and the package in force; signals: the case state and open actions answered by rwb-case, the closure answer and the rule package; the closure branch is this story's |
| `closeCase` | Activity, the closure step, one execution per case of the lot | `rwb-debtsale` | The lot, the account set and the case in; the rule ID with its version, the end state, the decision record and the closure answer out, with the record write and the answer in one transaction |

No child workflow for the case and no workflow for the money exists in this service. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the award confirmation of the lot, because the FSD declares no background event for the feature (FSD S6 A2.14.4.4, "No background event") while R-UNI-47 is a same-day rule of the award. The saga steps of reserve, approval, agreement and notices, payment, transfer, derecognition, posting and the lot close belong to the award, agreement, settlement, transfer, derecognition and put-back stories of this service; this story owns the closure step alone.

#### 12.6 Schedules

None. The step runs from the award confirmation and its bound is the durable same-day timer of R-UNI-47 inside the workflow, not a Temporal Schedule. The service owns no Job of Architecture v5 slide 44 in this story, and no Quartz row, no shared job table and no batch table is declared.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of the awarded accounts; read only here, no column written |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot whose cases are closed; read only here |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the closure (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated award signal and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this step writes no row to it |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `deviation` (S8), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), `partner` (S9) and every `v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_account.account_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | The case `RC-2026-000842` in `LOT_AWARDED` with three open actions; the same case already in `CASE_CLOSED_SOLD`; an account of the lot with no open case; no answer beyond 2 s | AC1, X3, X4, X5 |
| rwb-case closure-answer fake | The closure accepted with `CASE_CLOSED_SOLD`; the closure refused because the case is already closed | AC1, X3 |
| rwb-access authorise fake | The capability areas "Debt sale" with right C, R, U or A and "Case workflow" with right R for the TSD S6 T6.1 roles; a caller without the right | AC1, X2 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-47, and the DEBTSALE package at its version | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042`, with the closure element of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case closure answer and the rwb-access authorise call are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3010; ASM-4981).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case state read and the closure answer, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the settlement story's |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its `closeCase` step on `rwb-debtsale`; the same-day bound is a durable timer, not a Schedule |
| File | None | No file is read, built or delivered here; the account data transfer of the sale is RWB-S6-E6007-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `caseclosure`, Java package `th.co.scb.ace.workbench.recovery.debtsale.caseclosure`; front end `src/modules/recovery/debtsale/CaseClosure.tsx`, the SCR-26 Award closed-state fragment, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the closure answer commit together or not at all. DP-13 moves the base of the closure element and nothing else, and the legacy base `/api/recovery/v1` of the single endpoint row becomes `/api/recovery/debtsale/v1` on the operation that belongs to the award story. DP-19 is how SCR-26 Award reaches the element, one hop through the gateway.

**Dependencies the table adds and the plan does not hold.** The three metadata H rows are the plan's and need no change. The four consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-3010 (ASM-4976). DP-08 is not in the pattern set although the read of the element declares a capability area and a right, and DP-09 is not in the pattern set although the library object `outbox_event` exists in the schema; neither is added to the metadata rows, and both are named in the text and in the registers.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` closure branch | Workflow | Waits for the award confirmation, starts one `closeCase` execution per case of the lot, arms the same-day timer and reports the outcome to the parent |
| `closeCase` | Activity | The one step: read the lot and its account set, read the cases, evaluate R-UNI-47, write the record, answer the closure |
| `CaseClosureEvaluator` | Service | The rule evaluation against the UNIVERSAL package version in force, with the lot status and the end state of the closed lists |
| `ClosureDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID `R-UNI-47` and its version before any answer, hash-linked, and refuses the step when the write fails (DP-03) |
| `SoldCaseReader` | Repository | Reads `debt_sale_lot` and the `debt_sale_account` rows of the lot in `rwb_debtsale`, read only, with no lock and no write |
| `CaseStateClient` | Client | The case state, open actions and closure answer of rwb-case, one hop, 2 s, breaker |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `ClosureController` | Controller | The read of the closure element on the service base, the capability area and right, and the problem mapping of 400, 401, 403, 404 and 503; it declares no operation that TSD S6 T-A does not publish (GAP-3010; ASM-4977) |

**Build steps.** Publish the element of section 12 against the CON baseline; wire the closure branch and the same-day timer; implement the evaluator and the record writer; implement the lot and account read; implement the case read and the closure answer; implement the element read and its capability area; test the fakes, the failed record write and the repeat.

**Done when.** The step closes every case of an awarded lot on the fakes with one record per case, a failed record write closes nothing, a repeated signal closes once, the element reads through the composite route, and the boundary test shows no statement outside `rwb_debtsale`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which the eligibility check of FEAT-DBS-01 raises at lot building, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required parameter of the element read is absent or invalid | Enter {field}. |
| MSG-P4-002 | The caller lacks the Debt sale or the Case workflow right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the closure answer | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are the message set of the legacy story and of the FSD, copied unchanged; no message is reworded and no new one is added. `MSG-S6-001` stays in the set of the key although the closure does not raise it, because the legacy table carries it for the feature family.

### 15. Screens and states

`SCR-26 Award` in its open, closed, awarded and transferred states is the only screen of this step, and it is read only here. The closure element appears in the closed state with the lot reference, the case reference, the end state, the rule ID with its version and the decided-at time. The screen reaches this service through the gateway-bff composite route (DP-19), which also calls rwb-case for the case and its state and rwb-partner for the buyer; the composite route specification and the field list of the screen belong to RWB-PLT-N001-CON. The refusal, the not-recorded and the unavailable states read the messages of section 14 on the same route. No new screen, no new field and no new user action is introduced by this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-010-01 | AC1 | End to end | Lot `LOT-2026-000042` awarded to buyer `PTR-2026-000031` and case `RC-2026-000842` in `LOT_AWARDED` with three open actions; the closure is answered and the case reaches `CASE_CLOSED_SOLD` |
| TC-E6-010-02 | AC2 | Component | The decision-record stub stopped; nothing changes and MSG-P7-003 is answered, with no closure answer sent |
| TC-E6-010-03 | X2 | Component | A caller without the Debt sale right on the element read is refused with MSG-P4-002 before any read |
| TC-E6-010-04 | AC2, X1 | Component | A forced decision-record write failure during the closure of a case of the lot; the transaction writes nothing |
| TC-S6-E6010-APP-01 | AC1, BR4 | Component | A lot of three cases, one already closed and one with no open case; three evaluations, one record per open case, one answer per closed case and no re-close |

The four legacy cases are the legacy cases of RWB-E6-010 in their legacy order, with the legacy level `System` mapped to `End to end` for the closure journey and to `Component` for the access and forced-failure cases, because the artefact under test is this service's step. `TC-E6-010-03` covers the access case and `TC-E6-010-04` the forced-failure case, as the legacy table writes them. The case `TC-S6-E6010-APP-01` is new and tests the step's own selection and repeat behaviour. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here because this story holds no integration dependency.

### 17. Guardrails

- No business value in code: the `LOV-LOT-STATUS`, `LOV-PUTBACK`, `LOV-SEGMENT` and `LOV-BUYER-CLASS` values, the end state and the same-day timer stay reference data or rule rows, read with their version.
- No personal data in events, workflow inputs, the decision record or logs: the account is an identifier and the case a reference, and no name, identity number, date of birth, address or contact value is written; every fixture is synthetic.
- The case stays with rwb-case and the deviation with rwb-deviation: no `recovery_case` or `deviation` property is written here, and no case row, task or timer is created.
- ACE data only through the owner's contract or the `v_ace_*` views: this step reads no ACE table and no `v_ace_*` view, and the lot and account facts are its own rows.
- No posting and no balance: the derecognition, the ledger and the ALS update are R-DS-30 and R-DS-31 in RWB-S6-E6008-APP (GAP-3010).
- One base, one topic, one queue and one login per service; the story names no other service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: API-S6-003 is named as the surface that triggers the step and as RWB-S6-E6005-APP's (GAP-3010).
- The boundary test fails any statement outside `rwb_debtsale`, and the absence tests fail a published event, a consumed event or a Schedule of this step.

### 18. Traceability

| Requirement ID | Requirement (short) | Elements | Test cases |
|---|---|---|---|
| REQ-S6-007 | An account awarded in a lot stops every other open action on its case the same day (Business Requirements Program v5, FSD S6 A2.14); the split plan carries no requirement id for this slice (GAP-3010; ASM-4976) | The closure step, the R-UNI-47 evaluation, the decision record and the closure answer | TC-E6-010-01, TC-E6-010-02, TC-S6-E6010-APP-01 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the closure step | TC-E6-010-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-010-01, TC-E6-010-03 |
| ADR-022 | Local decision record plus central ledger | The record written before the closure answer | TC-E6-010-02, TC-E6-010-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-010, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story with their origin tag |
| Test cases | TC-E6-010-01 to TC-E6-010-04 and TC-S6-E6010-APP-01 |
| Feature and screens | FEAT-DBS-14 Close a case awarded in a sold lot; SCR-26 Award |
| Rules | R-UNI-47, with R-DS-23 tabled as its trigger, from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The contract baseline of the closure element, the closure answer, the consumed rows, the error set and the fakes: RWB-S6-E6010-CON.
- The award operation API-S6-003, the price test, the agreement and the customer notices, and the `LotAwarded` event: RWB-S6-E6005-APP and RWB-S6-E6006-APP.
- The transfer of the awarded account data under R-DS-29 and the `AccountsTransferred` event: RWB-S6-E6007-APP.
- The derecognition under R-DS-30, the general ledger posting under R-DS-31 and the ALS update: RWB-S6-E6008-APP (GAP-3010; ASM-4980).
- The lot close under R-DS-34 and R-DS-39, the put-back claim and the re-offer: the put-back story of this service.
- The buyer remittance under R-DS-25 to R-DS-27: RWB-S6-E6011-APP.
- The case of record, its route state, its tasks, its timers and the open stage children: rwb-case (P3), whose state and closure answer this story consumes and fakes (GAP-3010).
- The deviation records and their pause of the stage clock: rwb-deviation (S8).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3010).
- The authoring, testing, approval and versioning of the UNIVERSAL and DEBTSALE packages and of R-UNI-47 and R-DS-23: rwb-decision (P7).
- The gateway-bff composite route and the field list of SCR-26 Award: RWB-PLT-N001-CON.
- The buyer panel, the partner users and the partner channel: rwb-partner (S9).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
