# RWB-S6-E6004-CON Take buyer bids - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S6-E6004-CON-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1, the /v1 segment of /api/recovery/debtsale/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the take-bids step of rwb-debtsale, split from RWB-E6-004. It fixes the bid submission operation `POST /partner/data-room/{lotId}/bids` (API-S6-005) on `/api/recovery/debtsale/v1` with its `Bid` answer (DP-13), the `Bid` and lot elements and the four closed lists of the module, the consumed rwb-partner, rwb-case, rwb-access and rwb-decision rows, the decision-record element of DP-03, the Partner portal right, the error envelope, the fakes and the absence tests. The two endpoint rows of the legacy story, the award path and the data room read, are named as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's; the bid amount, bid time and bid reference have no column in TSD S6 T3.1, and no event carries a bid or a lot closure. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6004-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the take-bids step of rwb-debtsale — the bid submission operation on the service base with its `Bid` answer, the `Bid` and lot elements with their closed lists, the consumed rwb-partner, rwb-case, rwb-access and rwb-decision rows, the decision-record element, the Partner portal right, the error envelope and the fakes**, so that **the app story, the award screen, the data room and the wave 4 harness build against one fixed, testable contract on Day 1 and a bid field, a list value, a move name or an answer shape can never drift between rwb-debtsale, rwb-partner, rwb-case, rwb-access and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy bid of RWB-E6-004 crossed four boundaries at once: a partner portal submission, a buyer's clearance, a case state and a decision log. The target splits them: rwb-partner owns the panel and the clearance, rwb-case owns the case and its route states, rwb-access owns the right, rwb-decision owns the package in force and its ledger, and rwb-debtsale owns the lot, the bid and the realized recovery. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the values of `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK`, the `Bid` element and its answer, the fact the rwb-partner contract answers, the case state and move of rwb-case, the right of rwb-access and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (context pack S6).

Four points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs five consumed contracts (GAP-2989; ASM-4928). TSD S6 T-A.1 gives API-S6-005 "first in E5" while the data room story names the bid as a later story's, and the legacy endpoint table names the award path and the data room read instead of the bid operation (GAP-2989; ASM-4930). The bid amount, bid time and bid reference have no column on `debt_sale_lot` or `debt_sale_account` (GAP-2989; ASM-4931). And R-DS-18 is declared by RWB-S6-E6002-APP and R-DS-34 by RWB-S6-E6009-APP as well, so one answer shape has two declared holders until assembly (GAP-2989; ASM-4932).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `partner` and `partner_user` are S9's, `recovery_case` and `timer` are P3's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's, `notice` is P6's, `proceeds` is P8's and the reporting read model is P9's. This document never declares another service's table or operation as its own.
- The rwb-partner clearance read, the rwb-case state and move rows, the rwb-access authorise contract and the rwb-decision package row are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2989; ASM-4928).
- The Debt sale rule package and its rows for R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (GAP-2989; ASM-4931).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the bid submission operation with its `Bid` answer, its rights, its `Idempotency-Key` and the error responses, additive within major version 1.
2. Fix the `Bid` element: the lot reference, the buyer partner reference, the bid amount, the bid time and the bid reference, with the storage split of the amount, the time and the reference into the decision record because no column carries them (GAP-2989; ASM-4931).
3. Fix the lot element the answer and the closure read: the lot properties of DF-SAL-020 to DF-SAL-030, the realized recovery element of DF-SAL-036 and the four closed lists.
4. Fix the consumed rows: the rwb-partner clearance read, the rwb-case state read and move answer, the rwb-access authorise call and the rwb-decision package read, marking the fields the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the lot row changes, with the rule ID and the package version.
6. Record the closed vocabulary of the lists, the naming baseline and the rule that no value is a constant of the code.
7. Record that the buyer is an organisation and that no person name, identity number, date of birth or contact value is a property of any element, example or fake.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a sibling operation, the absence of a `partner` or `recovery_case` property, the drift between a fake and the document, and the absence of a published and a consumed event of this step.
10. Tag the baseline and hand it to RWB-S6-E6004-APP, the award screen, the data room and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC4 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3 |
| X5 | A value outside `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a sibling's operation as provided, a `partner` or `recovery_case` property, or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC1, AC5 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC5 |
| X8 | A person field — a name, an identity number, a date of birth or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC4 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-partner, rwb-case, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6004-APP, the award screen, the data room and the wave 4 harness on Day 1, and the rwb-partner, rwb-case, rwb-access and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, nine contract tables, eight fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the take-bids step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of partner and partner_user is S9, of recovery_case is P3, of role is P4 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The bid submission operation is declared on the debt sale base with its answer and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /partner/data-room/{lotId}/bids with a Bid answer of status 201 under the base /api/recovery/debtsale/v1, owned by rwb-debtsale (API-S6-005)
    Then it declares the Partner portal capability area with right C, the scope applied and a required Idempotency-Key
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition, each taken from section 14 (GAP-2989)
    Then it records that API-S6-001 and API-S6-002 are the lot builder's, API-S6-003 is RWB-S6-E6005-APP's and API-S6-004 is RWB-S6-E5026-APP's, and that the two endpoint rows of the legacy story are those last two
    Then it declares no other operation of this step and no operation of the award, the data room or the lot builder

  Scenario: AC2 The Bid and lot elements and their closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1, T3.2 and the rule rows R-DS-18 and R-DS-34
    Then the Bid element declares the lot reference, the buyer partner reference, the bid amount, the bid time and the bid reference, and records that no column of debt_sale_lot or debt_sale_account carries the amount, the time or the reference (GAP-2989; ASM-4931)
    Then the lot element declares the properties of DF-SAL-020 to DF-SAL-030 and the realized recovery element DF-SAL-036, and the account set of DF-SAL-031 to DF-SAL-037 is referenced
    Then status is declared against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED
    Then buyer_class is declared against LOV-BUYER-CLASS with the values AMC and NON_AMC, segment against LOV-SEGMENT with the values RETAIL, SSME and CORPORATE, and put_back_status against LOV-PUTBACK with the values NONE, CLAIMED, ACCEPTED and REJECTED
    Then the lot reference and the buyer partner reference are required and the other properties are optional
    Then no property carries a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The consumed rows for the clearance, the case state and move, the right and the package are declared (new, D-RCV-60)
    Given the consumed rows and the access section of the baseline
    When they are compared with the rwb-partner, rwb-case, rwb-access and rwb-decision contracts and with TSD S6 T6.1
    Then the buyer clearance read is declared as consumed from S9 rwb-partner, with the partner reference, the clearance for the lot, the panel status and the buyer class
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the move BIDS_RECEIVED or LOT_CLOSED carrying the rule ID and its version
    Then the authorise call is declared as consumed from P4 rwb-access, with the capability areas Partner portal and Debt sale and the rights PT-BUYER C or R scoped to its own lot, RW-DEBTSALE CRUA, RW-PRODHEAD RA and RW-HEADASL RA
    Then the Debt sale package read is declared as consumed from P7 rwb-decision, with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39 named and not declared
    Then the three operation names are Not specified in the source documents (GAP-2989; ASM-4928) and each row carries the placeholder
    Then a refused caller answers 403 with MSG-P4-002, and a repeated bid with the same Idempotency-Key describes no second effect
    Then the document declares no recovery_case property, no partner property and no decision_log_entry or rule_row column as its own

  Scenario: AC4 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the lot reference, the buyer partner reference, the rule ID, the package version in force, the bid amount, the bid time, the inputs reference, the outcome, the reason, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the lot row changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the rwb-partner fake answers the organisation PTR-2026-000031 cleared for lot LOT-2026-000042 with an active panel and the class AMC, the same organisation not cleared, with a suspended panel and with the class NON_AMC, and no answer beyond 2 s
    Then the rwb-case fake answers the states BIDDING_OPEN and GL_POSTED, an accepted move and a refused move, the rwb-access fake answers the two capability areas with and without the right, and the rwb-decision fake answers the Debt sale package at its version
    Then the decision-record stub answers a healthy chain and a stopped chain, the composite route fake answers the merged award screen and the partner gateway fake answers the same bid element scoped to one lot
    Then every fake carries organisation references, codes, amounts, dates and a rule version only, with no person name, identity number, date of birth or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC5 The naming baseline and the boundary are fixed and this step publishes and consumes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and partner, partner_user, recovery_case, role, permission, document, notice, proceeds, decision_log_entry, rule_row, the reporting read model and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event for this step, and records that LotAwarded is the only published event of the module and belongs to the award story (GAP-2989; ASM-4933)
    Then it declares no Schedule: the claim window is a durable timer of the workflow and its length is a package value (GAP-2989; ASM-4936)
    Then the partner channel is recorded as reaching the same operation through the partner gateway in the DMZ, which has no row in the plan (GAP-2989; ASM-4937)

  Scenario: AC6 Each rule BR1 to BR13 of section 8 is asserted by its ID and a rule with no assertion fails the build (new, D-RCV-60)
    Given the business rules of section 8 are the rules of this baseline
    When the contract suite is run against the document
    Then each of BR1 to BR13 is asserted by its ID in the contract suite
    Then a rule of section 8 with no assertion fails the build

  Scenario: AC7 A retried or timed-out bid submission describes no second effect (new, D-RCV-60)
    Given the bid operation is declared with a required Idempotency-Key and its stored answer
    When the same bid is submitted again after a retry or after a timeout
    Then the stored answer is returned and no second effect is described
    Then a timed-out call answers 503 as declared in AC1
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6004-APP, and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot, the bid and the realized recovery are rwb-debtsale's, and the contract declares their fields, their lists and their required flags on the bid and lot elements only | Context pack S6 (tables and operations); TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the lot row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-004 AC1 and AC3 |
| BR3 | The buyer panel, the clearance and the KYC and licence evidence stay with rwb-partner: the contract declares the clearance read as consumed and declares no partner property | Context pack S6 (S9 owns the partner objects); GAP-2989 |
| BR4 | The case move is answered and not written: the contract declares the state read and the two moves, and declares no `recovery_case` property and no case row write | TSD S6 T4; GAP-2989 |
| BR5 | The bid operation is API-S6-005 with the Partner portal right C, a required `Idempotency-Key` and its stored answer; the document claims no sibling operation | TSD S6 T-A.1 and T-A.2; GAP-2989 |
| BR6 | The vocabulary is closed: `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-008 |
| BR7 | No amount, time or reference is given a column that the data model does not have: the `Bid` element declares them and the storage row names the decision record and the idempotency row as their home | TSD S6 T3.1; GAP-2989; ASM-4931 |
| BR8 | No personal data in a schema, an example or a fake: the buyer is a partner organisation and no name, identity number, date of birth or contact value is declared | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | ADR-020 |
| BR11 | The rule rows of R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39 and the reference data of the lot status, the buyer class and the windows are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2989 |
| BR12 | The step declares no published and no consumed event: `LotAwarded` is the award story's and no catalogue entry carries a bid or a lot closure | TSD S6 T5.3; GAP-2989; ASM-4933 |
| BR13 | The partner channel and the staff screens read the same bid element behind two gateways, the partner gateway in the DMZ and the gateway-bff composite route, and neither is declared by this baseline | DP-19; GAP-2989; ASM-4937 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the award screen, the data room, the wave 4 harness and the rwb-partner, rwb-case, rwb-access and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional bid field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, or an operation is added or withdrawn | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1 and AC5 fail: a sibling operation, a `partner` property, a `recovery_case` property, an event or a Schedule | In review |

The lot vocabulary the document describes is the app story's: a bid is recorded on a lot in the window, and a lot with no claim closes with its realized recovery. This baseline fixes the vocabulary of `LOV-LOT-STATUS` and the two move names and moves no lot.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the publish-first question of API-S6-005 |
| Consuming teams (the app story, the award screen, the data room, the wave 4 harness and the owners of rwb-partner, rwb-case, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the buyer is an organisation |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline. The partner gateway in the DMZ is the edge owner's and is named here only as the channel (GAP-2989; ASM-4937).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Bid element | BR7 | The lot reference, the buyer partner reference, the bid amount, the bid time and the bid reference; the amount, the time and the reference are held in the decision record and the idempotency row because TSD S6 T3.1 carries no such column (GAP-2989; ASM-4931) |
| Lot and closure elements | BR1 | The lot properties of DF-SAL-020 to DF-SAL-030, with `buyer_partner_id` (DF-SAL-025), `buyer_class` (DF-SAL-026) and `status` (DF-SAL-030) as the columns the step writes; the account set of DF-SAL-031 to DF-SAL-037 is referenced and `selling_price` (DF-SAL-036) is the realized recovery element (GAP-2989; ASM-4931) |
| Lists | BR6 | `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), published as enumerations and read as reference data at their version |
| Decision record | BR2 | DF-DEC-001 to DF-DEC-018 through the local library, written before the lot row changes (DP-03) |
| Buyer facts | BR3 | The partner reference, the clearance for the lot, the panel status and the buyer class, of S9 rwb-partner, read only through the owner's contract and never copied or joined here (GAP-2989) |
| Not declared here | BR11 | `recovery_case` and `timer` (P3), `partner`, `partner_user` and the evidence tables (S9), `role` and `permission` (P4), `document` (P5), `notice` (P6), `proceeds` (P8), the reporting read model (P9), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) |
| Consumed fields with no source | BR3, BR4 | The operation names of the rwb-partner clearance read, the rwb-case state read and move answer, and the rwb-access authorise call: Not specified in the source documents (GAP-2989; ASM-4928) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

SCR-26 has no screen in this contract baseline; its empty, loading, error and no-access states are not declared here and are for the app story RWB-S6-E6004-APP to declare (DOR-RWB-S6-E6004-CON-10). The reference data read by the four lists and the lot windows, and the parameters they come from, are Not specified in the source documents (DOR-RWB-S6-E6004-CON-20; DP-06, DP-07).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/data-room/{lotId}/bids` | `BidRequest` in, `Bid` of status 201 out (API-S6-005) | Partner portal, right C, scope applied | `Idempotency-Key` required |

The operation answers 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot, 409 for a lot outside the window, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. TSD S6 appendix T-A.1 publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C). The two endpoint rows of the legacy story are API-S6-003 and API-S6-004, which are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's; the baseline therefore declares one operation as provided and records the publish-first question of API-S6-005 rather than deciding it silently (GAP-2989; ASM-4930).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The buyer clearance read (operation name Not specified in the source documents (GAP-2989; ASM-4928)) | `/api/recovery/partner/v1` | S9 rwb-partner | The partner reference, the clearance for the lot, the panel status and the buyer class; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The route state `BIDDING_OPEN` or `GL_POSTED`, the case reference and the lot link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2989; ASM-4928)) | rwb-case (P3) | P3 rwb-case | The move `BIDS_RECEIVED` or `LOT_CLOSED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-2989; ASM-4928)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Partner portal" and "Debt sale", the right of the caller and the scope of its own lots; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2989 with ASM-4928.

#### 12.3 Events published

None. TSD S6 T5.3 declares one published event for the module, `LotAwarded`, which is the award story's, on `rwb.debtsale.events.v1` with its retry and `.dlt` topics. No catalogue entry carries a bid, a window opening or a lot closure, so this baseline declares no event of its own, no outbox row and no producer, and the absence test of AC5 fails a build that adds one (GAP-2989; ASM-4933).

#### 12.4 Events consumed

None. No event carries a bid arrival or a claim-window close, and the close is driven by a durable timer of the workflow; the one consumed event of the service in the target belongs to the settlement step. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement, the claim window and the put-back window | `rwb-debtsale` | The stage that hosts the two steps; its input, its signals and its outcome for the parent are declared, not built |
| `takeBid` | Activity, the bid step | `rwb-debtsale` | The lot, the case, the buyer organisation and the bid in; the rule ID with its package version, the bid fact, the case move and the decision record out |
| `closeLotAfterClaimWindow` | Activity, the claim-window close | `rwb-debtsale` | The lot, the case and the timer outcome in; the realized recovery, the lot status, the case move and the decision record out |

The workflow, its queue and its saga shape come from TSD S6 T4 and the service row of the context pack; the activity names are a target design choice and are fixed by no source document. Start rule: the catalog gives the start trigger, the monthly sale cycle opening or a residual arriving from disposal (R-DS-01); the start or signalWithStart form, the workflow ID form and the duplicate-start policy are Not specified in the source documents (CG-ALL-10542). No activity is registered and no Schedule is declared by this story; the settlement, transfer, proceeds and put-back steps belong to the other stories of this service.

#### 12.6 Schedules

None. The claim window is a durable timer of `DebtSaleWorkflow`, not a Temporal Schedule; TSD S6 publishes no job for the module, and the "per claim window" timer of R-DS-34 is a package value whose length is Not specified in the source documents (GAP-2989; ASM-4936). No Quartz row, no shared job table and no batch table is declared here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class and its status; the columns the bid and the close write and the element the answer carries |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot; `selling_price` is the realized recovery element (GAP-2989; ASM-4931) |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record, and the home of the bid amount, time and reference (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated bid or claim-window answer and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the sibling stories relay the service's event through; this step declares no row |

`partner` and `partner_user` (S9), `recovery_case` and `timer` (P3), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), the reporting read model (P9) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner clearance fake | The organisation `PTR-2026-000031` cleared for lot `LOT-2026-000042` with an active panel and the class `AMC`; the same organisation not cleared, with a suspended panel and with the class `NON_AMC`; no answer beyond 2 s; an unreadable answer | AC3, AC4 |
| rwb-case state and move fake | The states `BIDDING_OPEN` and `GL_POSTED` of case `RC-2026-000842`; an accepted move and a refused move for each of the two move names | AC3, AC4 |
| rwb-access authorise fake | The capability areas "Partner portal" and "Debt sale" with their rights for the TSD S6 T6.1 roles; a caller without the right | AC3, AC4 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39 | AC3, AC4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the bid and closure element once | AC1, AC4 |
| Partner gateway route fake | The same bid element read and the bid submitted for `PTR-2026-000031`, scoped to its own lot, with no internal field | AC1, AC4, AC5 |
| Malformed payload set | An empty body, an absent lot reference, a body outside the lists and a repeated `Idempotency-Key` | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner clearance read, the rwb-case move answer and the rwb-access authorise call are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2989; ASM-4928). The partner gateway fake stands in for a channel that has no story row (GAP-2989; ASM-4937).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The bid submission declared; the rwb-partner clearance read, the rwb-case state read and the case-move answer, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` is the award story's; no event carries a bid or a lot closure |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `DebtSaleWorkflow` with `takeBid` and `closeLotAfterClaimWindow` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the partner portal |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no buyer record and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, eight fakes and four new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` with the bid operation, the `Bid`, `BidRequest`, lot and close elements, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record and the lot update commit together or not at all. DP-13 moves the base and nothing else. DP-19 is behind the award screen and the data room, whose screen model is the edge contract's, and the buyer reaches the same operation behind the partner gateway, which the plan does not carry (GAP-2989; ASM-4937).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. It leaves out the five consumed rows, which are C dependencies in fact and not in the metadata row, and the DP-08 guard, which the operation uses for the right but the pattern set does not carry; neither is added to the metadata rows (GAP-2989; ASM-4928).

**Build steps**

1. Write the bid operation of AC1, its `Idempotency-Key`, its errors and the record that the two legacy endpoint rows are siblings', then validate the additive rule in the pipeline.
2. Write the `Bid` and lot elements, their required flags and the four lists of AC2, with the storage split of the amount, time and reference.
3. Record the rwb-partner and rwb-case rows of AC3 with their owners, their budget and their placeholders.
4. Record the rwb-access rights, the rwb-decision package rows and the error envelope of AC3.
5. Record the decision-record element of AC4 and validate it against the library schema.
6. Publish the eight fakes of AC4 and the drift test.
7. Record the naming baseline, the boundary, the no-event and no-Schedule record and the partner channel of AC5, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the four new contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the award screen, the data room and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the partner identity lacks the Partner portal or the Debt sale right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states and PRT-05 Data room in its admitted, bidding and closed states, all read only. The staff route is the gateway-bff composite route (DP-19), which serves SCR-25 Lot builder and SCR-26 Award and publishes only the data and commands of this service (GAP-1787); the partner route is the partner gateway in the DMZ, which fronts rwb-partner and reaches the same bid element scoped to the buyer's own lots, with the buyer identity and the lot scope asserted by the gateway (GAP-1774; GAP-2989; ASM-4937). The route calls rwb-debtsale for the lot, the bid and the closure, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this baseline fixes the bid and closure element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, out-of-window and not-recorded states the app story shows read the messages of section 14 on the same routes. The empty, loading, error and no-access states of SCR-26 are Not specified in the source documents (CG-ALL-10546).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-004-01 | AC1, AC2 | Contract | Lot `LOT-2026-000042` and buyer `PTR-2026-000031`; the contract half answers the bid operation, the `Bid` element and the lot element |
| TC-E6-004-02 | AC2, AC3 | Contract | The realised recovery element and the claim-window close answer; the contract half answers DF-SAL-036 and the `LOT_CLOSED` move shape |
| TC-E6-004-03 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-004-04 | AC3 | Contract | RW-DEBTSALE holds CRUA and PT-BUYER holds RU scoped; the contract half answers the rights of the two capability areas |
| TC-E6-004-05 | AC4, AC5 | Contract | A malformed request and an absent clearance answer; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6004-CON-01 | AC1 | Contract | The fragment validates; the bid operation, the seven error answers and the sibling-operation record are present |
| TC-S6-E6004-CON-02 | AC2 | Contract | The `Bid` and lot elements validate with their properties, their required flags and the four closed lists |
| TC-S6-E6004-CON-03 | AC3 | Contract | The four consumed rows, their placeholders and the two move names; the no-`partner` and no-`recovery_case` boundary |
| TC-S6-E6004-CON-04 | AC4, AC5 | Contract | The eight fakes and the drift test; the absence of a published or consumed event, of a second topic and of a Schedule |
| TC-S6-E6004-CON-05 | AC5 | Contract | The two tables of §12.7 are the only tables owned; a third table, a foreign key out of the schema or a second owner is refused (DP-01) |
| TC-S6-E6004-CON-06 | AC1, AC2, AC3, AC4, AC5; BR1 to BR13 | Contract | Each rule BR1 to BR13 of section 8 is asserted by name in the contract suite; a rule with no assertion fails the build |
| TC-S6-E6004-CON-07 | AC6 | Contract | Not specified in the source documents (NEWAC-RWB-S6-E6004-CON-AC6) |
| TC-S6-E6004-CON-08 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-S6-E6004-CON-AC7) |

The five legacy cases are the legacy cases of RWB-E6-004 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6004-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6004-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the windows, the reserve, the tiered terms, the panel values, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: the buyer is a partner organisation and no name, identity number, date of birth, address or contact value is declared; every example is synthetic.
- The buyer panel and the evidence stay with rwb-partner and the case with rwb-case: the document declares no partner property, no `recovery_case` property, no case row write and no ACE table read (BR3, BR4).
- The realized recovery is named on an existing column and never given an invented one: `selling_price` carries it and the reporting destination is recorded, not declared (GAP-2989).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 and API-S6-004 are named as the two legacy endpoint rows and as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, never as provided here.
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2989; ASM-4935) | No programme requirement row covers taking the bid; the nearest rows, REQ-S6-004 and REQ-S6-006, belong to the sibling keys, and the PRD (C1) allocates one for this slice | The bid operation, the `Bid` element and the four consumed rows | TC-E6-004-01, TC-S6-E6004-CON-01, TC-S6-E6004-CON-02 |
| R-DS-18 | Record the bid against the lot and the buyer (Business Rules and Routing Logic v4) | The `Bid` element and the `BIDS_RECEIVED` move shape | TC-E6-004-01, TC-S6-E6004-CON-02 |
| R-DS-34 | Close the lot and record realized recovery by lot and by buyer (Business Rules and Routing Logic v4) | The realized recovery element DF-SAL-036 and the `LOT_CLOSED` move shape | TC-E6-004-02, TC-S6-E6004-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S6-E6004-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The provided operation and the five consumed rows with their budget and breaker | TC-S6-E6004-CON-01, TC-S6-E6004-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the lot changes | TC-E6-004-03, TC-S6-E6004-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-004, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S6-E6004-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S6-E6004-CON-01 to -04 |
| Feature and screens | FEAT-DBS-08 Take buyer bids, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-18 and R-DS-34 owned with the app story; R-DS-17, R-DS-35 and R-DS-39 tabled, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the operation, the evaluation of R-DS-18 and R-DS-34, the decision record, the bid fact, the realized recovery and the two case moves: RWB-S6-E6004-APP.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP (GAP-2989).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP (GAP-2989).
- The lot create and lot read API-S6-001 and API-S6-002, and the reserve and tiered terms: the lot builder and the terms stories of this service.
- The buyer panel, the partner users, the KYC, licence and non-disclosure evidence and the panel status: rwb-partner (S9) (GAP-2989).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked (GAP-2989).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-2989).
- The authoring, testing, approval and versioning of the Debt sale package and of the rule rows of R-DS-17 to R-DS-39: rwb-decision (P7).
- The qualification of a buyer under R-DS-14 to R-DS-16, the bar under R-DS-40 and R-DS-41 and the put-back claim under R-DS-35 to R-DS-39: RWB-S6-E6002-APP, RWB-S6-E6003-APP and RWB-S6-E6009-APP.
- The sale agreement, the customer notices, the posting of the proceeds and the derecognition: rwb-document (P5), rwb-comms (P6), rwb-payment (P8) and RWB-S6-E6008-APP.
- The reporting read model of realized recovery and the removed data lake: rwb-reporting (P9) and DP-17 (GAP-2989; ASM-4933).
- The gateway-bff composite route and the screen field list of SCR-26 and PRT-05: RWB-PLT-N001-CON and the edge stories.
- The partner gateway in the DMZ and the partner sign-in: the edge stories, with no plan row (GAP-2989; ASM-4937).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
