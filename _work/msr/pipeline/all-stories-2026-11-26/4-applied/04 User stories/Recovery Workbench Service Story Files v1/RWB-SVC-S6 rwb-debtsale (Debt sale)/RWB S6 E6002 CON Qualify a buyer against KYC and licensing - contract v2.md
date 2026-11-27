# RWB-S6-E6002-CON Qualify a buyer against KYC and licensing - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the buyer qualification step of rwb-debtsale, split from RWB-E6-002. It fixes the qualification, buyer and bid elements and the closed lists they use, the rwb-partner buyer row, the rwb-case signal and move contract, the rwb-decision package activity, the rwb-access right, the decision-record element of DP-03, the error envelope, the fakes and the absence tests, on base `/api/recovery/debtsale/v1` (DP-13) behind the gateway-bff composite route (DP-19). TSD S6 appendix T-A publishes no qualification operation and no bid table exists in T3.1, so the baseline declares no operation of its own and records both absences. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6002-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the buyer qualification step of rwb-debtsale — the qualification element and the answer shapes it appears in, the buyer and bid elements with the closed lists, the rwb-partner buyer row, the rwb-case signal and move contract, the rwb-decision package activity, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, the data room, the award screen and the wave 4 harness build against one fixed, testable contract on Day 1, and a buyer fact, a list value, a move name or an answer shape can never drift between rwb-debtsale, rwb-partner, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the connection matrix gives this service the Temporal cell for the case and for the package (context pack, slide 13, row S6). The legacy qualification of RWB-E6-002 crossed four boundaries at once: a partner portal request, the buyer's NDA, KYC and licence facts, a case state and a decision log. The target splits them: rwb-partner owns the buyer and its evidence, rwb-case owns the case and its route states, rwb-decision owns the package and the ledger, rwb-access owns the right, and rwb-debtsale owns the qualification outcome and the bid record. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the values of `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-PUTBACK`, the qualification and bid elements, the buyer fact the partner contract answers, the case state and the move, the right and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4; context pack). Four points are carried as gaps and assumptions instead of decided quietly: the plan's C row is None while the step consumes a partner row (GAP-2985; ASM-4912); TSD S6 T-A publishes no qualification operation, so the baseline declares none and names the sibling surfaces (GAP-2985; ASM-4917); no table carries a bid, so the element is declared and the table is raised (GAP-2985; ASM-4914); and the wave is EP06's wave 4 while the service is wave 3 (ASM-4916).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-partner buyer contract, the rwb-case state and move contract, the rwb-decision package activity and the rwb-access right are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2985; ASM-4912).
- The Debt sale package and its rows for R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).
- The FSD S6 and the TSD S6 are In review, so this baseline is accepted for planning in Draft (realignment v1) under the D-RCV-60 overlay (GAP-2985; ASM-4919).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the qualification element and the answer shapes it is embedded in, with the rights and the error responses, and no operation of its own.
2. Fix the qualification, buyer and bid elements: the lot and buyer references, the buyer class, the qualification state, the rule ID with its version, the decided-at time and the bid amount and window.
3. Fix the consumed rows: the rwb-partner buyer read with its NDA, KYC, licence and panel facts, the rwb-case state signal and move answer, the rwb-decision package activity and the rwb-access right, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before anything changes.
5. Record the closed vocabulary of the four lists, the naming baseline and the rule that no value is a constant of the code.
6. Record that the buyer is an organisation and that no person field is a property of any element, example or fake.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the error envelope, the absence of a provided operation, the absence of a `partner` or `recovery_case` property, the drift between a fake and the document and the absence of published and consumed events of this step.
9. Tag the baseline and hand it to RWB-S6-E6002-APP, the data room, the award screen and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails and the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, a `partner` or `recovery_case` property, a bid table or a write of another owner's row | The review fails the baseline and the boundary test fails the build | None | AC1, AC2, AC7 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | A person field — a name, an identity number, a date of birth or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the S6 context pack, FSD and TSD S6 and the published owner contracts of rwb-partner, rwb-case, rwb-decision and rwb-access only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the lists, the base, the topic and the queue are fixed by the architecture |
| Valuable | Unblocks RWB-S6-E6002-APP, the data room, the award screen and the wave 4 harness on Day 1, and the rwb-partner, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, nine contract tables, five fakes and nine contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the buyer qualification step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The qualification element is declared and no operation is claimed (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the qualification element with the lot reference, the buyer partner reference, the buyer class, the qualification state, the rule ID with its version and the decided-at time
    Then it records that the element is a property of the answer of the data room read API-S6-004, of the bid API-S6-005 and of the lot read API-S6-002, owned by RWB-S6-E5026-APP, RWB-S6-E6004-APP and RWB-S6-E5023-APP, and that it redefines none of those answers
    Then it declares no provided operation, and the award API-S6-003 is named as RWB-S6-E6005-APP's and not declared here
    Then the error answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition

  Scenario: AC2 The buyer and bid elements and the four closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1, T3.2 and the rule rows R-DS-14 to R-DS-18
    Then the Buyer element declares the partner reference, the buyer class, the non-disclosure agreement date, the KYC status, the licence expiry and the panel status as consumed facts of S9 rwb-partner
    Then the Bid element declares the lot reference, the buyer partner reference, the account set of the lot, the amount and the bid window, and records that no table of the service carries it (GAP-2985; ASM-4914)
    Then buyer_class is declared against LOV-BUYER-CLASS with the values AMC and NON_AMC, and status against LOV-LOT-STATUS with BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED
    Then segment is declared against LOV-SEGMENT with RETAIL, SSME and CORPORATE, and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then the lot reference, the buyer partner reference and the buyer class are required and the other properties optional
    Then no property is a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The rwb-partner buyer row is declared and the facts stay with the owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack and with the connection matrix
    Then the buyer read is declared as consumed from S9 rwb-partner, with the partner reference, the nda_signed_at date, the kyc_status, the licence_expiry, the panel_status and the buyer class
    Then its operation name and its call type are Not specified in the source documents (GAP-2985; ASM-4912), because the matrix gives rwb-debtsale no arrow to rwb-partner and the row is declared as a one-hop contract read with a 2 s budget and a breaker
    Then the document declares no partner or partner_user property, no partner table and no grant on any rwb_* schema of another owner
    Then a stale or missing answer is described as the app story's hold path, and no fallback value is declared

  Scenario: AC4 The rwb-case signal and move, the rwb-decision package and the rwb-access right are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with TSD S6 T4, T6.1 and the connection matrix
    Then the case state arrives as a signal from the parent CaseWorkflow and the four moves BUYER_PENDING_KYC, BUYER_CLEARED, BUYER_REJECTED and BIDS_RECEIVED are declared as the stage outcome answer, with the rule ID and its version
    Then no REST case-move operation is declared and the document declares no recovery_case property, because no source publishes one (GAP-2985; ASM-4915)
    Then the package activity of rwb-decision is declared with the Debt sale package, its version, its 41 rules over 29 states and the reference data of the four lists, and its name is Not specified in the source documents (GAP-2985; ASM-4913)
    Then the capability areas Debt sale and Partner portal and their rights are declared as answered by rwb-access, with RW-DEBTSALE CRUA, RW-PRODHEAD and RW-HEADASL RA and PT-BUYER RU scoped to its own lot
    Then a role or a partner identity without the right is described as refused with MSG-P4-002

  Scenario: AC5 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S6 T2
    Then one decision record is declared per outcome with the case and lot references, the buyer reference, the rule ID, the package version in force, the inputs reference, the outcome, the reason and the decided-at time
    Then the bid record is declared with the lot, the buyer, the account set, the amount and the bid window, because no table of the service carries it (GAP-2985; ASM-4914)
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation, the element or the signal it serves
    Then the rwb-partner fake answers organisation "PTR-2026-000031" with the NDA signed, KYC passed, a licence in date and an active panel, and the four failure variants with no answer beyond 2 s
    Then the rwb-case fake answers the states DATA_ROOM_OPEN, BUYER_PENDING_KYC, BIDDING_OPEN and BUYER_CLEARED of "RC-2026-000842", the four moves accepted and a move refused
    Then the rwb-decision fake answers the package at its version with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26, the decision-record stub answers a healthy and a stopped chain, and the gateway-bff fake answers the merged screen answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1 with its retry and .dlt topics, the queue is rwb-debtsale in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry, rule_row and the partner tables are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step and no consumed event, and it names LotAwarded (EV-23) as RWB-S6-E6005-APP's and AccountsTransferred as RWB-S6-E6007-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule, a bid table or a v_ace_* read
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6002-APP and copy no criterion of the legacy story, whose four criteria stay with the app story word for word. The absence of a qualification operation and of a bid table is declared here as a contract fact with a gap behind it, not filled by invention (GAP-2985; ASM-4914, ASM-4917).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract declares the qualification, buyer and bid elements and their properties only; it declares no table of another owner and no operation it does not own | TSD S6 T3.1, T3.2; context pack ownership rows (both S6) |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy AC1 and AC4 |
| BR3 | The buyer's NDA, KYC, licence and panel facts stay with rwb-partner: the contract declares the read as consumed, declares no partner property and describes no partner table read | ASM-4912; FSD S6 A2.6.2 |
| BR4 | The case state and the move are consumed on the workflow boundary and not written: no `recovery_case` property and no REST case-move operation is declared | ASM-4915; TSD S6 T4 |
| BR5 | No operation of a sibling is claimed: the data room read, the bid and the award are declared as their owners' surfaces | TSD S6 T-A.1; GAP-2985; ASM-4917 |
| BR6 | No bid table is declared: the Bid element is declared and the missing table is recorded for the DB story | GAP-2985; ASM-4914 |
| BR7 | No event of this step is declared: `LotAwarded` (EV-23) and `AccountsTransferred` are later stories', and the outbox library of DP-09 is recorded as an absent H row | TSD S6 T5.3; ASM-4918 |
| BR8 | The vocabulary is closed: the four lists are published as enumerations and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-006 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; the buyer is an organisation | Template and Rules §R7.2 (s17); FSD S6 A2.3 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The rule rows of R-DS-14 to R-DS-18 and R-DS-26 and their thresholds are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; FSD S6 A2.6.3.1; ASM-4913 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The elements, the lists, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the data room, the award screen, the wave 4 harness and the owners of rwb-partner, rwb-case, rwb-decision and rwb-access accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1 and AC7 fail | In review |

The state machine the document describes is the app story's and rwb-case's: `DATA_ROOM_OPEN`, `BUYER_PENDING_KYC`, `BUYER_CLEARED`, `BUYER_REJECTED`, `BIDDING_OPEN` and `BIDS_RECEIVED` are route states of rwb-case (TSD S6 T4). This baseline fixes the vocabulary and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the correction of the plan rows this baseline consumes, including the partner row and the absent bid table |
| Consuming teams (the app story, the data room, the award screen, the wave 4 harness and the owners of rwb-partner, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Qualification element | Lot reference, buyer partner reference, buyer class, qualification state, rule ID, rule version and decided-at time, one element per bidder on a lot |
| Buyer element | The partner reference, the buyer class against `LOV-BUYER-CLASS`, the non-disclosure agreement date, the KYC status, the licence expiry and the panel status, all consumed from S9 rwb-partner |
| Bid element | The lot reference, the buyer partner reference, the account set of the lot, the amount and the bid window; no location in the two tables of the service (GAP-2985; ASM-4914) |
| Required flags | Lot reference, buyer partner reference and buyer class required; the other properties optional |
| Lists | `LOV-BUYER-CLASS` (AMC, NON_AMC), `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED), `LOV-SEGMENT` (RETAIL, SSME, CORPORATE) and `LOV-PUTBACK` (NONE, CLAIMED, ACCEPTED, REJECTED), published as enumerations and read at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Case facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and the route state, consumed on the signal of the parent `CaseWorkflow` and never written here |
| Not declared here | `recovery_case` and `timer` (P3), the partner tables (S9), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and `proceeds` (P8) |
| Consumed fields with no source | The operation name of the buyer read, the name of the package activity, the call type of the buyer read and the bid table: Not specified in the source documents (GAP-2985; ASM-4912, ASM-4913, ASM-4914) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. TSD S6 appendix T-A publishes five operations for the module — the lot create (API-S6-001), the lot read (API-S6-002), the award (API-S6-003), the data room read (API-S6-004) and the bid (API-S6-005) — and none is a qualification operation. The qualification element is declared as a property of the answers of API-S6-004, API-S6-005 and API-S6-002, whose documents are owned by RWB-S6-E5026-APP, RWB-S6-E6004-APP and RWB-S6-E5023-APP; this baseline narrows none of them and declares no operation as its own (GAP-2985; ASM-4917). The error answers it fixes are 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, one envelope and one message ID per condition.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the buyer organisation (operation name Not specified in the source documents (GAP-2985; ASM-4912)) | `/api/recovery/partner/v1` | S9 rwb-partner | The partner reference, the `nda_signed_at` date, the `kyc_status`, the `licence_expiry`, the `panel_status` and the buyer class; faked. The matrix gives rwb-debtsale no arrow to rwb-partner, and the row is declared as a one-hop read with a 2 s budget and a breaker |

The row is a contract dependency of class C that the plan's C row does not carry, and the absence is recorded (GAP-2985; ASM-4912). The case state and the package are not REST rows: the connection matrix gives this service the Temporal cell for both, so they are declared as the parent's signal and the package activity (§12.5).

#### 12.3 Events published

None. The service owns `rwb.debtsale.events.v1` and its event set carries `LotAwarded` (event `EV-23`) with `AccountsTransferred` beside it, and neither belongs to this step: `LotAwarded` is declared as RWB-S6-E6005-APP's and `AccountsTransferred` as RWB-S6-E6007-APP's. This baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the two events is the platform library object of DP-09, which this key's pattern set does not carry (ASM-4918).

#### 12.4 Events consumed

None. The matrix gives the service the `ProceedsMatched` event of rwb-payment for the settlement and transfer steps, not for the qualification: no event of the module carries an access request, a KYC answer or a bid. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one. The FSD declares no background event for the feature (FSD S6 A2.6.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` in namespace `rwb-recovery` | Declared, not built: the stage that hosts the qualification step, its signals and the stage outcome it returns to the parent |
| `qualifyBuyer` | Activity, the one qualification step | `rwb-debtsale` | The lot, the case and the buyer in; the rule ID with its package version, the qualification state, the bid record and the four moves out |
| The package activity of rwb-decision (name Not specified in the source documents (GAP-2985; ASM-4913)) | Activity on the owner's queue | `rwb-decision` | The Debt sale package at its version in force with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26 |

The four moves cross the boundary as the child's stage outcome, which the parent applies; no REST case-move operation is declared because no source publishes one (ASM-4915). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the access request, the KYC answer and the bid; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The monthly cycle of the route set is a timer of R-DS-01 and not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot reference, the segment, the buyer class and the cut-off date the element answers from; read only for this step |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot a bid is recorded against; read only for this step |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of the qualification outcome and of the bid (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated request, answer or bid and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), the partner tables (S9), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `proceeds` (P8) are not owned by this baseline and are named only as answers or rule versions. No bid table is declared (GAP-2985; ASM-4914), and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner buyer fake | Organisation `PTR-2026-000031` with the NDA signed, KYC passed, a licence in date and an active panel; the NDA absent, KYC failed, the licence expired and the panel suspended; no answer beyond 2 s | AC2, AC3, AC6 |
| rwb-case case and move fake | The four states of `RC-2026-000842`, the four moves accepted and a move refused | AC4, AC6 |
| rwb-decision rule-package fake | The Debt sale package at its version with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26 and the four closed lists | AC2, AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged answer for `LOT-2026-000042` and `RC-2026-000842` with the qualification element read once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the buyer read and the name of the package activity carry the placeholder until their owners confirm them (GAP-2985; ASM-4912, ASM-4913).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The rwb-partner buyer read on `/api/recovery/partner/v1`; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `DebtSaleWorkflow` and `qualifyBuyer` on `rwb-debtsale`, with the package activity on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no lot, no case and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the record written before anything changes. DP-13 moves the base and nothing else. DP-19 sits behind the data room and SCR-26 Award, whose screen models are the edge contract's. DP-04, DP-08 and DP-09 are not in the pattern set: the package is a consumed activity rather than an embedded kit, the right is a service-template guard rather than a declared row, and the outbox is an absent library row rather than an event of this step (ASM-4913, ASM-4918).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan carries, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, and leaves out the outbox library `RWB-PLT-TE006-CON` that the topic would need and the Drools and access rows `RWB-PLT-E1072-CON`, `RWB-P7-E1073-CON`, `RWB-PLT-E1037-CON` and `RWB-P4-E1037-CON` that a kit and a guard would add. The partner row is a C dependency in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the fragment: the qualification element and the three answer shapes it is embedded in, with the error envelope and no provided operation (AC1).
2. Write the buyer and bid elements, their required flags and the four lists of AC2, with the placeholder where a type or a home is unstated (AC2).
3. Record the rwb-partner buyer row of AC3 with its owner, its budget, its call type and its placeholder.
4. Record the case signal and move contract, the package activity and the rights of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-debtsale-qualification.yaml`, the three elements with their account set, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The fragment validates in the pipeline, the nine contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the data room, the award screen and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | The contract carries the message of the key; it names an open deviation on an account, which is the eligibility story's, and no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the partner identity lacks the Debt sale or the Partner portal right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The case data product is stale after a late or failed ACE batch (VR-S6-006-1); the check is the owner's and this service holds no ACE batch-status read | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-26 Award and PRT-05 Data room in their loading, pending-KYC, cleared and rejected states through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and the qualification element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this baseline fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Open; closed; awarded; transferred", which belong to the award, settlement and transfer stories and are read from the same route; the qualification states are those of §9. The refusal, not-recorded and stale-data states read the messages of §14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-002-01 | AC1, AC3 | Contract | The fragment validates; the qualification element and the partner row are declared and no operation is claimed |
| TC-E6-002-02 | AC2, AC4 | Contract | The buyer and bid elements validate with the required flags and the four closed lists; the case signal, the move and the rights are declared |
| TC-E6-002-03 | AC2, AC6 | Contract | The five fakes match the document; a drifted fake fails the build |
| TC-E6-002-04 | AC5, AC7 | Contract | The decision-record element matches the library schema; the naming baseline and the absence tests pass |
| TC-E6-002-05 | AC4 | Contract | A role and a partner identity without the right; the declared 403 with MSG-P4-002 |
| TC-E6-002-06 | AC5, AC7 | Contract | A forced record failure is described as MSG-P7-003; no event, no bid table and no `v_ace_*` read is declared |
| TC-S6-E6002-CON-01 | AC1 | Contract | The fragment validates and declares no provided operation; the element and the error set are present |
| TC-S6-E6002-CON-02 | AC2 | Contract | The three elements validate with their properties, required flags and the four enumerations |
| TC-S6-E6002-CON-03 | AC3, AC4 | Contract | The consumed rows and their placeholders; the no-partner-property, no-case-property and no-rule-row boundary |
| TC-S6-E6002-CON-04 | AC5, AC6 | Contract | The decision element against the library schema; the five fakes and the drift test |
| TC-S6-E6002-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of an event, a Schedule and a bid table |

The six legacy cases are those of RWB-E6-002 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6002-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S6-E6002-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story.

### 17. Guardrails

- No business value in the contract: the NDA condition, the KYC, licence and panel values, the three-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; the buyer is an organisation and every example is synthetic.
- The buyer stays with rwb-partner and the case with rwb-case: the document declares no partner or `recovery_case` property and no case row write (BR3, BR4).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No operation and no table of a sibling is claimed, and no bid table is invented (BR5, BR6).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid; the contract fixes the elements, the consumed rows and the surfaces on which the check is built (FSD S6 A2.6); the split plan carries no requirement id for this slice (GAP-2985; ASM-4912) | The qualification, buyer and bid elements and the consumed rows | TC-E6-002-01, TC-E6-002-02, TC-S6-E6002-CON-01, TC-S6-E6002-CON-02, TC-S6-E6002-CON-03 |
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met; the contract fixes the rejection surface the sibling story starts from | The qualification state and the refusal reason | TC-S6-E6002-CON-02 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E6002-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as later stories' | TC-S6-E6002-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The partner row with its budget and breaker | TC-S6-E6002-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S6-E6002-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-002, disposition Split (rework); feature FEAT-DBS-06 |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6002-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-002; FSD S6 Debt sale v3 A2.6; TSD S6 Debt sale v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DS-14 to R-DS-18 and R-DS-26 |
| Test cases | The six legacy cases as the contract half, and the five new contract cases TC-S6-E6002-CON-01 to -05 |
| Feature and screens | FEAT-DBS-06; SCR-26 Award, PRT-05 Data room |
| Rules | R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of the rules, the decision record and the case-move answer: RWB-S6-E6002-APP.
- The data room read API-S6-004: RWB-S6-E5026-APP. The bid API-S6-005: RWB-S6-E6004-APP. The award API-S6-003: RWB-S6-E6005-APP. The lot read and create: RWB-S6-E5023-APP and RWB-S6-E5024-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3) (ASM-4915).
- The buyer panel, the partner users and the KYC, licence and panel facts: rwb-partner (S9) (ASM-4912).
- The authoring, testing, approval and versioning of the Debt sale package and of the rule rows: rwb-decision (P7) (ASM-4913).
- The capability areas, the rights and the scope rows: rwb-access (P4). The documents: rwb-document (P5). The notices: rwb-comms (P6). The proceeds: rwb-payment (P8).
- The bid table R-DS-18 needs: the DB story of this service, raised here and not declared (ASM-4914).
- The gateway-bff composite route, the partner gateway and the screen field lists: RWB-PLT-N001-CON and the edge stories.
- The remediation window of R-DS-40 and the bar of R-DS-41: the sibling story of this service.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
