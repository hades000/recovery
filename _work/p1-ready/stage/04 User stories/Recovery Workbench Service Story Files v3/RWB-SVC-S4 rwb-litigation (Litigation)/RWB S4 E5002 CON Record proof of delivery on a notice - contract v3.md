# RWB-S4-E5002-CON Record proof of delivery on a notice - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Contract version | Major version 1: the contract is additive within it (BR9), and /v1 is the path version |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5002-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-041 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 P1 developer readiness (RD-P1 register). Backfilled 4 mapped v9 test case IDs.
- The proof-of-delivery read of rwb-source-data is date-wide and open to rwb-comms only, so the delivery fact is declared on rwb-comms; the rwb-source-data consumed row and the pod fake are removed (five fakes, four consumed rows), and no ledger entry is appended here (RD-P1-007; findings #1, #3).
- How that fact reaches the step is Pending: GAP-3382 (Blocker, finding #2).
- Each error status carries one published `messageCode`; MSG-P1-001 takes the Standard text; the freshness read is named (RD-P1-004, RD-P1-005, RD-P1-041; findings #4, #5).

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the notice-served step of rwb-litigation, split from RWB-E5-002. It fixes the served-result vocabulary and the 7-day proof window, the three consumed facts (the WIN proof on rwb-source-data, the notice and its served result on rwb-comms, the case state and the case-stage answer on rwb-case), the rule package read of rwb-decision, the decision-record element of DP-03, the durable-timer element of `LitigationWorkflow` and the fakes. It declares no provided REST operation, because the ownership rows give this service five operations and none of them records a delivery (GAP-2744; ASM-4564); the fact is not a Kafka subscription (GAP-2745; ASM-4565); the notice period and the `v_ace_pod` element have no source specification (GAP-2746; ASM-4566). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5002-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 23 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-S4-E5002-CON-1)**, I want **the published contract baseline of the notice-served step of rwb-litigation — the served-result vocabulary and the 7-day proof window, the shape of the delivery fact taken from rwb-comms, the notice and served-result shape of rwb-comms, the case state and case-stage answer of rwb-case, the rule package read of rwb-decision, the decision-record element, the durable-timer element, the error set and the fakes**, so that **the app story, the screens and the wave 3 harness build against one fixed, testable contract on Day 1 and a served result, a proof window, a timer start or an answer shape can never drift between rwb-litigation, rwb-comms and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-002 crossed four boundaries in one process: a WIN consignment, a notice row, a case state with its timer, and a decision log row. The target splits them: the WIN proof is landed by ACE and read by rwb-comms on the rwb-source-data (P1) contract, the notice, its served result and its delivery fact are rwb-comms (P6), the case of record, its route state, the case-stage timer and the officer task are rwb-case (P3), and the rule evaluation, the decision record and the notice-period timer are rwb-litigation (S4). Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that rwb-litigation holds no `v_ace_*` grant, so DP-05 is declared as a prohibition and the delivery fact is taken from rwb-comms only (RD-P1-007).

Three points are carried as gaps and assumptions rather than decided quietly: the step has no provided operation, and no published operation for the delivery fact (GAP-3382), the case read or the case-stage answer (GAP-2744), the state-machine event `PROOF_OF_DELIVERY_RECEIVED` is not a Kafka subscription because the service publishes and consumes nothing (GAP-2745), and the notice period per product and notice type, the `v_ace_pod` element and the home of the timer have no source specification (GAP-2746, GAP-2748).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the idempotency rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `hearing` and `legal_action` are S4's, `notice` is P6's, `recovery_case`, `timer` and `task` are P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's. This document never declares another service's operation as provided.
- The consumed owner contracts are rwb-comms (the notice, read on `GET /notices/{noticeId}` of rwb-comms.yaml 5.1.0, and its delivery fact) and rwb-case (the case read and answer), each built against its fake. How the delivery fact reaches the step is Pending (GAP-3382), and no source names the operations of rwb-case, so those rows carry the placeholder (GAP-2745; ASM-4565).
- No rwb-source-data operation is a precondition: `GET /proof-of-delivery?businessDate=` (rwb-source-data.yaml 5.1.0) writes nothing and is open to the rwb-comms workload identity only, and rwb-comms matches its rows to notices (RD-P1-007 rule 7).
- The LITIGATION rule package, its rows for R-LIT-07, R-LIT-08 and R-LIT-09 and its D7 route set are governed in rwb-decision (P7); this baseline consumes them and declares none of them (GAP-2748; ASM-4568).
- The notice period of each product and notice type is a versioned reference row whose content no source gives (GAP-2746; ASM-4566).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its three consumed facts, its own durable timer and decision record, and its six error conditions.
2. Fix the served-result vocabulary — delivered, refused, returned, undeliverable — and the 7-day proof window, and record that both are values in force and not schema constants.
3. Fix the element of the delivery fact taken from rwb-comms and mark the fields the sources do not give with the placeholder. The arrival of the proof and the case-stage answer are workflow signals, one hop with a 2 s budget each; neither is a published or consumed event.
4. Fix the notice and served-result element of rwb-comms over the notice row DF-LEG-015 to DF-LEG-023, and mark the placeholder on the served-result part.
5. Fix the case read and the case-stage answer of rwb-case: the route state that gates the rules, the move, the case-stage timer, the officer task and the rule version.
6. Fix the rule package read of rwb-decision as a non-blocking consumed row with its fake, and the decision-record element of DP-03, written before anything changes; no rule row is authored in this key.
7. Fix the durable-timer element of `LitigationWorkflow` and the two clocks it holds: the proof window from dispatch and the notice period from `delivered_at`.
8. Publish the contract tables of section 12 and the five contract fakes.
9. Add the contract tests: vocabulary, proof window, shapes, placeholders, error envelope, the absence of a provided operation beyond the five owned ones, the absence of a `v_ace_*` read and of a `notice` or `recovery_case` write, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S4-E5002-APP, the screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a consumed fact or of the answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field of a consumed fact is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2, AC3 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed fact has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A value outside the served-result vocabulary appears in the document or in an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `notice` property or a `recovery_case` property | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | The same fact is replayed with the same notice reference and delivered-at time | The step answers with the stored answer and describes no second effect | None | AC6 |
| X8 | A required field of an answer is absent in an example | The example test fails the build | MSG-GEN-001 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the vocabulary, the proof window, the base, the topic and the queue are fixed |
| Valuable | Unblocks RWB-S4-E5002-APP, SCR-18 and SCR-19 and the wave 3 harness on Day 1, and the rwb-comms and rwb-case teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, five fakes and five contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the notice-served step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of hearing and legal_action is S4, of notice is P6, of recovery_case, timer and task is P3 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The served-result vocabulary and the proof window are fixed as data (new, D-RCV-60)
    Given the vocabulary section of the baseline
    When it is compared with R-LIT-07, R-LIT-08 and R-LIT-09 of the Business Rules and Routing Logic v4
    Then served_result is declared with exactly the values delivered, refused, returned and undeliverable
    Then the proof window is declared as 7 days, the timer column of R-LIT-08
    Then both are published as versioned reference values and neither is a constant of the code or an enumeration member of a schema
    Then the notice period is declared as "by product and notice type" and its content is Not specified in the source documents (GAP-2746; ASM-4566)

  Scenario: AC2 The delivery fact taken from rwb-comms is declared and the ACE boundary is fixed (new, D-RCV-60)
    Given the proof section of the baseline
    When it is compared with the delivery fact of the rwb-comms notice fake (§12.8)
    Then the proof of delivery is declared as consumed from P6 rwb-comms, with the notice reference, the served result, the delivered-at time and the recipient result
    Then the element and the transport of the delivery fact are Pending (GAP-3382; GAP-2744) and the row carries the placeholder
    Then the document declares no operation of rwb-source-data, so no call to `GET /proof-of-delivery` is generated
    Then the document declares no `v_ace_*` view, no ACE table and no grant of this service on ACE
    Then every call on the row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC3 The notice and served-result shape of rwb-comms is declared and never written here (new, D-RCV-60)
    Given the notice section of the baseline
    When it is compared with the notice row DF-LEG-015 to DF-LEG-023 and with rwb-comms as its owner
    Then the notice is declared as consumed from P6 rwb-comms, with id, case_id, document_id, notice_type, sent_date, barcode and the served result of the consignment
    Then the operation name is Not specified in the source documents (GAP-2744; ASM-4564) and the row carries the placeholder
    Then the document declares no notice property as owned and no write of a served result, a barcode or a sent date from rwb-litigation
    Then the three notice fields the legacy table leaves unnamed are not invented and the row names only the six it gives

  Scenario: AC4 The case read and the case-stage answer of rwb-case are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, timer and task
    Then the read is declared with the case route state, which must be NOTICE_DISPATCHED for the three rules
    Then the answer is declared with the case move WITH_CUSTOMER_NOTICE_PERIOD or NOTICE_UNSERVED, the case-stage timer, the officer task, the rule ID and the package version
    Then the document declares no recovery_case property, no route-state column, no timer row and no task row of its own
    Then the operation names are Not specified in the source documents (GAP-2745; ASM-4565) and both rows carry the placeholder

  Scenario: AC5 The error envelope and the rights of the consumed rows are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.2 and TSD S4 T6.1
    Then a malformed body answers 400 with `messageCode` MSG-GEN-001, a role without the Litigation right 403 with MSG-P4-002, an unknown notice or case 404 with MSG-P4-003, a case in another state 409 with MSG-P3-005, a field the fact or the answer needs 422 with MSG-GEN-001, and an owner that does not answer 503 with MSG-GEN-006, each as `application/problem+json`
    Then each condition carries one envelope and one `messageCode`, and no new message text is authored
    Then the reads declare Litigation right R and the case-stage answer declares the right the owner document gives it, with scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R

  Scenario: AC6 The decision-record element and the durable timer are declared (new, D-RCV-60)
    Given the decision and timer sections of the baseline
    When they are compared with the local decision-record library of DP-03 and with LitigationWorkflow
    Then one decision record is declared per rule outcome with the case reference, the notice reference, the rule ID, the package version in force, the inputs reference, the served result, the delivered-at time and the case move
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the notice and the case unchanged with MSG-P7-003
    Then the notice-period timer is declared as a durable timer of LitigationWorkflow started at delivered_at under R-LIT-07 and never started under R-LIT-08 and R-LIT-09, and the proof window as a durable timer of the same workflow
    Then the document declares no timer row, no Temporal Schedule and no Quartz job and no event of its own for the record

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the notice fake answers the demand notice of case "RC-2026-000602" sent on 2026-12-01 with its barcode, its delivery fact with served_result delivered and delivered_at 2026-12-07, a refused, a returned and an undeliverable result, no delivery fact inside the proof window, an unknown notice, and no answer beyond 2 s
    Then the case fake answers the state NOTICE_DISPATCHED, another state, and an accepted and a refused case move
    Then the rule-package fake answers the LITIGATION package with R-LIT-07, R-LIT-08 and R-LIT-09 and a second version
    Then the decision-record library stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-18 and SCR-19 model
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline, the absence of a provided operation and the no-v_ace_ boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares zero provided operations and names the five operations of the service as the sibling stories' (API-S4-001 to API-S4-005), and a sixth operation fails the review
    Then the tables named as this service's are legal_action and hearing, which this step writes none of, and notice, recovery_case, timer, task, rule_row, decision_log_entry and document are named as other owners' and consumed only through their contracts
    Then the document declares no read of a v_ace_* view, no grant on another rwb_* schema, no event published, no event consumed and no Schedule, and the absence test fails a build that adds one
    Then the document declares no operation of rwb-source-data as consumed and no append of an interaction entry (delivery entries are appended by rwb-comms), and the absence test fails a build that adds one

  Scenario: AC9 Each business rule BR1 to BR11 of section 8 is covered by a criterion, a test case or a boundary test (new, D-RCV-60)
    Given the business rules table of section 8 and the criteria and test cases of this story
    When each rule is traced to the criteria and test cases that prove it
    Then BR1 to BR11 each have a covering criterion or test, with the architecture constraints proved by the boundary test of AC8
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5002-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice-served step of the litigation journey is rwb-litigation's, and the contract declares its vocabulary, its decision record, its timer and the facts it consumes and nothing else | Context pack (workflow `LitigationWorkflow`, queue `rwb-litigation`); Architecture v5 slide 41; FSD S4 A2.2.3.1 |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-002 AC1 and AC4 |
| BR3 | The notice row and its served result stay with rwb-comms: the contract declares the notice as consumed, declares no notice property as owned and describes no write of a served result | Context pack (ownership rows of S4); Architecture v5 slide 10; GAP-2744 |
| BR4 | The case move, the route state, the case-stage timer and the officer task stay with rwb-case: the contract declares the answer and declares no `recovery_case`, `timer` or `task` property | Context pack; TSD S4 T5.2; GAP-2745 |
| BR5 | No ACE view and no ACE table is read: the delivery fact is taken from rwb-comms, and the service holds no `v_ace_*` grant | DP-05; context pack (ACE data only through the owner's contract or `v_ace_*` views) |
| BR6 | The served-result vocabulary is closed and the proof window is 7 days; both are reference values with a version, not schema constants | Business Rules and Routing Logic v4 (R-LIT-07, R-LIT-08, R-LIT-09); context pack slide 7 notes; BR-S4-002 |
| BR7 | No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values and a rule version only | Template and Rules v1 §R7.2 (s17); FSD S4 A2.2 field catalogue |
| BR8 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR9 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR10 | The document lists only operations owned by rwb-litigation, and this step owns none beyond the five of TSD S4 T-A.1 | Ownership rows of S4; TSD S4 T-A.1; GAP-2744 |
| BR11 | The rule rows of R-LIT-07, R-LIT-08 and R-LIT-09, the D7 route set and the notice period values are governed in rwb-decision and in reference data and are named here, never declared here | GAP-2748; ASM-4568; GAP-2746 |

**Coverage.** BR1 by AC1 with TC-S4-E5002-CON-01 and by AC8 with TC-S4-E5002-CON-04; BR2 by AC6 with TC-E5-002-06 and TC-S4-E5002-CON-03; BR3 by AC3 with TC-E5-002-03 and TC-S4-E5002-CON-02; BR4 by AC4 with TC-E5-002-02 and TC-S4-E5002-CON-02; BR5 by AC2 with TC-S4-E5002-CON-01; BR6 by AC1 with TC-E5-002-01; BR8 and BR10 by AC8 with TC-E5-002-05 and TC-S4-E5002-CON-04; BR11 by AC6 with TC-E5-002-06. BR7 and BR9 by AC9 with TC-S4-E5002-CON-06.

### 9. State transitions

The lifecycle of this document, not of a notice:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The vocabulary, the three consumed facts, the timer, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-comms, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a served-result value or the proof window changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a provided operation beyond the five, a `v_ace_*` read, a `notice` or `recovery_case` property, an event or a Schedule | In review |

The state machine of the notice itself is the app story's: `NOTICE_DISPATCHED` to `WITH_CUSTOMER_NOTICE_PERIOD` under R-LIT-07 and to `NOTICE_UNSERVED` under R-LIT-08 and R-LIT-09, and the state is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, the screens, the wave 3 harness and the owners of rwb-comms, rwb-case, rwb-decision, rwb-access and rwb-document) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Notice element | The notice row DF-LEG-015 to DF-LEG-023 of `notice` in `rwb_comms`, read only: id, case_id, document_id, notice_type, sent_date, barcode and the three fields the legacy table does not name | DF-LEG-015 to DF-LEG-023 |
| Served result | The delivered, refused, returned and undeliverable value of the vocabulary; its field identifier in `notice` is Not specified in the source documents (GAP-2744; ASM-4564). The value PENDING of LOV-DELIVERY is refused and leaves the notice unchanged until its mapping is settled (GAP-1192) | Not specified in the source documents (DOR-RWB-S4-E5002-CON-7) |
| Delivery fact (proof of delivery) | Taken from rwb-comms, which reads the `v_ace_pod` rows on the rwb-source-data contract and matches them to the notice (RD-P1-007 rule 7). The notice reference, the served result, the delivered-at time and the recipient result; the element and the transport are Pending (GAP-3382; GAP-2744; ASM-4564) | Not specified in the source documents (DOR-RWB-S4-E5002-CON-7) |
| Case answer | The route state, the move, the case-stage timer start and expiry, the officer task, the rule ID and the package version, all P3's rows and columns | Not specified in the source documents (DOR-RWB-S4-E5002-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Timer | The durable timer of `LitigationWorkflow`: the proof window of 7 days from dispatch and the notice period from `delivered_at`; the `timer` row DF-WRK-027 to DF-WRK-036 is P3's and is not declared here | DF-WRK-027 to DF-WRK-036 (P3) |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2748) | DF-REF-001 to DF-REF-015 |
| Not written here | `legal_action` and `hearing` (S4, the sibling stories'), `recovery_case`, `timer` and `task` (P3), `document` (P5), every `v_ace_*` view (P1) | Not applicable (not declared by this story) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR9. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. The ownership rows give rwb-litigation five operations (API-S4-001 to API-S4-005, TSD S4 T-A.1) and none of them records a delivery or starts a notice period: API-S4-001 `POST /notices/{noticeId}/approve` is the dispatch approval, and API-S4-002 to API-S4-005 are the legal-action operations of the sibling stories. This baseline therefore declares no provided operation and fixes only what the step consumes, what it holds and what it answers; a sixth operation fails the review of AC8 (BR10; GAP-2744; ASM-4564).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET `/notices/{noticeId}` (rwb-comms.yaml 5.1.0) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice of the case with its `notice_type`, `sent_date`, barcode, case, `deliveryStatus` and `callbackDate`; the delivery fact of the notice, which starts the notice period at `delivered_at` (GAP-1740); the notice state on the case is written by this service only; faked. Mapping to served_result and delivered_at: Pending (GAP-3382) |
| The case read (operation name Not specified in the source documents (GAP-2745; ASM-4565)) | `/api/recovery/case/v1` | P3 rwb-case | The case route state that gates the three rules; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2745; ASM-4565)) | rwb-case (P3) | P3 rwb-case | The move, the case-stage timer, the officer task and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2748; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-07, R-LIT-08 and R-LIT-09; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four rows are contract dependencies of class C in fact that the plan's C row does not carry, and the absence is recorded as GAP-2744, GAP-2745 and GAP-2748 with their assumptions.

No operation of rwb-source-data is consumed. The read `GET /proof-of-delivery?businessDate=` writes nothing and answers only the rwb-comms workload identity, and this service appends no interaction entry: delivery entries are appended by rwb-comms on `POST /cases/{caseId}/interactions` (RD-P1-007 rule 7).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service (GAP-2745; ASM-4565).

#### 12.4 Events consumed

None. `PROOF_OF_DELIVERY_RECEIVED` is the event name of R-LIT-07 in the state machine and EV-15 of the Temporal design, not a Kafka subscription: the service publishes and consumes nothing, DP-09 is not in the pattern set of this key, and the delivery fact comes from rwb-comms. The Service Contract Catalog and the rwb-comms AsyncAPI list rwb-litigation as a consumer of `rwb.comms.NoticeDelivered.v1`: Pending, owner solution architect (GAP-3382). This baseline declares no consumer group, no subscription and no inbox of its own (GAP-2745; ASM-4565).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the proof window and the notice-period durable timer |
| `recordNoticeDelivery` | Activity, the one notice-served step | `rwb-litigation` | The notice and its delivery fact in; the rule ID with its package version, the served result, the timer fact and the case move out |

The activity name and the state names of the step are target design choices and are fixed by no source; the trigger is read as the arrival of a proof-of-delivery fact for a notice whose case is in `NOTICE_DISPATCHED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2745; ASM-4565). No activity is registered by this story. The workflow ID form and the start rule (start or signalWithStart, duplicate-start policy) are Not specified in the source documents (CG-ALL-9035). Temporal Catalog v1 gives for `LitigationWorkflow` only the trigger 'Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02)'.

#### 12.6 Schedules

None. The two clocks of the step are durable timers of `LitigationWorkflow`: the proof window of 7 days from dispatch and the notice period from `delivered_at`. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 is owned or moved here (GAP-2746; ASM-4566).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row; the step writes none of its columns |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by the step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated fact |

`notice` (P6), `recovery_case`, `timer` and `task` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | The demand notice `NTC-2026-000602` of case `RC-2026-000602` sent on 2026-12-01 with its barcode; its delivery fact with `served_result` delivered and `delivered_at` 2026-12-07; a refused, a returned and an undeliverable result; no delivery fact inside the proof window; an unknown notice; no answer beyond 2 s | AC2, AC3, AC7 |
| rwb-case fake | The state `NOTICE_DISPATCHED` and another state; an accepted move to `WITH_CUSTOMER_NOTICE_PERIOD` and to `NOTICE_UNSERVED`; a refused move | AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-07, R-LIT-08 and R-LIT-09, and a second version | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 model for case `RC-2026-000602` | AC7 |
| SCR-18 and SCR-19 screen states | Empty, loading, error and no access states of each screen: Not specified in the source documents (DOR-RWB-S4-E5002-CON-10) | AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the unnamed consumed rows, the delivery-fact element, the served-result field identifier and the notice period values are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2744, GAP-2745, GAP-2746, GAP-2748).

Reference data read: the served-result vocabulary, the 7-day proof window and the notice period values are read as versioned reference parameters through the reference-data contract; the parameter keys are Not specified in the source documents (DOR-RWB-S4-E5002-CON-20).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The notice read, the case read, the case-stage answer and the rule package read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered, 2 durable timers | `LitigationWorkflow`, `recordNoticeDelivery`, the proof window and the notice period; no Schedule |
| File | None | The WIN file is ingested by ACE and its proof rows are read by rwb-comms on the P1 contract; no file is declared here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no notice, no case and no timer. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and five fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-notice.v1.yaml` for the consumed and answered elements, the vocabulary of `served_result` and the proof window as published reference values, the timer element of `LitigationWorkflow`, the contract README rows for the consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither; the delivery fact comes from rwb-comms (GAP-2744; RD-P1-007). DP-13 fixes the base of the service and this step provides no operation on it. DP-19 is behind SCR-18 and SCR-19, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries for the app story. The four consumed contracts are C dependencies in fact and not in the metadata row, which is None (GAP-2744, GAP-2745, GAP-2748).

**Build steps**

1. Write the vocabulary and the proof window of AC1 as versioned reference values and validate them in the pipeline.
2. Write the delivery-fact element of AC2 on the rwb-comms notice contract with its placeholder, and the boundary tests against a `v_ace_*` read and a rwb-source-data call.
3. Write the notice row of AC3 with its six named fields, its placeholder and the absence test for a notice write.
4. Write the case read and the case-stage answer of AC4 with their placeholders.
5. Write the error envelope and the rights of AC5.
6. Write the decision-record and timer elements of AC6 and validate them against the library schema and the workflow contract.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline, the absence of a provided operation and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the vocabulary and the proof window are published as reference values, the five fakes answer every consumed path and the drift test is green, the absence test blocks a sixth operation, a `v_ace_*` read, a notice write and a Schedule, and the app story, the screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a fact or an answer is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the row declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | The notice or case is unknown or outside the scope (404) | This case is not in your scope. |
| MSG-P3-005 | The case is in another state (409) | This case cannot move to {state} from {current}. |
| MSG-GEN-006 | An owner does not answer (503) | {system} is not available. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-002-1 of the FSD; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The nine message IDs are contract elements. MSG-P1-001, MSG-P4-003, MSG-P3-005 and MSG-GEN-006 carry the English text of Error and Message Standard v6, the others keep the legacy and FSD wording, and no new message is added. MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises it (GAP-2744; ASM-4564). The Thai wording, the field-level text and the approver are left to the message work of DL10 (GAP-1748).

### 15. Screens and states

The contract serves SCR-18 Notice approval in its generated, approved, sent, delivered and unserved states and SCR-19 Litigation workspace in its pack state, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the step outcome, rwb-comms for the notice and its served result and rwb-case for the case and its route state; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, failure and timer-held states the app story shows read the messages of section 14 on the same route. SCR-18 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9040). SCR-19 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9041).

The stale state of SCR-18 (VR-S4-002-1) reads the DP07 stamp that the owner publishes on `GET /data-products/freshness` (rwb-source-data.yaml 5.1.0; `status` `LOADED` or `STALE`, `businessDate` nullable; RD-P1-005, RD-P1-041). This baseline declares no call to it: which component calls it for SCR-18 is Pending, owner solution architect (GAP-3380).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-002-01 | RWB-S4-E5002-CON AC1, RWB-S4-E5002-CON AC6 | Contract | The proof of notice `NTC-2026-000602` with served_result delivered; the contract half answers the vocabulary, the proof window and the decision-record element |
| TC-E5-002-02 | RWB-S4-E5002-CON AC2, RWB-S4-E5002-CON AC4 | Contract | Delivered_at 2026-12-07 and case `RC-2026-000602` in `NOTICE_DISPATCHED`; the contract half answers the proof row, the case read and the move to `WITH_CUSTOMER_NOTICE_PERIOD` |
| TC-E5-002-03 | RWB-S4-E5002-CON AC3, RWB-S4-E5002-CON AC4 | Contract | No proof inside the 7-day proof window; the contract half answers the notice row and the move to `NOTICE_UNSERVED` |
| TC-E5-002-04 | RWB-S4-E5002-CON AC5, RWB-S4-E5002-CON AC8 | Contract | A role without the Litigation right and a malformed fact; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-002-05 | RWB-S4-E5002-CON AC5, RWB-S4-E5002-CON AC8 | Contract | RW-LITOFF holds CRUA and RW-ENFORCE holds CRU; the contract half answers the rights and the absence of a sixth operation |
| TC-E5-002-06 | RWB-S4-E5002-CON AC6, RWB-S4-E5002-CON AC7 | Contract | The decision-record stub stopped and a fact that satisfies no rule; the contract half answers the MSG-P7-003 path and the fakes |
| TC-S4-E5002-CON-01 | RWB-S4-E5002-CON AC1, RWB-S4-E5002-CON AC2 | Contract | The vocabulary, the proof window, the reference versions and the proof element with its placeholder validate; no `v_ace_*` read is declared |
| TC-S4-E5002-CON-02 | RWB-S4-E5002-CON AC3, RWB-S4-E5002-CON AC4 | Contract | The notice element over DF-LEG-015 to DF-LEG-023 and the case answer validate with their placeholders and one hop with a 2 s budget |
| TC-S4-E5002-CON-03 | RWB-S4-E5002-CON AC5, RWB-S4-E5002-CON AC6 | Contract | The error envelope, the rights, the decision-record element and the two durable timers validate |
| TC-S4-E5002-CON-04 | RWB-S4-E5002-CON AC7, RWB-S4-E5002-CON AC8 | Contract | The five fakes match the document and a drifted fake fails the build; the absence test for a sixth operation, a `v_ace_*` read, a notice or `recovery_case` property, an event and a Schedule |
| TC-S4-E5002-CON-05 | RWB-S4-E5002-CON AC8 | Contract | Boundary of the §12.7 tables: only the four owned tables are declared; a write declared to `notice`, `recovery_case`, `timer`, `task`, `decision_log_entry`, `rule_row`, `document` or any `v_ace_*` view fails the build |
| TC-S4-E5002-CON-06 | RWB-S4-E5002-CON AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5002-CON-AC9) |

The six legacy cases are the legacy cases of RWB-E5-002 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5002-APP. The legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5002-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness. The changed criteria cite their mapped cases from Recovery Workbench Test Cases v9.xlsx in this table.

### 17. Guardrails

- No business value in the contract: the served-result values, the 7-day proof window, the notice period, the D7 route set and the message texts stay reference rows and rule rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values and a rule version only; every example is synthetic.
- The notice stays with rwb-comms and the case with rwb-case: the document declares no notice property as owned, no served-result write, no `recovery_case` property, no timer row and no task row (BR3, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR10).
- No provided operation beyond the five of the ownership rows: a sixth operation fails the review and the absence test (BR10).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed; the contract fixes the vocabulary, the two clocks and the consumed facts on which the notice period is started (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID (GAP-2747; ASM-4567) | The served-result vocabulary, the proof window, the three consumed facts and the case answer | TC-E5-002-01, TC-E5-002-02, TC-S4-E5002-CON-01, TC-S4-E5002-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S4-E5002-CON-02, TC-S4-E5002-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-002, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5002-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5002-CON-01 to -04 |
| Feature and screens | FEAT-LIT-02, SCR-18 Notice approval and SCR-19 Litigation workspace |
| Rules | R-LIT-07, R-LIT-08 and R-LIT-09, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2748) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal with durable timers), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the step, the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09, the decision record, the timer and the case answer: RWB-S4-E5002-APP.
- The notice row, its served result, its barcode and its `sent_date`, and the WIN dispatch: rwb-comms (P6), rwb-document (P5) and the rwb-comms slice of this legacy key (GAP-2744; ASM-4564).
- The case of record, its route states, the parent `CaseWorkflow`, the case-stage timer and the officer task: rwb-case (P3) and its slice of this legacy key (GAP-2745; ASM-4565).
- The WIN consignment, its file and the ACE ingestion, and the read of `v_ace_pod`: rwb-integration (P2) and rwb-source-data (P1), whose proof-of-delivery read rwb-comms alone calls.
- The generation, the template and the dispatch approval of the notice, and the five legal-action operations of this service: the sibling stories of S4 and API-S4-001 to API-S4-005.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of R-LIT-07, R-LIT-08 and R-LIT-09: rwb-decision (P7) (GAP-2748; ASM-4568).
- The notice period value per product and notice type: the reference-data owner of rwb-case and the business owner of S4 (GAP-2746; ASM-4566).
- The rights, roles, scope and masking data themselves, and the composite route and screen field list of SCR-18 and SCR-19: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

### Remaining delivery steps

- Close GAP-3382 before the baseline is tagged (solution architect).
- Close GAP-3380 for the SCR-18 stale state (solution architect).
- Size the story at refinement (squad).
- Epic design sign-off (solution architect).
- Consumer sign-off, contract Done and the five fakes published (rwb-litigation squad).
- Test data in DEV (QA lead).
