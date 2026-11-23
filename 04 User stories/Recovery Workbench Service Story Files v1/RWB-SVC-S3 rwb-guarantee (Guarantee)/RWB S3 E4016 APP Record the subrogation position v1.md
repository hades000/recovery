# RWB-S3-E4016-APP Record the subrogation position

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S3-E4016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4016-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-016 split out for rwb-guarantee. All four legacy criteria of the key, AC1 to AC4, are copied word for word with their origin tags, and the cross-service part of AC1 and AC2 is mocked with an added `Given` line from the rwb-payment contract. The subrogation position becomes the `recordAndApply` step of `GuaranteeClaimWorkflow` on task queue `rwb-guarantee`: the posted payment arrives as an rwb-payment event (DP-05 retires the legacy `v_ace_payment` read), the GUARANTEE rule set decides the step and the case moves, the claim record and the local decision-record entry are written in one transaction (DP-03), and `PATCH /guarantee-claims/{claimId}` on base `/api/recovery/guarantee/v1` answers the claim with its position (DP-13), reached by SCR-17 through the gateway-bff composite route (DP-19). The service publishes no event, because the ownership rows give S3 none. No field, column or element exists for the position or for the guaranteed amount of R-GUA-22 (GAP-2720; ASM-4518); the payment reaches this service only on the rwb-payment event, and the posted-payment event name is not published (GAP-2721; ASM-4519); no event of this service is authored and no peer event name is published (GAP-2722; ASM-4520); R-GUA-23 and R-GUA-24 are identical and the claim's record status list is not mapped to the GUARANTEE case states (GAP-2723; ASM-4521); the TCG share has no published source and INT-29 is "Not available today" (GAP-2724; ASM-4522). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **guarantee officer**, I want **the Workbench to record what the guarantor may reclaim after payment, so the position is not lost**, so that **no guarantee claim misses its deadline**.

This is the application slice of legacy RWB-E4-016. It owns:

- the four legacy criteria of the key, AC1 to AC4, copied verbatim with their origin tags, and the rules, messages and screen they name;
- the subrogation step of `GuaranteeClaimWorkflow`, the one workflow the ownership rows give S3, on task queue `rwb-guarantee` in namespace `rwb-recovery`, with its activities `matchFullPayment`, `evaluateSubrogationRules` and `recordAndApply`;
- the match of a posted payment to the claim of record, on the payment fact that arrives from rwb-payment, and the comparison of the claim's paid amount with its guaranteed amount under R-GUA-22;
- the position itself: the TCG share, the basis it is taken on, the time it is set and the claim it is set for, recorded for every later recovery of the case (R-GUA-23 and R-GUA-24);
- the write of `guarantee_claim` (paid amount, status, optimistic version) and of the local decision record in one transaction, and the report of the case moves `CLAIM_PAID` and `SUBROGATION_POSITION` to the parent `CaseWorkflow` of rwb-case;
- the claim slice of `PATCH /guarantee-claims/{claimId}` on base `/api/recovery/guarantee/v1`: the position elements of `GuaranteeClaimUpdate` in and `GuaranteeClaim` out, the right, the `version` check and the problem mapping (API-S3-002; DP-13);
- the states of SCR-17 Guarantee claim that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the claim update, the consumed payment event element, the position element set, the workflow elements, the rights, the error set and the fakes, which are RWB-S3-E4016-CON; the preparation of the claim, its checklist and its submission, which are FEAT-GUA-01 and FEAT-GUA-02 (RWB-E4-013 and RWB-E4-014); the tracking of the claim, its service-level breach and the claim deadline timer, which are FEAT-GUA-03 (RWB-E4-015); guarantor notices and negotiation, which are FEAT-GUA-05 and FEAT-GUA-06 (RWB-E4-017 and RWB-E4-018); the close of the guarantee and of the case after the position, which is FEAT-GUA-07 (RWB-E4-019); the case of record, its states and the parent `CaseWorkflow`, which are rwb-case's (P3); the posting of the money, the ledger and the ALS entry, which are rwb-payment's (P8); the rule rows and the package version, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the SCR-17 field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

FSD S3 A2.4 states the feature in one line: records what the guarantor may reclaim after payment, so the position is not lost. The module problem is that guarantee and TCG claims are late because deadlines are not tracked, and the module measure is unchanged: claims filed inside the deadline, 100 percent, read monthly from the decision log and the Workbench records. REQ-S3-003 carries the requirement: a guarantee payment that clears the balance closes the case and records the subrogation position. Architecture v5 slide 3 places the route with this service, "Guarantee claim: claim on guarantors or schemes, rwb-guarantee S3", and states that routes can run in parallel, for example a guarantee claim alongside litigation, so the position must be recoverable from the case at any later point.

The monolith did this inside one S3 process: it read `v_ace_payment` on its own connection, matched the payment, posted it through ALS and GL, wrote `decision_log_entry` and moved the case in the same schema. In the 19-service target the three facts of that act belong to three owners, and this story is what keeps them apart while the rule stays the same.

- **the money is rwb-payment's.** Posting and the ALS and GL entries are P8's; slide 13 gives S3 no REST edge to P8 and one event subscription from it. This story receives the posted-payment fact, matches it to the claim and writes no posting row (GAP-2721; ASM-4519).
- **the position is this service's.** `guarantee_claim` is the one table the ownership rows give S3, and the position is the claim's own fact. The share is read as data with its version and never written in code (BR-S3-004).
- **the case stays with rwb-case.** `CLAIM_PAID` and `SUBROGATION_POSITION` are rows of the GUARANTEE state set of TSD S3 T4; this story reports the moves to the parent workflow and writes no case row (DP-01).
- **the decision is recorded first, and locally.** AC1 asks for the result to be written with the rule version and AC4 is the rule that makes it trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the claim row, with R-UNI-38 fixing the version in force and R-UNI-39 forbidding an action that is not logged.
- **nothing new is swallowed from ACE.** The legacy `v_ace_payment` read is not built: slide 8 reserves the 30 `recovery.v_ace_*` views to rwb-source-data, and the payment arrives on the event instead, so `rwb_guarantee` holds no ACE grant (DP-05; GAP-2721).
- **nothing is published.** The ownership rows give S3 no event, so the step adds no name to `rwb.guarantee.events.v1`; its outward facts are the claim answer, the case moves and the decision record, which the library sends to `rwb.decision-record.v1` (GAP-2722; ASM-4520).

The temporal shape is the one slide 5 of the Temporal design gives S3: "guarantee claims, claim deadline timer, missed deadline = lost claim". The deadline timer itself is FEAT-GUA-03; what this story keeps is that the position is set before the guarantee is closed, so that a later recovery of the same case still carries the TCG share.

### 3. Preconditions

- RWB-S3-E4016-CON is published: the claim-update element set, the position elements, the payment event element, the rights, the error envelope and the fakes are baselined and handed to this story (H).
- RWB-PLT-E1027-CON is published (DP-03): the local decision-record writer joins the caller's transaction, and a failed write stops the step with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): SCR-17 Guarantee claim reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (H).
- The service runs as its own login on schema `rwb_guarantee`, owns the table `guarantee_claim`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `decision_log_entry` or `v_ace_payment` is refused by the database and fails the boundary test.
- `GuaranteeClaimWorkflow` runs as a child of `CaseWorkflow` (rwb-case) on `rwb-guarantee`, started when the case enters the guarantee route, and reports its stage outcome to the parent; the parent applies the case state and writes `recovery_case`, `task` and `timer`.
- The posted-payment fact arrives on the rwb-payment topic `rwb.payment.events.v1` with the inbox of DP-09's platform library; the event name and its element set are Not specified in the source documents (GAP-2721; GAP-2722; ASM-4519; ASM-4520).
- The GUARANTEE rule set is the one of the Business Rules and Routing Logic v4: 32 rules over 17 states, with R-GUA-22, R-GUA-23 and R-GUA-24 for this step; the rule version in force is read as a row and no version number is asserted.
- The subrogation position and the guaranteed amount of R-GUA-22 have no published field: the eight fields of `guarantee_claim` are DF-TRT-015 to DF-TRT-022 and none of them holds a share (GAP-2720; ASM-4518).
- The TCG share has no published external source: TSD S3 T5.1 records INT-29 as "Not available today; entered and filed by the guarantee officer", so the share is a value on the claim update and no interface is called (GAP-2724; ASM-4522).
- The capability area is Treatment and offer: right U for RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, the rows of the legacy permission table and of TSD S3 T6.1.
- No approval is needed to build against a Draft contract baseline; RWB-S3-E4016-CON tags the version when its tests pass.

### 4. Flow

1. A case is at `CLAIM_SUBMITTED` on the guarantee route, with a claim on `guarantee_claim` in claim status `FILED`; the stage waits on `GuaranteeClaimWorkflow`, started by the parent `CaseWorkflow`.
2. rwb-payment posts the TCG or insurer payment against the case and publishes the posted-payment fact on `rwb.payment.events.v1`; the inbox of this service stores it once and signals the workflow (ASM-4519).
3. `matchFullPayment` matches the fact to the claim by the case and the payment reference, reads the payment amount and the claim's guaranteed amount, applies R-GUA-22 and returns the full-payment flag and the amounts; a partial payment returns the other branch, which is FEAT-GUA-03 and FEAT-GUA-07 (GAP-2720; GAP-2721).
4. On a full payment, `evaluateSubrogationRules` runs the GUARANTEE set in force in the service's own Drools kit and answers R-GUA-22: the claim moves to `CLAIM_PAID` and the subrogation step is due (R-GUA-23), with R-GUA-24 the same step reached from `CLAIM_PART_PAID` (GAP-2723; ASM-4521).
5. The step takes the TCG share, its basis and its effective scope as values on the claim update or as rows in force; no share, percentage or amount is a constant of the build (BR-S3-004; GAP-2724).
6. `recordAndApply`, one transaction: `guarantee_claim` is updated with `paid_amount`, the claim status, the optimistic `version`, `updated_at` and `updated_by`; the position is set on the claim; the decision record is written with the decision code, the rule id and version, the claim, the payment reference, the share and the role of the officer where one is involved; and the outbox row follows in the same transaction. A failed record write leaves the claim where it is and shows MSG-P7-003 (AC4; DP-03).
7. The stage reports the two case moves to the parent `CaseWorkflow`: `CLAIM_PAID` on the full payment under R-GUA-22, then `SUBROGATION_POSITION` under R-GUA-23 or R-GUA-24. The parent applies them to the case of record; this service writes no `recovery_case` row.
8. The workflow answers the claim with its position: the share, its basis, the set-at time and the claim status, on `PATCH /guarantee-claims/{claimId}` where the officer records or confirms the share, and in the claim answer that SCR-17 reads (API-S3-002; DP-13).
9. A repeat of the same posted-payment fact is caught by the inbox key and the optimistic `version`: one position, one record, one case move, and the stored answer is returned; a stale `version` is refused with 409 and nothing is written (R-UNI-40).
10. The step ends by handing the residual to FEAT-GUA-07: R-GUA-25 returns the balance to the route decision when the share leaves a remainder, and R-GUA-26 closes the guarantee and the case when it does not. This story records the position and reports no more than the two moves above.
11. SCR-17 shows the claim, its deadline, the payment, the position and its share, read through the gateway-bff composite route, read only (DP-19).
12. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (ASM-4520).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written, or is refused for a missing element | The transaction writes nothing, the position is not set and the claim does not move | MSG-P7-003 | AC4, TC-E4-016-04, TC-E4-016-06 |
| X2 | The role does not hold right U of Treatment and offer, or the caller is out of scope | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-016-05 |
| X3 | A required element of the claim, the payment fact or the share is absent or invalid | The step does not run, nothing is written and the missing element is named | MSG-GEN-001 | TC-E4-016-01 |
| X4 | The payment is partial, or no claim of the case matches the payment reference | The full-payment branch does not run; the claim stays at `CLAIM_SUBMITTED` and the partial path of FEAT-GUA-03 and FEAT-GUA-07 applies | None | TC-S3-E4016-APP-02, AC2 |
| X5 | The claim's `version` is stale, or the same posted-payment fact arrives again | 409 with nothing written for a stale version; one position and one record for a repeat | None | TC-S3-E4016-APP-02 |
| X6 | rwb-payment publishes no fact inside the workflow's wait, or the inbox is behind | The workflow keeps waiting on its durable timer and reads the backlog when it catches up; nothing is written and no position is set from an unposted payment | None | TC-S3-E4016-APP-02 |
| X7 | The data product behind the claim is stale, or the rules row in force is missing | The step holds, names the stale product and raises a task; no position is set on a stale fact | MSG-P1-001 | TC-S3-E4016-APP-02 |
| X8 | A component, a statement or a test reaches `recovery_case`, `v_ace_payment`, another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR7, BR9, TC-S3-E4016-APP-01 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X7 are the paths the target call types, the optimistic version and the stale-data rule add, and X8 is the DP-01 and DP-05 boundary. The legacy exception list of FSD S3 A2.4.4.3 names X1 and X2 in the same words as the legacy criteria; no new message is invented.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S3-E4016-CON, the rwb-payment event fake, the decision-record stub and the composite route fake, on its own schema, and needs no live P8, P3 or P7 |
| Negotiable | The activity names, the decision code and the shape of the step's own elements are this story's choice; the operation, the rights, the messages, the states and the screen are fixed |
| Valuable | The bank keeps the guarantor's share after payment, so a later recovery of the same case pays the right party, and the position is provable with the version that made it |
| Estimable | One workflow step, three activities, one event subscription, one record write, two case moves and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic claims, payments and shares through the contract fakes, plus the stopped record write, the partial payment, the stale version and the repeated fact |

### 7. Acceptance criteria

```gherkin
Feature: Record the subrogation position

  Scenario: AC1 Record the subrogation position (legacy RWB-E4-016 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-payment contract mock returns the posted payment of the claim matched against the case, with the claim's paid amount equal to its guaranteed amount
    When its trigger arrives
    Then records what the guarantor may reclaim after payment, so the position is not lost
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-22 (legacy RWB-E4-016 AC2)
    Given a case in state CLAIM_SUBMITTED
    Given the rwb-payment contract mock returns the full payment of the claim matched and posted against the case
    When full payment received
    Then match the payment, post it, and set the subrogation position
    Then the case moves to CLAIM_PAID

  Scenario: AC3 Rule R-GUA-23 (legacy RWB-E4-016 AC3)
    Given a case in state CLAIM_PAID
    When subrogation due
    Then record the TCG share against the case for all future recoveries
    Then the case moves to SUBROGATION_POSITION

  Scenario: AC4 Not recorded (legacy RWB-E4-016 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E4-016 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording `its trigger arrives`, `full payment received`, `subrogation due`, `the decision log cannot be written` and `record the TCG share against the case for all future recoveries` all stand. The cross-service part is mocked, so AC1 and AC2 carry one added `Given the <service> contract mock returns <x>` line each, and those two lines are the only additions to the legacy text; AC3 and AC4 need none, because the share is recorded in this service and the decision record is local to it. "The decision log" of AC1 and AC4 is the local decision record of DP-03 on its way to `rwb.decision-record.v1`; `decision_log_entry` stays P7's ledger and is neither written nor read here. "Post it" in AC2 is the posting of rwb-payment, which publishes the fact this story consumes; this service posts nothing (GAP-2721). No criterion is given a share, a percentage, an amount, a deadline or a version number: those are data in force of their owners (GAP-2720; GAP-2724).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S3-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S3-004 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-GUA-22 | CLAIM_SUBMITTED, FULL_PAYMENT_RECEIVED, claim_amount_paid = guaranteed_amount: match the payment, post it, and set the subrogation position. To CLAIM_PAID | None |
| R-GUA-23 | CLAIM_PAID, SUBROGATION_DUE, TCG holds a share of every later recovery: record the TCG share against the case for all future recoveries. To SUBROGATION_POSITION | None |
| R-GUA-24 | CLAIM_PART_PAID, SUBROGATION_DUE, TCG holds a share of every later recovery: record the TCG share against the case for all future recoveries. To SUBROGATION_POSITION | None |

The VR and BR rows are the rows of FSD S3 A2.4.3.1, copied character for character; the three GUA rows are the rows of the Business Rules and Routing Logic v4 with their from-state, event, condition, action and to-state in the same order, compressed onto one line and otherwise unchanged. R-GUA-25 and R-GUA-26 are the rows that follow the position and are FEAT-GUA-07's.

| ID | Rule | Source |
|---|---|---|
| BR1 | Every full payment of a guaranteed claim sets one subrogation position on the claim of record, before the guarantee is closed, so that every later recovery of the case carries the TCG share | R-GUA-23, R-GUA-24; FSD S3 A2.4.1; REQ-S3-003 |
| BR2 | The share, its basis and its effective scope are read as values with their version; no share, percentage, threshold or amount is a constant, a default or a branch of the build | BR-S3-004; FSD S3 A2.4.3.1 |
| BR3 | The posting is rwb-payment's: this service receives the posted-payment fact, matches it to the claim and writes no `proceeds`, ALS or GL row; a payment that is not posted sets no position | Arch v5 slide 13 (S3 ← P8 events only); GAP-2721 |
| BR4 | The case state is rwb-case's: this story reports `CLAIM_PAID` and `SUBROGATION_POSITION` to the parent `CaseWorkflow` and writes no `recovery_case`, `assignment`, `task` or `timer` row | DP-01; Ownership Map (`recovery_case` owner P3) |
| BR5 | The claim row and the decision record commit in one transaction, with the rule id and the version in force, and a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-38, R-UNI-39; AC4 |
| BR6 | One position per claim and payment: a repeated fact and a repeated command are caught by the inbox key and the optimistic `version`, and raise no second position and no second record | R-UNI-40; TSD S3 T3.0 (`version`) |
| BR7 | No new table, no new column and no foreign key: the position is carried as an element of the claim answer and of the decision record until the data owner names a field, because `guarantee_claim` closes at DF-TRT-022 | GAP-2720; ASM-4518; DP-01 |
| BR8 | No ACE data is read directly: the legacy `v_ace_payment` read is not built, the payment arrives on the rwb-payment event, and `rwb_guarantee` holds no `v_ace_*` grant | DP-05; Arch v5 slide 8 |
| BR9 | No event is published and no Schedule is declared: the ownership rows give S3 no event and no job, and the wait is a durable workflow timer or the next payment fact | context pack S3 ownership rows; GAP-2722; ASM-4523 |
| BR10 | No person name, address, contact value or identity number enters `rwb_guarantee`, the decision record, a log or a workflow input; the claim names parties by identifier and the officer by role | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case states below are rwb-case's and are not changed by this story: the stage reports its outcome and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story owns is the claim record's own status and the position set against it.

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| `CLAIM_SUBMITTED` | FULL_PAYMENT_RECEIVED | The posted payment equals the guaranteed amount of the claim | `CLAIM_PAID` (R-GUA-22) |
| `CLAIM_SUBMITTED` | PART_PAYMENT_RECEIVED | The posted payment is below the guaranteed amount | `CLAIM_PART_PAID`, the other branch of TSD S3 T4 |
| `CLAIM_PAID` | SUBROGATION_DUE | TCG holds a share of every later recovery | `SUBROGATION_POSITION` (R-GUA-23) |
| `CLAIM_PART_PAID` | SUBROGATION_DUE | TCG holds a share of every later recovery | `SUBROGATION_POSITION` (R-GUA-24) |
| `SUBROGATION_POSITION` | RESIDUAL_REMAINS | The balance after the guaranteed share is greater than zero | `RESIDUAL_TO_ROUTE` (R-GUA-25), FEAT-GUA-07 |
| `SUBROGATION_POSITION` | BALANCE_SATISFIED | The balance after the guaranteed share is zero | `GUARANTEE_CLOSED` (R-GUA-26), FEAT-GUA-07 |
| Any of the above | The record cannot be written | X1 | Unchanged, nothing applied and no position (AC4) |

| Claim record state (`guarantee_claim.status`, this story) | Event | Condition | To |
|---|---|---|---|
| `FILED` | The full posted payment is matched | The record and the claim row commit | `PAID`, with the position set on the claim |
| `FILED` | The posted payment is partial | The partial branch applies | `FILED`, unchanged by this story |
| `PREPARING`, `DEFECT`, `REJECTED` | Any payment fact | The claim is not in a payable state | Unchanged, and the fact is counted and not applied |
| `PAID` | The same payment fact arrives again | X5 | `PAID`, one position and no second record |

The case state names are the rows of the GUARANTEE state set of TSD S3 T4, and the claim record values are the closed list `LOV-CLAIM-STATUS` of TSD S3 T3.2: PREPARING, FILED, DEFECT, PAID, REJECTED. No source maps the two lists to each other, so `PAID` on the record and `CLAIM_PAID` on the case are declared as one step in the same transaction and the mapping is carried as GAP-2723 with ASM-4521; no further claim status is invented.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-GUARANT, guarantee officer | Treatment and offer CRU in TSD S3 T6.1 and the "also uses" role of FSD S3 A2.4.3.3: verifies the claim, records or confirms the share on the claim update and reads the position |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL | Treatment and offer U in the legacy permission table: read the claim, the position and the case answer; RW-RESTRUCT holds CRUA and RW-CASEOWN CRU in T6.1 |
| RW-TEAMMGR (R), RW-COMPLAIN (R), RW-FRAUD (R), RW-LITOFF (R), RW-LEGAL (R), RW-CONDUCT (R), RW-PRODHEAD (RA), RW-CREDCOMM (RA), RW-RISK (R), RW-COE (R), RW-AUDIT (R), RW-BIANAL (R), RW-TRIBE (R) | TSD S3 T6.1 rows for the capability area: read the claim, its position and its record in scope, and set nothing |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks as people |
| rwb-guarantee service identity | Consumes the payment fact, runs the three activities, writes the claim row and the decision record, reports the two case moves and answers the claim operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S3 T6.1 and of the legacy permission table of this key, and nothing wider. The feature row of the Epics 3 to 8 Specification v3 names the primary role of FEAT-GUA-04 as "Runs unattended", so the unattended step runs under the service identity and the officer's right U applies only where a person records or confirms the share (GAP-2724). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 to DF-TRT-022 | `guarantee_claim` (S3) | id, case_id, claim_type, claim_deadline, claimed_amount, filed_at, paid_amount, status | Write: `paid_amount`, `status`, `version`, `updated_at`, `updated_by`; read the rest |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read or written as a table: the case moves are reported to the parent workflow and applied by rwb-case |
| DF-CAS-030 to DF-CAS-035 | `case_party` (P3) | id, case_id, person_key, party_role, role_from, role_to | Not read or written: the guarantor and the co-borrower stay with the case |
| DF-WRK-027 to DF-WRK-036 | `timer` (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read or written: the claim deadline timer is FEAT-GUA-03's and belongs to rwb-case |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Not read: no `v_ace_*` grant here; the payment arrives on the rwb-payment event (GAP-2721) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_guarantee`) | decision code, rule id, rule version, inputs reference, claim, payment reference, share and basis, decided at, decider role | Write, one record per position, before the claim moves |
| The subrogation position and the guaranteed amount (no Field ID published) | The claim's own fact; its field is Not specified in the source documents (GAP-2720; ASM-4518) | The share, its basis, its effective scope, the set-at time, and the guaranteed amount R-GUA-22 compares with the paid amount | Written as an element of the claim answer and of the record; no column is added by this story |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S3 T3.1 and of the legacy Data table of the key, with the owners changed by the target. **No new table and no new column**: `guarantee_claim` already sits in `rwb_guarantee`, whose login and schema arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). The position element and the guaranteed amount are the open point of GAP-2720 and are not written into a column of this story's making.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and versions. No name, address, contact value or identity number enters `rwb_guarantee`, the decision record, a log, a workflow input or an answer; the officer is a role on the record and the parties are identifiers on the case.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story supplies the claim-result slice of the one write the legacy Endpoints table names, and its shape is baselined by RWB-S3-E4016-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` in and `GuaranteeClaim` out, carrying the claim result and, on this step, the subrogation position with its share, its basis, its effective scope and the set-at time (API-S3-002) | Treatment and offer, right U, scope applied | Not applicable in TSD S3 T-A.2; a repeat is refused on the stale `version` with 409 and nothing is written |

The element list of `GuaranteeClaimUpdate` and `GuaranteeClaim` is not published: TSD S3 T-A.2 names the two types and no field table, and the position elements are the baseline's (GAP-2720; ASM-4518). The errors are 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope claim, 409 on a stale `version`, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library does not answer. Opening a claim on `POST /cases/{caseId}/guarantee-claims` (API-S3-001) is the claim-preparation baseline of this service and not this story.

#### 12.2 REST operations consumed

None. The call matrix of Architecture v5 slide 13 gives S3 no REST edge: this service reaches other services through Temporal and through events, and route services reach shared capabilities through Temporal, never REST. The payment, the rules and the case therefore arrive as a workflow input, an event fact and a local rule row, and not as a call of this story.

#### 12.3 Events published

None. The ownership rows give rwb-guarantee no event, so this story adds no name, no outbox row and no payload to `rwb.guarantee.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the claim write (ASM-4520).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| The posted-payment event (name Not specified in the source documents (GAP-2722; ASM-4520)) | `rwb.payment.events.v1`, with `.retry` and `.dlt` | P8 rwb-payment | The claim, the payment reference, the amount, the posting date and the channel; matched to the claim and used by R-GUA-22 |

One subscription with the inbox of the platform event library: the event is stored once by its key, the workflow is signalled and the repeat is ignored (R-UNI-40). Slide 13 gives S3 an event subscription from P8 and from no other service, so no second subscription is declared. The element set of the event is the baseline's (RWB-S3-E4016-CON).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, one child execution per case per guarantee stage, child of `CaseWorkflow`, continues-as-new | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case, the claim and the rule version in force; signal: the posted-payment fact; reports the stage outcome and the two case moves to the parent |
| `matchFullPayment` | Activity, this story | `rwb-guarantee` | The case, the claim and the payment fact in; the matched payment, the paid amount, the guaranteed amount and the full-payment flag out |
| `evaluateSubrogationRules` | Activity, this story | `rwb-guarantee` | The claim state, the payment result and the business date in; the rule row that fired, its version, the share and the basis and the target state out |
| `recordAndApply` | Activity, this story | `rwb-guarantee` | The claim update and the position in; the claim row, the decision record and the outbox row out, in one transaction, plus the reported case moves |

`GuaranteeClaimWorkflow` is the one workflow the ownership rows give S3, and these three activities are this step's; the other activities of the claim belong to the preparation, submission and tracking stories. The activity names are a target design choice, fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the payment fact and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S3 no job. The claim deadline clock is FEAT-GUA-03's and is a workflow timer there, not a Schedule of this story (ASM-4523).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `guarantee_claim` | S3 | The one table of this service: read the claim and write `paid_amount`, `status`, `version`, `updated_at`, `updated_by` |
| decision_record | PLT library, created in `rwb_guarantee` | The local hash-linked decision record of DP-03, one per position |
| idempotency_key | PLT library, created in `rwb_guarantee` | The key of the repeated fact and the answer it holds |

Not owned and never read as a table: `recovery_case`, `case_party`, `assignment`, `task` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), `document` (P5), `deviation` (S8), and every `v_ace_*` view (P1). No foreign key leaves `rwb_guarantee`: the case, the payment and the rule are identifiers and values, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment payment-event fake | A posted full payment for claim `CLM-2027-000416`: the case, the payment reference, the amount and the posting date; the same event replayed; a partial payment; an event whose reference matches no claim; no event inside the wait | AC1, AC2, X4, X6, TC-S3-E4016-APP-02 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-17 answer for the claim, with the deadline, the payment, the position and its share read once | TC-E4-016-01 |
| rwb-guarantee claim-update contract fake (`RWB-S3-E4016-CON`) | The claim in claim status `FILED` and `PAID`, with and without a position, and a stale `version` | TC-E4-016-01, TC-E4-016-05, X5 |

The fakes are test-only and are replaced by the real service in SIT. The payment event name is not published, so its fake is built from the documents and carries the placeholder until the owner confirms it (GAP-2721; GAP-2722; ASM-4519).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed | `PATCH /guarantee-claims/{claimId}` on `/api/recovery/guarantee/v1`; the call matrix gives S3 no REST edge |
| Kafka | 0 published, 1 consumed | One subscription from rwb-payment on `rwb.payment.events.v1`; no event of this service; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 3 activities | `GuaranteeClaimWorkflow`, `matchFullPayment`, `evaluateSubrogationRules` and `recordAndApply` on `rwb-guarantee`, as a child of `CaseWorkflow`; no Schedule, one durable wait |
| File | None of this service | The step writes no file and calls no external system; INT-29 is not called (GAP-2724) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, module `subrogation`, Java package `th.co.scb.ace.workbench.recovery.guarantee.subrogation`; front end `src/modules/recovery/guarantee/SubrogationPosition.tsx`, the fragment SCR-17 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the claim row, the position and the record commit together or not at all. DP-05 is applied by retirement rather than by a call: the legacy `v_ace_payment` read is not built, the payment arrives on the rwb-payment event, and `rwb_guarantee` holds no `v_ace_*` grant, so the alternative of "the service's own ACE views" is not taken and no dependency is added. DP-13 moves the base of the one operation and keeps the monolith path out of the build. DP-19 is how SCR-17 reaches this service, one hop through the gateway. No other DP applies: no decision is asked of Drools through DP-04's kit row beyond the service's own embedded rule set, no event is published (no DP-09) and no job runs (no DP-10).

**Dependencies the tables add and the plan does not hold.** The payment subscription is class I in kind and the plan's I row is empty, so the step is built against the event's document and fake on Day 1 and the absence is recorded as GAP-2721 and GAP-2722 (ASM-4519). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19; no other H row is added, so the lane stays at depth two.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimWorkflow` subrogation step | Workflow | Waits for the payment fact, matches it, applies the rule, records the position and reports the two case moves to the parent |
| `matchFullPayment` | Activity | Matches the fact to the claim, compares the paid amount with the guaranteed amount and returns the full-payment flag |
| `evaluateSubrogationRules` | Activity | Runs the GUARANTEE rule set in force in the service's own Drools kit and returns the rule row, its version and the target state |
| `recordAndApply` | Activity | Writes the claim row, the position, the decision record and the outbox in one transaction and returns the answer |
| `PaymentEventConsumer` | Consumer | The inbox subscription on `rwb.payment.events.v1`, keyed by the payment reference, signalling the workflow once per fact |
| `GuaranteeClaimRepository` | Repository | Reads and writes `guarantee_claim` only, with the optimistic `version` |
| `SubrogationRecordWriter` | Library adapter | Writes one record per position, hash-linked, and refuses the step when the write fails (DP-03) |
| `SubrogationController` | Controller | The claim-update slice, its right, its `version` check and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `SubrogationPosition` | React component | Shows the claim, the payment, the position, its share and its basis, and the paid, held and not-recorded states on SCR-17, read only |

**Database and migrations.** No Flyway file. `rwb_guarantee` and its login arrive with the DB story of this service, `guarantee_claim` is already the service's table, and the decision record and the idempotency key are library objects created in the schema by the library's migration (DP-03). No column is added for the position: it is an element of the answer and of the record until the data owner names the field (BR7).

**Configuration and reference data.**

- The share, its basis and its effective scope, read as rows in force with their version and never as constants (GAP-2724).
- The GUARANTEE rule set of the workbook and its version in force, read through the service's rule kit.
- The claim type and claim status lists `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS`, referenced with their identifiers and never enumerated in code.
- The capability area Treatment and offer and its right U, as access rows read through the guard.
- The TCG share has no external source today: INT-29 is "Not available today", so no interface, endpoint or file of TCG is configured (GAP-2724).

**Build steps**

1. The subrogation step of `GuaranteeClaimWorkflow` and its input record, registered on `rwb-guarantee`, started when the case enters the guarantee stage.
2. `PaymentEventConsumer` against the event fake, with the inbox key, the replay path and the no-event path (X5, X6).
3. `matchFullPayment`, with the full, the partial and the unmatched-reference paths (X4).
4. `evaluateSubrogationRules` with the GUARANTEE set in force and the missing-rule path (X7).
5. `GuaranteeClaimRepository` and the optimistic `version`, with the stale-version refusal (X5).
6. `recordAndApply` and the record with the rule id and version, the claim, the payment reference and the share (AC1, AC3).
7. `SubrogationRecordWriter` against the library stub, with the failed-write path (AC4, X1).
8. The two case moves to the parent, with the `PAID` claim status in the same transaction (AC2, AC3).
9. `SubrogationController` with the right, the `version` check and the problem mapping (TC-E4-016-05).
10. `SubrogationPosition` and SCR-17 through the composite route fake, and the boundary test: no statement outside `rwb_guarantee`, no `v_ace_*` read, no write to a foreign schema, no outbox row of an event (X8, BR8, BR9).

**Feature flag.** `rwb.guarantee.subrogation-v1`, read as a flag of the platform library; off means a full payment holds the claim at `CLAIM_PAID` with no position, the stage raises a task and no guarantee is closed without one.

**Done when.** The tests of section 16 pass, a full posted payment sets exactly one position and one record in SIT, a partial payment sets none, a replayed fact sets none twice, a stale version is refused, a forced record failure changes nothing and shows MSG-P7-003, no case row and no `v_ace_*` read exists in the build, and SCR-17 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the claim, of the payment fact or of the share is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without right U of Treatment and offer calls the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the position is applied (X1, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product behind the claim is stale after a late or failed ACE batch (X7, VR-S3-004-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The three legacy message IDs and their text are the rows of the legacy Validation and messages table of this key, copied unchanged; MSG-P1-001 is the row of FSD S3 A2.4.3.1 and of VR-S3-004-1. No message is reworded, no new one is added and no message carries a share, an amount or a deadline.

### 15. Screens and states

SCR-17 Guarantee claim is served through the gateway-bff composite route (DP-19), and this story fixes the subrogation part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused | Loading while the claim and the payment fact are read; paid with the payment, the position, the share and its basis; held with the missing element named; not recorded with MSG-P7-003; refused with MSG-P4-002. The legacy "not due", "due" and "submitted" states belong to the preparation and tracking stories, and "refused" to the rejection path of the claim |

The legacy screen row of this key lists the five states above and no separate state for the position, so the position is shown inside the paid state and SCR-17 needs no sixth state (GAP-2720). The screen's field list, its merge order and its other elements belong to RWB-PLT-N001-CON and the sibling stories of this service; the position element list and the three service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-016-01 | AC1: a full posted payment sets the position, the answer carries it and the record carries the rule version; a claim with no matching payment sets nothing | Component | Claim `CLM-2027-000416` on case `RC-2027-000416` with a paid amount equal to the guaranteed amount, and a claim with no matching payment |
| TC-E4-016-02 | AC2: rule R-GUA-22 matches the payment, sets the position and reports `CLAIM_PAID` | Component | A claim at `CLAIM_SUBMITTED` and a full posted payment for the same case |
| TC-E4-016-03 | AC3: rule R-GUA-23 records the TCG share and reports `SUBROGATION_POSITION` | Component | A claim at `CLAIM_PAID`, a share row in force and an effective scope |
| TC-E4-016-04 | AC4: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no position set and MSG-P7-003 shown |
| TC-E4-016-05 | Access: a role without the right is refused with MSG-P4-002 | Component | A role without U of Treatment and offer, and an out-of-scope claim; 403 before any read |
| TC-E4-016-06 | Principle 5: a forced decision log write failure stops the action | NFR | A forced failure at the moment of the claim write; no position, no record and no case move |
| TC-S3-E4016-APP-01 | The boundary: no foreign schema write, no `v_ace_*` read and no published event | Component | The build scan of step 10, plus an outbox that must stay empty |
| TC-S3-E4016-APP-02 | The payment edge: the partial payment, the replayed fact, the stale `version`, the unmatched reference and the missing share row | Component | A partial payment, the same fact twice, a claim whose `version` has moved, an event with an unknown reference, and a case with no share row in force |

The six legacy case IDs are the legacy cases of RWB-E4-016 in their legacy order, with the Level column added: TC-E4-016-01 to -04 cover the four criteria, -05 the access path and -06 the principle-5 failure. They are Component because the step is tested on its fakes; the legacy wording of each case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases. The two `TC-S3-E4016-APP-` cases are new and cover the parts no legacy case touches. The `-ITG` copies belong to the wave 3 harness, RWB-ITG-W3J01, which owns the cross-service journey of this key.

### 17. Guardrails

- No business value in code: the share, its basis, its scope, the claim lists and the rule version stay rows read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_guarantee`, in a workflow input, in an answer or in a log: identifiers, codes, amounts, dates and versions only, and the record names the officer's role and never the officer.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the legacy `v_ace_payment` read is retired rather than moved (DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case`, `assignment`, `task`, `timer`, `proceeds` or ALS and GL row is written, and the case moves are reported and not applied (BR3, BR4).
- The position is recorded before it applies and the fact is consumed once; a build that sets a position before its record, or twice for one payment, fails the review (DP-03, BR5, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no direct ACE payment view read, no event published by this step.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-016, disposition Split (rework); AC1, AC2, AC3 and AC4 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-GUA-04 Record the subrogation position, module S3, epic E4, runs unattended, systems ALS and GL and Workbench, depends on FEAT-GUA-03 | 1, 2, 3 |
| FSD S3 v3 | A1.4 preconditions; A2.4.2 steps and integration points; A2.4.3.1 VR-S3-004-1 and BR-S3-004; A2.4.3.3 roles; A2.4.4.3 exception flows; requirements REQ-S3-001 to REQ-S3-007, REQ-S3-003 in particular; SCR-17 | 2, 3, 4, 5, 8, 14, 15 |
| TSD S3 v2 | T2 components; T3.0 standard columns; T3.1 `guarantee_claim`; T3.2 `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS`; T3.3 relationships; T4 GUARANTEE state machine; T5.1 INT-29; T5.3 no event; T6.1 rights; T-A.1 and T-A.2 API-S3-002 | 3, 9, 10, 11, 12, 13, 16 |
| Epics 3 to 8 Specification v3 | The feature row of FEAT-GUA-04 with its unattended role, its systems and its dependency on FEAT-GUA-03 | 1, 2, 3, 8 |
| Business rules | R-GUA-22, R-GUA-23 and R-GUA-24 of the Guarantee claim route set, with their from-state, event, condition, action and to-state; R-GUA-25 and R-GUA-26 as the follow-on rows | 4, 8, 9 |
| Logical data model | DF-TRT-015 to DF-TRT-022, DF-CAS-001 to DF-CAS-023, DF-CAS-030 to DF-CAS-035, DF-WRK-027 to DF-WRK-036, DF-ACE-043 to DF-ACE-054, DF-DEC-001 to DF-DEC-018 | 11 |
| Architecture v5 | Slide 3, the guarantee claim route and the parallel routes; slide 8, the schema, base, topic and queue of the service and the ACE views closed to it; slide 13, S3 temporal to P7 and subscriptions from P6 and P8; slide 5 and 13 of the Temporal design, the S3 scenario and the child-per-stage model | 2, 3, 4, 12 |
| Sibling stories | RWB-S3-E4016-CON, which baselines the surface this story touches; the preparation, submission, tracking, notice and close stories of this service | 1, 2, 3, 9, 12 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2720 to -5; ASM-4518 to -6 | 1, 3, 4, 5, 8, 9, 11, 12, 13, 14, 15, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published element set of the claim update, the position elements, the payment event element, the rights, the error envelope and the fakes: RWB-S3-E4016-CON.
- The preparation and submission of the claim, its checklist and its reference: FEAT-GUA-01 and FEAT-GUA-02.
- The tracking of the claim, the claim deadline timer, the service-level breach and the partial-payment path: FEAT-GUA-03, and R-GUA-20 and R-GUA-21.
- The close of the guarantee and of the case, R-GUA-25 and R-GUA-26, and the residual return to the route decision: FEAT-GUA-07.
- Guarantor notices, negotiation and the dispute holds: FEAT-GUA-05, FEAT-GUA-06, R-GUA-06 and R-GUA-29 to R-GUA-32.
- The posting, the ALS and GL entries, the `proceeds` row and the payment event's own shape: rwb-payment (P8) (GAP-2721).
- Where the position and the guaranteed amount are stored as a field: their data owner, carried by GAP-2720. The source of the share: GAP-2724 and INT-29.
- The case of record, its states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-17: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
