# RWB-S6-E5024-CON Build the lots and estimate the price - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5024-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-024 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the lot build and price step of rwb-debtsale, split from RWB-E5-024. It fixes the priced part of the two lot operations on `/api/recovery/debtsale/v1` (DP-13), the priced properties of `DebtSaleLot` and its account list, the four consumed rows of rwb-case, rwb-source-data, rwb-agent and rwb-decision, the decision-record element of DP-03, the rights of TSD S6 T6.1, the fakes and the absence tests. The operation shells belong to RWB-S6-E5023-CON and this baseline adds to them within major version 1; the estimate operation name, the minimum lot size and the model-version element have no source and carry the placeholder. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the lot build and price step of rwb-debtsale — the priced properties of the two lot operations on `/api/recovery/debtsale/v1`, the two elements with their closed lists, the four consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-25 and the wave 3 harness build against one fixed, testable contract on Day 1, and a lot field, a list value, an estimate answer or a consumed row can never drift between rwb-debtsale, rwb-case, rwb-source-data, rwb-agent and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy lot build and price step of RWB-E5-024 crossed five boundaries at once: the case facts, the ACE score, the model gateway, the rule version and a screen. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the COLLINS lot economics, rwb-agent owns the estimate and its model version, rwb-decision owns the DS package, and rwb-debtsale owns the lot, the price and the create and read of the lot. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

- **One document, one owner.** The service's OpenAPI 3.1 document `openapi/rwb-debtsale-v1.yaml` is the single artefact; RWB-S6-E5023-CON wrote its operation shells and elements, and this baseline fixes the priced part of the same document, additively within major version 1 (ASM-4898). The two baselines cannot drift, because a drift inside one document fails the same lint.
- **The naming is the platform's.** Schema and login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4; context pack).
- **The estimate is an input, not a model.** The element carries the estimate and its model version, and no property of the document holds a weight, a threshold or a formula; the estimate is rwb-agent's answer (ASM-4891).
- **Three points are recorded rather than decided quietly:** the plan's C row is None while the step consumes four rows; DP-04 and DP-09 and DP-20 are absent from the pattern set although the step reads a package, sits beside the service's topic and asks an agent (GAP-2976; ASM-4891, ASM-4893, ASM-4895); and the minimum lot size, the tiered terms and the reserve policy have no value in any source (ASM-4894).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- The operation shells and the unpriced element properties of `openapi/rwb-debtsale-v1.yaml` were baselined by RWB-S6-E5023-CON, and this baseline adds the priced properties within major version 1 without renaming or removing one (ASM-4898).
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `debt_sale_lot` and `debt_sale_account` are S6's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, the estimate is P10's, `document` is P5's, `notice` is P6's and `proceeds` is P8's.
- The rwb-case case-facts row, the rwb-source-data lot-economics row, the rwb-agent estimate row and the rwb-decision package row are published with their fakes; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2976; ASM-4890).
- The outbox and inbox library of DP-09 is the platform dependency of the service's topic; the plan's H row for this key does not carry it, and this baseline declares no event of this step (ASM-4895).
- The DS package with R-DS-04 and R-DS-05 is governed in rwb-decision (P7); this baseline names the rows and declares none of them.
- The `debt_sale_lot` and `debt_sale_account` tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W3` by rule (Template and Rules §R5.7).

### 4. Flow

1. Diff the priced part of the document against the shells of RWB-S6-E5023-CON and confirm that every change is additive within major version 1.
2. Fix the priced properties of `DebtSaleLot` — `reserve_price`, `buyer_class`, `payment_terms`, `status`, and the per-account `selling_price` — with their types, their required flags and the list each is declared against.
3. Fix the consumed rows: the case facts of rwb-case, the COLLINS lot economics of rwb-source-data with its as-of date, the estimate of rwb-agent with its model version, and the package of rwb-decision with its version, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the lot and price rows change, with the rule version and the model version.
5. Record the closed vocabulary of the four lists, the rights of the two operations, the naming baseline and the rule that no value is a constant of the code and no model is shipped.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the priced properties, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read, of a `recovery_case` write, of a model property and of an event, and the drift between a fake and the document.
8. Tag the baseline and hand it to RWB-S6-E5024-APP, SCR-25 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A property is renamed or removed, or the priced property narrows an optional one to required | The additive test fails; a narrowing change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A value outside `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` or `LOV-PUTBACK` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a `v_ace_*` view, a `recovery_case` row, a model weight or another service's operation as provided | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event of this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S6 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S6 appendices, the shells of RWB-S6-E5023-CON and the published owner contracts only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S6-E5024-APP, SCR-25 and the wave 3 harness on Day 1, and the rwb-agent and rwb-source-data teams on the same day |
| Estimable | One document diff, nine contract tables, six fakes and nine contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract of the lot build and price step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of every v_ace_* view is P1, of decision_log_entry and rule_row is P7 and of the estimate is P10
    Given the operation shells of the service document were baselined by RWB-S6-E5023-CON

  Scenario: AC1 The priced part of the two lot operations is declared and the change is additive (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-debtsale is published with this change
    When it is validated against the OpenAPI 3.1 schema and diffed against the previous baseline
    Then it validates with no error
    Then the create keeps POST /debt-sale-lots with a LotRequest body in, a DebtSaleLot answer of status 201 and the Idempotency-Key header, and the read keeps GET /debt-sale-lots/{lotId} with a DebtSaleLot answer of status 200, both under /api/recovery/debtsale/v1 and owned by rwb-debtsale
    Then every change is additive within major version 1: no path, element or property is renamed or removed and no optional property becomes required
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the award, the data room or the bids is declared by this change

  Scenario: AC2 The priced properties and the four closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1 and T3.2
    Then the DebtSaleLot element declares reserve_price, buyer_class and payment_terms as optional numeric, enumerated and text properties, and status as required against LOV-LOT-STATUS
    Then the account element of the lot declares selling_price as an optional numeric property, with id, lot_id, account_id and outstanding required as the previous baseline fixed them
    Then every lot and account property of DF-SAL-020 to DF-SAL-037 is declared exactly once and no property is added beyond them
    Then segment is declared against LOV-SEGMENT with RETAIL, SSME and CORPORATE, buyer_class against LOV-BUYER-CLASS with AMC and NON_AMC, status against LOV-LOT-STATUS with BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then the create is described as producing a lot at BUILDING with its reserve, its tiered terms and its prices, and no value of an approved or awarded state is accepted
    Then no property is added for the minimum lot size, a rule threshold, the COLLINS score or a model weight

  Scenario: AC3 The four consumed rows are declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case-facts read is declared as consumed from P3 rwb-case, with the case reference, the product group, the segment, the account link and the outstanding balance
    Then the COLLINS lot-economics read is declared as consumed from P1 rwb-source-data, with the score, the lot economics and the as-of date of the data product
    Then the estimate ask is declared as consumed from P10 rwb-agent, with the lot reference, the estimate and the model version in force
    Then the package read is declared as consumed from P7 rwb-decision, with the DS package, its version, its 41 rules over 29 states and the rows of R-DS-04 and R-DS-05
    Then the operation names of the four rows are Not specified in the source documents (GAP-2976; ASM-4890, ASM-4891, ASM-4893) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The decision-record element carries the rule version and the model version (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S6 T2
    Then one record is declared per priced lot with the lot reference, the rule IDs, the package version in force, the model version of the estimate, the inputs reference with the as-of date, the minimum lot size in force, the estimate and the outcome
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the lot and price rows change, and a failed write leaves them unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data

  Scenario: AC5 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S6 T-A.1 and T6.1
    Then the create declares Debt sale right C and the read declares Debt sale right R, both with the scope applied
    Then RW-DEBTSALE holds CRUA on the capability area, RW-PRODHEAD and RW-HEADASL hold RA, and every other role and every SY-* service identity of TSD S6 T6.1 holds R
    Then a role without the right is described as refused with MSG-P4-002, and the envelope carries one message ID per condition
    Then MSG-GEN-001, MSG-P7-003 and MSG-P1-001 are bound to the invalid request, the failed record and the stale data product, and no message is reworded

  Scenario: AC6 The six fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case-facts fake answers the 340 accounts of the population in LOT_BUILT with their segment, account link and balance, and a lot that has left the population
    Then the rwb-source-data fake answers the score and the lot economics with as-of date "2026-11-30", a stale product with its date and no answer beyond 2 s
    Then the rwb-agent fake answers the lot estimate with the model version in force, and an answer without one, refused as malformed
    Then the rwb-decision fake answers the DS package at its version with R-DS-04, R-DS-05, the minimum lot size, the tiered terms and the reserve policy
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-25 answer in its priced state
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the tables and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1 with its retry and .dlt topics, the queue is rwb-debtsale in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot and debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry, rule_row and the agent estimate are named as other owners' and are consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names LotAwarded (EV-23) as RWB-S6-E6005-APP's and AccountsTransferred as RWB-S6-E6007-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule, a v_ace_* read or a model property (ASM-4895)
```

These seven criteria are new for the baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E5024-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The estimate's own model version is declared as an element of the record and of the answer, never as a model in the build (ASM-4891).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and the price are rwb-debtsale's, and the contract declares the fields, the lists and the required flags on `DebtSaleLot` and its account element only | TSD S6 T3.1, T3.2; context pack ownership rows (both S6) |
| BR2 | The decision record is declared as an element written before the lot and price rows change, carrying the rule version and the model version; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E5-024 AC1 and AC2 |
| BR3 | The COLLINS lot economics stay with rwb-source-data: the contract declares the data-product read as consumed and declares no `v_ace_*` property | DP-05 as a prohibition; FSD S6 A2.2.2; ASM-4890 |
| BR4 | The estimate is rwb-agent's: the contract declares the ask as consumed with its model version and declares no weight, threshold or formula | ASM-4891; FSD S6 A2.2.2 |
| BR5 | The case is consumed and not written: the contract declares the case-facts row and no `recovery_case` property and no case move, which is RWB-S6-E6001-APP's | ASM-4892; TSD S6 T4 |
| BR6 | No event of this step is declared: `LotAwarded` (EV-23) is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-4895; TSD S6 T5.3 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S6 T-A.2 |
| BR8 | The vocabulary is closed: the four lists are published as enumerations and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-002 |
| BR9 | The minimum lot size, the tiered terms and the reserve policy are rule rows named by the contract and never declared as properties, defaults or examples | FSD S6 A2.2.3.1; ASM-4894 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and versions only, and `borrower_code` is a code | Template and Rules §R7.2 (s17); TSD S6 T6.2 |
| BR11 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR13 | The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The priced properties, the consumed rows, the record element, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-25, the wave 3 harness and the owners of rwb-case, rwb-source-data, rwb-agent and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | An optional property, a filter or an example changes within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, an optional property becomes required, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a model weight, an event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `LOT_BUILT`, `LOT_TOO_THIN` and `LOT_PRICED` are route states of rwb-case (TSD S6 T4), the lot status values are those of `LOV-LOT-STATUS`, and this baseline fixes the vocabulary and the enums and moves no lot and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the priced part of the document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the four consumed rows and the absent DP-04, DP-09 and DP-20 rows |
| Consuming teams (the app story, SCR-25, the wave 3 harness and the owners of rwb-case, rwb-source-data, rwb-agent, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Priced lot properties | `reserve_price` (DF-SAL-024), `buyer_class` (DF-SAL-026, against `LOV-BUYER-CLASS`), `payment_terms` (DF-SAL-029) and `status` (DF-SAL-030, required, against `LOV-LOT-STATUS`) |
| Priced account property | `selling_price` (DF-SAL-036); `outstanding` (DF-SAL-035) stays required and read-only |
| Optionality rule | The priced properties are optional on the element and required in the priced answer that RWB-S6-E5024-APP produces; the create accepts them only as the estimate's output, never as a caller's choice |
| Lists | `LOV-SEGMENT` (RETAIL, SSME, CORPORATE), `LOV-BUYER-CLASS` (AMC, NON_AMC), `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED) and `LOV-PUTBACK` (NONE, CLAIMED, ACCEPTED, REJECTED), published as enumerations and read as reference data at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, with the rule version and the model version, written before the rows change (DP-03) |
| Estimate element | The lot reference, the estimate, the reserves and the tiered terms, and the model version in force; the element shape is this baseline's and its operation name is Not specified in the source documents (GAP-2976; ASM-4891) |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), the agent's model, and the data-room, bid and transfer tables of the later stories |
| Consumed fields with no source | The operation names of the four consumed rows, the field list of the COLLINS lot economics, and the value of the minimum lot size: Not specified in the source documents (GAP-2976; ASM-4890, ASM-4891, ASM-4894) |

The field-level types and lengths of the priced properties follow TSD S6 T3.1 and are settled in the baseline review. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). The operation shells were baselined by RWB-S6-E5023-CON; this baseline declares the priced part of the same document, additively (ASM-4898).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots` | LotRequest in, DebtSaleLot of status 201 out; this change declares the priced part of the answer: `reserve_price`, `buyer_class`, `payment_terms`, the `status` at `BUILDING` and the per-account `selling_price` (API-S6-001) | Debt sale, right C, scope applied | `Idempotency-Key` header |
| GET | `/debt-sale-lots/{lotId}` | DebtSaleLot of status 200 out with its accounts, its prices, its reserve, its terms and its status (API-S6-002) | Debt sale, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S6 T-A.1 and the paths are those of the target base. `POST /debt-sale-lots/{lotId}/award` (API-S6-003) is RWB-S6-E6005-APP's, and `GET /partner/data-room/{lotId}` (API-S6-004) and `POST /partner/data-room/{lotId}/bids` (API-S6-005) are RWB-S6-E5026-APP's and the bidding stories'; none of the three is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case-facts read (operation name Not specified in the source documents (GAP-2976; ASM-4890)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, product group, segment, account link and outstanding balance of the lot accounts; faked |
| The COLLINS lot-economics read (operation name Not specified in the source documents (GAP-2976; ASM-4890)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score, the lot economics and the as-of date of the data product; faked |
| The price-estimate ask (operation name Not specified in the source documents (GAP-2976; ASM-4891)) | `/api/recovery/agent/v1` | P10 rwb-agent | The estimate of the lot, the reserve and the tiered terms, with the model version in force; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-2976; ASM-4893)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DS package at its version, with R-DS-04 and R-DS-05 among its 41 rules over 29 states, the minimum lot size, the tiered terms and the reserve policy; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-2976; ASM-4890, ASM-4891, ASM-4893).

#### 12.3 Events published

None. The service owns the topic `rwb.debtsale.events.v1`, whose event set carries `LotAwarded` (event `EV-23`) with `AccountsTransferred` beside it, and neither belongs to this step: pricing a lot awards nothing and transfers no account. The baseline declares `LotAwarded` as RWB-S6-E6005-APP's and `AccountsTransferred` as RWB-S6-E6007-APP's, so it declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the two events is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-4895).

#### 12.4 Events consumed

None. The service subscribes to `ProceedsMatched` of rwb-payment in the settlement and transfer steps of the saga, not in the build and price: no proceeds exist before a lot is awarded. This baseline therefore declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one. The trigger of the step is the completed ACE batch, the event or the timer of the cycle, because the FSD declares no background event for the feature (FSD S6 A2.2.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per sale cycle, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the build and price step; its signals, its input and its priced outcome are declared, not built |
| `buildLotsAndEstimatePrice` | Activity, the one grouping and pricing step | `rwb-debtsale` | The population, the COLLINS product, the estimate and the package in; the priced lots, the rule IDs with their versions, the model version, the priced fact and the record out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, and no activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the cycle's build trigger and from the stage signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row and no batch table. The 5 working days of R-DS-04 is the committee timer of RWB-S6-E6001-APP and not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot with its segment, reserve, terms, buyer class and status; the table the two operations answer from |
| debt_sale_account | S6 (`rwb_debtsale`) | One row per account of the lot, with its balance, its price and its put-back status |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), the agent's estimate and model (P10), `document` (P5), `notice` (P6), `proceeds` (P8) and the later stories' data-room, bid and transfer tables are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts fake | The 340 accounts of the population in `LOT_BUILT`, `RC-2026-000601` among them, with the segment, the account link and the balance; a lot that has left the population | AC1, AC3, AC6 |
| rwb-source-data COLLINS fake | The score and the lot economics with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s | AC3, AC6 |
| rwb-agent estimate fake | The lot estimate with the model version in force; an answer without one, refused as malformed | AC3, AC4, AC6 |
| rwb-decision package fake | The DS package at its version with R-DS-04, R-DS-05, the minimum lot size, the tiered terms and the reserve policy | AC2, AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-25 answer for the lot in its priced state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-2976; ASM-4890, ASM-4891, ASM-4893).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two lot operations on `/api/recovery/debtsale/v1`; the case-facts read, the COLLINS read, the estimate ask and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DebtSaleWorkflow` and `buildLotsAndEstimatePrice` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no lot, no price, no case and no rule package. What it publishes is one additive change to `openapi/rwb-debtsale-v1.yaml`, nine contract tables and six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the rows change. DP-13 moves the base and nothing else. DP-19 sits behind SCR-25, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-20 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE fact as a consumed data product and never a view, the outbox as an absent library row, and the estimate as a consumed row of rwb-agent rather than a DP-20 client row (GAP-2976; ASM-4890, ASM-4891, ASM-4893, ASM-4895).

**Dependencies the table adds and the plan does not hold.** The two H rows `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON` are the plan's. Left out are the outbox library `RWB-PLT-TE006-CON`, the Drools kit rows and the agent contract `RWB-P10-TE013-CON`; the four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Diff the priced part against the baseline of RWB-S6-E5023-CON and validate the additive rule of AC1.
2. Write the priced properties of AC2 and their required flags, against TSD S6 T3.1 and the four lists.
3. Record the four consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the decision-record element of AC4 with the rule version and the model version.
5. Record the rights and the error envelope of AC5.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline, the tables and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are the additive change to `openapi/rwb-debtsale-v1.yaml`, the priced element section with the account list, the four lists as published enumerations, the contract README rows for the four consumed rows and their placeholders, and the six fakes of 12.8.

**Done when.** The document validates in the pipeline and the diff is additive, the nine contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-25 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Debt sale right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The COLLINS data product of the population is stale after a late or failed ACE batch (VR-S6-002-1); the check is the owner's and this service holds no ACE batch-status read | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S6-001 | The contract describes the exclusion outcome that the selection raises, not this step | {account} has an open deviation and cannot be sold. |

The five IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data (ASM-4890).

### 15. Screens and states

The baseline serves SCR-25 Lot builder in its loading and priced states through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot, its accounts, the reserve, the terms and the prices, rwb-case for the case and its route state, rwb-source-data for the score and its as-of date, and rwb-agent for the estimate and its model version; this baseline fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Draft; priced; approved": the draft state belongs to RWB-S6-E5023-APP, the priced state to the app story of this key, and the approved state to RWB-S6-E6001-APP. `LOV-LOT-STATUS` has no "priced" value, so the priced state is a lot at `BUILDING` with its reserve and terms filled (ASM-4896). The refusal, not-recorded and stale-data states read the messages of section 14 on the same route, and PRT-05 Data room belongs to RWB-S6-E5026-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-024-01 | AC1, AC3 | Contract | The 340-account population, the COLLINS product and the estimate; the contract half answers the two operations, the priced properties and the four consumed rows |
| TC-E5-024-02 | AC2, AC4 | Contract | A lot with a reserve, terms and per-account prices; the contract half answers the element, the required flags and the record element |
| TC-E5-024-03 | AC5, AC7 | Contract | A role without the Debt sale right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-024-04 | AC4, AC7 | Contract | A stopped record stub and a stale product; the contract half answers MSG-P7-003 and MSG-P1-001 and the absence tests |
| TC-S6-E5024-CON-01 | AC1 | Contract | The document validates and the diff against the previous baseline is additive; the two operations, the base and the seven error answers are present |
| TC-S6-E5024-CON-02 | AC2 | Contract | `DebtSaleLot` validates with the priced properties, the account property, the required flags and the four closed lists |
| TC-S6-E5024-CON-03 | AC3 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-model-weight boundary |
| TC-S6-E5024-CON-04 | AC4, AC6 | Contract | The decision-record element matches the library schema; the six fakes match the document and a drifted fake fails the build |
| TC-S6-E5024-CON-05 | AC5, AC7 | Contract | The rights, the naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |

The four legacy cases are those of RWB-E5-024 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E5024-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five `TC-S6-E5024-CON-nn` cases are new. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the minimum lot size, the tiered terms, the reserve policy, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No model in the contract: the element carries the estimate and its model version, and no weight, threshold, prompt or formula is declared, shipped or logged (BR4).
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and versions only, `borrower_code` is a code, and every example is synthetic.
- The COLLINS fact stays with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property and no case move (BR3, BR5).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares an event of this step, a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-002 | Lots are built with an estimated price, and the reserve price is approved before the lot is offered (FSD S6 Requirements served); the split plan carries no requirement id for this slice (GAP-2976) | The priced properties of `DebtSaleLot` and its account element, and the four consumed rows | TC-E5-024-01, TC-E5-024-02, TC-S6-E5024-CON-01, TC-S6-E5024-CON-02, TC-S6-E5024-CON-03 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E5024-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as later stories' | TC-S6-E5024-CON-05 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The package row as consumed, with its version | TC-S6-E5024-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S6-E5024-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element with the rule and model versions | TC-S6-E5024-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-024, disposition Split (rework); feature FEAT-DBS-02 |
| Legacy criteria | AC1 and AC2, owned word for word by RWB-S6-E5024-APP; this baseline copies none of them |
| Source text | Legacy RWB-E5-024; FSD S6 Debt sale v3 A2.2 and Requirements served; TSD S6 Debt sale v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DS-04 and R-DS-05 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S6-E5024-CON-01 to -05 |
| Feature and screens | FEAT-DBS-02, SCR-25 Lot builder (priced state) |
| Rules | R-DS-05 applied by the app story; R-DS-04 produced by it and transitioned by RWB-S6-E6001-APP; both governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-014, ADR-015, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two operations, the grouping of R-DS-05, the estimate call, the decision record and the row writes: RWB-S6-E5024-APP.
- The operation shells and the unpriced properties of the same document, which were baselined by RWB-S6-E5023-CON; this baseline adds to them and never redefines them (ASM-4898).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose case facts this baseline declares as consumed and faked (ASM-4890).
- The COLLINS lot economics and the ACE data products: rwb-source-data (P1) (ASM-4890). The pricing model, its estimate and its model version: rwb-agent (P10) (ASM-4891).
- The authoring, testing, approval and versioning of the DS package and of the minimum lot size, the tiered terms and the reserve policy: rwb-decision (P7) (ASM-4893, ASM-4894).
- The committee approval and the case move to `LOT_WITH_COMMITTEE`, which carries R-DS-04's criterion: RWB-S6-E6001-APP.
- The masked data tape: RWB-S6-E5025-APP. The data room and the bids: RWB-S6-E5026-APP and the bidding stories.
- The award, the cap test of R-DS-19 and `LotAwarded`: RWB-S6-E6005-APP. The transfer and `AccountsTransferred`: RWB-S6-E6007-APP.
- The gateway-bff composite route and the screen field list of SCR-25: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
