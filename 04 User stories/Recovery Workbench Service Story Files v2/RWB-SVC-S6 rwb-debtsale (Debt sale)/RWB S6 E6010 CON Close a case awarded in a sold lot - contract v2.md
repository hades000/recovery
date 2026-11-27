# RWB-S6-E6010-CON Close a case awarded in a sold lot - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6010-CON |
| Work type | CON (Contract) |
| Contract version | 1 (major version 1 of the rwb-debtsale contract, base `/api/recovery/debtsale/v1`) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S6-E6010-CON-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | rwb-case case read and closure answer, rwb-access authorise call and rwb-decision package read (consumed, placeholders; operation names Not specified in the source documents (GAP-3011)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (REQ-S6-007 adopted for traceability) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the case-closure step of rwb-debtsale, split from RWB-E6-010. It fixes the closure element and the shape it appears in (DP-13), the closure answer and its vocabulary of end state and lot status, the consumed rows for the rwb-case case read and closure answer, the rwb-access right and the rwb-decision package, the decision-record element of DP-03, the rights, the error envelope, the fakes and the absence tests. TSD S6 T-A publishes no closure operation, so the baseline declares no provided operation and records the single legacy endpoint row as RWB-S6-E6005-APP's award path; the case of record stays with rwb-case (P3) and the transfer, derecognition and posting stay with RWB-S6-E6007-APP and RWB-S6-E6008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6010-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of the case-closure step of rwb-debtsale — the closure element and the answer shape it appears in, the closure answer with its end state and its lot status vocabulary, the consumed rwb-case, rwb-access and rwb-decision rows, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, SCR-26 Award and the wave 4 harness build against one fixed, testable contract on Day 1 and a closure state, a list value, a case reference or an answer shape can never drift between rwb-debtsale, rwb-case, rwb-decision and rwb-access without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy closure of RWB-E6-010 crossed four boundaries at once: a case with its open actions, a rule row with its version, a decision log and a lot. The target splits them: rwb-case owns the case, its state, its tasks and its timers; rwb-decision owns the UNIVERSAL package, R-UNI-47 and its ledger; rwb-access owns the right; rwb-debtsale owns the lot, the account set and the closure decision. Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the end state `CASE_CLOSED_SOLD`, the `LOV-LOT-STATUS`, `LOV-PUTBACK`, `LOV-SEGMENT` and `LOV-BUYER-CLASS` vocabulary, the closure answer, the case state and open actions of rwb-case, the right of rwb-access and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` and Java package `th.co.scb.ace.workbench.recovery.debtsale`.

Four points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs three consumed contracts (GAP-3011; ASM-4976). TSD S6 appendix T-A publishes no case-closure operation, and the single endpoint row of the legacy story is the award path of a sibling story (GAP-3011; ASM-4977). No source publishes the operation name of the closure answer, the case read or the authorise call (GAP-3011; ASM-4981). The feature is unattended in the FSD while the legacy permission row holds Debt sale right A for three human roles and TSD S6 T6.1 gives the service identities the right R, so the baseline fixes the right per surface and not per step (GAP-3011; ASM-4979). The integration points of FEAT-DBS-14 name ALS and GL while the derecognition and the posting are rules of FEAT-DBS-12, so the baseline declares no adapter and no posting (GAP-3011; ASM-4980). The wave of the story is EP06's wave 4 while the service is created in wave 3; the conflict is recorded once for the service and the business epic and is not raised again here.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `recovery_case` and `timer` are P3's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `deviation` is S8's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The rwb-case state read and closure answer, the rwb-access authorise contract and the rwb-decision package read are published with their fakes, so each consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3011; ASM-4976).
- The UNIVERSAL package and its row R-UNI-47, and the DEBTSALE package and its row R-DS-23, are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the closure element and the answer shape it is embedded in, with the rights and the error responses, and no operation of its own (GAP-3011; ASM-4977).
2. Fix the closure element: the lot reference, the case reference, the account reference, the end state, the rule ID with its version and the decided-at time.
3. Fix the closure answer that leaves the service for rwb-case: the case reference, the end state `CASE_CLOSED_SOLD`, the rule ID with its version, the decided-at time and the instruction to stop every open action on the case.
4. Fix the consumed rows: the rwb-case case read and closure answer, the rwb-access authorise call and the rwb-decision package read, marking with the placeholder every field the sources do not give.
5. Record the decision-record element of DP-03, written before the closure answer.
6. Record the closed vocabulary: the end state, the lot status, the put-back, the segment and the buyer class, the naming baseline and the rule that no value is a constant of the code.
7. Record that the case and the account are named by reference and identifier only, and that no person field is a property of any element, example or fake.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a provided operation, the absence of a `recovery_case` property, the drift between a fake and the document, and the absence of published and consumed events of this step.
10. Tag the baseline and hand it to RWB-S6-E6010-APP, SCR-26 Award and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `CASE_CLOSED_SOLD` or one of the four lists appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, a `recovery_case` property, a `partner` property or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC6 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC6 |
| X8 | A person field — a name, an identity number, a date of birth or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC5 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-case, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the end state, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6010-APP, SCR-26 Award and the wave 4 harness on Day 1, and the rwb-case, rwb-access and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, nine contract tables, six fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the case-closure step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case and timer is P3, of role and permission is P4, of decision_log_entry and rule_row is P7 and of deviation is S8
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The closure element and its answer shape are declared with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the closure element with the lot reference, the case reference, the account reference, the end state, the rule ID with its version and the decided-at time, and it declares no operation of its own
    Then it records that the element is embedded in the answer of the lot read API-S6-002, which is the lot story's, and in the composite answer of SCR-26 Award, and that it narrows neither
    Then the answers 400, 401, 403, 404 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the answers is copied from the baseline that owns the operation and is not redefined here

  Scenario: AC2 The closure vocabulary and the lot status lists are fixed (new, D-RCV-60)
    Given the element and the answer sections of the baseline
    When they are compared with TSD S6 T3.2, T4 and the rule rows R-UNI-47 and R-DS-23
    Then the end state is declared as CASE_CLOSED_SOLD, the end state of the UNIVERSAL route set, and no other end state is declared by this step
    Then status is declared against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, put_back_status against LOV-PUTBACK with the values NONE, CLAIMED, ACCEPTED and REJECTED, segment against LOV-SEGMENT with the values RETAIL, SSME and CORPORATE and buyer_class against LOV-BUYER-CLASS with the values AMC and NON_AMC
    Then the closure answer declares the case reference, the end state, the rule ID with its version, the decided-at time and the instruction to stop every open action, and it declares no case state other than the end state
    Then the lot reference, the case reference and the end state are required and the other properties are optional
    Then no property carries a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The consumed rows for the rwb-case case read and the closure answer are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with TSD S6 T4
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the route state and the open actions of the case
    Then the closure answer is declared as consumed from P3 rwb-case, with the end state CASE_CLOSED_SOLD carrying the rule ID and its version
    Then the operation names of the case read and of the closure answer are Not specified in the source documents (GAP-3011; ASM-4981) and the rows carry the placeholder
    Then the document declares no recovery_case property, no case task and no timer property, and no write of a case row from rwb-debtsale
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-decision package, the rwb-access right and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with the rule package registry, TSD S6 T6.1 and the platform error envelope
    Then the package read is declared as consumed from P7 rwb-decision, with the UNIVERSAL package at its version in force and R-UNI-47 named, and the DEBTSALE package with R-DS-23 named
    Then the capability areas Debt sale and Case workflow with their rights are declared as consumed from P4 rwb-access, with RW-DEBTSALE CRUA, RW-PRODHEAD RA, RW-HEADASL RA, RW-CREDITAD R and the SY-* identities R as TSD S6 T6.1 gives them
    Then the authorise operation name is Not specified in the source documents (GAP-3011; ASM-4981) and the row carries the placeholder
    Then a refused caller answers 403 with MSG-P4-002, and a repeated award signal or a repeated closure answer with the same Idempotency-Key describes no second effect
    Then the document declares no decision_log_entry column and no rule_row column as its own

  Scenario: AC5 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per closed case with the case reference, the lot reference, the account reference, the rule ID, the package version in force, the inputs reference, the outcome CASE_CLOSED_SOLD and the decided-at time
    Then the record is written through the library before the closure answer leaves the service, and a failed write leaves the case open with MSG-P7-003
    Then the rwb-case fake answers the case RC-2026-000842 in LOT_AWARDED with three open actions, the same case already in CASE_CLOSED_SOLD, an account of the lot with no open case, an accepted closure and a refused closure, and no answer beyond 2 s
    Then the rwb-access fake answers the two capability areas with and without the right, the rwb-decision fake answers the UNIVERSAL package with R-UNI-47 and the DEBTSALE package with R-DS-23, and the decision-record stub answers a healthy chain and a stopped chain
    Then the composite route fake answers the merged SCR-26 Award for lot LOT-2026-000042 carrying the closure element once
    Then every fake carries references, codes, dates and a rule version only, with no person name, identity number, date of birth or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The naming baseline and the boundary are fixed and this step publishes and consumes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that TSD S6 T-A publishes no case-closure operation and that the single legacy endpoint row POST /debt-sale-lots/{lotId}/award is API-S6-003, which is RWB-S6-E6005-APP's
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, deviation, role, permission, document, notice, partner, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event for this step, and it records that LotAwarded is RWB-S6-E6005-APP's, AccountsTransferred is RWB-S6-E6007-APP's and ProceedsMatched is RWB-S6-E6011-APP's
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6010-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word.

Scenario: AC7 Each business rule BR1 to BR13 of section 8 is declared, refused or governed as that rule states (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot, the account set and the closure decision are rwb-debtsale's, and the contract declares their fields, their lists and their required flags on the closure element and the closure answer | Architecture v5 slide 41; TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the closure answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-010 AC1 and AC2 |
| BR3 | The case stays with rwb-case: the contract declares the case read and the closure answer as consumed and declares no `recovery_case` property, no case task and no timer | Ownership Map (`recovery_case`, `timer` owner P3); GAP-3011 |
| BR4 | The end state is closed: the document declares `CASE_CLOSED_SOLD` and no other case state, and the lot status vocabulary carries the transition the sibling stories make | Business Rules and Routing Logic v4 R-UNI-47 and state table; TSD S6 T4 |
| BR5 | This baseline declares no provided operation: the step runs behind the lot read API-S6-002 and the composite route, and is signalled by the award operation API-S6-003 of RWB-S6-E6005-APP | TSD S6 T-A.1; GAP-3011 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none; the surfaces of this step are a read and an answer | Architecture v5 slide 11; TSD S6 T-A.2 |
| BR7 | The vocabulary is closed: `CASE_CLOSED_SOLD` and the four lists are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-014 |
| BR8 | No personal data in a schema, an example or a fake: the account is an identifier and the case a reference, and no name, identity number, date of birth or contact value is declared | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The rule rows R-UNI-47 and R-DS-23 and the reference data of the end state, the lot status and the put-back values are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-3011 |
| BR12 | The rights are fixed per surface, not per step: the unattended closure declares no right of its own, the element read declares Debt sale R and the award operation that triggers it declares Debt sale A | TSD S6 T6.1; FSD S6 A2.14.3.3; GAP-3011; ASM-4979 |
| BR13 | The derecognition, the ledger posting and the account data transfer are not declared by this baseline; the integration points of the feature are the sibling stories' rules | FSD S6 A2.14.2; GAP-3011; ASM-4980 |

**Coverage.** BR1: AC1, AC2 (TC-S6-E6010-CON-01, -02). BR2: AC5 (TC-S6-E6010-CON-04). BR3: AC3 (TC-S6-E6010-CON-03). BR4: AC2 (TC-S6-E6010-CON-02). BR5: AC1, AC6 (TC-S6-E6010-CON-01, -04). BR6: AC4 (TC-S6-E6010-CON-03). BR7: AC2 (TC-S6-E6010-CON-02). BR8: AC2, AC5 (TC-S6-E6010-CON-02, -04). BR9: AC6 (TC-S6-E6010-CON-04). BR10: AC1 (TC-S6-E6010-CON-01). BR11: AC2, AC4 (TC-S6-E6010-CON-03). BR12: AC4 (TC-S6-E6010-CON-03). BR13: AC6 (TC-S6-E6010-CON-04).

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the answer, the lists, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-26 Award, the wave 4 harness and the rwb-case, rwb-access and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional closure reason | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC6 fail: a provided operation, a `recovery_case` property, an event or a Schedule | In review |

The closure state machine that the document describes is the app story's: a case of an awarded lot answers `CASE_CLOSED_SOLD` once, and a case already closed answers nothing. This baseline fixes the vocabulary of that answer and moves no case and no lot.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent closure operation and the unattended-step right |
| Consuming teams (the app story, SCR-26 Award, the wave 4 harness and the owners of rwb-case, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the account and the case are named by reference only |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Closure element | The lot reference, the case reference, the account reference, the end state, the rule ID with its version and the decided-at time; a read-only element embedded in the lot read answer and in the composite route, its property set and required flags settled in the baseline review | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Closure answer | The case reference, the end state `CASE_CLOSED_SOLD`, the rule ID with its version, the decided-at time and the instruction to stop every open action on the case | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Lot and account elements | The lot properties of DF-SAL-020 to DF-SAL-030, of which `id`, `lot_no`, `buyer_partner_id`, `signing_date` and `status` are read by this step, and the account set of DF-SAL-031 to DF-SAL-037, read only | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Lists | `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), published as enumerations and read as reference data at their version through the reference-data contract (DP-06, DP-07); the parameters read: Not specified in the source documents (DOR-RWB-S6-E6010-CON-20) | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| End state | `CASE_CLOSED_SOLD`, the end state of the UNIVERSAL route set ("Case closed as sold", "Debt sold or asset cleared the balance") | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the closure answer (DP-03) | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Not declared here | `recovery_case`, `timer`, `assignment` and `task` (P3), `deviation` (S8), `role` and `permission` (P4), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), `partner` (S9) and every `v_ace_*` view (P1) | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |
| Consumed fields with no source | The operation names of the case read, the closure answer and the authorise call: Not specified in the source documents (GAP-3011; ASM-4981) | Not specified in the source documents (DOR-RWB-S6-E6010-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (Debt sale C), API-S6-002 `GET /debt-sale-lots/{lotId}` (Debt sale R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (Debt sale A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a case-closure operation. The single endpoint row of the legacy story is API-S6-003, which is RWB-S6-E6005-APP's award operation and on which the closure step is signalled. This baseline therefore declares no operation as provided, records the sibling row by name, and fixes only the closure element and the closure answer. The absence is recorded as GAP-3011 with ASM-4977.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read, operation name Not specified in the source documents (GAP-3011; ASM-4981)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, the case number, the route state and the open actions of each case of the awarded lot; faked |
| The case-closure answer (operation name Not specified in the source documents (GAP-3011; ASM-4981)) | rwb-case (P3) | P3 rwb-case | The end state `CASE_CLOSED_SOLD` with the rule ID, its version and the instruction to stop every open action; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3011; ASM-4981)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Case workflow", the right of the caller and the scope; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The UNIVERSAL package at its version with R-UNI-47 and the DEBTSALE package with R-DS-23; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3011 with ASM-4976.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23, consumers rwb-case and rwb-payment) and `AccountsTransferred` (consumers rwb-case and rwb-reporting). `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's; the closure step produces neither, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC6 fails a build that adds one.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched` (event 25), which belongs to RWB-S6-E6011-APP, and the closure is signalled inside the service's own workflow by the award confirmation. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC6 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the saga of the lot with pivot = transfer and continues-as-new across the settlement and the put-back window, and the stage workflow of the case, child of `CaseWorkflow` on rwb-case (P3), that carries the eligibility and the case-side steps; the case side is moved by rwb-case on LotAwarded and AccountsTransferred, never by a write into the case schema | `rwb-debtsale` | The stage that hosts the closure step; its signals and its outcome for the parent are declared, not built |
| `closeCase` | Activity, the closure step, one execution per case of the lot | `rwb-debtsale` | The lot, the account set and the case in; the rule ID with its version, the end state, the decision record and the closure answer out |

Workflow ID of `DebtSaleWorkflow`: Not specified in the source documents (CG-ALL-10778). Start rule of `DebtSaleWorkflow` per Temporal Catalog v1: 'The monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)'; duplicate-start policy: Not specified in the source documents (CG-ALL-10778).

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice and the trigger is read as the award confirmation of the lot, because the FSD declares no background event for the feature (FSD S6 A2.14.4.4) while R-UNI-47 bounds it to the same day. No activity is registered by this story, and the saga steps of approval, agreement and notices, payment, transfer, derecognition, posting, the lot close and the customer notices belong to the sibling stories of this service.

#### 12.6 Schedules

None. The step runs from the award confirmation and its bound is a durable timer inside the workflow; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of the awarded accounts; the element the closure reads, with no column written |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot whose cases are closed; read only |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the closure (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated award signal and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the service's sibling stories relay their events through; this step declares no row |

`recovery_case`, `timer`, `assignment` and `task` (P3), `deviation` (S8), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), `partner` (S9) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | The case `RC-2026-000842` in `LOT_AWARDED` with three open actions; the same case already in `CASE_CLOSED_SOLD`; an account of the lot with no open case; no answer beyond 2 s | AC3, AC5 |
| rwb-case closure-answer fake | The closure accepted with `CASE_CLOSED_SOLD` and the closure refused because the case is already closed | AC3, AC5 |
| rwb-access authorise fake | The capability areas "Debt sale" and "Case workflow" with their rights for the TSD S6 T6.1 roles; a caller without the right | AC4, AC5 |
| rwb-decision package fake | The UNIVERSAL package at its version in force with R-UNI-47 and the DEBTSALE package with R-DS-23 | AC4, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the closure element once | AC1, AC5 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the closure answer and the authorise call are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3011; ASM-4981).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case case read and closure answer, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` is RWB-S6-E6005-APP's, `AccountsTransferred` is RWB-S6-E6007-APP's and `ProceedsMatched` is RWB-S6-E6011-APP's |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DebtSaleWorkflow` and `closeCase` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; the account data transfer of the sale is RWB-S6-E6007-APP's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no account, no case and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, six fakes and five new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the closure element and the closure answer, the `Closure` and `ClosureAnswer` elements, the vocabulary of the end state and the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record and the closure answer commit together or not at all. DP-13 moves the base of the closure element and of the award path, whose legacy base `/api/recovery/v1` the story master carries. DP-19 is behind SCR-26 Award, whose screen model is the edge contract's.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. It leaves out the four consumed rows, which are C dependencies in fact and not in the metadata row, and the DP-08 guard, which the element read uses for the right but the pattern set does not carry; neither is added to the metadata rows (GAP-3011; ASM-4976).

**Build steps**

1. Write the closure element and the answer shape of AC1, with the no-provided-operation record, and validate the additive rule in the pipeline.
2. Write the closure answer of AC2 and the vocabulary of the end state and the four lists, with the placeholder where a type is unstated.
3. Record the rwb-case rows of AC3, their placeholders and the no-`recovery_case` boundary.
4. Record the rwb-decision package, the rwb-access rights and the error envelope of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the six fakes of AC5 and the drift test.
7. Record the naming baseline and the boundary of AC6, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the five contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-26 Award and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which the eligibility check of FEAT-DBS-01 raises at lot building, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The caller lacks the Debt sale or the Case workflow right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the closure answer | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states, all read only; its empty, loading, error and no-access states are Not specified in the source documents (CG-ALL-10781). The staff route is the gateway-bff composite route (DP-19), which also calls rwb-case for the case and its state and rwb-partner for the buyer; this baseline fixes the closure element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and the not-recorded states the app story shows read the messages of section 14 on the same route. No new screen, no new field and no new user action is declared by this baseline.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-010-01 | AC1, AC2 | Contract | Lot `LOT-2026-000042` and case `RC-2026-000842`; the contract half answers the closure element, the closure answer and the end state vocabulary |
| TC-E6-010-02 | AC3, AC5 | Contract | The case in `LOT_AWARDED` with three open actions and the decision-record stub stopped; the contract half answers the closure answer, the placeholder and the MSG-P7-003 path |
| TC-E6-010-03 | AC4 | Contract | RW-DEBTSALE holds CRUA and RW-CREDITAD holds R; the contract half answers the rights of the two capability areas and the 403 path |
| TC-E6-010-04 | AC5, AC6 | Contract | A malformed request and an absent case answer; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6010-CON-01 | AC1 | Contract | The fragment validates; the closure element, the five error answers and the no-provided-operation record are present |
| TC-S6-E6010-CON-02 | AC2 | Contract | The `Closure` and `ClosureAnswer` elements validate with their properties, their required flags, the end state and the four closed lists |
| TC-S6-E6010-CON-03 | AC3, AC4 | Contract | The rwb-case and rwb-access rows, their placeholders and the no-`recovery_case` boundary; the rwb-decision package rows |
| TC-S6-E6010-CON-04 | AC5, AC6 | Contract | The six fakes and the drift test; the absence of a published or consumed event, of a second topic and of a Schedule |
| TC-S6-E6010-CON-05 | AC5 | Contract | The boundary of the five tables of section 12.7: the owned tables only, no column written to debt_sale_lot and no foreign key leaving the schema |
| TC-S6-E6010-CON-06 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-S6-E6010-CON-AC7) |

The four legacy cases are the legacy cases of RWB-E6-010 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6010-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6010-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here because this story holds no integration dependency.

### 17. Guardrails

- No business value in the contract: the end state, the four lists, the same-day timer and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: the account is an identifier and the case a reference, and no name, identity number, date of birth, address or contact value is declared; every example is synthetic.
- The case stays with rwb-case and the deviation with rwb-deviation: the document declares no `recovery_case` property, no task, no timer, no deviation property and no case row write (BR3).
- No posting and no adapter: the derecognition, the ledger, the ALS update and the file transfer are the sibling stories' rules, and the document declares no posting, no balance and no file (GAP-3011).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 is named as the surface that signals the step and as RWB-S6-E6005-APP's, never as provided here (GAP-3011).
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-007 | An account awarded in a lot stops every other open action on its case the same day; the contract fixes the element, the answer and the consumed rows on which the closure is built (Business Requirements Program v5; FSD S6 A2.14); the split plan carries no requirement id for this slice (GAP-3011; ASM-4976) | The closure element, the closure answer and the four consumed rows | TC-E6-010-01, TC-E6-010-02, TC-S6-E6010-CON-01, TC-S6-E6010-CON-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S6-E6010-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-010-02, TC-S6-E6010-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the closure answer | TC-E6-010-02, TC-S6-E6010-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-010, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S6-E6010-APP; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the four new contract cases TC-S6-E6010-CON-01 to -04 |
| Feature and screens | FEAT-DBS-14 Close a case awarded in a sold lot; SCR-26 Award |
| Rules | R-UNI-47 and R-DS-23, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-UNI-47, the decision record and the closure answer: RWB-S6-E6010-APP.
- The award operation API-S6-003 and its `DecisionLogEntry` answer, the price test, the agreement and the customer notices: RWB-S6-E6005-APP and RWB-S6-E6006-APP (GAP-3011).
- The transfer of the awarded account data under R-DS-29 and the `AccountsTransferred` event: RWB-S6-E6007-APP.
- The derecognition under R-DS-30, the general ledger posting under R-DS-31 and the ALS update: RWB-S6-E6008-APP (GAP-3011; ASM-4980).
- The lot read API-S6-002 and the lot close under R-DS-34 and R-DS-39: the lot stories and the put-back story of this service.
- The buyer remittance under R-DS-25 to R-DS-27: RWB-S6-E6011-APP.
- The case of record, its state, its tasks, its timers and its open stage children: rwb-case (P3), whose read and closure answer this baseline declares as consumed and faked (GAP-3011).
- The deviation records and their pause of the stage clock: rwb-deviation (S8).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3011).
- The authoring, testing, approval and versioning of the UNIVERSAL and DEBTSALE packages and of R-UNI-47 and R-DS-23: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-26 Award: RWB-PLT-N001-CON and the edge stories.
- The buyer panel, the partner users and the partner channel: rwb-partner (S9).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
