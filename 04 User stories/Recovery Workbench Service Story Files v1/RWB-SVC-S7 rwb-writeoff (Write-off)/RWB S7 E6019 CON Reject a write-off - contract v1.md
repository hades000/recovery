# RWB-S7-E6019-CON Reject a write-off - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6019-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the committee decision of rwb-writeoff, split from RWB-E6-019. It fixes the reject branch of the published `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) on `/api/recovery/writeoff/v1` (DP-13) with the `CommitteeDecision` request and the `DecisionLogEntry` answer of TSD S7 T-A.2, the decision and reason fields with their placeholders where no source gives a value set or a length, the consumed rows of the rwb-case case read and case-move answer and the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. DP-04 and DP-09 are not in the plan's pattern set although the stage evaluates a package and the service owns a topic, the plan's C row is empty although the contract declares three consumed rows, and no source publishes the decision code set or the reason field (GAP-3030; ASM-5052, ASM-5053, ASM-5054, ASM-5005). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the committee decision of rwb-writeoff — the reject branch of the committee-decision operation on `/api/recovery/writeoff/v1`, the decision and write-off elements with their required flags, the reason field, the three consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a reason rule, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy rejection of RWB-E6-019 crossed three boundaries at once: the case of record, the rule version and a screen, and its single committee-decision endpoint carried the approve, reject and defer decisions with no element published for any of them. The target splits them: rwb-case owns the case and its route states, rwb-decision owns the WO package, and rwb-writeoff owns the write-off stage, its record and the committee decision for a case inside the limit. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Four points are carried as gaps and assumptions rather than decided quietly: the decision code set of the record and the reason field have no published value set, length or field ID (ASM-5053); the plan's C row is None while the operation consumes three rows, and DP-04 and DP-09 are absent from the pattern set (ASM-5054, ASM-5005, ASM-5055); the operation is published but its error set is a list of status codes with no message ID per condition, so each condition is bound to a message of the legacy set (ASM-5052); and the reject shares one requirement, REQ-S7-003, with the approval and the deferral stories (ASM-5057).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The committee-decision operation itself is published: TSD S7 T-A.1 gives API-S7-002 `POST /write-offs/{writeOffId}/committee-decision` with the request `CommitteeDecision`, the answer `DecisionLogEntry`, the rights and the idempotency rule, and TSD S7 T-A.2 gives the error set as 401, 403, 404, 409, 422 and 503. The reject branch is declared inside it and needs no new path; what the sources do not give is the decision code set and the reason field (GAP-3030; ASM-5052, ASM-5053).
- The rwb-case case row and case-move answer and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3030; ASM-5054, ASM-5005).
- The WO package and its rows for R-WO-16 and R-WO-18 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. The reason has no column in it (ASM-5053).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the reject branch of the OpenAPI 3.1 document of rwb-writeoff for API-S7-002: the operation with its request and answer elements, the decision and reason properties, the rights and the error responses.
2. Fix the `DecisionLogEntry` element over the write-off columns of DF-FIN-010 to DF-FIN-020 and the ledger properties of DF-DEC-001 to DF-DEC-018, and the `CommitteeDecision` element with the write-off reference, the decision, the reason and the request reference.
3. Fix the consumed rows: the case read of rwb-case, the case-move answer of rwb-case and the package read of rwb-decision with its version, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the case moves.
5. Record the rights of the operation, the naming baseline and the rule that no value is a constant of the code; record that the service publishes no list of values because TSD S7 T3.2 is empty, and that the decision code set is a placeholder.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
8. Tag the baseline and hand it to RWB-S7-E6019-APP, to the approval and deferral stories that share the operation, to SCR-27 and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | The reason or the decision code is declared as an enumeration taken from no source | The vocabulary test fails the build: TSD S7 T3.2 publishes no list, and no source gives the code set | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S7 T6.1 and T-A.2 give the committee decision | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones TSD S7 T-A.2 gives, the example values and the fake fixtures are settled in the baseline review; the base, the operation, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6019-APP, the approval and deferral stories that share the operation, SCR-27 and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the committee decision of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The committee-decision operation is declared with its reject branch and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-offs/{writeOffId}/committee-decision as API-S7-002 with a CommitteeDecision body in and a DecisionLogEntry answer of status 200, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the operation declares the path parameter writeOffId, the Idempotency-Key header and the repeated key answering the decision it recorded
    Then the reject branch is declared inside the one operation as the decision the request carries, with no second path, and the approve and defer branches of the same operation are named as RWB-S7-E6018-APP's and RWB-S7-E6020-APP's
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the scan, of the pack or of the posting is declared by this document

  Scenario: AC2 The decision and write-off elements, the reason and the decision code are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1, T3.2 and T-A.2
    Then the DecisionLogEntry element declares the write-off properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then it declares the decision properties of DF-DEC-001 to DF-DEC-018: the decision code, the rule ID R-WO-16 with its rule version, the from state WITH_COMMITTEE, the to state RETURNED_TO_PURSUE and the decided-at time
    Then the CommitteeDecision element declares the write-off reference, the decision and the reason, with the reason required on a reject and a free-text string of unstated length
    Then the decision code carries the placeholder Not specified in the source documents (GAP-3030; ASM-5053) and the reason declares no enumeration, because TSD S7 T3.2 lists none and the legacy field lists none
    Then committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after are optional, and committee_date is named as set on approval by RWB-S7-E6018-APP and posted_date by RWB-S7-E6021-APP
    Then no property is added for a credit-committee rejection, an ACE extract or a rule row

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move RETURNED_TO_PURSUE carrying the reason, the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version and its 51 rules over 27 states
    Then the operation names of the three rows are Not specified in the source documents (GAP-3030; ASM-5054, ASM-5005) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T-A.1, T-A.2 and T6.1
    Then the committee decision declares Write-off and posting right A with the scope applied, on API-S7-002 as T-A.1 gives it
    Then RW-WOCOMM holds RA and RW-CREDITAD holds CRUA on the capability area, RW-PRODHEAD and RW-FINANCE hold RA, and they are the four roles the legacy permission table gives right A
    Then RW-WRITEOFF holds CRU and reads the rejection without the right A
    Then every other role and every SY-* service identity of TSD S7 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the case moves (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S7 T2
    Then one decision record is declared per rule outcome with the case reference, the decision code, the rule ID R-WO-16, the package version in force, the reason, the from state, the to state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the case-move answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record carries no rule row, no state threshold as a literal and no personal data

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the case at WITH_COMMITTEE with its pack and limit, a case that has moved and a case that is not in the pack
    Then the rwb-case case-move fake answers RETURNED_TO_PURSUE accepted and refused
    Then the rwb-decision fake answers the WO package at its version with R-WO-16 and R-WO-18
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer in its in-committee and post-decision states
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as RWB-S7-E6021-APP's and JOB-16 as RWB-S7-E6013-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5055)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6019-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The rejection is a case move back to the pursue track: no amount is approved, no provision is released and no posting is declared here (ASM-5055).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The committee decision is rwb-writeoff's, and the contract declares the fields and the required flags on the `DecisionLogEntry` element and on the `CommitteeDecision` element only | TSD S7 T3.1, T-A.2; context pack ownership rows (table `write_off`) |
| BR2 | The decision record is declared as an element written before the case moves, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC2 |
| BR3 | The case stays with rwb-case: the contract declares the case read and the case-move answer as consumed, declares no `recovery_case` property and describes no case row write | ASM-5054; TSD S7 T4 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule version as a property set | DP-05 as a prohibition for ACE data; ASM-5005 |
| BR5 | No event of this step is declared: `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5055; TSD S7 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer | TSD S7 T-A.2 |
| BR7 | The reason is declared as free-text with no enumeration, and the decision code carries a placeholder, because TSD S7 T3.2 publishes no list of values, no legacy field list names a reason and no source gives a code set | ASM-5053; FSD S7 A2.7.3.1, A2.7.3.2 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a reason and a rule version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The reject is a branch of the one published operation and not a second path; the approve and defer branches of the same operation are named as other stories' | TSD S7 T-A.1; ASM-5052 |
| BR13 | The rights of the decision are the capability area's approval right: A, held by RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE, and not the C of a population change | TSD S7 T6.1, T-A.1, T-A.2; legacy permission table of RWB-E6-019 |
| BR14 | The states `WITH_COMMITTEE` and `RETURNED_TO_PURSUE` are declared as the vocabulary of the answer and of rwb-case's machine, and move no case | ASM-5054, ASM-5055; TSD S7 T4; Business Rules and Routing Logic v4 row R-WO-16 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the reason rule, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the approval and deferral stories, SCR-27, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The decision code set is confirmed | The business lead replaces the placeholder code set with the confirmed one inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reference or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the reason becomes an enumeration | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a second path, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `WITH_COMMITTEE` and `RETURNED_TO_PURSUE` are route states of rwb-case (TSD S7 T4), R-WO-18 keeps a case at `WITH_COMMITTEE` when the reason is absent, and `ESCALATED_TO_CREDIT_COMMITTEE` belongs to the approval slice of RWB-S7-E6018-APP. This baseline fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed decision code set, and the correction of the plan rows the baseline consumes, including the three consumed rows and the absent DP-04 and DP-09 rows |
| Business lead | Confirms the decision code set and the reason wording that replace the placeholders |
| Consuming teams (the app story, the approval and deferral stories, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` |
| Decision element | The decision code, the rule ID `R-WO-16`, the rule version, the reason, the from state `WITH_COMMITTEE`, the to state `RETURNED_TO_PURSUE` and the decided-at time, over the ledger fields DF-DEC-001 to DF-DEC-018 |
| Required flags | The write-off reference, the decision and the reason required on the request, the reason on a reject; `id`, `case_id`, `amount` and `tax_criteria_met` required on the write-off element; the other properties optional |
| Lists | None: TSD S7 T3.2 publishes no list of values, so the baseline declares no enumeration, the reason is free text and the decision code set is a placeholder (ASM-5053) |
| Event data | None of this step: no event is declared (§12.3) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the case moves (DP-03) |
| Case and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) |
| Consumed fields with no source | The operation names of the case read, the case-move answer and the package read, the decision code set, the length of the reason and the message ID of each error condition: Not specified in the source documents (GAP-3030; ASM-5052, ASM-5053, ASM-5054, ASM-5005) |

The field-level types, lengths and required flags of the added element properties are settled in the baseline review; this story fixes the element names, the reason rule of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/committee-decision` (API-S7-002) | `CommitteeDecision` in, `DecisionLogEntry` of status 200 out, carrying the decision, the rule `R-WO-16` with its version, the reason and the state `RETURNED_TO_PURSUE` | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The operation answers 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the pack, 409 for a case that has left `WITH_COMMITTEE`, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The path, the operation ID, the two element names and the rights are published in TSD S7 T-A.1 and T-A.2; the decision code set and the reason field carry the placeholder (GAP-3030; ASM-5052, ASM-5053). The approve and defer branches of the same operation belong to RWB-S7-E6018-APP and RWB-S7-E6020-APP, and the module's other published operation, `POST /write-off-scans` (API-S7-001, right C), belongs to RWB-S7-E6013-APP; none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3030; ASM-5054)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `WITH_COMMITTEE`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3030; ASM-5054)) | rwb-case (P3) | P3 rwb-case | The move `RETURNED_TO_PURSUE` with the reason, the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3030; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-16 and R-WO-18 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3030; ASM-5054, ASM-5005).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, `writeOffId`, `caseId`, `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21, declared by RWB-S7-E6021-APP. A rejection approves nothing, posts nothing and changes no amount, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the event is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5055).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7), not in the committee decision: a rejection reads no ACE extract and moves no money. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one. The trigger of the step is the committee member's decision on SCR-27 through the composite route, because the FSD declares no background event for the feature beyond the monthly scan (FSD S7 A2.7.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the decision step; its signals and its outcome for the parent are declared, not built |
| `recordCommitteeDecision` | Activity, the one decision step with the reject branch | `rwb-writeoff` | The case reference, the decision, the reason and the package version in; the rule ID with its version, the decision recorded and the case move out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, and the step runs from the committee member's decision. No activity is registered by this story.

#### 12.6 Schedules

None. The committee decision is a member-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. `JOB-16`, the write-off scan, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and the meeting booking of R-WO-11 is RWB-S7-E6017-APP's; both are named here only as other stories'.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its fields and its dates; the table the answer element is drawn from and the row a rejection does not change |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rejection (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `WITH_COMMITTEE` with its pack and limit, `RC-2026-000731` among 40 cases; a case that has moved; a case that is not in the pack | AC1, AC3, AC6 |
| rwb-case case-move fake | The move `RETURNED_TO_PURSUE` accepted with the reason and the rule version, and a move refused | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-16 and R-WO-18 among its 51 rules over 27 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000731`, in its in-committee and post-decision states | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case read, the case-move answer and the package read carry the placeholder until their owners confirm them (GAP-3030; ASM-5054, ASM-5005).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The committee-decision operation on `/api/recovery/writeoff/v1` (reject branch); the case read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `WriteOffWorkflow` and `recordCommitteeDecision` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no amount and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the case moves. DP-13 moves the base of the legacy paths and gives the committee-decision operation its home. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05 and DP-09 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE extract as another service's data and never a view, and the outbox as an absent library row rather than an event of this step (GAP-3030; ASM-5005, ASM-5055).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add. The three consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the reject branch of API-S7-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `DecisionLogEntry` and `CommitteeDecision` elements, their required flags, the free-text reason of AC2 and the decision-code placeholder.
3. Record the case row, the case-move row and the package row of AC3 with their owner, their budget and their placeholders.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the two elements, the contract README rows for the three consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the approval and deferral stories, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes the held-scan state from which no pack reaches the committee (R-WO-03), raised by RWB-S7-E6013-APP and not by this operation | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the reason on a reject among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right A the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its in-committee and post-decision states through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the pack, the decision and the reason, and rwb-case for the case and its route state; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": the rejection is this step's reading of "in committee", the scan state belongs to RWB-S7-E6013-APP, the proposed state to RWB-S7-E6015-APP, the routing to RWB-S7-E6017-APP, the approved state to RWB-S7-E6018-APP and the deferred state to RWB-S7-E6020-APP. The refusal, missing-reason and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-019-01 | AC1, AC3 | Contract | The 40-case in-committee population on the fake; the contract half answers the operation, the case row and the package row |
| TC-E6-019-02 | AC2, AC5 | Contract | `RC-2026-000731` at `WITH_COMMITTEE`; the contract half answers the two elements, the reason rule and the decision element |
| TC-E6-019-03 | AC4 | Contract | A role without the right A and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-019-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S7-E6019-CON-01 | AC1 | Contract | The document validates; the operation, the base, the reject branch, the `Idempotency-Key` and the seven error answers are present |
| TC-S7-E6019-CON-02 | AC2 | Contract | The `DecisionLogEntry` element validates with its eleven write-off properties, its seven decision properties, the required flags, the free-text reason and the decision-code placeholder |
| TC-S7-E6019-CON-03 | AC3, AC4 | Contract | The three consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary; the rights |
| TC-S7-E6019-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the five fakes match the document and a drifted fake fails the build |
| TC-S7-E6019-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |

The four legacy cases are those of RWB-E6-019 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6019-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S7-E6019-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: R-WO-16, its states, the reason rule, the decision code set and the package version stay rule rows and reference data, never a schema default, an enumeration member or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a reason and a rule version only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write (BR3).
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read.
- The money stays with rwb-payment and the ledger with rwb-decision: the document declares no posting, no proceeds and no rule row.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (FSD S7 Requirements served); the reject shares the row with the approval and the deferral stories (ASM-5057) | The reject branch of API-S7-002, the two elements and the three consumed rows | TC-E6-019-01, TC-E6-019-02, TC-S7-E6019-CON-01, TC-S7-E6019-CON-02, TC-S7-E6019-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6019-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S7-E6019-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S7-E6019-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6019-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-019, disposition Split (rework); feature FEAT-WOF-07 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S7-E6019-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-019; FSD S7 Write-off and recovery v3 A2.7, A2.7.2, A2.7.3 and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-16 and R-WO-18 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S7-E6019-CON-01 to -05 |
| Feature and screens | FEAT-WOF-07, SCR-27 Write-off proposal |
| Rules | R-WO-16, governed in rwb-decision; R-WO-18 named as the refusal of an incomplete decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the reject branch, the evaluation of R-WO-16, the decision record and the case-move answer: RWB-S7-E6019-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5054).
- The authoring, testing, approval and versioning of the WO package and of the rule rows: rwb-decision (P7) (ASM-5005).
- The decision code set and the reason wording: the business lead confirms them at the baseline review and the placeholder stands until then (GAP-3030; ASM-5053).
- The approve branch of the same operation and the credit-committee escalation and rejection: RWB-S7-E6018-APP. The defer branch: RWB-S7-E6020-APP.
- The monthly scan, the tax criteria, the pack and the routing into committee: RWB-S7-E6013-APP to RWB-S7-E6017-APP.
- The posting, `WriteOffApproved` (`EV-24`) and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
