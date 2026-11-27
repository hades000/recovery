# RWB-S7-E6014-CON Apply the tax criteria - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Contract version | v1, base `/api/recovery/writeoff/v1`, OpenAPI document `openapi/rwb-writeoff-v1.yaml` |
| Depends on (build) | None |
| Contract dependencies | The population read `/api/recovery/case/v1`, the package read `/api/recovery/decision/v1` and the case-move answer of rwb-case (P3), class C, per section 12.2 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the tax-criteria step of rwb-writeoff, split from RWB-E6-014. It fixes the scan operation on `/api/recovery/writeoff/v1` (DP-13), the `ScanRequest` and `WriteOffScan` elements with the fields DF-FIN-010 to DF-FIN-020 and the tax-criteria result, the consumed rows of the rwb-case population and case-move answer and the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. No source publishes a field list for the two elements or a home for `tax_criteria_version`; DP-04, DP-09 and DP-10 are not in the plan's pattern set although the step evaluates 51 rules, the service owns topic EV-24 and the scan is job JOB-16. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 12 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the tax-criteria step of rwb-writeoff — the scan operation on `/api/recovery/writeoff/v1`, the `ScanRequest` and `WriteOffScan` elements with the tax-criteria result and the post charge off remittance, the consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a list value, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy tax-criteria step of RWB-E6-014 crossed four boundaries at once: the proposed population, the case state, the rule version and a screen. The target splits them: rwb-case owns the case and its route states, rwb-decision owns the WO package and the tax criteria version, and rwb-writeoff owns the `write_off` row and the scan operation. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the fields of DF-FIN-010 to DF-FIN-020, the tax-criteria result and its version, the population and case-move rows, the package row and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the case facts are consumed on the owner's contract only.

Three points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the step consumes three rows, and DP-04, DP-09 and DP-10 are absent from the pattern set although a package is evaluated, the service owns an event and `JOB-16` is a scan (ASM-5015, ASM-5016); `tax_criteria_version` has no table, owner or key in any source, so its declaration is a working read (ASM-5011); and the R-WO-51 remittance has no channel into this service in the connection matrix, so its record is an element of this document and not a subscription (ASM-5014).

One boundary is stated rather than left to the reader: the scan operation is shared with the population half of the same feature, whose contract is RWB-S7-E6013-CON, so this baseline fixes the tax-criteria result, the tax criteria version and the remittance record on the `WriteOffScan` element and does not replace that document; the two are same-service baselines of one operation and are reconciled at the same contract freeze (ASM-5018).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case population row and case-move answer and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3019; ASM-5012).
- The outbox and inbox library of DP-09 and the schedule row of DP-10 are the platform dependencies of the service's topic and of `JOB-16`; the plan's H row for this key does not carry them, and this baseline keeps the row as the plan states it and declares no event and no Schedule (ASM-5015, ASM-5016).
- The WO package, its rows for R-WO-01, R-WO-03 and R-WO-51 and `tax_criteria_version` are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step: the scan operation with its request and answer elements, the filters, the right and the error responses.
2. Fix the `ScanRequest` and `WriteOffScan` elements: the write-off columns of DF-FIN-010 to DF-FIN-020, their types, their required flags and the list each is declared against, with the tax-criteria result and its version as the centre of the answer.
3. Fix the consumed rows: the population read and the case-move answer of rwb-case, and the package read of rwb-decision with its version and `tax_criteria_version`, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the `write_off` row changes, and the remittance element of R-WO-51 written on the same row.
5. Record the closed vocabulary, the right of the operation, the naming baseline and the rule that no value is a constant of the code.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
8. Tag the baseline and hand it to RWB-S7-E6014-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row or an element has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside a closed list appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event of this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S7 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operation, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6014-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the tax-criteria step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The scan operation is declared on the writeoff base with its shapes and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-off-scans with a ScanRequest body in and a WriteOffScan answer of status 201, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the create declares the Idempotency-Key header and the repeated key answering the scan it ran
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no committee-decision operation, no posting operation and no retention operation is declared by this document

  Scenario: AC2 The write-off element, the tax-criteria result and the lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1 and T3.2
    Then the WriteOffScan element declares the write-off properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id, amount, tax_criteria_met and recovered_after are required, and decision_log_id, committee_date, posted_date, responsibility_center, cost_center and gl_product are optional
    Then tax_criteria_met is declared as the recorded result of the tax-criteria test and carries no threshold and no criteria value of its own
    Then the answer carries the tax criteria version in force as the version of the package it was tested with, and an absent version is described as the held state and not as a default
    Then the create declares no committee date, no posting date, no responsibility center, no cost center and no GL product, which belong to the committee and posting stories
    Then no property is added for a person name, an address, a contact value or an identity number

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the population read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the balance, the account link and the case state of the cases in SCAN_DUE
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move POPULATION_PROPOSED, SCAN_HELD or CASE_CLOSED carrying the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version, its 51 rules over 27 states, R-WO-01, R-WO-03 and R-WO-51 and tax_criteria_version
    Then the operation names of the three rows and the owner of tax_criteria_version are Not specified in the source documents (GAP-3019; ASM-5011, ASM-5012) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The decision-record element and the remittance record of R-WO-51 are declared and written before the change (new, D-RCV-60)
    Given the decision and remittance sections of the baseline
    When they are compared with the library schema and with TSD S7 T2 and T3.1
    Then one decision record is declared per rule outcome with the case reference, the rule ID, the package version in force, the tax criteria version, the inputs reference, the outcome, the amount and the case move
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the write_off row changes, and a failed write leaves it unchanged with MSG-P7-003
    Then the remittance record is declared as an update of recovered_after on the sold account's write_off row, with the case reference, the amount and the decided-at time, and it creates no second row and no new table
    Then the record carries no rule row, no threshold as a literal and no personal data

  Scenario: AC5 The error envelope, the messages and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S7 T-A.1, T-A.2 and T6.1
    Then the operation declares Write-off and posting right C with the scope applied
    Then a missing tax criteria version is described as 422 with MSG-S7-001, a role without the right as 403 with MSG-P4-002, a failed record write as 503 with MSG-P7-003 and a missing required field as 422 with MSG-GEN-001
    Then RW-WRITEOFF holds CRU on the capability area, RW-CREDITAD holds CRUA, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and every other role and every SY-* service identity of TSD S7 T6.1 holds R
    Then the error envelope carries one message ID per condition and the four messages are the legacy and FSD wording, unchanged

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case population fake answers the population of the cut-off date with 120 cases in SCAN_DUE, a case that has left the population, and the three moves accepted and refused
    Then the rwb-decision fake answers the WO package at its version with R-WO-01, R-WO-03 and R-WO-51 and tax_criteria_version, and an absent version
    Then the rwb-case case-move fake answers POPULATION_PROPOSED, SCAN_HELD and CASE_CLOSED, the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event and no Schedule are declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the table named as owned is write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then the document declares no event of this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as the committee story's and JOB-16 as the scan story's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5014, ASM-5015)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6014-APP and copy no criterion of the legacy story, whose four criteria stay with the app story word for word. The tax criteria themselves are not a property of this document: `tax_criteria_met` is a recorded boolean and the criteria are rule facts of the WO package (ASM-5011).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The population and the write-off are rwb-writeoff's, and the contract declares the fields and the required flags of `write_off` only | TSD S7 T3.1; context pack ownership rows (table `write_off`) |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC4 |
| BR3 | The case facts stay with rwb-case: the contract declares the population read and the case-move answer as consumed, declares no `recovery_case` property and describes no ACE table read | DP-05 as a prohibition; ASM-5012 |
| BR4 | `tax_criteria_version` is declared as a consumed package fact, with the placeholder until its owner publishes it, and no criteria value, threshold, default or track name appears in the document; the version is recorded on every account and the scan opens only on a published version (GAP-1803); the package and rule version are recorded on every scan and decision, and the package code and its promotion date are Not specified in the source documents (GAP-1802) | FSD S7 VR-S7-002-1 and A2.2.3.1; ASM-5011; GAP-1803; GAP-1802 |
| BR5 | The post charge off remittance is an update of `recovered_after` on an existing row and not a new element family, a new table or a second write-off | TSD S7 T3.1 (DF-FIN-020); ASM-5013, ASM-5014 |
| BR6 | No event of this step is declared: `WriteOffApproved` (EV-24) is the committee story's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5016; TSD S7 T5.3 |
| BR7 | No Schedule is declared: `JOB-16` is the scan story's and the schedule row of DP-10 is recorded as absent; its trigger is a Temporal Schedule on the 3rd working day that also tests the ACE batch, with no Quartz table, connection or job (GAP-1801) | ASM-5015; ASM-A6-flows-12; context pack job row |
| BR8 | A POST declares the `Idempotency-Key` and stores its answer | TSD S7 T-A.2 |
| BR9 | The vocabulary is closed where a list exists, and no list value is a constant of the code; the parameters read and the reference-data contract (DP-06, DP-07) are Not specified in the source documents (DOR-RWB-S7-E6014-CON-20) | TSD S7 T3.2; FSD S7 BR-S7-002 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a boolean and a rule version only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR11 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR13 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the consumed rows, the decision and remittance elements and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional write-off field or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED`, `REMITTED_TO_BUYER` and `CASE_CLOSED` are route states of the WRITEOFF machine of TSD S7 T4 and live on the case of record. This baseline fixes the vocabulary and the enums and moves no write-off and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the three consumed rows and the absent DP-04, DP-09 and DP-10 rows |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-access and rwb-payment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

The authorise check of rwb-access (DP-08) is consumed and is not declared in this baseline; its operation name is Not specified in the source documents (DOR-RWB-S7-E6014-CON-6). The five roles above are the authority of this story.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` | DF-FIN-010 to DF-FIN-020 |
| Required flags | `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the other six optional, because the committee, the posting and the GL own their values | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Tax-criteria result | `tax_criteria_met` as the recorded boolean of the rule outcome, with the criteria version recorded beside it as a package fact, never as a threshold or a criteria value | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Remittance record | `recovered_after` on the sold account's row, written by the R-WO-51 path with the case reference, the amount and the decided-at time | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Lists | None is named for this step by TSD S7 T3.2, which leaves the list table empty; a value this step records is a rule outcome, a state name or a date | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Event data | None of this step: no event is declared (§12.3) | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Case facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, read only through the owner's rows and never written, copied or joined here | DF-CAS-001 to DF-CAS-023 |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8), and the later stories' tables of this service | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |
| Consumed fields with no source | The operation names of the three consumed rows and the owner, the table and the key of `tax_criteria_version`: Not specified in the source documents (GAP-3019; ASM-5011) | Not specified in the source documents (DOR-RWB-S7-E6014-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

The field list of the two elements is a working read of this baseline (ASM-B2-S7-002-1 to ASM-B2-S7-002-6): the scan is a `POST` on the base of this story, with a `ScanRequest` and a `WriteOffScan` answer, with the status code Not specified in the source documents (GAP-3019); the eleven write-off properties of DF-FIN-010 to DF-FIN-020 are declared, with `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the tax criteria version is carried as a package fact beside the result; the remittance is an update of `recovered_after` and not a new element family; the `Idempotency-Key` is declared on the POST; and the step declares no event and no Schedule.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in, WriteOffScan of status 201 out, the scan run for a cut-off date with the tested population, its tax-criteria result and the recorded remittances (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The operation answers 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 or MSG-S7-001 and 503 with MSG-P7-003, each with the error envelope and one message ID of section 14. The operation ID is that of TSD S7 T-A.1 and the path is that of the target base, not the monolith form. The population half of the same operation is RWB-S7-E6013-CON's; this baseline owns the tax-criteria result, the tax criteria version and the remittance record of the element and adds no second path, and the two baselines are reconciled at the wave 4 contract freeze (ASM-5018). `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is the approve, reject and defer stories' and is not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The population read (operation name Not specified in the source documents (GAP-3019; ASM-5012)) | `/api/recovery/case/v1` | P3 rwb-case | The cases in `SCAN_DUE` for the cut-off date and the sold account of the remittance path, with the case reference, product group, balance, account link and state; faked |
| The package read in force (operation name Not specified in the source documents (GAP-3019; ASM-5011)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-01, R-WO-03 and R-WO-51 among its 51 rules over 27 states and `tax_criteria_version`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3019; ASM-5012)) | rwb-case (P3) | P3 rwb-case | The move `POPULATION_PROPOSED`, `SCAN_HELD` or `CASE_CLOSED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3019; ASM-5012). This service reads no `v_ace_*` view and no ACE table; the freshness and the GL write-off posting are carried as the source field names that the rwb-source-data contract returns, and P1 confirms those fields and the freshness response before the wave 4 system test.

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`) with the retry and `.dlt` topics of the platform (TSD S7 T5.3; DP-14), and it does not belong to this step, because the tax-criteria test approves nothing. `WriteOffApproved` is declared as the committee story's, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays it is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5016).

#### 12.4 Events consumed

None. The step is started by the monthly scan and by the case signal the parent forwards, and the connection matrix shows no event line into S7 from the debt sale or partner side on which the buyer confirms receipt, so the remittance reaches the step as a forwarded signal. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one (ASM-5014).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end; workflow ID form, start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-10873) | `rwb-writeoff` | The stage that hosts the tax-criteria step; its input, signals and outcome for the parent are declared, not built |
| `evaluateTaxCriteria` | Activity, the one tax-criteria step | `rwb-writeoff` | The population, the package and the cut-off date in; the rule ID with its package version, the tax criteria version, the result, the remittance amount, the write-off reference and the case moves out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, and the step waits on the monthly scan and on the forwarded signal. No activity is registered by this story.

#### 12.6 Schedules

None. The monthly write-off scan is job `JOB-16` in the legacy and becomes a Temporal Schedule of the scan story (`RWB-S7-E6013-APP`); this baseline declares no Schedule, no Quartz row, no shared job table and no batch table, and records that DP-10 and its `RWB-PLT-E1071-CON` row are absent from the plan (ASM-5015).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a balance on a case, its fields and its required flags; the table the scan operation answers from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `proceeds` (P8) and the later stories' tables of this service are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case population fake | The population of the cut-off date with 120 cases in `SCAN_DUE`, `RC-2026-000914` among them, with the product group, the balance, the account link and the state; a case that has left the population | AC1, AC3, AC6 |
| rwb-decision package fake | The WO package at its version in force with R-WO-01, R-WO-03 and R-WO-51, `tax_criteria_version`, and an absent version | AC2, AC3, AC6 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED`, `SCAN_HELD` and `CASE_CLOSED` accepted, and a move refused | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000914`, in its scan state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows carry the placeholder until their owners confirm them (GAP-3019; ASM-5012).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1`; the population read, the package read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `WriteOffWorkflow` and `evaluateTaxCriteria` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no write-off, no case, no balance and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row changes. DP-13 moves the base and nothing else. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-10 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the case as a consumed population and never a table, the outbox as an absent library row rather than an event of this step, and `JOB-16` as the scan story's Schedule rather than this one's (GAP-3019; ASM-5015, ASM-5016).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the schedule row `RWB-PLT-E1071-CON` that `JOB-16` needs, the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit row `RWB-PLT-E1072-CON` and a second Drools kit row whose key is Not specified in the source documents (CG-ALL-10871) that a rule evaluation would add. The three consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the scan operation and validate the additive rule of AC1 in the pipeline.
2. Write the `ScanRequest` and `WriteOffScan` elements, their required flags, the tax-criteria result and the remittance property of AC2, with the placeholder where a type is unstated.
3. Record the population row, the package row and the case-move row of AC3 with their owner, their budget and their placeholders.
4. Record the decision-record element and the remittance record of AC4 and validate them against the library schema.
5. Record the error envelope, the four messages and the rights of AC5.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the two elements, the contract README rows for the three consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The document describes the held state of R-WO-03 when the tax criteria version is absent, which the app story raises while the rule runs | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 is the only condition that is this feature's own, and it is carried on the held answer of the operation.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its loading and scan states through the gateway-bff composite route (DP-19). The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-10878). The route calls rwb-writeoff for the tested population, its tax-criteria result and the remittance record, and rwb-case for the case and its route state; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved": the scan and proposed states are this step's, the in-committee and approved states belong to the committee stories, and the held state is the reading of MSG-S7-001. The refusal, not-recorded and hold states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-014-01 | AC1, AC2 | Contract | The document half answers the scan operation, the element and the tax-criteria result property |
| TC-E6-014-02 | AC2, AC3 | Contract | Case `RC-2026-000914` in `SCAN_DUE`; the contract half answers the population row and the `POPULATION_PROPOSED` move shape |
| TC-E6-014-03 | AC3, AC4 | Contract | Case `RC-2026-000914` at `REMITTED_TO_BUYER`; the contract half answers the remittance property and the `CASE_CLOSED` move shape |
| TC-E6-014-04 | AC4, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the fake drift test |
| TC-E6-014-05 | AC5 | Contract | A role without the Write-off and posting right and a malformed request; the 403 with MSG-P4-002 and the 422 envelope |
| TC-E6-014-06 | AC4, AC5 | Contract | An absent tax criteria version; the contract half answers the held answer with MSG-S7-001 |
| TC-S7-E6014-CON-01 | AC1 | Contract | The document validates; the operation, the base, the `Idempotency-Key` and the seven error answers are present |
| TC-S7-E6014-CON-02 | AC2 | Contract | The `WriteOffScan` element validates with its eleven properties, its five required flags and the tax-criteria result |
| TC-S7-E6014-CON-03 | AC3, AC4 | Contract | The three consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary; the record and remittance elements match the library schema |
| TC-S7-E6014-CON-04 | AC5, AC6 | Contract | The four messages, the rights of TSD S7 T6.1 and the five fakes; a drifted fake fails the build |
| TC-S7-E6014-CON-05 | AC7 | Contract | The naming baseline, the table owned and the absence of a published event, a consumed event, a second topic and a Schedule |
| TC-S7-E6014-CON-06 | AC7 | Contract | The four tables of §12.7 and the boundary: no table outside `rwb_writeoff` is declared as owned, and `recovery_case`, `timer` and the `v_ace_*` views are not in the list |

The six legacy cases are those of RWB-E6-014 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6014-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The six cases `TC-S7-E6014-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the tax criteria, `tax_criteria_version`, the eligibility and hold conditions, the remittance condition and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a boolean and a rule version only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3).
- The money and the posting reference stay with rwb-payment and the posting story: the document declares no posting, no proceeds and no settlement property.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks; the contract fixes the operation, the element and the consumed rows on which the test is built (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3019) | The `ScanRequest` and `WriteOffScan` elements, the tax-criteria result and the three consumed rows | TC-E6-014-01, TC-E6-014-02, TC-S7-E6014-CON-01, TC-S7-E6014-CON-02, TC-S7-E6014-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6014-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the committee story's | TC-S7-E6014-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S7-E6014-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6014-CON-03, TC-S7-E6014-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-014, disposition Split (rework); feature FEAT-WOF-02 |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S7-E6014-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-014; FSD S7 Write-off and recovery v3 A2.2; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-01, R-WO-03 and R-WO-51 |
| Test cases | The six legacy cases as the contract half, and the five new contract cases TC-S7-E6014-CON-01 to -05 |
| Feature and screens | FEAT-WOF-02, SCR-27 Write-off proposal |
| Rules | R-WO-01, R-WO-03 and R-WO-51, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the scan operation, the evaluation of R-WO-01, R-WO-03 and R-WO-51, the decision record, the row and the case-move answer: RWB-S7-E6014-APP.
- The case of record, its route states, the population and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5012).
- The authoring, testing, approval and versioning of the WO package and of the rule rows, and the home and the key of `tax_criteria_version`: rwb-decision (P7) (ASM-5011, ASM-5016).
- The monthly scan Schedule from `JOB-16` and the eligibility test on both tracks: the scan story of RWB-E6-013 (ASM-5015).
- The committee decision of API-S7-002, the pack, the routing, the approve, the reject and the defer: FEAT-WOF-03 and FEAT-WOF-05 to 08.
- The posting, the provision release, the Finance feed and the reconciliation of the approved and posted populations: FEAT-WOF-09 to 11.
- The exception loop, the retention closure, the change of the criteria and the post charge off sale: FEAT-WOF-12 to 14 and FEAT-WOF-16.
- The money, the remittance source and the posting reference: rwb-payment (P8) and the debt sale route (S6), neither of which publishes a row this baseline declares.
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
