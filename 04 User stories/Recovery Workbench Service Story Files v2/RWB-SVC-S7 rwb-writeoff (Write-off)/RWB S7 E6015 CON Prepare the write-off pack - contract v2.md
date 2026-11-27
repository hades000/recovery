# RWB-S7-E6015-CON Prepare the write-off pack - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Contract version | v1 (base `/api/recovery/writeoff/v1`, DP-13) |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S7-E6015-CON-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the pack step of rwb-writeoff, split from RWB-E6-015. It fixes the pack element with the five elements R-WO-05 names and the eleven `write_off` columns DF-FIN-010 to DF-FIN-020 with the standard columns, the seven consumed rows of rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision, the decision-record element of DP-03, the rights of TSD S7 T6.1, the message set, the fakes and the absence tests, under base `/api/recovery/writeoff/v1` (DP-13). The legacy key owns no REST operation, so the two operations it names are declared as the scan story's and the committee story's. DP-20 and DP-09 are absent from the plan's pattern set although the step calls the agent and the service owns topic `rwb.writeoff.events.v1` with `EV-24`; the plan's C row is None while seven rows are consumed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 18 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off team member (RW-WRITEOFF)**, I want **the published contract baseline of the pack step of rwb-writeoff — the pack element with its five elements, the `write_off` columns and the standard columns, the closed lists, the seven consumed rows, the decision-record element, the rights, the message set, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a pack element, a column, a consumed row or a message can never drift between rwb-writeoff, rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy pack step of RWB-E6-015 crossed six boundaries at once: the case facts, the ACE balance and asset state, the document index, an agent run, a rule version and a screen. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the ACE data products, rwb-document owns the documents, rwb-agent runs the pack assembly, rwb-decision governs the WO package, and rwb-writeoff owns the `write_off` row and the pack element. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the eleven columns of DF-FIN-010 to DF-FIN-020, the five pack elements of R-WO-05, the seven consumed rows, the decision record and the message set.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_document`, so DP-05 is declared as the read of the owner's data product and never as a view (ASM-5020).

It also records what the plan and the sources do not settle, rather than deciding it quietly: the plan's C row is None while seven rows are consumed, and DP-04, DP-09 and DP-20 are absent from the pattern set although the step evaluates a package, the service owns a topic and R-WO-05 names the Agent Runtime (ASM-5021, ASM-5022, ASM-5025); the pack elements `provision_carried`, `residual` and the pack document have no column (ASM-5023); and SCR-27 needs a write-off read the Ownership Map does not carry (ASM-5026).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, every `v_ace_*` view and every ACE data product is P1's, `document` is P5's, `notice` is P6's, `proceeds` is P8's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's table or operation as its own.
- The rwb-case case-facts read and case-move answer, the rwb-source-data data-product read, the rwb-document index read and registration, the rwb-agent pack run and the rwb-decision package read are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3022; ASM-5020).
- The outbox and inbox library of DP-09 is the platform dependency of the service's topic and the agent client of DP-20 the platform dependency of the pack run; the plan's H row for this key carries neither, and this baseline keeps the row as the plan states it and declares no event and no agent operation of its own (ASM-5022, ASM-5025).
- The WO package and its row R-WO-05, the tax criteria version and the state vocabulary are governed in rwb-decision; this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract document of rwb-writeoff for this step: the pack element, the `write_off` shape it answers from, the rights and the message set.
2. Fix the `WriteOffPack` element: the case reference, the pack reference, the five elements of R-WO-05, the tax criteria version, the document reference and the state, each against the column or the list that carries it.
3. Fix the `write_off` shape of DF-FIN-010 to DF-FIN-020 with its required flags, its standard record columns and the columns this step does not write.
4. Fix the seven consumed rows with their owner, their budget and the placeholder where the sources give no operation name.
5. Record the decision-record element of DP-03, written before the row changes, and the rule version it carries.
6. Record the closed vocabulary, the rights of the capability area, the naming baseline and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the pack elements, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` or `document` write, the drift between a fake and the document, and the absence of a provided operation, of a published and of a consumed event, and of a Schedule.
9. Tag the baseline and hand it to RWB-S7-E6015-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC2, AC6 |
| X5 | A pack element appears that R-WO-05 does not name, or one of the five is missing | The element test fails the build | None | AC1 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a `document` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares a published or consumed event of this step, a second topic, an agent operation of its own or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the capability area are not the ones TSD S7 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the columns, the pack elements, the lists, the base, the topic, the queue and the schema are fixed by the sources |
| Valuable | Unblocks RWB-S7-E6015-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision teams on the same day |
| Estimable | One contract document, nine contract tables, eight fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the pack step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view and ACE data product is P1, of document is P5 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The pack element and its five elements are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with R-WO-05 and with legacy AC2
    Then the WriteOffPack element declares the case reference, the pack reference, the balance, the provision carried, the route history, the legal and asset state, the residual, the tax criteria version, the document reference and the state
    Then the five elements are named in the order R-WO-05 gives them and none of them is dropped, merged or renamed
    Then the element declares the amount written off as the balance it carries, and the pack carries no committee decision, no posting reference and no recovery
    Then the element test fails a build that adds an element R-WO-05 does not name or that drops one of the five

  Scenario: AC2 The write_off shape and the standard columns are fixed (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with TSD S7 T3.0 and T3.1
    Then the shape declares the columns of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id and amount are required, and decision_log_id, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after carry the flags TSD S7 T3.1 gives them
    Then the shape declares the standard record columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then state carries the route state PACK_PREPARED and the values of the WO machine are named, not enumerated as code constants
    Then the columns this step does not write are declared optional and attributed to the committee story and the posting story
    Then no property is added for the provision carried, the residual or the pack document, and those live in the pack element with the placeholder (GAP-3022)

  Scenario: AC3 The seven consumed rows are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case-facts and route-history read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage code, the state, the recovery history and the route history
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move PACK_PREPARED carrying the rule ID and its version
    Then the balance and asset-state read is declared as consumed from P1 rwb-source-data, with the balance, the legal and asset state and the as-of date of each product, and it is the DP-05 row of this key
    Then the document-index read and the pack document registration are declared as consumed from P5 rwb-document, with the document reference, type, source and storage reference, and no document content
    Then the pack run is declared as consumed from P10 rwb-agent, with the five pack elements and a service identity subject to the same role checks as a person (GAP-3022; ASM-5022)
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version and its 51 rules over 27 states
    Then the operation names of the seven rows are Not specified in the source documents (GAP-3022; ASM-5020) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no document property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The decision-record element and the rule version are declared (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S7 T2
    Then one decision record is declared per rule outcome with the case reference, the rule ID, the package version in force, the inputs reference with the as-of dates of the data products, the pack reference, the outcome, the case move and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the write_off row changes, and a failed write leaves it unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data
    Then the tax criteria version is declared as read from the owner's reference and recorded with the pack, and a pack without it is the MSG-S7-001 path

  Scenario: AC5 The rights, the messages and the screen fields of SCR-27 are fixed (new, D-RCV-60)
    Given the access and message sections of the baseline
    When they are compared with TSD S7 T6.1 and T6.2 and with the legacy permission table
    Then the capability area is Write-off and posting, right A is held by RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE, and right C by RW-WRITEOFF and RW-CREDITAD
    Then RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA and every other role and every SY-* service identity of TSD S7 T6.1 holds R
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition
    Then the screen fields of SCR-27 are declared read only: the pack, its five elements, the state and the document reference, with the case state and the document answered by their owners
    Then the document declares no write on SCR-27 and no officer task on the pack path

  Scenario: AC6 The eight fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation, the element or the row it serves
    Then the rwb-case fakes answer the facts, the route history and the recovery history of "RC-2026-000715" at POPULATION_PROPOSED, a case that has left the population, and the PACK_PREPARED move accepted and refused
    Then the rwb-source-data fake answers the balance and the asset state with as-of date "2026-11-30", a stale product with its date and no answer beyond 2 s
    Then the rwb-document fake answers the index and a registration reference, the rwb-agent fake the five pack elements and an incomplete content, and the rwb-decision fake the WO package at its version in force
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is declared twice (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, document, notice, proceeds, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then this baseline declares no REST operation provided by this legacy key, and it names POST /write-off-scans (API-S7-001) as RWB-S7-E6013-CON's and POST /write-offs/{writeOffId}/committee-decision (API-S7-002) as RWB-S7-E6018-CON's
    Then the write-off read that SCR-27 needs is declared as a placeholder because the Ownership Map carries no such operation (GAP-3022; ASM-5026)
    Then the document declares no published event, no consumed event, no second topic, no agent operation of its own and no Schedule, and the absence test fails a build that adds one (ASM-5025)

  Scenario: AC8 Every business rule of section 8 is traced to a criterion and a test (new, D-RCV-60)
    Given the business rules BR1 to BR14 of section 8
    When each rule is compared with the criteria of section 7 and the test cases of section 16
    Then each of BR1 to BR14 names at least one criterion and one test case, and the coverage paragraph of section 8 gives the same mapping
    Then the architecture rules BR12, BR13 and BR14 are guarded by the boundary and absence tests TC-S7-E6015-CON-05 and TC-S7-E6015-CON-06
    Then a rule with no criterion or no test fails the build

  Scenario: AC9 A consumed call that fails or does not answer changes nothing and is refused (new, D-RCV-60)
    Given a consumed row declared in AC3 that fails or does not answer within its 2 s budget
    When the pack step calls it
    Then the write_off row is not changed and no decision record is written
    Then the error envelope carries one message ID per condition, as AC5 requires
    Then the row is not retried by this service, and its breaker is the only protection (DP-11, ADR-020)
```

These nine criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6015-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The pack elements are the five of R-WO-05 and are not a business value: they are the rule's own vocabulary, and the baseline fixes their names and their optionality, never a threshold, a zone or a limit.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The pack is rwb-writeoff's, and the contract declares the `write_off` shape, the pack element and the lists of this service only | TSD S7 T3.1, T3.2; context pack ownership rows (table `write_off`) |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR3 | The ACE facts stay with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read (DP-05) | FSD S7 A2.3.2; legacy Data table rows DF-ACE-001 to DF-ACE-042 and DF-ACE-208 to DF-ACE-219; ASM-5020 |
| BR4 | The case facts and the case move are consumed and not written: the contract declares the two rows and no `recovery_case` property and no case write | ASM-5020; TSD S7 T4 |
| BR5 | The documents stay with rwb-document: the index and the registration are consumed rows, and no `document` property is declared | TSD S7 T3.1; ASM-5023 |
| BR6 | The pack run is a consumed row of rwb-agent and the baseline declares no agent operation of its own; DP-20 is recorded as an absent pattern. The pack is product behaviour the agent drafts under its contract; when the agent is unavailable a template fallback drafts the pack inside 60 seconds, and the call type is an open question with the P10 owner | R-WO-05 Systems column; ASM-5022; GAP-1811 |
| BR7 | No event of this step is declared: the service's `EV-24` `WriteOffApproved` is the committee story's, and the outbox library of DP-09 is an absent H row | TSD S7 T5.3; context pack event row; ASM-5025 |
| BR8 | This legacy key provides no REST operation: the two operations it names belong to RWB-S7-E6013-CON and RWB-S7-E6018-CON under the Ownership Map | Ownership rows of S7; TSD S7 T-A.1; legacy Endpoints |
| BR9 | A POST declares the `Idempotency-Key` and stores its answer; a read declares none | TSD S7 T-A.2 |
| BR10 | The vocabulary is closed: the pack elements, the state values and the tax criteria version are published as named values and read as reference data, and no value is a constant of the code | TSD S7 T3.2; FSD S7 BR-S7-003 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, an amount, a boolean, dates and a rule version only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR12 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR13 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR14 | The document lists only what rwb-writeoff owns; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |

**Coverage of the rules (DOR-RWB-S7-E6015-CON-4).** BR1: AC1, AC2 (TC-S7-E6015-CON-01, TC-S7-E6015-CON-02). BR2: AC4 (TC-E6-015-03, TC-S7-E6015-CON-04). BR3: AC3 (TC-E6-015-01, TC-S7-E6015-CON-03). BR4: AC3 (TC-E6-015-02, TC-S7-E6015-CON-03). BR5: AC3 (TC-S7-E6015-CON-03). BR6: AC3 (TC-E6-015-01, TC-S7-E6015-CON-03). BR7: AC7 (TC-S7-E6015-CON-05). BR8: AC7 (TC-S7-E6015-CON-05). BR9: AC5 (TC-E6-015-04). BR10: AC2 (TC-S7-E6015-CON-02). BR11: AC6 (TC-S7-E6015-CON-04). BR12: AC7 (TC-S7-E6015-CON-05). BR13: AC7 (TC-S7-E6015-CON-05). BR14: AC6, AC7 (TC-S7-E6015-CON-04, TC-S7-E6015-CON-06).

### 9. State transitions

The lifecycle of this document, not of a pack:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the shape, the seven consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-source-data, rwb-document, rwb-agent and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional pack element | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` or `document` property, a provided operation, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `POPULATION_PROPOSED` and `PACK_PREPARED` are route states of the WRITEOFF machine of TSD S7 T4, and this baseline fixes the vocabulary and moves no pack and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the seven consumed rows and the absent DP-04, DP-09 and DP-20 rows |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-source-data, rwb-document, rwb-agent, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the agent client and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Pack element | `WriteOffPack` with the case reference, the pack reference, the five elements of R-WO-05 — the balance, the provision carried, the route history, the legal and asset state and the residual — the tax criteria version, the document reference and the state |
| Write-off shape | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after`, with the standard record columns of TSD S7 T3.0 |
| Required flags | `id`, `case_id` and `amount` required; `decision_log_id`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` as TSD S7 T3.1 gives them |
| Lists | The state values of the WRITEOFF machine (TSD S7 T4) and the tax criteria version are the parameters read here, published as named values and read as reference data at their version under the reference-data contract of DP-06 and DP-07 |
| Event data | None of this step: no event is declared (§12.3) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Case, ACE and document facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, DF-ACE-001 to DF-ACE-042 and DF-ACE-208 to DF-ACE-219 of the P1 data products and DF-DOC-001 to DF-DOC-011 of `document` in P5, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7) |
| Consumed fields with no source | The operation names of the seven consumed rows, the properties of the provision carried, the residual and the document reference, and the write-off read SCR-27 needs: Not specified in the source documents (GAP-3022; ASM-5020, ASM-5023, ASM-5026) |

**BR Field ID (DOR-RWB-S7-E6015-CON-7).** The nine rows above carry no BR Field ID: Not specified in the source documents (DOR-RWB-S7-E6015-CON-7).

**Open question (GAP-1797).** The call type from S7 to the document hub for the pack document and its retention class is not in the connection matrix; the P5 owner states it.

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the element names, the five pack elements, the vocabulary of AC2 and the optionality rule of BR13. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. This legacy key owns no REST operation: the pack is prepared by the stage step of `WriteOffWorkflow` and answers the case, and the screen reads it through the gateway-bff composite route. The Ownership Map gives rwb-writeoff exactly two operations, and the two the legacy story lists are those: `POST /write-off-scans` (API-S7-001), declared on `/api/recovery/writeoff/v1` by RWB-S7-E6013-CON under DP-13, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002), declared by RWB-S7-E6018-CON. No write-off read exists in the map, so SCR-27's pack read carries a placeholder and the absence test of AC7 fails a build that claims a path here (GAP-3022; ASM-5026).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case-facts and route-history read (operation name Not specified in the source documents (GAP-3022; ASM-5020)) | `/api/recovery/case/v1` | P3 rwb-case | The facts, the route history, the recovery history and the state of the case; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3022; ASM-5020)) | rwb-case (P3) | P3 rwb-case | The move `PACK_PREPARED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The balance and asset-state data-product read (operation name Not specified in the source documents (GAP-3022; ASM-5020)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The balance of the case, the legal and asset state of its collateral and the as-of date of each product (DP-05); faked |
| The document-index read (operation name Not specified in the source documents (GAP-3022; ASM-5023)) | `/api/recovery/document/v1` | P5 rwb-document | The document reference, type, source and storage reference of the case, without content; faked |
| The pack document registration (operation name Not specified in the source documents (GAP-3022; ASM-5023)) | `/api/recovery/document/v1` | P5 rwb-document | The pack document of the case, answered with the document reference the pack carries; faked |
| The write-off pack run (operation name Not specified in the source documents (GAP-3022; ASM-5022)) | `/api/recovery/agent/v1` | P10 rwb-agent | The five pack elements of the case, under a service identity; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3022; ASM-5021)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-05 among its 51 rules over 27 states, the zone and the state vocabulary; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The seven rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3022; ASM-5020).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1`, and its event `EV-24`, which TSD S7 T5.3 names `WriteOffApproved`, is the committee approval's and therefore RWB-S7-E6018-APP's: the pack approves nothing and changes no book. This baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the event is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5025; GAP-3022).

#### 12.4 Events consumed

None. The service subscribes to rwb-payment's events in the recovery-after-charge-off steps (context pack connection matrix, row S7), not in the pack: no recovery exists before the write-off is posted. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case, the child of `CaseWorkflow`, continues-as-new at each stage end; workflow ID form Not specified in the source documents (CG-ALL-10907); start on JOB-16, the third working day after AceDataReady (R-WO-01); duplicate-start policy Not specified in the source documents (CG-ALL-10907) | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the pack step; its input, its signals and its outcome for the parent are declared, not built |
| `prepareWriteOffPack` | Activity, the one pack step | `rwb-writeoff` | The case reference, the cut-off date and the package in force in; the pack element, the rule ID with its package version, the document reference, the row reference and the case move out |

No child workflow for the case and none for the money exists in this service, no activity is registered by this story, and this step declares no activity on another queue: the evaluation runs inside `prepareWriteOffPack` on the package read from rwb-decision, which is where DP-04 and ADR-017 place the rules. The connection matrix gives S7 one Temporal call to P7 and no source names its operation; it is recorded, not declared (GAP-3022; ASM-5021).

#### 12.6 Schedules

None. The step runs from the case signal the parent forwards after the monthly population is built; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-16, the write-off scan, is the service's single Schedule and belongs to RWB-S7-E6013-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the case, its columns, its lists and its state; the table the pack element answers from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated signal and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `proceeds` (P8) are not owned by this baseline; it names them only as consumed answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts fake | The facts, the route history and the recovery history of `RC-2026-000715` at `POPULATION_PROPOSED`; a case that has left the population | AC3, AC6 |
| rwb-case case-move fake | The move `PACK_PREPARED` accepted, and a move refused | AC3, AC6 |
| rwb-source-data data-product fake | The balance and the asset state with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC3, AC6 |
| rwb-document fake | The index of the case and a registration answered with a document reference; an index with a missing type | AC3, AC6 |
| rwb-agent pack-run fake | The five pack elements of `RC-2026-000715`; an incomplete content; no answer beyond 2 s | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-05, its 51 rules over 27 states, the zone and the state vocabulary | AC1, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000715`, in its pack-prepared state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the seven consumed rows carry the placeholder until their owners confirm them (GAP-3022; ASM-5020).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 7 consumed | The case read and move answer, the data-product read, the document index and registration, the agent run and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `EV-24` `WriteOffApproved` is the committee story's; no consumed event of this step (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `WriteOffWorkflow` and `prepareWriteOffPack` on `rwb-writeoff`; no Schedule and no activity on another queue |
| File | None | No file is read, built or delivered here; the pack document is a document of rwb-document |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no pack, no case, no balance and no rule package. What it publishes is one contract document, nine contract tables and eight fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract, with no `v_ace_*` grant in this service | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row changes. DP-05 is the contract row of the balance and the asset state and the prohibition of a view read. DP-13 fixes the service base the two sibling operations sit on and declares no path of its own. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-09 and DP-20 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the outbox as an absent library row rather than an event of this step, and the agent run as a consumed row without the client row the pattern would add (GAP-3022; ASM-5021, ASM-5022, ASM-5025).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the agent client `C RWB-P10-TE013-CON` that DP-20 would add, the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add. The seven consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the pack element of AC1 with the five elements of R-WO-05 and the element test.
2. Write the `write_off` shape, its required flags and the standard columns of AC2, with the placeholder where a column is not this step's.
3. Record the seven consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the decision-record element and the tax criteria read of AC4 and validate them against the library schema.
5. Record the rights, the message set and the screen fields of AC5 against TSD S7 T6.1.
6. Publish the eight fakes of AC6 and the drift test.
7. Record the naming baseline, the two sibling operations and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml` with the pack element and the write-off shape, the vocabulary of the state values and the tax criteria version as published enumerations, the contract README rows for the seven consumed rows and their placeholders, and the eight fakes of 12.8.

**Done when.** The contract document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes a pack without the tax criteria version, which the app story raises as VR-S7-003-1 (X4) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the capability area declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its pack-prepared state through the gateway-bff composite route (DP-19). The empty, loading, error and no-access states are Not specified in the source documents (CG-ALL-10911), since Screen Specifications v1 section SCR-27 gives none of the four. The route calls rwb-writeoff for the pack and its five elements, rwb-case for the case and its route state and rwb-document for the pack document; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": the pack-prepared state is this step's reading of "proposed", the scan state is RWB-S7-E6013-APP's and the two committee states are RWB-S7-E6017-APP's and RWB-S7-E6018-APP's. The write-off read the route needs has no operation in the Ownership Map and carries a placeholder (GAP-3022; ASM-5026).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-015-01 | AC1, AC3 | Contract | The population, the case and the pack content on the fakes; the contract half answers the pack element and the case and agent rows |
| TC-E6-015-02 | AC2, AC3 | Contract | Case `RC-2026-000715` at `POPULATION_PROPOSED`; the contract half answers the write-off shape, the standard columns and the `PACK_PREPARED` move shape |
| TC-E6-015-03 | AC4, AC7 | Contract | The decision-record stub stopped and a missing tax criteria version; the contract half answers the MSG-P7-003 and MSG-S7-001 paths and the absence tests |
| TC-E6-015-04 | AC5 | Contract | A role without the Write-off and posting right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-015-05 | AC4, AC5 | Contract | RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA; the contract half answers the rights and the decision element |
| TC-S7-E6015-CON-01 | AC1 | Contract | The pack element validates with its ten properties, the five R-WO-05 elements in order and no invented element |
| TC-S7-E6015-CON-02 | AC2 | Contract | The write-off shape validates with its eleven columns, its required flags and its seven standard columns |
| TC-S7-E6015-CON-03 | AC3 | Contract | The seven consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-`document` boundary |
| TC-S7-E6015-CON-04 | AC4, AC6 | Contract | The decision-record element matches the library schema; the eight fakes match the document and a drifted fake fails the build |
| TC-S7-E6015-CON-05 | AC5, AC7 | Contract | The rights, the screen fields, the naming baseline, the tables owned, and the absence of a provided operation, a published event, a consumed event, a second topic and a Schedule |
| TC-S7-E6015-CON-06 | AC7 | Contract | The four tables of §12.7 owned by this baseline at their boundary; a consumed table outside §12.7 (DP-01) fails the build |
| TC-S7-E6015-CON-07 | AC8 | Contract | The business rules BR1 to BR14 each traced to a criterion and a test; a rule with no criterion or no test fails the build |
| TC-S7-E6015-CON-08 | AC9 | Contract | A consumed row that fails and a consumed row that gives no answer within 2 s; the contract half answers the refusal, the unchanged write_off row, no decision record and no retry |

The five legacy cases are those of RWB-E6-015 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6015-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The eight cases `TC-S7-E6015-CON-01` to `-08` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the pack elements, the zone, the state values and the tax criteria version stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, a boolean, dates and a rule version only, and every example is synthetic.
- The ACE facts stay with rwb-source-data, the case with rwb-case and the documents with rwb-document: the document declares no `v_ace_*` path, no `recovery_case` property, no `document` property and no write on any of them (BR3, BR4, BR5).
- The money stays with rwb-payment and the ledger with rwb-decision: the document declares no posting, no proceeds, no decision row and no rule row.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document declares no provided operation of this legacy key; the two operations it names are attributed to their stories and a consumed operation is always described as consumed and faked (BR8, BR14).
- No retired element is reintroduced: the absence tests fail a build that declares a published event, a consumed event, a second topic, an agent operation of its own, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the agent client and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly; the contract fixes the element, the shape and the rows on which the pack is built (FSD S7 Requirements served), and TSD S7 T8 maps the same id to FEAT-WOF-01, a conflict recorded in GAP-3022 | The `WriteOffPack` element, the `write_off` shape and the seven consumed rows | TC-E6-015-01, TC-S7-E6015-CON-01, TC-S7-E6015-CON-02, TC-S7-E6015-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6015-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the committee story's | TC-S7-E6015-CON-05 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The package row and the rule version | TC-S7-E6015-CON-01, TC-S7-E6015-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed rows with their budget and breaker | TC-S7-E6015-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6015-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-015, disposition Split (rework); feature FEAT-WOF-03 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6015-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-015; FSD S7 Write-off and recovery v3 A2.3, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.0, T3.1, T3.2, T4, T5.3, T6.1, T6.2 and T-A; Business Rules and Routing Logic v4 row R-WO-05 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6015-CON-01 to -05 |
| Feature and screens | FEAT-WOF-03, SCR-27 Write-off proposal |
| Rules | R-WO-05, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-014, ADR-015, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the pack step, the evaluation of R-WO-05, the decision record, the row, the document registration and the case-move answer: RWB-S7-E6015-APP.
- The case of record, its route states, the case facts and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5020).
- The ACE data products: rwb-source-data (P1) (ASM-5020). The documents: rwb-document (P5) (ASM-5023). The pack run: rwb-agent (P10) (ASM-5022).
- The authoring, testing, approval and versioning of the WO package, of the tax criteria version and of R-WO-05: rwb-decision (P7) (ASM-5021).
- The monthly scan and its population: RWB-S7-E6013-CON and RWB-S7-E6013-APP; the tax criteria: RWB-S7-E6014-APP; the removal of a case: RWB-S7-E6016-APP.
- The committee routing and the pack check of R-WO-09: RWB-S7-E6017-CON and RWB-S7-E6017-APP. The committee decision, R-WO-15 and `EV-24`: RWB-S7-E6018-CON and RWB-S7-E6018-APP.
- The posting, the provision release and the post charge-off recovery: the later S7 stories, with the money in rwb-payment (P8).
- The gateway-bff composite route, the screen field list of SCR-27 and the write-off read the map does not carry: RWB-PLT-N001-CON (ASM-5026).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
