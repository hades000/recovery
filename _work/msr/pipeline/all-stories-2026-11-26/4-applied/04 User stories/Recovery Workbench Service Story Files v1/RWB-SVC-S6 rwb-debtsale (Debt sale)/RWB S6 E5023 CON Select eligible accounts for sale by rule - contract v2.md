# RWB-S6-E5023-CON Select eligible accounts for sale by rule - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5023-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the eligibility step of rwb-debtsale, split from RWB-E5-023. It fixes the two lot operations on `/api/recovery/debtsale/v1` (DP-13), the `LotRequest` and `DebtSaleLot` elements with the fields DF-SAL-020 to DF-SAL-037 and the four closed lists, the consumed rows of the rwb-case case list and case-move answer, the rwb-source-data COLLINS score product and the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S6 T6.1, the fakes and the absence tests. DP-04 and DP-09 are not in the plan's pattern set although the step evaluates a package and the service owns a topic, and the four consumed rows are absent from the plan's None C row. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E5023-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the eligibility step of rwb-debtsale — the two lot operations on `/api/recovery/debtsale/v1`, the lot and account elements with their closed lists, the four consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-25 and the wave 3 harness build against one fixed, testable contract on Day 1, and a lot field, a list value, a consumed row or an answer shape can never drift between rwb-debtsale, rwb-case, rwb-source-data and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy eligibility step of RWB-E5-023 crossed four boundaries at once: the case list, the ACE score, the rule version and a screen. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the COLLINS score, rwb-decision owns the DEBTSALE package, and rwb-debtsale owns the sale population and the create and read of the lot. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the fields of DF-SAL-020 to DF-SAL-037, the values of `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK`, the case-list and case-move rows, the score row, the package row and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the score is consumed on the owner's contract only (ASM-4883).

Three points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the step consumes four rows, and DP-04 is absent from the pattern set although the DEBTSALE package is evaluated (ASM-4883, ASM-4884); the pattern set omits DP-09 while the service owns topic `EV-23` and the events that carry it (ASM-4885); and the eligibility inputs `deviation_open` and `fraud_flag` have no published field (ASM-4887).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `debt_sale_lot` and `debt_sale_account` are S6's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case case-list row and case-move answer, the rwb-source-data score row and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2974; ASM-4883).
- The outbox and inbox library of DP-09 is the platform dependency of the service's topic; the plan's H row for this key does not carry it, and this baseline keeps the row as the plan states it and declares no event of this step (ASM-4885).
- The DEBTSALE package and its rows for R-DS-01, R-DS-02 and R-DS-03 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `debt_sale_lot` and `debt_sale_account` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W3` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-debtsale for this step: the two lot operations with their request and answer elements, the filters, the rights and the error responses.
2. Fix the `LotRequest` and `DebtSaleLot` elements: the lot columns of DF-SAL-020 to DF-SAL-030 and the account columns of DF-SAL-031 to DF-SAL-037, their types, their required flags and the list each is declared against.
3. Fix the consumed rows: the case-list read and the case-move answer of rwb-case, the score read of rwb-source-data with its as-of date, and the package read of rwb-decision with its version, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the lot and account rows change.
5. Record the closed vocabulary of the four lists, the rights of the two operations, the naming baseline and the rule that no value is a constant of the code.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
8. Tag the baseline and hand it to RWB-S6-E5023-APP, SCR-25 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A value outside `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` or `LOV-PUTBACK` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event of this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S6 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S6 appendices and the published owner contracts of rwb-case, rwb-source-data and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S6-E5023-APP, SCR-25 and the wave 3 harness on Day 1, and the rwb-case, rwb-source-data and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the eligibility step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two lot operations are declared on the debtsale base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-debtsale is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /debt-sale-lots with a LotRequest body in and a DebtSaleLot answer of status 201, and GET /debt-sale-lots/{lotId} with a DebtSaleLot answer of status 200, both under the base /api/recovery/debtsale/v1 and owned by rwb-debtsale
    Then the read declares the path parameter lotId, and the create declares the Idempotency-Key header and the repeated key answering the lot it created
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition, and the read declares no Idempotency-Key
    Then no operation of the award, the data room or the bids is declared by this document

  Scenario: AC2 The lot and account elements and the four closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1 and T3.2
    Then the DebtSaleLot element declares the lot properties of DF-SAL-020 to DF-SAL-030: id, lot_no, cut_off_date, segment, reserve_price, buyer_partner_id, buyer_class, signing_date, approval_authority, payment_terms and status
    Then it declares the account properties of DF-SAL-031 to DF-SAL-037: id, lot_id, account_id, borrower_code, outstanding, selling_price and put_back_status, as a list of account elements
    Then segment is declared against LOV-SEGMENT with the values RETAIL, SSME and CORPORATE, buyer_class against LOV-BUYER-CLASS with AMC and NON_AMC, status against LOV-LOT-STATUS with BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then id, lot_no, cut_off_date, segment and status are required on the lot, and id, lot_id, account_id and outstanding are required on the account
    Then the create writes no reserve, no terms, no signing date and no approval authority, and those properties are optional and owned by RWB-S6-E5024-APP and RWB-S6-E6001-APP
    Then no property is added for a deviation flag, a fraud flag or a COLLINS score, and those facts are rule inputs and owner facts

  Scenario: AC3 The consumed rows of rwb-case and rwb-source-data are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case-list read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the segment, the account link and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move LOT_BUILT, CASE_EXCLUDED or BACK_TO_CASE_LIST carrying the rule ID and its version
    Then the COLLINS score read is declared as consumed from P1 rwb-source-data, with the score, the as-of date of the data product and the amount the account row carries
    Then the operation names of the row and of the two case rows are Not specified in the source documents (GAP-2974; ASM-4883, ASM-4888) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-decision row, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-decision as the owner of the rule rows and with TSD S6 T-A.1 and T6.1
    Then the package read is declared as consumed from P7 rwb-decision, with the DEBTSALE package, its version, its 41 rules over 29 states, the cap value and the reference data of the four lists, and its operation name is Not specified in the source documents (GAP-2974; ASM-4883, ASM-4884)
    Then the document declares no rule row, no threshold and no cap value as a property, and the cap and the deviation codes are read from the package
    Then the create declares Debt sale right C and the read declares Debt sale right R, both with the scope applied
    Then RW-DEBTSALE holds CRUA on the capability area, RW-PRODHEAD and RW-HEADASL hold RA, and every other role and every SY-* service identity of TSD S6 T6.1 holds R
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S6 T2
    Then one decision record is declared per rule outcome with the case reference, the account reference, the rule ID, the package version in force, the inputs reference with the as-of date of the score product, the cap value, the outcome, the case move and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the lot and account rows change, and a failed write leaves them unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data

  Scenario: AC6 The six fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case-list fake answers the case list of the cycle with 340 cases in LOT_CANDIDATE_SELECTED, a case that has left the list, and the three moves accepted and refused
    Then the rwb-source-data fake answers the COLLINS score of the 340 cases with as-of date "2026-11-30", a stale product with its date and no answer beyond 2 s
    Then the rwb-decision fake answers the DEBTSALE package at its version with R-DS-01, R-DS-02 and R-DS-03 and the four closed lists
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-25 answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1 with its retry and .dlt topics, the queue is rwb-debtsale in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot and debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names LotAwarded (EV-23) as RWB-S6-E6005-APP's and AccountsTransferred as RWB-S6-E6007-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-4885)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E5023-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The 54 percent cap that the legacy AC1 names is not a property of this document either: it is a rule fact of the DEBTSALE package, its measure is FEAT-DBS-16 and its row is R-DS-19, both of RWB-S6-E6005-APP (ASM-4886).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The population is rwb-debtsale's, and the contract declares the fields, the lists and the required flags on the `DebtSaleLot` element and its account list only | TSD S6 T3.1, T3.2; context pack ownership rows (both S6) |
| BR2 | The decision record is declared as an element written before the lot and account rows change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy AC1 and AC3 |
| BR3 | The COLLINS score stays with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read | DP-05 as a prohibition; FSD S6 A2.1.2; ASM-4883 |
| BR4 | The case list and the case move are consumed and not written: the contract declares the two rows and declares no `recovery_case` property and no case row write | ASM-4888; TSD S6 T4 |
| BR5 | No event of this step is declared: `LotAwarded` (EV-23) is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-4885; TSD S6 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S6 T-A.2 |
| BR7 | The vocabulary is closed: the four lists are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-001 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only, and `borrower_code` is a code | Template and Rules §R7.2 (s17); TSD S6 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The rule rows of R-DS-01 to R-DS-03, the deviation codes X1 to X7, the fraud flag rule and the cap are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; FSD S6 A2.1.3.1; ASM-4884, ASM-4886 |
| BR13 | The eligibility inputs `deviation_open` and `fraud_flag` are declared as consumed rule inputs on the owner's row, with the placeholder until an owner publishes them | FSD S6 A2.1.3.1; ASM-4887 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the elements, the lists, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-25, the wave 3 harness and the owners of rwb-case, rwb-source-data and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional lot field or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `LOT_CANDIDATE_SELECTED`, `LOT_BUILT`, `CASE_EXCLUDED` and `BACK_TO_CASE_LIST` are route states of rwb-case (TSD S6 T4), and the lot status values are those of `LOV-LOT-STATUS`. This baseline fixes the vocabulary and the enums and moves no lot and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the four consumed rows and the absent DP-04 and DP-09 rows |
| Consuming teams (the app story, SCR-25, the wave 3 harness and the owners of rwb-case, rwb-source-data, rwb-decision, rwb-access and rwb-document) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Lot element | The columns of DF-SAL-020 to DF-SAL-030: `id`, `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id`, `buyer_class`, `signing_date`, `approval_authority`, `payment_terms` and `status` |
| Account element | The columns of DF-SAL-031 to DF-SAL-037: `id`, `lot_id`, `account_id`, `borrower_code`, `outstanding`, `selling_price` and `put_back_status`, one element per account of the lot |
| Required flags | `id`, `lot_no`, `cut_off_date`, `segment` and `status` required on the lot; `id`, `lot_id`, `account_id` and `outstanding` required on the account; the other properties optional |
| Lists | `LOV-SEGMENT` (RETAIL, SSME, CORPORATE), `LOV-BUYER-CLASS` (AMC, NON_AMC), `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED) and `LOV-PUTBACK` (NONE, CLAIMED, ACCEPTED, REJECTED), published as enumerations and read as reference data at their version |
| Event data | None of this step: no event is declared (§12.3) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the rows change (DP-03) |
| Case and score facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and the COLLINS score of the P1 data product, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), and the data-room, bid and transfer tables of the later stories |
| Consumed fields with no source | The operation names of the score read, the package read and the two rwb-case rows, and the owner of `deviation_open` and `fraud_flag`: Not specified in the source documents (GAP-2974; ASM-4883, ASM-4888) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots` | LotRequest in, DebtSaleLot of status 201 out, the lot created from eligible accounts with its accounts, its segment and its cut-off date (API-S6-001) | Debt sale, right C, scope applied | `Idempotency-Key` header |
| GET | `/debt-sale-lots/{lotId}` | DebtSaleLot of status 200 out, with its accounts, its status and its reserve (API-S6-002) | Debt sale, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S6 T-A.1 and the paths are those of the target base, not the monolith form. `POST /debt-sale-lots/{lotId}/award` (API-S6-003) is RWB-S6-E6005-APP's, and `GET /partner/data-room/{lotId}` (API-S6-004) and `POST /partner/data-room/{lotId}/bids` (API-S6-005) are RWB-S6-E5026-APP's and the bidding stories'; none of the three is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case list of the cycle in `LOT_CANDIDATE_SELECTED`: case reference, case number, product group, segment, account link and the eligibility facts; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2974; ASM-4888)) | rwb-case (P3) | P3 rwb-case | The move `LOT_BUILT`, `CASE_EXCLUDED` or `BACK_TO_CASE_LIST` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the COLLINS score data product (operation name Not specified in the source documents (GAP-2974; ASM-4883)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score of each case, the amount the account row carries and the as-of date of the product; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-2974; ASM-4883)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEBTSALE package at its version, with R-DS-01, R-DS-02 and R-DS-03 among its 41 rules over 29 states, the deviation codes and the cap value; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-2974; ASM-4883).

#### 12.3 Events published

None. The service owns the topic `rwb.debtsale.events.v1` and its event set carries `LotAwarded` (event `EV-23`) with `AccountsTransferred` beside it, and neither belongs to this step, because the selection awards nothing and transfers no account. `LotAwarded` is declared as RWB-S6-E6005-APP's and `AccountsTransferred` as RWB-S6-E6007-APP's, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the two events is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-4885).

#### 12.4 Events consumed

None. The service subscribes to `ProceedsMatched` of rwb-payment in the settlement and transfer steps of the saga, not in the selection: no proceeds exist before a lot is awarded. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one. The trigger of the step is the opening of the cycle and the case signal the parent forwards, because the FSD declares no background event for the feature (FSD S6 A2.1.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per sale cycle, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the eligibility step; its signals and its outcome for the parent are declared, not built |
| `selectEligibleAccounts` | Activity, the one eligibility step | `rwb-debtsale` | The case list, the cut-off date and the score in; the rule ID with its package version, the lot reference, the selected and excluded accounts, the cap value and the case moves out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, and the trigger is the opening of the cycle for a case list in `LOT_CANDIDATE_SELECTED`, because the FSD declares no background event. No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the opening of the cycle and from the case signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The monthly cycle of R-DS-01 is a timer of the route and not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of the population, its fields, its lists and its status; the table the two operations answer from |
| debt_sale_account | S6 (`rwb_debtsale`) | One row per selected account, with its balance, its price and its put-back status |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8) and the later stories' data-room, bid and transfer tables are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-list fake | The case list of the cycle with 340 cases in `LOT_CANDIDATE_SELECTED`, `RC-2026-000601` among them, with the segment, the account link and the eligibility facts; a case that has left the list | AC1, AC3, AC6 |
| rwb-source-data COLLINS data-product fake | The score of the 340 cases with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC3, AC6 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-01, R-DS-02 and R-DS-03 and the four closed lists | AC2, AC4, AC6 |
| rwb-case case-move fake | The moves `LOT_BUILT`, `CASE_EXCLUDED` and `BACK_TO_CASE_LIST` accepted, and a move refused | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-25 answer for `RC-2026-000601`, in its selection state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the score read, the package read and the two case rows carry the placeholder until their owners confirm them (GAP-2974; ASM-4883, ASM-4888).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two lot operations on `/api/recovery/debtsale/v1`; the case-list read and move answer, the score read and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DebtSaleWorkflow` and `selectEligibleAccounts` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no lot, no case, no balance and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the rows change. DP-13 moves the base and nothing else. DP-19 sits behind SCR-25, whose screen model is the edge contract's. DP-04, DP-05 and DP-09 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE score as a consumed data product and never a view, and the outbox as an absent library row rather than an event of this step (GAP-2974; ASM-4883, ASM-4884, ASM-4885).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add. The four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the `LotRequest` and `DebtSaleLot` elements, their required flags and the four lists of AC2, with the placeholder where a type is unstated.
3. Record the two rwb-case rows and the score row of AC3 with their owner, their budget and their placeholders.
4. Record the rwb-decision row, the rights and the error envelope of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-debtsale-v1.yaml`, the two elements with the account list, the vocabulary of the four lists as published enumerations, the contract README rows for the four consumed rows and their placeholders, and the six fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-25 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | The contract describes the R-DS-02 outcome of an account with an open deviation, which the app story raises while the rule runs | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Debt sale right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The COLLINS data product of the case list is stale after a late or failed ACE batch (VR-S6-001-1); the check is the owner's and this service holds no ACE batch-status read | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data (ASM-4883).

### 15. Screens and states

The contract serves SCR-25 Lot builder in its loading and selection states through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the population, its accounts and its status, rwb-case for the case and its route state and rwb-source-data for the score and its as-of date; this baseline fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Draft; priced; approved": the selection state is this step's reading of "Draft", the priced state belongs to RWB-S6-E5024-APP, the approved state to RWB-S6-E6001-APP, and PRT-05 Data room to RWB-S6-E5026-APP. The refusal, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-023-01 | AC1, AC3 | Contract | The 340-case list and the COLLINS score; the contract half answers the two operations, the case-list row and the score row |
| TC-E5-023-02 | AC2, AC3 | Contract | Case `RC-2026-000601` at `LOT_CANDIDATE_SELECTED`; the contract half answers the lot and account elements and the `LOT_BUILT` move shape |
| TC-E5-023-03 | AC5, AC7 | Contract | The decision-record stub stopped and a stale data product; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-E5-023-04 | AC4 | Contract | A role without the Debt sale right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-023-05 | AC4, AC5 | Contract | RW-DEBTSALE holds CRUA and RW-PRODHEAD holds RA; the contract half answers the rights and the decision element |
| TC-S6-E5023-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the `Idempotency-Key` and the seven error answers are present |
| TC-S6-E5023-CON-02 | AC2 | Contract | The `DebtSaleLot` element validates with its eleven lot properties, its seven account properties, the required flags and the four closed lists |
| TC-S6-E5023-CON-03 | AC3, AC4 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary |
| TC-S6-E5023-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the six fakes match the document and a drifted fake fails the build |
| TC-S6-E5023-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |

The five legacy cases are those of RWB-E5-023 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E5023-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S6-E5023-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the deviation codes X1 to X7, the fraud flag rule, the cap, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only, `borrower_code` is a code, and every example is synthetic.
- The score stays with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3, BR4).
- The money stays with rwb-payment: the document declares no posting, no proceeds and no settlement property.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-001 | Accounts eligible for sale are selected by rule against the policy cap; the contract fixes the operations, the elements and the consumed rows on which the selection is built (FSD S6 Requirements served); the split plan carries no requirement id for this slice (GAP-2974) | The `DebtSaleLot` and `LotRequest` elements and the four consumed rows | TC-E5-023-01, TC-E5-023-02, TC-S6-E5023-CON-01, TC-S6-E5023-CON-02, TC-S6-E5023-CON-03 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E5023-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as later stories' | TC-S6-E5023-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S6-E5023-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S6-E5023-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-023, disposition Split (rework); feature FEAT-DBS-01 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S6-E5023-APP; this baseline copies none of them |
| Source text | Legacy RWB-E5-023; FSD S6 Debt sale v3 A2.1; TSD S6 Debt sale v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DS-01 to R-DS-03 and R-DS-19 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S6-E5023-CON-01 to -05 |
| Feature and screens | FEAT-DBS-01, SCR-25 Lot builder |
| Rules | R-DS-01, R-DS-02 and R-DS-03, governed in rwb-decision; the cap row R-DS-19 is RWB-S6-E6005-APP's |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-DS-01 to R-DS-03, the decision record, the table rows and the case-move answer: RWB-S6-E5023-APP.
- The case of record, its route states, the case list and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-4888).
- The COLLINS score and the ACE data products: rwb-source-data (P1) (ASM-4883).
- The authoring, testing, approval and versioning of the DEBTSALE package and of the rule rows: rwb-decision (P7) (ASM-4884).
- The ownership and the field names of `deviation_open` and `fraud_flag`: no source names them (ASM-4887).
- The grouping and pricing, the reserve, the tiered terms and the buyer class: RWB-S6-E5024-APP.
- The masked data tape: RWB-S6-E5025-APP. The data room and the bids: RWB-S6-E5026-APP and the bidding stories.
- The committee approval: RWB-S6-E6001-APP. The award, the 54 percent cap test of R-DS-19 and FEAT-DBS-16 and `LotAwarded`: RWB-S6-E6005-APP. The transfer and `AccountsTransferred`: RWB-S6-E6007-APP.
- The gateway-bff composite route and the screen field list of SCR-25: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
