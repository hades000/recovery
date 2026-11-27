# RWB-S7-E6028-CON Sell a post charge-off population - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6028-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not sized in this story; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | Three consumed rows of section 12.2: the case read, the case-move answer and the rule-package read (GAP-3050; ASM-5127, ASM-5132) |
| Contract version | v1, the `/v1` path of `/api/recovery/writeoff/v1` (the only version in the source documents) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the sale selection of rwb-writeoff, split from RWB-E6-028. It fixes two operations on `/api/recovery/writeoff/v1` (DP-13) that no source publishes — the sale selection and the sold-population read — with their placeholders, the selection and write-off elements, the `placement_type` and sale-reference placeholders, the consumed rows of the rwb-case case read and case-move answer and the rwb-decision package read, the decision-record element of DP-03, the rights and the role conflict of the debt sale officer, the fakes and the absence tests. The plan's C row is empty although the contract declares three consumed rows, `placement_type` and the sale reference have no column, field ID or list, the debt sale officer holds right R only in TSD S7 T6.1, and the hand-off to rwb-debtsale has no edge in the connection matrix (GAP-3050; ASM-5125 to ASM-5058). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6028-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 15 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the sale selection of rwb-writeoff — the sale-selection operation and the sold-population read on `/api/recovery/writeoff/v1`, the selection, write-off and population elements with their required flags, the `placement_type` and sale-reference placeholders, the three consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, rwb-debtsale, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and an element, a placeholder, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy sale of a charged-off population in RWB-E6-028 crossed four boundaries at once: the case of record, the rule version, a screen and a debt sale route, and its Endpoints table carried the same two rows every S7 story carries — the scan and the committee decision — neither of which is a sale. The target splits them: rwb-case owns the case and its route states, rwb-decision owns the WO package and the limit, rwb-writeoff owns the write-off stage, the row and the selection, and rwb-debtsale owns the lots and the buyer side. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant, no grant on `rwb_case` and none on `rwb_debtsale`, so DP-05 is declared as a prohibition.

Four points are carried as gaps and assumptions rather than decided quietly: no source publishes either operation, so both carry a placeholder path and placeholder element names (ASM-5125); `placement_type` and the sale reference have no column, no field ID and no list, and TSD S7 T3.2 publishes no list at all (ASM-5126); the hand-off to the debt sale route has no edge in the connection matrix, so it is described as the case move plus the population read and no event is declared (ASM-5127); and the FSD gives the step to the debt sale officer while TSD S7 T6.1 gives RW-DEBTSALE right R and no row to the Head of Asset Liquidity (ASM-5130).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's, `payment` is P8's and every lot and buyer table is S6's. This document never declares another service's table or operation as its own.
- The published operations of the module are the scan (API-S7-001) and the committee decision (API-S7-002) in TSD S7 T-A.1; neither is a sale, so this baseline adds two operations with placeholders and declines to extend either published one (GAP-3050; ASM-5125).
- The rwb-case case read and case-move answer and the rwb-decision package read are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3050; ASM-5127, ASM-5132).
- The WO package and its rows for R-WO-12 and R-WO-32 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. `placement_type` and the sale reference have no column in it (ASM-5126).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step: the sale-selection operation and the sold-population read, with their request and answer elements, the rights and the error responses.
2. Fix the write-off element over the columns of DF-FIN-010 to DF-FIN-020, the selection element over the `placement_type` and sale-reference placeholders, and the population row element over the same write-off fields.
3. Fix the consumed rows: the case read of rwb-case, the case-move answer of rwb-case and the package read of rwb-decision with its version, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the row changes.
5. Record the rights of the two operations, the naming baseline, the role conflict of the debt sale officer and the rule that no value is a constant of the code; record that the service publishes no list of values because TSD S7 T3.2 is empty.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the paging of the population read, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` or `rwb_debtsale` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
8. Tag the baseline and hand it to RWB-S7-E6028-APP, to rwb-debtsale for the population read, to SCR-27 and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | `placement_type` or the sale reference is declared as an enumeration taken from no source | The vocabulary test fails the build: TSD S7 T3.2 publishes no list, and no source gives the value set | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a rule row or a lot | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operations are not the ones TSD S7 T6.1 gives the capability area, or the role conflict is decided quietly | The access test fails the build and the review fails the baseline | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The two paths, the element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the base, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6028-APP, rwb-debtsale's population read, SCR-27 and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, five fakes and eleven contract cases |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the sale selection of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1, of decision_log_entry and rule_row is P7 and of every lot and buyer table is S6
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations are declared with their placeholders and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-offs/{writeOffId}/sale-selection with a sale selection body in and a write-off answer of status 200, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then it declares GET /write-offs with the sale state as a filter and a paged population row out, under the same base and owner
    Then the two paths and the two element names carry the placeholder Not specified in the source documents (GAP-3050; ASM-5125) until the solution architect confirms them
    Then the selection operation declares the path parameter writeOffId, the Idempotency-Key header and the repeated key answering the selection it recorded, and the population read declares the page, the size and the scope
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the scan, of the committee decision, of the posting or of the debt sale is declared or extended by this document

  Scenario: AC2 The write-off, selection and population elements are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1 and T3.2
    Then the write-off answer element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then the selection element declares the write-off reference, the selection, the sale reference and the package version, with the selection required and placement_type declared alongside it
    Then the population row element declares the write-off reference, the case reference, the amount, the committee date, the posted date and the selection time
    Then placement_type and the sale reference carry the placeholder Not specified in the source documents (GAP-3050; ASM-5126) and declare no enumeration, because TSD S7 T3.2 lists none and no source gives the value set
    Then committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after are optional, and committee_date is named as the approval's fact of RWB-S7-E6018-APP and posted_date as RWB-S7-E6021-APP's
    Then no property is added for a lot, a reserve, an award, a buyer, an ACE extract or a rule row

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move SOLD_POST_CHARGEOFF carrying the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version, its 51 rules over 27 states, R-WO-12 and R-WO-32 and the write-off committee limit
    Then the operation names of the three rows are Not specified in the source documents (GAP-3050; ASM-5127, ASM-5132) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no rule_row property, no lot or buyer property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights, the role conflict and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T6.1 and the legacy permission table of RWB-E6-028
    Then the sale selection declares Write-off and posting right C with the scope applied, because a selection changes the population, and the sold-population read declares right R with the scope applied
    Then the baseline records that FSD S7 A2.16.3.3 gives the step to the debt sale officer and the Head of Asset Liquidity, that TSD S7 T6.1 gives RW-DEBTSALE right R and carries no Head of Asset Liquidity row, and that the confirmed right is a business decision carried as the placeholder ASM-5130
    Then RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA on the capability area, and RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA
    Then every other role and every SY-* service identity of TSD S7 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the row changes (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S7 T2
    Then one decision record is declared per rule outcome with the case and write-off references, the decision code, the rule ID R-WO-32, the package version in force, the selection, the from state, the to state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the write-off row is updated and before the case-move answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record is declared as chained to the approval record of RWB-S7-E6018-APP and as not overwriting decision_log_id
    Then the record carries no rule row, no state threshold as a literal and no personal data

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the case at PLACEMENT_DECIDED with placement_type sale, a case at another state, and a case above the write-off committee limit with no escalation
    Then the rwb-case case-move fake answers SOLD_POST_CHARGEOFF accepted and refused
    Then the rwb-decision fake answers the WO package at its version with R-WO-12, R-WO-32 and the write-off committee limit
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer before and after a selection
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry, rule_row and every lot and buyer table are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as RWB-S7-E6021-APP's, JOB-16 as RWB-S7-E6013-APP's and the sale cycle as RWB-S6-E6005-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5127)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6028-APP and copy no criterion of the legacy story, whose four criteria stay with the app story word for word. The sale is a hand-off of a charged-off population: no amount is written off, no provision is released and no lot is created here (ASM-5126, ASM-5127).

Scenario: AC8 Each business rule BR1 to BR14 of section 8 has a criterion, a test or a guardrail test that holds it (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The sale selection and the sold-population read are rwb-writeoff's, and the contract declares the fields and the required flags on the selection, write-off and population elements only | TSD S7 T3.1; context pack ownership rows (table `write_off`, operations of the service) |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC4 |
| BR3 | The case stays with rwb-case: the contract declares the case read and the case-move answer as consumed, declares no `recovery_case` property and describes no case row write | ASM-5127; TSD S7 T4 |
| BR4 | The package is rwb-decision's: the contract declares the package read with R-WO-12, R-WO-32 and the limit as consumed facts and declares no rule row and no threshold as a property set | ASM-5132 |
| BR5 | No event of this step is declared: the hand-off is the case move plus the population read, `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5127, ASM-5132; TSD S7 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET is paged, filtered and scoped | TSD S7 T-A.2 |
| BR7 | `placement_type` and the sale reference are declared with placeholders and no enumeration, because TSD S7 T3.2 publishes no list of values and no field catalog carries either | ASM-5126; FSD S7 A2.16.3.2 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates and a rule version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | Neither published operation of the module is extended: the scan is API-S7-001 and the committee decision is API-S7-002, and the sale needs two operations of its own | TSD S7 T-A.1; ASM-5125 |
| BR13 | The selection is declared at right C of the population change and the population read at right R, and the gap between that right and the roles the FSD names is recorded, not resolved in the schema | TSD S7 T6.1; FSD S7 A2.16.3.3; legacy permission table of RWB-E6-028; ASM-5130 |
| BR14 | The states `PLACEMENT_DECIDED` and `SOLD_POST_CHARGEOFF` are declared as the vocabulary of the answer and of rwb-case's machine, and move no case | ASM-5129, ASM-5131; TSD S7 T4; Business Rules and Routing Logic v4 row R-WO-32 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the elements, the placeholders, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, rwb-debtsale, SCR-27, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The paths, the element names and the role right are confirmed | The solution architect and the business lead replace the placeholders inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a sale date or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a path changes, or `placement_type` becomes an enumeration | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a lot, a second path, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `PLACEMENT_DECIDED` and `SOLD_POST_CHARGEOFF` are route states of rwb-case and WRITEOFF states of TSD S7 T4, and the entry state is filled by R-WO-29 outside this split (ASM-5129). This baseline fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed paths and element names, and the correction of the plan rows the baseline consumes, including the three consumed rows |
| Business lead | Confirms `placement_type`'s value set, the sale reference's format, the decision code set and the right and role of the debt sale officer (ASM-5126, ASM-5130) |
| Consuming teams (the app story, rwb-debtsale, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the paging convention, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that no buyer data crosses into this service's schema |
| Owner of the rwb-access authorise check | Confirms the authorise check that guards the operations of section 12.1; its operation name is Not specified in the source documents (DOR-RWB-S7-E6028-CON-6) |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Selection element | The write-off reference, the selection, `placement_type`, the sale reference and the package version, with the selection required | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7); `placement_type` appears in neither LDM v9 nor Data Classification v5 |
| Population element | The write-off reference, the case reference, the amount, the committee date, the posted date and the selection time, paged | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Required flags | The write-off reference and the selection required on the request; `id`, `case_id`, `amount` and `tax_criteria_met` required on the write-off element; the other properties optional | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Lists | None: TSD S7 T3.2 publishes no list of values, so the baseline declares no enumeration, `placement_type` keeps a placeholder value set and the sale reference keeps a placeholder format (ASM-5126) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Reference data and parameters | R-WO-12, R-WO-32, the write-off committee limit and the package version are read as reference data through the package read, under the reference-data contract of DP-06 and DP-07; the parameter names are Not specified in the source documents (DOR-RWB-S7-E6028-CON-20) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Event data | None of this step: no event is declared (§12.3) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes and chained to the approval record (DP-03) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Case and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8), every lot and buyer table (S6) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |
| Consumed fields with no source | The operation names of the case read, the case-move answer and the package read, the `placement_type` value set, the sale-reference format, the decision code set and the message ID of each error condition: Not specified in the source documents (GAP-3050; ASM-5125, ASM-5126, ASM-5127, ASM-5132) | Not specified in the source documents (DOR-RWB-S7-E6028-CON-7) |

The field-level types, lengths and required flags of the added element properties are settled in the baseline review; this story fixes the element names, the placeholder rule of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/sale-selection` (path and operation ID Not specified in the source documents (GAP-3050; ASM-5125)) | The sale selection in, with the write-off reference, the selection, `placement_type` and the sale reference; the write-off answer of status 200 out, with the rule `R-WO-32` and its version, the state `SOLD_POST_CHARGEOFF` and the record reference | Write-off and posting, right C, scope applied | `Idempotency-Key` header |
| GET | `/write-offs?sale=SOLD_POST_CHARGEOFF` (path and filter Not specified in the source documents (GAP-3050; ASM-5125)) | The sold population, paged: write-off reference, case reference, amount, committee date, posted date and selection time | Write-off and posting, right R, scope applied | none (a GET) |

The selection answers 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the population, 409 for a case that has left `PLACEMENT_DECIDED`, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The two paths, the two operation IDs and the element names are fixed by this baseline and copied from no source; TSD S7 T-A.1 publishes only API-S7-001 and API-S7-002, so the placeholder stands until the solution architect confirms it (GAP-3050; ASM-5125). The scan (API-S7-001, right C) and the committee decision (API-S7-002, right A) belong to RWB-S7-E6013-APP and RWB-S7-E6018-APP to RWB-S7-E6020-APP; neither is declared, extended or renumbered here (BR12).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3050; ASM-5127)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `PLACEMENT_DECIDED`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3050; ASM-5127)) | rwb-case (P3) | P3 rwb-case | The move `SOLD_POST_CHARGEOFF` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3050; ASM-5132)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-12, R-WO-32 and the write-off committee limit among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3050; ASM-5127, ASM-5132). rwb-debtsale consumes this service's population read; that row is provided here, not consumed, and no operation of rwb-debtsale is called in return (ASM-5127).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, `writeOffId`, `caseId`, `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21 and is declared by RWB-S7-E6021-APP. A sale selection hands a population over and posts nothing, and no source names an event for it, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one (ASM-5127). The outbox that relays events is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5132).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7), not in the sale selection: a selection reads no ACE extract and moves no money. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one. The trigger is the officer's selection on SCR-27 through the composite route, because the FSD declares no background event for the feature beyond the monthly scan (FSD S7 A2.16.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | The stage that hosts the sale step; its signals and its outcome for the parent are declared, not built |
| `recordSaleSelection` | Activity, the one sale step with R-WO-32 | `rwb-writeoff` | The write-off reference, the selection, the sale reference and the package version in; the rule ID with its version, the selection recorded, the row state and the case move out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, the step runs from the officer's selection, and no activity is registered by this story. The debt sale stage is a child of `CaseWorkflow` on `rwb-debtsale` and is S6's, not a workflow of this baseline (ASM-5127).

Workflow ID form: Not specified in the source documents (CG-ALL-11253). Start rule: the catalog row gives the trigger JOB-16 on the third working day after AceDataReady (R-WO-01); the start mode and the duplicate-start policy are Not specified in the source documents (CG-ALL-11253).

#### 12.6 Schedules

None. The sale selection is an officer-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The "per cycle" timer of R-WO-32 is the monthly sale cycle of rwb-debtsale (RWB-S6-E6005-APP), `JOB-16` becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and the placement review timer of R-WO-17 is RWB-S7-E6020-APP's; all three are named here only as other stories'.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its fields, its dates and its `state`; the table the write-off answer and the population row are drawn from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the selection (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `payment` (P8) and every lot and buyer table (S6) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `PLACEMENT_DECIDED` with `placement_type` sale, `RC-2027-000184` among 25 accounts; a case at another state; a case above the write-off committee limit with no escalation | AC1, AC3, AC6 |
| rwb-case case-move fake | The move `SOLD_POST_CHARGEOFF` accepted with the rule version, and a move refused | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-12, R-WO-32 and the write-off committee limit among its 51 rules over 27 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for the sold population, before and after a selection | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The paths, the operation IDs and the element names carry the placeholder until the solution architect confirms them, and the operation names of the three consumed rows until their owners confirm them (GAP-3050; ASM-5125, ASM-5127, ASM-5132).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The sale selection and the sold-population read on `/api/recovery/writeoff/v1`; the case read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `WriteOffWorkflow` and `recordSaleSelection` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here; the buyer files are S6's and rwb-integration's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no amount, no selection and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row changes. DP-13 moves the base of the legacy paths and gives the two operations their home. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-11 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE extract as another service's data and never a view, the outbox as an absent library row rather than an event of this step, and the hand-off to rwb-debtsale as a case move rather than a call (GAP-3050; ASM-5127, ASM-5132).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and a second kit row with no story file in the service story folder (CG-ALL-11251) that a rule evaluation would add. The three consumed rows are C dependencies in fact and not in the metadata row; the population read consumed by rwb-debtsale adds no row here because it is provided by this service.

**Deliverables and build steps**

1. Write the two operations of AC1 and validate the additive rule in the pipeline.
2. Write the three elements, their required flags, the `placement_type` and sale-reference placeholders of AC2.
3. Record the case row, the case-move row and the package row of AC3 with their owner, their budget and their placeholders.
4. Record the rights, the role conflict and the error envelope of AC4.
5. Record the decision-record element and the chain to the approval record of AC5 and validate it against the library schema.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the three elements, the contract README rows for the two provided and the three consumed operations and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract cases pass, the fakes answer every consumed path and the drift test is green, and the app story, rwb-debtsale, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes the held-scan state from which no case reaches the write-off population (R-WO-03), raised by RWB-S7-E6013-APP and not by this operation | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the selection among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its post-charge-off and sold states through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the population, the write-off facts and the selection, and rwb-case for the case and its route state; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved", and the post-charge-off state this step needs is not among them, so the screen gains a post-charge-off and a sold state that no source describes and the edge contract carries them as a placeholder (GAP-3050; ASM-5129). The scan state is RWB-S7-E6013-APP's, the proposed state RWB-S7-E6015-APP's and the committee states RWB-S7-E6017-APP's to RWB-S7-E6020-APP's. The refusal, missing-field, wrong-state and not-recorded states read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-11258).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-028-01 | AC1, AC3 | Contract | The 25-account post charge-off population on the fake; the contract half answers the two operations, the case row and the package row |
| TC-E6-028-02 | AC2, AC4 | Contract | `RC-2027-000184` at `PLACEMENT_DECIDED`; the contract half answers the three elements, the placeholders and the rights |
| TC-E6-028-03 | AC2, AC6 | Contract | The selection and population elements and the five fakes; the contract half answers the write-off facts and the fake drift |
| TC-E6-028-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-E6-028-05 | AC4 | Contract | A role without the right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-028-06 | AC5, AC7 | Contract | A forced record failure and a drifted fake; the contract half answers the failure and the absence of a published or consumed event |
| TC-S7-E6028-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the placeholders, the `Idempotency-Key`, the paging and the seven error answers are present |
| TC-S7-E6028-CON-02 | AC2 | Contract | The three elements validate with their properties, the required flags and the two placeholders |
| TC-S7-E6028-CON-03 | AC3, AC4 | Contract | The three consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-rule-row and no-lot boundary; the rights and the role conflict |
| TC-S7-E6028-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema and the chain; the five fakes match the document and a drifted fake fails the build |
| TC-S7-E6028-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |
| TC-S7-E6028-CON-06 | AC7 | Contract | The four tables of §12.7 at their boundary: each table with its owner, and a table outside §12.7 or a foreign key leaving the schema is refused |
| TC-S7-E6028-CON-07 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S7-E6028-CON-AC8) |

The six legacy cases are those of RWB-E6-028 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6028-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S7-E6028-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: R-WO-12, R-WO-32, its states, `placement_type`, the sale reference, the decision code set and the package version stay rule rows and reference data, never a schema default, an enumeration member or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates and a rule version only, and every example is synthetic; no buyer data crosses into this schema.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write (BR3).
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read.
- The buyer side stays with rwb-debtsale: the document declares no lot, reserve, award, buyer or sale agreement and calls no operation of S6.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the paging convention, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-006 | Post charge-off treatment is set by rule, including placement with an agency (FSD S7 Requirements served); the sale is the other placement of the same rule run and the row is taken over the empty plan row (ASM-5133) | The two operations, the three elements and the three consumed rows | TC-E6-028-01, TC-E6-028-02, TC-S7-E6028-CON-01, TC-S7-E6028-CON-02, TC-S7-E6028-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6028-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S7-E6028-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S7-E6028-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its chain to the approval record | TC-S7-E6028-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-028, disposition Split (rework); feature FEAT-WOF-16 |
| Legacy criteria | AC1, AC2, AC3 and AC4 of the legacy story, owned word for word by RWB-S7-E6028-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-028; FSD S7 Write-off and recovery v3 A2.16, A2.16.2, A2.16.3, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T3.3, T4, T5.3, T6.1, T8 and T-A; Business Rules and Routing Logic v4 rows R-WO-12 and R-WO-32; Recovery Workbench Epics 3 to 8 Specification v3 row FEAT-WOF-16 |
| Test cases | The six legacy cases as the contract half, and the five new contract cases TC-S7-E6028-CON-01 to -05 |
| Feature and screens | FEAT-WOF-16, SCR-27 Write-off proposal |
| Rules | R-WO-32, governed in rwb-decision; R-WO-12 named as the limit rule asserted by the app story |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-WO-32, the decision record, the row update and the case-move answer: RWB-S7-E6028-APP.
- The paths, operation IDs and element names: placeholders confirmed by the solution architect at the baseline review, and the value set of `placement_type`, the sale-reference format and the decision code set confirmed by the business lead (GAP-3050; ASM-5125, ASM-5126).
- Case state and write-off states (GAP-1800): the write-off states stay the stage's own record inside WriteOffWorkflow, the outcome is published, and rwb-case moves the case state; the split is an open question with the P3 owner so that no state has two writers.
- Payment matching after charge-off (GAP-1812): this service consumes ProceedsMatched (EV-25) as the match; an unmatched payment is held in the exception list; the ownership of the initial match is an open question with the P8 owner.
- Hand-off to the debt sale route (GAP-1799): the population, the route and the approval are recorded in this story; the call type and the direction are an open question with the S6 owner before the wave 4 system test.
- Sale harness pack (GAP-0458): the harness keys, amounts, the write-off committee limit, the business date and the gate are held as configuration for the wave 4 entry check; the population is asserted through the case read, the decision log and DP09.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5127).
- The authoring, testing, approval and versioning of the WO package, of the rule rows and of the write-off committee limit: rwb-decision (P7) (ASM-5132).
- The lots, reserve and tiered terms, the bids, the buyer portal, the award, the cap and the settled sale: rwb-debtsale (S6), RWB-S6-E5024-APP to RWB-S6-E6012-APP.
- The post charge-off decision of R-WO-29 and the agency placement of R-WO-30: outside this split (ASM-5129).
- The scan and the committee decision of the module: API-S7-001 and API-S7-002 are other stories', and neither is extended here.
- The posting, `WriteOffApproved` (`EV-24`) and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The gateway-bff composite route and the screen field list of SCR-27, including the post-charge-off and sold states: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
