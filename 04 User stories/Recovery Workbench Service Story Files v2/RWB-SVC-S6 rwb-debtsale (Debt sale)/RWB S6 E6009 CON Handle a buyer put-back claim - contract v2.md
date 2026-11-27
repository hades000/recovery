# RWB-S6-E6009-CON Handle a buyer put-back claim - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S6-E6009-CON-16) |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the put-back claim step of rwb-debtsale, split from RWB-E6-009. It fixes the claim element and the answer shape it appears in (DP-13), the lot and account elements and their closed lists, the six consumed rows for the rwb-partner claim and sale terms, the rwb-case move answer and claim-window parameter, the rwb-decision package and the rwb-access right, the decision-record element of DP-03, the realized-recovery element, the rights and the error envelope, the fakes and the absence tests. TSD S6 appendix T-A publishes no claim operation, so the baseline declares no operation as provided and records the two legacy endpoint rows as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's; the claim and the sale terms belong to rwb-partner (S9), the case states to rwb-case (P3), and the realized recovery has no column and no event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6009-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the put-back claim step of rwb-debtsale — the claim element and the answer shape it appears in, the lot and account elements with their closed lists, the six consumed rwb-partner, rwb-case, rwb-decision and rwb-access rows, the decision-record element, the realized-recovery element, the rights, the error envelope and the fakes**, so that **the app story, SCR-26 Award, PRT-05 Data room and the wave 4 harness build against one fixed, testable contract on Day 1 and a claim state, a list value, a move name, a window parameter or an answer shape can never drift between rwb-debtsale, rwb-partner, rwb-case, rwb-decision and rwb-access without a failing build**.

This is the contract slice of legacy RWB-E6-009 and it copies none of the legacy criteria, which stay word for word with RWB-S6-E6009-APP. It owns the shapes and the absence tests only: no table, no row and no workflow is created here.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy claim of RWB-E6-009 crossed four boundaries at once: a buyer's claim, the sale terms, a case route state and a decision log. The target splits them: rwb-partner owns the buyer, the sale terms and the claim, rwb-case owns the case and its route states, rwb-access owns the right, rwb-decision owns the package and the claim-window parameter with its ledger, and rwb-debtsale owns the sold account, its claim state and the lot close. Each boundary is a contract that another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming that the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Architecture v5 slide 19 notes).

Five points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs six consumed contracts (GAP-3009; ASM-4969). TSD S6 T-A publishes no claim operation, and the two endpoint rows of the legacy story are the award path and the data room read of two sibling stories (GAP-3009; ASM-4970). The claim window has no length, no parameter name and no column (ASM-4971). The realized recovery by lot and by buyer has no column and no event, and the data lake behind the monolith's Power BI is removed by DP-17 (ASM-4972). And the transfer and posting whose states the criteria start from belong to two sibling stories (ASM-4973). The wave is EP06's wave 4 while the service is created in wave 3, recorded once for the service and the epic (ASM-4974).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `partner` and `partner_user` are S9's, `recovery_case` and `assignment` are P3's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The rwb-partner claim and sale-terms contract, the rwb-case state and move rows, the rwb-access authorise contract and the rwb-decision package and parameter rows are published with their fakes; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3009; ASM-4969).
- The Debt sale rule package and its rows for R-DS-29, R-DS-34 and R-DS-35 to R-DS-39, and the claim-window parameter, are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (GAP-3009; ASM-4972).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the claim element and the answer shape it is embedded in, with the rights and the error responses, and no operation of its own (GAP-3009; ASM-4970).
2. Fix the lot and account elements: the lot reference, the account set, the selling price, the claim state against `LOV-PUTBACK`, the lot status against `LOV-LOT-STATUS` and the realized-recovery element.
3. Fix the consumed rows: the rwb-partner claim and sale-terms read, the rwb-case state read and move answer, the rwb-access authorise call, the rwb-decision package read and the claim-window parameter read, marking the fields the sources do not give with the placeholder.
4. Record the decision-record element of DP-03, written before the claim row changes.
5. Record the closed vocabulary of the lists, the naming baseline and the rule that no value is a constant of the code.
6. Record that the buyer is an organisation and that no person name, identity number, date of birth or contact value is a property of any element, example or fake.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a provided operation, the absence of a `partner`, `recovery_case` or `proceeds` property, the drift between a fake and the document, and the absence of published and consumed events of this step.
9. After the operation names of step 3 are confirmed with their owners, tag the baseline, record the tag date in the contract README, and hand it to RWB-S6-E6009-APP, SCR-26 Award, PRT-05 Data room and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A value outside `LOV-PUTBACK`, `LOV-LOT-STATUS`, `LOV-SEGMENT` or `LOV-BUYER-CLASS` appears in the document or in an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares a provided operation, a `partner`, `recovery_case` or `proceeds` property, or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC4, AC6 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC6 |
| X8 | A person field — a name, an identity number, a date of birth or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC1, AC5 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-partner, rwb-case, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6009-APP, SCR-26 Award, PRT-05 Data room and the wave 4 harness on Day 1, and the rwb-partner, rwb-case, rwb-access and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, nine contract tables, seven fakes and six new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the put-back claim step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of partner and partner_user is S9, of recovery_case and assignment is P3, of role is P4 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The claim element and its answer shape are declared with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the claim element with the lot reference, the account reference, the claim reference, the claim state, the rule ID with its version and the decided-at time, and it declares no operation of its own
    Then it records that the element is embedded in the answer of the lot read API-S6-002 and of the data room read API-S6-004, which are the lot read story's and RWB-S6-E5026-APP's, and that it narrows neither answer
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the answers is copied from the baseline that owns the operation and is not redefined here

  Scenario: AC2 The lot and account elements and their closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1 and T3.2 and the rule rows R-DS-34 to R-DS-39
    Then the Lot element declares the lot number, the cut-off date, the segment, the reserve price, the buyer partner reference, the buyer class, the signing date, the approval authority, the payment terms and the lot status
    Then the SoldAccount element declares the lot reference, the account reference, the borrower code, the outstanding, the selling price and the put-back status, and it declares no claim reason, no claim date and no claim-window column because TSD S6 T3.1 carries none (GAP-3009; ASM-4972)
    Then put_back_status is declared against LOV-PUTBACK with the values NONE, CLAIMED, ACCEPTED and REJECTED, and status against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED
    Then segment is declared against LOV-SEGMENT with the values RETAIL, SSME and CORPORATE, and buyer_class against LOV-BUYER-CLASS with the values AMC and NON_AMC
    Then the lot reference, the account reference and the claim state are required and the other properties are optional
    Then no property carries a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The consumed rows for the rwb-partner claim and the sale terms are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-partner contract and Architecture v5 slide 41
    Then the claim and sale-terms read is declared as consumed from S9 rwb-partner, with the claim reference, the sold account reference, the sale terms in force and the buyer organisation reference
    Then the operation name of the row is Not specified in the source documents (GAP-3009; ASM-4969) and the row carries the placeholder, with the read family GET /partners named as the Ownership Map family it belongs to
    Then the document declares no partner, partner_user or sale-terms table property and no grant on rwb_partner
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-case move answer, the rwb-decision rows and the rwb-access right are fixed (new, D-RCV-60)
    Given the consumed rows, the decision section and the access section of the baseline
    When they are compared with rwb-case as the owner of recovery_case, with the rule package registry, with TSD S6 T6.1 and with the platform error envelope
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the move PUTBACK_RAISED, PUTBACK_UPHELD, PUTBACK_REFUSED, BACK_TO_CASE_LIST or LOT_CLOSED carrying the rule ID and its version
    Then the operation name of the case-move answer is Not specified in the source documents (GAP-3009; ASM-4969) and the row carries the placeholder
    Then the Debt sale package read is declared as consumed from P7 rwb-decision with the rows R-DS-29, R-DS-34 and R-DS-35 to R-DS-39 named and not declared, and the claim-window parameter is declared as a versioned value whose length is Not specified in the source documents (GAP-3009; ASM-4971)
    Then the capability area Debt sale with right C, R, U or A and Partner portal with right R are declared as consumed from P4 rwb-access, with RW-DEBTSALE CRUA, RW-PRODHEAD RA, RW-HEADASL RA, PT-BUYER RU scoped to its own lots and the SY-* identities R as TSD S6 T6.1 gives them
    Then a refused caller answers 403 with MSG-P4-002, and a repeated claim or close with the same Idempotency-Key describes no second effect
    Then the document declares no recovery_case, assignment, proceeds or decision_log_entry property

  Scenario: AC5 The realized-recovery element and the fakes answer the document (new, D-RCV-60)
    Given the recovery section and the fakes of the baseline
    When each is compared with TSD S6 T3.1 and with the operation or the element it serves
    Then one realized-recovery element is declared by lot and by buyer from the selling price of the closed lots' account set, and it is declared on the lot read and not as a column of debt_sale_lot or debt_sale_account (GAP-3009; ASM-4972)
    Then one decision record is declared per claim outcome with the case reference, the lot reference, the account reference, the claim reference, the rule ID, the package version in force, the inputs reference, the outcome, the reason, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the claim row changes, and a failed write leaves the account unchanged with MSG-P7-003
    Then the rwb-partner fake answers the claim PB-2026-000017 on the account ACC-2026-000451 inside the sale terms, the same claim outside them, a claim on a lot that is not in GL_POSTED, no claim and no answer beyond 2 s
    Then the rwb-case fake answers the states SETTLED, DATA_TRANSFERRED, GL_POSTED, PUTBACK_RAISED, PUTBACK_UPHELD, PUTBACK_REFUSED and LOT_CLOSED and an accepted and a refused move, the rwb-access fake answers the two capability areas with and without the right, the rwb-decision fake answers the package at its version and the rwb-case parameter fake answers the claim-window parameter at its version
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged award and data room screens for lot LOT-2026-000042
    Then every fake carries organisation references, codes, amounts, dates and a rule version only, with no person name, identity number, date of birth or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The naming baseline and the boundary are fixed and this step publishes and consumes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that TSD S6 T-A publishes no claim operation and that the award path API-S6-003 and the data room read API-S6-004 are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and partner, partner_user, recovery_case, assignment, role, permission, document, notice, proceeds, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event for this step, and it records that LotAwarded (EV-23) and AccountsTransferred are sibling stories' and ProceedsMatched is the settlement step's, and that the realized recovery has no event
    Then the partner channel is recorded as reaching the same element through the partner gateway in the DMZ, which has no row in the plan (GAP-3009; ASM-4970)
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6009-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

Scenario: AC7 Every rule BR1 to BR13 of section 8 has a criterion and a test case that proves it (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The sold account and the lot are rwb-debtsale's, and the contract declares their fields, their lists and their required flags on the lot and account elements only | Architecture v5 slide 41; TSD S6 T3.1 and T3.2; GAP-3009 |
| BR2 | The claim state is declared as the single value of `LOV-PUTBACK`, and one account carries one state; the contract declares no claim history element | TSD S6 T3.2; R-DS-35 to R-DS-38 |
| BR3 | The decision record is declared as an element written before the claim row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-009 AC1 and AC4 |
| BR4 | The claim and the sale terms stay with rwb-partner: the contract declares the claim read as consumed and declares no partner property and no sale-terms storage | Architecture v5 slide 41; Ownership Map (`partner`, `partner_user` owner S9); GAP-3009 |
| BR5 | The case move is answered and not written: the contract declares the state read and the five moves, and declares no `recovery_case` property, no `assignment` property and no case row write; the case boundary is the child workflow's input, signals and stage outcome | Ownership Map (recovery_case owner P3); ASM-4975 |
| BR6 | This baseline declares no provided operation: the step runs behind the lot read and the data room read of its siblings | TSD S6 T-A.1; GAP-3009 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none; the surfaces this element appears in are reads | Architecture v5 slide 11; TSD S6 T-A.2 |
| BR8 | The claim window is declared as a versioned parameter whose length is a placeholder; no window length is an enumeration member or a schema default | R-DS-34 ("per claim window"); ASM-4971 |
| BR9 | The realized recovery is declared on the lot read only, from the selling price of the account and the closed lot, and is not a column of either table; no data lake output is declared (DP-17) | R-DS-34 and R-DS-39; TSD S6 T3.1; ASM-4972 |
| BR10 | The vocabulary is closed: `LOV-PUTBACK`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-BUYER-CLASS` are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-013 |
| BR11 | No personal data in a schema, an example or a fake: the buyer is a partner organisation, the account is a masked reference, and no name, identity number, date of birth or contact value is declared | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 |
| BR12 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR13 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |

Rule coverage: BR1 AC2, TC-E6-009-01, TC-S6-E6009-CON-02; BR2 AC2, TC-E6-009-02, TC-S6-E6009-CON-02; BR3 AC4, AC5, TC-E6-009-04; BR4 AC3, TC-E6-009-01, TC-S6-E6009-CON-03; BR5 AC3, AC4, TC-E6-009-02, TC-S6-E6009-CON-03; BR6 AC1, TC-S6-E6009-CON-01; BR7 AC6, TC-E6-009-06; BR8 AC4, TC-E6-009-03; BR9 AC5, TC-E6-009-03; BR10 AC2, TC-E6-009-03, TC-S6-E6009-CON-02; BR11 AC6, TC-E6-009-06; BR12 AC6, TC-S6-E6009-CON-03; BR13 AC1, TC-S6-E6009-CON-01. AC7 covers all of BR1 to BR13 and is proved by TC-S6-E6009-CON-05.

### 9. State transitions

The lifecycle of this document, not of a claim:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the lists, the consumed rows, the parameter and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-26 Award, PRT-05, the wave 4 harness and the rwb-partner, rwb-case, rwb-access and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional claim date | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC6 fail: a provided operation, a `partner`, `recovery_case` or `proceeds` property, an event or a Schedule | In review |

The claim state machine that the document describes is the app story's: a sold account moves from `NONE` to `CLAIMED`, then to `ACCEPTED` or `REJECTED`, and the lot closes when the window closes. This baseline fixes the vocabulary of those states and moves no account.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent claim operation, the claim-window parameter and the partner channel |
| Consuming teams (the app story, SCR-26 Award, PRT-05, the wave 4 harness and the owners of rwb-partner, rwb-case, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, that the buyer is an organisation and that the account is a masked reference |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline. The partner gateway in the DMZ is the edge owner's and is named here only as the channel (GAP-3009; ASM-4970).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Claim element | BR2 | The lot reference, the account reference, the claim reference, the claim state against `LOV-PUTBACK`, the rule ID with its version and the decided-at time |
| Lot and account elements | BR1 | DF-SAL-020 to DF-SAL-037 of TSD S6 T3.1, with `status` (DF-SAL-030), `selling_price` (DF-SAL-036) and `put_back_status` (DF-SAL-037) as the columns the step writes, and no claim reason, claim date or window column declared because none exists (GAP-3009; ASM-4972) |
| Lists | BR10 | `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), published as enumerations and read as reference data at their version |
| Realized recovery | BR9 | An element by lot and by buyer, derived from the `selling_price` of the closed lot's account set, on the lot read only; no column and no event (ASM-4972) |
| Decision record | BR3 | DF-DEC-001 to DF-DEC-018 through the local library, written before the claim row changes (DP-03) |
| Claim and sale terms | BR4 | The claim reference, the sold account reference, the sale terms in force and the buyer organisation, of S9 rwb-partner, read only through the owner's contract and never copied or joined here (GAP-3009; ASM-4969) |
| Not declared here | BR4, BR5, BR12 | `recovery_case` and `assignment` (P3), `partner` and `partner_user` (S9), `role` and `permission` (P4), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) |
| Consumed fields with no source | BR4, BR8 | The operation names of the rwb-partner claim read, the rwb-case state read and move answer, the rwb-access authorise call and the rwb-decision parameter read, and the claim-window length: Not specified in the source documents (GAP-3009; ASM-4969; ASM-4971) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR13. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a claim or a claim-decision operation. The two endpoint rows of the legacy story are API-S6-003 and API-S6-004; they are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, and API-S6-005 belongs to the take-bids story of this service. This baseline therefore declares no operation as provided, records the two sibling rows by name, and fixes only the claim element and the answer shape it is embedded in. The absence is recorded as GAP-3009 with ASM-4970.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The buyer claim and sale-terms read (operation name Not specified in the source documents (GAP-3009; ASM-4969)) | `/api/recovery/partner/v1` | S9 rwb-partner | The claim reference, the sold account reference, the sale terms in force and the buyer organisation; faked. The read family of the Ownership Map is `GET /partners` |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the lot and account link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3009; ASM-4969)) | rwb-case (P3) | P3 rwb-case | The move `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED`, `BACK_TO_CASE_LIST` or `LOT_CLOSED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3009; ASM-4969)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Partner portal", the right of the caller and the scope of its own lots; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39; faked |
| The claim-window parameter and its version (operation name Not specified in the source documents (GAP-3009; ASM-4971)) | `/api/recovery/case/v1` | P3 rwb-case | The claim-window parameter of R-DS-34 and R-DS-39 at its version, on the parameters contract the default ruling gives rwb-case, with a placeholder for its length; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3009 with ASM-4969. The contract version is fixed: each row is pinned to its `/v1` path version as the story paths state; the yaml that must declare each base is tracked as CG-ALL-10742 to CG-ALL-10746.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (EV-23) and `AccountsTransferred`. `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's; the claim outcome and the lot close produce neither, and the service's event set carries no recovery or claim event, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC6 fails a build that adds one (ASM-4972).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched`, which belongs to the settlement step of this service, and no event of the module carries a buyer claim or a claim-window close. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC6 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement and the claim window | `rwb-debtsale` | The stage that hosts the claim step; its signals, its durable window timer and its outcome for the parent are declared, not built. Workflow ID form: Not specified in the source documents (CG-ALL-10748). Start rule: opened by the monthly sale cycle or a residual arriving from disposal (R-DS-01); the start call and the duplicate-start policy: Not specified in the source documents (CG-ALL-10748) |
| `reviewPutbackClaim` | Activity, the one claim step | `rwb-debtsale` | The lot, the case, the account and the claim in; the rule ID with its package version, the claim state and the case move out |
| `closeLotOnClaimWindow` | Activity, the claim-window close | `rwb-debtsale` | The lot, the account set and the window parameter in; the lot close, the realized recovery and the case move out |

No child workflow for the case and none for the money exists in this service. The activity names are a target design choice. No activity is registered by this story, and the saga steps of reserve, approval, payment, transfer, proceeds, case closure and customer notices belong to the award, settlement, transfer and posting stories of this service.

#### 12.6 Schedules

None. The step runs from the claim and from a durable timer of the workflow; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer, its terms and its status; the columns the claim and the close read and write |
| debt_sale_account | S6 (`rwb_debtsale`) | The sold account, its outstanding, its selling price and its put-back status; the claim state is its column |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the claim outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated claim or close and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the service's sibling stories relay their events through; this step declares no row |

`partner` and `partner_user` (S9), `recovery_case` and `assignment` (P3), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner claim fake | The claim `PB-2026-000017` on the account `ACC-2026-000451` inside the sale terms, the same claim outside them, a claim on a lot that is not in `GL_POSTED`, no claim, no answer beyond 2 s and an unreadable answer | AC3, AC5 |
| rwb-case state and move fake | The states `SETTLED`, `DATA_TRANSFERRED`, `GL_POSTED`, `PUTBACK_RAISED`, `PUTBACK_UPHELD`, `PUTBACK_REFUSED` and `LOT_CLOSED` of case `RC-2026-000842`; an accepted move and a refused move for each of the five move names | AC4, AC5 |
| rwb-access authorise fake | The capability areas "Debt sale" and "Partner portal" with their rights for the TSD S6 T6.1 roles; a caller without the right | AC4, AC5 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-29, R-DS-34 and R-DS-35 to R-DS-39 | AC4, AC5 |
| rwb-case claim-window parameter fake | The claim-window parameter at its version in force, and a parameter set without the window | AC4, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-26 Award and PRT-05 answers for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the claim element once, and the partner gateway route for the organisation `PTR-2026-000031` scoped to its own lot | AC1, AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner claim read, the rwb-case move answer, the rwb-access authorise call and the rwb-decision parameter read are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3009; ASM-4969). The partner gateway fake stands in for a channel that has no story row (ASM-4970).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-partner claim read, the rwb-case state read and the case-move answer, the rwb-access authorise call, the rwb-decision package read and the rwb-case claim-window parameter read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` (EV-23) and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the settlement step's; no claim event exists |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `DebtSaleWorkflow`, `reviewPutbackClaim` and `closeLotOnClaimWindow` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the partner portal |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no claim, lot, case, buyer record or rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, seven fakes and six new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the claim element, the `Lot`, `SoldAccount`, `PutbackClaim` and `RealizedRecovery` elements, the vocabulary of the four lists as published enumerations, the contract README rows for the six consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record and the claim update commit together or not at all. DP-13 moves the base and nothing else. DP-19 is behind SCR-26 Award and PRT-05, whose screen model is the edge contract's, and the partner channel reaches the same element behind the partner gateway, which the plan does not carry (ASM-4970).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. It leaves out the six consumed rows, which are C dependencies in fact and not in the metadata row, and the DP-06 parameter and DP-08 guard the step uses; neither is added to the metadata rows (GAP-3009; ASM-4969; ASM-4971).

**Build steps**

1. Write the claim element and the answer shape of AC1, with the no-provided-operation record, and validate the additive rule in the pipeline.
2. Write the `Lot` and `SoldAccount` elements, their required flags and the four lists of AC2 with the placeholder where a type is unstated.
3. Record the rwb-partner row of AC3 with its owner, its budget and its placeholder.
4. Record the rwb-case rows of AC4, the five move names and the state vocabulary, and the rwb-decision package and claim-window parameter rows.
5. Record the rwb-access rights and the error envelope of AC4.
6. Record the realized-recovery element of AC5 and the decision-record element, and validate both against the library schema.
7. Publish the seven fakes of AC5 and the drift test.
8. Record the naming baseline, the boundary and the partner channel of AC6, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the five contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-26 Award, PRT-05 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account selected for a lot, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the partner identity lacks the Debt sale or the Partner portal right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the claim row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE product that carries the account balance is stale after a late or failed batch; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001, which is copied from the Error and Message Standard v4 (CG-ALL-10751); no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data.

Error binding of the status codes of TSD S6 T-A.2: 403 uses MSG-P4-002, 422 uses MSG-GEN-001 and 409 uses MSG-P7-003; 401, 404 and 503 have no message in the source documents and are Not specified in the source documents (GAP-3009).

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states and PRT-05 Data room in its data room, bid and claimed states, all read only. SCR-26 has no empty, loading, error or no-access state in Screen Specifications v1: each is Not specified in the source documents (CG-ALL-10753). The staff route is the gateway-bff composite route (DP-19); the partner route is the partner gateway in the DMZ, which fronts rwb-partner and reaches the same claim element scoped to the buyer's own lots (ASM-4970). The route calls rwb-debtsale for the lot, the account set, the claim element and the realized recovery, rwb-case for the case and its route state and rwb-partner for the claim and the sale terms; this baseline fixes the claim element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded, wrong-state and stale-data states the app story shows read the messages of section 14 on the same routes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-009-01 | AC1, AC2, AC3 | Contract | Lot `LOT-2026-000042`, account `ACC-2026-000451` and claim `PB-2026-000017`; the contract half answers the claim element, the lot and account elements and the claim and sale-terms row |
| TC-E6-009-02 | AC3, AC4 | Contract | The transfer and posted states of case `RC-2026-000842`; the contract half answers the `PUTBACK_RAISED` move shape and the state vocabulary |
| TC-E6-009-03 | AC2, AC4, AC5 | Contract | A closed lot with no claim; the contract half answers the `LOT_CLOSED` move shape, the realized-recovery element and the lot status vocabulary |
| TC-E6-009-04 | AC4, AC5 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-009-05 | AC4 | Contract | RW-DEBTSALE holds CRUA and PT-BUYER holds RU scoped; the contract half answers the rights of the two capability areas |
| TC-E6-009-06 | AC5, AC6 | Contract | A malformed request, an absent claim answer and a forged event; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6009-CON-01 | AC1 | Contract | The fragment validates; the claim element, the seven error answers and the no-provided-operation record are present |
| TC-S6-E6009-CON-02 | AC2 | Contract | The `Lot` and `SoldAccount` elements validate with their properties, their required flags and the four closed lists |
| TC-S6-E6009-CON-03 | AC3, AC4, AC5, AC6 | Contract | The six consumed rows with their placeholders, the five move names, the seven fakes, the drift test and the absence of a published or consumed event, of a second topic and of a Schedule |
| TC-S6-E6009-CON-04 | AC2 | Contract | Boundary of the five owned tables of §12.7: every owned table is declared, every table named as not owned is absent, and no foreign key leaves the schema (DP-01) |
| TC-S6-E6009-CON-05 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-S6-E6009-CON-AC7) |

The six legacy cases are the legacy cases of RWB-E6-009 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6009-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The three cases `TC-S6-E6009-CON-01` to `-03` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the claim-window length, the `LOV-PUTBACK` and `LOV-LOT-STATUS` values, the 10-working-day target and the rule rows stay data, reference data, parameters or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: the buyer is a partner organisation, the account is a masked reference, and no name, identity number, date of birth, address or contact value is declared; every example is synthetic.
- The claim and the sale terms stay with rwb-partner, the case with rwb-case, the settlement with rwb-payment and the posting with the GL story: the document declares no `partner`, `recovery_case`, `assignment` or `proceeds` property and no ACE table read (BR4, BR5).
- The central ledger stays with rwb-decision: the document declares no `decision_log_entry` column and no rule-row column as its own.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 and API-S6-004 are named as the surfaces the step runs behind and as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, never as provided here (GAP-3009).
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row, a shared job table or a data lake extract (DP-17).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-009 | A put-back claim from a buyer is reviewed against the sale terms and either accepted or refused with a reason; the contract fixes the element, the consumed rows, the lists and the parameter on which the review is built (FSD S6 Requirements served; Business Requirements Program v5); the split plan carries no requirement id for this slice (GAP-3009; ASM-4969) | The claim element, the `Lot` and `SoldAccount` elements, the six consumed rows and the claim-window parameter | TC-E6-009-01, TC-E6-009-02, TC-S6-E6009-CON-01, TC-S6-E6009-CON-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S6-E6009-CON-03 |
| ADR-018 | No data lake; rwb-reporting read model from events | The realized-recovery element served from the lot read and the removed Power BI output | TC-S6-E6009-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S6-E6009-CON-02, TC-S6-E6009-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the claim changes | TC-E6-009-04, TC-S6-E6009-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-009, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6009-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the three new contract cases TC-S6-E6009-CON-01 to -03 |
| Feature and screens | FEAT-DBS-13 Handle a buyer put-back claim, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-29, R-DS-34 and R-DS-35 to R-DS-39, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-018 (no data lake), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-DS-34 to R-DS-39, the decision record, the claim state, the lot close and the five case moves: RWB-S6-E6009-APP.
- The transfer under R-DS-29 and its `DATA_TRANSFERRED` move: RWB-S6-E6007-APP (GAP-3009).
- The derecognition, the posting and the reversal under R-DS-30 and R-DS-31: RWB-S6-E6008-APP (GAP-3009).
- The settlement adjustment of an upheld claim: rwb-payment (P8) and the settlement story of this service.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP; the data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP; the bid submission API-S6-005: the take-bids story of this service.
- The claim, the sale terms, the partner users and the buyer's identity: rwb-partner (S9) (GAP-3009).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked (ASM-4975).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3009).
- The authoring, testing, approval and versioning of the Debt sale package, of the rule rows of R-DS-29 to R-DS-39 and of the claim-window parameter: rwb-decision (P7) (ASM-4971).
- The read model and the reporting of realized recovery: rwb-reporting (P9), with no event or contract allocated (ASM-4972).
- The gateway-bff composite route and the screen field list of SCR-26 and PRT-05: RWB-PLT-N001-CON and the edge stories.
- The partner gateway in the DMZ and the partner sign-in: the edge stories, with no plan row (ASM-4970).
- The sale documents and the notices of a returned account: rwb-document (P5) and rwb-comms (P6).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
